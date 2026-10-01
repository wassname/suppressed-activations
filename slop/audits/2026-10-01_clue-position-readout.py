"""Readout at the end of the clue phrase vs the final prompt token, English v3/v4, same masks, F1@k. — PI/OpenAI
Position rule (label-free, development): last token before the final ' is'/' belongs' in the prompt."""
import hashlib
import json
from pathlib import Path
import re
import runpy
from statistics import mean

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
g = runpy.run_path("scripts/english/08_jlens_one_pass.py")["main"].__globals__
q, s4, trajectory = g["q"], g["s4"], g["trajectory"]
RUNS = {"v3": "out/2026-09-30_125330_jlens-one-pass", "v4": "out/2026-09-30_142814_jlens-one-pass"}
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W = model.lm_head.weight
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
word_index = s4.WordIndex(vocab_norm)


def lens(h, residual, use_j):
    h = h.float() @ J[residual - 1].cuda().float().T if use_j else h.float()
    return model.lm_head(model.model.norm(h.to(W.dtype))).float()


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts = {}
METHODS = [(f"{'J' if j else 'plain'}{r}", r, j) for r, j in [(16, False), (20, False), (24, False), (27, False), (16, True), (20, True), (24, True)]]
records, rows_out = [], []
for set_name, run in RUNS.items():
    for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
        prompt = ref["prompt"]
        enc = tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
        cut = [m.start() for m in re.finditer(r" (is|belongs)\b", prompt)][-1]
        position = max(i for i, (_, end) in enumerate(enc["offset_mapping"]) if end <= cut)
        ids = torch.tensor([enc["input_ids"]]).cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        final_logits = model.lm_head(model.model.norm(res[32][-1])).float()
        mask = q.prompt_word_mask(prompt, vocab_norm, "cuda") | s4.output_word_mask(final_logits, vocab_norm, word_index, max_n=1)
        assert [vocab[t] for t in lens(res[27][-1], 27, False).masked_fill(mask, -torch.inf).topk(32).indices.tolist()] == ref["top32"]
        aliases = tuple(ref["hidden_aliases"])
        if aliases not in label_counts:
            label_counts[aliases] = sum(any(hit(v, w) for w in aliases) for v in vocab)
        said_words = sorted(set(ref["answer_aliases"]) | set(ref["actual_words"])) if ref["intended_answer_observed"] else ref["actual_words"]
        for where, pos in (("final", -1), ("clue", position)):
            for name, r, j in METHODS:
                top = [vocab[t] for t in lens(res[r][pos], r, j).masked_fill(mask, -torch.inf).topk(32).indices.tolist()]
                rec = {"set": set_name, "concept": ref["concept"], "where": where, "method": name, "clue_token": vocab[enc["input_ids"][position]], "top32": top}
                for k in (8, 32):
                    tp = sum(any(hit(t, w) for w in aliases) for t in top[:k])
                    p, recall = tp / k, tp / label_counts[aliases]
                    rec[f"F1@{k}"] = 0.0 if tp == 0 else 2 * p * recall / (p + recall)
                rec["found_unsaid"] = any(any(hit(t, w) for w in aliases) for t in top) and not any(any(hit(t, w) for w in said_words) for t in top)
                rows_out.append(rec)
Path("slop/audits/2026-10-01_clue-position-readout.json").write_text(json.dumps(rows_out, ensure_ascii=False, indent=1))
summary = []
for set_name in RUNS:
    for where in ("final", "clue"):
        for name, _, _ in METHODS:
            sel = [r for r in rows_out if r["set"] == set_name and r["where"] == where and r["method"] == name]
            summary.append({"set": set_name, "position": where, "method": name, "F1@8": mean(r["F1@8"] for r in sel),
                            "F1@32": mean(r["F1@32"] for r in sel), "found∧unsaid": f"{sum(r['found_unsaid'] for r in sel)}/{len(sel)}"})
print(tabulate(summary, headers="keys", tablefmt="pipe", floatfmt=".3f"))
print("clue tokens:", sorted({(r["concept"], r["clue_token"]) for r in rows_out}))
for r in rows_out:
    if r["where"] == "clue" and r["method"] in ("plain20", "J20") and r["concept"] in ("Sweden", "rabbit", "December"):
        print(r["method"], r["concept"], r["top32"][:10])
