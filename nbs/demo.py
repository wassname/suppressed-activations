# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Can changing a suppressed activation subspace change the answer?
#
# This notebook contains one example. Qwen3.5-4B first answers that the web-spinning animal
# has 8 legs. We replace residual components with components extracted from a dog prompt.
# At the displayed strength, the answer changes to 4.
#
# The tokenizer's chat template is used identically for extraction and generation. The exact fact
# is an assistant-message prefill, so the model completes it with the number first.

# %%
import math
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(os.environ.get("SUPPRESSED_ROOT", ".")).resolve()
sys.path.insert(0, str(ROOT))

from IPython.display import Markdown, display
import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import generate, intervention_hooks, layer_hooks, top_tokens, trajectory
from scripts.prompt import assistant_prefill_input_ids
from suppressed_activation_subspace import union_suppressed_activation_subspace

# Edit this cell. `just notebook-smoke` overrides the same values with environment variables.
MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REVISION = os.environ.get(
    "SUPPRESSED_REVISION", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
SOURCE_PROMPT = os.environ.get(
    "SUPPRESSED_SOURCE_PROMPT", "Fact: The number of legs on the animal that spins webs is "
)
TARGET_PROMPT = os.environ.get(
    "SUPPRESSED_DOG_PROMPT",
    "Fact: The number of legs on the animal that barks and is called man's best friend is ",
)
SOURCE_OUTPUT = os.environ.get("SUPPRESSED_SOURCE_OUTPUT", "8")
TARGET_OUTPUT = os.environ.get("SUPPRESSED_DOG_OUTPUT", "4")
EARLY_LAYER = int(os.environ.get("SUPPRESSED_EARLY_LAYER", 23))
PEAK_LAYER = int(os.environ.get("SUPPRESSED_PEAK_LAYER", 25))
OUTPUT_LAYER = int(os.environ.get("SUPPRESSED_OUTPUT_LAYER", 32))
INTERVENTION_LAYER = int(os.environ.get("SUPPRESSED_INTERVENTION_LAYER", 24))
READOUT_POSITIONS = int(os.environ.get("SUPPRESSED_READOUT_POSITIONS", 4))
INTERVENTION_POSITIONS = int(os.environ.get("SUPPRESSED_INTERVENTION_POSITIONS", 4))
RANK = int(os.environ.get("SUPPRESSED_RANK", 8))
STRENGTH = float(os.environ.get("SUPPRESSED_STRENGTH", 2.5))
GENERATION_TOKENS = int(os.environ.get("SUPPRESSED_TOKENS", 32))
GIT_COMMIT = subprocess.run(
    ["git", "rev-parse", "--short", "HEAD"],
    cwd=ROOT,
    check=True,
    text=True,
    capture_output=True,
).stdout.strip()
{
    "git": GIT_COMMIT,
    "model": MODEL,
    "revision": REVISION,
    "extraction layers": (EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER),
    "prompt format": "chat template with assistant fact prefill",
    "intervention": f"residual L{INTERVENTION_LAYER}, final {INTERVENTION_POSITIONS} fact tokens",
    "readout positions": READOUT_POSITIONS,
    "rank": RANK,
    "C": STRENGTH,
    "generation tokens": GENERATION_TOKENS,
}

# %% [markdown]
# Each prompt gets its own suppressed subspace from an unmodified forward pass. Extraction does not
# receive *spider* or *dog* as a label:
#
# ```python
# rise = logits[L25] - logits[L23]
# fall = logits[L25] - logits[L32]
# token_ids = topk(min(relu(rise), relu(fall)), rank=8)
# S = qr(centered_lm_head[token_ids].T)
# ```

# %%
tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
dtype = torch.bfloat16 if DEVICE == "cuda" else torch.float32
model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=dtype).to(DEVICE).eval()
language_model = model.model
blocks = language_model.layers
final_norm = language_model.norm
unembedding = model.lm_head.weight
norm_gain = 1.0 + final_norm.weight


def extract(prompt):
    chat = assistant_prefill_input_ids(tokenizer, prompt, device=DEVICE)
    input_ids = chat["input_ids"]
    residuals, logits = trajectory(model, input_ids, final_norm)
    residuals_by_position = residuals[
        :, chat["content_end"] - READOUT_POSITIONS:chat["content_end"]
    ].permute(1, 0, 2)
    basis, selected, _ = union_suppressed_activation_subspace(
        residuals_by_position,
        unembedding,
        norm_gain,
        early_layer=EARLY_LAYER,
        peak_layer=PEAK_LAYER,
        output_layer=OUTPUT_LAYER,
        rank=RANK,
        normalize_unembedding_rows=True,
    )
    return {
        "input_ids": input_ids,
        "residuals": residuals,
        "logits": logits,
        "basis": basis[0],
        "selected": [tokenizer.decode([int(token_id)]) for token_id in selected[0]],
        "content_end": chat["content_end"],
        "rendered": chat["rendered"],
    }


