"""Word-level fall (after 2760: token-level fall let spelling variants of the spoken word through, e.g. ' stockholm').
The output side uses the max final logit over tokens that spell the same word (case/space-insensitive).

Your rise-and-fall, read through the J-lens instead of the plain logit lens. Per prompt, same pass, no labels.

    z_l = lens_l(h_l)                       # plain: W g rms(h_l); J: W g rms(J_l h_l)
    score = min(relu(center(z_peak - z_early)), relu(center(z_peak - z_out)))   # z_out = model's own final logits

Peak layer chosen on translation, then scored unchanged on English v3/v4. Input-word filter only. — PI/OpenAI
"""
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
q, trajectory = g["q"], g["trajectory"]
RUNS = {"translation": "out/2026-09-30_125500_jlens-one-pass", "v3": "out/2026-09-30_125330_jlens-one-pass",
        "v4": "out/2026-09-30_142814_jlens-one-pass"}
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
NUMBER_WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
_groups = {}
word_id = torch.tensor([_groups.setdefault(v, len(_groups)) if v else _groups.setdefault(("tok", i), len(_groups))
                        for i, v in enumerate(vocab_norm)], device="cuda")


def word_max(z):
    return torch.full((len(_groups),), -torch.inf, device=z.device).scatter_reduce(0, word_id, z, "amax")[word_id]


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def lens(h, residual, use_j):
    h = h.float() @ J[residual - 1].cuda().float().T if use_j else h.float()
    return W @ (gain * rms(h))


def centered(z):
    return z - z.mean()


def rise_fall(z_early, z_peak, z_out):
    return torch.minimum(centered(z_peak - z_early).clamp_min(0), centered(z_peak - z_out).clamp_min(0))


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts, rows = {}, []
for set_name, run in RUNS.items():
    for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
        ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        h = {r: res[r][-1] for r in (22, 27, 29, 32)}
        z_out = lens(h[32], 32, False)
        scores = {"plain27": lens(h[27], 27, False), "J29": lens(h[29], 29, True),
                  "rise-fall plain 22/27/32": rise_fall(lens(h[22], 22, False), lens(h[27], 27, False), z_out)}
        for peak in (27, 29):
            scores[f"rise-fall J 22/{peak}/out"] = rise_fall(lens(h[22], 22, True), lens(h[peak], peak, True), z_out)
            scores[f"fall-only J {peak}/out"] = centered(lens(h[peak], peak, True) - z_out)
            scores[f"word rise-fall J 22/{peak}/out"] = rise_fall(lens(h[22], 22, True), lens(h[peak], peak, True), word_max(z_out))
            scores[f"word fall-only J {peak}/out"] = centered(lens(h[peak], peak, True) - word_max(z_out))
        mask = q.prompt_word_mask(ref["prompt"], vocab_norm, "cuda")
        aliases = tuple(ref["hidden_aliases"])
        if aliases not in label_counts:
            label_counts[aliases] = sum(any(hit(v, w) for w in aliases) for v in vocab)
        said = sorted(set(ref["answer_aliases"]) | set(ref["actual_words"])) if ref["intended_answer_observed"] else list(ref["actual_words"])
        said += [NUMBER_WORDS[w] for w in said if w in NUMBER_WORDS]
        for name, z in scores.items():
            top = [vocab[t] for t in z.masked_fill(mask, -torch.inf).topk(32).indices.tolist()]
            tp = sum(any(hit(t, w) for w in aliases) for t in top[:8])
            p, recall = tp / 8, tp / label_counts[aliases]
            rows.append({"set": set_name, "concept": ref["concept"], "method": name, "top32": top,
                         "F1@8": 0.0 if tp == 0 else 2 * p * recall / (p + recall), "found8": tp > 0,
                         "said8": any(any(hit(t, w) for w in said) for t in top[:8])})
Path("slop/audits/2026-10-02_word-rise-fall.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
summary = []
for set_name in RUNS:
    for name in dict.fromkeys(r["method"] for r in rows):
        sel = [r for r in rows if r["set"] == set_name and r["method"] == name]
        summary.append({"set": set_name, "method": name, "F1@8": mean(r["F1@8"] for r in sel),
                        "hidden in top8": f"{sum(r['found8'] for r in sel)}/{len(sel)}",
                        "said word in top8": f"{sum(r['said8'] for r in sel)}/{len(sel)}",
                        "hidden, not said": f"{sum(r['found8'] and not r['said8'] for r in sel)}/{len(sel)}"})
print(tabulate(summary, headers="keys", tablefmt="pipe", floatfmt=".3f"))
for r in rows:
    if r["concept"] in ("Sweden", "Thursday", "snake") and r["method"] in ("word rise-fall J 22/27/out", "word rise-fall J 22/29/out", "rise-fall J 22/27/out"):
        print(r["set"], r["method"], r["concept"], r["top32"][:8])
