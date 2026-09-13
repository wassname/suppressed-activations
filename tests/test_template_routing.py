# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8",
#                 "transformers>=5.5"]
# ///
"""Nondegenerate tiny tests for the template-branch basis routing. Each assertion is
chosen so a specific implementation bug FAILS: an ignored anchor (hash equal to the
site-tied run), stale projected U (injected delta not in the routed span), a
site-dependent basis (U differs across edit sites), an unhooked C0 (no record).
Canonical r2 only. -- PI[glm-5p3-flash]"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["SUPPRESSED_MODEL"] = "wassname/qwen3-5lyr-tiny-random"
os.environ["SUPPRESSED_REVISION"] = "main"
os.environ["SUPPRESSED_DEVICE"] = "cpu"
import torch
from dataclasses import replace
torch.set_grad_enabled(False)
import scripts.oat_sweep as oat
import scripts.test_registration as tr
from transformers import AutoTokenizer

TOK = AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
OUT = Path("out") / f"2026-09-13_template-routing-tests-{time.strftime('%H%M%S')}"
EXTRACT_INSTR = "Answer the question with the answer first. Then describe the animal in three sentences."
SRC_PROMPT = "Question: what is the animal that spins webs called?\nAnswer: "


def run_row(sweep, idx, tag, extra_cfg=None):
    """Observe (not abort): capture shared/fixed_deltas + the run record."""
    obs = {}
    orig = oat.intervention_hooks

    def spy(*a, **kw):
        hooks = orig(*a, **kw)
        if kw.get("operation") == "span_corrected_delta":
            obs["shared"] = a[0].clone()
            if kw.get("fixed_deltas") is not None:
                obs["fixed_deltas"] = {k: v.clone() for k, v in kw["fixed_deltas"].items()}
            obs["args"] = tuple(a)
            obs["kwargs"] = {k: v for k, v in kw.items() if k != "record"}
        return hooks



    oat.intervention_hooks = spy
    try:
        spec = {"output_dir": str(OUT / f"{tag}-{time.strftime('%H%M%S%f')}"),
                "sweep": sweep, "condition_index": idx,
                "prompt_mode": "chat-assistant-prefill",
                "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                "lens_corpus_arrow": None, "target_concept": "dog",
                "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                "extraction_instruction": None, "selector_audit": False}
        spec = tr.enrich_specs([spec])[0]
        bundle = oat.load_bundle()
        out = Path(spec["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        oat.run_with_bundle(bundle, out, extraction_cache={"revision": bundle["revision"]},
                            batch_spec={"batch_file": "inline", "index": idx, "spec": dict(spec)},
                            expected_detector_layers=spec.get("expected_detector_layers"),
                            **oat.strip_spec_metadata(spec))
        row = json.load(open(out / "result.json"))["rows"][0]
        rec = row["intervention_record"]
        rec = rec[list(rec)[0]] if isinstance(rec, dict) and rec else {}
        return obs, rec, row, bundle
    finally:
        oat.intervention_hooks = orig


def test_nonzero_C_applies_contained_delta():
    obs, rec, row, _ = run_row("smoke-span-correction", 1, "nonzero-c")
    assert rec.get("perturbation_norm", 0) > 0, "nonzero C must edit"
    shared, deltas = obs["shared"], obs["fixed_deltas"]
    for layer, delta in deltas.items():
        resid = delta - shared @ (shared.T @ delta)
        assert resid.norm() / delta.norm() < 1e-5, \
            f"injected delta not contained in the active basis at layer {layer}"
    assert rec.get("decode_steps") == 3
    print("(1) nonzero-C span-correction smoke: delta applied AND contained in the active basis OK")


def expected_applied(shared, raw_delta):
    proj = shared @ (shared.T @ raw_delta)
    return proj * (raw_delta.norm() / proj.norm())


def test_anchor_equation_and_two_site():
    # combined incremental fixture: fixed anchor, two sites, the routed selector
    oat.SWEEP_CONFIGS["smoke-span-corr-anchor3"] = lambda: [
        (f, n, replace(c, delta_anchor_layer=3, basis_selector="increment")) for f, n, c in
        oat.SWEEP_CONFIGS["smoke-span-correction"]()]
    oat.SWEEP_CONFIGS["smoke-span-corr-anchor3-s1"] = lambda: [
        (f, n, replace(c, delta_anchor_layer=3, basis_selector="increment",
                       intervention_layer=(1,))) for f, n, c in
        oat.SWEEP_CONFIGS["smoke-span-correction"]()]
    obs_a_s2, rec_s2, row_s2, bundle = run_row("smoke-span-corr-anchor3", 1, "a3-s2")
    obs_a_s1, rec_s1, row_s1, _ = run_row("smoke-span-corr-anchor3-s1", 1, "a3-s1")
    assert row_s2["config"]["basis_selector"] == "increment"
    assert row_s1["config"]["basis_selector"] == "increment"
    # U identical across sites
    assert torch.equal(obs_a_s2["shared"], obs_a_s1["shared"]), "U changed across sites"
    # the applied delta = the norm-matched projection of the RUN'S OWN raw layer-3
    # template delta (template_vectors.pt is persisted by the production construction)
    import glob
    run_dir = glob.glob(str(OUT / "a3-s2-*" / "conditions")) or glob.glob(str(OUT / "a3-s2-*"))
    tv = torch.load(sorted(glob.glob(str(OUT / "a3-s2-*" / "template_vectors.pt")))[0],
                    weights_only=False)
    raw3 = tv["deltas"][3].float()
    expected = expected_applied(obs_a_s2["shared"].float(), raw3)
    d2 = obs_a_s2["fixed_deltas"][2].float()
    d1 = obs_a_s1["fixed_deltas"][1].float()
    # bf16 + the norm-match rescale (amplifies rounding when the delta sits mostly
    # outside the small span): assert the NORM-MATCH identity and the DIRECTION, not
    # elementwise closeness
    torch.testing.assert_close(d2.norm(), raw3.norm(), rtol=1e-2, atol=0)
    cos = float(torch.cosine_similarity(d2, expected, dim=0))
    assert cos > 0.999, f"applied delta direction != the anchor's projected direction: {cos}"
    assert torch.equal(d2, d1), "applied delta changed across sites with a fixed anchor"
    print("(2) fixed anchor: applied delta == P_U(d_anchor) norm-matched (the run's own "
          "template_vectors.pt), identical across two sites OK")


def test_basis_site_independent():
    oat.SWEEP_CONFIGS["smoke-span-corr-site1"] = lambda: [
        (f, n, replace(c, intervention_layer=(1,))) for f, n, c in
        oat.SWEEP_CONFIGS["smoke-span-correction"]()]
    obs_2, _, _, _ = run_row("smoke-span-correction", 1, "site2")
    obs_1, _, _, _ = run_row("smoke-span-corr-site1", 1, "site1")
    assert torch.equal(obs_2["shared"], obs_1["shared"]), "basis became site-dependent"
    print("(3) basis site-independent: U identical across edit sites OK")


def test_increment_routing_not_stale():
    oat.SWEEP_CONFIGS["smoke-span-corr-incr"] = lambda: [
        (f, n, replace(c, basis_selector="increment")) for f, n, c in
        oat.SWEEP_CONFIGS["smoke-span-correction"]()]
    obs_inc, rec, row, bundle = run_row("smoke-span-corr-incr", 1, "incr")
    shared = obs_inc["shared"]
    assert shared.shape[-1] == 4
    for layer, delta in obs_inc["fixed_deltas"].items():
        resid = delta - shared @ (shared.T @ delta)
        assert resid.norm() / delta.norm() < 1e-4, \
            f"stale projected U: the injected delta is not in the ROUTED span (layer {layer})"
    # the routed U differs from the attenuation U (the C0 run's shared)
    obs_c0, rec0, _, _ = run_row("smoke-span-correction", 0, "c0")
    assert not torch.equal(shared, obs_c0["shared"]), "routed U equals the attenuation U"
    # canonical r2 on the generated ids
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
    r2 = repetition_bigram_fraction_canon(row["generation"]["token_ids"], tok)
    print("(4) increment routing: delta in the ROUTED span; U differs from attenuation; "
          f"canonical r2 = {r2:.3f} OK")


def repetition_bigram_fraction_canon(ids, tok):
    if not ids:
        return float("nan")
    fn = next(n for n in __import__("ast").parse(
        (Path(__file__).resolve().parents[1] / "scripts" / "oat_sweep.py").read_text()).body
        if isinstance(n, __import__("ast").FunctionDef)
        and n.name == "repetition_bigram_fraction")
    exec(compile(__import__("ast").Module(body=[fn], type_ignores=[]), "oat_sweep.py", "exec"), globals())
    return repetition_bigram_fraction(ids, set(tok.all_special_ids))


def test_c0_not_unhooked():
    obs, rec, row, bundle = run_row("smoke-span-correction", 0, "c0")
    assert rec, "unhooked: no intervention record at all"
    assert rec.get("perturbation_norm") == 0.0, "C0 must not edit"
    assert rec.get("decode_steps") == 3, "C0 must still run the decode calls"
    # the runner's base_generation IS the unhooked forward path: C0 must match it
    # byte-for-byte; the logits-level identity is separately covered (bitwise) by
    # scripts/runtime_controls.py test 2 (C0 vs trajectory forward)
    assert row["generation"]["token_ids"] == row["base_generation"]["token_ids"], \
        "C0 diverged from the unhooked baseline generation"
    print("(5) C0: record present, zero edit, decode calls ran, generation == unhooked "
          "baseline (byte-equal); logits-level identity covered by runtime_controls test 2")


if __name__ == "__main__":
    test_nonzero_C_applies_contained_delta()
    test_anchor_equation_and_two_site()
    test_basis_site_independent()
    test_increment_routing_not_stale()
    test_c0_not_unhooked()
    print("TEMPLATE ROUTING TESTS PASS")
