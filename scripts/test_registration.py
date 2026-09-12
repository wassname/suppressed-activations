# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""CPU-only registration test: resolve EVERY advertised --sweep choice through the actual
registration dict and parse batch specs to resolved configs — no model load. Catches
choices/dict divergence and missing family functions before queueing.
Run: uv run --offline scripts/test_registration.py [spec.json ...] -- PI[claude]"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat

# runner_union_basis-style tolerance helper for spec resolution is not needed here; the
# test only resolves configs (function calls), never loads a model.


def main(specs: list[Path]) -> None:
    # single source of truth: the module-level registry; argparse choices are DERIVED from it
    registry = oat.SWEEP_CONFIGS
    text = (Path(__file__).resolve().parents[1] / "scripts/oat_sweep.py").read_text()
    failures = []
    if "choices=tuple(sorted(SWEEP_CONFIGS))" not in text:
        failures.append("argparse --sweep choices do not derive from SWEEP_CONFIGS "
                        "(divergence possible again)")
    for choice in sorted(registry):
        try:
            rows = registry[choice]()
            assert rows, f"{choice}: family returned no rows"
            for axis, value, cfg in rows:
                assert cfg is not None
        except Exception as e:  # noqa: BLE001 - report every resolution failure
            failures.append(f"choice {choice!r}: {type(e).__name__}: {e}")
    for spec_path in specs:
        try:
            entries = json.loads(Path(spec_path).read_text())
            for i, spec in enumerate(entries):
                choice = spec["sweep"]
                assert choice in registry, f"spec[{i}] sweep {choice!r} not in registry"
                rows = registry[choice]()
                idx = spec["condition_index"]
                assert idx < len(rows), f"spec[{i}] condition_index {idx} out of range ({len(rows)})"
                if "expected_condition" in spec:
                    # identity check: idx-in-range can still map to the WRONG condition
                    # (the 1154 incident: idx2 was in range but was C0, labeled A-replay)
                    got = rows[idx][1]
                    assert got == spec["expected_condition"], \
                        f"spec[{i}]: condition {idx} is {got!r}, expected {spec['expected_condition']!r}"
                if "expected_detector_layers" in spec:
                    got = list(rows[idx][2].detector_layers)
                    assert got == list(spec["expected_detector_layers"]), \
                        f"spec[{i}]: resolved selector {got} != requested {spec['expected_detector_layers']}"
                # full CONTRACT fields: any expected_<field> is checked against the resolved
                # config (strength, removal span, inject axes, site, wrapper, ...) - the
                # 1158 incident: strength ran at DEFAULT 2.5 while labels said C1.5
                cfg_res = rows[idx][2]
                for key, want in spec.items():
                    if not key.startswith("expected_") or key == "expected_detector_layers":
                        continue
                    field = key[len("expected_"):]
                    got = getattr(cfg_res, field, None)
                    got = list(got) if isinstance(got, tuple) else got
                    want = list(want) if isinstance(want, tuple) else want
                    assert got == want, f"spec[{i}]: config.{field} = {got!r} != expected {want!r}"
        except Exception as e:  # noqa: BLE001
            failures.append(f"spec {spec_path.name}: {type(e).__name__}: {e}")
    if failures:
        print("REGISTRATION TEST FAILURES:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"REGISTRATION TEST PASS: {len(registry)} registry choices resolved; "
          f"{len(specs)} spec files parsed to resolved configs (no model load).")


if __name__ == "__main__":
    main([Path(a) for a in sys.argv[1:]])
