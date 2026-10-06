# %% [markdown]
# # Explore: unspoken concepts layer by layer
#
# Part 1 reads the top words at each layer for a few prompts, including Gurnee et al.'s Fig. 12 idea with the
# question in Arabic and the answer in Russian. Part 2 shows, per layer, how much of the unspoken word each method
# finds. Part 3 redraws Wendler et al.'s Fig. 2 for Arabic→Russian. Add your own per-layer method to `METHODS`.
# Opens as a notebook in VS Code/Jupyter (percent cells), or run it:
# `uv run --with matplotlib scripts/challenge/notebook.py`. — PI/OpenAI

# %%
import gzip
import json
import textwrap
import time

import matplotlib
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tabulate import tabulate

from bench import (TEST, by_spelling, calibration_texts, chinese, judge, prepare, read_vector, script, spelled,
                   top_words, translation_prompts)
from common import ROOT, forward, readout, rms, tok, vocab
from transforms import FIRST, calibrate, jlens, project

state = calibrate(calibration_texts())
LAYERS = list(range(16, 32))
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_notebook"
out.mkdir(parents=True)
(ROOT / "docs/leaderboard").mkdir(exist_ok=True)


def minus_ends(hs, l):  # layer l minus the span of this prompt's layer-16 and output states (the leaderboard's idea)
    if l == FIRST:
        return None
    N = torch.linalg.qr(torch.stack([rms(hs[0, -1]), rms(hs[-1, -1])], 1)).Q
    x = rms(hs[l - FIRST, -1])
    return x - N @ (N.T @ x)


METHODS = {  # per-layer methods: fn(hs, layer) -> vector, or None if the layer does not apply
    "logit lens": lambda hs, l: hs[l - FIRST, -1],
    "random subspace": lambda hs, l: project(state["random"][:, :1024], hs[l - FIRST, -1]),
    "layer-change PCA": lambda hs, l: project(state[f"churn{l}"][:, :1024], hs[l - FIRST, -1]),
    "net-change PCA": lambda hs, l: project(state["net change"][:, :1024], hs[l - FIRST, -1]),
    "minus ends": minus_ends,
}

# %% [markdown]
# ## Part 1: what do the unspoken words look like?
#
# Top 8 words at the last prompt token, with the logit lens and the J-lens (a reference readout, not an entry).

# %%
words = lambda scores: " ".join(vocab[t].strip() for t in top_words(scores))
EIFFEL = ("سؤال: ما هي عاصمة اليابان؟\nОтвет: Токио\nسؤال: ما هي عاصمة ألمانيا؟\nОтвет: Берлин\n"
          "سؤال: ما هي عاصمة البلد الذي يقع فيه برج إيفل؟\nОтвет:")  # capital of the Eiffel Tower's country? (Arabic)
ar_ru = list(translation_prompts([("ar", "ru")], "test"))
examples = [(EIFFEL, "France", "Париж"),
            ("Fact: The number of legs on the animal that spins webs is ", "spider", "8"),
            *[(it["prompt"], it["word"], "") for it in ar_ru if it["word"] == "cloud"]]
report = []
for prompt, hidden, answer in examples:
    res, _, logits = forward(prompt)
    x = res[:, -1]
    table = [[l, words(readout(x[l])), words(readout(jlens(x[l], l)))] for l in (20, 22, 23, 24, 26, 28, 30, 31)]
    head = (f"**prompt** (last line): `{prompt.splitlines()[-1]!r}`; unspoken word: `{hidden}`; expected answer: "
            f"`{answer}`; model says: `{vocab[int(logits.argmax())]!r}`")
    report += [head, "", tabulate(table, ["layer", "logit lens", "J-lens"], "pipe"), ""]
    if prompt == EIFFEL:  # the README demo: J-lens rows, verbatim
        demo = tabulate([[l, words(readout(jlens(x[l], l)))] for l in (20, 22, 24, 26, 28, 30)],
                        ["layer", "top 8 words (J-lens)"], "pipe", colalign=("right", "left"))
        (ROOT / "docs/leaderboard/demo_eiffel.md").write_text(demo + "\n")
print("\n".join(report))
(out / "readouts.md").write_text("\n".join(report))

# %% [markdown]
# ## Part 2: how much of the unspoken word does each method find, per layer?
#
# Lines: the logit-lens probability of the unspoken word, the output-language words and the input-language words,
# averaged over the test prompts. Filled share of the orange curve: the share of prompts where a method's top 8 words
# hold the unspoken word. Red fill under the blue and grey curves: the share where they hold output- or input-language
# words.

# %%
leak_script = {lang: torch.tensor(sorted(script[lang])).cuda() for lang in script}
rows, truth = [], {k: [] for k in ("unspoken", "output", "input")}
for item in translation_prompts(TEST, "test"):
    prepared = prepare(item)
    if prepared is None:
        continue
    s, leak_in, leak_out = prepared
    src, tgt = item["split"].split("→")
    p = torch.softmax(readout(s["hs"][:, -1]), -1)                                    # [17 layers, vocab]
    truth["unspoken"].append(p[:, sorted(item["right"])].sum(-1).cpu())
    truth["output"].append(p[:, leak_script[tgt]].sum(-1).cpu())
    truth["input"].append(p[:, leak_script[src]].sum(-1).cpu())
    for name, fn in METHODS.items():
        for l in LAYERS:
            v = fn(s["hs"], l)
            if v is not None:
                rows.append({"method": name, "layer": l} | judge(read_vector(v, name), item, leak_in, leak_out))
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump(rows, f, ensure_ascii=False)
mean_truth = {k: torch.stack(v).mean(0)[: len(LAYERS)] for k, v in truth.items()}   # layers 16..31

