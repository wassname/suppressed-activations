# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Descriptive common-basis table from the saved trajectory bank (CPU-only).

For each prompt and end-aligned token window: concatenate the per-token orthonormal
rank-8 detector bases (union M = [B_t1 | ... | B_tN]), take the SVD, and report the
spectrum, effective rank, top-k energy, per-token capture of the common top-k projector,
projected residual-norm fractions per layer, and activation cosines of the projected
residuals as a SEPARATE diagnostic. Also reports cross-prompt subspace affinity and the
combined source+donor union a paired intervention would use. No intervention is run here.
Written by PI[claude].
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import Tensor

BANK = Path(__file__).resolve().parents[1] / "out/2026-09-10_trajbank"
OUT = Path(__file__).resolve().parents[1] / "out/2026-09-11_common-basis"
PROMPTS = ("source", "dog", "ant", "control")
RANKS = (4, 8, 16, 32)
LAYERS_SHOWN = (0, 8, 16, 20, 23, 25, 28, 32)


def window_slices(labels: list[str]) -> dict[str, tuple[int, int]]:
    that = labels.index(" that")
    return {
        "last2": (len(labels) - 2, len(labels)),
        "last4": (len(labels) - 4, len(labels)),
        "tail": (that + 1, len(labels)),
        "all": (0, len(labels)),
    }


def load(name: str) -> tuple[Tensor, Tensor, list[str]]:
    det = torch.load(BANK / f"{name}_detector.pt", weights_only=False)
    res = torch.load(BANK / f"{name}_residuals.pt", weights_only=False).float()
    labels = json.load(open(BANK / "manifest.json"))["entries"][name]["token_labels"]
    basis = det["basis"].float()  # (seq, hidden, 8) orthonormal per token
    torch.testing.assert_close(
        basis.transpose(1, 2) @ basis, torch.eye(8).expand(basis.shape[0], -1, -1), rtol=1e-4, atol=1e-4
    )
    return basis, res, labels


def svd_of_union(bases: Tensor) -> tuple[Tensor, Tensor]:
    m = bases.permute(1, 0, 2).reshape(bases.shape[1], -1)  # (hidden, 8N)
    u, s, _ = torch.linalg.svd(m, full_matrices=False)  # u: common hidden-space basis
    return s, u


def eff_rank(s: Tensor) -> float:
    lam = s.square()
    return float(lam.sum().square() / lam.square().sum())


def energy_frac(s: Tensor, k: int) -> float:
    lam = s.square()
    return float(lam[:k].sum() / lam.sum())


def capture(basis_win: Tensor, v_k: Tensor) -> list[float]:
    # per-token fraction of B_t inside span(V_k): ||B_t^T V_k||_F^2 / rank
    return [float(((b.T @ v_k).square().sum()) / b.shape[1]) for b in basis_win]


def affinity(u: Tensor, v: Tensor) -> float:
    cos = torch.linalg.svdvals(u.T @ v)  # principal-angle cosines
    return float(cos.square().mean())


