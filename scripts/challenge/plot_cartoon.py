"""Cartoon for the README: input, hidden English and output across layers. Not data. Writes figs/cartoon.png.

Usage: uv run --with matplotlib scripts/challenge/plot_cartoon.py (fonts: Humor Sans, Noto Sans Arabic) — PI/OpenAI
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
plt.rcParams["font.family"] = ["Humor Sans", "DejaVu Sans"]  # hand-drawn font; DejaVu for Cyrillic
np.random.seed(0)

GREY, ORANGE, BLUE = "#7f7f7f", "#d55e00", "#0072b2"
x = np.linspace(0, 1, 300)
bump = lambda c, w, h: h * np.exp(-((x - c) / w) ** 2)
curves = {"input": (bump(0.10, 0.26, 0.5), GREY), "hidden": (bump(0.58, 0.13, 0.8), ORANGE),
          "output": (1.0 / (1 + np.exp(-(x - 0.88) / 0.07)) * 0.95, BLUE)}

fig, ax = plt.subplots(figsize=(9.5, 5.6))
fig.subplots_adjust(left=0.08, right=0.98, top=0.89, bottom=0.17)
for y, color in curves.values():
    ax.plot(x, y, color=color, lw=3)


def label(x0, y0, name, words, color, family="DejaVu Sans"):
    """Language name, then example words in that language, as one direct label."""
    ax.text(x0, y0, name, color=color, fontsize=15, ha="center")
    ax.text(x0, y0 - 0.09, words, color=color, fontsize=13, ha="center", family=family)


label(0.17, 0.66, "ARABIC (input)", "قطة  كلب  شمس", GREY, family="Noto Sans Arabic")
label(0.58, 0.96, "ENGLISH (hidden)", "cat  dog  sun", ORANGE)
label(0.83, 1.12, "RUSSIAN (output)", "кошка  собака  солнце", BLUE)

ax.axvline(0.58, color="k", ls=":", lw=1.2, ymax=0.62)
ax.text(0.58, -0.035, "↑ one layer: a mix of all three", ha="center", va="top", fontsize=12,
        transform=ax.get_xaxis_transform())
ax.annotate("isolate the\nEnglish part", xy=(0.66, 0.62), xytext=(0.72, 0.52), fontsize=14, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
ax.annotate("not this", xy=(0.26, 0.37), xytext=(0.30, 0.52), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
ax.annotate("or this", xy=(0.86, 0.40), xytext=(0.90, 0.16), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
fig.text(0.5, 0.02, "The challenge: find a geometric transform or subspace of the activations that keeps\n"
         "the English part, without word lists, token lookup or language labels.", fontsize=12, ha="center")
ax.text(0.99, 1.0, "schematic, not data", fontsize=10, color="#999999", ha="right", va="top", transform=ax.transAxes)

ax.set_title("Arabic → Russian: English shows up in the middle layers", fontsize=16)
ax.text(1.0, -0.035, "layers →", ha="right", va="top", fontsize=12, transform=ax.transAxes)
ax.set_ylabel("how strongly the model\nholds each language")
ax.set(xlim=(0, 1), ylim=(0, 1.25), xticks=[], yticks=[])
ax.spines[["top", "right"]].set_visible(False)
(ROOT / "figs").mkdir(exist_ok=True)
fig.savefig(ROOT / "figs/cartoon.png", dpi=150)  # PNG: the hand-drawn font makes a large SVG
