# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Paired donor-anchor control (supervisor-approved, ONE confound): the current
legs-dog h1 k8/joint-16 C1.5 recipe with anchor 25 (existing replay) vs anchor 1
(depth-matched) — SAME code, SAME constructed basis (Q_src/Q_donor shared, projectors
asserted identical), ONLY the donor state anchor changes. Offset-wise inj/edit/
residual norms captured at prefill+decode; C0/base saved. Tiny production anchor
contract first. Descriptive control — no exoneration claims either way.
-- PI[glm-5p3-flash]"""
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
BATCH = ROOT / "slop" / "complete_rank_batch.json"
K8_ROW = 27
N_TOKENS = 128
TINY_MAX = 4


import ast as _ast
_src_sas = (ROOT / "scripts" / "oat_sweep.py").read_text()
_fn = next(n for n in _ast.parse(_src_sas).body
           if isinstance(n, _ast.FunctionDef) and n.name == "repetition_bigram_fraction")
exec(compile(_ast.Module(body=[_fn], type_ignores=[]), "suppressed_activation_subspace.py", "exec"))


def r2_of(ids, tok):
    from transformers import AutoTokenizer
    return repetition_bigram_fraction(ids, set(AutoTokenizer.from_pretrained(
        "Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a").all_special_ids))


def capture_spec(bundle, spec_row, out_dir):
    """Zero-generation capture of the built spec for one batch row."""
    capture: dict = {}
    orig = oat.intervention_hooks

    class SpecCaptured(Exception):
        pass

    def spy(*args, **kw):
        hooks = orig(*args, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs"):
            capture["args"] = args
            capture["kwargs"] = {k: v for k, v in kw.items() if k != "record"}
            raise SpecCaptured
        return hooks

    oat.intervention_hooks = spy
    try:
        d = Path(out_dir) / "spec-construction"
        d.mkdir(parents=True, exist_ok=True)
        oat.run_with_bundle(bundle, d, extraction_cache={"revision": bundle["revision"]},
                            batch_spec={"batch_file": str(BATCH), "index": K8_ROW,
                                        "spec": spec_row},
                            expected_detector_layers=spec_row.get("expected_detector_layers"),
                            **oat.strip_spec_metadata(spec_row))
        raise AssertionError("spec construction completed without capture")
    except SpecCaptured:
        pass
    finally:
        oat.intervention_hooks = orig
    return capture


def run_arm(model, tok, ids, blocks, capture, prefill_only, max_new):
    from scripts.demo import intervention_hooks
    from scripts.runtime_controls import cached_generate
    record = {}
    hooks = intervention_hooks(*capture["args"],
                               **{**capture["kwargs"], "record": record,
                                  "prefill_only": prefill_only})
    gen, rows, _ = cached_generate(model, tok, ids, blocks, hooks, max_new)
    return gen, rows, record


def main():
    tiny = "tiny" in os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B").lower()
    out_dir = ROOT / "out" / f"2026-09-13_anchor-control-{'tiny' if tiny else 'gpu'}-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=False)
    result = {"tiny": {"enabled": tiny}, "rows": {}}

    batch_row = json.loads(BATCH.read_text())[K8_ROW]
    row_a25 = dict(batch_row)
    # anchor-1 variant through the SAME construction: an in-process registry variant
    # (same cfg, only xdepth_anchor_layer 25->1); no production file change
    oat.SWEEP_CONFIGS["complete-rank-anchor1"] = lambda: [
        (fam, name, replace(cfg, xdepth_anchor_layer=1) if name == "k8_C1.5" else cfg)
        for fam, name, cfg in oat.SWEEP_CONFIGS["complete-rank"]()]
    row_a1 = dict(batch_row)
    row_a1["sweep"] = "complete-rank-anchor1"
    row_a1["expected_xdepth_anchor_layer"] = 1

    if tiny:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
        model = AutoModelForCausalLM.from_pretrained("wassname/qwen3-5lyr-tiny-random",
                                                     dtype=torch.bfloat16).eval()
        from scripts.demo import trajectory
        fn = model.model.norm
        src = assistant_prefill_input_ids(
            tok, "Question: what is the animal that spins webs called?\nAnswer: ",
            device="cpu", instruction="Answer the question with the answer first.")
        don = assistant_prefill_input_ids(
            tok, "Question: what is the animal that barks called?\nAnswer: ",
            device="cpu", instruction="Answer the question with the answer first.")
        res_s, _ = trajectory(model, src["input_ids"], fn)
        res_d, _ = trajectory(model, don["input_ids"], fn)
        L = 2
        U = torch.linalg.qr(torch.randn(res_s.shape[-1], 4, generator=torch.Generator().manual_seed(0)))[0]
        d3 = res_d[3, don["content_end"] - 1].float()
        d1 = res_d[1, don["content_end"] - 1].float()
        assert not torch.allclose(d3, d1), "anchor states identical; contract meaningless"
        # both specs keyed by the residual layer; only the donor-state anchor differs
        specs = {25: {L: {"src": U.unsqueeze(0), "donor_proj": (U @ (U.T @ d3)).unsqueeze(0),
                          "decode_src": U.unsqueeze(0),
                          "decode_proj": (U @ (U.T @ d3)).unsqueeze(0), "donor_U": U}},
                 1: {L: {"src": U.unsqueeze(0), "donor_proj": (U @ (U.T @ d1)).unsqueeze(0),
                         "decode_src": U.unsqueeze(0),
                         "decode_proj": (U @ (U.T @ d1)).unsqueeze(0), "donor_U": U}}}
        from scripts.demo import intervention_hooks
        from scripts.runtime_controls import cached_generate
        firsts, recs = {}, {}
        for anchor, spec in specs.items():
            record = {}
            hooks = intervention_hooks(U, U, res_s, operation="common_replace",
                                       common_specs=spec, blocks_to_hook=[L - 1],
                                       positions=1, source_position=src["content_end"] - 1,
                                       match_component_norm=False, restore_norm=False,
                                       strength=1.5, record=record)
            gen, rows, _ = cached_generate(model, tok, src["input_ids"],
                                           model.model.layers, hooks, TINY_MAX)
            firsts[anchor] = gen["token_ids"][0]
            recs[anchor] = record[L]
            assert recs[anchor]["residual_norm"] > 0 and recs[anchor]["decode_steps"] == TINY_MAX - 1
        # NOTE: first tokens may legitimately differ across anchors (different donor
        # vector); no equality assert here.
        # projectors identical: same U; donor vectors different
        assert torch.equal(specs[25][L]["src"], specs[1][L]["src"])
        assert not torch.allclose(specs[25][L]["donor_proj"], specs[1][L]["donor_proj"])
        result["tiny"] = {"first_tokens": firsts,
                          "decode_steps": {a: recs[a]["decode_steps"] for a in recs},
                          "donor_proj_norms": {a: float(recs[a]["perturbation_norm"]) for a in recs}}
        (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"TINY ANCHOR CONTRACT PASS | {out_dir / 'result.json'}")
        return

    bundle = oat.load_bundle()
    tok, model = bundle["tokenizer"], bundle["model"]
    blocks = model.model.layers

    cap25 = capture_spec(bundle, row_a25, out_dir)
    # anchor-1 spec: same construction, only the donor anchor differs
    cap1 = capture_spec(bundle, row_a1, out_dir)
    L = next(iter(cap25["kwargs"]["common_specs"]))
    s25, s1 = cap25["kwargs"]["common_specs"][L], cap1["kwargs"]["common_specs"][L]
    assert torch.equal(s25["src"], s1["src"]), "source/joint projector changed with anchor"
    assert torch.equal(s25["donor_U"], s1["donor_U"]), "donor basis changed with anchor"
    assert not torch.allclose(s25["donor_proj"], s1["donor_proj"]), \
        "donor vectors identical; anchor change ineffective"
    assert torch.equal(s25["decode_src"], s1["decode_src"]), "decode_src differs across anchors"
    # decode_proj IS the donor-state projection at the anchor layer: anchor-dependent
    assert not torch.equal(s25["decode_proj"], s1["decode_proj"]), \
        "decode_proj identical across anchors; anchor change did not flow to decode"

    saved = json.load(open(ROOT / "out" / "2026-09-12_cb-cr8" / "k8-legs-L1-dog" /
                           "result.json"))["rendered_inputs"]
    src_r = assistant_prefill_input_ids(tok, batch_row["source_prompt"], device=model.device,
                                        instruction=batch_row["prefill_instruction"])
    assert src_r["input_ids"].flatten().tolist() == saved["source"]["input_ids"], "input mismatch"
    ids = src_r["input_ids"]

    from scripts.runtime_controls import cached_generate
    gen_base, _, _ = cached_generate(model, tok, ids, blocks, {}, N_TOKENS)
    result["rows"]["base"] = {"text": gen_base["text"], "token_ids": gen_base["token_ids"],
                              "r2": r2_of(gen_base["token_ids"], tok),
                              "n_eos": sum(1 for t in gen_base["token_ids"] if t == tok.eos_token_id)}
    for name, cap, po in (("anchor25", cap25, False), ("anchor1", cap1, False)):
        gen, rows, record = run_arm(model, tok, ids, blocks, cap, po, N_TOKENS)
        result["rows"][name] = {
            "text": gen["text"], "token_ids": gen["token_ids"], "r2": r2_of(gen["token_ids"], tok),
            "replacement_trace_full": record[L]["replacement_trace"],
            "n_eos": sum(1 for t in gen["token_ids"] if t == tok.eos_token_id),
            "first_logits_sha256": hashlib.sha256(rows[0].cpu().numpy().tobytes()).hexdigest(),
            "prefill_edit_norm": next(e["applied_norm_after_dtype"]
                                      for e in record[L]["replacement_trace"] if e["phase"] == "prefill"),
            "decode_edit_norms": [round(e["applied_norm_after_dtype"], 3) for e
                                  in record[L]["replacement_trace"] if e["phase"] == "decode"][:8],
            "decode_steps": record[L]["decode_steps"]}
        print(f"{name}: {len(gen['token_ids'])} tok, r2 {result['rows'][name]['r2']:.3f}, "
              f"EOS {result['rows'][name]['n_eos']}")

    # save BEFORE asserting: the anchor change is SUPPOSED to change the edit (different
    # donor vector), so first-logits identity is NOT required here; record both hashes
    result["first_logits_sha256"] = {a: result["rows"][a]["first_logits_sha256"]
                                     for a in ("anchor25", "anchor1")}
    assert result["rows"]["anchor25"]["prefill_edit_norm"] != \
        result["rows"]["anchor1"]["prefill_edit_norm"], \
        "donor anchor did not change the prefill edit"
    result["outcome"] = "PASS"
    (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"ANCHOR CONTROL PASS | {out_dir / 'result.json'}")


if __name__ == "__main__":
    main()
