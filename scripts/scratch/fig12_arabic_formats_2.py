"""Second fixed list of Arabic wordings for Gurnee et al.'s Fig. 12 spider question (6 tried before, all failed).
Tried in this order; we keep the first that Qwen answers correctly and print its readout. — PI/OpenAI"""
import sys
sys.path.insert(0, "scripts/challenge")
import torch
from common import forward, readout, vocab
from transforms import jlens

BIRD = "كم عدد أرجل الطائر؟"
QS = {  # clearer wordings of "the animal that spins webs"
    "makes webs to catch insects": "كم عدد أرجل الحيوان الذي يصنع شباكًا ليصطاد الحشرات؟",
    "spins a web from silk threads": "كم عدد أرجل الحيوان الذي يغزل شبكة من خيوط الحرير؟",
}
FORMATS = {}
for qn, q in QS.items():
    FORMATS[f"{qn}, Russian word"] = (f"سؤال: {BIRD}\nОтвет: два\nسؤال: {q}\nОтвет:", ("вос",))
    FORMATS[f"{qn}, digit"] = (f"سؤال: {BIRD}\nالجواب: 2\nسؤال: {q}\nالجواب:", ("8",))
    FORMATS[f"{qn}, Fact-style statement, digit"] = (
        f"حقيقة: عدد أرجل الطائر هو 2\nحقيقة: عدد أرجل {q.removeprefix('كم عدد أرجل ').removesuffix('؟')} هو", ("8",))
    FORMATS[f"{qn}, Russian word, 'Ответ: '"] = (f"سؤال: {BIRD}\nОтвет: два\nسؤال: {q}\nОтвет: ", ("вос",))
# Fig. 12's third example (antonym of small -> big, with English "big" in the middle), here Arabic question -> Russian answer
HOT = "ما عكس كلمة \"حار\"؟"          # opposite of "hot"?  -> холодный (cold)
SMALL = "ما عكس كلمة \"صغير\"؟"       # opposite of "small"? -> большой (big)
FORMATS["antonym small, QA, hot shot"] = (f"سؤال: {HOT}\nОтвет: холодный\nسؤال: {SMALL}\nОтвет:", ("бол", "вели"))
FORMATS["antonym small, quoted, hot shot"] = (
    f'العربية: "{HOT}" - Русский: "холодный"\nالعربية: "{SMALL}" - Русский: "', ("бол", "вели"))
first = {}  # family ("spider" or "antonym") -> (format name, last-token residuals)
for name, (prompt, good) in FORMATS.items():
    res, _, logits = forward(prompt)
    p = torch.softmax(logits, -1)
    top = p.topk(5)
    nxt = vocab[int(top.indices[0])].strip().lower()
    ok = any(nxt.startswith(g) for g in good)
    print(f"{'OK ' if ok else '-- '} {name:58} " + " | ".join(f"{vocab[i]!r} {v:.2f}" for v, i in zip(top.values.tolist(), top.indices.tolist())), flush=True)
    family = "antonym" if name.startswith("antonym") else "spider"
    if ok and family not in first:
        first[family] = (name, res[:, -1])
for family, (name, x) in first.items():
    print(f"\nfirst {family} format that answers: {name}")
    for l in (20, 22, 24, 26, 28, 30, 31):
        ids = readout(jlens(x[l], l)).topk(8).indices.tolist()
        print(f"| {l} | {' '.join(vocab[i].strip() for i in ids)} |")
