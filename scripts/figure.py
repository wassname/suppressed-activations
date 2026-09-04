# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.10", "numpy>=2"]
# ///
# Written by PI/claude-opus-4.6 for Michael J. Clark.

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
ENGLISH = "#D55E00"
CHINESE = "#0072B2"
CONTROL = "#666666"
COLORS = {"en": ENGLISH, "zh": CHINESE, "en~": CONTROL}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open() as f:
        return list(csv.DictReader(f))


def assert_no_clip(fig: plt.Figure, tolerance_points: float = 1.0) -> None:
    fig.canvas.draw()
    box = fig.get_tightbbox(fig.canvas.get_renderer())
    width, height = fig.get_size_inches()
    tolerance = tolerance_points / 72
    assert box.x0 > -tolerance and box.y0 > -tolerance
    assert box.x1 < width + tolerance and box.y1 < height + tolerance


def language_probability(ax: plt.Axes, rows: list[dict[str, str]]) -> None:
    for language, style in (("en", "-"), ("zh", "-"), ("en~", "--")):
        lang_rows = [row for row in rows if row["language"] == language]
        layer = np.array([int(row["layer"]) for row in lang_rows])
        mean = np.array([float(row["mean_probability"]) for row in lang_rows])
        ci = np.array([float(row["ci95"]) for row in lang_rows])
        ax.plot(layer, mean, color=COLORS[language], lw=2.1, ls=style)
        ax.errorbar(layer, mean, yerr=ci, fmt="none", ecolor=COLORS[language],
                    elinewidth=0.65, capsize=1.2, alpha=0.42, errorevery=2)

    ax.text(27.3, 0.36, "English analog", color=ENGLISH, fontsize=8.5)
    ax.text(31.7, 0.61, "correct Chinese token", color=CHINESE, fontsize=8.5, ha="right")
    ax.annotate("unrelated English", xy=(19, 0.00007), xytext=(12.5, 0.055), color=CONTROL,
                fontsize=8, arrowprops={"arrowstyle": "-", "color": "0.65", "lw": 0.7})
    ax.set(xlim=(0, 32), ylim=(-0.015, 0.67), xlabel="layer index",
           ylabel="probability under the logit lens")
    ax.set_title("a   English appears before Chinese", loc="left", fontsize=10.5)


def layered_readout(
    ax: plt.Axes,
    rows: list[dict[str, str]],
    selection: str,
    title: str,
    shares: tuple[str, str],
) -> None:
    for language in ("en", "zh"):
        lang_rows = [
            row for row in rows
            if row["selection"] == selection and row["language"] == language
        ]
        layer = np.array([int(row["layer"]) for row in lang_rows])
        total = np.array([float(row["total_readout"]) for row in lang_rows])
        inside = np.array([float(row["inside_subspace"]) for row in lang_rows])
        color = COLORS[language]
        ax.plot(layer, total, color=color, lw=2.0, zorder=3)
        ax.fill_between(layer, 0, inside, where=inside >= 0, interpolate=True,
                        color=color, alpha=0.52, lw=0, zorder=1)
        ax.fill_between(layer, 0, inside, where=inside < 0, interpolate=True,
                        color=color, alpha=0.18, hatch="////", lw=0, zorder=1)

    ax.axhline(0, color="0.78", lw=0.7, zorder=0)
    ax.axvline(27, color="0.78", lw=0.7, ls=":", zorder=0)
    ax.axvline(32, color="0.78", lw=0.7, ls=":", zorder=0)
    ax.text(26.5, 0.098, shares[0], color=ENGLISH, fontsize=8, ha="right")
    ax.text(31.7, 0.143, shares[1], color=CHINESE, fontsize=8, ha="right")
    ax.set(xlim=(1, 32), ylim=(-0.014, 0.157), xlabel="layer index")
    ax.set_title(title, loc="left", fontsize=10.5)
    if selection == "same prompt":
        ax.legend(
            handles=[Line2D([], [], color="0.25", lw=1.7, label="complete readout"),
                     Patch(facecolor="0.45", alpha=0.45, label="inside subspace")],
            loc="upper left", frameon=False, fontsize=7.5, handlelength=1.5,
        )


def main() -> None:
    plt.rcParams["svg.hashsalt"] = "suppressed-activations"
    curves = read_rows(ROOT / "data/qwen_logit_lens_de_zh.csv")
    subspaces = read_rows(ROOT / "data/suppressed_subspace_by_layer.csv")

    fig, axes = plt.subplots(
        1, 3, figsize=(13.4, 4.15), constrained_layout=True,
        gridspec_kw={"width_ratios": [1.16, 1, 1]},
    )
    language_probability(axes[0], curves)
    layered_readout(
        axes[1], subspaces, "same prompt",
        "b   Own subspace\nEnglish inside; output mostly outside",
        ("English: 95% inside", "Chinese: 20% inside"),
    )
    layered_readout(
        axes[2], subspaces, "different prompt",
        "c   Different-prompt control\nNeither readout inside",
        ("English: 4% inside", "Chinese: −1% inside"),
    )
    axes[1].set_ylabel("answer readout / residual norm")
    axes[2].tick_params(labelleft=False)

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8.5)

    assert_no_clip(fig)
    out = ROOT / "figs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "suppressed_activations.png", dpi=220, facecolor="white")
    fig.savefig(out / "suppressed_activations.svg", facecolor="white", metadata={"Date": None})
    plt.close(fig)


if __name__ == "__main__":
    main()
