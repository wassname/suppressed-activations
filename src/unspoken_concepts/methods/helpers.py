"""Residual-space projection helpers. — PI/OpenAI"""
from ..model import rms

def project(B, x):
    return B @ (B.T @ rms(x))


def remove(B, x):
    x = rms(x)
    return x - B @ (B.T @ x)


last = lambda hs: rms(hs[:, -1])  # [17, d]: the last prompt token at each layer
