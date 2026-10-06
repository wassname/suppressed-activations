"""Candidate transforms of one forward pass.

The challenge is geometry: a `@geometry` transform maps activations to an activation-space vector (a projection or
other map), without the output head, token ids or logits. The scorer reads that vector with the model's output head
only to check which words it holds. `@reference` transforms (output head, token scores, J-lens) return token scores
directly and are listed separately. `settings` is the grid searched on the dev pair; `fitted` says what the transform
is fitted on besides the model's weights. — PI/OpenAI
"""
import json

import torch

from common import ROOT, W, forward, gain, load_jlens, model, readout, rms, tok, vocab

TRANSFORMS = {}  # name -> (settings, fitted, kind, fn); geometry fn -> vector [d], reference fn -> scores [vocab]
RANKS = (64, 256, 1024)
RIDGE_LAYERS, CAL_LAYERS = (24, 27, 29), (22, 26, 27, 28, 29, 32)
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
bases, token_counts = {}, torch.zeros(len(vocab), dtype=torch.long)


def fit_bases():
    d = W.shape[1]
    texts = json.loads((ROOT / "data/challenge/wikitext2_train_300.json").read_text())["texts"]
    keys = ("x22", "x24", "x27", "x29", "x32", "supp", "antipasto", "net") + tuple(f"d{l}" for l in CHURN_LAYERS)
    rf = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in ("27", "28", "27 shuffled")}  # sum aᵀb
    rf_first = {k: torch.zeros(2, d, dtype=torch.float64, device="cuda") for k in rf}
    cross = {l: torch.zeros(d, d, dtype=torch.float64, device="cuda") for l in RIDGE_LAYERS}   # sum of x32ᵀ x_l
    logit_sum = {l: torch.zeros(len(vocab), dtype=torch.float64, device="cuda") for l in CAL_LAYERS}
    logit_sq = {l: torch.zeros(len(vocab), dtype=torch.float64, device="cuda") for l in CAL_LAYERS}
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
        for l in RIDGE_LAYERS:
            cross[l] += x[32].T @ x[l]
        for k in rf:  # signed rise (peak - early) against fall (peak - output), per token
            p_ = int(k[:2])
            a, b = x[p_] - x[22], x[p_] - x[32]
            if k.endswith("shuffled"):
                b = b.roll(1, dims=0)  # control: pair each token's rise with another token's fall
            rf[k] += a.T @ b
            rf_first[k] += torch.stack([a.sum(0), b.sum(0)])
        for l in CAL_LAYERS:
            logits = ((gain * rms(res[l, 8:])) @ W.T).double()        # [tok, vocab], as readout() per token
            logit_sum[l] += logits.sum(0)
            logit_sq[l] += logits.square().sum(0)
        pairs = [("x22", x[22]), ("x24", x[24]), ("x27", x[27]), ("x29", x[29]), ("x32", x[32]), ("supp", supp),
                 ("antipasto", antipasto), ("net", net)] + [(f"d{l}", x[l + 1] - x[l]) for l in CHURN_LAYERS]
        for k, v in pairs:
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
    for l in CHURN_LAYERS:
        bases[f"churn{l}"] = top(cov[f"d{l}"])
    for l in (24, 27, 29):
        write = torch.linalg.svd(mlp(l - 1).down_proj.weight.float(), full_matrices=False).U
        read = torch.linalg.svd(torch.cat([mlp(l).up_proj.weight.float(), mlp(l).gate_proj.weight.float()]),
                                full_matrices=False).Vh.T
        bases[f"write minus top-read{l}"] = {r: torch.linalg.qr(write[:, :r] - read[:, :r] @ (read[:, :r].T @ write[:, :r])).Q
                                             for r in RANKS}
    bases["erased-variance"] = top(cov["x27"] - cov["x32"])
    bases["added then removed"] = top(cov["supp"])
    bases["suppressed (AntiPaSTO)"] = top(cov["antipasto"])
    bases["net change"] = top(cov["net"])
    for k in rf:
        m = rf[k] / n - torch.outer(rf_first[k][0] / n, rf_first[k][1] / n)
        bases[f"rise-fall {k}"] = top((m + m.T) / 2)                    # most positive rise-fall coupling first
    bases["output"] = top(cov["x32"])
    bases["mean28"] = (mean28 / n).float()
    eye = torch.eye(d, dtype=torch.float64, device="cuda")
    C32 = cov["x32"]
    mu = {k: first[k] / n for k in keys}
    B = bases["churn27"][:, :1024].double()
    for l in (22, 27, 32):  # mean and spread of each layer-change PC coordinate, per layer
        bases[f"pc stats{l}"] = ((B.T @ mu[f"x{l}"]).float(), torch.diagonal(B.T @ cov[f"x{l}"] @ B).sqrt().float())
    for l in RIDGE_LAYERS:  # ridge regression of x_l on x32: what the output state does not explain
        A = torch.linalg.solve(C32 + 1e-2 * C32.trace() / d * eye, cross[l] / n - torch.outer(mu["x32"], mu[f"x{l}"]))
        bases[f"ridge{l}"] = (A.float(), mu[f"x{l}"].float(), mu["x32"].float())
    for l in CAL_LAYERS:  # per-layer, per-token logit mean and shrunk scale
        m = logit_sum[l] / n
        var = (logit_sq[l] / n - m.square()).clamp_min(0)
        bases[f"calib{l}"] = (m.float(), (var + var.median()).sqrt().float())
    L = torch.linalg.cholesky(C32 + 1e-3 * C32.trace() / d * eye)  # generalized eigenvectors of (C27, C32)
    M = torch.linalg.solve_triangular(L, torch.linalg.solve_triangular(L, cov["x27"], upper=False).T, upper=False)
    V = torch.linalg.solve_triangular(L.T, torch.linalg.eigh(M)[1].flip(-1), upper=True)
    bases["variance ratio"] = {r: torch.linalg.qr(V[:, :r]).Q.float() for r in RANKS}


