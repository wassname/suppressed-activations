# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""CPU-only registration/contract test: resolve EVERY registry choice (calls each family),
then validate the given batch specs through the runner's ACTUAL validate_specs (no model
load, no duplicate logic). Run: uv run --offline scripts/test_registration.py [spec.json...]
-- PI[glm-5p3-flash]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat


EXPECTED = {  # independent expected values (hand-written, not read from the families)
    "snapshot-h8": {"expected_strength": 1.5, "expected_condition": "snapshot_h8_C1.5",
                    "expected_selector": "snapshot", "expected_site": 8,
                    "expected_detector_layers": [23, 25, 32]},
    "increment-h8": {"expected_strength": 1.5, "expected_condition": "increment_h8_C1.5",
                     "expected_selector": "increment", "expected_site": 8,
                     "expected_detector_layers": [23, 25, 32]},
    "snapshot-h20": {"expected_strength": 1.5, "expected_condition": "snapshot_h20_C1.5",
                     "expected_selector": "snapshot", "expected_site": 20,
                     "expected_detector_layers": [23, 25, 32]},
    "increment-h20": {"expected_strength": 1.5, "expected_condition": "increment_h20_C1.5",
                      "expected_selector": "increment", "expected_site": 20,
                      "expected_detector_layers": [23, 25, 32]},
    "random-h8": {"expected_strength": 1.5, "expected_condition": "random_h8_C1.5",
                  "expected_selector": "snapshot", "expected_site": 8,
                  "expected_detector_layers": [23, 25, 32]},
    "random-h20": {"expected_strength": 1.5, "expected_condition": "random_h20_C1.5",
                   "expected_selector": "snapshot", "expected_site": 20,
                   "expected_detector_layers": [23, 25, 32]},
    "C0": {"expected_strength": 0.0, "expected_condition": "C0",
           "expected_selector": "snapshot", "expected_site": 8,
           "expected_detector_layers": [23, 25, 32]},
}


# independent expectations, keyed by output-dir condition prefix. All keys are Config
# fields with the expected_ prefix (validate_specs resolves them via getattr(cfg, field)):
# selector/site/basis/removal/rank/window/positions are all real Config fields.
EXPECTED = {
    "snapshot-h8": {"expected_strength": 1.5, "expected_condition": "snapshot_h8_C1.5",
                    "expected_common_selector": "snapshot", "expected_intervention_layer": [8],
                    "expected_common_basis": "top8_union", "expected_common_removal": "joint",
                    "expected_rank": 8, "expected_common_window": 4,
                    "expected_intervention_positions": 3,
                    "expected_detector_layers": [23, 25, 32]},
    "increment-h8": {"expected_strength": 1.5, "expected_condition": "increment_h8_C1.5",
                     "expected_common_selector": "increment", "expected_intervention_layer": [8],
                     "expected_common_basis": "top8_union", "expected_common_removal": "joint",
                     "expected_rank": 8, "expected_common_window": 4,
                     "expected_intervention_positions": 3,
                     "expected_detector_layers": [23, 25, 32]},
    "snapshot-h20": {"expected_strength": 1.5, "expected_condition": "snapshot_h20_C1.5",
                     "expected_common_selector": "snapshot", "expected_intervention_layer": [20],
                     "expected_common_basis": "top8_union", "expected_common_removal": "joint",
                     "expected_rank": 8, "expected_common_window": 4,
                     "expected_intervention_positions": 3,
                     "expected_detector_layers": [23, 25, 32]},
    "increment-h20": {"expected_strength": 1.5, "expected_condition": "increment_h20_C1.5",
                      "expected_common_selector": "increment", "expected_intervention_layer": [20],
                      "expected_common_basis": "top8_union", "expected_common_removal": "joint",
                      "expected_rank": 8, "expected_common_window": 4,
                      "expected_intervention_positions": 3,
                      "expected_detector_layers": [23, 25, 32]},
    "random-h8": {"expected_strength": 1.5, "expected_condition": "random_h8_C1.5",
                  "expected_common_selector": "snapshot", "expected_intervention_layer": [8],
                  "expected_common_basis": "random_shared", "expected_common_removal": "joint",
                  "expected_common_random_rank": 8, "expected_common_window": 4,
                  "expected_intervention_positions": 3,
                  "expected_detector_layers": [23, 25, 32]},
    "random-h20": {"expected_strength": 1.5, "expected_condition": "random_h20_C1.5",
                   "expected_common_selector": "snapshot", "expected_intervention_layer": [20],
                   "expected_common_basis": "random_shared", "expected_common_removal": "joint",
                   "expected_common_random_rank": 8, "expected_common_window": 4,
                   "expected_intervention_positions": 3,
                   "expected_detector_layers": [23, 25, 32]},
    "C0": {"expected_strength": 0.0, "expected_condition": "C0",
           "expected_common_selector": "snapshot", "expected_intervention_layer": [8],
           "expected_common_basis": "top8_union", "expected_common_removal": "joint",
           "expected_rank": 8, "expected_common_window": 4,
           "expected_intervention_positions": 3,
           "expected_detector_layers": [23, 25, 32]},
}


