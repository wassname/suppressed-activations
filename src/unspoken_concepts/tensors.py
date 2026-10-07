"""Tensor operations without model loading. — PI/OpenAI"""
import torch


def rms(h):
    h = h.float()
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
