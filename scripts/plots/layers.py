"""Stack language-role curves and overlay prompt detection rates. No model needed. — PI/OpenAI"""
import argparse
import gzip
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import torch

ROOT = Path(__file__).resolve().parents[2]
METHOD = "random subspace"


def plot_layers(rows, truth, destination):
    layers = list(range(16, 32))
    groups = [[r for r in rows if r["method"] == METHOD and r["layer"] == l] for l in layers]
    assert all(len(g) == len(groups[0]) > 0 for g in groups)
    rates = {k: torch.tensor([sum(r[k] for r in g) / len(g) for g in groups])
             for k in ("hidden", "leaked_in", "leaked_out", "leaked")}
    colors = {"input": "#888888", "unspoken": "#d89535", "output": "#4489be"}
    green, red = "#087b3c", "#b32332"
    fig, (header, ax) = plt.subplots(2, 1, figsize=(10, 5.8), layout="constrained",
                                    gridspec_kw={"height_ratios": [1, 5]})
    header.axis("off")
    header.text(0, 0.97, f"Random subspace: found, missed and leaked ({len(groups[0])} prompts)",
                fontsize=13, va="top", transform=header.transAxes)
    base, bands = torch.zeros(len(layers)), {}
    for key, rate, hatch_color in (("input", "leaked_in", red), ("unspoken", "hidden", green),
                                    ("output", "leaked_out", red)):
        mass = truth[key]
        selected = base + mass * rates[rate]
        top = base + mass
        ax.fill_between(layers, base, top, facecolor=colors[key], alpha=0.27, linewidth=0)
        ax.fill_between(layers, base, selected, facecolor="none", edgecolor=hatch_color,
                        hatch="//" if key == "unspoken" else "\\\\", linewidth=0)
        ax.plot(layers, selected, color=hatch_color, linewidth=1.0)
        ax.plot(layers, top, color=colors[key], linewidth=1.5)
        bands[key] = (base, selected, top)
        base = top
    language_legend = header.legend(
        [Patch(facecolor=c, alpha=0.4) for c in colors.values()],
        ["Input language · exclude", "Unspoken word · find", "Output language · exclude"],
        loc="upper left", bbox_to_anchor=(0, 0.69), ncol=3, frameon=False, fontsize=10,
        borderaxespad=0)
    header.add_artist(language_legend)
    selection_legend = header.legend([Patch(facecolor="none", edgecolor=green, hatch="//"),
               Patch(facecolor="none", edgecolor=red, hatch="\\\\"),
               Patch(facecolor="white", edgecolor="#aaaaaa")],
              ["Found (TP)", "Leaked (FP)", "No hatching: missed (FN) / excluded (TN)"],
              loc="upper left", bbox_to_anchor=(0, 0.30), ncol=3, frameon=False, fontsize=10,
              borderaxespad=0)

    def annotate(text, xy, position):
        ax.annotate(text, xy=xy, xytext=position, fontsize=10, color="#222222",
                    va="center", ha="left",
                    arrowprops={"arrowstyle": "->", "color": "#333333", "linewidth": 1,
                                "connectionstyle": "arc3,rad=0"})

    i = layers.index(24)
    lo, selected, hi = bands["unspoken"]
    annotate(f"FN {1 - rates['hidden'][i]:.0%} · missed\nlayer 24",
             (24, float((selected[i] + hi[i]) / 2)), (20.3, 0.43))
    annotate(f"TP {rates['hidden'][i]:.0%} · found\nlayer 24",
             (24, float((lo[i] + selected[i]) / 2)), (20.3, 0.27))
    i = layers.index(31)
    lo, selected, hi = bands["output"]
    annotate(f"TN {1 - rates['leaked_out'][i]:.0%}\noutput excluded\nlayer 31",
             (31, float((selected[i] + hi[i]) / 2)), (31.8, 0.78))
    annotate(f"FP {rates['leaked_out'][i]:.0%}\noutput leaked\nlayer 31",
             (31, float((lo[i] + selected[i]) / 2)), (31.8, 0.39))
    ax.set(xlim=(16, 35), ylim=(0, 0.9), xticks=[16, 20, 24, 28, 31],
           xlabel="Layer", ylabel="Summed mean logit-lens probability")
    ax.spines[["top", "right"]].set_visible(False)
    fig.canvas.draw()
    for legend in (language_legend, selection_legend):
        assert fig.bbox.contains(*legend.get_window_extent().p0)
        assert fig.bbox.contains(*legend.get_window_extent().p1)
    bounds = fig.get_tightbbox(fig.canvas.get_renderer())
    width, height = fig.get_size_inches()
    assert bounds.x0 >= 0 and bounds.y0 >= 0 and bounds.x1 <= width and bounds.y1 <= height
    fig.savefig(destination, dpi=160)
    plt.close(fig)
    return {l: {k: float(v[l - 16]) for k, v in rates.items()} for l in (24, 28, 31)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, nargs="?", default=ROOT / "results/layer_plot.json.gz")
    parser.add_argument("--output", type=Path, default=ROOT / "figs/layers.png")
    args = parser.parse_args()
    with gzip.open(args.evidence, "rt") as f:
        evidence = json.load(f)
    rows = evidence["rows"]
    truth = {k: torch.tensor(v) for k, v in evidence["truth_curves"].items()}
    print(json.dumps(plot_layers(rows, truth, args.output), indent=2))
