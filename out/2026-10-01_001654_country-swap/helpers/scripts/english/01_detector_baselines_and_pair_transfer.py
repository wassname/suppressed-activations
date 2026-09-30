"""English-setting checks (Wendler de->zh words, Qwen3.5-4B).

Q1: does the rise-and-fall selector find the English answer better than plain logit lens at the peak layer?
Q2: does the single heart->school component replacement generalise across many word pairs?
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import csv
import json
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

import torch
from loguru import logger
from tabulate import tabulate
from torch import Tensor
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.demo import layer_hooks, replace_output, trajectory  # noqa: E402
from suppressed_activation_subspace import (  # noqa: E402
    matched_random_rotation,
    replace,
    subspace_from_scores,
    suppressed_activation_scores,
)

MODEL = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
WENDLER_COMMIT = "d0e4f292f204d69bf9bc51cbe35e73e4f66e896f"  # epfl-dlab/llm-latent-language; no licence, so fetched not vendored
WENDLER = ROOT / "data/wendler_words"
EARLY, PEAK, OUT = 22, 27, 32  # README figure layers
RANK_DETECT = 32  # README hit-rate rank
# heart->school demo config (git b9255a1^:scripts/demo.py): early 22, peak 27, out 32, rank 8, residuals L23..L30
RANK_PATCH = 8
PATCH_START = int(sys.argv[1]) if len(sys.argv) > 1 else 23  # optional window start for layer sweeps
PATCH_RESIDUALS = range(PATCH_START, PATCH_START + 8)
N_GEN = 24


def load_words() -> list[dict]:
    for lang in ("de", "zh"):
        path = WENDLER / f"{lang}/clean.csv"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            url = f"https://raw.githubusercontent.com/epfl-dlab/llm-latent-language/{WENDLER_COMMIT}/data/langs/{lang}/clean.csv"
            urllib.request.urlretrieve(url, path)
    de = {r["word_original"]: r["word_translation"] for r in csv.DictReader(open(WENDLER / "de/clean.csv"))}
    zh = {r["word_original"]: r["word_translation"] for r in csv.DictReader(open(WENDLER / "zh/clean.csv"))}
    return [{"en": en, "de": de[en], "zh": zh[en]} for en in de if en in zh]


def is_prefix_hit(token_text: str, word: str, min_chars: int) -> bool:
    t = token_text.strip().lower()
    return len(t) >= min(min_chars, len(word)) and word.lower().startswith(t)


def logit_lens(h: Tensor, W: Tensor, g: Tensor) -> Tensor:
    hn = h.float() * torch.rsqrt(h.float().square().mean(-1, keepdim=True) + 1e-6) * g.float()
    return hn @ W.float().T


def centered(z: Tensor) -> Tensor:
    return z - z.mean(-1, keepdim=True)


def prompt_word_mask(prompt: str, vocab_norm: list[str], device) -> Tensor:
    """True for tokens that spell a word, or a >=3-char prefix of a word, already in the prompt. Uses no language info."""
    words = set(re.findall(r"\w+", prompt.lower()))
    prefixes = {w[:i] for w in words for i in range(3, len(w) + 1)}
    return torch.tensor([bool(v) and (v in words or v in prefixes) for v in vocab_norm], device=device)


def selector_scores(res_last: Tensor, W: Tensor, g: Tensor, in_prompt: Tensor | None = None) -> dict[str, Tensor]:
    """res_last [layers, d] -> vocab scores [V] per selector. in_prompt adds variants that drop words read in the input."""
    z_early, z_peak, z_out = logit_lens(res_last[[EARLY, PEAK, OUT]], W, g)
    rise, fall = centered(z_peak - z_early), centered(z_peak - z_out)
    rise_fall = suppressed_activation_scores(res_last[None], W, g, early_layer=EARLY, peak_layer=PEAK, output_layer=OUT)[0]
    torch.testing.assert_close(rise_fall, torch.minimum(rise.clamp_min(0), fall.clamp_min(0)))
    out = {"rise_and_fall (repo)": rise_fall, "peak logit lens": centered(z_peak), "fall only": fall,
           "rise only": rise, "output logits (sanity)": centered(z_out)}
    if in_prompt is not None:
        for k in ("rise_and_fall (repo)", "fall only", "peak logit lens"):
            out[f"{k} − prompt words"] = out[k].masked_fill(in_prompt, float("-inf"))
    return out


def basis_from_ids(ids: list[int], W: Tensor, g: Tensor) -> Tensor:
    rows = (W.float() - W.float().mean(0))[ids] * g.float()
    return torch.linalg.qr(rows.T, mode="reduced").Q[None]


def main() -> None:
    torch.set_grad_enabled(False)
    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "out" / f"{stamp}_english-baselines-L{PATCH_START}"
    out_dir.mkdir(parents=True)
    logger.add(out_dir / "stderr.log")

    tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=torch.bfloat16).cuda().eval()
    blocks, final_norm = model.model.layers, model.model.norm
    W, g = model.lm_head.weight, 1.0 + final_norm.weight
    vocab_text = tok.convert_ids_to_tokens(list(range(W.shape[0])))
    vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in vocab_text]
    vocab_norm = [v.strip().lower() for v in vocab_text]

    words = load_words()
    logger.info(f"{len(words)} de/zh/en word triples")

    # ---------- Q1: detector hit rates, Wendler few-shot prompt ----------
    # Eval: language is only the answer key. hidden = English (find), said = Chinese (exclude), input = German (exclude).
    def word_ids(word: str, min_chars: int) -> set[int]:
        return {t for t, s in enumerate(vocab_text) if s.strip() and is_prefix_hit(s, word, min_chars)}

    def auroc(score: Tensor, pos: list[int], neg: list[int] | None) -> float:
        """P(score of a hidden-word token > score of a negative token), ties count half."""
        p = score[pos][:, None]
        n = score[neg][None] if neg is not None else score[torch.ones_like(score, dtype=torch.bool).index_fill_(0, torch.tensor(pos, device=score.device), False)][None]
        return float((p > n).float().mean() + 0.5 * (p == n).float().mean())

    rng = random.Random(0)
    q1_records: dict[str, list[dict]] = {}
    examples = []
    n_q1 = 0
    for i, w in enumerate(words):
        shots = rng.sample([x for j, x in enumerate(words) if j != i], 4)
        prompt = "".join(f'Deutsch: "{s["de"]}" - 中文: "{s["zh"]}"\n' for s in shots) + f'Deutsch: "{w["de"]}" - 中文: "'
        ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, final_norm)
        n_q1 += 1
        en_ids, zh_ids = word_ids(w["en"], 3), word_ids(w["zh"], 1)
        de_ids = word_ids(w["de"], 3) - en_ids  # German/English cognates (Hand/hand) count as English
        assert en_ids and zh_ids and not (en_ids & zh_ids), w
        for name, score in selector_scores(res[:, -1], W, g, prompt_word_mask(prompt, vocab_norm, res.device)).items():
            top = set(score.topk(RANK_DETECT).indices.tolist())
            rec = {"en": bool(top & en_ids), "zh": bool(top & zh_ids), "de": bool(top & de_ids),
                   "auroc_en_vs_zh": auroc(score, sorted(en_ids), sorted(zh_ids)),
                   "auroc_en_vs_vocab": auroc(score, sorted(en_ids), None)}
            rec["isolates"] = rec["en"] and not rec["zh"] and not rec["de"]
            q1_records.setdefault(name, []).append(rec)
            if i < 3 and name == "rise_and_fall (repo)":
                examples.append({"word": w, "top8": [vocab_text[t] for t in score.topk(8).indices.tolist()]})

    def med(x): return sorted(x)[len(x) // 2]
    hits = {name: {k: sum(r[k] for r in rs) for k in ("isolates", "en", "zh", "de")} for name, rs in q1_records.items()}
    for name, rs in q1_records.items():  # pick a variant on even prompts, report it on odd prompts
        hits[name]["isolates_even"] = sum(r["isolates"] for r in rs[0::2])
        hits[name]["isolates_odd"] = sum(r["isolates"] for r in rs[1::2])
    q1_rows = [[name, f"**{h['isolates']}/{n_q1}**", f"{h['isolates_even']}/{len(words[0::2])}", f"{h['isolates_odd']}/{len(words[1::2])}", f"{h['en']}/{n_q1}", f"{h['zh']}/{n_q1}", f"{h['de']}/{n_q1}",
                f"{med([r['auroc_en_vs_zh'] for r in q1_records[name]]):.2f}",
                f"{med([r['auroc_en_vs_vocab'] for r in q1_records[name]]):.3f}"] for name, h in hits.items()]
    q1_table = tabulate(q1_rows, headers=["selector (top-32 tokens)", "isolates hidden word", "even half", "odd half", "English in", "Chinese in",
                                          "German in", "median AUROC EN vs ZH", "median AUROC EN vs vocab"],
                        tablefmt="pipe")
    logger.info("\n" + q1_table)

    # ---------- Q2: component replacement across word pairs, zero-shot prompt (as heart->school) ----------
    def zero_shot(de_word: str) -> str:
        return f'The Chinese translation of the German word "{de_word}" is "'

    clean = []
    extra = [{"en": "heart", "de": "Herz", "zh": "心"}, {"en": "school", "de": "Schule", "zh": "学校"}]
    for w in extra + [x for x in words if x["de"] not in ("Herz", "Schule")]:
        ids = tok(zero_shot(w["de"]), return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, logits = trajectory(model, ids, final_norm)
        zh_id = tok(w["zh"], add_special_tokens=False).input_ids[0]
        if int(logits.argmax()) != zh_id:
            continue  # model does not translate this word correctly first-token; not a usable pair
        en_ids = sorted({t for t, s in enumerate(vocab_text) if s.strip() and is_prefix_hit(s, w["en"], 3)
                         and len(s.strip()) >= max(3, len(w["en"]) - 2)})
        zh_ids = sorted({t for t, s in enumerate(vocab_text) if s.strip() and is_prefix_hit(s, w["zh"], 1)})
        scores = selector_scores(res[:, -1], W, g, prompt_word_mask(zero_shot(w["de"]), vocab_norm, res.device))
        clean.append({"w": w, "ids": ids, "res": res, "logits": logits, "zh_id": zh_id,
                      "bases": {
                          "rise_and_fall (repo)": subspace_from_scores(scores["rise_and_fall (repo)"][None], W, g, rank=RANK_PATCH)[0],
                          "rise_and_fall (repo) − prompt words": subspace_from_scores(scores["rise_and_fall (repo) − prompt words"][None], W, g, rank=RANK_PATCH)[0],
                          "peak logit lens": subspace_from_scores(scores["peak logit lens"][None], W, g, rank=RANK_PATCH)[0],
                          "English answer tokens (oracle)": basis_from_ids(en_ids, W, g) if en_ids else None,
                          "Chinese answer tokens (oracle)": basis_from_ids(zh_ids, W, g),
                      },
                      "rf_selected": [vocab_text[t] for t in scores["rise_and_fall (repo)"].topk(RANK_PATCH).indices.tolist()]})
    logger.info(f"{len(clean)} words translated correctly zero-shot (top-1 = first zh token)")
    assert clean[0]["w"]["de"] == "Herz" and clean[1]["w"]["de"] == "Schule", "heart->school pair must reproduce"

    pairs = [(0, 1)] + [(i, i + 1) for i in range(2, len(clean) - 1)]  # fixed pairing, heart->school first

    def run(src: dict, tgt: dict, mode: str, distances: dict | None = None, gen: bool = False) -> dict:
        record: dict[int, float] = {}
        gen_rng = torch.Generator(device="cuda").manual_seed(src["zh_id"])

        def hook_for(r: int):
            def hook(_m, _i, output):
                hidden = output[0] if isinstance(output, tuple) else output
                if hidden.shape[1] == 1:
                    return output  # prefill-only patch
                h = hidden[:, -1:].float()
                h_t = tgt["res"][r, -1].reshape(1, 1, -1).float()
                if mode == "full residual (upper bound)":
                    p = h_t
                elif mode == "random rotation, matched to rise_and_fall norm":
                    direction = torch.randn(h.shape, device=h.device, generator=gen_rng)
                    p = matched_random_rotation(h, direction, torch.full_like(h[..., :1], distances[r]))
                else:
                    S_s, S_t = src["bases"][mode], tgt["bases"][mode]
                    p = replace(h, S_s, h_t, S_t, strength=1.0, restore_norm=True)
                record[r] = float((p - h).norm())
                hidden = hidden.clone()
                hidden[:, -1:] = p.to(hidden.dtype)
                return replace_output(output, hidden)
            return hook

        hooks = {r - 1: hook_for(r) for r in PATCH_RESIDUALS}
        with layer_hooks(blocks, hooks):
            logits = model(input_ids=src["ids"], use_cache=False).logits[0, -1].float()
            text = None
            if gen:
                o = model.generate(src["ids"], max_new_tokens=N_GEN, do_sample=False)
                text = tok.decode(o[0, src["ids"].shape[1]:])
        lp, lp0 = logits.log_softmax(-1), src["logits"].log_softmax(-1)
        s, t = src["zh_id"], tgt["zh_id"]
        return {"top1": tok.decode([int(logits.argmax())]), "to_target": int(logits.argmax()) == t,
                "still_source": int(logits.argmax()) == s,
                "d_logodds": float((lp[t] - lp[s]) - (lp0[t] - lp0[s])), "distances": record, "gen": text}

    modes = ["rise_and_fall (repo)", "rise_and_fall (repo) − prompt words", "peak logit lens", "English answer tokens (oracle)", "Chinese answer tokens (oracle)",
             "random rotation, matched to rise_and_fall norm", "full residual (upper bound)"]
    rows, per_pair = {m: [] for m in modes}, []
    for k, (a, b) in enumerate(pairs):
        src, tgt = clean[a], clean[b]
        pair_rec = {"src": src["w"], "tgt": tgt["w"], "rf_selected": [src["rf_selected"], tgt["rf_selected"]],
                    "rf_english_in_both": all(any(is_prefix_hit(t, x["w"]["en"], 3) for t in x["rf_selected"]) for x in (src, tgt))}
        for m in modes:
            if m == "English answer tokens (oracle)" and (src["bases"][m] is None or tgt["bases"][m] is None):
                continue
            dist = pair_rec["rise_and_fall (repo)"]["distances"] if m.startswith("random") else None
            r = run(src, tgt, m, dist, gen=(k < 6 and m in ("rise_and_fall (repo)", "full residual (upper bound)")))
            rows[m].append(r)
            pair_rec[m] = r
        per_pair.append(pair_rec)
        if k == 0:
            hs = pair_rec["rise_and_fall (repo)"]
            logger.info(f"heart->school reproduction: top1={hs['top1']!r} d_logodds={hs['d_logodds']:+.2f} (job 63: 学校, -12.83 -> +0.12)")

    q2_rows = [[m, len(rows[m]), f"{sum(r['to_target'] for r in rows[m])}/{len(rows[m])}",
                f"{sum(r['still_source'] for r in rows[m])}/{len(rows[m])}",
                f"{med([r['d_logodds'] for r in rows[m]]):+.2f}"] for m in modes]
    q2_table = tabulate(q2_rows, headers=[f"replacement at L{PATCH_START}-L{PATCH_START + 7}, last token, prefill", "pairs",
                                           "top-1 = target zh", "top-1 = source zh", "median Δ log-odds (nats)"],
                        tablefmt="pipe")
    logger.info("\n" + q2_table)

    split = []
    for flag in (True, False):
        sub = [p for p in per_pair if p["rf_english_in_both"] == flag]
        split.append([f"English answer in both rank-8 selections = {flag}", len(sub),
                      f"{sum(p['rise_and_fall (repo)']['to_target'] for p in sub)}/{len(sub)}"])
    split_table = tabulate(split, headers=["rise_and_fall pairs", "n", "top-1 = target zh"], tablefmt="pipe")
    logger.info("\n" + split_table)

    gens = "\n\n".join(
        f"**{p['src']['de']} → {p['tgt']['de']}** (want {p['tgt']['zh']})\n\n"
        + "\n".join(f"- {m}: `{p[m]['gen']!r}`" for m in ("rise_and_fall (repo)", "full residual (upper bound)"))
        for p in per_pair[:6])

    md = f"""---
