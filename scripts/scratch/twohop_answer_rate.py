"""Does Qwen answer the TwoHopFact prompts? Next-token check with and without a "Fact: " prefix. — PI/OpenAI"""
import ast, csv, random, re, sys
sys.path.insert(0, "scripts/challenge")
from common import TWOHOP, forward, vocab

rows = list(csv.DictReader(open(TWOHOP())))
random.Random(0).shuffle(rows)
rows = rows[:150]
aliases = lambda r, e: [a for g in ast.literal_eval(r[f"{e}.aliases"]) for a in g] or [r[f"{e}.value"]]
for fmt in ("{p}", "Fact: {p} "):
    n_word = n_right = 0
    for r in rows:
        _, _, logits = forward(fmt.format(p=r["r2(r1(e1)).prompt"]))
        nxt = vocab[int(logits.argmax())]
        word = bool(re.search(r"[^\W_]", nxt))
        right = word and any(a.lower().startswith(nxt.strip().lower()) for a in aliases(r, "e3")) and len(nxt.strip()) > 0
        n_word += word
        n_right += right
    print(f"{fmt!r:16} next token is a word: {n_word}/{len(rows)}   starts the right answer: {n_right}/{len(rows)}", flush=True)
