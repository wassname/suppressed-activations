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
# # Suppressed activation replacement
#
# This notebook finds vocabulary directions that rise in a prompt's middle layers and fall before
# output. It changes one residual vector: the final prompt token at residual layer 26.
#
# Each complete prompt gets its own rank-8 subspace. `C=1` replaces the source component with the
# target component at the same norm. `C>1` extrapolates past that replacement. L23/L25/L32, rank 8,
# L26, and C=4 are settings selected in earlier exploration, not general defaults.
#
# The edit changes the Spider prompt's next answer from 8 to 6 or 4. Controls show that this is best
# read as transfer of the target prompt's next-answer state, not proof that an Ant or Dog concept was
# transferred. See the [fixed confirmation](../out/2026-09-05_211609_causal-confirmation/recovered_log.md).

# %%
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(os.environ.get("SUPPRESSED_ROOT", ".")).resolve()
sys.path.insert(0, str(ROOT))

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import (
    generate,
    intervention_hooks,
    layer_hooks,
    metrics,
    one_token,
    run_forward,
    top_tokens,
    trajectory,
)
from suppressed_activation_subspace import suppressed_activation_subspace

# Edit this cell. `just notebook-smoke` overrides the same values with environment variables.
MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REVISION = os.environ.get(
    "SUPPRESSED_REVISION", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
SOURCE_PROMPT = os.environ.get(
    "SUPPRESSED_SOURCE_PROMPT", "Fact: The number of legs on the animal that spins webs is "
)
TARGET_PROMPTS = {
    "ant": os.environ.get(
        "SUPPRESSED_ANT_PROMPT",
        "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ",
    ),
    "dog": os.environ.get(
        "SUPPRESSED_DOG_PROMPT",
        "Fact: The number of legs on the animal that barks and is called man's best friend is ",
    ),
}
SOURCE_OUTPUT = os.environ.get("SUPPRESSED_SOURCE_OUTPUT", "8")
TARGET_OUTPUTS = {
    "ant": os.environ.get("SUPPRESSED_ANT_OUTPUT", "6"),
    "dog": os.environ.get("SUPPRESSED_DOG_OUTPUT", "4"),
}
EARLY_LAYER = int(os.environ.get("SUPPRESSED_EARLY_LAYER", 23))
PEAK_LAYER = int(os.environ.get("SUPPRESSED_PEAK_LAYER", 25))
OUTPUT_LAYER = int(os.environ.get("SUPPRESSED_OUTPUT_LAYER", 32))
INTERVENTION_LAYER = int(os.environ.get("SUPPRESSED_INTERVENTION_LAYER", 26))
RANK = int(os.environ.get("SUPPRESSED_RANK", 8))
MAX_NEW_TOKENS = int(os.environ.get("SUPPRESSED_TOKENS", 64))
C_VALUES = tuple(
    float(value)
    for value in os.environ.get("SUPPRESSED_STRENGTHS", "-1,0,1,2,4,8").split(",")
)
GIT_DESCRIBE = subprocess.run(
    ["git", "describe", "--always", "--dirty"],
    cwd=ROOT,
    check=True,
    text=True,
    capture_output=True,
).stdout.strip()
{
    "git": GIT_DESCRIBE,
    "model": MODEL,
    "revision": REVISION,
    "extraction layers": (EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER),
    "intervention": f"one vector at residual L{INTERVENTION_LAYER}, final prompt token",
    "rank": RANK,
    "C values": C_VALUES,
}

# %% [markdown]
# ## Extract one subspace per prompt
#
# Extraction is a first, unmodified forward pass at the final prompt token. It does not receive the
# words *spider*, *ant*, or *dog* as labels:
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
    input_ids = tokenizer(
        prompt, return_tensors="pt", add_special_tokens=False
    ).input_ids.to(DEVICE)
    residuals, logits = trajectory(model, input_ids, final_norm)
    basis, selected = suppressed_activation_subspace(
        residuals[:, -1][None],
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
    }


source = extract(SOURCE_PROMPT)
targets = {name: extract(prompt) for name, prompt in TARGET_PROMPTS.items()}

# %% [markdown]
# The core operation is small. `S @ S.T` is a projector; it does not depend on how QR rotates the
# columns of `S`.
#
# ```python
# match_norm(x, ref) = x * norm(ref) / norm(x)
# source = h @ S_source @ S_source.T
# target = match_norm(h_target @ S_target @ S_target.T, source)
# h_replaced = match_norm(h + C * (target - source), h)
# ```

# %%
block = INTERVENTION_LAYER - 1  # block 25 writes residual L26
source_output_id = one_token(tokenizer, SOURCE_OUTPUT)
target_output_ids = {
    name: one_token(tokenizer, output) for name, output in TARGET_OUTPUTS.items()
}


def hooks(target_name, strength, *, prefill_only=False, record=None):
    if strength == 0:
        return {}
    return intervention_hooks(
        source["basis"],
        targets[target_name]["basis"],
        targets[target_name]["residuals"],
        operation="replace",
        strength=strength,
        blocks_to_hook=[block],
        prefill_only=prefill_only,
        record=record,
    )


# %% [markdown]
# ## Readout before and after
#
# The source readout contains `Spider` and web tokens. The Dog target is also readable. The Ant
# target is not lexically clear, which is one reason not to call this an animal-concept swap.

# %%
readout_rows = [["spider, before", ", ".join(source["selected"])]]
for target_name in targets:
    with layer_hooks(blocks, hooks(target_name, 4)):
        changed_residuals, _ = trajectory(model, source["input_ids"], final_norm)
    _, changed_selected = suppressed_activation_subspace(
        changed_residuals[:, -1][None],
        unembedding,
        norm_gain,
        early_layer=EARLY_LAYER,
        peak_layer=PEAK_LAYER,
        output_layer=OUTPUT_LAYER,
        rank=RANK,
        normalize_unembedding_rows=True,
    )
    readout_rows += [
        [f"{target_name}, target", ", ".join(targets[target_name]["selected"])],
        [
            f"spider after {target_name}, C=4",
            ", ".join(tokenizer.decode([int(token_id)]) for token_id in changed_selected[0]),
        ],
    ]
print(tabulate(
    readout_rows,
    headers=["trajectory", "subspace readout tokens"],
    tablefmt="rounded_outline",
))

# %% [markdown]
# ## Two target directions and several strengths
#
# Positive C moves the source component toward the named target prompt. Negative C moves away from
# that prompt. `C=1` is the replacement endpoint; larger magnitudes are extrapolations.

# %%
metric_rows = []
for target_name, target_id in target_output_ids.items():
    for strength in C_VALUES:
        record = {}
        hook_by_layer = hooks(target_name, strength, record=record)
        logits = (
            source["logits"]
            if strength == 0
            else run_forward(model, source["input_ids"], blocks, hook_by_layer)
        )
        row = metrics(tokenizer, logits, source["logits"], source_output_id, target_id)
        geometry = record.get(INTERVENTION_LAYER, {"perturbation_norm": 0, "residual_norm": 1})
        metric_rows.append({
            "target prompt": target_name,
            "C": strength,
            "top": row["top"][0]["token"],
            f"p({SOURCE_OUTPUT})": row["p_source"],
            f"p({TARGET_OUTPUTS[target_name]})": row["p_target"],
            "target/source log odds": row["log_odds_target_vs_source"],
            "distance/residual": geometry["perturbation_norm"] / geometry["residual_norm"],
        })
print(tabulate(metric_rows, headers="keys", tablefmt="rounded_outline", floatfmt="+.4f"))

# %% [markdown]
# ## Exact continuations
#
# The hook is active only while reading the prompt. Each row contains 64 greedily generated tokens.
# The C=4 continuations match simply forcing the first token to 6 or 4, so the longer text is not
# separate evidence for persistent animal information.

# %%
clean_generation = generate(
    model, tokenizer, source["input_ids"], blocks, {}, max_new_tokens=MAX_NEW_TOKENS
)
assert len(clean_generation["token_ids"]) == MAX_NEW_TOKENS
generation_rows = [{
    "target prompt": "clean",
    "C": 0,
    "generation": clean_generation["text"],
}]
for target_name in targets:
    for strength in C_VALUES:
        if strength == 0:
            continue
        result = generate(
            model,
            tokenizer,
            source["input_ids"],
            blocks,
            hooks(target_name, strength, prefill_only=True),
            max_new_tokens=MAX_NEW_TOKENS,
        )
        assert len(result["token_ids"]) == MAX_NEW_TOKENS
        generation_rows.append({
            "target prompt": target_name,
            "C": strength,
            "generation": result["text"],
        })
print(tabulate(
    generation_rows,
    headers="keys",
    tablefmt="grid",
    floatfmt="+.1f",
    maxcolwidths=[8, 5, 100],
))

# %% [markdown]
# ## What the fixed controls found
#
# The C=4 Ant and Dog effects failed the preregistered 95% criterion: only 238/256 and 235/256
# matched random effects were smaller. Arithmetic target prompts for 6 and 4 reproduced or exceeded the
# animal-target effects. The operation therefore provides a sample-specific place to intervene on
# the next-answer state, but this experiment does not identify a transferable animal direction.
#
# <!-- Notebook written by PI/gpt-5.4 from Michael J. Clark's requested demo structure. -->
