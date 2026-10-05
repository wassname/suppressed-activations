"""Figure for the README's "How it is scored": logit-lens probability by layer of the hidden word (positive) and of
the input and output languages (negative), on test prompts. Writes figs/scoring.svg and figs/scoring.png.

Usage: uv run --with matplotlib scripts/challenge/plot_scoring.py — PI/OpenAI
"""
import matplotlib
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bench import TEST, script, translation_prompts
from common import ROOT, forward, readout

READ_LAYER = 28
leak_script = {lang: torch.tensor(sorted(script[lang])).cuda() for lang in script}

curves = {"hidden": [], "output": [], "input": []}
for item in translation_prompts(TEST, "test"):  # the leaderboard's test prompts
    src, tgt = item["split"].split("→")
    res, _, _ = forward(item["prompt"])
    p = torch.softmax(readout(res[:, -1]), -1)                                      # [33 layers, vocab], logit lens
    curves["hidden"].append(p[:, sorted(item["right"])].sum(-1).cpu())
    curves["output"].append(p[:, leak_script[tgt]].sum(-1).cpu())
    curves["input"].append(p[:, leak_script[src]].sum(-1).cpu())
n = len(curves["hidden"])

fig, ax = plt.subplots(figsize=(9, 4.6))
style = {"hidden": ("#d55e00", "hidden word (English or Chinese)"),
         "output": ("#0072b2", "output language (and the next token)"),
         "input": ("#7f7f7f", "input language")}
layers = range(33)
for k, (color, label) in style.items():
    y = torch.stack(curves[k])
    lo, mid, hi = y.quantile(0.25, 0), y.median(0).values, y.quantile(0.75, 0)
    ax.fill_between(layers, lo, hi, color=color, alpha=0.15, lw=0)
    ax.plot(layers, mid, color=color, lw=2.5, label=label)
ax.axvline(READ_LAYER, color="k", ls="--", lw=1)
ax.text(READ_LAYER - 0.3, 0.97, f"a transform reads\nlayer {READ_LAYER} here", ha="right", va="top", fontsize=9,
        transform=ax.get_xaxis_transform())

h28 = torch.stack(curves["hidden"]).median(0).values[READ_LAYER]
ax.annotate("positive: in the top 8 → TP\nmissing → FN", xy=(READ_LAYER, h28), xytext=(13, 0.62),
            color=style["hidden"][0], fontsize=11, arrowprops=dict(arrowstyle="->", color=style["hidden"][0]))
o12 = torch.stack(curves["output"]).median(0).values[12]
ax.annotate("negative (input and output languages):\nin the top 8 → FP, absent → TN", xy=(12, o12), xytext=(4, 0.30),
            color=style["output"][0], fontsize=11, arrowprops=dict(arrowstyle="->", color=style["output"][0]))
ax.set(xlabel="layer", ylabel="probability under the logit lens", xlim=(0, 32), ylim=(0, 1))
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.set_title(f"Qwen3.5-4B translating ar→hi, hi→th, th→ru, ko→ar ({n} prompts, last token; median and quartiles)",
             fontsize=10, loc="left")
fig.tight_layout()
(ROOT / "figs").mkdir(exist_ok=True)
for ext in ("svg", "png"):
    fig.savefig(ROOT / f"figs/scoring.{ext}", dpi=150)
print({k: [round(float(v), 3) for v in torch.stack(c).median(0).values[[0, 16, 22, 26, 28, 30, 32]]] for k, c in curves.items()})
