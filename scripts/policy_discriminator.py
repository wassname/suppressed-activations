# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""TWO-row policy discriminator (supervisor-approved): continuous frozen-late-donor
decode injection vs explicit prompt-only control. Same saved legs-dog h1 row
(k8/joint-16 basis, C1.5, anchor 25, last-3 prefill edit, 128 tokens), same code, one
bundle, one spec construction (zero-generation capture). The prompt-only arm uses the
production `prefill_only` flag: identical prefill edit, decode calls happen but edit
nothing. Assertions: first-logits hash identical, prefill edit records identical,
continuous decode_steps = n-1 / prompt-only decode_steps = 0 while decode calls
happen. Causal claim, if any, is limited to the additional decode editing under this
fixed initial condition. Tiny preflight first (CPU), then the 4B on GPU via queue.
-- PI[glm-5p3-flash]"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
torch.set_grad_enabled(False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat
from scripts.prompt import assistant_prefill_input_ids

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "complete_rank_batch.json"
K8_ROW = 27  # legs-dog k8_C1.5
N_TOKENS = 128
TINY_MAX = 4


def r2_of(text_ids):
    bigrams = list(zip(text_ids, text_ids[1:]))
    return 1 - len(set(bigrams)) / len(bigrams) if len(bigrams) > 1 else 0.0


def two_arm_run(model, tok, ids, blocks, spec, L, c_end, max_new, label_prefix, capture_decodes=True):
    """Run continuous and prompt-only arms from the SAME spec; return records."""
    from scripts.demo import intervention_hooks
    from scripts.runtime_controls import cached_generate
    out = {}
    for arm, prefill_only in (("continuous", False), ("prompt_only", True)):
        record = {}
        spec_arm = {L: {**spec[L]}}
        hooks = intervention_hooks(
            *capture["args"], **{**capture["kwargs"], "record": record,
                                 "prefill_only": prefill_only})
        decode_calls = []
        h = model.lm_head.register_forward_hook(
            lambda m, i, o: decode_calls.append(1)) if capture_decodes else None
        try:
            gen, rows, fin = cached_generate(model, tok, ids, blocks, hooks, max_new)
        finally:
            if h:
                h.remove()
        out[arm] = {"gen": gen, "record": record, "decode_call_count": len(decode_calls),
                    "first_logits": rows[0].clone()}
        print(f"{label_prefix}/{arm}: {len(gen['token_ids'])} tok, decode_calls "
              f"{len(decode_calls)}, decode_steps {record[1 if 1 in record else list(record)[0]]['decode_steps']}")
    return out


def main():
    tiny = os.environ.get("SUPPRESSED_DEVICE", "cuda") == "cpu"
    out_dir = ROOT / "out" / f"2026-09-13_policy-discriminator-{'tiny' if tiny else 'gpu'}-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=False)
    result = {"tiny": {"enabled": tiny}, "rows": {}}
    if tiny:
        result["tiny"] = {"device": "cpu"}

    # ---- tiny CPU proof: decode-disable keeps prefill edit + first token, decode
    # calls happen but edit nothing
    if tiny:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
        model = AutoModelForCausalLM.from_pretrained(
            "wassname/qwen3-5lyr-tiny-random", dtype=torch.bfloat16).eval()
        from scripts.demo import trajectory
        fn = model.model.norm
        src = assistant_prefill_input_ids(tok, "Question: what is the animal that spins webs called?\nAnswer: ",
                                          device="cpu", instruction="Answer the question with the answer first.")
        don = assistant_prefill_input_ids(tok, "Question: what is the animal that barks called?\nAnswer: ",
                                          device="cpu", instruction="Answer the question with the answer first.")
        res_s, _ = trajectory(model, src["input_ids"], fn)
        res_d, _ = trajectory(model, don["input_ids"], fn)
        L = 2
        U = torch.linalg.qr(torch.randn(res_s.shape[-1], 4, generator=torch.Generator().manual_seed(0)))[0]
        d = res_d[L, don["content_end"] - 1].float()
        spec = {L: {"src": U.unsqueeze(0), "donor_proj": (U @ (U.T @ d)).unsqueeze(0),
                    "decode_src": U.unsqueeze(0), "decode_proj": (U @ (U.T @ d)).unsqueeze(0),
                    "donor_U": U}}
        from scripts.demo import intervention_hooks
        from scripts.runtime_controls import cached_generate
        firsts, recs = {}, {}
        for arm, po in (("continuous", False), ("prompt_only", True)):
            record = {}
            hooks = intervention_hooks(U, U, res_s, operation="common_replace",
                                       common_specs=spec, blocks_to_hook=[L - 1],
                                       positions=1, source_position=src["content_end"] - 1,
                                       match_component_norm=False, restore_norm=False,
                                       strength=1.5, prefill_only=po, record=record)
            gen, rows, _ = cached_generate(model, tok, src["input_ids"], model.model.layers, hooks, TINY_MAX)
            firsts[arm] = gen["token_ids"][0]
            recs[arm] = record[L]
        result["tiny"] = {"first_token_continuous": firsts["continuous"],
                          "first_token_prompt_only": firsts["prompt_only"],
                          "decode_steps": {a: recs[a]["decode_steps"] for a in recs}}
        assert firsts["continuous"] == firsts["prompt_only"], \
            "decode-disable changed the first token: prefill edit lost"
        assert recs["prompt_only"]["decode_steps"] == 0, "prompt-only edited at decode"
        assert recs["continuous"]["decode_steps"] == TINY_MAX - 1
        # prefill edit identity via the per-call traces (the top-level record fields
        # are overwritten by the last decode call in the continuous arm)
        tr_c = [e for e in recs["continuous"]["replacement_trace"] if e["phase"] == "prefill"]
        tr_p = [e for e in recs["prompt_only"]["replacement_trace"] if e["phase"] == "prefill"]
        assert tr_c and tr_p and tr_c[0]["applied_norm_after_dtype"] == tr_p[0]["applied_norm_after_dtype"], \
            "prefill edit differs between arms"
        result["tiny"]["prefill_edit_norm"] = tr_p[0]["applied_norm_after_dtype"]
        (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"TINY PREFLIGHT PASS | {out_dir / 'result.json'}")
        return

    # ---- 4B: one bundle, one spec construction (zero-generation capture)
    batch_1230 = json.loads(BATCH.read_text())
    spec_row = batch_1230[K8_ROW]
    assert spec_row["expected_condition"] == "k8_C1.5"
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
        bundle = oat.load_bundle()
    finally:
        oat.intervention_hooks = orig
    tok, model = bundle["tokenizer"], bundle["model"]
    blocks = model.model.layers
    spec_dir = out_dir / "spec-construction"
    spec_dir.mkdir(parents=True, exist_ok=True)
    try:
        oat.run_with_bundle(bundle, spec_dir, extraction_cache={"revision": bundle["revision"]},
                            batch_spec={"batch_file": str(BATCH), "index": K8_ROW,
                                        "spec": spec_row},
                            expected_detector_layers=spec_row.get("expected_detector_layers"),
                            **oat.strip_spec_metadata(spec_row))
        raise AssertionError("spec construction ran to completion without capture")
    except SpecCaptured:
        pass  # spec + bundle in hand; no generation happened
    src_r = assistant_prefill_input_ids(tok, spec_row["source_prompt"], device=model.device,
                                        instruction=spec_row["prefill_instruction"])
    saved = json.load(open(ROOT / "out" / "2026-09-12_cb-cr8" / "k8-legs-L1-dog" /
                           "result.json"))["rendered_inputs"]
    assert src_r["input_ids"].flatten().tolist() == saved["source"]["input_ids"], "input mismatch"
    ids = src_r["input_ids"]
    L = next(iter(capture["kwargs"]["common_specs"]))
    spec = {L: {k: v for k, v in capture["kwargs"]["common_specs"][L].items()}}

    arms = two_arm_run(model, tok, ids, blocks, spec, L, spec_row, capture, out_dir, result)

    # base (no hooks) for the row
    from scripts.runtime_controls import cached_generate
    gen_base, rows_base, _ = cached_generate(model, tok, ids, blocks, {}, N_TOKENS)
    result["rows"]["base"] = {"text": gen_base["text"], "token_ids": gen_base["token_ids"],
                              "r2": r2_of(gen_base["token_ids"]),
                              "n_eos": sum(1 for t in gen_base["token_ids"] if t == tok.eos_token_id)}
    for arm, data in arms.items():
        gen = data["gen"]
        result["rows"][arm] = {
            "text": gen["text"], "token_ids": gen["token_ids"],
            "r2": r2_of(gen["token_ids"]),
            "n_eos": sum(1 for t in gen["token_ids"] if t == tok.eos_token_id),
            "first_logits_sha256": hashlib.sha256(
                data["first_logits"].cpu().numpy().tobytes()).hexdigest(),
            "decode_steps": data["record"][L]["decode_steps"],
            "decode_call_count": data["decode_call_count"],
            "prefill_edit_norm": next(e["applied_norm_after_dtype"] for e
                                      in data["record"][L]["replacement_trace"]
                                      if e["phase"] == "prefill"),
            "prefill_positions": data["record"][L]["prefill_positions"]}
    h_c = result["rows"]["continuous"]["first_logits_sha256"]
    h_p = result["rows"]["prompt_only"]["first_logits_sha256"]
    assert h_c == h_p, "first-logits hash differs between arms"
    pc, pp = result["rows"]["continuous"]["prefill_positions"], result["rows"]["prompt_only"]["prefill_positions"]
    assert pc == pp and result["rows"]["continuous"]["prefill_edit_norm"] == \
        result["rows"]["prompt_only"]["prefill_edit_norm"], "prefill edits differ"
    n = len(arms["continuous"]["gen"]["token_ids"])
    assert result["rows"]["continuous"]["decode_steps"] == n - 1, "continuous decode not fully edited"
    assert result["rows"]["prompt_only"]["decode_steps"] == 0, "prompt-only edited at decode"
    assert result["rows"]["prompt_only"]["decode_call_count"] == n - 1, \
        "prompt-only decode calls did not happen"
    result["outcome"] = "PASS"
    (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"POLICY DISCRIMINATOR PASS | {out_dir / 'result.json'}")


if __name__ == "__main__":
    main()
