"""Remove the 'will be said' component in residual space, then read the rest (oracle proposals, 2026-10-02).

    v = g * rms(x)                          # x = h27 (plain) or J28 h29 (J-lens), g = final-norm gain
    orth:     v_hat = v - (v.u) u,  u = unit(g * rms(h32))          # per prompt, no fitting (Gemini #1)
    residual: v_hat = g * (rms(x) - A rms(x)),  A = ridge(rms(x) -> rms(h32)) on 300 WikiText texts   # Fable #1
    readout = W_U v_hat

No labels; same pass. Ridge strength chosen on translation, then scored on English v3/v4. Input-word filter only. — PI/OpenAI
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
J28 = torch.load(LENS, weights_only=True, map_location="cpu")["J"][28].cuda().float()  # residual 29 -> final
NUMBER_WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}
RIDGE = (1e-3, 1e-1)  # times mean diagonal of X^T X / n
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]


def rms(h):
    h = h.float()
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def sources(res):
    return {"plain27": rms(res[27]), "J29": rms(res[29].float() @ J28.T)}


# offline ridge fit on generic text
texts = json.loads(Path(".local/wikitext2_train_300.json").read_text())["texts"]
d = W.shape[1]
xtx = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in ("plain27", "J29")}
xty = {k: torch.zeros(d, d, dtype=torch.float64, device="cuda") for k in ("plain27", "J29")}
n = 0
for text in texts:
    ids = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=128).input_ids.cuda()
    res, _ = trajectory(model, ids, model.model.norm)
    y = rms(res[32][8:]).double()
    for k, x in sources({r: res[r][8:] for r in (27, 29, 32)}).items():
        x = x.double(); xtx[k] += x.T @ x; xty[k] += x.T @ y
    n += y.shape[0]
A = {}
for k in xtx:
    scale = xtx[k].diagonal().mean()
    for lam in RIDGE:
        A[k, lam] = torch.linalg.solve(xtx[k] + lam * scale * torch.eye(d, dtype=torch.float64, device="cuda"), xty[k]).float()  # x @ A ~ y
print(f"ridge fit on {len(texts)} texts, {n} tokens", flush=True)


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts, rows = {}, []
for set_name, run in RUNS.items():
    for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
        ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        last = {r: res[r][-1] for r in (27, 29, 32)}
        u = gain * rms(last[32]); u = u / u.norm()
        scores = {}
        for k, x in sources(last).items():
            v = gain * x
            scores[k] = W @ v
            scores[f"{k} ⊥ h32"] = W @ (v - (v @ u) * u)
            for lam in RIDGE:
                scores[f"{k} − ridge→h32 λ={lam:g}"] = W @ (gain * (x - x @ A[k, lam]))
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
Path("slop/audits/2026-10-02_remove-said-readout.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
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
    if r["concept"] in ("cloud", "Sweden", "Thursday", "snake") and ("⊥" in r["method"] or "λ=0.1" in r["method"] or r["method"] == "J29"):
        print(r["set"], r["method"], r["concept"], r["top32"][:8])
