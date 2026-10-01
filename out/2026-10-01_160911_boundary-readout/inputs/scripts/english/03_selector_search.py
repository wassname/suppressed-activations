"""Challenge: find the hidden English word without using that it is English.

Allowed inputs: activations (all layers, last prompt token), the model's own unembedding and final norm,
and the prompt text. Language labels are used only by the scorer.
Scorer per prompt: best rank of an English-answer token < K, and best ranks of Chinese (said) and
German (input) tokens >= K. Selectors are compared on even prompts; the winner is reported on odd prompts.
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import importlib.util
import json
import random
import re
import sys
import time
from pathlib import Path

import torch
from loguru import logger
from tabulate import tabulate
from torch import Tensor
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.demo import trajectory  # noqa: E402

_spec = importlib.util.spec_from_file_location("q", ROOT / "scripts/english/01_detector_baselines_and_pair_transfer.py")
q = importlib.util.module_from_spec(_spec)
_argv, sys.argv = sys.argv, sys.argv[:1]
_spec.loader.exec_module(q)
sys.argv = _argv

K = 32
N_LAYERS = 32  # residual index 32 = pre-final-norm output


def ranks_of_best(score: Tensor, ids: list[int]) -> int:
    """0-based rank of the highest-scoring token in ids (ties broken pessimistically)."""
    if not ids:
        return 10**9
    best = score[ids].max()
    return int((score > best).sum()) if torch.isfinite(best) else 10**9


# ---------------- selectors: (lens logits [L+1, V], prompt mask [V]) -> score [V] ----------------

def c(z: Tensor) -> Tensor:
    return z - z.mean(-1, keepdim=True)


def rise_fall(z: Tensor, e: int, p: int, o: int = N_LAYERS) -> Tensor:
    return torch.minimum(c(z[p] - z[e]).clamp_min(0), c(z[p] - z[o]).clamp_min(0))


def peak_any(z: Tensor, e: int, lo: int, hi: int, o: int = N_LAYERS) -> Tensor:
    """Rise-and-fall with the peak layer chosen per token: max over peak layers in [lo, hi]."""
    return torch.stack([rise_fall(z, e, p, o) for p in range(lo, hi + 1)]).amax(0)


def build_selectors(logp: bool) -> dict:
    s = {
        "rise_fall 22/27/32 (repo)": lambda z: rise_fall(z, 22, 27),
        "fall 27-32": lambda z: c(z[27] - z[32]),
        "peak_any e22 p24-30": lambda z: peak_any(z, 22, 24, 30),
        "peak_any e18 p22-30": lambda z: peak_any(z, 18, 22, 30),
        "max_l(z_l) - z_out, l24-30": lambda z: c(z[24:31].amax(0) - z[32]),
        "mean_l(z_l) - z_out, l24-30": lambda z: c(z[24:31].mean(0) - z[32]),
    }
    for e in (16, 20, 22):
        for p in (25, 26, 27, 28, 29):
            s[f"rise_fall {e}/{p}/32"] = (lambda e, p: lambda z: rise_fall(z, e, p))(e, p)
    return s


def main() -> None:
    torch.set_grad_enabled(False)
    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "out" / f"{stamp}_selector-search"
    out_dir.mkdir(parents=True)
    logger.add(out_dir / "stderr.log")

    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16).cuda().eval()
    W, g, final_norm = model.lm_head.weight, 1.0 + model.model.norm.weight, model.model.norm
    vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
    vocab_norm = [v.strip().lower() for v in vocab_text]
    words = q.load_words()

    def ids_for(word: str, min_chars: int) -> set[int]:
        return {t for t, v in enumerate(vocab_text) if v.strip() and q.is_prefix_hit(v, word, min_chars)}

    # cache lens logits per prompt (all layers, last token) as fp16 on GPU: 33 x V per prompt
    rng = random.Random(0)
    data = []
    for i, w in enumerate(words):
        shots = rng.sample([x for j, x in enumerate(words) if j != i], 4)
        prompt = "".join(f'Deutsch: "{s["de"]}" - 中文: "{s["zh"]}"\n' for s in shots) + f'Deutsch: "{w["de"]}" - 中文: "'
        res, _ = trajectory(model, tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda(), final_norm)
        z = q.logit_lens(res[:, -1], W, g)  # [33, V] float32
        en, zh = ids_for(w["en"], 3), ids_for(w["zh"], 1)
        de = ids_for(w["de"], 3) - en
        data.append({"w": w, "z": z.half(), "mask": q.prompt_word_mask(prompt, vocab_norm, z.device),
                     "en": sorted(en), "zh": sorted(zh), "de": sorted(de)})
    logger.info(f"cached {len(data)} prompts")

    rows, per_selector = [], {}
    for name, fn in build_selectors(logp=False).items():
        for drop_prompt in (False, True):
            label = name + (" − prompt words" if drop_prompt else "")
            recs = []
            for d in data:
                score = fn(d["z"].float())
                if drop_prompt:
                    score = score.masked_fill(d["mask"], float("-inf"))
                r_en, r_zh, r_de = (ranks_of_best(score, d[k]) for k in ("en", "zh", "de"))
                recs.append({"r_en": r_en, "r_zh": r_zh, "r_de": r_de,
                             "ok": r_en < K and r_zh >= K and r_de >= K})
            per_selector[label] = recs
            even, odd = recs[0::2], recs[1::2]
            med = sorted(r["r_en"] for r in recs)[len(recs) // 2]
            rows.append([label, sum(r["ok"] for r in even), len(even), sum(r["ok"] for r in odd), len(odd),
                         sum(r["r_en"] < K for r in recs), sum(r["r_zh"] < K for r in recs),
                         sum(r["r_de"] < K for r in recs), med])
    rows.sort(key=lambda r: -r[1])
    best = rows[0][0]
    table = tabulate(
        [[f"**{r[0]}**" if r[0] == best else r[0], f"{r[1]}/{r[2]}", f"{r[3]}/{r[4]}", r[5], r[6], r[7], r[8]] for r in rows],
        headers=["selector (sorted by even-half score)", f"success@{K} even (select)", f"success@{K} odd (report)",
                 "English in top-32 (all 120)", "Chinese in", "German in", "median best-English rank"],
        tablefmt="pipe")
    logger.info("\n" + table)

    md = f"""---
script: scripts/english/03_selector_search.py
model: {q.MODEL}@{q.REVISION}
k: {K}
n_prompts: {len(data)}
selected_on: even-index prompts
reported_on: odd-index prompts
best_on_even: {best!r}
---
# Selector search: find the hidden word without language info -- Claudypoo[opus-4.8]

success@{K}: best English-answer token rank < {K}, best Chinese (said) and German (input) ranks >= {K}.
Selection uses the even half only; the odd column is the held-out estimate for the selected row.
SHOULD: the winner's odd score is close to its even score; a large drop means the choice overfit.

{table}
"""
    (out_dir / "run.md").write_text(md)
    (out_dir / "result.json").write_text(json.dumps({"rows": rows, "per_selector": per_selector,
                                                     "words": [d["w"] for d in data]}, ensure_ascii=False))
    print(md)
    print(f"run.md: {out_dir / 'run.md'}")


if __name__ == "__main__":
    main()
