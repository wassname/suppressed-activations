# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
# ---

# %% [markdown]
# # Suppressed-activation intervention: paired Base / Causal-intervention examples
#
# Development evidence from measured span-correction cells at **C=1.5**, the evidence-backed
# operating point for naming+legs on both animals. Every block reads saved `result.json`
# artifacts (CPU, no model run). This notebook does NOT demonstrate cross-question
# persistence; property cells are marked pending.
#
# Production/scientific status: **development evidence, not achieved reliability.**
# Reserved evaluation strings (spinneret naming, limb-count, live-birth) not used.

# %%
import json
from pathlib import Path

BATCH = Path("/workspace/2026/suppressed-activations-batchwork")  # worktree holding the measured out/

# Slot -> result.json path (relative to BATCH). Edit to swap development evidence for new runs.
# Replay artifacts (regression verification, tasks 1005/1006): the same measured cells
# re-run from the recovered config; probabilities are bitwise-identical to the originals.
PATHS = {
    "legs_dog_c15": "out/2026-09-10_replay-C1.5-legs-dog/result.json",
    "legs_ant_c15": "out/2026-09-10_replay-C1.5-legs-ant/result.json",
    "naming_dog_c15": "out/2026-09-10_replay-C1.5-naming-dog/result.json",
    "naming_ant_c15": "out/2026-09-10_replay-C1.5-naming-ant/result.json",
    "prop_dog_c15": "out/2026-09-10_replay-C1.5-property-dog/result.json",
    "prop_ant_c15": "out/2026-09-10_replay-C1.5-property-ant/result.json",
}
DB = {}
for slot, rel in PATHS.items():
    if rel is None:
        continue
    p = BATCH / rel
    assert p.exists(), f"missing {rel}"
    data = json.loads(p.read_text())
    row = data["rows"][0]
    DB[slot] = (data, row)
print("loaded measured slots:", sorted(DB.keys()))

# %% [markdown]
# ## Tokenizer to decode exact previews

# %%
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer

data0 = DB["legs_dog_c15"][0]
TOK = AutoTokenizer.from_pretrained("Qwen/" + data0["model"].split("/")[-1],
                                     revision=data0["revision"], trust_remote_code=True)
print("tokenizer:", data0["model"], data0["revision"][:12])

def md_table(rows, with_delta):
    lines = ["| token | log p | p |" + (" change in log p |" if with_delta else ""),
             "|---|---|---|" + ("---|" if with_delta else "")]
    for r in rows[:10]:
        cell = [f"`{r['token']}`", f"{r['logp']:.3f}", f"{r['p']:.5f}"] + ([f"{r['delta_logp']:+.3f}"] if with_delta else [])
        lines.append("| " + " | ".join(cell) + " |")
    return "\n".join(lines)

def first32(row, kind):
    ids = row[kind]["token_ids"]
    return len(ids), TOK.decode(ids[:32])

from IPython.display import Markdown, display

