"""README leaderboard from a 09 scoreboard run: pick each family's setting on the dev pair by unsaid F1, report test and English transfer.

unsaid F1 = F1 over the top 8 distinct words, set to 0 when any spoken or input token is in them (computed in 09).
Usage: uv run scripts/english/10_leaderboard.py out/<run>_transform-scoreboard — PI/OpenAI
"""
import gzip
import json
from pathlib import Path
import sys
from statistics import mean

from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
run = Path(sys.argv[1]).resolve()
rows = json.loads((gzip.open(run / "rows.json.gz") if (run / "rows.json.gz").exists() else open(run / "rows.json")).read())
SRC = "scripts/english/09_transform_scoreboard.py"
src_lines = (ROOT / SRC).read_text().splitlines()
# ★: the transform itself uses a lens or per-prompt vocabulary scores, not only a fixed subspace
LENS_BASED = {"plain lens", "J-lens", "J-lens minus output subspace", "your suppressed subspace (rank 32)",
              "your suppressed subspace via J-lens (rank 32)", "your rise-and-fall, plain", "rise-and-fall through J-lens",
              "attention output, J-lens"}
BASELINES = {"plain lens", "random subspace (floor)"}


def unsaid_f1(r):
    return r["unsaid_F1"]


def unsaid_share(r):
    return r["unsaid_share"]


def link(fam):
    n = next(i for i, line in enumerate(src_lines, 1) if f'"{fam}"' in line)
    return f"[{fam}]({SRC}#L{n})"


table = []
for fam in dict.fromkeys(r["family"] for r in rows):
    mine = [r for r in rows if r["family"] == fam]
    settings = sorted({(r["layer"], r["rank"]) for r in mine})
    dev = lambda s: mean(unsaid_share(r) for r in mine if (r["layer"], r["rank"]) == s and r["role"] == "dev")
    best = max(settings, key=lambda s: (round(dev(s), 6), -s[0], -s[1]))
    pick = [r for r in mine if (r["layer"], r["rank"]) == best]
    test, eng = [r for r in pick if r["role"] == "test"], [r for r in pick if r["role"] == "transfer"]
    name = link(fam) + (" ★" if fam in LENS_BASED else "")
    table.append({"transform": f"*{name}*" if fam in BASELINES else name,
                  "setting": f"L{best[0]}" + (f" r{best[1]}" if best[1] else ""),
                  "unsaid en/zh share↑": mean(unsaid_share(r) for r in test), "en/zh share↑": mean(r["hidden_share"] for r in test),
                  "right-word unsaid F1↑": mean(unsaid_f1(r) for r in test),
                  "said↓": mean(r["said"] for r in test), "transfer unsaid F1↑": mean(unsaid_f1(r) for r in eng),
                  "settings tried": len(settings), "_n": (len(test), len(eng))})
table.sort(key=lambda r: -r["unsaid en/zh share↑"])
n_test, n_eng = table[0].pop("_n")
for r in table[1:]:
    assert r.pop("_n") == (n_test, n_eng)
for col in ("unsaid en/zh share↑", "en/zh share↑", "right-word unsaid F1↑", "transfer unsaid F1↑"):
    top = max(r[col] for r in table)
    for r in table:
        r[col] = f"**{r[col]:.2f}**" if r[col] == top else f"{r[col]:.2f}"
low = min(r["said↓"] for r in table)
for r in table:
    r["said↓"] = f"**{r['said↓']:.2f}**" if r["said↓"] == low else f"{r['said↓']:.2f}"
md = tabulate(table, headers="keys", tablefmt="pipe", disable_numparse=True, colalign=("left", "left") + ("right",) * 6)
pairs = sorted({r["split"] for r in rows if r["role"] == "test"}); dev = sorted({r["split"] for r in rows if r["role"] == "dev"})
caption = (f"<sub>Table: top 8 distinct words per prompt, no masks. Test = translation {', '.join(pairs)} ({n_test} prompts); "
           f"English transfer = all-English two-step questions ({n_eng}), never used to choose anything. Each row's setting was chosen on {', '.join(dev)} only. "
           "en/zh share = share of the 8 words written in English or Chinese; unsaid = set to 0 when any of the 8 is in the input or output language's script. "
           "right-word F1 scores only the translation of this prompt's word (from the dictionary). said = share of lists with an output-script token. "
           "All rows read out through the model's output head; ★ means the transform also uses a lens or per-prompt vocabulary scores. "
           f"Source: [{run.name}]({run.relative_to(ROOT)}/run.md).</sub>")
out = md + "\n\n" + caption + "\n"
(run / "leaderboard.md").write_text(out)
print(out)
