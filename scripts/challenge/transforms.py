"""Candidate methods for one forward pass.

A `@geometry` method gets one prompt's residual stream (layers 16-32, all prompt tokens) and returns one
residual-stream vector. It picks no layer by hand, and uses no token scores, token ids or word lists; it may use the
model's weights, including the output head as a matrix. The scorer reads the vector with the output head only to check
which words it holds. `@reference` methods (token scores, J-lens, a layer picked on the dev pair) are listed
separately. `settings` is the grid searched on the dev pair; `fitted` says what the method is fitted on besides the
model's weights. — PI/OpenAI
"""
import json

import torch

from common import ROOT, W, forward, gain, load_jlens, readout, rms, vocab

TRANSFORMS = {}  # name -> (settings, fitted, kind, fn); geometry fn -> vector [d], reference fn -> scores [vocab]
RANKS = (64, 256, 1024)
CAL_LAYERS = (22, 26, 27, 28, 29, 32)
CHURN_LAYERS = tuple(range(16, 32))  # layer-change PCA bases, for the leaderboard and notebook.py
J = load_jlens()
_J = {}


def jlens(x, l):
    """Residual l through the Jacobian lens to the final residual."""
    if l not in _J:
        _J[l] = J[l - 1].cuda().float()
    return x.float() @ _J[l].T


def _register(kind):
    def transform(name, settings, fitted):
        def register(fn):
            TRANSFORMS[name] = (list(settings), fitted, kind, fn)
            return fn
        return register
    return transform


geometry, reference = _register("geometry"), _register("reference")


def project(B, x):
    return B @ (B.T @ rms(x))


def remove(B, x):
    x = rms(x)
    return x - B @ (B.T @ x)


# ---- fixed subspaces, fitted once on 300 WikiText texts (no prompts, no labels) ----
bases = {}


def fit_bases():
    d = W.shape[1]
    texts = json.loads((ROOT / "data/challenge/wikitext2_train_300.json").read_text())["texts"]
    keys = ("x32", "antipasto", "net") + tuple(f"d{l}" for l in CHURN_LAYERS)
    logit_sum = {l: torch.zeros(len(vocab), dtype=torch.float64, device="cuda") for l in CAL_LAYERS}
    logit_sq = {l: torch.zeros(len(vocab), dtype=torch.float64, device="cuda") for l in CAL_LAYERS}
    gram_w = sum((c.T @ c).double() for c in W.split(16384))
    lm_head = torch.linalg.eigh(gram_w)[1].flip(-1)[:, :256]                 # top-256 right singular vectors of W_U
    second = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in keys}
    first = {k: torch.zeros(d, dtype=torch.float64, device="cuda") for k in keys}
    n, mean28 = 0, torch.zeros(d, dtype=torch.float64, device="cuda")
    for text in texts:
        res, _, _ = forward(text, max_length=128)
        x = rms(res[:, 8:]).double()                                   # [33, tok, d], skip the first tokens
        raw = res[:, 8:].double()
        net = (raw[1:] - raw[:-1])[3:].sum(0)                         # AntiPaSTO written - read, layers 3..32 (= h32 - h3)
        antipasto = net - (net @ lm_head) @ lm_head.T                 # minus the lm-head-readable directions
        for l in CAL_LAYERS:
            logits = ((gain * rms(res[l, 8:])) @ W.T).double()        # [tok, vocab], as readout() per token
            logit_sum[l] += logits.sum(0)
            logit_sq[l] += logits.square().sum(0)
        pairs = [("x32", x[32]), ("antipasto", antipasto), ("net", net)] + [(f"d{l}", x[l + 1] - x[l]) for l in CHURN_LAYERS]
        for k, v in pairs:
            second[k] += v.T @ v
            first[k] += v.sum(0)
        mean28 += x[28].sum(0)
        n += x.shape[1]
    cov = {k: second[k] / n - torch.outer(first[k] / n, first[k] / n) for k in keys}
    top = lambda m: torch.linalg.eigh(m)[1].flip(-1).float()          # eigenvectors, largest eigenvalue first
    gram = sum((c.T @ c).double() for c in (W * gain).split(16384))
    bases["weak-readout"] = torch.linalg.eigh(gram)[1].float()         # smallest first: what the head reads least
    bases["random"] = torch.linalg.qr(torch.randn(d, max(RANKS), generator=torch.Generator().manual_seed(0)).cuda()).Q
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


