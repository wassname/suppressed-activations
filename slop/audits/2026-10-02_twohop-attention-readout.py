"""Frozen attention-output readout on the 62 TwoHopFact prompts saved by job 2499 (not used to choose this method).

Methods, all with the input-word filter only: plain27, J29, rise-and-fall J 22/27/out, attn23 J, attn23 J minus said
(p_attn23 - final next-token probability of the same word). Layer 23 was chosen on translation (2765).
Hidden = TwoHopFact bridge aliases; said = answer aliases + words of the model's own continuation. — PI/OpenAI
"""
import ast
import csv
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
q = g["q"]
CASES = json.loads(Path("out/2026-09-29_204246_twohop-english/result.json").read_text())["peak_any − prompt & output-layer words (dev winner)"]
assert len(CASES) == 62
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
_groups = {}
word_id = torch.tensor([_groups.setdefault(v, len(_groups)) if v else _groups.setdefault(("tok", i), len(_groups))
                        for i, v in enumerate(vocab_norm)], device="cuda")

rows_csv = list(csv.DictReader(open("data/twohop/TwoHopFact.csv")))


def aliases(row, entity):
    return [a for group in ast.literal_eval(row[f"{entity}.aliases"]) for a in group] or [row[f"{entity}.value"]]


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def jlens(h, residual):
    return W @ (gain * rms(h.float() @ J[residual - 1].cuda().float().T))


def word_sum(p):
    return torch.zeros(len(_groups), device=p.device).scatter_add(0, word_id, p)[word_id]


def centered(z):
    return z - z.mean()


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


captured = {}
block = model.model.layers[23]
handle = block.self_attn.register_forward_hook(lambda _m, _a, out: captured.__setitem__(23, out[0][0, -1].float()))
rows = []
try:
    for case in CASES:
        match = [r for r in rows_csv if r["r2(r1(e1)).prompt"] == case["prompt"] and aliases(r, "e2")[0] == case["bridge"]]
        assert match, case["prompt"]
        bridge, answer = aliases(match[0], "e2"), aliases(match[0], "e3")
        prompt_words = set(re.findall(r"\w+", case["prompt"].lower()))
        hidden = [w for w in bridge if w.lower() not in prompt_words]
        said = sorted(set(answer) | {w for w in re.findall(r"[^\W_]+", case["said_text"]) if len(w) >= 3})
        ids = tok(case["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        out = model(input_ids=ids, use_cache=False, output_hidden_states=True)
        hs = out.hidden_states
        z_out = out.logits[0, -1].float()
        z = {r: jlens(hs[r][0, -1], r) for r in (22, 27, 29)}
        rise, fall = centered(z[27] - z[22]), centered(z[27] - z_out)
        scores = {"plain27": W @ (gain * rms(hs[27][0, -1].float())), "J29": z[29],
                  "rise-fall J 22/27/out": torch.minimum(rise.clamp_min(0), fall.clamp_min(0)),
                  "attn23 J": jlens(captured[23], 24)}  # J[23] maps block 23's output
        scores["attn23 J minus said"] = scores["attn23 J"].softmax(-1) - word_sum(z_out.softmax(-1))
        mask = q.prompt_word_mask(case["prompt"], vocab_norm, "cuda")
        for name, s in scores.items():
            top = [vocab[t] for t in s.masked_fill(mask, -torch.inf).topk(8).indices.tolist()]
            found = any(any(hit(t, w) for w in hidden) for t in top)
            leak = any(any(hit(t, w) for w in said) for t in top)
            rows.append({"category": case["category"], "prompt": case["prompt"], "bridge": case["bridge"], "answer": case["answer"],
                         "two_hop_correct": case["two_hop_correct"], "hidden_scorable": bool(hidden), "method": name,
                         "top8": top, "found8": found, "said8": leak})
finally:
    handle.remove()
Path("slop/audits/2026-10-02_twohop-attention-readout.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
summary = []
for subset, keep in (("all 62", lambda r: True), ("answer correct", lambda r: r["two_hop_correct"])):
    for name in dict.fromkeys(r["method"] for r in rows):
        sel = [r for r in rows if r["method"] == name and keep(r)]
        summary.append({"subset": subset, "method": name, "hidden in top8": f"{sum(r['found8'] for r in sel)}/{len(sel)}",
                        "said word in top8": f"{sum(r['said8'] for r in sel)}/{len(sel)}",
                        "hidden, not said": f"{sum(r['found8'] and not r['said8'] for r in sel)}/{len(sel)}"})
print(tabulate(summary, headers="keys", tablefmt="pipe"))
print("unscorable (bridge words all in prompt):", sum(not r["hidden_scorable"] for r in rows) // 5)
for r in rows[:5 * 62]:
    if r["method"] == "attn23 J minus said" and r["two_hop_correct"]:
        print(f"{r['bridge'][:18]:18s} -> {r['answer'][:14]:14s}", "found" if r["found8"] else "-----", "SAID" if r["said8"] else "    ", r["top8"])
