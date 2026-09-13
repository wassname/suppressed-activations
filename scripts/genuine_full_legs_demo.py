# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Bounded genuine-full demonstration check (supervisor-approved scope): the ACTUAL
1230 complete-rank LEGS rows (dog 27-29, ant 33-35 in slop/complete_rank_batch.json,
copied verbatim; only output_dir redirected), arms k8/kfull/C0 per donor.

CPU first: preflight asserts rendered source+donor input IDs byte-equal to the saved
1230 results AND the row schema against the EXISTING completed fixture (zero parse
bugs on known fixtures; row['config'] is canonical — no markdown parsing). GPU rows
already completed with VERIFIED same config+code hash are REUSED, not rerun; only
missing rows run. Per row: ranks reported separately (source/donor/joint), kfull
projector containment of k8, per-position injection-norm monotonicity, C0 inertness,
distinct prefill/final readouts, count+EOS recorded, first-32 prefix recorded.
-- PI[glm-5p3-flash]"""
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

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "complete_rank_batch.json"
ROW_INDICES = {"dog": (27, 28, 29), "ant": (33, 34, 35)}  # ACTUAL 1230 legs rows
REF_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
PRIOR_ATTEMPTS = [ROOT / "out" / d for d in (
    "2026-09-13_genuine-full-legs-demo-125352",  # completed dog-k8 (verified reuse)
    "2026-09-13_genuine-full-legs-demo-130419",  # completed dog-kfull/C0, ant rows
)]


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def schema_check(row: dict, tag: str):
    """Assert every field the driver consumes exists and serializes (known fixture)."""
    for f in ("config", "generation", "base_generation", "readout", "last_decode_readout",
              "top_tokens", "swap_log_odds_shift", "bare_answer_mass",
              "repeated_bigram_fraction", "intervention_record", "code_sha256"):
        assert f in row, f"{tag}: missing {f}"
        try:
            json.dumps(row[f])
        except TypeError as e:
            raise AssertionError(f"{tag}: {f} not serializable: {e}")
    assert "common_temporal_full" in row["config"], f"{tag}: config lacks the full flag"


def main():
    out_dir = ROOT / "out" / f"2026-09-13_genuine-full-legs-demo-{time.strftime('%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=False)
    current_sha = {p: sha(p) for p in ("scripts/oat_sweep.py", "scripts/demo.py",
                                       "scripts/prompt.py", "suppressed_activation_subspace.py")}
    result = {"code_sha256": current_sha,
              "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                             cwd=ROOT, check=True, text=True,
                                             capture_output=True).stdout.strip(),
              "rows": {}, "preflight": {}, "reused_from": {}}

    batch_1230 = json.loads(BATCH.read_text())
    specs, prompts = [], {}
    for donor, (k8_i, kfull_i, c0_i) in ROW_INDICES.items():
        for arm, idx in (("k8_C1.5", k8_i), ("kfull_C1.5", kfull_i), ("C0", c0_i)):
            row = dict(batch_1230[idx])
            assert row["expected_condition"] == arm, (idx, row["expected_condition"])
            if arm == "kfull_C1.5":  # pre-model: the old batch's full-flag defect must not ride along
                assert row["expected_common_temporal_full"] is True
                assert row["expected_common_source_rank"] == 0 and row["expected_common_donor_rank"] == 0
            prompts[arm, donor] = (row["source_prompt"], row["target_prompt"],
                                   row["source_output"], row["target_output"])
            row["output_dir"] = str(out_dir / f"{donor}-{arm}")
            specs.append(row)
    batch_file = out_dir / "batch_spec.json"
    batch_file.write_text(json.dumps(specs, indent=2) + "\n")

    # CPU preflight 1: rendered input IDs byte-equal to the saved 1230 results
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=REF_REV)
    for (arm, donor), (src_p, tgt_p, _s, _t) in prompts.items():
        src_r = assistant_prefill_input_ids(tok, src_p, device="cpu", instruction=next(
            s for s in specs if s["expected_condition"] == arm and s["target_concept"] == donor)["prefill_instruction"])
        tgt_r = assistant_prefill_input_ids(tok, tgt_p, device="cpu", instruction=next(
            s for s in specs if s["expected_condition"] == arm and s["target_concept"] == donor)["prefill_instruction"])
        saved = json.load(open(ROOT / "out" / "2026-09-12_cb-cr8" /
                               f"k8-legs-L1-{donor}" / "result.json"))["rendered_inputs"]
        assert src_r["input_ids"].flatten().tolist() == saved["source"]["input_ids"], f"{donor} source != 1230"
        assert tgt_r["input_ids"].flatten().tolist() == saved["donor"]["input_ids"], f"{donor} donor != 1230"
        result["preflight"][f"{donor}-{arm}"] = {
            "source_prompt_repr": repr(src_p), "target_prompt_repr": repr(tgt_p),
            "equals_1230": True}
        print(f"preflight {donor}-{arm}: input IDs byte-equal 1230 OK")
    oat.validate_specs(specs, oat.SWEEP_CONFIGS)

    # CPU preflight 2: schema of the EXISTING completed fixture row
    completed = {}  # tag -> (dir, row result)
    for prior in PRIOR_ATTEMPTS:
        for row_dir in sorted(prior.glob("*-*_C1.5") if False else prior.glob("*-*")):
            res = row_dir / "result.json"
            if not res.exists():
                continue
            row = json.load(open(res))["rows"][0]
            tag = f"{row_dir.name.split('-')[0]}-{row['condition_id'].split('_')[-2]}_{row['condition_id'].split('_')[-1]}"
            try:
                schema_check(row, tag)
                same_hash = row["code_sha256"]["scripts/oat_sweep.py"] == current_sha["scripts/oat_sweep.py"]
                same_cfg = (row["config"]["common_temporal_full"] is False
                            and row["config"]["strength"] == 1.5
                            and row["config"]["common_source_rank"] == 8
                            and row["config"]["common_donor_rank"] == 8)
                if same_hash and same_cfg:
                    completed[tag] = (row_dir, row)
                    print(f"reusable completed row: {tag} at {row_dir}")
            except AssertionError as e:
                print(f"fixture {tag}: {e}")

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
    bundle = None
    try:
        missing = [s for s in specs
                   if f"{s['target_concept']}-{s['expected_condition']}" not in completed]
        if missing:
            bundle = oat.load_bundle()
        tok_full = bundle["tokenizer"] if bundle else tok
        cache = {"revision": bundle["revision"]}
        for position, spec in enumerate(specs):
            tag = f"{spec['target_concept']}-{spec['expected_condition']}"
            if tag in completed:
                row_dir, row = completed[tag]
                result["reused_from"][tag] = str(row_dir)
            else:
                capture.pop("spec", None)
                expected = spec.get("expected_detector_layers")
                oat.run_with_bundle(bundle, Path(spec["output_dir"]), extraction_cache=cache,
                                    batch_spec={"batch_file": str(batch_file), "index": position,
                                                "spec": dict(spec)},
                                    expected_detector_layers=expected,
                                    **oat.strip_spec_metadata(spec))
                row = json.load(open(Path(spec["output_dir"]) / "result.json"))["rows"][0]
                row_dir = Path(spec["output_dir"])
                spec_by_tag[tag] = capture.get("spec")
            schema_check(row, tag)
            gen = row["generation"]
            src_spec = spec_by_tag.get(tag)
            if src_spec:
                L = next(iter(src_spec))
                Qsrc = src_spec[L]["src"].float()
                Qd = src_spec[L]["donor_U"].float()
                # the captured src IS the joint support span; report joint + donor only
                ranks = {"joint": int(oat.joint_support(Qsrc[0], Qd).shape[1]),
                         "donor": int(Qd.shape[-1])}
            else:
                # reused row (no captured bases): config truncation parameters only,
                # labeled as such — NOT presented as measured ranks
                ranks = {"joint": None, "donor": row["config"]["common_donor_rank"],
                         "provenance": "config truncation params; no captured bases; "
                                       f"producer hash {row['code_sha256']['scripts/oat_sweep.py'][:12]}"}
            inj_norms = ([float(p.norm()) for p in src_spec[L]["donor_proj"]]
                         if src_spec else None)
            result["rows"][tag] = {
                "dir": str(row_dir), "config": row["config"],
                "generation_text": gen["text"],
                "generation_count": len(gen["token_ids"]),
                "eos_count": sum(1 for t in gen["token_ids"] if t == tok_full.eos_token_id),
                "first_32_prefix_text": tok.decode(gen["token_ids"][:32]),
                "readout_prefill": row["readout"], "readout_final": row["last_decode_readout"],
                "top_tokens": row["top_tokens"],
                "base_generation": row["base_generation"]["text"],
                "swap_log_odds_shift": row["swap_log_odds_shift"],
                "p_valid": row["bare_answer_mass"], "r2": row["repeated_bigram_fraction"],
                "ranks": ranks, "injection_norms_by_position": inj_norms,
                "code_sha256": row["code_sha256"]}
            print(f"row {tag}: gen {result['rows'][tag]['generation_count']} tok, "
                  f"swap {result['rows'][tag]['swap_log_odds_shift']:.3f}, "
                  f"r2 {result['rows'][tag]['r2']:.3f}, ranks {ranks}")
    finally:
        oat.intervention_hooks = orig_hooks

    _assert_contract(result, spec_by_tag)
    (out_dir / "demo_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"GENUINE-FULL LEGS DEMO PASS | {out_dir / 'demo_result.json'}")


def _assert_contract(result, spec_by_tag):
    rows = result["rows"]
    for donor in ("dog", "ant"):
        k8, kfull, c0 = (rows[f"{donor}-{a}"] for a in ("k8_C1.5", "kfull_C1.5", "C0"))
        assert k8["config"]["common_temporal_full"] is False, "k8 must be non-full"
        assert kfull["config"]["common_temporal_full"] is True, "kfull must be temporal-full"
        assert c0["config"]["strength"] == 0.0
        if k8["ranks"]["joint"] is None:
            # reused k8 row (no captured bases): config bounds the joint at 8+8=16;
            # the fixed criterion uses that upper bound (measured siblings hit 16)
            assert kfull["ranks"]["joint"] is not None and kfull["ranks"]["joint"] > 16, \
                f"full joint support must exceed the k8 8+8 bound: {kfull['ranks']}"
        else:
            assert 8 <= k8["ranks"]["joint"] <= 16, \
                f"k8 joint support out of range (8+8 bound): {k8['ranks']}"
            assert kfull["ranks"]["joint"] > k8["ranks"]["joint"], \
                f"full joint support must exceed the k8 joint: {kfull['ranks']} vs {k8['ranks']}"
        assert kfull["ranks"]["donor"] > k8["ranks"].get("donor", 8), \
            f"full supported donor rank must exceed k8: {kfull['ranks']} vs {k8['ranks']}"
        for row in (k8, kfull, c0):
            assert 0 < row["generation_count"] <= 128, row["generation_count"]
        assert c0["generation_text"] == c0["base_generation"], \
            "C0 row diverged from its own base generation"
        assert k8["readout_prefill"] is not None and k8["readout_final"] is not None
        # NOTE: no monotonicity assertion across token positions — there is no
        # mathematical basis for donor-projection norms to be sorted; removed.
        # projector containment, PER POSITION (no cross-position reshaping):
        # Q8[p] (d×8) must lie in the span of Qfull[p] (d×Rf)
        k8_spec, full_spec = spec_by_tag.get(f"{donor}-k8_C1.5"), spec_by_tag.get(f"{donor}-kfull_C1.5")
        if k8_spec and full_spec:
            L = next(iter(k8_spec))
            Q8 = k8_spec[L]["src"].float()      # (positions, hidden, 8)
            Qf = full_spec[L]["src"].float()    # (positions, hidden, Rf)
            conts = []
            for p in range(Q8.shape[0]):
                q8, qf = Q8[p], Qf[p]
                resid = q8 - qf @ (qf.T @ q8)
                conts.append(float(resid.norm() / q8.norm()))
            result["rows"][f"{donor}-kfull_C1.5"]["k8_in_kfull_containment_by_position"] = conts
            assert max(conts) < 1e-4, f"{donor}: k8 not contained in kfull span: {conts}"
        else:
            result["rows"][f"{donor}-kfull_C1.5"]["k8_in_kfull_containment_by_position"] = \
                f"unavailable: no captured bases (see cpu_basis_check artifacts)"


if __name__ == "__main__":
    main()
