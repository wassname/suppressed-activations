"""Out-of-sample test: frozen selectors on language pairs without English or Chinese at either end.

New selector: erase the prompt's input embeddings (hs[layer 0] at every prompt position) from the
lens-space hidden state before reading it, instead of masking prompt words by string.
Hidden = English word, or Chinese word when Chinese is not the output (Qwen may think in either).
Pass = a hidden token ranks < K; best input and output tokens rank >= K.
de->fr is the dev pair; de->zh is a reference only (all earlier results used it).
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import csv
import importlib.util
import json
import bisect
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
from scripts.demo import trajectory  # noqa: E402

_spec = importlib.util.spec_from_file_location("s3", ROOT / "scripts/english/03_selector_search.py")
s3 = importlib.util.module_from_spec(_spec)
_argv, sys.argv = sys.argv, sys.argv[:1]
_spec.loader.exec_module(s3)
sys.argv = _argv
q, c, rise_fall, peak_any, ranks_of_best = s3.q, s3.c, s3.rise_fall, s3.peak_any, s3.ranks_of_best

K = 32
LANGS = ("de", "fr", "ru", "zh")
NAME = {"fr": "Français", "de": "Deutsch", "ru": "Русский", "zh": "中文"}
PAIRS = [("de", "zh"), ("de", "fr"), ("fr", "ru"), ("ru", "fr"), ("de", "ru"), ("ru", "de"), ("fr", "de")]
ROLE = {("de", "zh"): "ref", ("de", "fr"): "dev"}  # rest are test; Qwen trains mostly on en+zh, so neither is input/output
MIN_CHARS = {"en": 3, "zh": 1, "de": 3, "fr": 3, "ru": 3}
READ = range(22, 33)  # layers the selectors read at the last token


def load_lang(lang: str) -> dict[str, str]:
    path = q.WENDLER / f"{lang}/clean.csv"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/epfl-dlab/llm-latent-language/"
                                   f"{q.WENDLER_COMMIT}/data/langs/{lang}/clean.csv", path)
    return {r["word_original"]: r["word_translation"] for r in csv.DictReader(open(path))}


class WordIndex:
    """Find vocab tokens that spell the same word as a given token string (case/space-insensitive)."""

    def __init__(self, vocab_norm: list[str]):
        self.by_str: dict[str, list[int]] = {}
        for t, v in enumerate(vocab_norm):
            if v:
                self.by_str.setdefault(v, []).append(t)
        self.sorted = sorted(self.by_str)

    def same_word(self, w: str) -> set[int]:
        out = set(self.by_str.get(w, []))
        out |= {t for i in range(3, len(w)) for t in self.by_str.get(w[:i], [])}  # tokens that are a prefix of w
        if len(w) >= 2 or "\u4e00" <= w <= "\u9fff":  # tokens that start with w (skip 1-letter Latin/Cyrillic)
            i = bisect.bisect_left(self.sorted, w)
            while i < len(self.sorted) and self.sorted[i].startswith(w):
                out |= set(self.by_str[self.sorted[i]])
                i += 1
        return out


def output_word_mask(z_out: Tensor, vocab_norm: list[str], index: WordIndex, top_p: float = 0.9, max_n: int = 20) -> Tensor:
    """One pass: 'said' = words of the output layer's top tokens at this step. No generation."""
    p = z_out.softmax(-1)
    top = p.topk(max_n)
    keep = top.indices[(top.values.cumsum(0) - top.values) < top_p].tolist()
    ids = set().union(*(index.same_word(vocab_norm[t]) for t in keep if vocab_norm[t])) | set(keep)
    mask = torch.zeros_like(z_out, dtype=torch.bool)
    mask[sorted(ids)] = True
    return mask


def lens_space(h: Tensor, g: Tensor) -> Tensor:
    """u such that logits = u @ W.T (rmsnorm and gain applied)."""
    h = h.float()
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * g.float()


