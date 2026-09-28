"""Summary figure for the English setting: lens curves, selector hit rates, pair transfer by layer window.
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.figure import CHINESE, CONTROL, ENGLISH, language_probability, read_rows  # noqa: E402

RUNS = sorted(ROOT.glob("out/*_english-baselines-L*/result.json"))
SERIES = {  # basis name in result.json -> (label, colour, style)
    "rise_and_fall (repo)": ("rise-and-fall selector (unsupervised)", "black", "-o"),
    "English answer tokens (oracle)": ("English answer tokens (oracle)", ENGLISH, "-s"),
    "Chinese answer tokens (oracle)": ("Chinese answer tokens (oracle)", CHINESE, "-s"),
    "full residual (upper bound)": ("whole residual vector", "0.6", "--"),
    "random rotation, matched to rise_and_fall norm": ("random, same edit norm", CONTROL, ":x"),
}


def main() -> None:
    runs = {int(re.search(r"-L(\d+)/", str(p)).group(1)): json.loads(p.read_text()) for p in RUNS}
    starts = sorted(runs)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), constrained_layout=True,
                             gridspec_kw={"width_ratios": [1.15, 0.9, 1.1]})

    language_probability(axes[0], read_rows(ROOT / "data/qwen_logit_lens_de_zh.csv"))
    axes[0].set_title("a   Logit lens: English rises, then Chinese", loc="left", fontsize=10.5)

    ax = axes[1]
    q1, n = runs[23]["q1"], runs[23]["n_q1"]
    names = ["rise_and_fall (repo)", "peak logit lens", "fall only", "rise only"]
    labels = ["rise-and-fall\n(this repo)", "L27 logit lens\n(top-32)", "fall only", "rise only"]
    y = range(len(names))
    ax.barh([i - 0.27 for i in y], [q1[k]["isolates"] / n for k in names], 0.26, color="black",
            label="isolates: English in, Chinese and German out")
    ax.barh([i for i in y], [q1[k]["en"] / n for k in names], 0.26, color=ENGLISH, label="English (hidden) in")
    ax.barh([i + 0.27 for i in y], [q1[k]["zh"] / n for k in names], 0.26, color=CHINESE, label="Chinese (said) in")
    ax.set_yticks(list(y), labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set(xlim=(0, 1), xlabel=f"fraction of {n} prompts with the word in the top-32 tokens")
    ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=1)
    ax.set_title("b   Find the hidden word, exclude the said word", loc="left", fontsize=10.5)

    ax = axes[2]
    for key, (label, colour, style) in SERIES.items():
        rate = [sum(r["to_target"] for r in runs[s]["q2"][key]) / len(runs[s]["q2"][key]) for s in starts]
        ax.plot(starts, rate, style, color=colour, label=label, lw=1.8, ms=5)
    n_pairs = len(runs[23]["q2"]["rise_and_fall (repo)"])
    ax.set(ylim=(-0.03, 1.03), xticks=starts, xticklabels=[f"L{s}–{s + 7}" for s in starts],
           xlabel="patched residual layers (last prompt token)",
           ylabel=f"fraction of {n_pairs} word pairs where\nthe top-1 token becomes the target's")
    en_word = [sum(r["top1"].strip().lower() == p["tgt"]["en"].lower()
                   for p, r in zip(runs[s]["pairs"], runs[s]["q2"]["English answer tokens (oracle)"])) for s in starts]
    ax.annotate(f"{en_word[-1]}/{n_pairs} say the target's\nEnglish word instead", xy=(starts[-1], 0.1),
                xytext=(starts[-1] - 3.2, 0.2), fontsize=7.5, color=ENGLISH,
                arrowprops={"arrowstyle": "-", "color": ENGLISH, "lw": 0.7})
    ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=2)
    ax.set_title("c   Swap component with another word's", loc="left", fontsize=10.5)

    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=8.5)
    out = ROOT / "figs/english_setting.png"
    fig.savefig(out, dpi=180, facecolor="white")
    print(out)


if __name__ == "__main__":
    main()
