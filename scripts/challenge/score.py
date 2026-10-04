"""Score every transform and write the leaderboard. One GPU, about 7 minutes.

Translation between languages that share no script with English or Chinese. The model thinks in English (and Qwen
perhaps Chinese); it reads one language and writes another. For each prompt we keep a transform's top 8 distinct words
(case and space variants share a slot) at the last prompt token:

    TP = the hidden word (English, or its Chinese translation) is in the top 8, else FN
    FP = a top-8 word is in the input or output language (script), or is the model's next word, else TN
    F1 = 2TP / (2TP + FP + FN), with counts over prompts

Each transform's setting is chosen on the dev pair by F1, then frozen for the test pairs and for transfer:
English-only two-hop questions (TwoHopFact), where the hidden word is the bridge entity.
Usage: uv run scripts/challenge/make_word_lists.py (once), then uv run scripts/challenge/score.py — PI/OpenAI
"""
import ast
import csv
import gzip
import inspect
import json
import random
import re
import subprocess
import time
from statistics import mean

from tabulate import tabulate
import torch

from common import LANG_NAME, ROOT, SCRIPT, TWOHOP, WENDLER_ZH, forward, tok, tokens_in_script, vocab
from transforms import TRANSFORMS, fit_bases

K, PER_PAIR, N_TRANSFER = 8, 60, 150  # per pair capped by the word list
DEV, TEST = [("ru", "ko")], [("ar", "hi"), ("hi", "th"), ("th", "ru"), ("ko", "ar")]
script = {lang: tokens_in_script(pattern) for lang, pattern in SCRIPT.items()}
fit_bases()
special = frozenset(tok.all_special_ids) | {t for t, v in enumerate(vocab) if not v}
by_spelling = {}
for t, v in enumerate(vocab):
    by_spelling.setdefault(v.strip().lower(), []).append(t)


def spelled(phrase):
    """Tokens that are exactly one word (3+ letters) of the phrase, ignoring case and spaces."""
    return frozenset(t for w in re.findall(r"\w{3,}", phrase.lower()) for t in by_spelling.get(w, []))


def top_words(scores):
    """Top K distinct strings (case and space variants share a slot), special tokens excluded."""
    kept, seen = [], set()
    for t in scores.topk(4096).indices.tolist():
        key = vocab[t].strip().lower()
        if t not in special and key not in seen:
            seen.add(key)
            kept.append(t)
            if len(kept) == K:
                return kept
    raise AssertionError("fewer than K distinct words in the top 4096")


chinese = {r["word_original"]: r["word_translation"] for r in csv.DictReader(open(WENDLER_ZH()))}


def translation_prompts(pairs, role):
    words = json.loads((ROOT / "data/challenge/words.json").read_text())
    for src, tgt in pairs:
        pool = sorted(w for w, forms in words.items() if src in forms and tgt in forms)
        random.Random(0).shuffle(pool)
        line = lambda w: f'{LANG_NAME[src]}: "{words[w][src]}" - {LANG_NAME[tgt]}: "'
        shots = "".join(line(w) + f'{words[w][tgt]}"\n' for w in pool[:4])
        for w in pool[4:4 + PER_PAIR]:
            before_input = shots + f'{LANG_NAME[src]}: "{words[w][src]}'
            n = len(tok(before_input, add_special_tokens=False).input_ids)
            assert tok(shots + line(w), add_special_tokens=False).input_ids[:n] == tok(before_input, add_special_tokens=False).input_ids
            yield {"role": role, "split": f"{src}→{tgt}", "word": w, "prompt": shots + line(w),
                   "input_pos": n - 1,  # last token of the input word
                   "leak": script[src] | script[tgt], "right": spelled(w) | frozenset(by_spelling.get(chinese[w], []))}