def cos_pairs(x: Tensor) -> float:
    # mean off-diagonal cosine between rows
    xn = x / x.norm(dim=-1, keepdim=True)
    g = xn @ xn.T
    n = g.shape[0]
    return float((g.sum() - g.diagonal().sum()) / (n * n - n))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data, basis_all, res_all, labels_all = {}, {}, {}, {}
    for name in PROMPTS:
        basis_all[name], res_all[name], labels_all[name] = load(name)

    # 1) union spectrum + rank capture per prompt x window
    for name in PROMPTS:
        for wname, (a, b) in window_slices(labels_all[name]).items():
            bw = basis_all[name][a:b]  # (n, hidden, 8)
            s, u = svd_of_union(bw)
            row = {
                "n_tokens": int(b - a),
                "union_cols": int(8 * bw.shape[0]),
                "s1": float(s[0]), "s8": float(s[7]) if len(s) > 7 else None,
                "s8_over_s1": float(s[7] / s[0]) if len(s) > 7 else None,
                "eff_rank": eff_rank(s),
                "energy": {f"top{k}": energy_frac(s, k) for k in (4, 8, 16, 32) if k <= len(s)},
                "capture_mean": {}, "resid_frac_L25": {},
                "resid_norm_mean_L25": float(res_all[name][25, a:b].norm(dim=-1).mean()),
            }
            for k in RANKS:
                if k > len(s):
                    continue
                v_k = u[:, :k]
                row["capture_mean"][f"top{k}"] = float(torch.tensor(capture(bw, v_k)).mean())
                # projected residual-norm fraction at peak layer 25
                p = v_k @ (v_k.T @ res_all[name][25, a:b].T)  # (hidden, n)
                row["resid_frac_L25"][f"top{k}"] = float(
                    (p.norm(dim=0) / res_all[name][25, a:b].norm(dim=-1)).mean()
                )
            data.setdefault("union", {})[f"{name}:{wname}"] = row

    # 2) projected residual-norm fraction per layer, top8 union (growth diagnostic)
    for name in PROMPTS:
        for wname in ("last4", "tail"):
            a, b = window_slices(labels_all[name])[wname]
            bw = basis_all[name][a:b]
            _, u8 = svd_of_union(bw)
            v8 = u8[:, :8]
            fr, raw = [], []
            for layer in range(res_all[name].shape[0]):
                r = res_all[name][layer, a:b]  # (n, hidden)
                p = (v8.T @ r.T).T @ v8.T  # (n, hidden) projected
                fr.append(float((p.norm(dim=-1) / r.norm(dim=-1)).mean()))
                raw.append(float(r.norm(dim=-1).mean()))
            data.setdefault("by_layer", {})[f"{name}:{wname}"] = {
                "frac_top8": {str(L): fr[L] for L in LAYERS_SHOWN},
                "raw_norm": {str(L): raw[L] for L in LAYERS_SHOWN},
            }

    # 3) activation cosines (SEPARATE diagnostic, not a subspace metric)
    for name in PROMPTS:
        for wname in ("last4", "tail"):
            a, b = window_slices(labels_all[name])[wname]
            bw = basis_all[name][a:b]
            _, u8 = svd_of_union(bw)
            v8 = u8[:, :8]
            data.setdefault("cosines", {})[f"{name}:{wname}"] = {
                f"L{L}": {
                    "raw": cos_pairs(res_all[name][L, a:b]),
                    "proj_top8": cos_pairs((v8.T @ res_all[name][L, a:b].T).T),
                }
                for L in (23, 25, 32)
            }

    # 4) cross-prompt affinity of top8 unions
    top8 = {}
    for name in PROMPTS:
        for wname in ("last4", "tail"):
            a, b = window_slices(labels_all[name])[wname]
            _, uu = svd_of_union(basis_all[name][a:b])
            top8[f"{name}:{wname}"] = uu[:, :8]
    pairs = [("source", "dog"), ("source", "ant"), ("source", "control"), ("dog", "ant")]
    for wname in ("last4", "tail"):
        for p, q in pairs:
            data.setdefault("affinity", {})[f"{p}-{q}:{wname}"] = affinity(
                top8[f"{p}:{wname}"], top8[f"{q}:{wname}"]
            )

    # 5) combined source+donor union (what a paired common replacement would use)
    for donor in ("dog", "ant", "control"):
        for wname in ("last4", "tail"):
            a_s, b_s = window_slices(labels_all["source"])[wname]
            a_d, b_d = window_slices(labels_all[donor])[wname]
            m = torch.cat(
                [basis_all["source"][a_s:b_s].permute(1, 0, 2).reshape(bases_h := basis_all["source"].shape[1], -1),
                 basis_all[donor][a_d:b_d].permute(1, 0, 2).reshape(bases_h, -1)], dim=1
            )
            _, s, _ = torch.linalg.svd(m, full_matrices=False)
            data.setdefault("combined", {})[f"source+{donor}:{wname}"] = {
                "n_tokens": int(b_s - a_s + b_d - a_d),
                "s1": float(s[0]), "s8_over_s1": float(s[7] / s[0]),
                "eff_rank": eff_rank(s),
                "energy": {f"top{k}": energy_frac(s, k) for k in (4, 8, 16, 32)},
            }

    data["provenance"] = {
        "bank": str(BANK), "model": "Qwen/Qwen3.5-4B rev 851bf6e8",
        "basis": "per-token rank-8 QR of centered norm-gain-scaled unembedding rows, "
                 "selected by top-8 suppression scores (layers 23/25/32)",
        "written": datetime.now(timezone.utc).isoformat(),
    }
    json.dump(data, open(OUT / "table.json", "w"), indent=1)
    print(f"wrote {OUT/'table.json'}")


if __name__ == "__main__":
    main()
