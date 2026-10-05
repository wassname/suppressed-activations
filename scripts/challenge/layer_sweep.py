# %% [markdown]
# # Layer sweep: how does each geometry transform do at every layer?
#
# Runs on the leaderboard's test prompts and plots F1 (with a 90% bootstrap band), TPR and FPR per layer.
# Add your own transform to `METHODS`: a function `(s, layer) -> activation vector`, same rules as `@geometry`.
# Opens as a notebook in VS Code/Jupyter (percent cells), or run it:
# `uv run --with matplotlib scripts/challenge/layer_sweep.py`. Writes figs/layers.png. — PI/OpenAI

# %%
import gzip
import json
import time

import matplotlib
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bench import TEST, f1, judge, prepare, read_vector, translation_prompts
from common import ROOT, rms
from transforms import CHURN_LAYERS, bases, fit_bases, project

fit_bases()
LAYERS = list(CHURN_LAYERS)  # 16..31


def minus_early_and_output(s, l):  # the leaderboard winner, at any layer after 22
    if l <= 22:
        return None
    N = torch.linalg.qr(torch.stack([rms(s["res"][22]), rms(s["res"][32])], 1)).Q
    x = rms(s["res"][l])
    return x - N @ (N.T @ x)


METHODS = {  # name -> (fn(s, layer) -> vector or None, colour)
    "identity (logit lens)": (lambda s, l: s["res"][l], "#555555"),
    "random subspace, rank 1024": (lambda s, l: project(bases["random"][:, :1024], s["res"][l]), "#aaaaaa"),
    "layer-change PCA, rank 1024": (lambda s, l: project(bases[f"churn{l}"][:, :1024], s["res"][l]), "#0072b2"),
    "net-change PCA, rank 1024": (lambda s, l: project(bases["net change"][:, :1024], s["res"][l]), "#009e73"),
    "minus this prompt's x22 and x32": (minus_early_and_output, "#d55e00"),
}

# %%
rows = []
for item in translation_prompts(TEST, "test"):
    prepared = prepare(item)
    if prepared is None:
        continue
    state, leak = prepared
    s = {"res": state["res"], "attn": state["attn"]}  # geometry gets no logits or token ids
    for name, (fn, _) in METHODS.items():
        for l in LAYERS:
            v = fn(s, l)
            if v is not None:
                rows.append({"method": name, "layer": l, "split": item["split"], "word": item["word"]}
                            | judge(read_vector(v, name), item, leak))
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_layer-sweep"
out.mkdir(parents=True)
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump(rows, f, ensure_ascii=False)
print(out)

# %%
def boot_band(rs, n_boot=1000):
    g = torch.Generator().manual_seed(0)
    idx = torch.randint(len(rs), (n_boot, len(rs)), generator=g)
    vals = sorted(f1([rs[i] for i in row]) for row in idx.tolist())
    return vals[int(0.05 * n_boot)], vals[int(0.95 * n_boot)]


fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharex=True)
for name, (_, color) in METHODS.items():
    by_layer = {l: [r for r in rows if r["method"] == name and r["layer"] == l] for l in LAYERS}
    ls = [l for l in LAYERS if by_layer[l]]
    band = [boot_band(by_layer[l]) for l in ls]
    axes[0].fill_between(ls, [b[0] for b in band], [b[1] for b in band], color=color, alpha=0.15, lw=0)
    axes[0].plot(ls, [f1(by_layer[l]) for l in ls], color=color, lw=2)
    axes[0].text(ls[-1] + 0.2, f1(by_layer[ls[-1]]), name, color=color, fontsize=8, va="center")
    axes[1].plot(ls, [sum(r["hidden"] for r in by_layer[l]) / len(by_layer[l]) for l in ls], color=color, lw=2)
    axes[2].plot(ls, [sum(r["leaked"] for r in by_layer[l]) / len(by_layer[l]) for l in ls], color=color, lw=2)
n = len({(r["split"], r["word"]) for r in rows})
for ax, title in zip(axes, ["F1 ↑ (90% band)", "TPR ↑: hidden word in the top 8", "FPR ↓: input/output word in the top 8"]):
    ax.set_title(title, fontsize=10, loc="left")
    ax.set(xlabel="layer", ylim=(0, 1))
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_xlim(LAYERS[0], LAYERS[-1] + 6)  # room for the direct labels
fig.suptitle(f"Geometry transforms per layer, Qwen3.5-4B, {n} test prompts", fontsize=11, x=0.01, ha="left")
fig.tight_layout()
fig.savefig(ROOT / "figs/layers.png", dpi=150)
