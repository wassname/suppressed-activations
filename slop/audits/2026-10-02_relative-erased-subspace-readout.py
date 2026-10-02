"""Relative version (after 2748: absolute variance picked punctuation/format directions).
Generalised eigenproblem Cov(y) v = lambda Cov(x) v; smallest lambda = directions where layer 32 keeps the smallest
FRACTION of layer-27 variance. Span orthonormalised by QR before projecting.

Fixed 'erased by late layers' subspace, learned once on generic WikiText with no labels, then read through the output layer.

    x = rms(h27), y = rms(h32)  (RMS-normalised residuals at the same token)
    S_k = top-k eigenvectors of Cov(x) - Cov(y)   # variance present at layer 27 that is gone by layer 32
    C_k = top-k eigenvectors of -sym Cov(x, y - x)   # directions the late-layer change cancels; ignores newly written variance
    readout(h) = W @ (g * S_k S_k^T (x - mu_x))

Same S for every prompt and task. k is chosen on translation, then the same S is scored on English v3/v4.
Only the prompt-word filter is applied, to every method; no output-word mask. — PI/OpenAI
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
EARLY, LATE, N_TEXTS, SKIP = 27, 32, 300, 8
KS = (16, 64, 256, 1024)
RUNS = {"translation": "out/2026-09-30_125500_jlens-one-pass", "v3": "out/2026-09-30_125330_jlens-one-pass",
        "v4": "out/2026-09-30_142814_jlens-one-pass"}
WIKI = Path(".local/wikitext2_train_300.json")  # WikiText-2 train @b08601e, first 300 lines >400 chars
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
NUMBER_WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}

tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight, 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]


def rms(h):
    h = h.float()
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


# offline fit on generic text: no prompts, no labels
texts = json.loads(WIKI.read_text())["texts"][:N_TEXTS]
assert len(texts) == N_TEXTS
d = W.shape[1]
sx, sy = torch.zeros(d, dtype=torch.float64, device="cuda"), torch.zeros(d, dtype=torch.float64, device="cuda")
sxx, syy, sxy = (torch.zeros(d, d, dtype=torch.float64, device="cuda") for _ in range(3))
n = 0
for text in texts:
    ids = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=128).input_ids.cuda()
    res, _ = trajectory(model, ids, model.model.norm)
    x, y = rms(res[EARLY][SKIP:]).double(), rms(res[LATE][SKIP:]).double()
    sx += x.sum(0); sy += y.sum(0); sxx += x.T @ x; syy += y.T @ y; sxy += x.T @ y; n += x.shape[0]
mu_x, mu_y = sx / n, sy / n
cov_x, cov_y = sxx / n - torch.outer(mu_x, mu_x), syy / n - torch.outer(mu_y, mu_y)
cov_xy = sxy / n - torch.outer(mu_x, mu_y)


def top_eig(matrix):
    values, vectors = torch.linalg.eigh(matrix)
    order = values.argsort(descending=True)
    return values[order], vectors[:, order].float()


L = torch.linalg.cholesky(cov_x + 1e-6 * cov_x.diagonal().mean() * torch.eye(d, dtype=cov_x.dtype, device="cuda"))
Linv = torch.linalg.inv(L)
ratio, U = torch.linalg.eigh(Linv @ cov_y @ Linv.T)  # ascending: smallest kept fraction first
eigvals = ratio
eigvecs = torch.linalg.qr((Linv.T @ U).float())[0]  # nested spans: first k columns span the k most-erased directions
cross = Linv @ ((cov_xy + cov_xy.T) / 2) @ Linv.T
cancel_vals, cancel_U = torch.linalg.eigh(cross)  # ascending: most cancelled (negative carry-over) first
cancel_vecs = torch.linalg.qr((Linv.T @ cancel_U).float())[0]
print(f"kept-variance ratio, smallest: {ratio[:5].tolist()}; carry-over, smallest: {cancel_vals[:5].tolist()}", flush=True)
print(f"fit: {len(texts)} texts, {n} tokens; top eigenvalues {eigvals[:5].tolist()}; positive count {(eigvals > 0).sum().item()}/{d}", flush=True)
torch.save({"mu_x": mu_x.float().cpu(), "eigvals": eigvals.cpu(), "eigvecs": eigvecs[:, :max(KS)].cpu(), "cancel_vals": cancel_vals.cpu(), "cancel_vecs": cancel_vecs[:, :max(KS)].cpu(), "n_tokens": n,
            "layers": (EARLY, LATE), "texts_sha256": hashlib.sha256("\n".join(texts).encode()).hexdigest()},
           "slop/audits/2026-10-02_relative-erased-subspace.pt")
# what the subspace means on its own: top tokens of the leading directions
for i in range(3):
    z = W.float() @ (gain * eigvecs[:, i])
    print(f"direction {i}: +{[vocab[t] for t in z.topk(8).indices.tolist()]}  -{[vocab[t] for t in (-z).topk(8).indices.tolist()]}", flush=True)


def hit(token, word):
    t = token.strip().lower()
    return bool(t) and len(t) >= min(3, len(word)) and word.lower().startswith(t)


label_counts, rows = {}, []
for set_name, run in RUNS.items():
    for ref in [r for r in json.loads((Path(run) / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
        ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        mask = q.prompt_word_mask(ref["prompt"], vocab_norm, "cuda")
        x = rms(res[EARLY][-1])
        scores = {"plain27": W.float() @ (gain * x), "J29": W.float() @ (gain * rms(res[29][-1].float() @ J[28].cuda().float().T))}
        for k in KS:
            S = eigvecs[:, :k]
            scores[f"erased-S k={k}"] = W.float() @ (gain * (S @ (S.T @ (x - mu_x.float()))))
            C = cancel_vecs[:, :k]
            scores[f"cancel-C k={k}"] = W.float() @ (gain * (C @ (C.T @ (x - mu_x.float()))))
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
Path("slop/audits/2026-10-02_relative-erased-subspace-readout.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
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
    if r["method"] in ("plain27", "erased-S k=64", "erased-S k=256", "cancel-C k=64") and r["concept"] in ("cloud", "Sweden", "Thursday"):
        print(r["set"], r["method"], r["concept"], r["top32"][:8])
