"""README demo: Gurnee et al.'s Fig. 12 spider question, asked in Arabic. Writes docs/leaderboard/demo_spider.md.

The prompt is the 1st of 14 fixed Arabic wordings that Qwen answers correctly (scripts/scratch/fig12_arabic_formats*.py).
One table: input, thoughts by layer, output; spider in any language bold, eight in any language italic.
Usage: uv run scripts/challenge/demo.py (a minute on CPU) — PI/OpenAI
"""
import torch
from tabulate import tabulate

from bench import top_words
from common import ROOT, forward, readout, vocab
from transforms import jlens

READ = ["سؤال: كم عدد أرجل الطائر؟", "Ответ: два", "سؤال: كم عدد أرجل الحيوان الذي يغزل شبكة من خيوط الحرير؟", "Ответ: "]
READ_EN = ["Question: How many legs does a bird have?", "Answer: two",
           "Question: How many legs does the animal that spins a web from silk threads have?", "Answer:"]
LAYERS = (22, 24, 26, 28, 30)
GLOSS = {"？": "?", "。": ".", "．": ".", "！": "!", "：": ":", "昆虫": "insect", "蜘蛛": "spider", "蛛": "spider", "爬": "crawl", "腿": "leg", "腿部": "leg", "八": "eight",
         "八个": "eight", "八条": "eight", "восемь": "eight", "huit": "eight", "ocho": "eight", "acht": "eight"}
SPIDER, EIGHT = {"spider", "spiders"}, {"eight", "8", "-eight", "_eight"}


def meaning(w):
    return GLOSS.get(w, w).lower()


def mark(w):
    return f"**{w}**" if meaning(w) in SPIDER else f"*{w}*" if meaning(w) in EIGHT else w


def translate(ws):
    """The row in English, as if through Google Translate: every word replaced by its English, markup kept."""
    return " ".join(mark(GLOSS.get(w, w)) for w in ws)


if __name__ == "__main__":
    with torch.no_grad():
        res, _, logits = forward("\n".join(READ))
    x = res[:, -1].float()
    answer = vocab[int(logits.argmax())].strip()
    print("model says:", repr(answer), f"p={torch.softmax(logits, -1).max():.2f}")
    rows = [["**input**", "<br>".join(READ), "<br>".join(READ_EN)]]
    for i, l in enumerate(LAYERS):
        ws = [vocab[t].strip() for t in top_words(readout(jlens(x[l], l)))]
        rows.append([("**thoughts**, layer " if i == 0 else "layer ") + str(l), "⟨" + " ".join(mark(w) for w in ws) + "⟩",
                     "⟨" + translate(ws) + "⟩"])  # ⟨ ⟩: read out of intermediate states, never said
    rows.append(["**output**", mark(answer), mark(GLOSS.get(answer, answer))])
    table = tabulate(rows, ["", "model", "English, for the reader"], "pipe", colalign=("left", "left", "left"))
    print(table)
    (ROOT / "docs/leaderboard").mkdir(exist_ok=True)
    (ROOT / "docs/leaderboard/demo_spider.md").write_text(table + "\n")
