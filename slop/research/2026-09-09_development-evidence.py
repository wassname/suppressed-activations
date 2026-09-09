# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
# ---

# %% [markdown]
# # Development evidence: paired intervention examples (saved results only)
#
# Status: **development evidence, not achieved reliability**. Every block renders strings,
# token IDs, and metrics read from saved `result.json` artifacts on CPU. No model runs here.
# To replace development evidence with new experiments, edit only the `PATHS` dict —
# prose and helpers stay unchanged.
#
# Missing by construction (labelled, not reconstructed): the exact chat-rendered input token
# sequence is not stored in any `result.json` (no `input_ids` field); blocks show `repr` of
# the stored prompt components plus content boundaries. Suppressed-readout → concept mapping
# has no calibration: readout token lists are verbatim and **unvalidated**. The substring
# flags on the random sweep are mechanical string matches, not semantic validation; worker
# semantic judgments are stated separately and explicitly as judgments.

# %%
import json
from pathlib import Path

ROOT = Path(".").resolve()
while not (ROOT / "AGENTS.md").exists():
    ROOT = ROOT.parent
NB_DIR = Path(".").resolve()  # notebook dir; links below are relative to it

# Slot -> (result.json path, condition-id substring). New experiments replace paths here.
PATHS = {
    "dog_legs": ("out/2026-09-08_134000_fixed-band-dog-legs/result.json", "009_"),
    "ant_legs": ("out/2026-09-08_134000_fixed-band-ant-legs/result.json", "009_"),
    "dog_name": ("out/2026-09-08_134000_fixed-band-dog-name/result.json", "009_"),
    "ant_name": ("out/2026-09-08_134000_fixed-band-ant-name/result.json", "009_"),
    "dog_property": ("out/2026-09-08_134000_fixed-band-dog-property/result.json", "009_"),
    "ant_property": ("out/2026-09-08_134000_fixed-band-ant-property/result.json", "009_"),
    "random_dog": ("out/2026-09-08_134200_matched-random-band-dog/result.json", None),
    "random_ant": ("out/2026-09-08_134200_matched-random-band-ant/result.json", None),
}

DB = {}
for slot, (rel, cond) in PATHS.items():
    p = ROOT / rel
    assert p.exists(), f"missing artifact {p}"
    data = json.loads(p.read_text())
    rows = data["rows"] if cond is None else [r for r in data["rows"] if cond in r["condition_id"]]
    assert rows, f"no rows for {slot}"
    DB[slot] = (data, rows)

from IPython.display import Markdown, display

models = {(d["model"], d["revision"]) for d, _ in DB.values()}
assert len(models) == 1, f"model/revision differs across artifacts: {models}"
MODEL, REVISION = next(iter(models))
loaded = {k: (len(v) if isinstance(v, list) else 1) for k, (_, v) in DB.items()}
display(Markdown(f"Artifacts share model/revision: `{MODEL}` `{REVISION}`. Loaded slots: `{json.dumps(loaded)}`"))

# %% [markdown]
# ## Strict token-ID verification (pinned tokenizer, declared decode options)
#
# For every Base, intervention, and donor generation in every paired slot:
# `TOK.decode(token_ids)` with **default options** (`skip_special_tokens=False`,
# `clean_up_tokenization_spaces=True`) must equal the stored text byte-for-byte.
# `skip_special_tokens=True` provably breaks equality (drops the trailing `<|im_end|>`).

# %%
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer

TOK = AutoTokenizer.from_pretrained("Qwen/" + MODEL.split("/")[-1], revision=REVISION, trust_remote_code=True)
DECODE_OPTS = {}  # declared: tokenizer defaults
ROOT_PREFIX = "../../"  # this notebook lives in slop/research/; artifacts at repo root
PAIRED = ["dog_legs", "ant_legs", "dog_name", "ant_name", "dog_property", "ant_property"]
strict_checks = 0
for slot in PAIRED:
    _, (row,) = DB[slot][0], DB[slot][1]
    assert len(DB[slot][1]) == 1
    for kind in ("base_generation", "generation", "donor_generation"):
        assert TOK.decode(row[kind]["token_ids"], **DECODE_OPTS) == row[kind]["text"], (slot, kind)
        strict_checks += 1
