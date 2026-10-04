"""Candidate transforms: one forward pass at the last prompt token -> a score per vocabulary token.

Add one with @transform. `settings` is the grid searched on the dev pair; `fitted` says what it is
fitted on besides the model's weights: "nothing", "WikiText", "random seed", or "J-lens" (an external learned matrix). — PI/OpenAI
"""
import json

import torch

from common import ROOT, W, forward, gain, load_jlens, model, readout, rms, tok, vocab

TRANSFORMS = {}  # name -> (settings, fitted, fn(state, setting) -> scores [vocab])
RANKS = (64, 256, 1024)
J = load_jlens()
_J = {}


def jlens(x, l):
    """Residual l through the Jacobian lens to the final residual."""
    if l not in _J:
        _J[l] = J[l - 1].cuda().float()
    return x.float() @ _J[l].T


def transform(name, settings, fitted):
    def register(fn):
        TRANSFORMS[name] = (list(settings), fitted, fn)
        return fn
    return register


def project(B, x):
    return B @ (B.T @ rms(x))


# ---- fixed subspaces, fitted once on 300 WikiText texts (no prompts, no labels) ----
bases, token_counts = {}, torch.zeros(len(vocab), dtype=torch.long)


def fit_bases():
    d = W.shape[1]
    texts = json.loads((ROOT / "data/challenge/wikitext2_train_300.json").read_text())["texts"]
    keys = ("x27", "x32", "d24", "d27", "d29", "supp", "antipasto")
    gram_w = sum((c.T @ c).double() for c in W.split(16384))
    lm_head = torch.linalg.eigh(gram_w)[1].flip(-1)[:, :256]                 # top-256 right singular vectors of W_U
    second = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in keys}
    first = {k: torch.zeros(d, dtype=torch.float64, device="cuda") for k in keys}
    n, mean28 = 0, torch.zeros(d, dtype=torch.float64, device="cuda")
    for text in texts:
        token_counts.add_(torch.bincount(tok(text, add_special_tokens=False, truncation=True, max_length=128,
                                             return_tensors="pt").input_ids[0], minlength=len(vocab))[:len(vocab)])
        res, _, _ = forward(text, max_length=128)
        x = rms(res[:, 8:]).double()                                   # [33, tok, d], skip the first tokens
        step = x[2:].abs() - x[1:-1].abs()                             # per-coordinate magnitude change, layers 1..32
        supp = torch.minimum(step.clamp_min(0).sum(0), (-step).clamp_min(0).sum(0))  # added then removed
        raw = res[:, 8:].double()
        net = (raw[1:] - raw[:-1])[3:].sum(0)                         # AntiPaSTO written - read, layers 3..32 (= h32 - h3)
        antipasto = net - (net @ lm_head) @ lm_head.T                 # minus the lm-head-readable directions
        for k, v in (("x27", x[27]), ("x32", x[32]), ("d24", x[25] - x[24]), ("d27", x[28] - x[27]),
                     ("d29", x[30] - x[29]), ("supp", supp), ("antipasto", antipasto)):
            second[k] += v.T @ v
            first[k] += v.sum(0)
        mean28 += x[28].sum(0)
        n += x.shape[1]
    cov = {k: second[k] / n - torch.outer(first[k] / n, first[k] / n) for k in keys}
    mlp = lambda i: model.model.layers[i].mlp
    top = lambda m: torch.linalg.eigh(m)[1].flip(-1).float()          # eigenvectors, largest eigenvalue first
    gram = sum((c.T @ c).double() for c in (W * gain).split(16384))
    bases["weak-readout"] = torch.linalg.eigh(gram)[1].float()         # smallest first: what the head reads least
    bases["random"] = torch.linalg.qr(torch.randn(d, max(RANKS), generator=torch.Generator().manual_seed(0)).cuda()).Q
    for l in (24, 27, 29):
        bases[f"churn{l}"] = top(cov[f"d{l}"])
        write = torch.linalg.svd(mlp(l - 1).down_proj.weight.float(), full_matrices=False).U
        read = torch.linalg.svd(torch.cat([mlp(l).up_proj.weight.float(), mlp(l).gate_proj.weight.float()]),
                                full_matrices=False).Vh.T
        bases[f"write minus top-read{l}"] = {r: torch.linalg.qr(write[:, :r] - read[:, :r] @ (read[:, :r].T @ write[:, :r])).Q
                                             for r in RANKS}
    bases["erased-variance"] = top(cov["x27"] - cov["x32"])
    bases["added then removed"] = top(cov["supp"])
    bases["suppressed (AntiPaSTO)"] = top(cov["antipasto"])
    bases["output"] = top(cov["x32"])
    bases["mean28"] = (mean28 / n).float()


# ---- the transforms ----
@transform("logit lens", [(l,) for l in range(20, 32)], fitted="nothing")
def plain(s, l):
    return readout(s["res"][l])


