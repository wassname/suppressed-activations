"""Transform scoreboard: F1 of fixed readout transforms for "thought but not said", no masks, no language lookups.

Every candidate maps one forward pass to a score per vocabulary token. We keep its top 8 distinct words
(case and space variants share a slot) and score them.
Translation between distant languages (Russian, Korean, Arabic, Hindi, Thai; MUSE dictionary words, 4-shot) is the
labelled scoreboard: hidden = English and Chinese words for the meaning; said = any token in the output language's Unicode
script, every dictionary translation, and the model's actual next token; input = any token in the input language's script.
Prompts where the model's next token is whitespace or punctuation are skipped and counted (prompt format problem).

    readout(v) = W_U (g * rms(v))                              # the model's own output head
    P = hidden words in the top 8 / 8;  R = hidden languages (English, Chinese) found / 2
    unsaid F1 = 2PR/(P+R), or 0 if a said or input token is in the top 8; mean over prompts

"Minus output subspace": remove the top-r principal directions of the final residual on 300 WikiText texts (a fixed
projection), then read through the plain lens or J-lens.

Hyperparameters (layer, rank) are chosen per family on the dev pair only, then frozen for the test pairs and the English
transfer sets. Nothing uses English/Chinese token lists except scoring. — PI/OpenAI
"""
import ast
import csv
import hashlib
import json
from pathlib import Path
import random
import re
import runpy
import time
from statistics import mean

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
ROOT = Path(__file__).resolve().parents[2]
g = runpy.run_path(str(ROOT / "scripts/english/08_jlens_one_pass.py"))["main"].__globals__
q, s4 = g["q"], g["s4"]
from suppressed_activation_subspace import subspace_from_scores, suppressed_activation_scores  # noqa: E402

K, PER_PAIR = 8, 20
DEV, TEST = [("ru", "ko")], [("ar", "hi"), ("hi", "th"), ("th", "ru"), ("ko", "ar")]  # no script shared with English/Chinese
LANG_NAME = {"ru": "Русский", "ko": "한국어", "ar": "العربية", "hi": "हिन्दी", "th": "ไทย"}
MIN_CHARS = {"ru": 3, "ko": 2, "ar": 2, "hi": 2, "th": 2}
SCRIPT = {"ru": "\u0400-\u04ff", "ko": "\u1100-\u11ff\u3130-\u318f\uac00-\ud7af", "ar": "\u0600-\u06ff\u0750-\u077f",
          "hi": "\u0900-\u097f", "th": "\u0e00-\u0e7f"}  # Unicode blocks; no two languages share one
LAYERS, RANKS = range(20, 32), (64, 256, 1024)
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
out_dir = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_transform-scoreboard"
out_dir.mkdir(parents=True)

tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"]
Jc = {l: J[l - 1].cuda().float() for l in list(LAYERS) + [22, 24]}  # residual l -> final
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
d = W.shape[1]


def rms(h):
    return h.float() * torch.rsqrt(h.float().square().mean(-1, keepdim=True) + 1e-6)


by_norm = {}
for t, v in enumerate(vocab):
    if v.strip():
        by_norm.setdefault(v.strip().lower(), []).append(t)


def label(word, min_chars=3):  # same tokens as q.is_prefix_hit: normalised token is a prefix of the word, long enough
    w = word.lower()
    return frozenset(t for i in range(min(min_chars, len(w)), len(w) + 1) for t in by_norm.get(w[:i], []))


raw_final = {}
model.model.norm.register_forward_pre_hook(lambda _m, args: raw_final.__setitem__("h", args[0]))


def hidden_states(ids):
    out = model(input_ids=ids, use_cache=False, output_hidden_states=True)
    return out, list(out.hidden_states[:-1]) + [raw_final["h"]]  # residuals 0..32, 32 = before final norm


def orth(m):
    return torch.linalg.qr(m, mode="reduced").Q


# ---- fixed bases, built once from weights or generic text (no prompts, no labels) ----
bases = {}
G = torch.zeros(d, d, dtype=torch.float64, device="cuda")
for chunk in (W * gain).split(16384):
    G += (chunk.T @ chunk).double()
evals, evecs = torch.linalg.eigh(G)  # ascending
for r in RANKS:
    bases[("weak-readout", 0, r)] = evecs[:, :r].float().cuda()  # directions the output head reads least
noise = torch.randn(d, max(RANKS), generator=torch.Generator().manual_seed(0)).cuda()
for r in RANKS:
    bases[("random subspace (floor)", 27, r)] = orth(noise[:, :r])  # same rank, no structure