display(Markdown(f"**Strict full-generation decode equality: {strict_checks}/{strict_checks}** (6 slots x base/intervention/donor, declared default decode options)"))

# %%
def rel_link(target, label):
    rel = Path(target)
    return f"[{label}]({rel.as_posix()})"


def run_link(slot, row):
    # run.md path relative to this notebook (slop/research/ -> ../../out/...).
    return (Path("../../") / PATHS[slot][0].replace("result.json", row["log"])).as_posix()


def md_top10(rows, with_delta):
    lines = ["| token | log p | p |" + (" change in log p |" if with_delta else ""),
             "|---|---|---|" + ("---|" if with_delta else "")]
    for r in rows[:10]:
        cells = [f"`{r['token']}`", f"{r['logp']:.3f}", f"{r['p']:.6f}"] + ([f"{r['delta_logp']:+.3f}"] if with_delta else [])
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def first32(row, kind):
    ids = row[kind]["token_ids"]
    return len(ids), TOK.decode(ids[:32], **DECODE_OPTS)


def condition_block(slot, title):
    data, (row,) = DB[slot][0], DB[slot][1]
    link = run_link(slot, row)
    n_base, prev_base = first32(row, "base_generation")
    n_steer, prev_steer = first32(row, "generation")
    display(Markdown(f"## {title}\n\n`{row['condition_id']}` · {rel_link(ROOT_PREFIX + PATHS[slot][0], 'result.json')} · {rel_link(link, 'full condition log')}"))
    display(Markdown(
        "### Base\n\n"
        f"Stored input components (actual `repr`, fenced):\n\n```python\n"
        f"source_prompt = {data['source_prompt']!r}\n"
        f"prefill_instruction = {row['prefill_instruction']!r}\n"
        f"extraction_instruction = {row['extraction_instruction']!r}\n```\n\n"
        f"Content boundaries: {json.dumps(data.get('prompt_boundaries'))}. "
        "**Missing:** exact chat-rendered input token sequence (no `input_ids` stored; not reconstructed).\n\n"
        f"Source readout at prefill, clean (**unvalidated**, verbatim): `{json.dumps(row['base_readout'], ensure_ascii=False)}`\n\n"
        f"First 32 of {n_base} generated token IDs, decoded (verbatim):\n\n```text\n{prev_base}\n```\n\n"
        f"Full Base continuation ({n_base} tokens): {rel_link(link, 'condition log, base section')}\n\n```text\n{row['base_generation']['text']}\n```\n\n"
        f"Base top-10:\n\n{md_top10(row['base_top_tokens'], with_delta=False)}"
    ))
    display(Markdown(
        "### Causal intervention (input unchanged)\n\n"
        f"Stored input components (actual `repr`, fenced — same source, donor shown):\n\n```python\n"
        f"source_prompt = {data['source_prompt']!r}\n"
        f"target_prompt = {data['target_prompt']!r}\n"
        f"prefill_instruction = {row['prefill_instruction']!r}\n```\n\n"
        "**Missing:** exact chat-rendered input token sequence (no `input_ids` stored; not reconstructed).\n\n"
        f"Readout after intervention, prefill (**unvalidated**, verbatim): `{json.dumps(row['readout'], ensure_ascii=False)}`\n\n"
        f"Readout at last decode step, separate from prefill (**unvalidated**, verbatim): `{json.dumps(row['last_decode_readout'], ensure_ascii=False)}`\n\n"
        f"Donor readout, unmodified donor (**unvalidated**, verbatim): `{json.dumps(row['target_readout'], ensure_ascii=False)}`\n\n"
        f"First 32 of {n_steer} generated token IDs, decoded (verbatim):\n\n```text\n{prev_steer}\n```\n\n"
        f"Full intervention continuation ({n_steer} tokens, including all text past sentence three): {rel_link(link, 'condition log, intervention section')}\n\n```text\n{row['generation']['text']}\n```\n\n"
        f"Intervention top-10 (change in log p vs Base):\n\n{md_top10(row['top_tokens'], with_delta=True)}\n\n"
        f"Donor clean continuation ({len(row['donor_generation']['token_ids'])} tokens, verbatim):\n\n```text\n{row['donor_generation']['text']}\n```\n\n"
        f"Expected base {json.dumps(row['expected_base_answer'])} steered {json.dumps(row['expected_steered_answer'])}; "
        f"S_swap={row['swap_log_odds_shift']:+.3f}, bare_answer_mass={row['bare_answer_mass']:.4f}, "
        f"r2={row['repeated_bigram_fraction']:.3f}. Config: `{json.dumps(row['config'], sort_keys=True)}`"
    ))

