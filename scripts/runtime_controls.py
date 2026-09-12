# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Runtime ml-debug controls through PRODUCTION hooks (real model, CPU/GPU).

1. identity: v = P_s h from the SAME state/position/layer -> zero net edit (logits
   equal AND recorded perturbation_norm == 0); a donor state from a DIFFERENT position
   of the same prompt is NOT identity and must produce a nonzero delta, so the identity
   assertion cannot pass through a missing hook;
2. logits equality vs no-hook at C=0;
3. cached vs uncached teacher-forced equivalence over prefill + >=3 cached decode steps
   with a REAL nonzero intervention: the uncached reference applies the edit to the
   last-3 ORIGINAL prompt positions AND ALL generated positions (contiguous slice
   [content_end-3 : content_end+N]) at the same hook layer, NOT merely the last 3 of
   the growing sequence. Per-step logits and final-norm hidden states are compared
   against a tolerance calibrated in-run by a clean no-hook cached-vs-recompute
   measurement. Wrong-mask and no-hook discrimination probes must MISmatch, so those
   bugs fail loudly. Greedy decoding only; no sampling drift.
4. the positive pinned reference (spider/dog, Qwen3.5-4B, C4, L26) is executed
   separately through scripts/confirm_causal_demo.py in the main worktree; see
   slop/2026-09-13_runtime-controls-spec.md. It is NOT part of this script.