# ---- geometry: one prompt's residual stream, layers 16-32, all prompt tokens -> one residual-stream vector ----
# No hand-picked layer: a method uses every layer it gets, or picks one from the activations themselves.
FIRST = 16  # hs[i] is layer FIRST + i; hs[-1] is the output layer (32)
last = lambda hs: rms(hs[:, -1])  # [17, d]: the last prompt token at each layer


@geometry("mean over layers (logit lens)", [()], fitted="nothing")
def mean_lens(hs):
    return last(hs).mean(0)


@geometry("random subspace (control)", [(r,) for r in RANKS], fitted="random seed")
def random_subspace(hs, r):
    return project(bases["random"][:, :r], last(hs).mean(0))


@geometry("mean WikiText activation (control)", [()], fitted="WikiText")
def fixed_list(hs):  # ignores the prompt
    return bases["mean28"]


@geometry("layer-change PCA", [(r,) for r in RANKS], fitted="WikiText")
def churn(hs, r):  # each layer projected on the PCs of that layer's change on generic text, averaged over layers 16-31
    x = last(hs)
    return torch.stack([project(bases[f"churn{FIRST + i}"][:, :r], x[i]) for i in range(len(x) - 1)]).mean(0)


@geometry("net-change PCA (AntiPaSTO without the output-head step)", [(r,) for r in RANKS], fitted="WikiText")
def net_change(hs, r):  # PCA of h32 - h3 on WikiText
    return project(bases["net change"][:, :r], last(hs).mean(0))


@geometry("AntiPaSTO suppressed subspace", [(r,) for r in RANKS], fitted="WikiText")
def suppressed_antipasto(hs, r):  # compute_suppressed_from_hidden_states in github.com/wassname/AntiPaSTO
    return project(bases["suppressed (AntiPaSTO)"][:, :r], last(hs).mean(0))


@geometry("directions the output head reads least", [(r,) for r in RANKS], fitted="nothing")
def weak_readout(hs, r):  # uses the output head only as a matrix
    return project(bases["weak-readout"][:, :r], last(hs).mean(0))


@geometry("minus output-layer PCA", [(r,) for r in (16, 64, 256)], fitted="WikiText")
def minus_output(hs, r):  # remove the top-r PCs of output-layer activations on WikiText
    return remove(bases["output"][:, :r], last(hs).mean(0))


def _minus_ends(hs, k=1, mode="mean"):
    """Layers 17-31 minus the span of this prompt's first (16) and output (32) layers, at its last k tokens."""
    first, out = rms(hs[0, -k:]), rms(hs[-1, -k:])                                    # [k, d] each
    D = torch.stack([first.mean(0), out.mean(0)], 1) if mode == "mean" else torch.cat([first, out]).T
    N = torch.linalg.qr(D).Q
    x = last(hs)[1:-1]
    return x - (x @ N) @ N.T                                                           # [15, d]


@geometry("minus this prompt's first and output layers", [()], fitted="nothing")
def minus_ends(hs):
    return _minus_ends(hs).mean(0)


@geometry("minus this prompt's first and output layers, at the layer they explain least", [()], fitted="nothing")
def minus_ends_least_explained(hs):  # each row starts with the same norm, so the largest remainder is the least explained
    left = _minus_ends(hs)
    return left[left.norm(dim=-1).argmax()]


