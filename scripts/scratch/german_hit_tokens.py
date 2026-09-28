"""Which tokens count as German/English hits for rise-and-fall? Checks short-prefix artefacts. -- Claudypoo[opus-4.8]"""

import importlib.util
import random
import sys
from collections import Counter
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("q", ROOT / "scripts/english/01_detector_baselines_and_pair_transfer.py")
q = importlib.util.module_from_spec(spec)
sys.argv = sys.argv[:1]
spec.loader.exec_module(q)

torch.set_grad_enabled(False)
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16).cuda().eval()
W, g, final_norm = model.lm_head.weight, 1.0 + model.model.norm.weight, model.model.norm
vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
words = q.load_words()
rng = random.Random(0)
de_hits, en_hits = Counter(), Counter()
for strict in (3, 4):
    counts = Counter()
    rng = random.Random(0)
    for i, w in enumerate(words):
        shots = rng.sample([x for j, x in enumerate(words) if j != i], 4)
        prompt = "".join(f'Deutsch: "{s["de"]}" - 中文: "{s["zh"]}"\n' for s in shots) + f'Deutsch: "{w["de"]}" - 中文: "'
        res, _ = q.trajectory(model, tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda(), final_norm)
        score = q.selector_scores(res[:, -1], W, g)["rise_and_fall (repo)"]
        top = [vocab_text[t] for t in score.topk(q.RANK_DETECT).indices.tolist()]
        en = [t for t in top if q.is_prefix_hit(t, w["en"], strict)]
        de = [t for t in top if q.is_prefix_hit(t, w["de"], strict) and not q.is_prefix_hit(t, w["en"], 3)]
        zh = [t for t in top if q.is_prefix_hit(t, w["zh"], 1)]
        counts["en"] += bool(en); counts["de"] += bool(de); counts["zh"] += bool(zh)
        counts["isolates"] += bool(en) and not de and not zh
        if strict == 3:
            de_hits.update((w["de"], t) for t in de); en_hits.update((w["en"], t) for t in en)
    print(f"min prefix chars {strict}: {dict(counts)} of {len(words)}")
print("German hits (word, token):", de_hits.most_common(40))
print("English hits sample:", en_hits.most_common(25))