for l in (24, 27, 29):
    down = model.model.layers[l - 1].mlp.down_proj.weight.float()            # [d, m] writes residual l
    reads = torch.cat([model.model.layers[l].mlp.up_proj.weight.float(), model.model.layers[l].mlp.gate_proj.weight.float()])  # [2m, d]
    Uw = torch.linalg.svd(down, full_matrices=False).U
    Vr = torch.linalg.svd(reads, full_matrices=False).Vh.T
    for r in RANKS:
        write = Uw[:, :r]
        bases[("write-not-read", l, r)] = orth(write - Vr[:, :r] @ (Vr[:, :r].T @ write))
texts = json.loads((ROOT / ".local/wikitext2_train_300.json").read_text())["texts"]
cov = {key: torch.zeros(d, d, dtype=torch.float64, device="cuda") for key in ("x27", "x32", "d24", "d27", "d29", "supp")}
sums = {key: torch.zeros(d, dtype=torch.float64, device="cuda") for key in cov}
n = 0
for text in texts:
    ids = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=128).input_ids.cuda()
    _, hs = hidden_states(ids)
    x = {l: rms(hs[l][0, 8:]).double() for l in (24, 25, 27, 28, 29, 30, 32)}
    # AntiPaSTO "suppressed" primitive: per coordinate, magnitude added in some layers and removed in others
    mag = torch.stack([rms(hs[l][0, 8:]).abs() for l in range(1, 33)]).double()   # [layers, tok, d]
    step = mag[1:] - mag[:-1]
    supp = torch.minimum(step.clamp_min(0).sum(0), (-step).clamp_min(0).sum(0))   # [tok, d]
    for key, v in (("x27", x[27]), ("x32", x[32]), ("d24", x[25] - x[24]), ("d27", x[28] - x[27]), ("d29", x[30] - x[29]), ("supp", supp)):
        cov[key] += v.T @ v; sums[key] += v.sum(0)
    n += x[27].shape[0]
C = {key: cov[key] / n - torch.outer(sums[key] / n, sums[key] / n) for key in cov}
for l in (24, 27, 29):
    vecs = torch.linalg.eigh(C[f"d{l}"])[1].flip(-1).float()
    for r in RANKS:
        bases[("churn", l, r)] = vecs[:, :r]  # largest layer-to-layer change on generic text
vecs = torch.linalg.eigh(C["x27"] - C["x32"])[1].flip(-1).float()
for r in RANKS:
    bases[("erased-variance", 27, r)] = vecs[:, :r]  # variance at 27 that is gone by 32 (generic text)
vecs = torch.linalg.eigh(C["supp"])[1].flip(-1).float()
for r in RANKS:
    bases[("AntiPaSTO suppressed (WikiText)", 27, r)] = vecs[:, :r]  # pca(min(increases, decreases)) per README
out_vecs = torch.linalg.eigh(C["x32"])[1].flip(-1).float()
OUT_RANKS = (16, 64, 256)
remove_output = {r: out_vecs[:, :r] for r in OUT_RANKS}  # main directions of the final residual on generic text: "what gets said"
print(f"fixed bases from weights and {len(texts)} WikiText texts ({n} tokens): {len(bases)}", flush=True)

# ---- data ----
lists = json.loads((ROOT / "data/muse/word_lists.json").read_text())["words"]  # from 11_dictionary_word_lists.py
in_script = {l: frozenset(t for t, v in enumerate(vocab) if re.search(f"[{r}]", v)) for l, r in SCRIPT.items()}


def translation_items(pairs, role):
    for src, tgt in pairs:
        words = sorted(w for w, e in lists.items() if src in e and tgt in e)
        random.Random(0).shuffle(words)
        shots, targets = words[:4], words[4:4 + PER_PAIR]
        head = "".join(f'{LANG_NAME[src]}: "{lists[w][src]["canonical"]}" - {LANG_NAME[tgt]}: "{lists[w][tgt]["canonical"]}"\n' for w in shots)
        for w in targets:
            prompt = head + f'{LANG_NAME[src]}: "{lists[w][src]["canonical"]}" - {LANG_NAME[tgt]}: "'
            # any token in the output (input) language's script counts as said (input), plus the dictionary forms
            said = in_script[tgt] | frozenset().union(*(label(a, MIN_CHARS[tgt]) for a in lists[w][tgt]["aliases"]))
            inp = in_script[src] | frozenset().union(*(label(a, MIN_CHARS[src]) for a in lists[w][src]["aliases"]))
            groups = [label(w) - said - inp, label(lists[w]["zh"], 1) - said - inp]  # hidden: English, Chinese
            yield role, f"{src}→{tgt}", prompt, w, [g for g in groups if g], said, inp


