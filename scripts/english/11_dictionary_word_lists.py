"""Word lists for distant input/output languages from the MUSE bilingual dictionaries (Conneau et al. 2018).

Languages: Russian, Korean, Arabic, Hindi, Thai: no shared script with English or Chinese, which stay the hidden languages.
English words: Wendler's list with a Chinese translation. Each word keeps all MUSE translations as aliases. The canonical
form shown in prompts is the MUSE alias the model finds most likely after an English 4-shot prompt (sum of token
log-probabilities, closing quote included); the word is dropped for that language unless the model's most likely next
token starts that alias. Shots are hand-written words outside the list. — PI/OpenAI
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
import re
import runpy

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
ROOT = Path(__file__).resolve().parents[2]
q = runpy.run_path(str(ROOT / "scripts/english/08_jlens_one_pass.py"))["main"].__globals__["q"]
LANGS = {"ru": "Русский", "ko": "한국어", "ar": "العربية", "hi": "हिन्दी", "th": "ไทย"}
SHOTS = {
    "ru": [("dog", "собака"), ("tree", "дерево"), ("bird", "птица"), ("bread", "хлеб")],
    "ko": [("dog", "개"), ("tree", "나무"), ("bird", "새"), ("bread", "빵")],
    "ar": [("dog", "كلب"), ("tree", "شجرة"), ("bird", "طائر"), ("bread", "خبز")],
    "hi": [("dog", "कुत्ता"), ("tree", "पेड़"), ("bird", "पक्षी"), ("bread", "रोटी")],
    "th": [("dog", "สุนัข"), ("tree", "ต้นไม้"), ("bird", "นก"), ("bread", "ขนมปัง")],
}
zh = {r["word_original"]: r["word_translation"] for r in csv.DictReader(open(ROOT / "data/wendler_words/zh/clean.csv"))}
muse = {}
for lang in LANGS:
    m = defaultdict(list)
    for line in open(ROOT / f"data/muse/en-{lang}.txt"):
        a, b = line.rstrip("\n").split(None, 1)
        if a in zh and not re.search(r"[A-Za-z\u4e00-\u9fff]", b) and b not in m[a]:
            m[a].append(b)
    muse[lang] = m
words = sorted(w for w in zh if all(muse[l].get(w) for l in LANGS))
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
out = {"author": "PI/OpenAI", "source": "MUSE en-xx dictionaries, data/muse/; Wendler en/zh list", "words": {}}
for lang, name in LANGS.items():
    kept = 0
    for w in words:
        prompt = "".join(f'English: "{e}" - {name}: "{x}"\n' for e, x in SHOTS[lang]) + f'English: "{w}" - {name}: "'
        prompt_ids = tok(prompt, add_special_tokens=False).input_ids
        n = len(prompt_ids)
        best, best_lp, top = None, -float("inf"), None
        for alias in muse[lang][w]:
            # continuation tokenised on its own, as the model would generate it after the fixed prompt
            ids = torch.tensor([prompt_ids + tok(alias + '"', add_special_tokens=False).input_ids]).cuda()
            lp = model(input_ids=ids, use_cache=False).logits[0, n - 1:-1].float().log_softmax(-1)
            if top is None:
                top = int(lp[0].argmax())
            score = float(lp.gather(1, ids[0, n:, None]).sum())
            if score > best_lp:
                best, best_lp, first = alias, score, int(ids[0, n])
        entry = out["words"].setdefault(w, {"zh": zh[w]})
        if top == first:
            entry[lang] = {"canonical": best, "aliases": muse[lang][w], "log_p": best_lp}
            kept += 1
    print(lang, kept, "of", len(words), flush=True)
out["words"] = {w: e for w, e in out["words"].items() if len(e) > 1}
(ROOT / "data/muse/word_lists.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print({l: sum(l in e for e in out["words"].values()) for l in LANGS})
