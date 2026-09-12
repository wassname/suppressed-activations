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
    for spec_path in spec_paths:
        try:
            entries = json.loads(spec_path.read_text())
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