def english_items():
    sets = {"English v3": "out/2026-09-30_125330_jlens-one-pass", "English v4": "out/2026-09-30_142814_jlens-one-pass"}
    for name, run in sets.items():
        for ref in [r for r in json.loads((ROOT / run / "readout.json").read_text()) if r["method"] == "end-pass plain27"]:
            said_words = set(ref["answer_aliases"]) | set(ref["actual_words"]) if ref["intended_answer_observed"] else set(ref["actual_words"])
            yield from english_item(name, ref["prompt"], ref["concept"], ref["hidden_aliases"], said_words)
    rows_csv = list(csv.DictReader(open(ROOT / "data/twohop/TwoHopFact.csv")))
    aliases = lambda row, e: [a for grp in ast.literal_eval(row[f"{e}.aliases"]) for a in grp] or [row[f"{e}.value"]]
    for case in json.loads((ROOT / "out/2026-09-29_204246_twohop-english/result.json").read_text())["peak_any − prompt & output-layer words (dev winner)"]:
        row = [r for r in rows_csv if r["r2(r1(e1)).prompt"] == case["prompt"] and aliases(r, "e2")[0] == case["bridge"]][0]
        said_words = set(aliases(row, "e3")) | {w for w in re.findall(r"[^\W_]+", case["said_text"]) if len(w) >= 3}
        yield from english_item("TwoHopFact", case["prompt"], case["bridge"], aliases(row, "e2"), said_words)


NUMBER = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}


def english_item(name, prompt, concept, hidden_words, said_words):
    said_words = set(said_words) | {NUMBER[w] for w in said_words if w in NUMBER}
    prompt_words = {w for w in re.findall(r"\w+", prompt) if len(w) >= 3}
    hidden = frozenset().union(*[label(w) for w in hidden_words if w.lower() not in {p.lower() for p in prompt_words}] or [frozenset()])
    said = frozenset().union(*[label(w) for w in said_words] or [frozenset()])
    inp = frozenset().union(*[label(w) for w in prompt_words] or [frozenset()])
    hidden = hidden - said - inp
    if hidden:
        yield "transfer", name, prompt, concept, [hidden], said, inp - hidden


# ---- candidates: one forward, every family and setting ----
captured = {}
hook = model.model.layers[23].self_attn.register_forward_hook(lambda _m, _a, o: captured.__setitem__("a23", o[0][0, -1]))


def candidates(prompt):
    ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    out, hs = hidden_states(ids)
    h = {l: hs[l][0, -1].float() for l in range(33)}
    z_out = out.logits[0, -1].float()
    next_token = int(z_out.argmax())
    vecs, names = [], []
    for l in LAYERS:
        vecs.append(rms(h[l])); names.append(("plain lens", l, 0))
        vecs.append(rms(h[l] @ Jc[l].T)); names.append(("J-lens", l, 0))
    x27 = rms(h[27])
    for (fam, l, r), B in bases.items():
        x = rms(h[l if l else 27])
        vecs.append(B @ (B.T @ x)); names.append((fam, l if l else 27, r))
    rf_scores = suppressed_activation_scores(torch.stack([h[l] for l in range(33)])[None], W, gain, early_layer=22, peak_layer=27, output_layer=32)[0]
    S, _ = subspace_from_scores(rf_scores[None], W, gain, rank=32)
    vecs.append(S[0] @ (S[0].T @ x27)); names.append(("your suppressed subspace (rank 32)", 27, 32))
    for l in (26, 28, 30):
        for r, B in remove_output.items():
            x = rms(h[l]); xj = rms(h[l] @ Jc[l].T)
            vecs.append(x - B @ (B.T @ x)); names.append(("plain lens minus output subspace", l, r))
            vecs.append(xj - B @ (B.T @ xj)); names.append(("J-lens minus output subspace", l, r))
    vecs.append(rms(captured["a23"].float() @ Jc[24].T)); names.append(("attention output, J-lens", 23, 0))
    z = (torch.stack(vecs) * gain) @ W.T                         # [candidates, vocab]
    scores = {name: zz for name, zz in zip(names, z)}
    scores[("your rise-and-fall, plain", 27, 0)] = rf_scores
    for peak in (26, 27, 28, 29):
        zj = lambda l: W @ (gain * rms(h[l] @ Jc[l].T))
        rise, fall = zj(peak) - zj(22), zj(peak) - z_out
        rf_j = torch.minimum((rise - rise.mean()).clamp_min(0), (fall - fall.mean()).clamp_min(0))
        scores[("rise-and-fall through J-lens", peak, 0)] = rf_j
        # your rank-32 subspace, built from the J-lens rise-and-fall scores and read in J-lens space
        Sj, _ = subspace_from_scores(rf_j[None], W, gain, rank=32)
        xj = rms(h[peak] @ Jc[peak].T)
        scores[("your suppressed subspace via J-lens (rank 32)", peak, 32)] = W @ (gain * (Sj[0] @ (Sj[0].T @ xj)))
    return scores, next_token


