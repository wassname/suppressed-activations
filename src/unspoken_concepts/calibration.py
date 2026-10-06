"""Shared fits on supplied unlabelled activations. — PI/OpenAI"""
import torch
from .model import DEVICE, W, gain, rms, vocab

RANKS = (64, 256, 1024)


CAL_LAYERS = (22, 26, 27, 28, 29, 32)


FIRST = 16  # hs[i] is layer FIRST + i; hs[-1] is the output layer (32)


CHURN_LAYERS = tuple(range(16, 32))


bases = {}


def calibrate(texts):
    """texts: iterable of hs [17 layers (16-32), tokens, d]. Fills and returns `bases`, the state built-in methods share."""
    d = W.shape[1]
    keys = ("x32", "antipasto", "net") + tuple(f"d{l}" for l in CHURN_LAYERS)
    logit_sum = {l: torch.zeros(len(vocab), dtype=torch.float64, device=DEVICE) for l in CAL_LAYERS}
    logit_sq = {l: torch.zeros(len(vocab), dtype=torch.float64, device=DEVICE) for l in CAL_LAYERS}
    gram_w = sum((c.T @ c).double() for c in W.split(16384))
    lm_head = torch.linalg.eigh(gram_w)[1].flip(-1)[:, :256]                 # top-256 right singular vectors of W_U
    second = {k: torch.zeros(d, d, dtype=torch.float64, device=DEVICE) for k in keys}
    first = {k: torch.zeros(d, dtype=torch.float64, device=DEVICE) for k in keys}
    n, mean28 = 0, torch.zeros(d, dtype=torch.float64, device=DEVICE)
    L = lambda l: l - FIRST                                            # layer number -> index into hs
    for hs in texts:
        x = rms(hs[:, 8:]).double()                                    # [17, tok, d], skip the first tokens
        raw = hs[:, 8:].double()
        net = raw[-1] - raw[0]                                         # AntiPaSTO written - read, layers 16..32 (= h32 - h16)
        antipasto = net - (net @ lm_head) @ lm_head.T                 # minus the lm-head-readable directions
        for l in CAL_LAYERS:
            logits = ((gain * rms(hs[L(l), 8:])) @ W.T).double()      # [tok, vocab], as readout() per token
            logit_sum[l] += logits.sum(0)
            logit_sq[l] += logits.square().sum(0)
        pairs = [("x32", x[L(32)]), ("antipasto", antipasto), ("net", net)] + [(f"d{l}", x[L(l + 1)] - x[L(l)])
                                                                               for l in CHURN_LAYERS]
        for k, v in pairs:
            second[k] += v.T @ v
            first[k] += v.sum(0)
        mean28 += x[L(28)].sum(0)
        n += x.shape[1]
    cov = {k: second[k] / n - torch.outer(first[k] / n, first[k] / n) for k in keys}
    top = lambda m: torch.linalg.eigh(m)[1].flip(-1).float()          # eigenvectors, largest eigenvalue first
    gram = sum((c.T @ c).double() for c in (W * gain).split(16384))
    bases["weak-readout"] = torch.linalg.eigh(gram)[1].float()         # smallest first: what the head reads least
    bases["random"] = torch.linalg.qr(torch.randn(d, max(RANKS), generator=torch.Generator().manual_seed(0)).to(DEVICE)).Q
    for l in CHURN_LAYERS:
        bases[f"churn{l}"] = top(cov[f"d{l}"])
    bases["suppressed (AntiPaSTO)"] = top(cov["antipasto"])
    bases["net change"] = top(cov["net"])
    bases["output"] = top(cov["x32"])
    bases["mean28"] = (mean28 / n).float()
    for l in CAL_LAYERS:  # per-layer, per-token logit mean and shrunk scale
        m = logit_sum[l] / n
        var = (logit_sq[l] / n - m.square()).clamp_min(0)
        bases[f"calib{l}"] = (m.float(), (var + var.median()).sqrt().float())
    return bases