@geometry("minus first and output layers over recent tokens (idea: Sandy Fraser)",
          [(k, mode) for k in (2, 4, 8, 16) for mode in ("mean", "span")], fitted="nothing")
def minus_window(hs, k, mode):  # Sandy's idea: average the early and output states over the last k tokens, then remove
    return _minus_ends(hs, k, mode).mean(0)


# ---- reference: may use logits, token ids or the J-lens, and pick a layer on the dev pair ----
@reference("logit lens, layer picked on the dev pair", [(l,) for l in range(20, 32)], fitted="nothing")
def plain(s, l):  # the old rule: shows what knowing the layer is worth
    return readout(s["res"][l])


@reference("J-lens", [(l,) for l in range(20, 32)], fitted="J-lens")
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@reference("J-lens minus output-layer PCA", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], fitted="J-lens, WikiText")
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


@reference("rise-and-fall", [(27,)], fitted="nothing")
def rise_and_fall(s, peak):  # tokens whose logit rises from layer 22 to the peak and falls by the output
    return _rise_fall(readout(s["res"][22]), readout(s["res"][peak]), readout(s["res"][32]))


@reference("rise-and-fall, J-lens", [(p,) for p in (26, 27, 28, 29)], fitted="J-lens")
def rise_and_fall_j(s, peak):
    return _rise_fall(readout(jlens(s["res"][22], 22)), readout(jlens(s["res"][peak], peak)), s["logits"])


@reference("rise-and-fall token span (rank 32)", [(27,)], fitted="nothing")
def suppressed_subspace(s, l):  # per prompt: span of the 32 rise-and-fall tokens' unembeddings
    S = _token_span(rise_and_fall(s, l), 32)
    return readout(S @ (S.T @ rms(s["res"][l])))


@reference("rise-and-fall token span (rank 32), J-lens", [(p,) for p in (26, 27, 28, 29)], fitted="J-lens")
def suppressed_subspace_j(s, peak):
    S = _token_span(rise_and_fall_j(s, peak), 32)
    return readout(S @ (S.T @ rms(jlens(s["res"][peak], peak))))


@reference("calibrated rise-and-fall", [(p,) for p in (26, 27, 28, 29)], fitted="WikiText")
def calibrated_rise_and_fall(s, peak):  # rise-and-fall on per-token z-scores of each layer's logits
    z = lambda l: (readout(s["res"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]
    return _rise_fall(z(22), z(peak), z(32))


@reference("calibrated rise-and-fall, last line", [(p,) for p in (27, 28)], fitted="WikiText")
def calibrated_rise_and_fall_line(s, peak):  # max over the tokens of the prompt's last line, not just the last token
    z = lambda l: (readout(s["line"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]   # [tok, vocab]
    early, mid, out = z(22), z(peak), z(32)
    return torch.stack([_rise_fall(e, m, o) for e, m, o in zip(early, mid, out)]).amax(0)


@reference("calibrated rise-and-fall, attention-weighted", [(p, t) for p in (27, 28) for t in (1.0, 3.0)], fitted="WikiText")
def calibrated_rise_and_fall_attn(s, peak, temperature):  # favour tokens the layer-23 attention output also writes
    a = readout(s["attn"])
    return calibrated_rise_and_fall(s, peak) * torch.sigmoid((a - a.mean()) / (a.std() * temperature))


@reference("logit lens minus read and said", [(l, k) for l in (24, 26, 28) for k in (8, 32)], fitted="nothing")
def minus_read_and_said(s, l, k):  # remove the prompt's token directions and the model's top-k next tokens
    ids = torch.cat([s["ids"], s["logits"].topk(k).indices]).unique()
    Q = torch.linalg.qr((W[ids] * gain).T, mode="reduced").Q
    x = rms(s["res"][l])
    return readout(x - Q @ (Q.T @ x))


@reference("layer-23 attention output, J-lens", [(23,)], fitted="J-lens")
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