@transform("J-lens", [(l,) for l in range(20, 32)], fitted="J-lens")
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@transform("mean WikiText activation (control)", [(28,)], fitted="WikiText")
def fixed_list(s, l):  # ignores the prompt: readout of the mean WikiText residual
    return readout(bases["mean28"])


@transform("input word (control)", [(l,) for l in (8, 12, 16, 20)], fitted="nothing")
def input_word(s, l):  # reads the input word itself, not the last token: does recovering the meaning need a hidden step?
    return readout(s["input"][l])


@transform("random subspace (control)", [(27, r) for r in RANKS], fitted="random seed")
def random_subspace(s, l, r):
    return readout(project(bases["random"][:, :r], s["res"][l]))


@transform("layer-change PCA", [(l, r) for l in (24, 27, 29) for r in RANKS], fitted="WikiText")
def churn(s, l, r):  # largest layer-to-layer change on generic text
    return readout(project(bases[f"churn{l}"][:, :r], s["res"][l]))


@transform("MLP write minus next MLP read", [(l, r) for l in (24, 27, 29) for r in RANKS], fitted="nothing")
def write_minus_top_read(s, l, r):  # top-r directions block l-1's MLP writes, minus the top-r its next MLP reads
    return readout(project(bases[f"write minus top-read{l}"][r], s["res"][l]))


@transform("variance gone by the output (PCA)", [(27, r) for r in RANKS], fitted="WikiText")
def erased_variance(s, l, r):  # variance at layer 27 that is gone by 32
    return readout(project(bases["erased-variance"][:, :r], s["res"][l]))


@transform("directions the output head reads least", [(27, r) for r in RANKS], fitted="nothing")
def weak_readout(s, l, r):
    return readout(project(bases["weak-readout"][:, :r], s["res"][l]))


@transform("added then removed", [(27, r) for r in RANKS], fitted="WikiText")
def added_then_removed(s, l, r):  # pca(min(increases, decreases)) of per-coordinate magnitudes
    return readout(project(bases["added then removed"][:, :r], s["res"][l]))


@transform("AntiPaSTO suppressed subspace", [(27, r) for r in RANKS], fitted="WikiText")
def suppressed_antipasto(s, l, r):  # compute_suppressed_from_hidden_states in github.com/wassname/AntiPaSTO, on all tokens
    return readout(project(bases["suppressed (AntiPaSTO)"][:, :r], s["res"][l]))


@transform("logit lens minus output-layer PCA", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], fitted="WikiText")
def plain_minus_output(s, l, r):
    x, B = rms(s["res"][l]), bases["output"][:, :r]
    return readout(x - B @ (B.T @ x))


@transform("J-lens minus output-layer PCA", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], fitted="J-lens, WikiText")
def j_minus_output(s, l, r):
    x, B = rms(jlens(s["res"][l], l)), bases["output"][:, :r]
    return readout(x - B @ (B.T @ x))


def _token_span(scores, rank):
    """Orthonormal basis for the (centred, gain-scaled) unembedding rows of the top-`rank` tokens."""
    ids = scores.topk(rank).indices
    return torch.linalg.qr(((W - W.mean(0))[ids] * gain).T, mode="reduced").Q


def _rise_fall(early, peak, out):
    rise, fall = peak - early, peak - out
    return torch.minimum((rise - rise.mean()).clamp_min(0), (fall - fall.mean()).clamp_min(0))


@transform("rise-and-fall", [(27,)], fitted="nothing")
def rise_and_fall(s, peak):  # tokens whose logit rises from layer 22 to the peak and falls by the output
    return _rise_fall(readout(s["res"][22]), readout(s["res"][peak]), readout(s["res"][32]))


@transform("rise-and-fall, J-lens", [(p,) for p in (26, 27, 28, 29)], fitted="J-lens")
def rise_and_fall_j(s, peak):
    return _rise_fall(readout(jlens(s["res"][22], 22)), readout(jlens(s["res"][peak], peak)), s["logits"])


@transform("rise-and-fall token span (rank 32)", [(27,)], fitted="nothing")
def suppressed_subspace(s, l):  # per prompt: span of the 32 rise-and-fall tokens' unembeddings
    S = _token_span(rise_and_fall(s, l), 32)
    return readout(S @ (S.T @ rms(s["res"][l])))


@transform("rise-and-fall token span (rank 32), J-lens", [(p,) for p in (26, 27, 28, 29)], fitted="J-lens")
def suppressed_subspace_j(s, peak):
    S = _token_span(rise_and_fall_j(s, peak), 32)
    return readout(S @ (S.T @ rms(jlens(s["res"][peak], peak))))


@transform("layer-23 attention output, J-lens", [(23,)], fitted="J-lens")
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
