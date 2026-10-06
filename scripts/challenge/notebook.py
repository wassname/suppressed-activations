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
import time

import matplotlib
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tabulate import tabulate

from bench import (TEST, by_spelling, calibration_texts, chinese, judge, prepare, read_vector, script, spelled,
                   top_words, translation_prompts)
from common import DEVICE, ROOT, forward, readout, rms, tok, vocab
from transforms import FIRST, calibrate, jlens, project
import demo

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
SPIDER_AR = "\n".join(demo.READ)  # the README demo prompt (demo.py writes the README table)
# Fig. 12's third example (antonym of small), asked in Arabic, answered in Russian: the 1st of 2 wordings tried.
ANTONYM_AR = 'العربية: "ما عكس كلمة \"حار\"؟" - Русский: "холодный"\nالعربية: "ما عكس كلمة \"صغير\"؟" - Русский: "'

ar_ru = list(translation_prompts([("ar", "ru")], "test"))
examples = [(SPIDER_AR, "spider", "8"), (ANTONYM_AR, "big", "большой"),
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
print("\n".join(report))
(out / "readouts.md").write_text("\n".join(report))

# %% [markdown]
# ## Part 2: how much of the unspoken word does each method find, per layer?
#
# Areas: the logit-lens probability of the input-language words, the unspoken word and the output-language words,
# averaged over the test prompts (real data for the README cartoon). Lines: for "minus ends" (solid) and the plain logit
# lens (dashed), the share of prompts where the top 8 words hold the unspoken word and nothing leaked (green), and where
# they hold input- or output-language words (red).

# %%
leak_script = {lang: torch.tensor(sorted(script[lang])).to(DEVICE) for lang in script}
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

torch.save(mean_truth, out / "truth_curves.pt")
GREY, ORANGE, BLUE, GREEN, RED = "#7f7f7f", "#d55e00", "#0072b2", "#1a9850", "#d73027"
fig, ax = plt.subplots(figsize=(8, 4.4), constrained_layout=True)
# input-language words are near 0 at the last prompt token at every layer, so READ is left out (said in the caption)
for k, color, label, xy, ha in (("unspoken", ORANGE, "THINK: unspoken word", (26.6, 0.09), "center"),
                                ("output", BLUE, "SAY: output language", (31.2, 0.60), "left")):
    y = mean_truth[k]
    ax.fill_between(LAYERS, y, color=color, alpha=0.15, lw=0)
    ax.plot(LAYERS, y, color=color, lw=1.5)
    ax.text(*xy, label, color=color, ha=ha, va="center", fontsize=9)  # placed clear of the lines
for name, ls in (("minus ends", "-"), ("logit lens", "--")):
    by_layer = {l: [r for r in rows if r["method"] == name and r["layer"] == l] for l in LAYERS}
    ls_ = [l for l in LAYERS if by_layer[l]]
    clean = [sum(r["hidden"] and not r["leaked"] for r in by_layer[l]) / len(by_layer[l]) for l in ls_]
    leak = [sum(r["leaked"] for r in by_layer[l]) / len(by_layer[l]) for l in ls_]
    lw = 2.5 if ls == "-" else 1.2
    ax.plot(ls_, clean, color=GREEN, ls=ls, lw=lw)
    ax.plot(ls_, leak, color=RED, ls=ls, lw=lw)
    ax.text(ls_[-1] + 0.2, clean[-1], f"{name}: found, clean", color=GREEN, fontsize=8, va="center")
    ax.text(ls_[-1] + 0.2, leak[-1], f"{name}: shows input/output words", color=RED, fontsize=8, va="center")
ax.set(xlim=(LAYERS[0], LAYERS[-1] + 6), ylim=(0, 1.05), xticks=[16, 20, 24, 28, 31], xlabel="layer",
       ylabel="areas: logit-lens probability\nlines: share of prompts")
ax.margins(x=0)
ax.spines[["top", "right"]].set_visible(False)
ax.set_title(f"Where the unspoken word is, and how often a method gets it cleanly ({len(truth['unspoken'])} test prompts)",
             fontsize=10, loc="left")
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