def top_words(s):
    """Top K distinct words: case and surrounding-space variants of one string share a slot."""
    kept, seen = [], set()
    for t in s.topk(256).indices.tolist():
        key = vocab[t].strip().lower()
        if key not in seen:
            seen.add(key); kept.append(t)
        if len(kept) == K:
            break
    return kept


def score(top, groups, said, inp):
    hidden = frozenset().union(*groups)
    p = sum(t in hidden for t in top) / K                  # share of the K slots holding a hidden word
    r = sum(bool(set(top) & g) for g in groups) / len(groups)  # share of hidden languages (English, Chinese) found
    f1 = 0.0 if p == 0 else 2 * p * r / (p + r)
    leak_said, leak_input = bool(set(top) & said), bool(set(top) & inp)
    return {"F1": f1, "P": p, "R": r, "hit": p > 0, "said": leak_said, "input": leak_input,
            "unsaid_F1": 0.0 if leak_said or leak_input else f1, "pass": p > 0 and not leak_said and not leak_input}


results, skipped = [], []  # one row per (item, candidate)
for item in list(translation_items(DEV, "dev")) + list(translation_items(TEST, "test")) + list(english_items()):
    role, split, prompt, concept, groups, said, inp = item
    scores, next_token = candidates(prompt)
    if not re.search(r"\w", vocab[next_token]):  # the model is about to emit whitespace or punctuation: prompt format problem
        skipped.append({"split": split, "concept": concept, "next_token": vocab[next_token]})
        continue
    model_correct = next_token in said
    said = said | {next_token}  # whatever the model actually says next is spoken
    for name, s in scores.items():
        top = top_words(s)
        results.append({"role": role, "split": split, "concept": concept, "family": name[0], "layer": name[1], "rank": name[2],
                        "next_token": vocab[next_token], "model_correct": model_correct,
                        "top8": [vocab[t] for t in top], **score(top, groups, said, inp)})
print(f"skipped for formatting (next token is whitespace/punctuation): {len(skipped)}", skipped[:10], flush=True)
(out_dir / "skipped.json").write_text(json.dumps(skipped, ensure_ascii=False, indent=1))
hook.remove()
(out_dir / "rows.json").write_text(json.dumps(results, ensure_ascii=False))

# ---- choose each family's setting on the dev pair only, then report it everywhere ----
def mean_of(rows, key):
    return mean(r[key] for r in rows) if rows else float("nan")


families = list(dict.fromkeys(r["family"] for r in results))
chosen = {}
for fam in families:
    settings = sorted({(r["layer"], r["rank"]) for r in results if r["family"] == fam})
    dev = {s: [r for r in results if r["family"] == fam and (r["layer"], r["rank"]) == s and r["role"] == "dev"] for s in settings}
    chosen[fam] = max(settings, key=lambda s: (round(mean_of(dev[s], "unsaid_F1"), 6), -s[0], -s[1]))
splits = {"dev": [f"{a}→{b}" for a, b in DEV], "test": [f"{a}→{b}" for a, b in TEST], "English v3": ["English v3"],
          "English v4": ["English v4"], "TwoHopFact": ["TwoHopFact"]}
table = []
for fam in families:
    l, r = chosen[fam]
    row = {"transform": fam, "setting (chosen on dev)": f"layer {l}" + (f", rank {r}" if r else "")}
    for col, keys in splits.items():
        sel = [x for x in results if x["family"] == fam and (x["layer"], x["rank"]) == (l, r) and x["split"] in keys]
        row[f"{col} unsaid F1"] = mean_of(sel, "unsaid_F1")
        row[f"{col} pass"] = f"{sum(x['pass'] for x in sel)}/{len(sel)}"
    table.append(row)
table.sort(key=lambda r: -r["test unsaid F1"])
md = tabulate(table, headers="keys", tablefmt="pipe", floatfmt=".3f")
said_table = tabulate([{"transform": fam, **{f"{col} said in top8": f"{sum(x['said'] for x in results if x['family'] == fam and (x['layer'], x['rank']) == chosen[fam] and x['split'] in keys)}/"
                                                                 f"{sum(1 for x in results if x['family'] == fam and (x['layer'], x['rank']) == chosen[fam] and x['split'] in keys)}"
                                            for col, keys in splits.items()}} for fam in families], headers="keys", tablefmt="pipe")
(out_dir / "run.md").write_text(f"# Transform scoreboard\n\n— PI/OpenAI. No masks; top {K} distinct words. Settings chosen on {DEV} only.\n\n{md}\n\nSpoken word in top 8:\n\n{said_table}\n")
print(md, "\n", said_table, f"\nrun.md: {out_dir / 'run.md'}", flush=True)