# %% [markdown]
# ## Paired examples: legs (digit + description transfer; dog description has a factual slip)

# %%
condition_block("dog_legs", "Dog legs")
condition_block("ant_legs", "Ant legs")

# %% [markdown]
# ## Naming self-corrections: donor name first, then correction back to spider
#
# Worker semantic judgment (not a metric): both emit the donor name, then explicitly
# correct to spider with spider-consistent descriptions. Judge meaning, not first token.

# %%
condition_block("dog_name", "Dog naming (self-correction)")
condition_block("ant_name", "Ant naming (self-correction)")

# %% [markdown]
# ## Property questions: known transfer failures/partials stay in the comparison
#
# Worker semantic judgment: dog-property stays spider throughout (failure — included so no
# known failure disappears); ant-property is an implicit affirmative with ant identity —
# the raw donor starts `1. Yes, the animal has antennae.` and the intervention states
# `a pair of antennae used for sensing the environment`; the leading `1.` is formatting
# noted separately, literal `Yes` not required.

# %%
condition_block("dog_property", "Dog property (stays spider)")
condition_block("ant_property", "Ant property (implicit affirmative, ant body)")

# %% [markdown]
# ## Matched-random band: mechanical substring flags only (not semantic validation)
#
# Flags: donor/animal word present, spider word present, loop-phrase present. Selected rows
# score donor-persistent 2/2; random rows 0/16 — a string signal consistent with, but weaker
# than, the worker judgments above.

# %%
import re
LOOP = re.compile(r"wait|incorrect|mistake|restart|stuck in a loop", re.I)
flag_rows = []
for slot, words in (("random_dog", ["dog", "canine", "puppy", "bark"]), ("random_ant", ["ant", "colony", "pheromone"])):
    data, rows = DB[slot]
    lines = [f"### {slot}: {rel_link(ROOT_PREFIX + PATHS[slot][0], 'result.json')}", "", "| condition | S_swap | first token | donor words | spider | loop phrase |", "|---|---|---|---|---|---|"]
    for r in rows:
        t = r["generation"]["text"]
        tl = t.lower()
        flags = (any(w in tl for w in words), "spider" in tl, bool(LOOP.search(t)))
        flag_rows.append((slot, r["condition_id"][:28], flags))
        lines.append(f"| `{r['condition_id'][:28]}` | {r['swap_log_odds_shift']:+.3f} | `{t.split()[0]}` | {flags[0]} | {flags[1]} | {flags[2]} |")
    display(Markdown("\n".join(lines)))

# %% [markdown]
# ## What is missing (do not guess)
#
# - Exact rendered input IDs and historical exact-input provenance: not stored; not reconstructed.
# - Readout calibration: no mapping from readout fragments to concepts; all readouts unvalidated.
# - Independent validation set: selected development conditions only.
# - Reliability across prompts: not shown; naming corrections and the dog-property stay-spider run are counter-evidence.
