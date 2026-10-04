"""Candidate transforms: one forward pass at the last prompt token -> a score per vocabulary token.

Add one with @transform. `settings` is the grid searched on the dev pair; `lens_based` marks transforms that use a lens or
per-prompt vocabulary scores rather than only a fixed subspace (starred on the leaderboard). — PI/OpenAI
"""
import json

import torch

from common import ROOT, W, forward, gain, load_jlens, model, readout, rms, tok, vocab
from suppressed_activation_subspace import subspace_from_scores, suppressed_activation_scores

TRANSFORMS = {}  # name -> (settings, lens_based, fn(state, setting) -> scores [vocab])
RANKS = (64, 256, 1024)
J = load_jlens()
_J = {}


def jlens(x, l):
    """Residual l through the Jacobian lens to the final residual."""
    if l not in _J:
        _J[l] = J[l - 1].cuda().float()
    return x.float() @ _J[l].T


def transform(name, settings, lens_based):
    def register(fn):
        TRANSFORMS[name] = (list(settings), lens_based, fn)
        return fn
    return register


def project(B, x):
    return B @ (B.T @ rms(x))


# ---- fixed subspaces, fitted once on 300 WikiText texts (no prompts, no labels) ----
bases, token_counts = {}, torch.zeros(len(vocab), dtype=torch.long)


def fit_bases():
    d = W.shape[1]
    texts = json.loads((ROOT / "data/challenge/wikitext2_train_300.json").read_text())["texts"]
    keys = ("x27", "x32", "d24", "d27", "d29", "supp")
    second = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in keys}
    first = {k: torch.zeros(d, dtype=torch.float64, device="cuda") for k in keys}
    n, mean28 = 0, torch.zeros(d, dtype=torch.float64, device="cuda")
    for text in texts:
        token_counts.add_(torch.bincount(tok(text, add_special_tokens=False, truncation=True, max_length=128,
                                             return_tensors="pt").input_ids[0], minlength=len(vocab))[:len(vocab)])
        res, _, _ = forward(text, max_length=128)
        x = rms(res[:, 8:]).double()                                   # [33, tok, d], skip the first tokens
        step = x[2:].abs() - x[1:-1].abs()                             # per-coordinate magnitude change, layers 1..32
        supp = torch.minimum(step.clamp_min(0).sum(0), (-step).clamp_min(0).sum(0))  # added then removed (AntiPaSTO)
        for k, v in (("x27", x[27]), ("x32", x[32]), ("d24", x[25] - x[24]), ("d27", x[28] - x[27]),
                     ("d29", x[30] - x[29]), ("supp", supp)):
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
    bases["suppressed (AntiPaSTO)"] = top(cov["supp"])
    bases["output"] = top(cov["x32"])
    bases["mean28"] = (mean28 / n).float()


# ---- the transforms ----
@transform("plain lens", [(l,) for l in range(20, 32)], lens_based=True)
def plain(s, l):
    return readout(s["res"][l])


@transform("J-lens", [(l,) for l in range(20, 32)], lens_based=True)
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@transform("fixed list (control)", [(28,)], lens_based=True)
def fixed_list(s, l):  # ignores the prompt: J-lens readout of the mean WikiText residual
    return readout(jlens(bases["mean28"], l))


@transform("input word, J-lens (control)", [(l,) for l in (4, 8, 12, 16)], lens_based=True)
def input_word(s, l):  # reads the input word itself, not the last token: does recovering the meaning need a hidden step?
    return readout(jlens(s["input"][l], l))


@transform("random subspace (floor)", [(27, r) for r in RANKS], lens_based=False)
def random_subspace(s, l, r):
    return readout(project(bases["random"][:, :r], s["res"][l]))


@transform("churn", [(l, r) for l in (24, 27, 29) for r in RANKS], lens_based=False)
def churn(s, l, r):  # largest layer-to-layer change on generic text
    return readout(project(bases[f"churn{l}"][:, :r], s["res"][l]))


@transform("write minus top-read", [(l, r) for l in (24, 27, 29) for r in RANKS], lens_based=False)
def write_minus_top_read(s, l, r):  # top-r directions block l-1's MLP writes, minus the top-r its next MLP reads
    return readout(project(bases[f"write minus top-read{l}"][r], s["res"][l]))


@transform("erased-variance", [(27, r) for r in RANKS], lens_based=False)
def erased_variance(s, l, r):  # variance at layer 27 that is gone by 32
    return readout(project(bases["erased-variance"][:, :r], s["res"][l]))


@transform("weak-readout", [(27, r) for r in RANKS], lens_based=False)
def weak_readout(s, l, r):
    return readout(project(bases["weak-readout"][:, :r], s["res"][l]))


@transform("suppressed (AntiPaSTO)", [(27, r) for r in RANKS], lens_based=False)
def suppressed_antipasto(s, l, r):  # pca(min(increases, decreases)) of per-coordinate magnitudes
    return readout(project(bases["suppressed (AntiPaSTO)"][:, :r], s["res"][l]))


@transform("plain lens minus output subspace", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], lens_based=False)
def plain_minus_output(s, l, r):
    x, B = rms(s["res"][l]), bases["output"][:, :r]
    return readout(x - B @ (B.T @ x))


@transform("J-lens minus output subspace", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], lens_based=True)
def j_minus_output(s, l, r):
    x, B = rms(jlens(s["res"][l], l)), bases["output"][:, :r]
    return readout(x - B @ (B.T @ x))


def _rise_fall(early, peak, out):
    rise, fall = peak - early, peak - out
    return torch.minimum((rise - rise.mean()).clamp_min(0), (fall - fall.mean()).clamp_min(0))


@transform("rise-and-fall", [(27,)], lens_based=True)
def rise_and_fall(s, peak):  # tokens whose logit rises from layer 22 to the peak and falls by the output
    return suppressed_activation_scores(s["res"][None], W, gain, early_layer=22, peak_layer=peak, output_layer=32)[0]


@transform("rise-and-fall, J-lens", [(p,) for p in (26, 27, 28, 29)], lens_based=True)
def rise_and_fall_j(s, peak):
    return _rise_fall(readout(jlens(s["res"][22], 22)), readout(jlens(s["res"][peak], peak)), s["logits"])


@transform("suppressed subspace (rank 32)", [(27,)], lens_based=True)
def suppressed_subspace(s, l):  # per prompt: span of the 32 rise-and-fall tokens' unembeddings
    S = subspace_from_scores(rise_and_fall(s, l)[None], W, gain, rank=32)[0][0]
    return readout(S @ (S.T @ rms(s["res"][l])))


@transform("suppressed subspace (rank 32), J-lens", [(p,) for p in (26, 27, 28, 29)], lens_based=True)
def suppressed_subspace_j(s, peak):
    S = subspace_from_scores(rise_and_fall_j(s, peak)[None], W, gain, rank=32)[0][0]
    return readout(S @ (S.T @ rms(jlens(s["res"][peak], peak))))


@transform("attention output, J-lens", [(23,)], lens_based=True)
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
