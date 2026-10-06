# %% [markdown]
# # Explore: what the hidden words look like, and how each method does per layer
#
# Part 1 prints the top 8 words at each layer for a few prompts. Part 2 scores geometry methods at every layer on the
# leaderboard's test prompts and draws figs/layers.png. Add your own method to `METHODS`: a function
# `(s, layer) -> activation vector`, same rules as `@geometry`.
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

from bench import TEST, f1, judge, prepare, read_vector, top_words, transfer_prompts, translation_prompts
from common import ROOT, forward, readout, rms, tok, vocab
from transforms import CHURN_LAYERS, bases, fit_bases, jlens, project

fit_bases()
LAYERS = list(CHURN_LAYERS)  # 16..31


def minus_early_and_output(s, l):  # the leaderboard winner, at any layer after 22
    if l <= 22:
        return None
    N = torch.linalg.qr(torch.stack([rms(s["res"][22]), rms(s["res"][32])], 1)).Q
    x = rms(s["res"][l])
    return x - N @ (N.T @ x)


METHODS = {  # name -> fn(s, layer) -> vector, or None if the layer does not apply
    "logit lens (activations unchanged)": lambda s, l: s["res"][l],
    "random subspace, rank 1024": lambda s, l: project(bases["random"][:, :1024], s["res"][l]),
    "layer-change PCA, rank 1024": lambda s, l: project(bases[f"churn{l}"][:, :1024], s["res"][l]),
    "net-change PCA, rank 1024": lambda s, l: project(bases["net change"][:, :1024], s["res"][l]),
    "remove this prompt's early and output states": minus_early_and_output,
}

# %% [markdown]
# ## Part 1: what do the hidden words look like?
#
# The top 8 words at the last prompt token, read three ways: the logit lens (activations unchanged), the J-lens
# (Gurnee et al. 2026, a reference readout that uses the model's Jacobian, not an entry), and the best geometry entry.
# The middle layers often show words the model uses on the way to its answer but never says.

# %%
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_notebook"
out.mkdir(parents=True)
words = lambda scores: " ".join(vocab[t].strip() for t in top_words(scores))
examples = [("Fact: The number of legs on the animal that spins webs is ", "spider", "8")]
examples += [(it["prompt"], it["word"], "") for it in list(transfer_prompts())[:3]]
examples += [(it["prompt"], it["word"], "") for it in list(translation_prompts(TEST, "test"))[::60][:2]]
report = []
for prompt, hidden, _ in examples:
    res, _, logits = forward(prompt)
    x = res[:, -1]
    table = [[l, words(readout(x[l])), words(readout(jlens(x[l], l))),
              words(read_vector(METHODS["remove this prompt's early and output states"]({"res": x}, l), "")) if l > 22 else ""]
             for l in (20, 22, 24, 26, 28, 30, 31)]
    head = f"**prompt** (last line): `{prompt.splitlines()[-1]!r}`; expected hidden word: `{hidden}`; model says: `{vocab[int(logits.argmax())]!r}`"
    report += [head, "", tabulate(table, ["layer", "logit lens", "J-lens", "remove early and output states"], "pipe"), ""]
print("\n".join(report))
(out / "readouts.md").write_text("\n".join(report))

# %% [markdown]
# ## Part 2: every method at every layer

# %%
rows = []
for item in translation_prompts(TEST, "test"):
    prepared = prepare(item)
    if prepared is None:
        continue
    state, leak = prepared
    s = {"res": state["res"], "attn": state["attn"]}  # geometry gets no logits or token ids
    for name, fn in METHODS.items():
        for l in LAYERS:
            v = fn(s, l)
            if v is not None:
                rows.append({"method": name, "layer": l, "split": item["split"], "word": item["word"]}
                            | judge(read_vector(v, name), item, leak))
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump(rows, f, ensure_ascii=False)
print(out)

