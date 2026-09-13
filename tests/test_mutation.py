# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""PERMANENT mutation tests: each wrong independent expectation must FAIL validation.
-- PI[glm-5p3-flash]"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.test_registration as tr

def test_mutations():
    base = json.load(open(Path(__file__).resolve().parents[1] / "slop/common_basis_selsite_batch.json"))
    for name, patch, idx in (("selector", {"expected_common_selector": "increment"}, 0),
                             ("site", {"expected_intervention_layer": [20]}, 0),
                             ("basis", {"expected_common_basis": "random_shared"}, 0),
                             ("removal", {"expected_common_removal": "source"}, 0),
                             ("strength", {"expected_strength": 2.5}, 0)):
        try:
            bad = tr.enrich_specs([{**base[idx], **patch}])
        except AssertionError:
            # independent-expectation conflict at enrich time is also a caught mutation
            continue
        try:
            import scripts.oat_sweep as oat
            oat.validate_specs(bad, oat.SWEEP_CONFIGS)
            raise AssertionError(f"mutation {name} NOT caught")
        except AssertionError as e:
            # caught either as a config mismatch or a spec-vs-independent conflict
            assert ("!= expected" in str(e) or "condition" in str(e)
                    or "expectation conflict" in str(e)), e
    print("MUTATION TEST PASS: 5/5 wrong expectations caught")

if __name__ == "__main__":
    test_mutations()
