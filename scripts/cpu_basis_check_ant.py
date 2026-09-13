# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Complete the basis check for the ANT pair only (dog artifacts already valid in
out/2026-09-13_cpu-basis-check-131429/). Zero-generation capture: the spy raises
SpecCaptured inside intervention_hooks immediately after the spec is built, BEFORE any
generation starts; the script catches ONLY that exception. Also captures the donor
anchor states so the donor-projection nesting (full >= k8 at the SAME donor
state/offset, no sorting across positions) is computed from actual states.
CPU only; runs through the real run_with_bundle construction.
-- PI[glm-5p3-flash]"""
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("SUPPRESSED_DEVICE", "cpu")
import torch
torch.set_grad_enabled(False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.oat_sweep as oat

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "slop" / "complete_rank_batch.json"
BASIS_DIR = ROOT / "out" / "2026-09-13_cpu-basis-check-131429"
ANCHOR_LAYER = 25  # xdepth_anchor_layer, verified in the batch rows


class SpecCaptured(Exception):
    pass


def main():
    batch_1230 = json.loads(BATCH.read_text())
    assert all(batch_1230[i]["expected_common_temporal_full"] is True
               for i in (34,)) and batch_1230[33]["expected_common_temporal_full"] is False
    report = {}
    orig = oat.intervention_hooks
    current = {}

    def spy(*args, **kw):
        hooks = orig(*args, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs") and "tag" in current:
            L = next(iter(kw["common_specs"]))
            Q = kw["common_specs"][L]["src"].float().clone()
            Qd = kw["common_specs"][L]["donor_U"].float().clone()
            dproj = kw["common_specs"][L]["donor_proj"].float().clone()
            res = args[2]  # target (donor) residuals: (layers+1, seq, hidden)
            c_end = kw["source_position"] + 1
            pos = kw["positions"]
            v = torch.stack([res[ANCHOR_LAYER, c_end - pos + p].float() for p in range(pos)])
            current["Q_src"], current["Q_donor"], current["Q_proj"] = Q, Qd, dproj
            current["v_donor_states"] = v
            raise SpecCaptured  # before any generation starts

    oat.intervention_hooks = spy
    try:
        bundle = oat.load_bundle()
        cache = {"revision": bundle["revision"]}
        for donor, (k8_i, kfull_i) in (("ant", (33, 34)),):
            for arm, idx in (("k8_C1.5", k8_i), ("kfull_C1.5", kfull_i)):
                spec = dict(batch_1230[idx])
                spec["output_dir"] = str(BASIS_DIR / f"{donor}-{arm}")
                current["tag"] = f"{donor}-{arm}"
                try:
                    with_ref = oat.run_with_bundle(
                        bundle, Path(spec["output_dir"]), extraction_cache=cache,
                        batch_spec={"batch_file": str(BATCH), "index": idx, "spec": spec},
                        expected_detector_layers=spec.get("expected_detector_layers"),
                        **oat.strip_spec_metadata(spec))
                except SpecCaptured:
                    pass  # the only expected exit path; generation never started
                else:
                    raise AssertionError(f"{donor}-{arm}: run completed without capture")
                L = 1
                Q, Qd, dproj = current["Q_src"], current["Q_donor"], current["Q_proj"]
                v = current["v_donor_states"]
                torch.save({"Q_src": Q, "Q_donor": Qd, "Q_proj": dproj,
                            "v_donor_states": v, "tag": f"{donor}-{arm}", "layer": L,
                            "anchor_layer": ANCHOR_LAYER},
                           BASIS_DIR / f"basis_{donor}-{arm}.pt")
                report[f"{donor}-{arm}"] = {"joint_cols": int(Q.shape[-1]),
                                            "donor_cols": int(Qd.shape[-1]),
                                            "positions": int(Q.shape[0])}
                print(f"{donor}-{arm}: joint {Q.shape[-1]}, donor {Qd.shape[-1]}, "
                      f"{Q.shape[0]} positions, donor states captured -> artifacts saved")
    finally:
        oat.intervention_hooks = orig
    report.update(dog_files="preserved from 131429 (k8/kfull)", capture_mode="zero-generation")
    (BASIS_DIR / "cpu_basis_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"ANT BASIS ARTIFACTS SAVED | {BASIS_DIR / 'cpu_basis_report.json'}")


if __name__ == "__main__":
    main()