# ---- the transforms ----
@geometry("identity (logit lens)", [(l,) for l in range(20, 32)], fitted="nothing")
def plain(s, l):
    return s["res"][l]


@reference("J-lens", [(l,) for l in range(20, 32)], fitted="J-lens")
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@geometry("mean WikiText activation (control)", [(28,)], fitted="WikiText")
def fixed_list(s, l):  # ignores the prompt: readout of the mean WikiText residual
    return bases["mean28"]


@geometry("input word (control)", [(l,) for l in (8, 12, 16, 20)], fitted="nothing")
def input_word(s, l):  # reads the input word itself, not the last token: does recovering the meaning need a hidden step?
    return s["input"][l]


@geometry("random subspace (control)", [(27, r) for r in RANKS], fitted="random seed")
def random_subspace(s, l, r):
    return project(bases["random"][:, :r], s["res"][l])


@geometry("layer-change PCA", [(l, r) for l in (24, 27, 29) for r in RANKS], fitted="WikiText")
def churn(s, l, r):  # largest layer-to-layer change on generic text
    return project(bases[f"churn{l}"][:, :r], s["res"][l])


@geometry("MLP write minus next MLP read", [(l, r) for l in (24, 27, 29) for r in RANKS], fitted="nothing")
def write_minus_top_read(s, l, r):  # top-r directions block l-1's MLP writes, minus the top-r its next MLP reads
    return project(bases[f"write minus top-read{l}"][r], s["res"][l])


@geometry("variance gone by the output (PCA)", [(27, r) for r in RANKS], fitted="WikiText")
def erased_variance(s, l, r):  # variance at layer 27 that is gone by 32
    return project(bases["erased-variance"][:, :r], s["res"][l])


@reference("directions the output head reads least", [(27, r) for r in RANKS], fitted="nothing")
def weak_readout(s, l, r):
    return readout(project(bases["weak-readout"][:, :r], s["res"][l]))


@geometry("added then removed", [(27, r) for r in RANKS], fitted="WikiText")
def added_then_removed(s, l, r):  # pca(min(increases, decreases)) of per-coordinate magnitudes
    return project(bases["added then removed"][:, :r], s["res"][l])


@geometry("net-change PCA (AntiPaSTO without the output-head step)", [(27, r) for r in RANKS], fitted="WikiText")
def net_change(s, l, r):  # PCA of h32 - h3 on WikiText
    return project(bases["net change"][:, :r], s["res"][l])


@reference("AntiPaSTO suppressed subspace", [(27, r) for r in RANKS], fitted="WikiText")
def suppressed_antipasto(s, l, r):  # compute_suppressed_from_hidden_states in github.com/wassname/AntiPaSTO, on all tokens
    return readout(project(bases["suppressed (AntiPaSTO)"][:, :r], s["res"][l]))


@geometry("minus output-layer PCA", [(l, r) for l in (26, 28, 30) for r in (16, 64, 256)], fitted="WikiText")
def minus_output(s, l, r):  # remove the top-r PCs of output-layer activations on WikiText
    return remove(bases["output"][:, :r], s["res"][l])


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


