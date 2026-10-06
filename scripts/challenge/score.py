"""Score every transform and write the leaderboard. One GPU, about 7 minutes.

Translation between languages that share no script with English or Chinese. The model thinks in English (and Qwen
perhaps Chinese); it reads one language and writes another. For each prompt we keep a transform's top 8 distinct words
(case and space variants share a slot) at the last prompt token:

    TP = the hidden word (English, or its Chinese translation) is in the top 8, else FN
    FP = a top-8 word is in the input or output language (script), or is the model's next word, else TN
    F1 = 2TP / (2TP + FP + FN), with counts over prompts

Each transform's setting is chosen on the dev pair by F1, then frozen for the test pairs and for transfer:
English-only two-hop questions (TwoHopFact), where the hidden word is the bridge entity.
Usage: uv run scripts/challenge/make_word_lists.py (once), then uv run scripts/challenge/score.py — PI/OpenAI
"""
import gzip
import inspect
import json
import subprocess
import time
from statistics import mean

from tabulate import tabulate

from common import ROOT
from transforms import TRANSFORMS, fit_bases
from bench import (DEV, TEST, delta_ci, f1, f1_ci, judge, prepare, read_vector, transfer_prompts,
                   translation_prompts)

fit_bases()

def evaluate(item, settings_of):
    """Score one prompt for every transform under the given settings; returns rows, or [] if the prompt is skipped."""
    prepared = prepare(item)
    if prepared is None:
        skipped.append({k: item[k] for k in ("split", "word")})
        return []
    state, leak = prepared
    geo_state = {k: state[k] for k in ("res", "attn", "line", "input")}  # activations only: no logits, no token ids
    out = []
    for name, (_, _, kind, fn) in TRANSFORMS.items():
        for setting in settings_of(name):
            if kind == "geometry":
                scores = read_vector(fn(geo_state, *setting), name)
            else:
                scores = fn(state, *setting)
            out.append({"role": item["role"], "split": item["split"], "word": item["word"], "transform": name,
                        "setting": list(setting)} | judge(scores, item, leak))
    return out


skipped = []
dev_rows = [r for item in translation_prompts(DEV, "dev") for r in evaluate(item, lambda name: TRANSFORMS[name][0])]
assert dev_rows, "no dev prompts survived"
chosen = {name: max(settings, key=lambda s: f1([r for r in dev_rows if r["transform"] == name and r["setting"] == list(s)]))
          for name, (settings, _, _, _) in TRANSFORMS.items()}
rows = dev_rows + [r for item in [*translation_prompts(TEST, "test"), *transfer_prompts()]
                   for r in evaluate(item, lambda name: [chosen[name]])]
for role in ("test", "transfer"):
    assert any(r["role"] == role for r in rows), f"no {role} prompts survived"

# ---- leaderboard ----
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_leaderboard"
out.mkdir(parents=True)
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump({"rows": rows, "skipped": skipped, "chosen": chosen}, f, ensure_ascii=False)
source_lines = inspect.getsource(__import__("transforms")).splitlines()
CONTROLS = ("identity (logit lens)", "random subspace (control)", "mean WikiText activation (control)", "input word (control)")
COLS = (("F1↑", max), ("TPR↑", max), ("FPR↓", min), ("English-only F1↑", max))
rows_by_table = {"geometry": [], "reference": []}
random_test = [r for r in rows if r["transform"] == "random subspace (control)" and r["role"] == "test"
               and r["setting"] == list(chosen["random subspace (control)"])]
for name, (settings, fitted, kind, _) in TRANSFORMS.items():
    mine = lambda role: [r for r in rows if r["transform"] == name and r["role"] == role and r["setting"] == list(chosen[name])]
    test, transfer = mine("test"), mine("transfer")
    line = next(i for i, text in enumerate(source_lines, 1) if f'@{TRANSFORMS[name][2]}("{name}"' in text)
    label = f"[{name}](scripts/challenge/transforms.py#L{line})"
    rows_by_table[kind].append({
        "transform": f"*{label}*" if name in CONTROLS else label, "F1↑": f1(test), "90% CI": f1_ci(test),
        "Δ vs random": "" if name == "random subspace (control)" else delta_ci(test, random_test), "TPR↑": mean(r["hidden"] for r in test),
        "FPR↓": mean(r["leaked"] for r in test), "English-only F1↑": f1(transfer),
        "fitted on": fitted})
n_test, n_transfer = len(test), len(transfer)


def render(table):
    table.sort(key=lambda r: -r["F1↑"])
    for col, better in COLS:
        best, tied = better(r[col] for r in table), len({r[col] for r in table}) == 1
        for r in table:
            r[col] = f"**{r[col]:.2f}**" if r[col] == best and not tied else f"{r[col]:.2f}"
    return tabulate(table, headers="keys", tablefmt="pipe", disable_numparse=True,
                    colalign=("left",) + ("right",) * 6 + ("left",))


commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
caption = (f"Qwen3.5-4B, {n_test} test prompts ({', '.join(f'{a}→{b}' for a, b in TEST)}). Each row's layer and rank "
           f"were chosen on {DEV[0][0]}→{DEV[0][1]} only. 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random "
           f"subspace on the same prompts. English-only F1: {n_transfer} two-hop questions (TwoHopFact). "
           f"[Per-prompt rows]({out.relative_to(ROOT)}/rows.json.gz), commit {commit}.")
markdown = (render(rows_by_table["geometry"]) + "\n\n" + caption
            + "\n\n### Reference: methods that use the output head, token scores or the J-lens\n\n"
            + render(rows_by_table["reference"]) + "\n")
(out / "leaderboard.md").write_text(markdown)
print(markdown, f"\nskipped: {skipped}\n{out / 'leaderboard.md'}", flush=True)
