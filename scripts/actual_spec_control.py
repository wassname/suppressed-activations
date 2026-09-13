# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Actual-spec h1 diagnostic: ONE production row (task 1230, condition
v25imported_h1_C1.5, common-basis-earlyloc batch) run through the REAL
run_with_bundle construction to CAPTURE the actual built common_specs, then the same
corrected cached-vs-uncached teacher-forced comparison (prefill + 5 cached decode
steps) reusing those captured specs — joining bank construction to the hook/cache
path with the real perturbation. Random-basis controls are NOT used here.

Captured from production (observed, not rederived): common_specs, positions,
source_position, strength, source input_ids. Fixed 2x-null tolerance (no widening);
failure saves first-divergence tensors. -- PI[glm-5p3-flash]"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
torch.set_grad_enabled(False)

sys_path = str(Path(__file__).resolve().parents[1])
sys_path in sys.path or sys.path.insert(0, sys_path)
import scripts.oat_sweep as sweep
from scripts.runtime_controls import cached_generate, forward_final, hidden_pairs

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "common_basis_earlyloc_batch.json"
N_GEN = 6
TOL_FACTOR = 2.0  # fixed in advance, same as runtime_controls


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    condition = json.loads(BATCH.read_text())[0]  # v25imported_h1_C1.5, index 0
    capture: dict = {}

    orig_hooks = sweep.intervention_hooks

    def spy_hooks(*args, **kw):
        hooks = orig_hooks(*args, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs"):
            capture.update(args=args, kwargs={k: v for k, v in kw.items() if k != "record"},
                           spec=kw["common_specs"], positions=kw["positions"],
                           source_position=kw["source_position"], strength=kw["strength"],
                           blocks_to_hook=kw.get("blocks_to_hook"),
                           target_residuals_shape=tuple(args[2].shape))
        return hooks

    orig_gen = sweep.generate_with_first_logits
    pending_ids = []

    def spy_gen(model, tok, ids, *a, **kw):
        pending_ids.append(ids)
        return orig_gen(model, tok, ids, *a, **kw)

    sweep.intervention_hooks = spy_hooks
    sweep.generate_with_first_logits = spy_gen
    try:
        bundle = sweep.load_bundle()
        out_dir = ROOT / "out" / f"2026-09-13_actualspec-h1-diag-{time.strftime('%H%M%S')}"
        out_dir.mkdir(parents=True, exist_ok=False)
        run_kwargs = sweep.strip_spec_metadata(condition)
        run_kwargs.pop("max_new_tokens", None)  # keep production default path intact
        sweep.run_with_bundle(bundle, out_dir, extraction_cache={"revision": bundle["revision"]},
                              batch_spec={"batch_file": str(BATCH), "index": 0,
                                          "spec": dict(condition)},
                              expected_detector_layers=condition.get("expected_detector_layers"),
                              **run_kwargs)
    finally:
        sweep.intervention_hooks = orig_hooks
        sweep.generate_with_first_logits = orig_gen

    assert "spec" in capture, "production run never built common_replace specs"
    result = {"condition": condition["expected_condition"], "output_dir": str(out_dir),
              "code_sha256": {p: sha(p) for p in ("scripts/oat_sweep.py", "scripts/demo.py",
                                                  "scripts/prompt.py",
                                                  "suppressed_activation_subspace.py")},
              "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                             cwd=ROOT, check=True, text=True,
                                             capture_output=True).stdout.strip(),
              "captured_positions": capture["positions"],
              "captured_source_position": capture["source_position"],
              "captured_strength": capture["strength"],
              "captured_blocks_to_hook": capture["blocks_to_hook"],
              "captured_target_residuals_shape": capture["target_residuals_shape"],
              "batch_flags": {k: condition[k] for k in (
                  "common_basis", "expected_common_selector", "expected_common_removal",
                  "expected_intervention_layer", "expected_xdepth_anchor_layer",
                  "expected_xdepth_norm_from_layer", "expected_detector_layers", "rank")
                  if k in condition}}
    spec = capture["spec"]
    L = next(iter(spec))
    result["actual_basis_rank"] = int(spec[L]["src"].shape[-1])
    result["spec_src_shape"] = list(spec[L]["src"].shape)
    result["spec_decode_src_shape"] = list(spec[L]["decode_src"].shape)

    model, tok = bundle["model"], bundle["tokenizer"]
    from scripts.prompt import assistant_prefill_input_ids
    ids_src = assistant_prefill_input_ids(
        tok, condition["source_prompt"], device=next(model.parameters()).device,
        instruction=condition["prefill_instruction"])["input_ids"]
    match = [c for c in pending_ids if c.shape == ids_src.shape and bool((c == ids_src).all())]
    assert match, "no production generation call used the rendered source prompt"
    ids = match[0]
    c_end = capture["source_position"] + 1
    assert c_end >= capture["positions"], "captured positions exceed prompt"
    blocks = model.model.layers
    fn = model.model.norm

    # null: no-hook cached generation vs full-history recompute of the same tokens
    gen_cl, rows_cl, fin_cl = cached_generate(model, tok, ids, blocks, {}, N_GEN)
    ids_cl = torch.cat([ids, torch.tensor([gen_cl["token_ids"]], device=ids.device)], dim=1)
    logits_cl, fin_cl_ref = forward_final(model, ids_cl, {})
    rows_cl_ref = logits_cl[c_end - 1:c_end - 1 + len(rows_cl)]
    rel = lambda a, b: [float((a[j] - b[j]).abs().max() / (b[j].std() + 1e-9)) for j in range(len(a))]
    clean_step_delta = rel(rows_cl, rows_cl_ref)
    clean_hidden = [(float((a - b).abs().max()),
                     float((a - b).abs().max() / (b.std() + 1e-9)), name)
                    for a, b, name in hidden_pairs(fin_cl, fin_cl_ref, c_end, len(rows_cl))]
    tol_rel = max(1e-3, TOL_FACTOR * max(clean_step_delta))
    tol_hidden = max(1e-3, TOL_FACTOR * max(r for _, r, _ in clean_hidden))
    result["null_step_logit_rel"] = clean_step_delta
    result["null_hidden_abs_rel"] = clean_hidden
    result["tol_rel"] = tol_rel
    result["tol_hidden_rel"] = tol_hidden
    print(f"null: logit rel per step {['%.2e' % d for d in clean_step_delta]}, "
          f"hidden rel max {max(r for _, r, _ in clean_hidden):.2e}; "
          f"tol = {TOL_FACTOR}x max null (fixed) = {tol_rel:.2e} / {tol_hidden:.2e}")

    # C0: the ACTUAL spec at strength 0 must be bitwise inert (exact production args)
    hooks0 = sweep.intervention_hooks(*capture["args"],
                                      **{**capture["kwargs"], "strength": 0.0})
    with sweep.layer_hooks(blocks, hooks0), torch.no_grad():
        out0 = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    clean_logits, _ = forward_final(model, ids, {})
    assert torch.equal(out0, clean_logits[c_end - 1]), "actual-spec C0 changed the logits"
    result["C0_bitwise"] = True
    print("C0 with actual spec: bitwise OK")

    # intervened cached generation through the production path with the ACTUAL spec
    record = {}
    hooks = sweep.intervention_hooks(*capture["args"],
                                     **{**capture["kwargs"], "record": record})
    gen, rows, fin = cached_generate(model, tok, ids, blocks, hooks, N_GEN)
    n = len(gen["token_ids"])
    assert record[L]["decode_steps"] == n - 1 and n - 1 >= 3, \
        f"cached decode did not actually run: {record[L]['decode_steps']}"
    result["decode_steps"] = record[L]["decode_steps"]
    result["generated_token_ids"] = gen["token_ids"]
    result["replacement_trace"] = record[L].get("replacement_trace", [])
    result["prefill_residual_norm"] = record[L]["residual_norm"]
    result["prefill_perturbation_norm"] = record[L]["perturbation_norm"]
    result["relative_perturbation_by_position"] = record[L]["relative_perturbation_by_position"]

    # uncached reference: teacher-force the same tokens; ACTUAL basis, prompt-last3 rows
    # + frozen production decode vector on every generated position
    ids_full = torch.cat([ids, torch.tensor([gen["token_ids"]], device=ids.device)], dim=1)
    spec_ext = {L: {"src": torch.cat([spec[L]["src"], spec[L]["decode_src"].expand(n, -1, -1)], 0),
                    "donor_proj": torch.cat([spec[L]["donor_proj"],
                                             spec[L]["decode_proj"].expand(n, -1)], 0),
                    "decode_src": spec[L]["decode_src"], "decode_proj": spec[L]["decode_proj"],
                    "donor_U": spec[L]["donor_U"]}}
    hooks_ext = sweep.intervention_hooks(*capture["args"], **{**capture["kwargs"],
                                         "common_specs": spec_ext,
                                         "positions": capture["positions"] + n,
                                         "source_position": c_end + n - 1})
    logits_full, fin_ref = forward_final(model, ids_full, hooks_ext)
    rows_ref = logits_full[c_end - 1:c_end - 1 + n]

    step_delta = rel(rows, rows_ref)
    hidden = [(float((a - b).abs().max()),
               float((a - b).abs().max() / (b.std() + 1e-9)), name)
              for a, b, name in hidden_pairs(fin, fin_ref, c_end, n)]
    argmax_match = [int(rows[j].argmax()) == int(rows_ref[j].argmax()) for j in range(n)]
    step_abs = [float((rows[j] - rows_ref[j]).abs().max()) for j in range(n)]
    top2 = lambda row: float(row.topk(2).values[0] - row.topk(2).values[1])
    result.update(step_logit_delta_rel=step_delta, step_abs_delta=step_abs,
                  step_hidden_abs_rel=hidden,
                  per_step_abs_null_vs_control={f"step{j}": [
                      float((rows_cl[j] - rows_cl_ref[j]).abs().max()), step_abs[j]]
                      for j in range(n)},
                  cached_top2_gap=[top2(r) for r in rows],
                  ref_top2_gap=[top2(r) for r in rows_ref],
                  step_argmax_match=argmax_match,
                  first_token_logit_shift_vs_clean=float((rows[0] - clean_logits[c_end - 1]).abs().max()))

    failures = []
    try:
        for j, d in enumerate(step_delta):
            assert d <= tol_rel, f"step {j}: rel {d:.3e} > tol {tol_rel:.3e}"
        for ab, r, name in hidden:
            assert r <= tol_hidden, f"{name}: rel {r:.3e} > tol {tol_hidden:.3e}"
        tie_flip = [j for j in range(n) if not argmax_match[j] and result["cached_top2_gap"][j] <= step_abs[j]]
        result["argmax_tie_flips"] = tie_flip
        for j in range(n):
            assert argmax_match[j] or j in tie_flip, \
                f"argmax differs beyond tie numerics at step {j}: gap {result['cached_top2_gap'][j]:.3e} vs delta {step_abs[j]:.3e}"
        first_shift = result["first_token_logit_shift_vs_clean"]
        clean_abs0 = float((rows_cl[0] - rows_cl_ref[0]).abs().max())
        assert first_shift > max(1e-3, 10 * clean_abs0), \
            f"intervention undetectable above numerics: shift {first_shift:.3e} vs null {clean_abs0:.3e}"
        result["outcome"] = "PASS"
        print(f"ACTUAL-SPEC CONTROL PASS (n={n}, decode_steps={n - 1}): logit rel max "
              f"{max(step_delta):.2e} (null {max(clean_step_delta):.2e}), hidden rel max "
              f"{max(r for _, r, _ in hidden):.2e} (null {max(r for _, r, _ in clean_hidden):.2e}), "
              f"argmax {sum(argmax_match)}/{n}, first-token shift {first_shift:.2e}")
    except AssertionError as e:
        j = next((j for j in range(n) if step_delta[j] > tol_rel), 0)
        torch.save({"ids_full": ids_full, "rows_cached": rows[j].cpu(),
                    "rows_ref": rows_ref[j].cpu(), "spec": spec, "step": j,
                    "result": result}, out_dir / "first_divergence.pt")
        result["outcome"] = f"FAILED: {e}"
        print(f"ACTUAL-SPEC CONTROL FAIL: {e} | first-divergence tensors: "
              f"{out_dir / 'first_divergence.pt'}")
    (out_dir / "actual_spec_control_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"result: {out_dir / 'result.json'}")


if __name__ == "__main__":
    main()
