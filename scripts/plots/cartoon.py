"""Distribution schematic with words from the measured spider readout. — PI/OpenAI"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from unspoken_concepts import ROOT


def draw():
    demo = json.loads((ROOT / "results/spider_demo.json").read_text())
    words = {r["layer"]: r["words"] for r in demo["readouts"]}
    assert {"spider", "蜘蛛"} <= set(words[24]) and demo["answer"] == "8"
    plt.rcParams["font.family"] = ["DejaVu Sans", "Noto Sans CJK SC"]
    grey, orange, blue = "#7f7f7f", "#d55e00", "#0072b2"
    x = np.linspace(0, 1, 300)
    bump = lambda c, w, h: h * np.exp(-((x - c) / w) ** 2)
    curves = ((bump(0.10, 0.26, 0.5), grey), (bump(0.58, 0.13, 0.8), orange),
              (0.95 / (1 + np.exp(-(x - 0.88) / 0.07)), blue))
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.81, bottom=0.10)
    for y, color in curves:
        ax.fill_between(x, y, color=color, alpha=0.12, linewidth=0)
        ax.plot(x, y, color=color, linewidth=3)
    ax.text(0.16, 0.25, "INPUT: Arabic", ha="center", fontsize=13, weight="bold", color="#333333")
    ax.text(0.16, 0.19, "How many legs on a\nweb-spinning animal?", ha="center", va="top", fontsize=12,
            color="#333333", linespacing=1.25)
    ax.text(0.16, 0.025, "short English gloss", ha="center", fontsize=9, color="#555555")
    ax.text(0.58, 0.40, "THOUGHTS", ha="center", fontsize=13, weight="bold", color="#8a3200")
    ax.text(0.58, 0.28, "spider  蜘蛛", ha="center", fontsize=18, color="#8a3200")
    ax.text(0.58, 0.20, "English / Chinese", ha="center", fontsize=11, color="#555555")
    ax.text(0.88, 0.22, "OUTPUT", ha="center", fontsize=13, weight="bold", color="#00456e")
    ax.text(0.88, 0.075, demo["answer"], ha="center", fontsize=25, color="#00456e")
    ax.annotate("find this", xy=(0.635, 0.68), xytext=(0.66, 0.85), fontsize=14, color="#8a3200",
                weight="bold", arrowprops={"arrowstyle": "->", "color": orange, "lw": 2})
    ax.annotate("not this", xy=(0.22, 0.41), xytext=(0.27, 0.63), fontsize=14,
                arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.5})
    ax.annotate("or this", xy=(0.955, 0.71), xytext=(0.88, 0.95), fontsize=14,
                arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.5})
    fig.text(0.5, 0.95, "Unspoken Concepts Challenge", fontsize=17, ha="center")
    fig.text(0.5, 0.865, "Find the unspoken intermediate concepts in a language model.",
             fontsize=14, ha="center", weight="bold")
    ax.text(1, -0.045, "layers →", ha="right", va="top", fontsize=12, transform=ax.transAxes)
    ax.set_ylabel("how strongly the model\nrepresents each part")
    ax.set(xlim=(0, 1), ylim=(0, 1.05), xticks=[], yticks=[])
    ax.spines[["top", "right"]].set_visible(False)
    fig.canvas.draw()
    bounds = fig.get_tightbbox(fig.canvas.get_renderer())
    width, height = fig.get_size_inches()
    assert bounds.x0 >= 0 and bounds.y0 >= 0 and bounds.x1 <= width and bounds.y1 <= height
    fig.savefig(ROOT / "figs/cartoon.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    draw()
