"""Cartoon for the README: input, hidden English and output across layers. Not data. Writes figs/cartoon.svg/.png.

Usage: uv run --with matplotlib scripts/challenge/plot_cartoon.py — PI/OpenAI
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
plt.xkcd(scale=1, length=120, randomness=2)
plt.rcParams["font.family"] = ["Humor Sans", "DejaVu Sans"]  # fallback for Cyrillic
np.random.seed(0)

x = np.linspace(0, 1, 300)
bump = lambda c, w, h: h * np.exp(-((x - c) / w) ** 2)
arabic = bump(0.08, 0.10, 0.55)
english = bump(0.62, 0.13, 0.9)
russian = 1.0 / (1 + np.exp(-(x - 0.93) / 0.025))

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.plot(x, arabic, color="#7f7f7f", lw=3)
ax.plot(x, english, color="#d55e00", lw=3)
ax.plot(x, russian, color="#0072b2", lw=3)

ax.text(0.17, 0.40, 'Arabic (input)', color="#7f7f7f", fontsize=13)
ax.text(0.52, 0.95, 'English (hidden): "cat"', color="#d55e00", fontsize=13)
ax.text(0.71, 1.07, 'Russian (output): "кошка"', color="#0072b2", fontsize=13)

white = dict(facecolor="white", edgecolor="none", pad=2)
ax.annotate("We want to isolate this", xy=(0.58, 0.9), xytext=(0.18, 1.0), fontsize=14, color="#d55e00",
            arrowprops=dict(arrowstyle="->", color="#d55e00", lw=1.5))
ax.annotate("but not this", xy=(0.09, 0.56), xytext=(0.17, 0.78), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
ax.annotate("or this", xy=(0.92, 0.42), xytext=(0.76, 0.30), fontsize=14,
            arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
ax.text(0.5, 0.06, "without using language or tokens", fontsize=14, ha="center", bbox=white)

ax.set_title("When models translate Arabic to Russian, they think in English", fontsize=15)
ax.set_xlabel("layers →")
ax.set_ylabel("how much the model\nis thinking it")
ax.set(xlim=(0, 1), ylim=(0, 1.2), xticks=[], yticks=[])
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
(ROOT / "figs").mkdir(exist_ok=True)
for ext in ("svg", "png"):
    fig.savefig(ROOT / f"figs/cartoon.{ext}", dpi=150)
