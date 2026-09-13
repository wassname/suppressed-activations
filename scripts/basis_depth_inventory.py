# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8", "transformers>=5.5"]
# ///
"""Bank inventory: what does the ACTUAL increment rank-4 basis select across depth?

CPU only, existing att3 bank arrays (the 1230-family exact inputs — the current
recipe's dev family), production code only (increment_scores/subspace_from_scores).
Outputs: per-position selected IDs + decoded labels (wrapper positions included), the
union-SVD rank-4 U with per-direction contributions, and the 33-layer score shape of
each selected direction (where its variation lives vs the intended build-then-late-cut).
NOTES: the att3 bank does NOT cover the 2026-09-10 bridge prompts (wording differs;
verified) — a minimal 24-forward capture (no generation) would be needed for those.
The runner's row['readout'] field is the CHANGED-readout vocab list, not the basis IDs.
-- PI[glm-5p3-flash]"""
import json
import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
D = ROOT / "out" / "2026-09-12_exact-input-bank-att3"
OUT = ROOT / "out" / "2026-09-13_basis-depth-inventory"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B",
                                        revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    U_all = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()
    rown = (gain * U_all).norm(dim=-1)
    report = {}
    for stem in ("legs-L1-dog-source", "legs-L1-dog-donor", "legs-L1-ant-donor"):
        res = torch.load(D / f"{stem}_residuals.pt", weights_only=False).float()
        seq = res.shape[1]
        sc = increment_scores(res.permute(1, 0, 2), U_all, gain,
                              normalize_unembedding_rows=True)
        # readout positions: the last 4 content positions (wrapper included)
        rpos = [seq - 4, seq - 3, seq - 2, seq - 1]
        sel = {}
        for p in rpos:
            ids8 = sc[p].topk(8).indices.tolist()
            sel[p] = {"ids": ids8, "labels": [tok.decode([t]) for t in ids8],
                      "scores": [float(sc[p, t]) for t in ids8]}
        # union: concat the per-position bases, SVD, rank 4
        cols = []
        for p in rpos:
            b, _ = subspace_from_scores(sc[p:p + 1], U_all, gain, rank=8,
                                        normalize_unembedding_rows=True)
            cols.append(b[0])
        cols = torch.cat(cols, dim=1)
        vecs, vals, _ = torch.linalg.svd(cols, full_matrices=False)
        U4 = vecs[:, :4]
        # per-direction: each SVD direction's composition across positions
        contrib = [(float(vals[i]), [float((vecs[:, i].T @ cols[:, j]).norm() / vals[:4].max())
                                     for j in range(len(rpos))]) for i in range(4)]
        # depth shape of each selected token (position = the last wrapper position):
        h = res[:, rpos[-1], :].float()
        rms = (h.square().mean(-1) + 1e-6).sqrt()
        hn = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain
        lg = (hn @ U_all.T) / rown
        shapes = {}
        for t in sel[rpos[-1]]["ids"]:
            traj = lg[:, t]
            d = traj[1:] - traj[:-1]
            build = float(d[12:22].clamp_min(0).sum())
            cut = float((-d[-3:]).clamp_min(0).sum())
            early = float(d[:12].abs().sum())
            mid = float(d[12:22].abs().sum())
            late = float(d[22:].abs().sum())
            tot = early + mid + late
            shapes[t] = {"label": tok.decode([t]), "build": round(build, 3),
                         "cut": round(cut, 3), "var_early": round(early / tot, 3),
                         "var_build": round(mid / tot, 3), "var_late": round(late / tot, 3),
                         "min_selected": bool(min(build, cut) > 0)}
        report[stem] = {"selected": sel, "svd_contrib": contrib, "depth_shapes": shapes}
        n_shape = sum(1 for v in shapes.values() if v["min_selected"])
        print(f"{stem}: union support {cols.shape[1]}, rank-4 U; "
              f"selected tokens with build>0 AND cut>0 at the last position: {n_shape}/8")
        print("  labels:", sel[rpos[-1]]["labels"])
        print("  depth shapes (var_early/build/late):",
              [(v["label"], v["var_early"], v["var_build"], v["var_late"],
                v["build"], v["cut"]) for v in shapes.values()])
    (OUT / "inventory.json").write_text(json.dumps(report, indent=1) + "\n")
    print(f"saved: {OUT / 'inventory.json'}")


from suppressed_activation_subspace import increment_scores, subspace_from_scores

if __name__ == "__main__":
    main()
