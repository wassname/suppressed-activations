"""Where is the bridge entity readable? Diagnostic upper bound, not a readout method (uses the labels to locate).
TwoHopFact prompts from 2499, J-lens at every position and layers 12-31, input-word filter. For each prompt: best rank of
any bridge-alias token, and where (last token / inside the first-hop entity's name / elsewhere). — PI/OpenAI"""
import ast
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import runpy

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
g = runpy.run_path("scripts/english/08_jlens_one_pass.py")["main"].__globals__
q = g["q"]
CASES = json.loads(Path("out/2026-09-29_204246_twohop-english/result.json").read_text())["peak_any − prompt & output-layer words (dev winner)"]
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
rows_csv = list(csv.DictReader(open("data/twohop/TwoHopFact.csv")))
LAYERS = range(12, 32)


def aliases(row, entity):
    return [a for group in ast.literal_eval(row[f"{entity}.aliases"]) for a in group] or [row[f"{entity}.value"]]


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


out = []
for case in CASES:
    row = [r for r in rows_csv if r["r2(r1(e1)).prompt"] == case["prompt"] and aliases(r, "e2")[0] == case["bridge"]][0]
    prompt_words = set(re.findall(r"\w+", case["prompt"].lower()))
    hidden = [w for w in aliases(row, "e2") if w.lower() not in prompt_words]
    label = torch.tensor([any(hit(v, w) for w in hidden) for v in vocab], device="cuda")
    e1 = row["e1.value"]
    start = case["prompt"].find(e1)
    enc = tok(case["prompt"], return_offsets_mapping=True, add_special_tokens=False)
    span = {i for i, (a, b) in enumerate(enc["offset_mapping"]) if start >= 0 and a < start + len(e1) and b > start}
    ids = torch.tensor([enc["input_ids"]]).cuda()
    hs = model(input_ids=ids, use_cache=False, output_hidden_states=True).hidden_states
    mask = q.prompt_word_mask(case["prompt"], vocab_norm, "cuda")
    best = (10**9, None, None)
    last_best = 10**9
    for layer in LAYERS:
        z = (W @ (gain * rms(hs[layer][0].float() @ J[layer - 1].cuda().float().T)).T).T.masked_fill(mask, -torch.inf)  # [pos, vocab]
        top_label = z.masked_fill(~label, -torch.inf).max(-1).values
        ranks = (z > top_label[:, None]).sum(-1)
        for pos, r in enumerate(ranks.tolist()):
            if r < best[0]:
                best = (r, layer, pos)
        last_best = min(last_best, int(ranks[-1]))
    r, layer, pos = best
    where = "last token" if pos == ids.shape[1] - 1 else ("first-hop entity" if pos in span else "elsewhere")
    out.append({"prompt": case["prompt"], "bridge": case["bridge"], "correct": case["two_hop_correct"], "best_rank": r,
                "best_layer": layer, "best_position": pos, "where": where, "token": tok.decode([int(ids[0, pos])]),
                "last_token_best_rank": last_best, "e1": e1})
Path("slop/audits/2026-10-02_twohop-bridge-location.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for subset, keep in (("all 62", lambda r: True), ("answer correct", lambda r: r["correct"])):
    sel = [r for r in out if keep(r)]
    print(f"{subset}: bridge in top 8 anywhere {sum(r['best_rank'] < 8 for r in sel)}/{len(sel)}; "
          f"at last token (any layer) {sum(r['last_token_best_rank'] < 8 for r in sel)}/{len(sel)}; "
          f"best location {dict(Counter(r['where'] for r in sel if r['best_rank'] < 8))}; "
          f"best layers {sorted(Counter(r['best_layer'] for r in sel if r['best_rank'] < 8).items())}", flush=True)
print(tabulate([{k: r[k] for k in ("bridge", "correct", "best_rank", "best_layer", "where", "token", "last_token_best_rank")} for r in out],
               headers="keys", tablefmt="pipe"))