@geometry("signed rise-fall coupling", [(p, r) for p in (27, 28) for r in RANKS], fitted="WikiText")
def rise_fall_coupling(s, peak, r):  # directions where a rise (peak - layer 22) goes with a fall (peak - output)
    return project(bases[f"rise-fall {peak}"][:, :r], s["res"][peak])


@geometry("signed rise-fall coupling, shuffled (control)", [(27, r) for r in RANKS], fitted="WikiText")
def rise_fall_coupling_shuffled(s, peak, r):  # same, but rise and fall from different tokens
    return project(bases["rise-fall 27 shuffled"][:, :r], s["res"][peak])


@geometry("minus this prompt's early and output states", [(p, e, o) for p in (26, 27, 28) for e in ("22", "16,19,22")
                                                          for o in ("32", "30,31,32")], fitted="nothing")
def minus_early_and_output(s, peak, early, late):  # remove the span of this prompt's own early and output-side states
    layers = [int(l) for l in f"{early},{late}".split(",")]
    N = torch.linalg.qr(torch.stack([rms(s["res"][l]) for l in layers], 1)).Q
    x = rms(s["res"][peak])
    return x - N @ (N.T @ x)


@geometry("minus early and output states over recent tokens (idea: Sandy Fraser)",
          [(p, k, mode) for p in (26, 27, 28) for k in (1, 2, 4, 8, 16) for mode in ("mean", "span")], fitted="nothing")
def minus_window(s, peak, k, mode):  # like the row above, but uses layers 22 and 32 at the last k tokens of the last line
    early, late = rms(s["line"][22, -k:]), rms(s["line"][32, -k:])                    # [k, d] each
    D = torch.stack([early.mean(0), late.mean(0)], 1) if mode == "mean" else torch.cat([early, late]).T
    N = torch.linalg.qr(D).Q
    x = rms(s["res"][peak])
    return x - N @ (N.T @ x)


@geometry("layer-change PCs gated by rise and fall", [(r, tau) for r in (256, 1024) for tau in (0.1, 1.0)],
          fitted="WikiText")
def pc_rise_fall_gate(s, r, tau):  # keep PC coordinates that rise from layer 22 to 27 and fall by the output
    B = bases["churn27"][:, :r]
    z = lambda l: (B.T @ rms(s["res"][l]) - bases[f"pc stats{l}"][0][:r]) / bases[f"pc stats{l}"][1][:r]
    rise, fall = (z(27) - z(22)).clamp_min(0), (z(27) - z(32)).clamp_min(0)
    g = rise * fall / (rise * fall + tau)
    return B @ (g * (B.T @ rms(s["res"][27])))


@geometry("layer-change PCs gated by attention", [(r, k) for r in (256, 1024) for k in (0.1, 1.0)], fitted="WikiText")
def pc_attention_gate(s, r, k):  # keep PC coordinates that layer 23's attention output also writes
    B = bases["churn27"][:, :r]
    a = B.T @ rms(s["attn"])
    g = a.square() / (a.square() + k * a.square().mean())
    return B @ (g * (B.T @ rms(s["res"][27])))


@geometry("output-unexplained residual (ridge)", [(l,) for l in RIDGE_LAYERS], fitted="WikiText")
def ridge_residual(s, l):  # x_l minus its ridge prediction from x32 (fitted on WikiText)
    A, mu_x, mu_y = bases[f"ridge{l}"]
    return (rms(s["res"][l]) - mu_x) - (rms(s["res"][32]) - mu_y) @ A


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


@geometry("variance ratio, layer 27 vs output", [(27, r) for r in RANKS], fitted="WikiText")
def variance_ratio(s, l, r):  # directions with high variance at layer 27 relative to the output layer
    return project(bases["variance ratio"][r], s["res"][l])


@reference("logit lens minus read and said", [(l, k) for l in (24, 26, 28) for k in (8, 32)], fitted="nothing")
def minus_read_and_said(s, l, k):  # remove the prompt's token directions and the model's top-k next tokens
    ids = torch.cat([s["ids"], s["logits"].topk(k).indices]).unique()
    Q = torch.linalg.qr((W[ids] * gain).T, mode="reduced").Q
    x = rms(s["res"][l])
    return readout(x - Q @ (Q.T @ x))


@reference("layer-23 attention output, J-lens", [(23,)], fitted="J-lens")
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
