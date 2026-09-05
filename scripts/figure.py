# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.10", "numpy>=2"]
# ///
"""Draw the public figures. Written by PI/claude-opus-4.6 and PI/gpt-5.4."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import textwrap

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


def suppressed_overlay(
    ax: plt.Axes,
    probability_rows: list[dict[str, str]],
    subspace_rows: list[dict[str, str]],
    selection: str,
    title: str,
    shares: tuple[str, str],
) -> None:
    for language in ("en", "zh"):
        lang_rows = [row for row in probability_rows if row["language"] == language]
        layer = np.array([int(row["layer"]) for row in lang_rows])
        probability = np.array([float(row["mean_probability"]) for row in lang_rows])
        ax.plot(layer, probability, color=COLORS[language], lw=2.1, zorder=3)

        if language == "en":
            share_by_layer = {
                int(row["layer"]): float(row["share"])
                for row in subspace_rows
                if row["selection"] == selection and row["language"] == language
            }
            shown = layer > 0
            inside = probability[shown] * np.array([share_by_layer[l] for l in layer[shown]])
            ax.fill_between(layer[shown], 0, inside, where=inside >= 0, interpolate=True,
                            color=ENGLISH, alpha=0.52, lw=0, zorder=1)
            ax.fill_between(layer[shown], 0, inside, where=inside < 0, interpolate=True,
                            color=ENGLISH, alpha=0.18, hatch="////", lw=0, zorder=1)

    ax.axhline(0, color="0.78", lw=0.7, zorder=0)
    ax.axvline(27, color="0.78", lw=0.7, ls=":", zorder=0)
    ax.axvline(32, color="0.78", lw=0.7, ls=":", zorder=0)
    ax.text(26.5, 0.40, shares[0], color=ENGLISH, fontsize=8, ha="right")
    ax.text(31.7, 0.62, shares[1], color=CHINESE, fontsize=8, ha="right")
    ax.set(xlim=(0, 32), ylim=(-0.015, 0.67), xlabel="layer index")
    ax.set_title(title, loc="left", fontsize=10.5)
    if selection == "same prompt":
        ax.legend(
            handles=[Line2D([], [], color="0.25", lw=1.7,
                            label="same probability curve as a"),
                     Patch(facecolor=ENGLISH, alpha=0.45,
                           label="English probability × readout share")],
            loc="upper left", frameon=False, fontsize=7.5, handlelength=1.5,
        )


def causal_demo(data: dict) -> plt.Figure:
    rows = {row["condition"]: row["metrics"] for row in data["interventions"]}
    random_rows = [
        row["metrics"]
        for row in data["interventions"]
        if row["condition"].startswith("random_seed=")
    ]
    metadata = data["metadata"]

    fig, axes = plt.subplots(
        1,
        4,
        figsize=(14.8, 4.25),
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1.75, 1, 1, 1.25]},
    )

    ax = axes[0]
    ax.axis("off")
    translated_labels = {"สุนัข": "Thai: dog"}
    source_tokens = [repr(row["token"].strip()) for row in data["source_selected_tokens"]]
    target_tokens = [
        repr(translated_labels.get(row["token"].strip(), row["token"].strip()))
        for row in data["target_selected_tokens"]
    ]
    source_words = ", ".join(source_tokens[:4]) + "\n  " + ", ".join(source_tokens[4:])
    target_words = ", ".join(target_tokens[:4]) + "\n  " + ", ".join(target_tokens[4:])
    source_prompt = textwrap.fill(metadata["source_prompt"].strip(), width=47)
    target_prompt = textwrap.fill(metadata["target_prompt"].strip(), width=47)
    ax.set_title("a   Per-prompt component replacement", loc="left", fontsize=10.5)
    ax.text(
        0,
        0.94,
        f"Source prompt\n  {source_prompt}\n"
        f"Selected rank 8, no hidden-word label\n  {source_words}\n\n"
        f"Target prompt\n  {target_prompt}\n"
        f"Selected rank 8, no hidden-word label\n  {target_words}",
        va="top",
        fontsize=8.25,
        linespacing=1.27,
        transform=ax.transAxes,
    )
    ax.text(
        0,
        0.19,
        r"$h' = \operatorname{norm}\!\left[h + 2\left("
        r"\operatorname{match}(P_{dog}h_{dog}) - P_{spider}h\right)\right]$",
        fontsize=8.2,
        transform=ax.transAxes,
    )
    ax.text(
        0,
        0.07,
        "Expected next token:  8  →  4\n"
        "Last prompt position, residual L23–L30",
        fontsize=8.5,
        transform=ax.transAxes,
    )

    for ax, condition, title, color in (
        (axes[1], "base", "b   Clean next token: 8", ENGLISH),
        (axes[2], "replace", "c   Replaced next token: 4", CHINESE),
    ):
        top = rows[condition]["top"]
        labels = [row["token"].replace(" ", "␠", 1) if row["token"].startswith(" ") else row["token"] for row in top]
        probabilities = np.exp([row["logp"] for row in top])
        y = np.arange(len(top))[::-1]
        ax.barh(y, probabilities, color=color, alpha=0.82, height=0.66)
        ax.set_yticks(y, labels)
        ax.set_xlim(0, 1.0)
        ax.set_xlabel("next-token probability")
        ax.set_title(title, loc="left", fontsize=10.5)
        for yi, probability in zip(y, probabilities):
            ax.text(probability + 0.012, yi, f"{probability:.2f}", va="center", fontsize=7.5)

    ax = axes[3]
    random_odds = np.array([row["log_odds_target_vs_source"] for row in random_rows])
    rng = np.random.default_rng(0)
    ax.scatter(random_odds, 1 + rng.uniform(-0.13, 0.13, len(random_odds)), s=13, color="0.55", alpha=0.75)
    points = [
        (rows["base"]["log_odds_target_vs_source"], 0, "clean", ENGLISH),
        (rows["remove"]["log_odds_target_vs_source"], 2, "remove spider", "0.35"),
        (rows["replace"]["log_odds_target_vs_source"], 3, "spider → dog", CHINESE),
    ]
    for x, y, label, color in points:
        ax.scatter([x], [y], s=35, color=color, zorder=3)
        ax.text(x, y + 0.20, f"{x:+.2f}", ha="center", color=color, fontsize=7.5)
    ax.axvline(0, color="0.65", lw=0.8, ls=":")
    ax.set_yticks(
        [0, 1, 2, 3],
        ["clean", f"{len(random_rows)} matched random", "remove spider", "spider → dog"],
    )
    all_odds = np.append(random_odds, [point[0] for point in points])
    ax.set_xlim(all_odds.min() - 0.5, all_odds.max() + 0.5)
    ax.set_ylim(-0.45, 3.45)
    ax.set_xlabel("log p(4) − log p(8)")
    smaller = int(np.sum(random_odds < rows["replace"]["log_odds_target_vs_source"]))
    ax.set_title(f"d   {smaller}/{len(random_rows)} random effects are smaller", loc="left", fontsize=10.5)

    for ax in axes[1:]:
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8)
    fig.suptitle(
        f"Qwen3.5-4B, rank {metadata['rank']} suppressed subspaces; residual norm restored",
        fontsize=10,
        color="0.25",
    )
    return fig


def canonicalize_svg_clip_ids(path: Path) -> None:
    svg = path.read_text()
    replacements: dict[str, str] = {}

    def replace_id(match: re.Match[str]) -> str:
        old_id = match.group(0)
        if old_id not in replacements:
            replacements[old_id] = f"p{len(replacements):010d}"
        return replacements[old_id]

    path.write_text(re.sub(r"\bp[0-9a-f]{10}\b", replace_id, svg))


def main() -> None:
    plt.rcParams["svg.hashsalt"] = "suppressed-activations"
    curves = read_rows(ROOT / "data/qwen_logit_lens_de_zh.csv")
    subspaces = read_rows(ROOT / "data/suppressed_subspace_by_layer.csv")

    fig, axes = plt.subplots(
        1, 3, figsize=(13.4, 4.15), constrained_layout=True, sharey=True,
        gridspec_kw={"width_ratios": [1.16, 1, 1]},
    )
    language_probability(axes[0], curves)
    suppressed_overlay(
        axes[1], curves, subspaces, "same prompt",
        "b   Own-prompt subspace\ndesired: English filled; Chinese share low",
        ("L27 English: 95% inside", "L32 Chinese: 20% inside"),
    )
    suppressed_overlay(
        axes[2], curves, subspaces, "different prompt",
        "c   Different-prompt control\ndesired: English unfilled",
        ("L27 English: 4% inside", "L32 Chinese: −1% inside"),
    )
    axes[1].tick_params(labelleft=False)
    axes[2].tick_params(labelleft=False)

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8.5)

    assert_no_clip(fig)
    out = ROOT / "figs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "suppressed_activations.png", dpi=220, facecolor="white")
    svg_path = out / "suppressed_activations.svg"
    fig.savefig(svg_path, facecolor="white", metadata={"Date": None})
    canonicalize_svg_clip_ids(svg_path)
    plt.close(fig)

    demo = json.loads((ROOT / "data/causal_demo.json").read_text())
    with plt.rc_context({"font.family": "Noto Sans CJK SC"}):
        fig = causal_demo(demo)
    assert_no_clip(fig)
    fig.savefig(out / "causal_demo.png", dpi=220, facecolor="white")
    svg_path = out / "causal_demo.svg"
    fig.savefig(svg_path, facecolor="white", metadata={"Date": None})
    canonicalize_svg_clip_ids(svg_path)
    plt.close(fig)


if __name__ == "__main__":
    main()
