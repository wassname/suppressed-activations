"""Shared benchmark pieces: prompts, labels, top-8 words, F1. Used by score.py and notebook.py.

See score.py for the scoring rule. — PI/OpenAI
"""
import csv
import json
import random
import re

import torch

from common import DEVICE, LANG_NAME, ROOT, SCRIPT, WENDLER_ZH, W, forward, readout, tok, tokens_in_script, vocab

K, PER_PAIR = 8, 60  # per pair capped by the word list
DEV, TEST = [("ru", "ko")], [("ar", "ru"), ("ar", "hi"), ("hi", "th"), ("th", "ru"), ("ko", "ar")]  # ar→ru: the README pair
script = {lang: tokens_in_script(pattern) for lang, pattern in SCRIPT.items()}
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
                   "leak_in": script[src], "leak_out": script[tgt], "right": spelled(w) | frozenset(by_spelling.get(chinese[w], []))}


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


def calibration_prompts():
    """Shared unlabelled calibration strings, without target answers. — PI/OpenAI"""
    texts = json.loads((ROOT / "data/challenge/wikitext2_train_300.json").read_text())["texts"]
    return texts + [item["prompt"] for item in translation_prompts(DEV, "dev")]


def calibration_texts():
    """Unlabelled text for calibrate(): hs [17 layers (16-32), tokens, d] for 300 WikiText texts and the dev prompts."""
    for text in calibration_prompts():
        yield forward(text, max_length=128)[0][16:]


def prepare(item):
    """One forward pass -> (state, input-side leaks, output-side leaks incl. the next token), or None if the model is
    about to write whitespace or punctuation."""
    res, attn, logits = forward(item["prompt"])
    nxt = int(logits.argmax())
    if not re.search(r"\w", vocab[nxt]):
        return None
    enc = tok(item["prompt"], add_special_tokens=False, return_offsets_mapping=True)
    line_start = item["prompt"].rfind("\n") + 1
    line = [i for i, (_, end) in enumerate(enc.offset_mapping) if end > line_start]  # tokens of the prompt's last line
    state = {"res": res[:, -1], "attn": attn[-1], "logits": logits, "ids": torch.tensor(enc.input_ids).to(DEVICE),
             "line": res[:, line], "input": res[:, item["input_pos"]],
             "hs": res[16:]}  # what geometry methods get: layers 16-32, all prompt tokens
    return state, item["leak_in"], item["leak_out"] | {nxt}


def read_vector(v, name):
    """The output head is used only here, to check which words a geometry transform's vector holds."""
    assert v.shape == (W.shape[1],), f"{name} must return an activation-space vector"
    return readout(v)


def judge(scores, item, leak_in, leak_out):
    top = set(top_words(scores))
    return {"top8": [vocab[t] for t in top_words(scores)], "hidden": bool(top & item["right"]),
            "leaked_in": bool(top & leak_in), "leaked_out": bool(top & leak_out), "leaked": bool(top & (leak_in | leak_out))}
