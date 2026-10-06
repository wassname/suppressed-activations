"""Minus ends methods and related variants. — PI/OpenAI"""
import torch
from ..model import rms
from .helpers import last
from .registry import geometry


def _minus_ends(hs, k=1, mode="mean"):
    """Layers 17-31 minus the span of this prompt's first (16) and output (32) layers, at its last k tokens."""
    first, out = rms(hs[0, -k:]), rms(hs[-1, -k:])                                    # [k, d] each
    D = torch.stack([first.mean(0), out.mean(0)], 1) if mode == "mean" else torch.cat([first, out]).T
    N = torch.linalg.qr(D).Q
    x = last(hs)[1:-1]
    return x - (x @ N) @ N.T                                                           # [15, d]


@geometry("minus ends", about="Layers 17-31 minus the span of this prompt's layer-16 and output-layer states, averaged")
def minus_ends(hs, state):
    return _minus_ends(hs).mean(0)


@geometry("minus ends, least-explained layer",
          about="As 'minus ends', but keep the one layer the two states explain least (picked per prompt, no labels)")
def minus_ends_least_explained(hs, state):  # each row starts with the same norm, so the largest remainder is the least explained
    left = _minus_ends(hs)
    return left[left.norm(dim=-1).argmax()]


@geometry("minus ends, recent tokens", (8, "mean"), author="[Sandy Fraser](https://github.com/z0u)",
          about="As 'minus ends', but average the layer-16 and output states over the last 8 tokens first")
def minus_window(hs, state, k, mode):
    return _minus_ends(hs, k, mode).mean(0)