# %%
OUTCOMES = [  # each prompt is exactly one of these; the shares stack to 1
    ("hidden word, nothing leaked (the goal)", lambda r: r["hidden"] and not r["leaked"], "#d55e00", None),
    ("hidden word, but input/output words too", lambda r: r["hidden"] and r["leaked"], "#f4b183", None),
    ("only input/output words", lambda r: not r["hidden"] and r["leaked"], "#9ecae1", None),
    ("neither", lambda r: not r["hidden"] and not r["leaked"], "#eeeeee", None),
]
names = list(METHODS)
fig, axes = plt.subplots(1, len(names), figsize=(3 * len(names), 3.6), sharey=True)
for ax, name in zip(axes, names):
    by_layer = {l: [r for r in rows if r["method"] == name and r["layer"] == l] for l in LAYERS}
    ls = [l for l in LAYERS if by_layer[l]]
    shares = [[sum(map(test, by_layer[l])) / len(by_layer[l]) for l in ls] for _, test, _, _ in OUTCOMES]
    ax.stackplot(ls, shares, colors=[c for *_, c, _ in OUTCOMES], lw=0)
    if ls[0] > LAYERS[0]:
        ax.text((LAYERS[0] + ls[0]) / 2, 0.5, f"starts at\nlayer {ls[0]}\n(it removes\nlayer {ls[0] - 1})", ha="center", va="center", fontsize=9,
                color="#777777")
    best = max(ls, key=lambda l: f1(by_layer[l]))
    ax.set_title(f"{textwrap.fill(name, 30)}\nbest F1 {f1(by_layer[best]):.2f} at layer {best}", fontsize=9, loc="left")
    ax.set(xlim=(LAYERS[0], LAYERS[-1]), ylim=(0, 1), xticks=[16, 20, 24, 28, 31], xlabel="layer")
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("share of prompts")
fig.legend([plt.Rectangle((0, 0), 1, 1, color=c) for *_, c, _ in OUTCOMES], [o[0] for o in OUTCOMES],
           loc="lower center", ncol=4, frameon=False, fontsize=9)
n = len({(r["split"], r["word"]) for r in rows})
fig.suptitle(f"What each method's top 8 words show, per layer (Qwen3.5-4B, {n} test prompts)", fontsize=11, x=0.01,
             ha="left")
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(ROOT / "figs/layers.png", dpi=150)


# %% [markdown]
# ## Part 3: translation layer by layer, as in Wendler et al. (2024), Fig. 2
#
# Probability of the unspoken word (English or Chinese), the output-language word and the input word, at the last
# prompt token, for every layer. Mean over the test prompts, with a 95% band. Writes figs/translation_by_layer.png.

# %%
words_json = json.loads((ROOT / "data/challenge/words.json").read_text())
first_token = lambda w: tok(w, add_special_tokens=False).input_ids[0]
curves = {"lens": {k: [] for k in ("unspoken", "output", "input")}, "J-lens": {k: [] for k in ("unspoken", "output", "input")}}
for item in translation_prompts(TEST, "test"):
    src, tgt = item["split"].split("→")
    x = forward(item["prompt"])[0][:, -1]                                               # [33, d]
    ids = {"unspoken": sorted(item["right"]), "output": [first_token(words_json[item["word"]][tgt])],
           "input": [first_token(words_json[item["word"]][src])]}
    for lens, read in (("lens", lambda l: readout(x[l])), ("J-lens", lambda l: readout(jlens(x[l], l) if 0 < l < 32 else x[l]))):
        p = torch.stack([torch.softmax(read(l), -1) for l in range(33)])                # [33, vocab]
        for k, v in ids.items():
            curves[lens][k].append(p[:, v].sum(-1).cpu())

style = {"unspoken": ("#d55e00", "unspoken word (English or Chinese)"), "output": ("#0072b2", "output-language word"),
         "input": ("#7f7f7f", "input word")}
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
for ax, (lens, title) in zip(axes, (("lens", "logit lens"), ("J-lens", "J-lens"))):
    for k, (color, label) in style.items():
        y = torch.stack(curves[lens][k])                                                 # [prompts, 33]
        m, se = y.mean(0), y.std(0) / len(y) ** 0.5
        ax.fill_between(range(33), m - 1.96 * se, m + 1.96 * se, color=color, alpha=0.2, lw=0)
        ax.plot(range(33), m, color=color, lw=2, label=label)
    ax.set_title(title, fontsize=10, loc="left")
    ax.set(xlabel="layer", xlim=(0, 32), ylim=(0, 1))
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("probability")
axes[0].legend(frameon=False, fontsize=9, loc="upper left")
fig.suptitle(f"Qwen3.5-4B translating between non-English languages ({len(y)} test prompts)", fontsize=11, x=0.01,
             ha="left")
fig.tight_layout()
fig.savefig(ROOT / "figs/translation_by_layer.png", dpi=150)
