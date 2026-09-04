# Written by PI/claude-opus-4.6 for Michael J. Clark.

from __future__ import annotations

import torch
from torch import Tensor


def suppressed_activation_subspace(
    residuals: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    early_layer: int,
    peak_layer: int,
    output_layer: int,
    rank: int = 32,
) -> tuple[Tensor, Tensor]:
    """Find per-sample token directions written by `peak_layer` and suppressed by output."""
    h = residuals[:, [early_layer, peak_layer, output_layer]].float()
    h_norm = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
    h_norm = h_norm * rms_norm_gain.float()

    logits = h_norm @ unembedding.float().T
    rise = logits[:, 1] - logits[:, 0]
    fall = logits[:, 1] - logits[:, 2]
    rise = rise - rise.mean(-1, keepdim=True)
    fall = fall - fall.mean(-1, keepdim=True)

    suppressed_score = torch.minimum(rise.clamp_min(0), fall.clamp_min(0))
    token_ids = suppressed_score.topk(rank, dim=-1).indices

    centered_unembedding = unembedding.float() - unembedding.float().mean(0)
    token_directions = centered_unembedding[token_ids] * rms_norm_gain.float()
    basis = torch.linalg.qr(token_directions.transpose(1, 2), mode="reduced").Q
    return basis, token_ids
