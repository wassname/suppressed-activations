"""Score every method and write the leaderboard. One GPU, about 10 minutes.

Translation between languages that share no script with English or Chinese. For each prompt we keep a method's top 8
distinct words (case and space variants share a slot) at the last prompt token:

    TP = the unspoken word (English, or its Chinese translation) is in the top 8, else FN
    FP = a top-8 word is in the input or output language (script), or is the model's next word, else TN
    F1 = 2TP / (2TP + FP + FN), with counts over prompts

Each method has one fixed setting. Authors develop on the dev pair; only the test pairs and the English-only questions
(TwoHopFact, where the unspoken word is the bridge entity) are reported.
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
from transforms import TRANSFORMS, calibrate
from bench import (TEST, calibration_texts, delta_ci, f1, f1_ci, judge, prepare, read_vector, transfer_prompts,
                   translation_prompts)

state = calibrate(calibration_texts())
skipped = []


def evaluate(item):
    """Score one prompt for every method; returns rows, or [] if the prompt is skipped."""
    prepared = prepare(item)
    if prepared is None:
        skipped.append({k: item[k] for k in ("split", "word")})
        return []
    s, leak_in, leak_out = prepared
    out = []
    for name, e in TRANSFORMS.items():
        if e["kind"] == "geometry":
            scores = read_vector(e["fn"](s["hs"], state, *e["setting"]), name)  # activations only: no logits, no ids
        else:
            scores = e["fn"](s, *e["setting"])
        out.append({"role": item["role"], "split": item["split"], "word": item["word"], "transform": name}
                   | judge(scores, item, leak_in, leak_out))
    return out


rows = [r for item in [*translation_prompts(TEST, "test"), *transfer_prompts()] for r in evaluate(item)]
for role in ("test", "transfer"):
    assert any(r["role"] == role for r in rows), f"no {role} prompts survived"

# ---- leaderboard ----
out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_leaderboard"
out.mkdir(parents=True)
with gzip.open(out / "rows.json.gz", "wt") as f:
    json.dump({"rows": rows, "skipped": skipped, "settings": {n: list(e["setting"]) for n, e in TRANSFORMS.items()}},
              f, ensure_ascii=False)
source_lines = inspect.getsource(__import__("transforms")).splitlines()
CONTROLS = ("mean over layers", "random subspace", "mean calibration text", "logit lens, best layer")
COLS = (("F1↑", max), ("found↑", max), ("showed input/output words↓", min), ("English-only F1↑", max))
mine = lambda name, role: [r for r in rows if r["transform"] == name and r["role"] == role]
random_test = mine("random subspace", "test")
tables = {"geometry": [], "reference": []}
for name, e in TRANSFORMS.items():
    test, transfer = mine(name, "test"), mine(name, "transfer")
    line = next(i for i, text in enumerate(source_lines, 1) if f'@{e["kind"]}("{name}"' in text)
    label = f'[{name}](scripts/challenge/transforms.py#L{line} "{e["about"]}")'
    tables[e["kind"]].append({
        "method": f"*{label}*" if name in CONTROLS else label, "by": e["author"], "F1↑": f1(test), "90% CI": f1_ci(test),
        "Δ vs random": "" if name == "random subspace" else delta_ci(test, random_test),
        "found↑": mean(r["hidden"] for r in test), "showed input/output words↓": mean(r["leaked"] for r in test),
        "English-only F1↑": f1(transfer), "fitted on": e["fitted"]})
n_test, n_transfer = len(test), len(transfer)


def render(table):
    table.sort(key=lambda r: -r["F1↑"])
    for col, better in COLS:
        best, tied = better(r[col] for r in table), len({r[col] for r in table}) == 1
        pct = col != "F1↑" and col != "English-only F1↑"
        for r in table:
            text = f"{r[col]:.0%}" if pct else f"{r[col]:.2f}"
            r[col] = f"**{text}**" if r[col] == best and not tied else text
    return tabulate(table, headers="keys", tablefmt="pipe", disable_numparse=True,
                    colalign=("left", "left") + ("right",) * 6 + ("left",))


commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
caption = (f"Qwen3.5-4B, {n_test} test prompts ({', '.join(f'{a}→{b}' for a, b in TEST)}) and {n_transfer} English-only "
           f"two-hop questions. 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random subspace on the same "
           f"prompts. Hover a name for what it does. [Per-prompt rows]({out.relative_to(ROOT)}/rows.json.gz), commit {commit}.")
geometry, reference = render(tables["geometry"]), render(tables["reference"])
(out / "leaderboard.md").write_text(f"{geometry}\n\n{caption}\n\n### Reference methods\n\n{reference}\n")
docs = ROOT / "docs/leaderboard"
docs.mkdir(exist_ok=True)
(docs / "geometry.md").write_text(geometry + "\n")      # included by README.qmd
(docs / "README.md").write_text(f"# Leaderboard\n\nGenerated by scripts/challenge/score.py.\n\n## Geometry methods\n\n"
                                f"{geometry}\n\n{caption}\n\n## Reference methods\n\nThese may use token scores, the "
                                f"J-lens, or a layer picked on the dev pair; they show what is possible, not entries.\n\n"
                                f"{reference}\n")
(docs / "caption.md").write_text(caption + "\n")
print(geometry, f"\n\n{caption}\n\n{reference}\n\nskipped: {skipped}\n{out / 'leaderboard.md'}", flush=True)
