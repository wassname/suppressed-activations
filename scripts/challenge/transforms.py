"""Candidate methods for one forward pass.

A `@geometry` method gets one prompt's residual stream (layers 16-32, all prompt tokens) and returns one
residual-stream vector. It picks no layer by hand, and uses no token scores, token ids or word lists; it may use the
model's weights, including the output head as a matrix. The scorer reads the vector with the output head only to check
which words it holds. `@reference` methods (token scores, J-lens, a layer picked on the dev pair) are listed
separately. `settings` is the grid searched on the dev pair; `fitted` says what the method is fitted on besides the
model's weights. — PI/OpenAI
"""
import torch

from common import DEVICE, W, gain, load_jlens, readout, rms, vocab

TRANSFORMS = {}  # short name -> entry; geometry fn(hs, state) -> vector [d], reference fn(s) -> scores [vocab]
RANKS = (64, 256, 1024)
CAL_LAYERS = (22, 26, 27, 28, 29, 32)
FIRST = 16  # hs[i] is layer FIRST + i; hs[-1] is the output layer (32)
CHURN_LAYERS = tuple(range(16, 32))  # layer-change PCA bases, for the leaderboard and notebook.py
J = load_jlens()
_J = {}


def jlens(x, l):
    """Residual l through the Jacobian lens to the final residual."""
    if l not in _J:
        _J[l] = J[l - 1].to(DEVICE).float()
    return x.float() @ _J[l].T


def _register(kind):
    def transform(name, setting=(), fitted="nothing", about="", author=""):
        def register(fn):
            TRANSFORMS[name] = {"kind": kind, "fn": fn, "setting": tuple(setting), "fitted": fitted,
                                "about": about or name, "author": author}
            return fn
        return register
    return transform


geometry, reference = _register("geometry"), _register("reference")


def project(B, x):
    return B @ (B.T @ rms(x))


def remove(B, x):
    x = rms(x)
    return x - B @ (B.T @ x)


# ---- calibration: fitted once on unlabelled text (WikiText, and dev prompts without their answers) ----
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


# ---- geometry: method(hs, state) -> one residual-stream vector ----
# hs: one prompt's residual stream, layers 16-32, all prompt tokens. No hand-picked layer: a method uses every layer
# it gets, or picks one from the activations. state: what calibrate() fitted.
last = lambda hs: rms(hs[:, -1])  # [17, d]: the last prompt token at each layer


@geometry("mean over layers", about="Logit lens of the last token, averaged over layers 16-32 (control)")
def mean_lens(hs, state):
    return last(hs).mean(0)


@geometry("random subspace", (1024,), fitted="random seed", about="Mean over layers, projected on a random rank-1024 subspace (control)")
def random_subspace(hs, state, r):
    return project(state["random"][:, :r], last(hs).mean(0))


@geometry("mean calibration text", fitted="calibration text", about="Ignores the prompt: the mean layer-28 activation on calibration text (control)")
def fixed_list(hs, state):
    return state["mean28"]


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
          about="Mean over layers, projected on AntiPaSTO's suppressed subspace (github.com/wassname/AntiPaSTO)")
def suppressed_antipasto(hs, state, r):
    return project(state["suppressed (AntiPaSTO)"][:, :r], last(hs).mean(0))


@geometry("weak head directions", (1024,), about="Mean over layers, projected on the directions the output head reads least")
def weak_readout(hs, state, r):
    return project(state["weak-readout"][:, :r], last(hs).mean(0))


@geometry("minus output PCA", (16,), fitted="calibration text",
          about="Mean over layers, minus the top PCs of output-layer activations on calibration text")
def minus_output(hs, state, r):
    return remove(state["output"][:, :r], last(hs).mean(0))


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


# ---- reference: may use logits, token ids or the J-lens, and pick a layer on the dev pair ----
@reference("logit lens, best layer", (27,), about="Logit lens at layer 27, the best layer on the dev pair: what knowing the layer is worth")
def plain(s, l):  # the old rule: shows what knowing the layer is worth
    return readout(s["res"][l])


@reference("J-lens", (23,), fitted="J-lens", about="Jacobian lens (Gurnee et al. 2026) at layer 23")
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@reference("J-lens minus output PCA", (28, 256), fitted="J-lens, calibration text", about="J-lens at layer 28, minus the top-256 output-layer PCs")
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


@reference("rise-and-fall", (27,), about="Tokens whose logit rises from layer 22 to 27 and falls by the output")
def rise_and_fall(s, peak):  # tokens whose logit rises from layer 22 to the peak and falls by the output
    return _rise_fall(readout(s["res"][22]), readout(s["res"][peak]), readout(s["res"][32]))


@reference("rise-and-fall, J-lens", (28,), fitted="J-lens", about="Rise-and-fall on J-lens scores, peak layer 28")
def rise_and_fall_j(s, peak):
    return _rise_fall(readout(jlens(s["res"][22], 22)), readout(jlens(s["res"][peak], peak)), s["logits"])


@reference("rise-and-fall span", (27,), about="Span of the 32 rise-and-fall tokens' output-head rows, applied to layer 27")
def suppressed_subspace(s, l):  # per prompt: span of the 32 rise-and-fall tokens' unembeddings
    S = _token_span(rise_and_fall(s, l), 32)
    return readout(S @ (S.T @ rms(s["res"][l])))


@reference("rise-and-fall span, J-lens", (28,), fitted="J-lens", about="As rise-and-fall span, with the J-lens, layer 28")
def suppressed_subspace_j(s, peak):
    S = _token_span(rise_and_fall_j(s, peak), 32)
    return readout(S @ (S.T @ rms(jlens(s["res"][peak], peak))))


@reference("calibrated rise-and-fall", (28,), fitted="calibration text", about="Rise-and-fall on per-token z-scores of each layer's logits, peak layer 28")
def calibrated_rise_and_fall(s, peak):  # rise-and-fall on per-token z-scores of each layer's logits
    z = lambda l: (readout(s["res"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]
    return _rise_fall(z(22), z(peak), z(32))


@reference("calibrated rise-and-fall, last line", (27,), fitted="calibration text", about="Calibrated rise-and-fall, max over the tokens of the prompt's last line")
def calibrated_rise_and_fall_line(s, peak):  # max over the tokens of the prompt's last line, not just the last token
    z = lambda l: (readout(s["line"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]   # [tok, vocab]
    early, mid, out = z(22), z(peak), z(32)
    return torch.stack([_rise_fall(e, m, o) for e, m, o in zip(early, mid, out)]).amax(0)


@reference("calibrated rise-and-fall, attention", (28, 1.0), fitted="calibration text", about="Calibrated rise-and-fall, weighted towards tokens the layer-23 attention output writes")
def calibrated_rise_and_fall_attn(s, peak, temperature):  # favour tokens the layer-23 attention output also writes
    a = readout(s["attn"])
    return calibrated_rise_and_fall(s, peak) * torch.sigmoid((a - a.mean()) / (a.std() * temperature))


@reference("logit lens minus read and said", (28, 8), about="Layer 28 minus the prompt's token directions and the model's top-8 next tokens")
def minus_read_and_said(s, l, k):  # remove the prompt's token directions and the model's top-k next tokens
    ids = torch.cat([s["ids"], s["logits"].topk(k).indices]).unique()
    Q = torch.linalg.qr((W[ids] * gain).T, mode="reduced").Q
    x = rms(s["res"][l])
    return readout(x - Q @ (Q.T @ x))


@reference("attention output, J-lens", (23,), fitted="J-lens", about="J-lens of what layer 23's attention adds at the last token")
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
