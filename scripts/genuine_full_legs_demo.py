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
from scripts.prompt import assistant_prefill_input_ids

REF_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "complete_rank_batch.json"
# the ACTUAL 1230 legs rows (source of truth): dog = indices 27/28/29, ant = 33/34/35
ROW_INDICES = {"dog": (27, 28, 29), "ant": (33, 34, 35)}
ARMS = (("k8_C1.5", 27), ("kfull_C1.5", 28), ("C0", 29))  # per-donor offsets +0/+1/+2
MAX_NEW_TOKENS = None  # exact 1230 config; no editorial change


def main():
    out_dir = ROOT / "out" / f"2026-09-13_genuine-full-legs-demo-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=False)
    result = {"code_sha256": {p: sha(p) for p in ("scripts/oat_sweep.py", "scripts/demo.py",
                                                  "scripts/prompt.py",
                                                  "suppressed_activation_subspace.py")},
              "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                             cwd=ROOT, check=True, text=True,
                                             capture_output=True).stdout.strip(),
              "rows": {}}

    # EXACT 1230 rows (source of truth): copy the six legs condition dicts, change ONLY
    # output_dir (frozen provenance: never write into the historical dirs)
    batch_1230 = json.loads(BATCH.read_text())
    specs, prompts = [], {}
    for donor, (k8_i, kfull_i, c0_i) in ROW_INDICES.items():
        for arm, idx in (("k8_C1.5", k8_i), ("kfull_C1.5", kfull_i), ("C0", c0_i)):
            row = dict(batch_1230[idx])
            assert row["expected_condition"] == arm, (idx, row["expected_condition"])
            # pre-model flag check: the old batch's full-flag defect must not ride along
            if arm == "kfull_C1.5":
                assert row["expected_common_temporal_full"] is True, \
                    "copied kfull row carries the temporal_full=False defect"
                assert row["expected_common_source_rank"] == 0 \
                    and row["expected_common_donor_rank"] == 0, \
                    "kfull must use the full-support sentinels"
            prompts[arm, donor] = (row["source_prompt"], row["target_prompt"],
                                   row["source_output"], row["target_output"])
            row["output_dir"] = str(out_dir / f"{donor}-{arm}")
            specs.append(row)
    batch_file = out_dir / "batch_spec.json"
    batch_file.write_text(json.dumps(specs, indent=2) + "\n")

    # preflight BEFORE model load: exact 1230 prompt equality + rendered input-ID
    # equality against the saved 1230 results, for all six rows
    preflight = {}
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=REF_REV)
    for (arm, donor), (src_p, tgt_p, src_out, tgt_out) in prompts.items():
        row = next(s for s in specs if s["expected_condition"] == arm and s["target_concept"] == donor)
        src_r = assistant_prefill_input_ids(tok, src_p, device="cpu", instruction=row["prefill_instruction"])
        tgt_r = assistant_prefill_input_ids(tok, tgt_p, device="cpu", instruction=row["prefill_instruction"])
        saved = json.load(open(ROOT / "out" / "2026-09-12_cb-cr8" /
                               f"k8-legs-L1-{donor}" / "result.json"))["rendered_inputs"]
        assert (src_r["input_ids"].flatten().tolist() == saved["source"]["input_ids"]), \
            f"{donor} source input IDs differ from 1230"
        assert (tgt_r["input_ids"].flatten().tolist() == saved["donor"]["input_ids"]), \
            f"{donor} donor input IDs differ from 1230"
        preflight[f"{donor}-{arm}"] = {
            "source_prompt_repr": repr(src_p), "target_prompt_repr": repr(tgt_p),
            "source_ids_sha256": hashlib.sha256(json.dumps(
                src_r["input_ids"].flatten().tolist()).encode()).hexdigest(),
            "donor_ids_sha256": hashlib.sha256(json.dumps(
                tgt_r["input_ids"].flatten().tolist()).encode()).hexdigest(),
            "equals_1230": True}
        print(f"preflight {donor}-{arm}: source+donor input IDs EQUAL 1230 OK")
    result["preflight"] = preflight
    oat.validate_specs(specs, oat.SWEEP_CONFIGS)
    batch_file.write_text(json.dumps(specs, indent=2) + "\n")

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
                "first_32_prefix_text": tok.decode(gen["token_ids"][:32]) if len(gen["token_ids"]) >= 32 else None,
                "first_32_prefix_ids": gen["token_ids"][:32],
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
        # generation counts and EOS recording (AGENTS: state the actual token count);
        # the 32-token demo view is the FIRST-32 prefix of the exact 1230 config
        for row in (k8, kfull, c0):
            assert 0 < row["generation_count"] <= 128, row["generation_count"]
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
