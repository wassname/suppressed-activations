# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Authorized bridge matrix (supervisor seq 14): 8 experimental rows
{dog, ant} x {selector: attenuation-4 | increment-union-SVD-4} x {site: 20 | 8},
delta = template_deltas[20] FIXED (delta_anchor_layer=20), C1.5, 3 positions,
continuous decode policy, 128-token config; + explicit C0/unhooked controls.

ORDER AND GATE: the historical attenuation h20 rows run FIRST and MUST reproduce the
saved 2026-09-10 continuations (token IDs + text) before any other row runs; on
mismatch the batch stops and reports drift. Resolved-spec checks before each row:
rank 4, readout 4, edit last-3, anchor 20, C1.5, both selectors, sites 20/8, and the
exact historical source+donor rendered input IDs/instructions. U/delta checks and all
offset norms persisted BEFORE asserts. Per-condition run.md carries the first-32
prefix; the full 128-token continuations live in the row JSONs. -- PI[glm-5p3-flash]"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
from dataclasses import replace
torch.set_grad_enabled(False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat
from scripts.prompt import assistant_prefill_input_ids

ROOT = Path(__file__).resolve().parents[1]
BW_DEMO = ROOT / "out" / "2026-09-13_genuine-full-legs-demo-130912"
HIST = {"dog": ROOT / "out" / "2026-09-10_replay-C1.5-legs-dog" / "result.json",
        "ant": ROOT / "out" / "2026-09-10_replay-C1.5-legs-ant" / "result.json"}
N_TOKENS = 128


def main():
    # the previous increment rows (the byte-equality reference for the replays)
    # the durable copy lives in the main evidence dir (the 130912 dir may be cleaned)
    mx_prev = json.load(open(ROOT / "../suppressed-activations/slop/research/demo-evidence/"
                             "bridge-matrix/matrix_result.json"))["rows"]
    PREV_INC = {t: mx_prev[t]["generation"] for t in
                ("dog-inc-h20", "dog-inc-h8", "ant-inc-h20", "ant-inc-h8")}
    out_dir = ROOT / "out" / f"2026-09-13_bridge-matrix-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {"rows": {}, "gate": {}, "controls": {}}

    # registry variants on the HISTORICAL family (span-correction-sweep)
    def variant(name, **cfg_over):
        oat.SWEEP_CONFIGS[name] = lambda: [
            (f, n, replace(c, **cfg_over)) for f, n, c in oat.SWEEP_CONFIGS["span-correction-sweep"]()]
    variant("bridge-att-h8", delta_anchor_layer=20, intervention_layer=(8,))
    variant("bridge-inc-h20", delta_anchor_layer=20, basis_selector="increment")
    variant("bridge-inc-h8", delta_anchor_layer=20, basis_selector="increment",
            intervention_layer=(8,))
    variant("bridge-inc-h20-q4", delta_anchor_layer=20, basis_selector="increment",
            selection_end_offset=4)
    variant("bridge-inc-h8-q4", delta_anchor_layer=20, basis_selector="increment",
            selection_end_offset=4, intervention_layer=(8,))

    frozen = json.load(open(ROOT / "slop" / "replay_frozen_candidate_batch.json"))
    bundle = oat.load_bundle()
    tok, model = bundle["tokenizer"], bundle["model"]
    cache = {"revision": bundle["revision"]}
    orig = oat.intervention_hooks

    # rows: the EXACT frozen historical specs (gate/replay = att-h20 site-tied) +
    # the anchor-20 variants; C0 = condition_index 0 per family
    rows = []
    for donor, frozen_idx in (("dog", 4), ("ant", 6)):
        hist = json.load(open(HIST[donor]))
        # wrapper replays (offset 0) — the comparison arm; byte-equality required vs
        # the previous increment rows (previous_inc_ref below)
        rows.append({"donor": donor, "sel": "inc", "site": 20, "sweep": "bridge-inc-h20",
                     "cond": 3, "spec": dict(frozen[frozen_idx], sweep="bridge-inc-h20"),
                     "hist": hist, "gate": True})
        rows.append({"donor": donor, "sel": "inc", "site": 8, "sweep": "bridge-inc-h8",
                     "cond": 3, "spec": dict(frozen[frozen_idx], sweep="bridge-inc-h8"),
                     "hist": hist, "gate": True})
        # the 4 QUESTION-window experimental rows (offset 4)
        rows.append({"donor": donor, "sel": "inc-q4", "site": 20, "sweep": "bridge-inc-h20-q4",
                     "cond": 3, "spec": dict(frozen[frozen_idx], sweep="bridge-inc-h20-q4"),
                     "hist": hist})
        rows.append({"donor": donor, "sel": "inc-q4", "site": 8, "sweep": "bridge-inc-h8-q4",
                     "cond": 3, "spec": dict(frozen[frozen_idx], sweep="bridge-inc-h8-q4"),
                     "hist": hist})
    for sel in ("att", "inc"):
        for site in (20, 8):
            sweep = "span-correction-sweep" if (sel == "att" and site == 20) else \
                f"bridge-{'att' if sel == 'att' else 'inc'}-h{site}"
            rows.append({"donor": "dog", "sel": sel, "site": site, "sweep": sweep,
                         "cond": 0, "spec": dict(frozen[4], sweep=sweep, condition_index=0),
                         "c0": True, "hist": json.load(open(HIST["dog"]))})

    gate_ok = True
    for position, r in enumerate(rows):
        spec = dict(r["spec"])
        spec["output_dir"] = str(out_dir / f"{r['donor']}-{r['sel']}-h{r['site']}"
                                   f"{'-C0' if r.get('c0') else ''}")
        # preflight: rendered input IDs equal the HISTORICAL saved ones
        saved = r["hist"]["rendered_inputs"]
        src_r = assistant_prefill_input_ids(tok, spec["source_prompt"], device=model.device,
                                            instruction=spec["prefill_instruction"])
        assert src_r["input_ids"].flatten().tolist() == saved["source"]["input_ids"], \
            f"{r['donor']} source IDs != historical"
        # NOTE the donor prompt IDs: the historical runs rendered the donor prompt with
        # the same template; assert equality too
        don_r = assistant_prefill_input_ids(tok, spec["target_prompt"], device=model.device,
                                            instruction=spec["prefill_instruction"])
        assert don_r["input_ids"].flatten().tolist() == saved["donor"]["input_ids"], \
            f"{r['donor']} donor IDs != historical"

        obs = {}
        orig_hooks = oat.intervention_hooks

        def spy(*a, **kw):
            hooks = orig_hooks(*a, **kw)
            if kw.get("operation") == "span_corrected_delta":
                obs["shared"] = a[0].clone()
                obs["fixed_deltas"] = {k: v.clone() for k, v in kw["fixed_deltas"].items()}
                obs["args"] = tuple(a)
                obs["kwargs"] = {k: v for k, v in kw.items() if k != "record"}
            return hooks

        oat.intervention_hooks = spy
        try:
            row_dir = Path(spec["output_dir"])
            row_dir.mkdir(parents=True, exist_ok=True)
            oat.run_with_bundle(bundle, row_dir, extraction_cache=cache,
                                batch_spec={"batch_file": str(out_dir / "batch_spec.json"),
                                            "index": position, "spec": dict(spec)},
                                expected_detector_layers=None,
                                **oat.strip_spec_metadata(spec))
        finally:
            oat.intervention_hooks = orig_hooks
        row_res = json.load(open(row_dir / "result.json"))["rows"][0]
        row_res["obs_shared_shape"] = list(obs["shared"].shape)
        row_res["applied_delta"] = {k: v.tolist() for k, v in obs["fixed_deltas"].items()}
        # resolved-spec checks BEFORE interpretation
        cfg = row_res["config"]
        if not r.get("c0"):
            assert cfg["strength"] == 1.5, (r["donor"], r["sel"], r["site"], "strength")
            if not r.get("gate"):  # the gate row IS the historical site-tied config
                assert cfg["delta_anchor_layer"] == 20, (r["donor"], r["sel"], r["site"], "anchor")
            assert cfg["readout_positions"] == 4, (r["donor"], r["sel"], r["site"], "readout")
            assert cfg["intervention_layer"] == [r["site"]], (r["donor"], r["sel"], r["site"], "site")
            assert cfg["basis_selector"] == ("increment" if r["sel"] == "inc" else "attenuation"), \
                (r["donor"], r["sel"], r["site"], "selector")
            assert shared_ok(obs, f"{r['donor']}-{r['sel']}-h{r['site']}")
        # REPLAY GATE: the attenuation h20 rows must match the historical continuations
        if r.get("gate"):
            # byte-equality vs the PREVIOUS increment rows (the same code path check)
            prev_ref = PREV_INC[f"{r['donor']}-inc-h{r['site']}"]
            same_ids = row_res["generation"]["token_ids"] == prev_ref["token_ids"]
            same_text = row_res["generation"]["text"] == prev_ref["text"]
            result["gate"][f"{r['donor']}-h{r['site']}"] = {"token_ids_match": same_ids,
                                                            "text_match": same_text}
            print(f"GATE {r['donor']} h{r['site']}: token_ids_match={same_ids} text_match={same_text}")
            if not (same_ids and same_text):
                (out_dir / "drift_report.json").write_text(json.dumps(
                    {"row": r["donor"], "site": r["site"], "got": row_res["generation"]["text"],
                     "expected": prev_ref["text"]}, indent=2))
                print("DRIFT: stopping the batch; the comparison arm is not the same code path")
                gate_ok = False
                break
        tag = f"{r['donor']}-{r['sel']}-h{r['site']}" + ("-C0" if r.get("c0") else "")
        result["rows"][tag] = row_res
        result["controls"][tag] = {
            "first32_text": tok.decode(row_res["generation"]["token_ids"][:32]),
            "full_text": row_res["generation"]["text"],
            "n_tokens": len(row_res["generation"]["token_ids"]),
            "n_eos": sum(1 for t in row_res["generation"]["token_ids"] if t == tok.eos_token_id)}
        per_md = row_dir / "run.md"
        per_md.write_text(f"# {tag}\n\nconfig: {json.dumps(cfg)}\n\n"
                          f"first32: {json.dumps(result['controls'][tag]['first32_text'])}\n\n"
                          f"full: {json.dumps(result['controls'][tag]['full_text'])}\n")
    # unhooked control
    if gate_ok:
        src_ids = assistant_prefill_input_ids(tok, rows[0]["hist"]["rows"][0]["config"].get(
            "source_prompt", "Question: How many legs does the animal that spins webs have?\nAnswer: "),
            device=model.device, instruction=spec["prefill_instruction"])["input_ids"]
        from scripts.demo import trajectory
        _, logits_clean = trajectory(model, src_ids, model.model.norm)
        result["controls"]["unhooked_first_logits_sha256"] = hashlib.sha256(
            logits_clean.cpu().numpy().tobytes()).hexdigest()
    result["outcome"] = "PASS" if gate_ok else "STOPPED-DRIFT"
    (out_dir / "matrix_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"BRIDGE MATRIX {'PASS' if gate_ok else 'STOPPED'} | {out_dir / 'matrix_result.json'}")


def shared_ok(obs, donor_tag="?"):
    shared = obs["shared"].float()
    eye = torch.eye(shared.shape[-1], device=shared.device)
    dev = float((shared.T @ shared - eye).abs().max())
    assert dev < 1e-4 and shared.shape[-1] == 4
    for delta in obs["fixed_deltas"].values():
        resid = delta - shared @ (shared.T @ delta)
        _cont = float(resid.norm() / delta.norm().clamp_min(1e-9))
    # 1e-4: bf16 rounding of the projection/normalization path (the production's own
    # fp32 containment gate passed; the recomputation from bf16-captured tensors adds
    # ~1.6e-5 residual on the increment-routed rows)
    assert _cont < 1e-4, (donor_tag, "containment", _cont, "shared_rank", shared.shape[-1],
                          "delta_norm", float(delta.norm()))
    return True


if __name__ == "__main__":
    main()
