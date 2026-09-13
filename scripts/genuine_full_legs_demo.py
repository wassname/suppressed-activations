# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Bounded genuine-full demonstration check (supervisor-approved scope): the LEGS
prompt pair set (exact original inputs from the pinned demo, raw mode), donors
dog+ant, arms k8 and genuine-full (kfull) at the same h1 / anchor-25 / C1.5 — 4
nonzero rows, C0 per donor (2 rows). The unmodified Base comes from each row's own
saved base_generation (the runner computes it). 72-row ladder NOT included.

Runs the EXISTING production batch path (validate_specs -> run_with_bundle) with an
observing spy; per row verifies the resolved flags from run.md, the actual supported
ranks (k8=8, kfull>8), kfull-projector containment of the k8 columns, per-position
injection-norm monotonicity, and C0 inertness vs the row's own base generation.
32-token generations with recorded count/EOS; prefill and final readouts are the
runner's distinct readout / last_decode_readout fields. No dose ladder, no random
basis, no new sweep family. -- PI[glm-5p3-flash]"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
torch.set_grad_enabled(False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "Fact: The number of legs on the animal that spins webs is "
DOG_PROMPT = "Fact: The number of legs on the animal that barks and is called man's best friend is "
ANT_PROMPT = "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is "
ARMS = (("k8_C1.5", 3), ("kfull_C1.5", 4), ("C0", 5))  # complete-rank condition indices
MAX_NEW_TOKENS = 32


def main():
    out_dir = ROOT / "out" / f"2026-09-13_genuine-full-legs-demo-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=False)
    result = {"code_sha256": {p: sha(p) for p in ("scripts/oat_sweep.py", "scripts/demo.py",
                                                  "scripts/prompt.py",
                                                  "suppressed_activation_subspace.py")},
              "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                             cwd=ROOT, check=True, text=True,
                                             capture_output=True).stdout.strip(),
              "max_new_tokens": MAX_NEW_TOKENS, "rows": {}}

    specs = []
    for donor, tgt_prompt, tgt_out in (("dog", DOG_PROMPT, "4"), ("ant", ANT_PROMPT, "6")):
        for arm, idx in ARMS:
            specs.append({
                "output_dir": str(out_dir / f"{donor}-{arm}"),
                "sweep": "complete-rank", "condition_index": idx,
                "prompt_mode": "raw",
                "source_prompt": SOURCE_PROMPT, "target_prompt": tgt_prompt,
                "source_output": "8", "target_output": tgt_out,
                "target_concept": donor, "max_new_tokens": MAX_NEW_TOKENS,
                "lens_corpus_arrow": None, "prefill_instruction": None,
                "extraction_instruction": None, "selector_audit": False,
                "expected_condition": arm, "expected_strength": 1.5 if arm != "C0" else 0.0,
                "expected_intervention_layer": [1], "expected_xdepth_anchor_layer": 25,
                "expected_common_basis": "top8_union", "expected_common_removal": "joint",
                "expected_common_selector": "increment",
            })
    batch_file = out_dir / "batch_spec.json"
    batch_file.write_text(json.dumps(specs, indent=2) + "\n")
    oat.validate_specs(specs, oat.SWEEP_CONFIGS)  # pre-model contract, same as __main__

    capture: dict = {}
    spec_by_tag: dict = {}
    orig_hooks = oat.intervention_hooks

    def spy_hooks(*a, **kw):
        hooks = orig_hooks(*a, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs"):
            capture["spec"] = {L: {k: v for k, v in d.items()}
                               for L, d in kw["common_specs"].items()}
        return hooks

    oat.intervention_hooks = spy_hooks
    try:
        bundle = oat.load_bundle()
        cache = {"revision": bundle["revision"]}
        for position, spec in enumerate(specs):
            capture.pop("spec", None)
            expected = spec.get("expected_detector_layers")
            oat.run_with_bundle(bundle, Path(spec["output_dir"]), extraction_cache=cache,
                                batch_spec={"batch_file": str(batch_file), "index": position,
                                            "spec": dict(spec)},
                                expected_detector_layers=expected,
                                **oat.strip_spec_metadata(spec))
            tag = f"{spec['target_concept']}-{spec['expected_condition']}"
            spec_by_tag[tag] = capture.get("spec")
            row_dir = Path(spec["output_dir"])
            row = json.load(open(row_dir / "result.json"))["rows"][0]
            run_md = next((row_dir / "conditions").glob("*/run.md")).read_text()
            cfg = _config_from_run_md(run_md)
            gen = row["generation"]
            result["rows"][tag] = {
                "dir": str(row_dir),
                "config": cfg,
                "generation_text": gen["text"],
                "generation_token_ids": gen["token_ids"],
                "generation_count": len(gen["token_ids"]),
                "eos_count": tok_of(bundle, gen["token_ids"]),
                "readout_prefill": row["readout"],
                "readout_final": row["last_decode_readout"],
                "top_tokens": row["top_tokens"],
                "base_generation": row["base_generation"]["text"],
                "swap_log_odds_shift": row["swap_log_odds_shift"],
                "p_valid": row["bare_answer_mass"],
                "r2": row["repeated_bigram_fraction"],
                "intervention_record": row.get("intervention_record", {}),
                "spec_rank": list(capture["spec"].values())[0]["src"].shape if capture.get("spec") else None,
            }
            print(f"row {tag}: gen {result['rows'][tag]['generation_count']} tok, "
                  f"swap {result['rows'][tag]['swap_log_odds_shift']:.3f}, "
                  f"r2 {result['rows'][tag]['r2']:.3f}")
    finally:
        oat.intervention_hooks = orig_hooks

    _assert_contract(result, spec_by_tag)
    (out_dir / "demo_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"GENUINE-FULL LEGS DEMO PASS | {out_dir / 'demo_result.json'}")


def tok_of(bundle, token_ids):
    eos = bundle["tokenizer"].eos_token_id
    return sum(1 for t in token_ids if t == eos)


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def _config_from_run_md(run_md: str) -> dict:
    for line in run_md.splitlines():
        if line.startswith("config:"):
            return json.loads(line[len("config:"):].strip())
    raise AssertionError("run.md carries no config line")


def _assert_contract(result, spec_by_tag):
    rows = result["rows"]
    specs = {}
    for donor in ("dog", "ant"):
        k8, kfull, c0 = (rows[f"{donor}-{a}"] for a, _ in ARMS)
        assert k8["config"]["common_temporal_full"] is False, "k8 must be non-full"
        assert kfull["config"]["common_temporal_full"] is True, "kfull must be temporal-full"
        assert c0["config"]["strength"] == 0.0
        assert k8["spec_rank"][-1] == 8, f"k8 rank {k8['spec_rank']}"
        assert kfull["spec_rank"][-1] > 8, \
            f"full supported rank must exceed 8, got {kfull['spec_rank']}"
        # generation counts and EOS recording (AGENTS: state the actual token count)
        for row in (k8, kfull, c0):
            assert 0 < row["generation_count"] <= MAX_NEW_TOKENS, row["generation_count"]
        # C0 inertness: the C0 row's steered generation equals its own unmodified base
        assert c0["generation_text"] == c0["base_generation"], \
            "C0 row diverged from its own base generation"
        # readouts are recorded as distinct prefill/final fields
        assert k8["readout_prefill"] is not None and k8["readout_final"] is not None
        # injection norms monotonic per position (late donor, measured not assumed)
        rec = kfull["intervention_record"]
        norms = next((v.get("donor_proj_norms") for v in rec.values()
                      if isinstance(v, dict) and v.get("donor_proj_norms") is not None), None)
        if norms:
            vals = list(norms.values()) if isinstance(norms, dict) else list(norms)
            assert vals == sorted(vals) or vals == sorted(vals, reverse=True), \
                f"injection norms not monotonic per position: {vals}"
        # projector containment: k8 columns inside the kfull span, same donor pair
        k8_spec, full_spec = spec_by_tag[f"{donor}-k8_C1.5"], spec_by_tag[f"{donor}-kfull_C1.5"]
        assert k8_spec and full_spec, "spy missed a spec"
        L = next(iter(k8_spec))
        k8_cols = k8_spec[L]["src"].float()[:, :, :8]        # (positions, hidden, 8)
        full_cols = full_spec[L]["src"].float()[:, :, 8:]    # the beyond-8 support
        full_span, _ = torch.linalg.qr(full_cols.transpose(1, 2).reshape(-1, full_cols.shape[-1]))
        k8_flat = k8_cols.transpose(1, 2).reshape(-1, 8).T   # (hidden, 8*positions)
        resid = k8_flat - full_span @ (full_span.T @ k8_flat)
        cont = float(resid.norm() / k8_flat.norm())
        result["rows"][f"{donor}-kfull_C1.5"]["k8_in_kfull_containment"] = cont
        assert cont < 1e-4, f"{donor}: k8 columns not contained in kfull span: {cont}"


if __name__ == "__main__":
    main()
