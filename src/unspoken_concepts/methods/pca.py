"""Pca methods and related variants. — PI/OpenAI"""
import torch
from ..calibration import FIRST
from .helpers import last, project, remove
from .registry import geometry


@geometry("layer-change PCA", (1024,), fitted="calibration text",
          about="Each layer projected on the top PCs of that layer's change on calibration text, averaged over layers 16-31")
def churn(hs, embeddings, state, r):
    x = last(hs)
    return torch.stack([project(state[f"churn{FIRST + i}"][:, :r], x[i]) for i in range(len(x) - 1)]).mean(0)


@geometry("net-change PCA", (1024,), fitted="calibration text",
          about="Mean over layers, projected on the top PCs of h32 - h16 on calibration text")
def net_change(hs, embeddings, state, r):
    return project(state["net change"][:, :r], last(hs).mean(0))


@geometry("Output-filtered net-change PCA", (1024,), fitted="calibration text",
          about="Remove the output head's top 256 directions from h32 - h16 on calibration text, fit PCA, then project the mean residual on its top 1024 PCs")
def suppressed_antipasto(hs, embeddings, state, r):
    return project(state["suppressed (AntiPaSTO)"][:, :r], last(hs).mean(0))


@geometry("weak head directions", (1024,), about="Mean over layers, projected on the directions the output head reads least")
def weak_readout(hs, embeddings, state, r):
    return project(state["weak-readout"][:, :r], last(hs).mean(0))


@geometry("minus output PCA", (16,), fitted="calibration text",
          about="Mean over layers, minus the top PCs of output-layer activations on calibration text")
def minus_output(hs, embeddings, state, r):
    return remove(state["output"][:, :r], last(hs).mean(0))
