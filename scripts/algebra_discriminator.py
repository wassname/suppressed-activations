# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""CPU algebra discriminator for the interval re-correction degeneration.

T(h) = (I - C Ps)h + C v, v = Pd d, Ps != Pd: (I-Ps)T(h) = (I-Ps)h + C(I-Ps)v, so the
outside-source component accumulates linearly (within Ps: coefficient 1-C). Measures the
outside fraction, cross-layer agreement, and toy operator iterations (identity between
sites -- toy algebra, NOT transformer evidence) on the saved dev-bank bases/states.
-- PI[claude]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from suppressed_activation_subspace import (
    suppressed_activation_scores, subspace_from_scores)

BANK = ROOT / "out/2026-09-12_devbank"
OUT = ROOT / "out/2026-09-12_late-blocks-dev/algebra.json"
LAYERS = (25, 26, 27, 28, 29, 30)
C = 1.5


def main() -> None:
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    manifest = json.load(open(BANK / "manifest.json"))["entries"]
    out = {"per_cell": {}, "note_toy": "identity between sites; toy algebra, NOT transformer evidence"}

    cell_ids = sorted({n.rsplit('-source', 1)[0].rsplit('-donor', 1)[0] for n in manifest})
    for cid in cell_ids:
        res_s = torch.load(BANK / f"{cid}-source_residuals.pt", weights_only=False).float()
        res_d = torch.load(BANK / f"{cid}-donor_residuals.pt", weights_only=False).float()
        seq_s, seq_d = res_s.shape[1], res_d.shape[1]
        a_s, a_d = seq_s - 4, seq_d - 4
        def support_rank(s_vals):
            # numerical support: s > max(shape) * eps * s1 (shared tolerance helper)
            return int((s_vals > max(s_vals.shape[0], 1) * torch.finfo(torch.float32).eps * s_vals[0]).sum())

        def own_bases(res, a):
            rows1 = res.permute(1, 0, 2)
            sc = suppressed_activation_scores(rows1, unembed, gain, early_layer=23,
                                              peak_layer=25, output_layer=32,
                                              normalize_unembedding_rows=True)
            b, _ = subspace_from_scores(sc, unembed, gain, rank=8,
                                        normalize_unembedding_rows=True)
            M = b[a:].permute(1, 0, 2).reshape(res.shape[2], -1)
            uu, ss, _ = torch.linalg.svd(M, full_matrices=False)
            tol = max(M.shape) * torch.finfo(ss.dtype).eps * ss[0]
            return uu[:, :8], int((ss > tol).sum())
        Us8, sup_s = own_bases(res_s, a_s)
        Ud8, sup_d = own_bases(res_d, a_d)
        Ps = Us8 @ Us8.T
        Pu_cols, pu_s, _ = torch.linalg.svd(torch.cat([Us8, Ud8], dim=1), full_matrices=False)
        pu_keep = support_rank(pu_s)  # shared tolerance: max(shape) * eps * s1
        Pu = Pu_cols[:, :pu_keep]  # SLICED once; the only joint projector used below
        torch.testing.assert_close(Pu.T @ Pu, torch.eye(pu_keep), rtol=1e-4, atol=1e-4)

        idem_rows, entry_contract = [], None
        entry = {"support_union": pu_keep, "support_source": sup_s, "support_donor": sup_d,
                 "fixed_v_idempotence_C1": {"rows": idem_rows},
                 "fixed_v_contraction_C1p5": entry_contract, "positions": []}
        for o in (1, 2, 3):  # end-aligned offsets (the 3 patched positions)
            pos_s, pos_d = seq_s - o, seq_d - o
            v_ls, outs, rec = {}, {}, []
            for L in LAYERS:
                d_l = res_d[L, pos_d]               # donor residual at the ACTUAL layer
                v_l = Ud8 @ (Ud8.T @ d_l)           # Pd d_l (injection vector)
                # v containment in the JOINT span: (I - P_union) v must vanish
                containment = float((v_l - Pu @ (Pu.T @ v_l)).norm() / v_l.norm())
                assert containment < 1e-5, f"v not in joint span: residual {containment}"
                out_v = v_l - Ps @ v_l              # (I - Ps) v_l
                r_l = float(out_v.norm() / v_l.norm())
                v_ls[L], outs[L] = v_l, out_v
                rec.append({"layer": L, "outside_norm_frac": r_l,
                            "outside_energy_frac": r_l ** 2,
                            "v_norm": float(v_l.norm()), "outside_norm": float(out_v.norm()),
                            "joint_containment_residual": containment})
            # signed cross-layer agreement of outside components
            agree = {}
            for i, L1 in enumerate(LAYERS):
                for L2 in LAYERS[i+1:]:
                    c = float((outs[L1] @ outs[L2]) / (outs[L1].norm() * outs[L2].norm() + 1e-9))
                    agree[f"{L1}-{L2}"] = c
            # toy simulations from the actual clean source state at h25
            h0 = res_s[25, pos_s].clone()
            v_frozen = v_ls[25]  # frozen donor state = final prefill donor projection? use L25 actual
            def sim(step_vs):
                h = h0.clone()
                log = []
                for k, v in enumerate(step_vs, 1):
                    h = h - C * (Ps @ h) + C * v   # T(h) = (I - C Ps) h + C v
                    log.append({"k": k, "full": float(h.norm()),
                                "source_span": float((Us8.T @ h).norm()),
                                "outside": float((h - Ps @ h).norm())})
                return log
            seq_frozen = [v_frozen] * 6
            seq_actual = [v_ls[L] for L in LAYERS]
            # union-variant operator: h' = h + C(v - P_union h), v = Pd d (v in union span)
            def sim_union(step_vs, c):
                h = h0.clone(); log = []
                for k, v in enumerate(step_vs, 1):
                    h = h + c * (v - Pu @ (Pu.T @ h))
                    log.append({"k": k, "full": float(h.norm()),
                                "source_span": float((Us8.T @ h).norm()),
                                "outside": float((h - Pu @ (Pu.T @ h)).norm()),
                                "fixed_point_dist": float((Pu.T @ h - Pu.T @ v).norm())})
                return log
            # EXPLICIT fixed-v idempotence assertion at C=1: T(T(h)) == T(h)
            hA = h0.clone()
            v_fix = v_ls[25]
            T1 = hA + 1.0 * (v_fix - Pu @ (Pu.T @ hA))
            T2 = T1 + 1.0 * (v_fix - Pu @ (Pu.T @ T1))
            idem_res = float((T2 - T1).norm())
            assert idem_res < 1e-6 * h0.norm(), f"C=1 fixed-v idempotence fails: {idem_res}"
            idem_rows.append({"T2_minus_T1": idem_res, "relative": idem_res / float(h0.norm())})
            def sim_restricted(step_vs, c):
                h = h0.clone(); log = []
                for k, v in enumerate(step_vs, 1):
                    pv = Ps @ v
                    h = h + c * (pv - Ps @ h)
                    log.append({"k": k, "full": float(h.norm()),
                                "source_span": float((Us8.T @ h).norm()),
                                "outside": float((h - Ps @ h).norm())})
                return log
            # EXACT fixed-v contraction check: h* = (I - Pu)h0 + v with the SAME v each
            # step; ||h_{k+1} - h*|| = |1-C| ||h_k - h*|| exactly (h*-h0 in the joint span).
            h_star = (h0 - Pu @ (Pu.T @ h0)) + v_frozen
            h_fx = h0.clone(); contract = []
            for k in range(1, 7):
                h_fx = h_fx + C * (v_frozen - Pu @ (Pu.T @ h_fx))
                dist = float((h_fx - h_star).norm())
                contract.append({"k": k, "dist_to_h_star": dist})
                assert abs(dist - (0.5 ** k) * float((h0 - h_star).norm())) < 1e-4 * float(h0.norm()), \
                    f"fixed-v contraction violated at k={k}: {dist}"
            entry_contract = contract
            # (the earlier per-layer-v 'fixed_point_dist' sequence is NOT a fixed-point
            #  proof: the reference moves with v_k; kept only as descriptive)
            entry["positions"].append({
                "offset": o, "injection": rec, "outside_cross_layer_cos": agree,
                "toy_frozen_1to6": sim(seq_frozen), "toy_actual_layers": sim(seq_actual),
                "toy_union_C1p5_actual": sim_union(seq_actual, 1.5),
                "toy_union_C1_actual": sim_union(seq_actual, 1.0),
                "toy_restricted_C1p5_actual": sim_restricted(seq_actual, 1.5),
            })
        out["per_cell"][cid] = entry
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
