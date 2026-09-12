# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Same-question vector/procedure map at L20: why does the recovered template-delta
reference transfer while the projector replacements do not?

Reconstructs the reference tensors EXACTLY as the sweep builds them (template corpus from
the template bank; attenuation_basis on the fit split; delta = template-mean difference;
applied delta = P_ref delta rescaled to the raw delta norm via match_component_norm) and
compares with the same-question replacement vector v = Pd d and the plain donor-source
residual difference g, on the SAME 12 dev pairs. All quantities are measured per position;
no norm is read as semantic strength. -- PI[claude]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from torch import Tensor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from suppressed_activation_subspace import (
    suppressed_activation_scores, subspace_from_scores)

BANK = ROOT / "out/2026-09-12_devbank"
TBANK = ROOT / "out/2026-09-12_templatebank"
OUT = ROOT / "out/2026-09-12_vector-map"
L20 = 20
RANK_REF = 4


def attenuation_basis(peak: Tensor, output: Tensor, rank: int):
    """Verbatim from scripts/oat_sweep.py:737 (fit positive contrast-energy attenuation)."""
    columns = torch.cat([peak.T, output.T], dim=1)
    vectors, _, _ = torch.linalg.svd(columns, full_matrices=False)
    joint = vectors[:, :torch.linalg.matrix_rank(columns)]
    peakJ, outputJ = peak @ joint, output @ joint
    energy_difference = (peakJ.T @ peakJ - outputJ.T @ outputJ) / len(peak)
    values, eigenvectors = torch.linalg.eigh(energy_difference)
    assert (values > 0).sum() >= rank
    return joint @ eigenvectors[:, -rank:].flip(1), values


def top_readout(x: Tensor, unembed: Tensor, gain: Tensor, k: int = 8):
    row = (unembed * gain)
    row = row / row.norm(dim=-1, keepdim=True)
    xn = x / (x.square().mean().sqrt() + 1e-6)
    scores = ((xn * gain) @ row.T)
    top = scores.topk(k)
    return [(int(i), float(v)) for i, v in zip(top.indices, top.values)]


