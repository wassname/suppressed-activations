"""Causal check on language pairs: swap the selected hidden-word component between two prompts.

Prompt pair (same 4 shots, different test word), e.g. de->fr "Herz" (source) and "Schule" (target).
At residuals 23-30, last token, prefill, replace the source component in basis S_s with the target
component in basis S_t (as heart->school). Pass = top-1 becomes the target's first output token.
Bases come from each prompt's clean pass (one forward each, no generation), top-8 tokens of a selector.
The dev winner is frozen from 04 (de->fr); test pairs have neither English nor Chinese at either end.
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import importlib.util
import json
import random
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
from scripts.demo import layer_hooks, replace_output, trajectory  # noqa: E402
from suppressed_activation_subspace import matched_random_rotation, replace  # noqa: E402

_spec = importlib.util.spec_from_file_location("s4", ROOT / "scripts/english/04_erase_and_language_pairs.py")
s4 = importlib.util.module_from_spec(_spec)
_argv, sys.argv = sys.argv, sys.argv[:1]
_spec.loader.exec_module(s4)
sys.argv = _argv
q, c, peak_any, lens_space = s4.q, s4.c, s4.peak_any, s4.lens_space

PAIRS = [("de", "fr"), ("fr", "ru"), ("ru", "de")]  # de->fr is dev
N_PAIRS = 40  # word pairs per language pair
RANK = 8  # heart->school config
PATCH_RESIDUALS = range(23, 31)
N_GEN = 12  # greedy tokens, first 3 pairs only, for reading


def basis_from_ids(ids: list[int], W: Tensor, g: Tensor) -> Tensor:
    rows = (W.float() - W.float().mean(0))[ids] * g.float()
    return torch.linalg.qr(rows.T, mode="reduced").Q[None]  # [1, d, k]


def main() -> None:
    torch.set_grad_enabled(False)
    out_dir = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_edit-language-pairs"
    out_dir.mkdir(parents=True)
    logger.add(out_dir / "stderr.log")

    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16).cuda().eval()
    blocks, final_norm = model.model.layers, model.model.norm
    W, g = model.lm_head.weight, 1.0 + final_norm.weight
    Wf = W.float()
    vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
    vocab_norm = [v.strip().lower() for v in vocab_text]
    windex = s4.WordIndex(vocab_norm)
    tables = {l: s4.load_lang(l) for l in ("de", "fr", "ru")}

    def en_ids(word: str) -> list[int]:  # as 01: English tokens long enough to name the word
        return sorted(t for t, v in enumerate(vocab_text) if v.strip() and q.is_prefix_hit(v, word, 3)
                      and len(v.strip()) >= max(3, len(word) - 2))

    def said_ids(word: str) -> list[int]:
        return sorted(t for t, v in enumerate(vocab_text) if v.strip() and q.is_prefix_hit(v, word, 3))

    modes = ["peak_any − prompt & output-layer words (dev winner)", "peak lens L27 − prompt & output-layer words",
             "English word tokens (oracle)", "output word tokens (oracle, said)",
             "random rotation, norm matched to dev winner", "full residual (upper bound)"]
    summary, examples, per_pair_all = {}, [], {}
    for src_l, tgt_l in PAIRS:
        pair = f"{src_l}→{tgt_l}"
        words = [{"en": en, "src": tables[src_l][en], "tgt": tables[tgt_l][en]} for en in tables[src_l] if en in tables[tgt_l]]
        rng = random.Random(0)
        rng.shuffle(words)
        shots, pool = words[:4], words[4:]
        head = "".join(f'{s4.NAME[src_l]}: "{s["src"]}" - {s4.NAME[tgt_l]}: "{s["tgt"]}"\n' for s in shots)

        clean = []
        for w in pool:
            if len(clean) >= 2 * N_PAIRS:
                break
            prompt = head + f'{s4.NAME[src_l]}: "{w["src"]}" - {s4.NAME[tgt_l]}: "'
            ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            res, logits = trajectory(model, ids, final_norm)
            first = tok(w["tgt"], add_special_tokens=False).input_ids[0]
            e_ids = en_ids(w["en"])
            if int(logits.argmax()) != first or not e_ids or set(e_ids) & set(said_ids(w["tgt"])):
                continue  # wrong translation, or English spelled like the output: skip
            z = torch.zeros(33, W.shape[0], device=res.device)
            z[list(s4.READ)] = lens_space(res[list(s4.READ), -1], g) @ Wf.T
            mask = q.prompt_word_mask(prompt, vocab_norm, z.device) | s4.output_word_mask(z[32], vocab_norm, windex)
            sel = {modes[0]: peak_any(z, 22, 24, 30).masked_fill(mask, float("-inf")).topk(RANK).indices.tolist(),
                   modes[1]: c(z[27]).masked_fill(mask, float("-inf")).topk(RANK).indices.tolist()}
            bases = {m: basis_from_ids(sel[m], W, g) for m in modes[:2]}
            bases[modes[2]] = basis_from_ids(e_ids[:RANK], W, g)
            bases[modes[3]] = basis_from_ids(said_ids(w["tgt"])[:RANK], W, g)
            clean.append({"w": w, "ids": ids, "res": res, "logits": logits, "first": first, "bases": bases,
                          "selected": [vocab_text[t] for t in sel[modes[0]]],
                          "en_in_selected": bool(set(sel[modes[0]]) & set(e_ids))})
        logger.info(f"{pair}: {len(clean)} prompts translated correctly (top-1 = first output token)")

        def run(src: dict, tgt: dict, mode: str, distances: dict | None, gen: bool) -> dict:
            record: dict[int, float] = {}
            gen_rng = torch.Generator(device="cuda").manual_seed(src["first"])

            def hook_for(r: int):
                def hook(_m, _i, output):
                    hidden = output[0] if isinstance(output, tuple) else output
                    if hidden.shape[1] == 1:
                        return output  # prefill-only patch
                    h = hidden[:, -1:].float()
                    h_t = tgt["res"][r, -1].reshape(1, 1, -1).float()
                    if mode == modes[5]:
                        p = h_t
                    elif mode == modes[4]:
                        p = matched_random_rotation(h, torch.randn(h.shape, device=h.device, generator=gen_rng),
                                                    torch.full_like(h[..., :1], distances[r]))
                    else:
                        p = replace(h, src["bases"][mode], h_t, tgt["bases"][mode], strength=1.0, restore_norm=True)
                    record[r] = float((p - h).norm())
                    hidden = hidden.clone()
                    hidden[:, -1:] = p.to(hidden.dtype)
                    return replace_output(output, hidden)
                return hook

            with layer_hooks(blocks, {r - 1: hook_for(r) for r in PATCH_RESIDUALS}):
                logits = model(input_ids=src["ids"], use_cache=False).logits[0, -1].float()
                text = tok.decode(model.generate(src["ids"], max_new_tokens=N_GEN, do_sample=False)[0, src["ids"].shape[1]:]) if gen else None
            lp, lp0 = logits.log_softmax(-1), src["logits"].log_softmax(-1)
            a0, a1 = src["first"], tgt["first"]
            return {"top1": vocab_text[int(logits.argmax())], "to_target": int(logits.argmax()) == a1,
                    "still_source": int(logits.argmax()) == a0,
                    "swap_log_odds_shift": float((lp[a1] - lp[a0]) - (lp0[a1] - lp0[a0])),
                    "bare_answer_mass": float(lp[a0].exp() + lp[a1].exp()),
                    "rel_norm": sum(record.values()) / sum(float(src["res"][r, -1].float().norm()) for r in record),
                    "distances": record, "gen": text}

        rows, per_pair = {m: [] for m in modes}, []
        for k in range(len(clean) // 2):
            src, tgt = clean[2 * k], clean[2 * k + 1]
            rec = {"src": src["w"], "tgt": tgt["w"], "selected": [src["selected"], tgt["selected"]],
                   "en_in_both": src["en_in_selected"] and tgt["en_in_selected"]}
            for m in modes:
                rec[m] = run(src, tgt, m, rec[modes[0]]["distances"] if m == modes[4] else None,
                             gen=k < 3 and m in (modes[0], modes[5]))
                rows[m].append(rec[m])
            per_pair.append(rec)
        per_pair_all[pair] = per_pair

        def med(x): return sorted(x)[len(x) // 2]
        summary[pair] = [[m, f"{sum(r['to_target'] for r in rows[m])}/{len(rows[m])}",
                          f"{sum(r['still_source'] for r in rows[m])}/{len(rows[m])}",
                          f"{med([r['swap_log_odds_shift'] for r in rows[m]]):+.2f}",
                          f"{med([r['bare_answer_mass'] for r in rows[m]]):.2f}",
                          f"{med([r['rel_norm'] for r in rows[m]]):.2f}"] for m in modes]
        examples += [f"- {pair} **{p['src']['src']} → {p['tgt']['src']}** (want `{p['tgt']['tgt']}`); selected (source) "
                     f"{p['selected'][0]}; dev winner → `{p[modes[0]]['gen']!r}`; full residual → `{p[modes[5]]['gen']!r}`"
                     for p in per_pair[:3]]
        logger.info(f"{pair}\n" + tabulate(summary[pair], tablefmt="pipe"))

    headers = ["component replaced (rank 8, L23-30, last token)", "top-1 = target", "top-1 = source",
               "median swap_log_odds_shift (nats)", "median bare_answer_mass", "median ‖Δh‖/‖h‖"]
    tables_md = "\n\n".join(f"### {pair}{' (dev)' if pair == 'de→fr' else ' (test)'}\n\n{tabulate(rows, headers=headers, tablefmt='pipe')}"
                            f"\n\nEnglish word in both rank-8 selections: {sum(p['en_in_both'] for p in per_pair_all[pair])}/{len(per_pair_all[pair])} pairs"
                            for pair, rows in summary.items())
    md = f"""---
script: scripts/english/07_edit_language_pairs.py
model: {q.MODEL}@{q.REVISION}
pairs: {list(summary)}
n_word_pairs_max: {N_PAIRS}
rank: {RANK}
patch_residuals: {list(PATCH_RESIDUALS)}
---
# Swapping the selected hidden-word component between prompts -- Claudypoo[opus-4.8]

Pass = top-1 next token becomes the target prompt's first output token. Bases from each prompt's clean pass.
swap_log_odds_shift > 0 means movement from the source answer toward the target answer.

SHOULD: dev winner well above random (random ≈ 0); oracle-English above dev winner if the selection is noisy;
the output-word oracle is the easy case (it edits what is said, not what is thought).

{tables_md}

First three pairs per language pair ({N_GEN} greedy tokens, patch on prefill only):

{chr(10).join(examples)}
"""
    (out_dir / "run.md").write_text(md)
    (out_dir / "result.json").write_text(json.dumps({pair: [{k: v for k, v in p.items()} for p in pp] for pair, pp in per_pair_all.items()}, ensure_ascii=False, indent=1))
    print(md)
    print(f"run.md: {out_dir / 'run.md'}")


if __name__ == "__main__":
    main()
