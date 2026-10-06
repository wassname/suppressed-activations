"""Pca methods and related variants. — PI/OpenAI"""
import torch
from ..calibration import FIRST
from .helpers import last, project, remove
from .registry import geometry


@geometry("layer-change PCA", (1024,), fitted="calibration text",
          about="Each layer projected on the top PCs of that layer's change on calibration text, averaged over layers 16-31")
def churn(hs, state, r):
    x = last(hs)
    return torch.stack([project(state[f"churn{FIRST + i}"][:, :r], x[i]) for i in range(len(x) - 1)]).mean(0)


@geometry("net-change PCA", (1024,), fitted="calibration text",
          about="Mean over layers, projected on the top PCs of h32 - h16 on calibration text (AntiPaSTO without the output-head step)")
def net_change(hs, state, r):
    return project(state["net change"][:, :r], last(hs).mean(0))


@geometry("AntiPaSTO subspace", (1024,), fitted="calibration text",
          about="Mean over layers, projected on the suppressed subspace from the AntiPaSTO paper (Clark 2026, arXiv 2601.07473, App. A.1)")
def suppressed_antipasto(hs, state, r):
    return project(state["suppressed (AntiPaSTO)"][:, :r], last(hs).mean(0))


@geometry("weak head directions", (1024,), about="Mean over layers, projected on the directions the output head reads least")
def weak_readout(hs, state, r):
    return project(state["weak-readout"][:, :r], last(hs).mean(0))


@geometry("minus output PCA", (16,), fitted="calibration text",
          about="Mean over layers, minus the top PCs of output-layer activations on calibration text")
def minus_output(hs, state, r):
    return remove(state["output"][:, :r], last(hs).mean(0))
