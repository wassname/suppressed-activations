"""Per-position "minus said" (after 2815: pooled lists were each position's own next-word guesses).
At each position subtract the model's own next-token probability there (same word), then take the max:
    score = max over positions of [ p_J(pos) - p_out(pos, word) ]
No labels, no language cue, one pass.

Readout over all prompt positions (after 2812: the bridge is J-readable at the first-hop entity's tokens in 24/36
readable cases, at the last token in only 12/62).

    p_l[pos] = softmax(W_U g rms(J_l h_l[pos]))       for every prompt position after the first 4 tokens
    score    = max over positions of p_l[pos]  -  p_out(word)          # p_out: final next-token probability, same word
Layer chosen on translation by F1@8 from {16, 20, 24, 28}, then scored unchanged on English v3/v4 and the 62 TwoHopFact
prompts. One pass, no labels, input-word filter only. — PI/OpenAI
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
LAYERS, SKIP = (20, 24, 26, 28, 30), 4
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


def word_sum(p):  # p: [..., vocab]
    flat = p.reshape(-1, p.shape[-1])
    sums = torch.zeros(flat.shape[0], len(_groups), device=p.device).scatter_add(1, word_id.expand_as(flat), flat)
    return sums[:, word_id].reshape(p.shape)


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


def items():
    for set_name, run in (("translation", "out/2026-09-30_125500_jlens-one-pass"), ("v3", "out/2026-09-30_125330_jlens-one-pass"),
                          ("v4", "out/2026-09-30_142814_jlens-one-pass")):
        for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
            said = sorted(set(ref["answer_aliases"]) | set(ref["actual_words"])) if ref["intended_answer_observed"] else list(ref["actual_words"])
            yield set_name, ref["prompt"], ref["concept"], ref["hidden_aliases"], said
    rows_csv = list(csv.DictReader(open("data/twohop/TwoHopFact.csv")))
    aliases = lambda row, e: [a for grp in ast.literal_eval(row[f"{e}.aliases"]) for a in grp] or [row[f"{e}.value"]]
    for case in json.loads(Path("out/2026-09-29_204246_twohop-english/result.json").read_text())["peak_any − prompt & output-layer words (dev winner)"]:
        row = [r for r in rows_csv if r["r2(r1(e1)).prompt"] == case["prompt"] and aliases(r, "e2")[0] == case["bridge"]][0]
        words = set(re.findall(r"\w+", case["prompt"].lower()))
        said = sorted(set(aliases(row, "e3")) | {w for w in re.findall(r"[^\W_]+", case["said_text"]) if len(w) >= 3})
        yield "twohop", case["prompt"], case["bridge"], [w for w in aliases(row, "e2") if w.lower() not in words], said


rows = []
for set_name, prompt, concept, hidden, said in items():
    said = said + [NUMBER_WORDS[w] for w in said if w in NUMBER_WORDS]
    ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    out = model(input_ids=ids, use_cache=False, output_hidden_states=True)
    p_out_pos = word_sum(out.logits[0, SKIP:].float().softmax(-1))  # [pos, vocab]
    mask = q.prompt_word_mask(prompt, vocab_norm, "cuda")
    for layer in LAYERS:
        h = out.hidden_states[layer][0, SKIP:].float()
        p = (W @ (gain * rms(h @ J[layer - 1].cuda().float().T)).T).T.softmax(-1)  # [pos, vocab]
        for name, s in ((f"position-max J{layer} minus own next word", (p - p_out_pos).max(0).values),):
            top = [vocab[t] for t in s.masked_fill(mask, -torch.inf).topk(8).indices.tolist()]
            found = any(any(hit(t, w) for w in hidden) for t in top)
            rows.append({"set": set_name, "concept": concept, "method": name, "top8": top, "found8": found,
                         "said8": any(any(hit(t, w) for w in said) for t in top), "scorable": bool(hidden)})
Path("slop/audits/2026-10-02_position-minus-next.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
summary = []
for set_name in ("translation", "v3", "v4", "twohop"):
    for name in dict.fromkeys(r["method"] for r in rows):
        sel = [r for r in rows if r["set"] == set_name and r["method"] == name]
        summary.append({"set": set_name, "method": name, "hidden in top8": f"{sum(r['found8'] for r in sel)}/{len(sel)}",
                        "said word in top8": f"{sum(r['said8'] for r in sel)}/{len(sel)}",
                        "hidden, not said": f"{sum(r['found8'] and not r['said8'] for r in sel)}/{len(sel)}"})
print(tabulate(summary, headers="keys", tablefmt="pipe"))
best = max((r for r in summary if r["set"] == "translation"), key=lambda r: int(r["hidden, not said"].split("/")[0]))["method"]
print("chosen on translation (hidden, not said):", best)
for r in rows:
    if r["method"] == best and r["set"] != "translation" and r["concept"] in ("Sweden", "Thursday", "snake", "Bulgaria", "Iceland", "Hungary"):
        print(r["set"], r["concept"], "found" if r["found8"] else "-----", "SAID" if r["said8"] else "    ", r["top8"])