def enrich_specs(specs: list[dict]) -> list[dict]:
    """Attach independent expectations WITHOUT letting the spec override them: conflicts
    are separate entries that fail validation (the independent value wins)."""
    out = []
    for spec in specs:
        dirname = Path(spec["output_dir"]).name
        for prefix, exp in EXPECTED.items():
            if dirname.startswith(prefix + "-") or dirname == prefix:
                merged = {**spec}
                for k, v in exp.items():
                    if k in spec and spec[k] != v:
                        # a spec expectation CONFLICTING with the independent value is a
                        # spec error: fail it (neither silently overrides)
                        raise AssertionError(
                            f"spec expectation conflict on {k}: spec {spec[k]!r} != "
                            f"independent {v!r} ({dirname})")
                out.append(merged)
                break
        else:
            out.append({**spec, "expected_condition": "UNMATCHED-PREFIX"})
    return out


def main(spec_paths: list[Path]) -> None:
    registry = oat.SWEEP_CONFIGS
    text = (Path(__file__).resolve().parents[1] / "scripts/oat_sweep.py").read_text()
    failures = []
    if "choices=tuple(sorted(SWEEP_CONFIGS))" not in text:
        failures.append("argparse --sweep choices do not derive from SWEEP_CONFIGS")
    for choice in sorted(registry):
        try:
            rows = registry[choice]()
            assert rows, f"{choice}: family returned no rows"
            for axis, value, cfg in rows:
                assert cfg is not None
        except Exception as e:  # noqa: BLE001
            failures.append(f"choice {choice!r}: {type(e).__name__}: {e}")
    bank_hashes = {}
    bank_manifest = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3/manifest.json"
    if bank_manifest.exists():
        for name, e in json.load(open(bank_manifest))["entries"].items():
            bank_hashes[(e["cell_id"], e["side"])] = e["rendered_input_sha256"]
    for spec_path in spec_paths:
        try:
            entries = json.loads(spec_path.read_text())
            if "selsite" in spec_path.name:
                entries = enrich_specs(entries)  # independent expected values attached
                # bank linkage: every spec cell id must exist in the exact-input bank
                # (rendered-ID equality was verified 24/24 at capture and re-asserted by
                # the runner's preflight before capture; here the spec<->bank linkage)
                cell_ids = {bc for bc, _ in bank_hashes}
                uncovered = [e["output_dir"] for e in entries
                             if not any(bc in e["output_dir"] for bc in cell_ids)]
                assert not uncovered, f"specs without bank coverage: {uncovered[:3]}"
            oat.validate_specs(entries, registry)
        except Exception as e:  # noqa: BLE001
            failures.append(f"spec {spec_path.name}: {type(e).__name__}: {e}")
    if failures:
        print("REGISTRATION TEST FAILURES:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"REGISTRATION TEST PASS: {len(registry)} registry choices resolved; "
          f"{len(spec_paths)} spec files validated (no model load).")


if __name__ == "__main__":
    main([Path(a) for a in sys.argv[1:]])
