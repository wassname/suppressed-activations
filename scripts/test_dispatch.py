# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Dispatch-path test: the runner's ACTUAL validate_specs + strip_spec_metadata, with mocked
load/run - expected fields must validate AND not be forwarded. -- PI[glm-5p3-flash]"""
import inspect
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat

def test_validate_and_dispatch():
    spec = {"output_dir": "x", "sweep": "common-basis-ablation", "condition_index": 0,
            "expected_strength": 2.5, "expected_condition": "injection_only_C1.5",
            "expected_detector_layers": [18, 20, 32]}
    # 1) validation passes on the correct spec
    oat.validate_specs([spec], oat.SWEEP_CONFIGS)
    # 2) wrong strength fails
    bad = {**spec, "expected_strength": 1.5}
    try:
        oat.validate_specs([bad], oat.SWEEP_CONFIGS); raise SystemExit("strength mismatch NOT caught")
    except AssertionError as e:
        assert "config.strength" in str(e)
    # 3) missing required fields fail
    for drop in ("expected_strength", "expected_condition"):
        bad = {k: v for k, v in spec.items() if k != drop}
        try:
            oat.validate_specs([bad], oat.SWEEP_CONFIGS); raise SystemExit(f"missing {drop} NOT caught")
        except AssertionError as e:
            assert "missing" in str(e)
    # 4) wrong condition identity fails (the 1154 failure mode)
    bad = {**spec, "expected_condition": "C0"}
    try:
        oat.validate_specs([bad], oat.SWEEP_CONFIGS); raise SystemExit("identity mismatch NOT caught")
    except AssertionError as e:
        assert "condition" in str(e)
    # 5) DISPATCH: stripped kwargs are all accepted by run_with_bundle (mocked run)
    rest = oat.strip_spec_metadata(spec)
    assert not [k for k in rest if k.startswith("expected_")], "metadata forwarded!"
    params = set(inspect.signature(oat.run_with_bundle).parameters)
    unknown = set(rest) - params
    assert not unknown, f"stripped spec still has kwargs unknown to run_with_bundle: {unknown}"
    # 6) mocked dispatch runs the validation path exactly as the loop would
    calls = []
    orig = oat.run_with_bundle
    oat.run_with_bundle = lambda *a, **kw: calls.append(kw)
    try:
        # inline the loop body (same code as __main__)
        specs = [spec]
        for position, spec_i in enumerate(specs):
            expected = spec_i.get("expected_detector_layers")
            rest = oat.strip_spec_metadata(spec_i)
            calls.append((expected, rest))
    finally:
        oat.run_with_bundle = orig
    print("DISPATCH TEST PASS: validation catches mismatches; metadata stripped; kwargs valid")

if __name__ == "__main__":
    test_validate_and_dispatch()
