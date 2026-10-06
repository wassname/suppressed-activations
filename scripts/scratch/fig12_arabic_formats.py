"""Gurnee et al. Fig. 12 spider prompt, question in Arabic, answer in Russian: which fixed formats does Qwen answer?
Tried in this order; the README uses the first that answers восемь and says how many were tried. — PI/OpenAI"""
import sys
sys.path.insert(0, "scripts/challenge")
import torch
from common import forward, vocab

Q_DOG, Q_BIRD, Q_HUMAN = "كم عدد أرجل الكلب؟", "كم عدد أرجل الطائر؟", "كم عدد أرجل الإنسان؟"
Q = "كم عدد أرجل الحيوان الذي ينسج الشبكات؟"       # how many legs does the animal that weaves webs have?
FORMATS = {
    "QA, dog+bird shots": f"سؤال: {Q_DOG}\nОтвет: четыре\nسؤال: {Q_BIRD}\nОтвет: два\nسؤال: {Q}\nОтвет:",
    "QA, bird shot": f"سؤال: {Q_BIRD}\nОтвет: два\nسؤال: {Q}\nОтвет:",
    "QA, human shot": f"سؤال: {Q_HUMAN}\nОтвет: два\nسؤال: {Q}\nОтвет:",
    "quoted, like the test prompts": f'العربية: "{Q_BIRD}" - Русский: "два"\nالعربية: "{Q}" - Русский: "',
    "quoted, dog+bird shots": f'العربية: "{Q_DOG}" - Русский: "четыре"\nالعربية: "{Q_BIRD}" - Русский: "два"\nالعربية: "{Q}" - Русский: "',
    "instruction, zero-shot": f"Ответь по-русски одним словом.\nسؤال: {Q}\nОтвет:",
}
for name, prompt in FORMATS.items():
    p = torch.softmax(forward(prompt)[2], -1)
    top = p.topk(5)
    words = [f"{vocab[i]!r} {v:.2f}" for v, i in zip(top.values.tolist(), top.indices.tolist())]
    ok = vocab[int(top.indices[0])].strip().lower().startswith("вос")
    print(f"{'OK ' if ok else '-- '} {name:32} {' | '.join(words)}", flush=True)