def main() -> None:
    torch.set_grad_enabled(False)
    out_dir = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_erase-language-pairs"
    out_dir.mkdir(parents=True)
    logger.add(out_dir / "stderr.log")

    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16).cuda().eval()
    W, g, final_norm = model.lm_head.weight, 1.0 + model.model.norm.weight, model.model.norm
    assert model.config.get_text_config().tie_word_embeddings, "erasure assumes tied embeddings"
    Wf = W.float()
    vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
    vocab_norm = [v.strip().lower() for v in vocab_text]
    tables = {l: load_lang(l) for l in LANGS}
    windex = WordIndex(vocab_norm)

    id_cache: dict[tuple[str, int], frozenset[int]] = {}

    def ids_for(word: str, lang: str) -> frozenset[int]:
        key = (word, MIN_CHARS[lang])
        if key not in id_cache:
            id_cache[key] = frozenset(t for t, v in enumerate(vocab_text) if v.strip() and q.is_prefix_hit(v, word, MIN_CHARS[lang]))
        return id_cache[key]

    selector_names = ["rise_fall 22/27/32 (repo)", "peak_any − prompt words (frozen 03 winner)",
                      "rise_fall 22/27/32, erased", "peak_any, erased", "peak_any, prompt words erased (re-tokenized)",
                      "peak logit lens L27",
                      "peak_any − prompt & output-layer words", "peak lens max L24-30 − prompt & output-layer words",
                      "peak lens L27 − prompt & output-layer words"]
    results, curves, n_skipped = {}, {}, {}
    for src, tgt in PAIRS:
        pair = f"{src}→{tgt}"
        words = [{"en": en, src: tables[src][en], tgt: tables[tgt][en], "zh": tables["zh"][en]}
                 for en in tables[src] if en in tables[tgt] and en in tables["zh"]]
        rng = random.Random(0)
        recs = {n: [] for n in selector_names}
        curve_sum, n_curve, n_skip = None, 0, 0
        for i, w in enumerate(words):
            shots = rng.sample([x for j, x in enumerate(words) if j != i], 4)
            prompt = "".join(f'{NAME[src]}: "{s[src]}" - {NAME[tgt]}: "{s[tgt]}"\n' for s in shots) + f'{NAME[src]}: "{w[src]}" - {NAME[tgt]}: "'
            ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            res, _ = trajectory(model, ids, final_norm)  # [33, seq, d]

            en, said, inp = ids_for(w["en"], "en"), ids_for(w[tgt], tgt), ids_for(w[src], src)
            zh_latent = ids_for(w["zh"], "zh") if tgt != "zh" else frozenset()
            if en & (said | inp):  # English spelled like the input or output: no activation-only method can separate it
                n_skip += 1
                continue
            hidden = sorted((en | zh_latent) - said - inp)
            said, inp = sorted(said), sorted(inp - en)

            # logit-lens probability curves at the last token, all layers
            p = (lens_space(res[:, -1], g) @ Wf.T).softmax(-1)
            row = torch.stack([p[:, sorted(en)].sum(-1), p[:, sorted(ids_for(w["zh"], "zh"))].sum(-1),
                               p[:, inp].sum(-1) if inp else torch.zeros(33, device=p.device), p[:, said].sum(-1)])
            curve_sum = row if curve_sum is None else curve_sum + row
            n_curve += 1

            # erase span of input embeddings: hs[layer 0] at every prompt position, in lens space
            E = res[0].float()
            torch.testing.assert_close(E, Wf[ids[0]], atol=1e-2, rtol=1e-2)  # tied: layer-0 residual = embedding row
            Q = torch.linalg.qr(E.T, mode="reduced").Q  # [d, seq]; logit_t = u · W_t, so erase W_t (= E rows), not g·W_t
            u = lens_space(res[list(READ), -1], g)
            u_erased = u - (u @ Q) @ Q.T
            # erase the tokens the model would use to *say* each prompt word (first token of common spellings)
            say_ids = set(ids[0].tolist())
            for word in set(re.findall(r"\w+", prompt)):
                for v in {word, word.lower(), word.capitalize()}:
                    for pre in ("", " "):
                        say_ids.add(tok(pre + v, add_special_tokens=False).input_ids[0])
            Q2 = torch.linalg.qr(Wf[sorted(say_ids)].T, mode="reduced").Q
            u_erased2 = u - (u @ Q2) @ Q2.T
            z, z_er = torch.zeros(33, W.shape[0], device=u.device), torch.zeros(33, W.shape[0], device=u.device)
            z_er2 = torch.zeros(33, W.shape[0], device=u.device)
            z[list(READ)], z_er[list(READ)], z_er2[list(READ)] = u @ Wf.T, u_erased @ Wf.T, u_erased2 @ Wf.T
            mask = q.prompt_word_mask(prompt, vocab_norm, u.device)
            # "said" = what the output layer is about to say at this step (one pass, no generation)
            mask_rs = mask | output_word_mask(z[32], vocab_norm, windex)
            scores = {
                "rise_fall 22/27/32 (repo)": rise_fall(z, 22, 27),
                "peak_any − prompt words (frozen 03 winner)": peak_any(z, 22, 24, 30).masked_fill(mask, float("-inf")),
                "rise_fall 22/27/32, erased": rise_fall(z_er, 22, 27),
                "peak_any, erased": peak_any(z_er, 22, 24, 30),
                "peak_any, prompt words erased (re-tokenized)": peak_any(z_er2, 22, 24, 30),
                "peak logit lens L27": c(z[27]),
                "peak_any − prompt & output-layer words": peak_any(z, 22, 24, 30).masked_fill(mask_rs, float("-inf")),
                "peak lens max L24-30 − prompt & output-layer words": c(z[24:31]).amax(0).masked_fill(mask_rs, float("-inf")),
                "peak lens L27 − prompt & output-layer words": c(z[27]).masked_fill(mask_rs, float("-inf")),
            }
            for name, score in scores.items():
                r_h, r_s, r_i = ranks_of_best(score, hidden), ranks_of_best(score, said), ranks_of_best(score, inp)
                r_en = ranks_of_best(score, sorted(en - set(said) - set(inp)))
                top1 = int(score.argmax())
                recs[name].append({"word": w["en"], "r_hidden": r_h, "r_said": r_s, "r_input": r_i,
                                   "hidden_is_zh": top1 in zh_latent, "ok": r_h < K and r_s >= K and r_i >= K,
                                   "ok_en_only": r_en < K and r_s >= K and r_i >= K})
        results[pair], n_skipped[pair] = recs, n_skip
        curves[pair] = (curve_sum / n_curve).tolist()
        logger.info(f"{pair}: {len(recs[selector_names[0]])} scored, {n_skip} skipped (English = input/output spelling)")

    def cell(rs): return f"{sum(r['ok'] for r in rs)}/{len(rs)}"
    table = tabulate([[n] + [cell(results[f"{s}→{t}"][n]) for s, t in PAIRS] for n in selector_names],
                     headers=["selector (top-32; pass = hidden in, input and output out)"] + [f"{s}→{t} ({ROLE.get((s, t), 'test')})" for s, t in PAIRS],
                     tablefmt="pipe")
    fails = tabulate([[n] + [f"{sum(r['r_hidden'] >= K for r in results[f'{s}→{t}'][n])}/{sum(r['r_said'] < K for r in results[f'{s}→{t}'][n])}/{sum(r['r_input'] < K for r in results[f'{s}→{t}'][n])}" for s, t in PAIRS] for n in selector_names],
                     headers=["failure counts: hidden missing / output in / input in"] + [f"{s}→{t}" for s, t in PAIRS], tablefmt="pipe")
    en_only = tabulate([[n] + [f"{sum(r['ok_en_only'] for r in results[f'{s}→{t}'][n])}/{len(results[f'{s}→{t}'][n])}" for s, t in PAIRS] for n in selector_names],
                       headers=["English-only passes (Chinese not counted)"] + [f"{s}→{t}" for s, t in PAIRS], tablefmt="pipe")
    peaks = tabulate([[pair, *[f"{max(curves[pair][k]):.2f} @L{max(range(33), key=lambda l: curves[pair][k][l])}" for k in range(4)]] for pair in curves],
                     headers=["pair", "English max p", "Chinese max p", "input max p", "output max p"], tablefmt="pipe")
    md = f"""---
script: scripts/english/04_erase_and_language_pairs.py
model: {q.MODEL}@{q.REVISION}
k: {K}
pairs: {[f"{s}->{t}" for s, t in PAIRS]}
dev_pair: de->fr
reference_pair: de->zh
skipped_per_pair: {json.dumps(n_skipped)}
---
# Erasing input embeddings, and frozen selectors on unseen language pairs -- Claudypoo[opus-4.8]

Which language does Qwen think in? Mean logit-lens probability at the last token (max over layers):

{peaks}

SHOULD: on pairs without zh, a Chinese peak well above zero means Qwen also thinks in Chinese.

{table}

{en_only}

{fails}
"""
    (out_dir / "run.md").write_text(md)
    (out_dir / "result.json").write_text(json.dumps({"results": results, "curves": curves, "skipped": n_skipped}, ensure_ascii=False))
    print(md)
    print(f"run.md: {out_dir / 'run.md'}")


if __name__ == "__main__":
    main()
