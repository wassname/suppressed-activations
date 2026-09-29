"""Generalisation test: frozen translation selectors on English-only two-hop prompts (TwoHopFact, Yang et al. 2024).

Prompt r2(r1(e1)): "The author of the novel Nineteen Eighty-Four was born in the city of".
Hidden = bridge e2 (George Orwell), said = answer e3, read = prompt words. The method runs in one pass;
generation is used only by the scorer (bridge-knowledge filter, answer-correct split).
Pass = a bridge-word token ranks < K and no answer-word token (e3) ranks < K.
Only prompts where the model states the bridge when asked the first hop directly are scored,
so the bridge is known to the model. Selectors and layers are frozen from the language-pair dev run.
-- Claudypoo[opus-4.8]
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import importlib.util
import json
import random
import re
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

import torch
from loguru import logger
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.demo import trajectory  # noqa: E402

_spec = importlib.util.spec_from_file_location("s4", ROOT / "scripts/english/04_erase_and_language_pairs.py")
s4 = importlib.util.module_from_spec(_spec)
_argv, sys.argv = sys.argv, sys.argv[:1]
_spec.loader.exec_module(s4)
sys.argv = _argv
q, c, rise_fall, peak_any, ranks_of_best, lens_space = s4.q, s4.c, s4.rise_fall, s4.peak_any, s4.ranks_of_best, s4.lens_space

K = 32
PER_CATEGORY = 6
MAX_TRIES_PER_CATEGORY = 20  # 52 categories; caps the scorer's hop-1 generations at ~1000 (a few GPU minutes)
DATA = ROOT / "data/twohop/TwoHopFact.csv"  # CC-BY-4.0, fetched not vendored (45k rows)
URL = "https://huggingface.co/datasets/soheeyang/TwoHopFact/resolve/main/TwoHopFact.csv"


def name_words(names: list[str]) -> set[str]:
    return {w for n in names for w in re.findall(r"\w+", n) if len(w) >= 3}


def aliases(row: dict, entity: str) -> list[str]:
    return [a for group in ast.literal_eval(row[f"{entity}.aliases"]) for a in group] or [row[f"{entity}.value"]]


def main(diagnose: Path | None = None) -> None:
    torch.set_grad_enabled(False)
    started = time.monotonic()
    suffix = "twohop-four-case-diagnostic" if diagnose else "twohop-english"
    out_dir = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_{suffix}"
    out_dir.mkdir(parents=True)
    logger.add(out_dir / "stderr.log")
    if not DATA.exists():
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, DATA)

    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16).cuda().eval()
    W, g, final_norm = model.lm_head.weight, 1.0 + model.model.norm.weight, model.model.norm
    Wf = W.float()
    vocab_text = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
    vocab_norm = [v.strip().lower() for v in vocab_text]
    windex = s4.WordIndex(vocab_norm)

    word_ids: dict[str, frozenset[int]] = {}

    def ids_for_words(words: set[str]) -> set[int]:
        out: set[int] = set()
        for w in words:
            if w not in word_ids:
                word_ids[w] = frozenset(t for t, v in enumerate(vocab_text) if v.strip() and q.is_prefix_hit(v, w, 3))
            out |= word_ids[w]
        return out

    def greedy(prompt: str, n: int = 12) -> str:
        ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        return tok.decode(model.generate(ids, max_new_tokens=n, do_sample=False)[0, ids.shape[1]:], skip_special_tokens=True)

    rows = list(csv.DictReader(open(DATA)))
    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    rng = random.Random(0)
    names = ["peak_any − prompt & output-layer words (dev winner)", "peak lens L27 − prompt & output-layer words",
             "rise_fall 22/27/32 (repo)", "peak logit lens L27"]
    if diagnose:
        # Label-guided localisation is diagnostic only, not a new readout method. — PI/OpenAI
        prior = json.loads(diagnose.read_text())[names[0]]
        cases = [r for r in prior if r["two_hop_correct"]][:4]
        assert len(cases) == 4
        reports = []
        for case in cases:
            prompt = case["prompt"]
            matches = [r for r in rows if r["r2(r1(e1)).prompt"] == prompt
                       and aliases(r, "e2")[0] == case["bridge"] and aliases(r, "e3")[0] == case["answer"]]
            assert matches, case
            labels = {(tuple(aliases(r, "e2")), tuple(aliases(r, "e3"))) for r in matches}
            assert len(labels) == 1, labels
            bridge, answer = labels.pop()
            prompt_words = set(re.findall(r"\w+", prompt.lower()))
            hidden = sorted(ids_for_words({w.lower() for w in name_words(bridge)} - prompt_words))
            said = sorted(ids_for_words({w.lower() for w in name_words(answer)} - prompt_words))
            assert hidden and said and not set(hidden) & set(said)
            ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            res, logits = trajectory(model, ids, final_norm)
            locations = []
            for pos in range(ids.shape[1]):
                z = lens_space(res[:, pos], g) @ Wf.T
                best = z[:, hidden].max(-1)
                ranks = (z > best.values[:, None]).sum(-1).tolist()
                for layer, rank in enumerate(ranks):
                    t = hidden[int(best.indices[layer])]
                    locations.append({"position": pos, "input_token": tok.decode([int(ids[0, pos])]),
                                      "layer": layer, "r_hidden": rank, "best_hidden_token": vocab_text[t]})
            torch.save(z.cpu(), out_dir / f"case_{len(reports)}_last_logits.pt")
            prompt_mask = q.prompt_word_mask(prompt, vocab_norm, z.device)
            output_mask = s4.output_word_mask(z[32], vocab_norm, windex)
            raw = peak_any(z, 22, 24, 30)
            variants = {"peak_any raw": raw,
                        "peak_any prompt mask": raw.masked_fill(prompt_mask, -torch.inf),
                        "peak_any output mask": raw.masked_fill(output_mask, -torch.inf),
                        names[0]: raw.masked_fill(prompt_mask | output_mask, -torch.inf),
                        "plain L27 raw": c(z[27])}
            stages = {}
            for name, score in variants.items():
                r_h, r_s = ranks_of_best(score, hidden), ranks_of_best(score, said)
                stages[name] = {"r_hidden": r_h, "r_said": r_s, "ok": r_h < K and r_s >= K,
                                "top8": [vocab_text[t] for t in score.topk(8).indices.tolist()]}
            assert stages[names[0]]["r_hidden"] == case["r_hidden"], (stages, case)
            last = [r for r in locations if r["position"] == ids.shape[1] - 1]
            report = {"prior": case, "bridge_aliases": bridge, "answer_aliases": answer,
                      "best_anywhere": min(locations, key=lambda r: r["r_hidden"]),
                      "best_last_position": min(last, key=lambda r: r["r_hidden"]),
                      "stages": stages, "locations": locations,
                      "hidden_tokens": [{"token": vocab_text[t], "id": t,
                                         "prompt_masked": bool(prompt_mask[t]), "output_masked": bool(output_mask[t])}
                                        for t in hidden],
                      "actual_next_token": tok.decode([int(logits.argmax())])}
            reports.append(report)
            (out_dir / "result.json").write_text(json.dumps(reports, ensure_ascii=False, indent=1))
            logger.info(f"{case['bridge']}: prior rank reproduced; raw={stages['peak_any raw']['r_hidden']}, "
                        f"masked={stages[names[0]]['r_hidden']}, best last={report['best_last_position']}")
        table = tabulate([[r["prior"]["bridge"], r["stages"][names[0]]["r_hidden"],
                           r["stages"]["peak_any raw"]["r_hidden"], r["best_last_position"]["r_hidden"],
                           r["best_last_position"]["layer"], r["best_anywhere"]["r_hidden"],
                           f"L{r['best_anywhere']['layer']}/P{r['best_anywhere']['position']}"] for r in reports],
                         headers=["bridge", "frozen rank", "unmasked rank", "best last-token lens rank",
                                  "layer", "best anywhere lens rank", "location"], tablefmt="pipe")
        details = "\n\n".join(f"Input: {r['prior']['prompt']!r}\n\nPrior continuation: {r['prior']['said_text']!r}\n\n"
                               f"Stages: {json.dumps(r['stages'], ensure_ascii=False)}" for r in reports)
        source_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        md = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nsource_sha256: {source_sha}\nprior: {diagnose}\n"
              f"forward_passes: 4\ngenerations: 0\nelapsed_seconds: {time.monotonic() - started:.2f}\n---\n"
              "# Four-case localisation diagnostic\n\nWritten by PI/OpenAI.\n\n"
              "Selection: first four previously answer-correct cases, in saved order. No success-rate claim.\n"
              "SHOULD: frozen ranks reproduce exactly. If masking causes the misses, unmasked ranks improve. "
              "If location causes misses, the plain lens finds the bridge elsewhere. These label-selected locations "
              "are diagnostics, not a frozen method or causal evidence.\n\n"
              f"{table}\n\n{details}\n\nrun.md: {out_dir / 'run.md'}\n")
        (out_dir / "run.md").write_text(md)
        print(md)
        return

    recs, n_tried, n_unknown, n_overlap = {n: [] for n in names}, 0, 0, 0
    for cat in sorted(by_cat):
        pool = by_cat[cat][:]
        rng.shuffle(pool)
        kept = 0
        for r in pool[:MAX_TRIES_PER_CATEGORY]:
            if kept >= PER_CATEGORY:
                break
            n_tried += 1
            bridge, answer = aliases(r, "e2"), aliases(r, "e3")
            prompt = r["r2(r1(e1)).prompt"]
            hop1 = greedy(r["r1(e1).prompt"])
            if not any(b.lower() in hop1.lower() for b in bridge):  # model must know the bridge
                n_unknown += 1
                continue
            prompt_words = {w.lower() for w in re.findall(r"\w+", prompt)}
            hidden_words = {w.lower() for w in name_words(bridge)} - prompt_words
            answer_words = {w.lower() for w in name_words(answer)} - prompt_words
            hidden, said = ids_for_words(hidden_words), ids_for_words(answer_words)
            if not hidden or not said or hidden & said:
                n_overlap += 1
                continue
            kept += 1
            ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            res, _ = trajectory(model, ids, final_norm)
            said_text = greedy(prompt, 8)  # scorer only: splits results by whether the two-hop answer is right
            z = torch.zeros(33, W.shape[0], device=res.device)
            z[list(s4.READ)] = lens_space(res[list(s4.READ), -1], g) @ Wf.T
            mask_rs = q.prompt_word_mask(prompt, vocab_norm, z.device) | s4.output_word_mask(z[32], vocab_norm, windex)
            scores = {
                names[0]: peak_any(z, 22, 24, 30).masked_fill(mask_rs, float("-inf")),
                names[1]: c(z[27]).masked_fill(mask_rs, float("-inf")),
                names[2]: rise_fall(z, 22, 27),
                names[3]: c(z[27]),
            }
            two_hop_correct = any(a.lower() in said_text.lower() for a in answer)
            for n, score in scores.items():
                r_h, r_s = ranks_of_best(score, sorted(hidden)), ranks_of_best(score, sorted(said))
                top = [vocab_text[t] for t in score.topk(8).indices.tolist()]
                recs[n].append({"category": cat, "prompt": prompt, "bridge": bridge[0], "answer": answer[0],
                                "said_text": said_text, "two_hop_correct": two_hop_correct,
                                "r_hidden": r_h, "r_said": r_s, "ok": r_h < K and r_s >= K, "top8": top})
        logger.info(f"{cat}: kept {kept}; total scored {len(recs[names[0]])}, tried {n_tried}")
    n = len(recs[names[0]])
    logger.info(f"tried {n_tried}, bridge unknown {n_unknown}, overlap/empty {n_overlap}, scored {n}")

    def rate(rs, cond=lambda r: True):
        sub = [r for r in rs if cond(r)]
        return f"{sum(r['ok'] for r in sub)}/{len(sub)}"
    table = tabulate([[nm, rate(recs[nm]), rate(recs[nm], lambda r: r["two_hop_correct"]),
                       rate(recs[nm], lambda r: not r["two_hop_correct"]),
                       sum(r["r_hidden"] < K for r in recs[nm]), sum(r["r_said"] < K for r in recs[nm]),
                       sorted(r["r_hidden"] for r in recs[nm])[n // 2]] for nm in names],
                     headers=["selector (frozen)", "pass, all", "pass, two-hop answer correct", "pass, answer wrong",
                              "bridge in top-32", "answer in top-32", "median bridge rank"], tablefmt="pipe")
    ex = [r for r in recs[names[0]] if r["two_hop_correct"]][:6]
    examples = "\n".join(f"- `{r['prompt']}` → said `{r['said_text'].strip()[:40]!r}`; bridge **{r['bridge']}** at rank {r['r_hidden']}; top-8 {r['top8']}" for r in ex)
    md = f"""---
script: scripts/english/06_twohop_english.py
model: {q.MODEL}@{q.REVISION}
data: TwoHopFact (Yang et al. 2024), CC-BY-4.0
k: {K}
per_category: {PER_CATEGORY}
tried: {n_tried}
max_tries_per_category: {MAX_TRIES_PER_CATEGORY}
bridge_unknown_to_model: {n_unknown}
skipped_overlap_or_empty: {n_overlap}
scored: {n}
---
# Frozen selectors on English-only two-hop prompts -- Claudypoo[opus-4.8]

Hidden = bridge entity (e2), said = answer entity (e3). Scored only when the model names the bridge
when asked the first hop directly. Pass = bridge token in top {K}, answer tokens not.

SHOULD: if the method generalises, the dev winner passes far more often than the plain logit lens.

{table}

First six scored prompts where the two-hop answer is correct (dev winner):

{examples}
"""
    (out_dir / "run.md").write_text(md)
    (out_dir / "result.json").write_text(json.dumps(recs, ensure_ascii=False))
    print(md)
    print(f"run.md: {out_dir / 'run.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnose", type=Path, help="Inspect four correct cases from an earlier result.json; no generation.")
    main(**vars(parser.parse_args()))