script: scripts/english/01_detector_baselines_and_pair_transfer.py
model: {MODEL}@{REVISION}
layers: {{early: {EARLY}, peak: {PEAK}, out: {OUT}}}
rank_detect: {RANK_DETECT}
rank_patch: {RANK_PATCH}
patch_residuals: {list(PATCH_RESIDUALS)}
n_q1: {n_q1}
n_pairs: {len(pairs)}
---
# English-setting baselines -- Claudypoo[opus-4.8]

## Q1. Which top-32 selector contains the answer word? (Wendler 4-shot de->zh prompt, all words)

English hit = a selected token is a >=3-char prefix of the English word. Chinese hit = a selected token is a prefix of the Chinese word.

{q1_table}

rise_and_fall top-8 examples: {json.dumps(examples, ensure_ascii=False)}

## Q2. Does replacing the component move the answer to the target word? (zero-shot prompt, fixed consecutive pairing)

SHOULD: rise_and_fall well above random; if peak logit lens ≈ rise_and_fall, the fall term adds nothing causally.

{q2_table}

{split_table}

First-token generations ({N_GEN} tokens, patch on prompt only):

{gens}
"""
    (out_dir / "run.md").write_text(md)
    (out_dir / "result.json").write_text(json.dumps(
        {"q1": hits, "n_q1": n_q1, "q2": {m: [{k: v for k, v in r.items()} for r in rows[m]] for m in modes},
         "pairs": [{k: p[k] for k in ("src", "tgt", "rf_selected", "rf_english_in_both")} for p in per_pair]}, ensure_ascii=False, indent=1))
    print(md[-3000:])
    print(f"run.md: {out_dir / 'run.md'}")


if __name__ == "__main__":
    main()