def span_fractions(x: Tensor, cols: Tensor):
    """norm and energy fraction of x inside span(cols); cols orthonormal."""
    c = cols.T @ x
    return float(c.norm()), float(c.square().sum())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    unembed = torch.load(BANK / "unembedding.pt", weights_only=False).float()
    gain = torch.load(BANK / "norm_gain.pt", weights_only=False).float()
    tb = json.load(open(TBANK / "manifest.json"))
    # rebuild the sweep's per-concept construction: contrasts = donor-suffix - source-suffix
    # per template; peak/output states at L20/32; fit split = first 4 templates
    table = {"per_cell": {}, "notes": {
        "delta_definition": "template-mean difference: mean over 8 CONCEPT_TEMPLATES of "
                            "(donor-template suffix residual - source-template suffix residual), "
                            "mean over the last-3 positions, at L20",
        "applied_delta": "P_ref @ delta, rescaled to ||delta|| via match_component_norm "
                         "(sweep-side renormalization); a full-norm vector in the rank-4 ref span",
        "v_definition": "Pd20 d = donor top8 temporal-union projection of the SAME-question donor "
                        "residual at L20 (bank criterion 23/25/32), per end-aligned offset",
        "g_definition": "donor - source residual difference at L20, same question, same positions",
    }}
    for animal in ("dog", "ant"):
        # contrasts for this concept: (8 templates, 3 positions, layers, hidden)
        cons = []
        for ti in range(8):
            suf = [torch.load(TBANK / f"t{ti}-{a}_suffix.pt", weights_only=False).float()
                   for a in ("spider", animal)]
            cons.append(suf[1] - suf[0])
        cons = torch.stack(cons)  # (8, 33layers, 3pos, hidden)
        peak = cons[:, L20, :].flatten(0, 1)    # (8*3, hidden)
        output = cons[:, 32, :].flatten(0, 1)
        fit = peak.shape[0] // 2                # 12: first 4 templates (the sweep's fit split)
        P_ref, ref_vals = attenuation_basis(peak[:fit], output[:fit], RANK_REF)
        delta = cons[:, L20, :].mean(dim=(0, 1))      # mean over templates+positions at L20
        proj = P_ref.T @ delta
        delta_applied = P_ref @ (proj / proj.norm()) * delta.norm()  # match_component_norm
        for cid in sorted({n.rsplit('-source', 1)[0] for n in json.load(open(BANK / 'manifest.json'))['entries']
                           if n.endswith('-source') and f"-{animal}" in n}):
            res_s = torch.load(BANK / f"{cid}-source_residuals.pt", weights_only=False).float()
            res_d = torch.load(BANK / f"{cid}-donor_residuals.pt", weights_only=False).float()
            seq_s, seq_d = res_s.shape[1], res_d.shape[1]
            rows1s, rows1d = res_s.permute(1, 0, 2), res_d.permute(1, 0, 2)
            sc_s = suppressed_activation_scores(rows1s, unembed, gain, early_layer=23, peak_layer=25,
                                                output_layer=32, normalize_unembedding_rows=True)
            sc_d = suppressed_activation_scores(rows1d, unembed, gain, early_layer=23, peak_layer=25,
                                                output_layer=32, normalize_unembedding_rows=True)
            Bs, _ = subspace_from_scores(sc_s, unembed, gain, rank=8, normalize_unembedding_rows=True)
            Bd, _ = subspace_from_scores(sc_d, unembed, gain, rank=8, normalize_unembedding_rows=True)
            def union_cols(bw):
                M = bw.permute(1, 0, 2).reshape(bw.shape[1], -1)
                u, sv, _ = torch.linalg.svd(M, full_matrices=False)
                tol = max(M.shape) * torch.finfo(sv.dtype).eps * sv[0]
                return u[:, :int((sv > tol).sum())]
            Cs, Cd = union_cols(Bs[seq_s-4:]), union_cols(Bd[seq_d-4:])
            Cj = torch.linalg.svd(torch.cat([Cs, Cd], dim=1), full_matrices=False)[0]
            rows = []
            for o in (1, 2, 3):
                h20 = res_s[L20, seq_s - o]
                d20 = res_d[L20, seq_d - o]
                v = Cd @ (Cd.T @ d20)
                g = d20 - h20
                row = {"offset": o,
                       "norms": {"delta_raw": float(delta.norm()), "delta_applied": float(delta_applied.norm()),
                                 "v": float(v.norm()), "g": float(g.norm()), "h20": float(h20.norm())},
                       "cosines": {"delta_applied_vs_v": float(delta_applied @ v / (delta_applied.norm() * v.norm() + 1e-9)),
                                   "delta_applied_vs_g": float(delta_applied @ g / (delta_applied.norm() * g.norm() + 1e-9)),
                                   "v_vs_g": float(v @ g / (v.norm() * g.norm() + 1e-9))},
                       "spans": {}}
                for sname, cols in (("source_top8", Cs), ("donor_top8", Cd), ("joint", Cj), ("ref_span", P_ref)):
                    fn, fe = span_fractions(delta_applied, cols)
                    vn, ve = span_fractions(v, cols)
                    gn, ge = span_fractions(g, cols)
                    row["spans"][sname] = {
                        "delta_applied": {"norm_frac": fn / delta_applied.norm(), "energy_frac": fe / delta_applied.square().sum()},
                        "v": {"norm_frac": vn / v.norm(), "energy_frac": ve / v.square().sum()},
                        "g": {"norm_frac": gn / g.norm(), "energy_frac": ge / g.square().sum()}}
                row["readouts"] = {"delta_applied": top_readout(delta_applied, unembed, gain, 6),
                                   "v": top_readout(v, unembed, gain, 6),
                                   "g": top_readout(g, unembed, gain, 6)}
                rows.append(row)
            table["per_cell"][f"{cid}"] = {"ref_singular_values": [float(x) for x in ref_vals],
                                            "rows": rows}
    json.dump(table, open(OUT / "vector_map.json", "w"), indent=1)
    print(f"wrote {OUT/'vector_map.json'}")


if __name__ == "__main__":
    main()
