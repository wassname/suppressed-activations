"""README figure: which language Qwen thinks in, and pass rates on unseen language pairs. -- Claudypoo[opus-4.8]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.figure import CHINESE, CONTROL, ENGLISH  # noqa: E402

RUN = sorted(ROOT.glob("out/*_erase-language-pairs/result.json"))[-1]
EXAMPLE = "fr→ru"
TEST = ["fr→ru", "ru→fr", "de→ru", "ru→de", "fr→de"]
SHOW = {  # selector key -> label, colour
    "peak_any − prompt & said words": ("rise-and-fall, read and said words removed", "black"),
    "peak lens L27 − prompt & said words": ("plain logit lens, read and said words removed", "0.4"),
    "rise_fall 22/27/32 (repo)": ("original rise-and-fall", "0.72"),
    "peak logit lens L27": ("plain logit lens", "#d0d0d0"),
}


def main() -> None:
    d = json.loads(RUN.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True, gridspec_kw={"width_ratios": [1, 1.3]})

    ax = axes[0]
    cur = np.array(d["curves"][EXAMPLE])  # [4, 33]: en, zh, input, output
    for k, (label, colour, style) in enumerate([("English (hidden)", ENGLISH, "-"), ("Chinese", CHINESE, "--"),
                                                ("French (input)", CONTROL, ":"), ("Russian (output)", "black", "-")]):
        ax.plot(range(33), cur[k], style, color=colour, lw=2, label=label)
    ax.set(xlim=(0, 32), ylim=(0, 0.65), xlabel="layer", ylabel="probability under the logit lens")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title(f"a   {EXAMPLE}: English word appears, then Russian (mean of 78 words)", loc="left", fontsize=10.5)

    ax = axes[1]
    keys = [k for k in SHOW if k in d["results"][TEST[0]]]
    x = np.arange(len(TEST))
    w = 0.8 / len(keys)
    for j, key in enumerate(keys):
        rate = [np.mean([r["ok"] for r in d["results"][p][key]]) for p in TEST]
        ax.bar(x + (j - (len(keys) - 1) / 2) * w, rate, w * 0.95, color=SHOW[key][1], label=SHOW[key][0])
    ax.set_xticks(x, TEST)
    ax.set(ylim=(0, 1), ylabel="fraction of prompts passed", xlabel="unseen language pair (input→output)")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2)
    ax.set_title("b   Find the hidden word, leave out input and output", loc="left", fontsize=10.5)

    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
    out = ROOT / "figs/language_pairs.png"
    fig.savefig(out, dpi=180, facecolor="white")
    print(out, "from", RUN)


if __name__ == "__main__":
    main()
