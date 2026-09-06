# Written by PI/claude-opus-4.6 and PI/gpt-5.4 for Michael J. Clark.

from __future__ import annotations

import torch
from torch import Tensor


def suppressed_activation_scores(
    residuals: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    early_layer: int,
    peak_layer: int,
    output_layer: int,
    normalize_unembedding_rows: bool = False,
) -> Tensor:
    """Score tokens written by `peak_layer` and suppressed by `output_layer`."""
    h = residuals[:, [early_layer, peak_layer, output_layer]].float()
    h_norm = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
    h_norm = h_norm * rms_norm_gain.float()

    logits = h_norm @ unembedding.float().T
    if normalize_unembedding_rows:
        row_norm = (unembedding.float() * rms_norm_gain.float()).norm(dim=-1)
        if torch.any(row_norm == 0):
            raise ValueError("cannot normalize a zero unembedding row")
        logits = logits / row_norm
    rise = logits[:, 1] - logits[:, 0]
    fall = logits[:, 1] - logits[:, 2]
    rise = rise - rise.mean(-1, keepdim=True)
    fall = fall - fall.mean(-1, keepdim=True)

    return torch.minimum(rise.clamp_min(0), fall.clamp_min(0))


def subspace_from_scores(
    suppressed_score: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    rank: int,
) -> tuple[Tensor, Tensor]:
    """Construct an orthonormal token-direction basis from suppressed scores."""
    token_ids = suppressed_score.topk(rank, dim=-1).indices

    centered_unembedding = unembedding.float() - unembedding.float().mean(0)
    token_directions = centered_unembedding[token_ids] * rms_norm_gain.float()
    basis = torch.linalg.qr(token_directions.transpose(1, 2), mode="reduced").Q
    return basis, token_ids


def suppressed_activation_subspace(
    residuals: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    early_layer: int,
    peak_layer: int,
    output_layer: int,
    rank: int = 32,
    normalize_unembedding_rows: bool = False,
) -> tuple[Tensor, Tensor]:
    """Find per-sample token directions written by `peak_layer` and suppressed by output."""
    scores = suppressed_activation_scores(
        residuals,
        unembedding,
        rms_norm_gain,
        early_layer=early_layer,
        peak_layer=peak_layer,
        output_layer=output_layer,
        normalize_unembedding_rows=normalize_unembedding_rows,
    )
    return subspace_from_scores(scores, unembedding, rms_norm_gain, rank=rank)


def persistent_suppressed_activation_subspace(
    residuals_by_position: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    early_layer: int,
    peak_layer: int,
    output_layer: int,
    rank: int = 32,
    normalize_unembedding_rows: bool = False,
) -> tuple[Tensor, Tensor, Tensor]:
    """Select one subspace from tokens suppressed at every supplied position."""
    scores_by_position = suppressed_activation_scores(
        residuals_by_position,
        unembedding,
        rms_norm_gain,
        early_layer=early_layer,
        peak_layer=peak_layer,
        output_layer=output_layer,
        normalize_unembedding_rows=normalize_unembedding_rows,
    )
    persistent_scores = scores_by_position.amin(dim=0, keepdim=True)
    basis, token_ids = subspace_from_scores(
        persistent_scores, unembedding, rms_norm_gain, rank=rank
    )
    return basis, token_ids, scores_by_position


def union_suppressed_activation_subspace(
    residuals_by_position: Tensor,
    unembedding: Tensor,
    rms_norm_gain: Tensor,
    *,
    early_layer: int,
    peak_layer: int,
    output_layer: int,
    rank: int = 32,
    normalize_unembedding_rows: bool = False,
) -> tuple[Tensor, Tensor, Tensor]:
    """Select one subspace from tokens strongly suppressed at any supplied position."""
    scores_by_position = suppressed_activation_scores(
        residuals_by_position,
        unembedding,
        rms_norm_gain,
        early_layer=early_layer,
        peak_layer=peak_layer,
        output_layer=output_layer,
        normalize_unembedding_rows=normalize_unembedding_rows,
    )
    union_scores = scores_by_position.amax(dim=0, keepdim=True)
    basis, token_ids = subspace_from_scores(union_scores, unembedding, rms_norm_gain, rank=rank)
    return basis, token_ids, scores_by_position


def component(h: Tensor, basis: Tensor) -> Tensor:
    """Project residuals `[..., d]` into sample-specific bases `[..., d, k]`."""
    coordinates = torch.matmul(h.unsqueeze(-2), basis).squeeze(-2)
    return torch.matmul(coordinates.unsqueeze(-2), basis.transpose(-2, -1)).squeeze(-2)


def match_norm(x: Tensor, reference: Tensor) -> Tensor:
    """Give each vector in `x` the corresponding reference norm."""
    norm = x.norm(dim=-1, keepdim=True)
    if torch.any(norm == 0):
        raise ValueError("cannot scale a zero vector")
    return x * reference.norm(dim=-1, keepdim=True) / norm


def remove(h: Tensor, basis: Tensor, *, restore_norm: bool = False) -> Tensor:
    """Remove the component of `h` inside `basis`."""
    removed = h - component(h, basis)
    return match_norm(removed, h) if restore_norm else removed


def replace(
    h: Tensor,
    source_basis: Tensor,
    target_h: Tensor,
    target_basis: Tensor,
    *,
    strength: float = 1.0,
    match_component_norm: bool = True,
    restore_norm: bool = False,
) -> Tensor:
    """Move a sample from its source component toward another sample's component."""
    source = component(h, source_basis)
    target = component(target_h, target_basis)
    if match_component_norm:
        target = match_norm(target, source)
    replaced = h + strength * (target - source)
    return match_norm(replaced, h) if restore_norm else replaced


def steer(h: Tensor, basis: Tensor, strength: float, *, restore_norm: bool = False) -> Tensor:
    """Amplify or suppress a sample's own subspace component."""
    steered = h + strength * component(h, basis)
    return match_norm(steered, h) if restore_norm else steered


def random_basis_like(basis: Tensor, seed: int) -> Tensor:
    """Draw an orthonormal basis with the same shape, device, and dtype."""
    generator = torch.Generator(device=basis.device).manual_seed(seed)
    random_matrix = torch.randn(
        basis.shape, device=basis.device, dtype=basis.dtype, generator=generator
    )
    return torch.linalg.qr(random_matrix, mode="reduced").Q


def matched_random_rotation(h: Tensor, direction: Tensor, distance: Tensor) -> Tensor:
    """Move along a random tangent while matching residual and perturbation norms."""
    h_norm = h.norm(dim=-1, keepdim=True)
    tangent = direction - (direction * h).sum(-1, keepdim=True) * h / h_norm.square()
    tangent = match_norm(tangent, h)
    cosine = 1 - distance.square() / (2 * h_norm.square())
    if torch.any(cosine.abs() > 1):
        raise ValueError("requested perturbation exceeds the sphere diameter")
    sine = torch.sqrt(1 - cosine.square())
    rotated = cosine * h + sine * tangent
    torch.testing.assert_close(rotated.norm(dim=-1), h_norm.squeeze(-1), atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(
        (rotated - h).norm(dim=-1), distance.squeeze(-1), atol=1e-4, rtol=1e-4
    )
    return rotated
