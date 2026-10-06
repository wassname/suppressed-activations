"""Write data/challenge/words.json: one word per meaning in each of ru, ko, ar, hi, th, for building prompts.

Candidates come from the MUSE bilingual dictionaries (Conneau et al. 2018, CC-BY-NC; downloaded, not shipped). For each English word
the kept form is the candidate the model scores highest after a 4-shot English->xx prompt; the word is dropped for that
language unless the model's top next token starts that form, so the lists are screened by the model being scored.
They are used only to write prompts; scoring uses Unicode scripts and the English word. Run once before score.py. — PI/OpenAI
"""
import json
import re
from collections import defaultdict

import torch

from common import DEVICE, LANG_NAME, ROOT, fetch, model, tok

SHOTS = {  # fixed example words, kept out of the list
    "ru": ["собака", "дерево", "птица", "хлеб"], "ko": ["개", "나무", "새", "빵"], "ar": ["كلب", "شجرة", "طائر", "خبز"],
    "hi": ["कुत्ता", "पेड़", "पक्षी", "रोटी"], "th": ["สุนัข", "ต้นไม้", "นก", "ขนมปัง"],
}
MUSE_MD5 = {'ru': '0e1f659a276b1969ac0c4fb6a26c092e', 'ko': 'ee99bdd36358b1a899150df33fe143fa', 'ar': 'c08059fa8272e2fe20cc95dbb1595fc8', 'hi': '43a77ef70b62be500b2a91cfd592eb6d', 'th': 'd6fcb5c788a6bf80e3b395bbf178ab09'}
SHOT_EN = ["dog", "tree", "bird", "bread"]
english = sorted(set(json.loads((ROOT / "data/challenge/english_words.json").read_text())) - set(SHOT_EN))

words = defaultdict(dict)
for lang, name in LANG_NAME.items():
    candidates = defaultdict(list)
    muse = fetch(f"data/muse/en-{lang}.txt", f"https://dl.fbaipublicfiles.com/arrival/dictionaries/en-{lang}.txt", MUSE_MD5[lang])
    for line in open(muse):
        en, x = line.rstrip("\n").split(None, 1)
        if en in english and not re.search(r"[A-Za-z\u4e00-\u9fff]", x):
            candidates[en].append(x)
    head = "".join(f'English: "{e}" - {name}: "{x}"\n' for e, x in zip(SHOT_EN, SHOTS[lang]))
    for en in english:
        prompt_ids = tok(head + f'English: "{en}" - {name}: "', add_special_tokens=False).input_ids
        best = None
        for x in candidates[en]:
            ids = torch.tensor([prompt_ids + tok(x + '"', add_special_tokens=False).input_ids]).to(DEVICE)
            logp = model(input_ids=ids, use_cache=False).logits[0, len(prompt_ids) - 1:-1].float().log_softmax(-1)
            score = float(logp.gather(1, ids[0, len(prompt_ids):, None]).sum())
            if best is None or score > best[0]:
                best = (score, x, int(ids[0, len(prompt_ids)]), int(logp[0].argmax()))
        if best and best[2] == best[3]:
            words[en][lang] = best[1]
    print(lang, sum(lang in w for w in words.values()), "of", len(english), flush=True)
(ROOT / "data/challenge/words.json").write_text(json.dumps(dict(sorted(words.items())), ensure_ascii=False, indent=1) + "\n")
