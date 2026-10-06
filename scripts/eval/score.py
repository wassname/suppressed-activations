"""Score every method and write the leaderboard. One GPU, about 10 minutes.

Translation between languages that share no script with English or Chinese. For each prompt we keep a method's top 8
distinct words (case and space variants share a slot) at the last prompt token:

    TP = the unspoken word (English, or its Chinese translation) is in the top 8, else FN
    FP = a top-8 word is in the input or output language (script), or is the model's next word, else TN
    F1 = 2TP / (2TP + FP + FN), with counts over prompts

Each method has one fixed setting. Authors develop on the dev pair; only the test pairs are reported.
Usage: uv run scripts/data/build_word_lists.py (once), then uv run scripts/eval/score.py — PI/OpenAI
"""
import gzip
import inspect
import json
from pathlib import Path
import subprocess
import time


from unspoken_concepts.model import ROOT, MODEL, REVISION, LENS
from unspoken_concepts.methods import TRANSFORMS
from unspoken_concepts.calibration import calibrate
from unspoken_concepts.benchmark import TEST, calibration_texts, judge, prepare, read_vector, translation_prompts
from unspoken_concepts.reporting import tables

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


rows = [r for item in translation_prompts(TEST, "test") for r in evaluate(item)]
assert rows, "no test prompts survived"

out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_leaderboard"
out.mkdir(parents=True)
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
methods = {}
for name, entry in TRANSFORMS.items():
    methods[name] = {k: v for k, v in entry.items() if k != "fn"}
    methods[name]["code"] = (f"https://github.com/wassname/unspoken-concepts/blob/{commit}/"
                             f"{Path(inspect.getsourcefile(entry['fn'])).relative_to(ROOT)}#L{entry['fn'].__code__.co_firstlineno}")
evidence = {"rows": rows, "skipped": skipped,
            "settings": {name: list(e["setting"]) for name, e in TRANSFORMS.items()},
            "methods": methods, "provenance": {"source_run": out.name, "source_commit": commit,
                                               "MODEL": MODEL, "REVISION": REVISION, "LENS": LENS}}
with gzip.open(out / "leaderboard.json.gz", "wt") as f:
    json.dump(evidence, f, ensure_ascii=False)
report = tables(evidence, "leaderboard.json.gz")[-1]
(out / "leaderboard.md").write_text(report)
print(report, f"\nskipped: {skipped}\n{out / 'leaderboard.md'}", flush=True)
