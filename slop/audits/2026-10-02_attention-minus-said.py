"""Attention output (layer 23, chosen on translation in 2765) minus what the model is about to say:
    score = p_attn23(t) - p_out(word(t)),  p_attn23 = softmax(W_U g rms(J_23 a_23)),  p_out = final next-token probs summed over same-spelling tokens.
No new selection; one pass, no labels.

Read the token-mixer output (attention or gated-delta-net) at the last prompt position: what was retrieved from
earlier positions, before the MLP computes the next step (Fable oracle #3, 2026-10-02).

    a_l = mixer_l(...)[-1]                    # block l's attention/linear-attention output, before it is added
    plain: W_U (g * rms(a_l));   J: W_U (g * rms(J_l a_l))

Layer and lens chosen on translation by F1@8, then scored on English v3/v4. One pass, no labels, input-word filter only. — PI/OpenAI
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
q = g["q"]
RUNS = {"translation": "out/2026-09-30_125500_jlens-one-pass", "v3": "out/2026-09-30_125330_jlens-one-pass",
        "v4": "out/2026-09-30_142814_jlens-one-pass"}
LAYERS = [23]
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


def word_sum(p):
    return torch.zeros(len(_groups), device=p.device).scatter_add(0, word_id, p)[word_id]
captured = {}


def capture(layer):
    def hook(_module, _args, output):
        captured[layer] = (output[0] if isinstance(output, tuple) else output)[0, -1].float()
    return hook


handles = []
for l in LAYERS:
    block = model.model.layers[l]
    mixer = block.linear_attn if hasattr(block, "linear_attn") else block.self_attn
    handles.append(mixer.register_forward_hook(capture(l)))


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts, rows = {}, []
try:
    for set_name, run in RUNS.items():
        for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
            captured.clear()
            ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            p_out = word_sum(model(input_ids=ids, use_cache=False).logits[0, -1].float().softmax(-1))
            assert sorted(captured) == list(LAYERS)
            scores = {}
            for l, a in captured.items():
                kind = "lin" if hasattr(model.model.layers[l], "linear_attn") else "attn"
                scores[f"{kind}{l} plain"] = W @ (gain * rms(a))
                scores[f"{kind}{l} J"] = W @ (gain * rms(a @ J[l].cuda().float().T))
                scores[f"{kind}{l} J minus said"] = scores[f"{kind}{l} J"].softmax(-1) - p_out
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
finally:
    for h in handles:
        h.remove()
Path("slop/audits/2026-10-02_attention-minus-said.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))


def summarize(set_name, name):
    sel = [r for r in rows if r["set"] == set_name and r["method"] == name]
    return {"set": set_name, "method": name, "F1@8": mean(r["F1@8"] for r in sel),
            "hidden in top8": f"{sum(r['found8'] for r in sel)}/{len(sel)}",
            "said word in top8": f"{sum(r['said8'] for r in sel)}/{len(sel)}",
            "hidden, not said": f"{sum(r['found8'] and not r['said8'] for r in sel)}/{len(sel)}"}


methods = list(dict.fromkeys(r["method"] for r in rows))
print(tabulate([summarize(s, m) for s in RUNS for m in methods], headers="keys", tablefmt="pipe", floatfmt=".3f"))
for r in rows:
    if r["method"] == "attn23 J minus said" and r["set"] != "translation":
        print(r["set"], r["concept"], "found" if r["found8"] else "-----", "SAID" if r["said8"] else "    ", r["top32"][:8])
