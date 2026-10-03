"""Score every transform and write the leaderboard. One GPU, a few minutes.

Translation between languages that share no script with English or Chinese. The model thinks in English (and Qwen
perhaps Chinese); it reads one language and writes another. For each prompt we keep a transform's top 8 distinct words
(case and space variants share a slot) at the last prompt token:

    share  = top-8 words written in English or Chinese / 8      (200 commonest WikiText tokens excluded)
    unsaid = share, or 0 if any top-8 word is in the input or output script, or is the model's next token
    found  = 1 if a top-8 word is exactly the English word (any word of an alias for transfer), else 0; 0 if leaked

Script membership is not relevance: the "fixed list" control row shows what a prompt-independent list scores.

Each transform's setting is chosen on the dev pair by unsaid, then frozen for the test pairs and for transfer:
English-only two-hop questions (TwoHopFact), where the hidden word is the bridge entity and scoring uses its spelling.
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

from common import LANG_NAME, ROOT, SCRIPT, forward, tok, tokens_in_script, vocab
from transforms import TRANSFORMS, fit_bases, token_counts

K, PER_PAIR, N_TRANSFER = 8, 20, 50
DEV, TEST = [("ru", "ko")], [("ar", "hi"), ("hi", "th"), ("th", "ru"), ("ko", "ar")]
script = {lang: tokens_in_script(pattern) for lang, pattern in SCRIPT.items()}
fit_bases()
common_tokens = frozenset(token_counts.topk(200).indices.tolist())
thought_script = tokens_in_script(r"A-Za-z\u4e00-\u9fff") - common_tokens - frozenset().union(*script.values())
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


def translation_prompts(pairs, role):
    words = json.loads((ROOT / "data/challenge/words.json").read_text())
    for src, tgt in pairs:
        pool = sorted(w for w, forms in words.items() if src in forms and tgt in forms)
        random.Random(0).shuffle(pool)
        line = lambda w: f'{LANG_NAME[src]}: "{words[w][src]}" - {LANG_NAME[tgt]}: "'
        shots = "".join(line(w) + f'{words[w][tgt]}"\n' for w in pool[:4])
        for w in pool[4:4 + PER_PAIR]:
            yield {"role": role, "split": f"{src}→{tgt}", "word": w, "prompt": shots + line(w),
                   "leak": script[src] | script[tgt], "right": spelled(w)}


def transfer_prompts():
    rows = list(csv.DictReader(open(ROOT / "data/twohop/TwoHopFact.csv")))
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
        yield {"role": "transfer", "split": "TwoHopFact", "word": r["e2.value"], "prompt": prompt, "leak": leak, "right": right - leak}
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
    state = {"res": res[:, -1], "attn": attn[-1], "logits": logits}
    out = []
    for name, (_, _, fn) in TRANSFORMS.items():
        for setting in settings_of(name):
            top = top_words(fn(state, *setting))
            leaked = bool(set(top) & leak)
            share = sum(t in thought_script for t in top) / K
            found = any(t in item["right"] for t in top)
            out.append({"role": item["role"], "split": item["split"], "word": item["word"], "transform": name,
                        "setting": list(setting), "top8": [vocab[t] for t in top], "leaked": leaked, "share": share,
                        "unsaid": 0.0 if leaked else share, "found": float(found and not leaked)})
    return out


skipped = []
dev_rows = [r for item in translation_prompts(DEV, "dev") for r in evaluate(item, lambda name: TRANSFORMS[name][0])]
assert dev_rows, "no dev prompts survived"
chosen = {name: max(settings, key=lambda s: mean(r["unsaid"] for r in dev_rows if r["transform"] == name and r["setting"] == list(s)))
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
CONTROLS = ("plain lens", "random subspace (floor)", "fixed list (control)")
table = []
for name, (settings, lens_based, _) in TRANSFORMS.items():
    mine = lambda role: [r for r in rows if r["transform"] == name and r["role"] == role and r["setting"] == list(chosen[name])]
    test, transfer = mine("test"), mine("transfer")
    line = next(i for i, text in enumerate(source_lines, 1) if f'@transform("{name}"' in text)
    label = f"[{name}](scripts/challenge/transforms.py#L{line})" + (" ★" if lens_based else "")
    table.append({"transform": f"*{label}*" if name in CONTROLS else label, "setting": "/".join(map(str, chosen[name])),
                  "unsaid↑": mean(r["unsaid"] for r in test), "share↑": mean(r["share"] for r in test),
                  "leaked↓": mean(r["leaked"] for r in test), "found↑": mean(r["found"] for r in test),
                  "transfer found↑": mean(r["found"] for r in transfer), "tried": len(settings)})
n_test, n_transfer = len(test), len(transfer)
table.sort(key=lambda r: -r["unsaid↑"])
for col, better in (("unsaid↑", max), ("share↑", max), ("leaked↓", min), ("found↑", max), ("transfer found↑", max)):
    best = better(r[col] for r in table)
    for r in table:
        r[col] = f"**{r[col]:.2f}**" if r[col] == best else f"{r[col]:.2f}"
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
caption = (f"<sub>Table: test = {', '.join(f'{a}→{b}' for a, b in TEST)} ({n_test} prompts); each setting chosen on "
           f"{DEV[0][0]}→{DEV[0][1]}. unsaid = share of the top {K} distinct words written in English or Chinese, 0 if any is in "
           f"the input or output script or is the model's next word. leaked = share of lists with such a word. found = share of "
           f"lists holding the exact English word without a leak. transfer found = the same on {n_transfer} English-only "
           f"TwoHopFact questions, for the hidden bridge entity. ★ = uses a lens or per-prompt vocabulary scores. Italic = control. "
           f"{len(skipped)} prompts skipped because the model's next token was whitespace or punctuation. "
           f"Commit {commit}, [rows]({out.relative_to(ROOT)}/rows.json.gz).</sub>")
markdown = tabulate(table, headers="keys", tablefmt="pipe", disable_numparse=True,
                    colalign=("left", "left") + ("right",) * 6) + "\n\n" + caption + "\n"
(out / "leaderboard.md").write_text(markdown)
print(markdown, f"\nskipped: {skipped}\n{out / 'leaderboard.md'}", flush=True)