def block(slot, title):
    data, row = DB[slot]
    rel = PATHS[slot]
    log_rel = row["log"]
    nbase, pbase = first32(row, "base_generation")
    nsteer, psteer = first32(row, "generation")
    display(Markdown(f"## {title} :: `{row['condition_id']}`"))
    display(Markdown(f"Source (`repr`):\\n\\n```python\\n{data['source_prompt']!r}\\n```\\n\\n"
                     f"Target (`repr`):\\n\\n```python\\n{data['target_prompt']!r}\\n```\\n\\n"
                     f"Missing: exact chat-rendered input token sequence (no `input_ids` stored)."))
    display(Markdown(
        f"### Base\\n\\nClean-source prefill readout (**unvalidated**, verbatim): "
        f"`{json.dumps(row['base_readout'], ensure_ascii=False)}`\\n\\n"
        f"First 32 of {nbase} generated tokens, decoded:\\n\\n```text\\n{pbase}\\n```\\n\\n"
        f"Full Base continuation: [`{log_rel}`](../{rel.replace('result.json', log_rel)})\\n\\n"
        f"Base top-10:\\n\\n{md_table(row['base_top_tokens'], with_delta=False)}"))
    display(Markdown(
        f"### Causal intervention\\n\\nEdited-source prefill readout (**unvalidated**, verbatim): "
        f"`{json.dumps(row['readout'], ensure_ascii=False)}`\\n\\n"
        f"First 32 of {nsteer} generated tokens, decoded:\\n\\n```text\\n{psteer}\\n```\\n\\n"
        f"Full intervention continuation: [`{log_rel}`](../{rel.replace('result.json', log_rel)})\\n\\n"
        f"Intervention top-10 (change in log p vs Base):\\n\\n{md_table(row['top_tokens'], with_delta=True)}\\n\\n"
        f"Expected base `{row['expected_base_answer']}` steered `{row['expected_steered_answer']}`; "
        f"S_swap={row['swap_log_odds_shift']:+.3f}, bare_answer_mass={row['bare_answer_mass']:.4f}, "
        f"r2={row['repeated_bigram_fraction']:.3f}"))

# %% [markdown]
# ## Legs (C=1.5): digit + identity transfer (measured)

# %%
block("legs_dog_c15", "Dog legs, C=1.5")
block("legs_ant_c15", "Ant legs, C=1.5")

# %% [markdown]
# ## Naming (C=1.5): identity transfer (measured)

# %%
block("naming_dog_c15", "Dog naming, C=1.5")
block("naming_ant_c15", "Ant naming, C=1.5")

# %% [markdown]
# ## Property (C=1.5): measured FAILURE, kept visible
#
# The answer stays `No` for both animals while identity moves. Dog: "The animal that spins
# webs is a dog, which is a mammal" -- then answers No, a self-contradiction (a dog is a
# mammal). Ant: identity moves to a honey bee (a third animal). Property transfer does not
# work at the frozen operating point; these rows are shown unedited.

# %%
block("prop_dog_c15", "Dog property, C=1.5 (FAILED transfer: identity moves, answer contradicts)")
block("prop_ant_c15", "Ant property, C=1.5 (FAILED transfer: identity moves to honey bee)")

# %% [markdown]
# ## Semantic reliability table (frozen manifest; fresh evaluation pending)
#
# The frozen manifest (batchwork `slop/2026-09-10_eval_manifest.md` rev 2) declares 12 FRESH
# never-executed questions (2 wordings x naming/legs/property x dog/ant), four separate
# judgments (Answer / Identity / Coherence / Formatting; primary rate = first three), exact
# source+donor strings with donor-competence-verified ground truth, C=0 and matched-random
# controls at the candidate strength, and Clopper-Pearson intervals over the declared
# denominator. It has NOT been executed: no fresh-set numbers exist yet. The rows above are
# DEVELOPMENT regression evidence on heavily exposed prompts, not the reliability estimate.
#
# Ground-truth corrections of record: property-mammal-ant's expected answer is No (the clean
# donor answers "1. No, it is not a mammal"); historical runner configs pairing mammal wording
# with expected Yes had invalid ground truth and pushed a factually wrong answer.

# %% [markdown]
# ## Provenance
#
# Each artifact stores its own git describe, code SHA-256 of the runner files, resolved config,
# and revision; the runner writes them at run time and the reliability table must be computed
# from those fields, not from notebook state. Worker: PI[claude] (glm-5p3-flash session,
# user-confirmed switch). Recovery decision: batchwork `slop/2026-09-10_recovery_decision.md`.

# %% [markdown]
# ## Fresh-evaluation reliability (frozen manifest rev4; task 1008)
#
# Twelve never-executed questions, frozen candidate, C=0 and strength-matched in-span random
# controls. Primary semantic success = answer + persistent identity + coherence; formatting
# separate. Descriptive n/N on a paired convenience sample -- NOT a population estimate.

