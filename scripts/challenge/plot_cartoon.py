"""Cartoon for the README: input, hidden English and output across layers. The curves are made up; the words are a
real J-lens readout, its first 4 words (Arabic→Russian "tea", layer 23: the first ar→ru test prompt
where the J-lens finds the word cleanly, out/2026-10-06_141151_leaderboard). Writes figs/cartoon.png.

Usage: uv run --with matplotlib scripts/challenge/plot_cartoon.py (font: Noto Sans Arabic) — PI/OpenAI
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
plt.rcParams["font.family"] = ["DejaVu Sans"]  # plain font, easy to read
np.random.seed(0)

GREY, ORANGE, BLUE = "#7f7f7f", "#d55e00", "#0072b2"
DARK = {GREY: "#333333", ORANGE: "#8a3200", BLUE: "#00456e"}  # text colours, readable on the light fills
x = np.linspace(0, 1, 300)
bump = lambda c, w, h: h * np.exp(-((x - c) / w) ** 2)
curves = {"input": (bump(0.10, 0.26, 0.5), GREY), "hidden": (bump(0.58, 0.13, 0.8), ORANGE),
          "output": (1.0 / (1 + np.exp(-(x - 0.88) / 0.07)) * 0.95, BLUE)}

fig, ax = plt.subplots(figsize=(9.5, 5.6))
fig.subplots_adjust(left=0.08, right=0.98, top=0.83, bottom=0.09)
for y, color in curves.values():
    ax.fill_between(x, y, color=color, alpha=0.12, lw=0)
    ax.plot(x, y, color=color, lw=3)


def label(x0, y0, name, words, color, family="DejaVu Sans"):
    """Language name, then example words in that language, as one direct label."""
    ax.text(x0, y0, name, color=DARK[color], fontsize=13, ha="center", weight="bold")
    ax.text(x0, y0 - 0.035, words, color=DARK[color], fontsize=13, ha="center", va="top", family=family)


label(0.12, 0.22, "READ: Arabic", "شاي\n(tea)", GREY, family=["Noto Sans Arabic", "DejaVu Sans"])
label(0.58, 0.36, "THINK: English", "tea  drink\ncoffee  vodka", ORANGE)
label(0.865, 0.19, "SAY: Russian", "чай (tea)", BLUE)

ax.annotate("find this", xy=(0.635, 0.68), xytext=(0.66, 0.84), fontsize=14, color=DARK[ORANGE],
            weight="bold", arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
ax.annotate("not this", xy=(0.22, 0.41), xytext=(0.27, 0.62), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
ax.annotate("or this", xy=(0.955, 0.71), xytext=(0.90, 0.95), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))

fig.text(0.5, 0.95, "Translating Arabic to Russian, the model thinks partly in English", fontsize=16, ha="center")
fig.text(0.5, 0.885, "Challenge: find the thinking part, without using a dictionary", fontsize=15,
         ha="center", weight="bold")
ax.text(1.0, -0.035, "layers →", ha="right", va="top", fontsize=12, transform=ax.transAxes)
ax.set_ylabel("how strongly the model\nholds each language")
ax.set(xlim=(0, 1), ylim=(0, 1.05), xticks=[], yticks=[])
ax.spines[["top", "right"]].set_visible(False)
(ROOT / "figs").mkdir(exist_ok=True)
fig.savefig(ROOT / "figs/cartoon.png", dpi=150)
