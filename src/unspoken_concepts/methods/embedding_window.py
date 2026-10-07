"""Position-averaged embedding/output removal, from Sandy Fraser's suggestion. — PI/OpenAI"""
import torch

from ..tensors import rms
from .registry import geometry


def pooled(h, k, normalize_first):
    window = h[..., -k:, :].float()
    return rms((rms(window) if normalize_first else window).mean(dim=-2))


def window_components(hs, embeddings, k, normalize_first, readout_window):
    assert k > 0 and embeddings.shape == hs.shape[1:]
    endpoints = torch.stack([pooled(embeddings, k, normalize_first), pooled(hs[-1], k, normalize_first)], dim=1)
    u, singular_values, _ = torch.linalg.svd(endpoints, full_matrices=False)
    tolerance = max(endpoints.shape) * torch.finfo(endpoints.dtype).eps * singular_values[0]
    basis = u[:, singular_values > tolerance]
    middle = pooled(hs[1:-1], k if readout_window else 1, normalize_first)
    removed = (middle @ basis) @ basis.T
    return middle, removed


@geometry("minus embedding/output window", (8, False, True), author="[Sandy Fraser](https://github.com/z0u)",
          about="Average input embeddings and output states over 8 tokens; remove their span from window-averaged layers 17-31")
def embedding_window(hs, embeddings, state, k, normalize_first, readout_window):
    middle, removed = window_components(hs, embeddings, k, normalize_first, readout_window)
    return (middle - removed).mean(0)