def probability_table(logits, expected_token, unexpected_token, base_logits=None):
    base_logp = base_logits.float().log_softmax(-1) if base_logits is not None else None
    rows = []
    for rank, row in enumerate(top_tokens(tokenizer, logits, k=10), start=1):
        token = row["token"]
        shown = f"**{token}**" if token == expected_token else token
        if token == unexpected_token:
            shown = f"*{token}*"
        values = [rank, shown, f'{row["logp"]:.3f}', f'{math.exp(row["logp"]):.6f}']
        if base_logp is not None:
            values.append(f'{row["logp"] - float(base_logp[row["token_id"]]):+.3f}')
        rows.append(values)
    headers = ["rank", "token", "log p", "p"]
    if base_logp is not None:
        headers.append("Δ log p")
    return tabulate(rows, headers=headers, tablefmt="pipe", disable_numparse=True)


source = extract(SOURCE_PROMPT)
target = extract(TARGET_PROMPT)
clean_generation = generate(
    model, tokenizer, source["input_ids"], blocks, {}, max_new_tokens=GENERATION_TOKENS
)
assert len(clean_generation["token_ids"]) == GENERATION_TOKENS

# %% [markdown]
# ## Base

# %%
display(Markdown(f"""\
Input (`repr`, including the trailing space):

`PROMPT START`

```python
{SOURCE_PROMPT!r}
```

`PROMPT END`

Rendered model input (`repr`, chat template; used for extraction and generation):

```python
{source['rendered']!r}
```

Readout ("what it is thinking but not saying"):

```python
{source['selected']!r}
```

Generation (next {GENERATION_TOKENS} tokens, verbatim):

`GENERATION START`

```text
{clean_generation['text']}
```

`GENERATION END`

{probability_table(source['logits'], SOURCE_OUTPUT, TARGET_OUTPUT)}
"""))

# %% [markdown]
# ## Causal intervention
#
# Now we replace the suppressed component selected from the spider prompt with the component
# selected from a dog prompt. The input stays unchanged. The readout below is recomputed after
# the intervention.

# %%
block = INTERVENTION_LAYER - 1  # decoder block output is the next residual
hook_by_layer = intervention_hooks(
    source["basis"],
    target["basis"],
    target["residuals"],
    operation="replace",
    strength=STRENGTH,
    blocks_to_hook=[block],
    positions=INTERVENTION_POSITIONS,
    source_position=source["content_end"] - 1,
    target_position=target["content_end"] - 1,
    prefill_only=True,
)
with layer_hooks(blocks, hook_by_layer):
    changed_residuals, changed_logits = trajectory(model, source["input_ids"], final_norm)
changed_by_position = changed_residuals[
    :, source["content_end"] - READOUT_POSITIONS:source["content_end"]
].permute(1, 0, 2)
_, changed_selected_ids, _ = union_suppressed_activation_subspace(
    changed_by_position,
    unembedding,
    norm_gain,
    early_layer=EARLY_LAYER,
    peak_layer=PEAK_LAYER,
    output_layer=OUTPUT_LAYER,
    rank=RANK,
    normalize_unembedding_rows=True,
)
changed_selected = [tokenizer.decode([int(token_id)]) for token_id in changed_selected_ids[0]]
changed_generation = generate(
    model,
    tokenizer,
    source["input_ids"],
    blocks,
    hook_by_layer,
    max_new_tokens=GENERATION_TOKENS,
)
assert len(changed_generation["token_ids"]) == GENERATION_TOKENS

display(Markdown(f"""\
Input (`repr`, unchanged):

`PROMPT START`

```python
{SOURCE_PROMPT!r}
```

`PROMPT END`

Rendered model input (`repr`, unchanged):

```python
{source['rendered']!r}
```

Readout after intervention ("what it is thinking but not saying"):

```python
{changed_selected!r}
```

Generation (next {GENERATION_TOKENS} tokens, verbatim):

`GENERATION START`

```text
{changed_generation['text']}
```

`GENERATION END`

{probability_table(changed_logits, TARGET_OUTPUT, SOURCE_OUTPUT, source['logits'])}
"""))

# %% [markdown]
# The dog component comes from an unmodified pass over this target input:
#
# ```python
# "Fact: The number of legs on the animal that barks and is called man's best friend is "
# ```
#
# For each complete input, an unmodified first pass extracts a separate subspace. We then change
# the final four fact-token residuals at L24. The donor's final fact-token component is used at
# each source position:
#
# ```python
# source = h_spider @ S_spider @ S_spider.T
# target = h_dog @ S_dog @ S_dog.T
# target = target * norm(source) / norm(target)
# h_replaced = match_norm(h_spider + C * (target - source), h_spider)
# ```
#
# C=2 was just below the answer crossing under this chat template. C=2.5 is the smallest tested
# value that generated 4. This is a selected single-prompt demonstration. It does not establish a
# reusable dog direction or distinguish dog identity transfer from target-answer-state transfer.
# See the [measured sweep](../out/2026-09-06_220932_chat-strength/run.md).
#
# <!-- Notebook written by PI/gpt-5.4 from Michael J. Clark's requested demo structure. -->