# %%
import re

def eval_dir(cond):
    return BATCH / f"out/2026-09-10_eval-{cond}/result.json"

def judge(cond, expect, donor_word):
    row = json.loads(eval_dir(cond).read_text())["rows"][0]
    gen = row["generation"]["text"]
    low = gen.lower()
    answer = row.get("first_answer")
    ans_ok = (answer == expect) or bool(re.search(rf"\b{re.escape(expect.lower())}\b", low.split("\n")[0].lower()))
    ident = donor_word in low
    spider_claim = ("the spider" in low and ("is a" in low or "are" in low))
    third = any(w in low for w in ("honey bee", "cow", "cat")) and not ident
    bigram = row.get("repeated_bigram_fraction", 0)
    censored = len(row["generation"]["token_ids"]) >= 128
    ident_status = "yes" if (ident and not spider_claim) else ("no" if (spider_claim or third) else "unknown")
    coherence = (bigram < 0.2) and not censored
    return ans_ok, ident_status, coherence, bigram, censored

FRESH = json.loads((BATCH / "slop/eval_fresh_batch.json").read_text())
meta = {e["id"]: e for e in FRESH}
counts = {"candidate-C1.5": [0, 0], "random-C1.5": [0, 0]}
table = ["| question | judgment | answer | identity | coherence | censored |", "|---|---|---|---|---|---|"]
for cond in [e["output_dir"].split("eval-")[1] for e in
             json.loads((BATCH / "slop/eval_fresh_run_batch.json").read_text())]:
    # three arms: candidate-C1.5 / random-C1.5 / C0 (identity control, not rubric-scored)
    arm = next((a for a in ("candidate-C1.5", "random-C1.5") if cond.startswith(a)), None)
    if arm is None:
        assert cond.startswith("C0"), cond  # identity control; verified in the runner
        continue
    qid = cond[len(arm) + 1:]
    m = meta[qid]
    a, i, c, b, cen = judge(cond, m["donor_expected_answer"], qid.rsplit("-", 1)[-1])
    counts[arm][0] += int(a and i == "yes" and c)
    counts[arm][1] += 1
    if arm == "candidate-C1.5":
        noop = " (no-op control)" if not m["fact_changes"] else ""
        table.append(f"| {qid}{noop} | candidate | {'Y' if a else 'n'} | {i} | {'Y' if c else 'n'} | {cen} |")
for arm, (k, n) in counts.items():
    table.append(f"| **{arm} PRIMARY** | | | | | **{k}/{n}** |")
display(Markdown("\n".join(table)))

# %% [markdown]
# ## Paired fresh-set demonstrations (candidate cells, verbatim)

# %%
for cond, title in (("candidate-C1.5-legs-L1-dog", "Fresh legs, dog (digit + identity + coherent)"),
                    ("candidate-C1.5-prop-P1-spinneret-dog", "Fresh property, dog (source-bound answer: FAILS)")):
    row = json.loads(eval_dir(cond).read_text())["rows"][0]
    data = json.loads(eval_dir(cond).read_text())
    n = len(row["generation"]["token_ids"])
    display(Markdown(f"### {title} :: {cond}"))
    display(Markdown(f"Source (`repr`):\n\n```python\n{data['source_prompt']!r}\n```\n\n"
                     f"First 32 of {n} tokens:\n\n```text\n{TOK.decode(row['generation']['token_ids'][:32])}\n```\n\n"
                     f"Full continuation ({n} tokens):\n\n```text\n{row['generation']['text']}\n```"))

# %% [markdown]
# ## Not demonstrated here
#
# Cross-question persistence, readout calibration, and wider transfer are not established.
# Readouts are verbatim and unvalidated. The 128-token cap is censoring: a capped continuation
# is not evidence of natural completion. The 6/12 fresh-set rate is a descriptive fraction of a
# paired convenience sample, not a population estimate or a solved mechanism.
