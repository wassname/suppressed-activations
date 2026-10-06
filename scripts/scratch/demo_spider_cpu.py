"""CPU run of notebook Part 1's README demo (the GPU queue is busy). Writes docs/leaderboard/demo_spider.md; the next
GPU notebook run overwrites it with the canonical version. — PI/OpenAI"""
import re, sys
import torch
torch.nn.Module.cuda = lambda self, *a, **k: self   # run on CPU
torch.Tensor.cuda = lambda self, *a, **k: self
sys.path.insert(0, "scripts/challenge")
from tabulate import tabulate
from common import ROOT, forward, readout, vocab
from bench import top_words
from transforms import jlens

src = open("scripts/challenge/notebook.py").read()
SPIDER_AR = eval(re.search(r'^SPIDER_AR = (".*")$', src, re.M).group(1))   # the notebook's prompt, one source
words = lambda scores: " ".join(vocab[t].strip() for t in top_words(scores))
with torch.no_grad():
    res, _, logits = forward(SPIDER_AR)
x = res[:, -1].float()
p = torch.softmax(logits, -1).topk(5)
print("model says:", [(vocab[i], round(v, 2)) for v, i in zip(p.values.tolist(), p.indices.tolist())])
demo = tabulate([[l, words(readout(jlens(x[l], l)))] for l in (20, 22, 24, 26, 28, 30)], ["layer", "top 8 words (J-lens)"],
                "pipe", colalign=("right", "left"))
print(demo)
(ROOT / "docs/leaderboard/demo_spider.md").write_text(demo + "\n")