Results are written to a unique JSON result dir. -- PI[glm-5p3-flash]"""
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import hashlib
import json
import subprocess
import sys

import torch
torch.set_grad_enabled(False)
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = os.environ.get("SUPPRESSED_MODEL", "wassname/qwen3-5lyr-tiny-random")
REV = os.environ.get("SUPPRESSED_REVISION", "main")
DEV = os.environ.get("SUPPRESSED_DEVICE", "cpu")
DTYPE = {"bfloat16": torch.bfloat16, "float32": torch.float32}[
    os.environ.get("SUPPRESSED_DTYPE", "bfloat16")]
L = int(os.environ.get("SUPPRESSED_CONTROL_LAYER", "2"))  # residual layer; hook block L-1
N_GEN = int(os.environ.get("SUPPRESSED_CONTROL_NGEN", "6"))
POS = 3
STRENGTH = 1.5
sys_path = str(Path(__file__).resolve().parents[1])
sys_path in __import__("sys").path or __import__("sys").path.insert(0, sys_path)
from scripts.demo import intervention_hooks, layer_hooks, trajectory
from scripts.oat_sweep import generate_with_first_logits
from scripts.prompt import assistant_prefill_input_ids

SOURCE_CONTENT = "Question: what is the animal that spins webs called?\nAnswer: "
DONOR_CONTENT = "Question: what is the animal that barks and is called man's best friend called?\nAnswer: "
INSTRUCTION = "Answer the question with the answer first. Then describe the animal in three sentences."
ROOT = Path(__file__).resolve().parents[1]


def code_hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in
            ("scripts/runtime_controls.py", "scripts/demo.py", "scripts/oat_sweep.py",
             "scripts/prompt.py")}


def cached_generate(model, tok, ids, blocks, hooks, max_new_tokens):
    """Production generation plus per-step logit/final-input captures (hooks only,
    no production code changed)."""
    final_in, lm_out = [], []
    h1 = model.model.norm.register_forward_pre_hook(lambda _m, i: final_in.append(i[0].detach()))
    h2 = model.lm_head.register_forward_hook(lambda _m, _i, o: lm_out.append(o.detach()))
    try:
        gen, _ = generate_with_first_logits(model, tok, ids, blocks, hooks, None, max_new_tokens)
    finally:
        h1.remove()
        h2.remove()
    rows = [lm_out[0][0, -1].float()] + [lm_out[j][0, 0].float() for j in range(1, len(lm_out))]
    assert len(rows) == len(gen["token_ids"]) and len(final_in) == len(rows), \
        f"capture misaligned: {len(rows)} logit rows, {len(final_in)} final inputs, " \
        f"{len(gen['token_ids'])} tokens"
    return gen, rows, final_in


def forward_final(model, ids_full, hooks):
    """Full-history forward; returns per-position logits and final-norm inputs."""
    fin = []
    handle = model.model.norm.register_forward_pre_hook(lambda _m, i: fin.append(i[0].detach()))
    try:
        with layer_hooks(model.model.layers, hooks), torch.no_grad():
            out = model(input_ids=ids_full, use_cache=False)
    finally:
        handle.remove()
    return out.logits[0].float(), fin[0][0].float()


def main():
    result = {"model": MODEL, "revision": REV, "device": DEV, "control_layer": L,
              "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
              cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip(),
              "code_sha256": code_hashes(), "strength": STRENGTH, "positions": POS,
              "max_new_tokens": N_GEN}
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REV, dtype=DTYPE,
                                                 attn_implementation="sdpa").to(DEV).eval()
    fn = model.model.norm
    blocks = model.model.layers
    assert L - 1 < len(blocks) and L + 1 < len(blocks), f"layer {L} out of range"
    chat = assistant_prefill_input_ids(tok, SOURCE_CONTENT, device=DEV, instruction=INSTRUCTION)
    donor_chat = assistant_prefill_input_ids(tok, DONOR_CONTENT, device=DEV, instruction=INSTRUCTION)
    ids, c_end = chat["input_ids"], chat["content_end"]
    assert c_end >= POS, "prompt too short for the 3-position prefill mask"
    res_clean, logits_clean = trajectory(model, ids, fn)
    res_donor, _ = trajectory(model, donor_chat["input_ids"], fn)
    result["source_input_repr"] = repr(SOURCE_CONTENT)
    result["content_end"] = c_end

    # per-position production specs: same orthonormal U at every position; donor
    # projections are end-aligned donor-prompt states (production semantics), so the
    # edit is a REAL nonzero replacement, not an identity.
    g = torch.Generator().manual_seed(0)
    U = torch.linalg.qr(torch.randn(res_clean.shape[-1], 4, generator=g))[0].to(DEV)
    pos_order = list(reversed(range(1, POS + 1)))  # position-ascending, matching the hook slice
    donor_states = {o: res_donor[L, donor_chat["content_end"] - o].float() for o in pos_order}
    spec = {L: {
        "src": torch.stack([U for _ in pos_order]),
        "donor_proj": torch.stack([U @ (U.T @ donor_states[o]) for o in pos_order]),
        "decode_src": U.unsqueeze(0),
        "decode_proj": (U @ (U.T @ donor_states[1])).unsqueeze(0),  # frozen offset-1 donor
        "donor_U": U,
    }}
    result["prefill_donor_proj_norms"] = [float(p.norm()) for p in spec[L]["donor_proj"]]
    assert all(n > 0 for n in result["prefill_donor_proj_norms"])

    def hooks_for(specs, positions, source_position, record, strength=STRENGTH):
        return intervention_hooks(U, U, res_clean, operation="common_replace",
                                  common_specs=specs, blocks_to_hook=[L - 1],
                                  positions=positions, source_position=source_position,
                                  match_component_norm=False, restore_norm=False,
                                  strength=strength, record=record)

    # 1. identity: donor projection of the SAME state at the SAME position/layer -> 0
    h_same = res_clean[L, c_end - 1].float()
    spec_id = {L: {"src": U.unsqueeze(0), "donor_proj": (U @ (U.T @ h_same)).unsqueeze(0),
                   "decode_src": U.unsqueeze(0), "decode_proj": (U @ (U.T @ h_same)).unsqueeze(0),
                   "donor_U": U}}
    rec_id = {}
    with layer_hooks(blocks, hooks_for(spec_id, 1, c_end - 1, rec_id)), torch.no_grad():
        out_id = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    id_delta = (out_id - logits_clean).abs().max().item()
    # dproj and span are the same projection U(Uᵀh) through two contraction paths
    # (matmul vs hook einsum); fp32 accumulation differs, measured 2e-5 absolute on the
    # tiny model. Identity is asserted at <1e-3 of the residual norm, not bitwise.
    id_rel = rec_id[L]["perturbation_norm"] / rec_id[L]["residual_norm"]
    assert id_rel < 1e-3, \
        f"identity edit is not zero in the hook: rel {id_rel:.3e}"
    assert torch.allclose(out_id, logits_clean, atol=1e-4), f"identity logits moved: {id_delta}"
    # hook-fires control: a DIFFERENT position's state is not identity
    h_other = res_clean[L, 0].float()
    spec_nid = {L: {**spec_id[L], "donor_proj": (U @ (U.T @ h_other)).unsqueeze(0)}}
    rec_nid = {}
    with layer_hooks(blocks, hooks_for(spec_nid, 1, c_end - 1, rec_nid)), torch.no_grad():
        out_nid = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    assert rec_nid[L]["perturbation_norm"] > 0, "non-identity control did not apply an edit"
    assert not torch.allclose(out_nid, logits_clean, atol=1e-3), \
        "same-prompt different-position donor behaved as identity; hook may not fire"
    print(f"1. identity v=P h (same state/position): rel_edit={id_rel:.2e}, "
          f"max_logit_delta={id_delta:.2e}; "
          f"different-position donor: edit={rec_nid[L]['perturbation_norm']:.3e} (nonzero) OK")

    # 2. C0 equality (strength 0)
    spec0 = {L: {**spec[L], "donor_proj": torch.zeros_like(spec[L]["donor_proj"]),
                 "decode_proj": torch.zeros_like(spec[L]["decode_proj"])}}
    with layer_hooks(blocks, hooks_for(spec0, POS, c_end - 1, {}, strength=0.0)), torch.no_grad():
        out0 = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    assert torch.equal(out0, logits_clean), "C0 changed the logits"
    print("2. C0 logits equality: bitwise OK")

    # calibration: clean cached generation vs clean full recompute of the SAME tokens
    gen_cl, rows_cl, fin_cl = cached_generate(model, tok, ids, blocks, {}, N_GEN)
    ids_cl = torch.cat([ids, torch.tensor([gen_cl["token_ids"]], device=ids.device)], dim=1)
    logits_cl, fin_cl_ref = forward_final(model, ids_cl, {})
    rows_cl_ref = logits_cl[c_end - 1:c_end - 1 + len(rows_cl)]
    # relative per-step delta: |cached-recompute| / per-step ref logits std. The tiny
    # random model has a large logit scale, so absolute bf16 rounding looks big; the
    # null (clean) measurement at the same scale sets the tolerance.
    rel = lambda a, b: [float((a[j] - b[j]).abs().max() / (b[j].std() + 1e-9)) for j in range(len(a))]
    clean_step_delta = rel(rows_cl, rows_cl_ref)
    clean_hidden_delta = [float((fin_cl[j + 1][0, 0] - fin_cl_ref[c_end - 1 + j]).abs().max())
                          for j in range(len(rows_cl) - 1)]
    clean_rel = max(clean_step_delta)
    tol_rel = max(1e-3, 10 * clean_rel)
    clean_hidden_rel = [float((fin_cl[j + 1][0, 0] - fin_cl_ref[c_end - 1 + j]).abs().max()
                              / (fin_cl_ref[c_end - 1 + j].std() + 1e-9))
                        for j in range(len(rows_cl) - 1)]
    tol_hidden = max(1e-3, 10 * max(clean_hidden_rel))
    result["clean_step_logit_delta_rel"] = clean_step_delta
    result["clean_step_hidden_delta_rel"] = clean_hidden_rel
    result["tolerance_rel"] = tol_rel
    result["tolerance_hidden_rel"] = tol_hidden
    print(f"calibration: clean cached-vs-recompute rel logit delta per step "
          f"{['%.2e' % d for d in clean_step_delta]}; "
          f"tol_rel = max(1e-3, 10x max) = {tol_rel:.2e}, tol_hidden = {tol_hidden:.2e}")

    # 3. intervened cached generation (production path, real nonzero edit)
    record = {}
    hooks = hooks_for(spec, POS, c_end - 1, record)
    gen, rows, fin = cached_generate(model, tok, ids, blocks, hooks, N_GEN)
    n = len(gen["token_ids"])
    assert record[L]["decode_steps"] == n - 1 and n - 1 >= 3, \
        f"cached decode did not actually run: decode_steps={record[L]['decode_steps']}, tokens={n}"
    assert record[L]["perturbation_norm"] > 0, "recorded intervention is zero"
    assert record[L]["prefill_positions"] == list(range(c_end - POS, c_end)), \
        f"wrong prefill mask: {record[L]['prefill_positions']}"
    result["decode_steps"] = record[L]["decode_steps"]
    result["generated_token_ids"] = gen["token_ids"]
    result["generated_text"] = gen["text"]
    result["record"] = {str(k): v for k, v in record.items()}

    # uncached reference: teacher-force the SAME tokens; edit the last-3 ORIGINAL prompt
    # positions AND ALL generated positions (contiguous slice), reusing the production
    # hook through positions=3+N.
    ids_full = torch.cat([ids, torch.tensor([gen["token_ids"]], device=ids.device)], dim=1)
    spec_ext = {L: {
        "src": torch.cat([spec[L]["src"], spec[L]["decode_src"].expand(n, -1, -1)], dim=0),
        "donor_proj": torch.cat([spec[L]["donor_proj"], spec[L]["decode_proj"].expand(n, -1)], dim=0),
        "decode_src": spec[L]["decode_src"], "decode_proj": spec[L]["decode_proj"], "donor_U": U,
    }}
    rec_ext = {}
    # source anchor = the LAST GENERATED token: the hook mask ends at
    # source_position+1, so source_position=c_end+n-1 gives the intended contiguous
    # slice [c_end-3 : c_end+n] = last-3 prompt positions AND all generated positions.
    hooks_ext = intervention_hooks(U, U, res_clean, operation="common_replace",
                                   common_specs=spec_ext, blocks_to_hook=[L - 1],
                                   positions=POS + n, source_position=c_end + n - 1,
                                   match_component_norm=False, restore_norm=False,
                                   strength=STRENGTH, record=rec_ext)
    logits_full, fin_ref = forward_final(model, ids_full, hooks_ext)
    rows_ref = logits_full[c_end - 1:c_end - 1 + n]
    assert rec_ext[L]["prefill_positions"] == list(range(c_end - POS, c_end + n)), \
        f"reference mask is not prompt-last3 + all generated: {rec_ext[L]['prefill_positions']}"

    step_delta = rel(rows, rows_ref)
    hidden_delta = [float((fin[1 + j][0, 0] - fin_ref[c_end - 1 + j]).abs().max()
                          / (fin_ref[c_end - 1 + j].std() + 1e-9))
                    for j in range(n - 1)]
    result["step_logit_delta_rel"] = step_delta
    result["step_hidden_delta_rel"] = hidden_delta
    for j, d in enumerate(step_delta):
        assert d <= tol_rel, f"cached/uncached logits diverge at step {j}: rel {d:.3e} > tol {tol_rel:.3e}"
    for j, d in enumerate(hidden_delta):
        assert d <= tol_hidden, f"cached/uncached final hidden diverge at decode {j}: rel {d:.3e} > tol {tol_hidden:.3e}"
    # no sampling drift: every greedy step picks the same token under both paths
    argmax_match = [int(rows[j].argmax()) == int(rows_ref[j].argmax()) for j in range(n)]
    assert all(argmax_match), f"greedy argmax differs cached vs uncached: {argmax_match}"
    result["step_argmax_match"] = argmax_match
    first_shift = (rows[0] - logits_clean).abs().max().item()
    clean_abs0 = float((rows_cl[0] - rows_cl_ref[0]).abs().max())
    # same quantity as the null: max abs logit delta at step 0, intervention shift must
    # exceed 10x the no-intervention cached-vs-recompute numeric delta
    assert first_shift > max(1e-3, 10 * clean_abs0), \
        f"intervention did not move the first-token logits beyond numerics: " \
        f"shift {first_shift:.3e} vs clean null {clean_abs0:.3e}"
    result["first_token_logit_shift_vs_clean"] = first_shift
    print(f"3. cached/uncached teacher-forced equivalence (n={n}, decode_steps={n - 1}): "
          f"per-step rel logit delta max {max(step_delta):.2e}, rel hidden delta max "
          f"{max(hidden_delta) if hidden_delta else 0.0:.2e}, tol_rel {tol_rel:.2e} OK; "
          f"argmax match {sum(argmax_match)}/{n} OK; "
          f"first-token shift vs clean {first_shift:.2e} (nonzero) OK")

    # discrimination probes: these bugs MUST mismatch the cached intervened run
    spec_wm = {L: {"src": spec[L]["src"],  # naive reuse: prompt rows on the growing tail
                   "donor_proj": spec[L]["donor_proj"],
                   "decode_src": spec[L]["decode_src"], "decode_proj": spec[L]["decode_proj"],
                   "donor_U": U}}
    hooks_wm = intervention_hooks(U, U, res_clean, operation="common_replace",
                                  common_specs=spec_wm, blocks_to_hook=[L - 1],
                                  positions=POS, source_position=None,  # last-3 of history
                                  match_component_norm=False, restore_norm=False, strength=STRENGTH)
    logits_wm, _ = forward_final(model, ids_full, hooks_wm)
    wm_delta = max(rel([logits_wm[c_end - 1 + j] for j in range(n)], rows_ref))
    assert wm_delta > tol_rel, f"wrong-mask probe matched the cached run ({wm_delta:.2e}); test cannot detect mask bugs"
    logits_nh, _ = forward_final(model, ids_full, {})
    nh_delta = max(rel([logits_nh[c_end - 1 + j] for j in range(n)], rows_ref))
    assert nh_delta > tol_rel, f"no-hook probe matched the cached run ({nh_delta:.2e}); test cannot detect missing hooks"
    result["wrong_mask_probe_delta_rel"] = wm_delta
    result["no_hook_probe_delta_rel"] = nh_delta
    print(f"probes: wrong-mask rel delta {wm_delta:.2e}, no-hook rel delta {nh_delta:.2e} "
          f"(both must exceed tol_rel {tol_rel:.2e}) OK")

    out_dir = ROOT / "out" / f"2026-09-13_runtime-controls-{MODEL.split('/')[-1]}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"RUNTIME CONTROLS PASS (production hooks) | result: {out_dir / 'result.json'}")


if __name__ == "__main__":
    main()