def transfer_prompts():
    rows = list(csv.DictReader(open(TWOHOP())))
    random.Random(0).shuffle(rows)
    aliases = lambda r, e: [a for group in ast.literal_eval(r[f"{e}.aliases"]) for a in group] or [r[f"{e}.value"]]
    seen = set()
    for r in rows:
        prompt = r["r2(r1(e1)).prompt"]
        prompt_words = {w.lower() for w in re.findall(r"\w+", prompt)}
        right = frozenset().union(*[spelled(a) for a in aliases(r, "e2")])
        leak = frozenset().union(*[spelled(a) for a in aliases(r, "e3")]) | spelled(prompt)
        if prompt in seen or not right - leak:
            continue
        seen.add(prompt)
        yield {"role": "transfer", "split": "TwoHopFact", "word": r["e2.value"], "prompt": prompt, "leak": leak,
               "right": right - leak, "input_pos": -1}
        if len(seen) == N_TRANSFER:
            return


def evaluate(item, settings_of):
    """Score one prompt for every transform under the given settings; returns rows, or None if the prompt is skipped."""
    res, attn, logits = forward(item["prompt"])
    nxt = int(logits.argmax())
    if not re.search(r"\w", vocab[nxt]):  # the model is about to write whitespace or punctuation: bad prompt format
        skipped.append({k: item[k] for k in ("split", "word")} | {"next": vocab[nxt]})
        return []
    leak = item["leak"] | {nxt}
    enc = tok(item["prompt"], add_special_tokens=False, return_offsets_mapping=True)
    ids = torch.tensor(enc.input_ids).cuda()
    line_start = item["prompt"].rfind("\n") + 1
    line = [i for i, (_, end) in enumerate(enc.offset_mapping) if end > line_start]  # tokens of the prompt's last line
    state = {"res": res[:, -1], "attn": attn[-1], "logits": logits, "ids": ids, "line": res[:, line],
             "input": res[:, item["input_pos"]]}
    out = []
    for name, (_, _, fn) in TRANSFORMS.items():
        for setting in settings_of(name):
            top = top_words(fn(state, *setting))
            leaked = bool(set(top) & leak)
            hidden = any(t in item["right"] for t in top)
            out.append({"role": item["role"], "split": item["split"], "word": item["word"], "transform": name,
                        "setting": list(setting), "top8": [vocab[t] for t in top], "hidden": hidden, "leaked": leaked})
    return out


skipped = []
dev_rows = [r for item in translation_prompts(DEV, "dev") for r in evaluate(item, lambda name: TRANSFORMS[name][0])]
assert dev_rows, "no dev prompts survived"
def f1(rs):
    tp, fp = sum(r["hidden"] for r in rs), sum(r["leaked"] for r in rs)
    return 2 * tp / (2 * tp + fp + len(rs) - tp)


def delta_ci(rs, base, n_boot=2000):
    """F1(rs) - F1(base) on the same prompts, with a 90% paired bootstrap interval."""
    by_key = {(r["split"], r["word"]): r for r in base}
    pairs = [(r, by_key[(r["split"], r["word"])]) for r in rs]
    assert len(pairs) == len(base)
    rng = random.Random(0)
    boots = sorted(f1(a) - f1(b) for a, b in (zip(*[rng.choice(pairs) for _ in pairs]) for _ in range(n_boot)))
    return f"{f1(rs) - f1(base):+.2f} ({boots[int(0.05 * n_boot)]:+.2f} to {boots[int(0.95 * n_boot)]:+.2f})"


def f1_ci(rs, n_boot=2000):
    """90% bootstrap interval over prompts."""
    rng = random.Random(0)
    boots = sorted(f1([rng.choice(rs) for _ in rs]) for _ in range(n_boot))
    return f"{boots[int(0.05 * n_boot)]:.2f}–{boots[int(0.95 * n_boot)]:.2f}"


chosen = {name: max(settings, key=lambda s: f1([r for r in dev_rows if r["transform"] == name and r["setting"] == list(s)]))
          for name, (settings, _, _) in TRANSFORMS.items()}
