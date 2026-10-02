"""How many final-layer predicted words to mask (max_n 1/5/20, top_p .9 as in 04): choose on translation, check on English v3/v4.
Methods plain27, J24, J29 at the final prompt token. One prefill per prompt. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
from statistics import mean

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
g = runpy.run_path("scripts/english/08_jlens_one_pass.py")["main"].__globals__
q, s4, trajectory = g["q"], g["s4"], g["trajectory"]
RUNS = {"translation": "out/2026-09-30_125500_jlens-one-pass", "v3": "out/2026-09-30_125330_jlens-one-pass",
        "v4": "out/2026-09-30_142814_jlens-one-pass"}
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W = model.lm_head.weight
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
word_index = s4.WordIndex(vocab_norm)
NUMBER_WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}
METHODS = [("plain27", 27, False), ("J24", 24, True), ("J29", 29, True)]
MAX_N = (1, 5, 20)


def lens(h, residual, use_j):
    h = h.float() @ J[residual - 1].cuda().float().T if use_j else h.float()
    return model.lm_head(model.model.norm(h.to(W.dtype))).float()


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts, rows_out = {}, []
for set_name, run in RUNS.items():
    for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
        ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        final_logits = model.lm_head(model.model.norm(res[32][-1])).float()
        prompt_mask = q.prompt_word_mask(ref["prompt"], vocab_norm, "cuda")
        aliases = tuple(ref["hidden_aliases"])
        if aliases not in label_counts:
            label_counts[aliases] = sum(any(hit(v, w) for w in aliases) for v in vocab)
        said = sorted(set(ref["answer_aliases"]) | set(ref["actual_words"])) if ref["intended_answer_observed"] else list(ref["actual_words"])
        said += [NUMBER_WORDS[w] for w in said if w in NUMBER_WORDS]
        for n in MAX_N:
            mask = prompt_mask | s4.output_word_mask(final_logits, vocab_norm, word_index, max_n=n)
            for name, r, j in METHODS:
                top = [vocab[t] for t in lens(res[r][-1], r, j).masked_fill(mask, -torch.inf).topk(32).indices.tolist()]
                if n == 1 and name == "plain27":
                    assert top == ref["top32"], ref["concept"]
                tp = sum(any(hit(t, w) for w in aliases) for t in top[:8])
                p, recall = tp / 8, tp / label_counts[aliases]
                found = tp > 0
                leak = any(any(hit(t, w) for w in said) for t in top[:8])
                rows_out.append({"set": set_name, "concept": ref["concept"], "max_n": n, "method": name, "top32": top,
                                 "F1@8": 0.0 if tp == 0 else 2 * p * recall / (p + recall), "found8": found, "clean8": found and not leak})
Path("slop/audits/2026-10-02_output-mask-width.json").write_text(json.dumps(rows_out, ensure_ascii=False, indent=1))
summary = []
for set_name in RUNS:
    for n in MAX_N:
        for name, _, _ in METHODS:
            sel = [r for r in rows_out if r["set"] == set_name and r["max_n"] == n and r["method"] == name]
            summary.append({"set": set_name, "mask max_n": n, "method": name, "F1@8": mean(r["F1@8"] for r in sel),
                            "found in top8": f"{sum(r['found8'] for r in sel)}/{len(sel)}",
                            "found, answer not in top8": f"{sum(r['clean8'] for r in sel)}/{len(sel)}"})
print(tabulate(summary, headers="keys", tablefmt="pipe", floatfmt=".3f"))
