# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Block-by-block energy table for FIXED late-selected per-token bases (CPU-only).

Question (user): which dimensions do the LAST THREE blocks suppress, and where are those
components built? Indexing for Qwen3.5-4B (32 blocks, 0..31): bank residual index l holds
h_l = residual ENTERING block l; h_0 = embeddings, h_l = output of block l-1, h_32 = final
residual before the final norm/tied head. Block l writes Delta_h_l = h_{l+1} - h_l; the last
three blocks are 29, 30, 31 with outputs h_30, h_31, h_32.

Late selector (same construction family as the bank detector, moved to the tail):
score_i = min( clampmax(logit_i(h_30) - logit_i(h_29), 0), clampmax(logit_i(h_30) - logit_i(h_32), 0) ),
mean-centred over vocab, RMS+gain-normalised readout (suppressed_activation_scores at
early=29, peak=30, output=32). A pure-removal variant clampmax(logit_i(h_29) - logit_i(h_32))
is also computed as a diagnostic. Per-token rank-8 bases = QR of centred gain-scaled
unembedding rows, top-8 scores; window = end-aligned last-4; combined by support-filtered
temporal union (SVD left vectors) and top8. With P FIXED, for every layer l:
E_l = ||P h_l||^2, fraction E_l / ||h_l||^2, signed block change E_{l+1} - E_l (written by
block l), and the exact decomposition
E_{l+1} - E_l = 2<P h_l, P Delta_h_l> + ||P Delta_h_l||^2 (verified numerically).
Readout logits of the selected tokens are tracked per layer so vocabulary suppression
(logits fall) is separable from geometric energy attenuation (E_l falls). -- PI[claude]"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch import Tensor

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from suppressed_activation_subspace import (
    subspace_from_scores,
    suppressed_activation_scores,
)

LAYERS = tuple(range(33))  # h_0 .. h_32


def late_scores(res: Tensor, unembedding: Tensor, gain: Tensor) -> dict[str, Tensor]:
    """res: (1, layers, hidden) for one position row of the bank."""
    rise_fall = suppressed_activation_scores(
        res, unembedding, gain, early_layer=29, peak_layer=30, output_layer=32,
        normalize_unembedding_rows=True,
    )
    # pure-removal diagnostic: readout present before the last three blocks, gone at the end
    h = res[:, [29, 32]].float()
    h_norm = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain.float()
    logits = h_norm @ unembedding.float().T
    row = (unembedding.float() * gain.float()).norm(dim=-1)
    logits = logits / row
    removal = (logits[:, 0] - logits[:, 1]).clamp_min(0)
    removal = removal - removal.mean(-1, keepdim=True)
    return {"rise_fall": rise_fall, "removal": removal.clamp_min(0)}


def union_basis(win: Tensor):
    m = win.permute(1, 0, 2).reshape(win.shape[1], -1)  # (hidden, 8N)
    u, s, _ = torch.linalg.svd(m, full_matrices=False)
    tol = max(m.shape) * torch.finfo(s.dtype).eps * s[0]
    support = int((s > tol).sum())
    return u[:, :support], s, support


def main(bank: Path, out_dir: Path, window: int = 4) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.load(open(bank / "manifest.json"))
    gain = torch.ones(1)
    # norm gain is a per-dim vector; stored in the dev bank, reconstructed for the old bank
    if (bank / "norm_gain.pt").exists():
        gain = torch.load(bank / "norm_gain.pt", weights_only=False).float()
    unembedding = torch.load(bank / "unembedding.pt", weights_only=False).float() if (bank / "unembedding.pt").exists() else None
    assert unembedding is not None, "bank must save the (tied) unembedding rows"

    table: dict = {}
    for name, entry in manifest["entries"].items():
        res = torch.load(bank / f"{name}_residuals.pt", weights_only=False).float()  # (33, seq, hidden)
        labels = entry["token_labels"]
        seq = res.shape[1]
        a, b = max(seq - window, 0), seq
        labels_win = labels[a:b]
        rows1 = res.permute(1, 0, 2)  # (seq, layers, hidden)
        scores = late_scores(rows1, unembedding, gain)
        bases, sel_ids = subspace_from_scores(
            scores["rise_fall"], unembedding, gain, rank=8, normalize_unembedding_rows=True)
        # (seq, hidden, 8)
        win = bases[a:b]
        proj: dict[str, list[Tensor]] = {}
        u, s, support = union_basis(win)
        proj["union"] = [u] * (b - a)
        proj["top8"] = [u[:, :8]] * (b - a)
        proj["per_token"] = [win[i] for i in range(b - a)]
        sel_tokens = sorted({int(i) for i in sel_ids[a:b].flatten().tolist()})
        vocab_traj = {}
        hsel = rows1[:, :, :][a:b]  # window residuals
        for tok in sel_tokens[:32]:
            row = unembedding[tok] * gain
            row = row / row.norm()
            vocab_traj[tok] = {
                "token": "",
                "logits": [float(((hsel[:, l] / hsel[:, l].square().mean(-1, keepdim=True).sqrt().clamp_min(1e-6) * gain) @ row).mean()
                                 ) for l in LAYERS if l < res.shape[0]],
            }
        for pname, Ps in proj.items():
            E, frac, dE, dec = [], [], [], []
            max_err = 0.0
            for t in range(b - a):
                E_t, frac_t, dE_t = [], [], []
                # orthonormal columns: ||P h||^2 = ||U^T h||^2
                for l in LAYERS:
                    if l >= res.shape[0]:
                        break
                    U = Ps[t]
                    h = res[l, a + t]
                    Uh = U.T @ h
                    E_t.append(float(Uh.square().sum()))
                    frac_t.append(float(Uh.square().sum()) / float(h.square().sum()))
                for l in range(res.shape[0] - 1):
                    U = Ps[t]
                    h, h1 = res[l, a + t], res[l + 1, a + t]
                    dh = h1 - h
                    Uh, Uh1, Udh = U.T @ h, U.T @ h1, U.T @ dh
                    lhs = float(Uh1.square().sum()) - float(Uh.square().sum())
                    rhs = 2 * float(Uh @ Udh) + float(Udh.square().sum())
                    max_err = max(max_err, abs(lhs - rhs))
                    dE_t.append(lhs)
                E.append(E_t), frac.append(frac_t), dE.append(dE_t)
            table[f"{name}:{pname}"] = {
                "token_labels": labels_win,
                "positions": list(range(a, b)),
                "n_union_cols": int(8 * (b - a)), "support": support,
                "s1": float(s[0]), "s_min_kept": float(s[support - 1]),
                "E": E, "frac": frac, "block_dE": dE,
                "decomposition_max_abs_err": max_err,
                "selected_vocab_ids": sel_ids[a:b].tolist(),
                "vocab_logits_by_layer": vocab_traj,
            }
    json.dump(table, open(out_dir / "late_blocks_table.json", "w"), indent=1)
    print(f"wrote {out_dir/'late_blocks_table.json'} ({len(table)} prompt:projector groups)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", type=Path, default=ROOT / "out/2026-09-10_trajbank")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--window", type=int, default=4)
    args = ap.parse_args()
    out = args.out or ROOT / "out/2026-09-12_late-blocks"
    main(args.bank, out, args.window)