rows = dev_rows + [r for item in [*translation_prompts(TEST, "test"), *transfer_prompts()]
                   for r in evaluate(item, lambda name: [chosen[name]])]
for role in ("test", "transfer"):
    assert any(r["role"] == role for r in rows), f"no {role} prompts survived"

# ---- leaderboard ----
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_leaderboard"
out.mkdir(parents=True)
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump({"rows": rows, "skipped": skipped, "chosen": chosen}, f, ensure_ascii=False)
source_lines = inspect.getsource(__import__("transforms")).splitlines()
CONTROLS = ("logit lens", "random subspace (control)", "mean WikiText activation (control)", "input word (control)")
COLS = (("F1↑", max), ("TPR↑", max), ("FPR↓", min), ("English-only F1↑", max))
rows_by_table = {False: [], True: []}  # uses the J-lens?
random_test = [r for r in rows if r["transform"] == "random subspace (control)" and r["role"] == "test"
               and r["setting"] == list(chosen["random subspace (control)"])]
for name, (settings, fitted, _) in TRANSFORMS.items():
    mine = lambda role: [r for r in rows if r["transform"] == name and r["role"] == role and r["setting"] == list(chosen[name])]
    test, transfer = mine("test"), mine("transfer")
    line = next(i for i, text in enumerate(source_lines, 1) if f'@transform("{name}"' in text)
    label = f"[{name}](scripts/challenge/transforms.py#L{line})"
    rows_by_table["J-lens" in name].append({
        "transform": f"*{label}*" if name in CONTROLS else label, "F1↑": f1(test), "90% CI": f1_ci(test),
        "Δ vs random": "" if name == "random subspace (control)" else delta_ci(test, random_test), "TPR↑": mean(r["hidden"] for r in test),
        "FPR↓": mean(r["leaked"] for r in test), "English-only F1↑": f1(transfer),
        "fitted on": fitted, "setting": "/".join(map(str, chosen[name])), "tried": len(settings)})
n_test, n_transfer = len(test), len(transfer)


def render(table):
    table.sort(key=lambda r: -r["F1↑"])
    for col, better in COLS:
        best, tied = better(r[col] for r in table), len({r[col] for r in table}) == 1
        for r in table:
            r[col] = f"**{r[col]:.2f}**" if r[col] == best and not tied else f"{r[col]:.2f}"
    return tabulate(table, headers="keys", tablefmt="pipe", disable_numparse=True,
                    colalign=("left",) + ("right",) * 6 + ("left", "left", "right"))


commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
caption = (f"<sub>Table: Qwen3.5-4B. Test = {', '.join(f'{a}→{b}' for a, b in TEST)} ({n_test} prompts); setting = layer, or "
           f"layer/rank. Each row's settings (tried) are compared only on {DEV[0][0]}→{DEV[0][1]}, a pair not in the test, so trying more "
           f"settings does not see the test prompts. 90% CI = bootstrap over test prompts; Δ vs random = F1 minus the random subspace on the same prompts, with a paired 90% interval. TP, FN, FP, TN as in the README, counted over prompts; F1 = 2TP/(2TP+FP+FN). "
           f"English-only F1 = F1 on {n_transfer} English-only TwoHopFact questions, where the hidden word is the bridge entity and "
           f"input/output words are the question's words and its answer. fitted on = what the transform is fitted on besides the model weights (WikiText = 300 texts of generic text). "
           f"Italic = control. {len(skipped)} prompts skipped because the model's next token was whitespace or punctuation. "
           f"Commit {commit}, [rows]({out.relative_to(ROOT)}/rows.json.gz).</sub>")
markdown = (render(rows_by_table[False]) + "\n\n" + caption + "\n\n### Using the J-lens\n\n"
            + render(rows_by_table[True]) + "\n")
(out / "leaderboard.md").write_text(markdown)
print(markdown, f"\nskipped: {skipped}\n{out / 'leaderboard.md'}", flush=True)
