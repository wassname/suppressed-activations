# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""CPU reconstruction of the ACTUAL k8/kfull bases for the legs rows, using the SAME
production run_with_bundle construction (no GPU): runs each basis row on CPU with
max_new_tokens=2, spy-captures the built common_specs, and saves the per-position
Q8/Qfull basis artifacts. The demo driver then asserts per-position orthonormality
and nesting from these artifacts. This is metadata reconstruction, not a results run.
-- PI[glm-5p3-flash]"""
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("SUPPRESSED_DEVICE", "cpu")  # CPU reconstruction by design
import torch
torch.set_grad_enabled(False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "complete_rank_batch.json"
ROW_INDICES = {"dog": (27, 28), "ant": (33, 34)}  # k8 + kfull only
OUT = ROOT / "out" / f"2026-09-13_cpu-basis-check-{time.strftime('%H%M%S')}"


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    batch_1230 = json.loads(BATCH.read_text())
    capture: dict = {}
    orig_hooks = oat.intervention_hooks

    def spy_hooks(*a, **kw):
        hooks = orig_hooks(*a, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs"):
            capture["spec"] = {L: {k: (v.clone() if isinstance(v, torch.Tensor) else v)
                                   for k, v in d.items()}
                               for L, d in kw["common_specs"].items()}
        return hooks

    oat.intervention_hooks = spy_hooks
    report = {}
    try:
        bundle = oat.load_bundle()
        cache = {"revision": bundle["revision"]}
        for donor, (k8_i, kfull_i) in ROW_INDICES.items():
            for arm, idx in (("k8_C1.5", k8_i), ("kfull_C1.5", kfull_i)):
                spec = dict(batch_1230[idx])
                spec["output_dir"] = str(OUT / f"{donor}-{arm}")
                capture.pop("spec", None)
                oat.run_with_bundle(bundle, Path(spec["output_dir"]),
                                    extraction_cache=cache,
                                    batch_spec={"batch_file": str(BATCH), "index": idx,
                                                "spec": spec},
                                    expected_detector_layers=spec.get("expected_detector_layers"),
                                    **oat.strip_spec_metadata(spec))
                assert "spec" in capture, f"{donor}-{arm}: spec not captured"
                tag = f"{donor}-{arm}"
                L = next(iter(capture["spec"]))
                Q = capture["spec"][L]["src"].float()   # (positions, hidden, R)
                Qd = capture["spec"][L]["donor_U"].float()
                torch.save({"Q_src": Q, "Q_donor": Qd, "tag": tag, "layer": L},
                           OUT / f"basis_{tag}.pt")
                report[tag] = {"joint_cols": int(Q.shape[-1]), "donor_cols": int(Qd.shape[-1]),
                               "positions": int(Q.shape[0]), "artifact": str(OUT / f"basis_{tag}.pt")}
                print(f"{tag}: joint {Q.shape[-1]} cols, donor {Qd.shape[-1]} cols, "
                      f"{Q.shape[0]} positions -> {OUT / f'basis_{tag}.pt'}")
    finally:
        oat.intervention_hooks = orig_hooks
    (OUT / "cpu_basis_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"CPU BASIS ARTIFACTS SAVED | {OUT / 'cpu_basis_report.json'}")


if __name__ == "__main__":
    main()