fig, axes = plt.subplots(1, len(METHODS), figsize=(3 * len(METHODS), 3.6), sharey=True)
colors = {"unspoken": "#d55e00", "output": "#0072b2", "input": "#7f7f7f"}
for ax, name in zip(axes, METHODS):
    by_layer = {l: [r for r in rows if r["method"] == name and r["layer"] == l] for l in LAYERS}
    ls = [l for l in LAYERS if by_layer[l]]
    rate = lambda key: torch.tensor([sum(r[key] for r in by_layer[l]) / len(by_layer[l]) for l in ls])
    idx = [l - LAYERS[0] for l in ls]
    ax.fill_between(ls, 0, mean_truth["unspoken"][idx] * rate("hidden"), color=colors["unspoken"], alpha=0.6, lw=0)
    ax.fill_between(ls, 0, mean_truth["output"][idx] * rate("leaked_out"), color="#d62728", alpha=0.5, lw=0)
    ax.fill_between(ls, 0, mean_truth["input"][idx] * rate("leaked_in"), color="#d62728", alpha=0.5, lw=0)
    for k, c in colors.items():
        ax.plot(LAYERS, mean_truth[k], color=c, lw=1.5)
    ax.set_title(textwrap.fill(name, 30), fontsize=9, loc="left")
    ax.set(xlim=(LAYERS[0], LAYERS[-1]), ylim=(0, 1), xticks=[16, 20, 24, 28, 31], xlabel="layer")
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("logit-lens probability")
handles = [plt.Line2D([], [], color=colors["unspoken"], lw=1.5), plt.Rectangle((0, 0), 1, 1, color=colors["unspoken"], alpha=0.6),
           plt.Line2D([], [], color=colors["output"], lw=1.5), plt.Line2D([], [], color=colors["input"], lw=1.5),
           plt.Rectangle((0, 0), 1, 1, color="#d62728", alpha=0.5)]
labels = ["unspoken word", "share the method finds", "output-language words", "input-language words",
          "share where the method shows them"]
fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False, fontsize=9)
fig.suptitle(f"How much of the unspoken word each method finds, per layer (Qwen3.5-4B, {len(truth['unspoken'])} test prompts)",
             fontsize=11, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(ROOT / "figs/layers.png", dpi=150)

# %% [markdown]
# ## Part 3: Arabic→Russian layer by layer, as in Wendler et al. (2024), Fig. 2
#
# Probability of the unspoken word (English or Chinese, also shown apart), the Russian word and the Arabic word, at
# the last prompt token. Mean over the Arabic→Russian test prompts, with a 95% band. Writes figs/translation_by_layer.png.

# %%
words_json = json.loads((ROOT / "data/challenge/words.json").read_text())
first_token = lambda w: tok(w, add_special_tokens=False).input_ids[0]
KINDS = ("unspoken", "English", "Chinese", "output", "input")
curves = {lens: {k: [] for k in KINDS} for lens in ("lens", "J-lens")}
for item in ar_ru:
    x = forward(item["prompt"])[0][:, -1]                                               # [33, d]
    ids = {"unspoken": sorted(item["right"]), "English": sorted(spelled(item["word"])),
           "Chinese": by_spelling.get(chinese[item["word"]], []), "output": [first_token(words_json[item["word"]]["ru"])],
           "input": [first_token(words_json[item["word"]]["ar"])]}
    for lens, read in (("lens", lambda l: readout(x[l])), ("J-lens", lambda l: readout(jlens(x[l], l) if 0 < l < 32 else x[l]))):
        p = torch.stack([torch.softmax(read(l), -1) for l in range(33)])                # [33, vocab]
        for k, v in ids.items():
            curves[lens][k].append(p[:, v].sum(-1).cpu())

style = {"unspoken": ("#d55e00", "-", 2, "unspoken word (English or Chinese)"),
         "English": ("#d55e00", "--", 1, "  English only"), "Chinese": ("#d55e00", ":", 1.2, "  Chinese only"),
         "output": ("#0072b2", "-", 2, "Russian word (output)"), "input": ("#7f7f7f", "-", 2, "Arabic word (input)")}
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
for ax, (lens, title) in zip(axes, (("lens", "logit lens"), ("J-lens", "J-lens"))):
    for k, (color, ls, lw, label) in style.items():
        y = torch.stack(curves[lens][k])                                                 # [prompts, 33]
        m, se = y.mean(0), y.std(0) / len(y) ** 0.5
        if lw == 2:  # bands only on the main lines
            ax.fill_between(range(33), m - 1.96 * se, m + 1.96 * se, color=color, alpha=0.2, lw=0)
        ax.plot(range(33), m, color=color, ls=ls, lw=lw, label=label)
    ax.set_title(title, fontsize=10, loc="left")
    ax.set(xlabel="layer", xlim=(0, 32), ylim=(0, 1))
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("probability")
axes[0].legend(frameon=False, fontsize=9, loc="upper left")
fig.suptitle(f"Qwen3.5-4B translating Arabic to Russian ({len(y)} test prompts)", fontsize=11, x=0.01, ha="left")
fig.tight_layout()
fig.savefig(ROOT / "figs/translation_by_layer.png", dpi=150)
