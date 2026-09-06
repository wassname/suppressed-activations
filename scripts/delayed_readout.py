# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Read an early, four-position intervention after identical cached continuation tokens."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import torch
from loguru import logger
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.demo import (
    generate,
    intervention_hooks,
    layer_hooks,
    one_token,
    run_forward,
    top_tokens,
    trajectory,
)
from suppressed_activation_subspace import (
    component,
    match_norm,
    persistent_suppressed_activation_subspace,
    suppressed_activation_subspace,
)

MODEL = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
INSTRUCTION = "Complete this fact with only the number.\n\n"
SOURCE_PROMPT = "Fact: The number of legs on the animal that spins webs is "
TARGET_PROMPT = "Fact: The number of legs on the animal that barks and is called man's best friend is "
EARLY_LAYER = 23
PEAK_LAYER = 25
OUTPUT_LAYER = 32
INTERVENTION_LAYER = 23
RANK = 8
POSITIONS = 4
PERSISTENCE_POSITIONS = 4
FORCED_TOKENS = 4
SWEEP_LAYERS = tuple(range(1, 33))
SWEEP_POSITIONS = (1, 2, 3, 4, 8)
SWEEP_STRENGTHS = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
DEMO_TOKENS = 32


def find_subsequence(sequence: list[int], subsequence: list[int]) -> int:
    matches = [
        start
        for start in range(len(sequence) - len(subsequence) + 1)
        if sequence[start:start + len(subsequence)] == subsequence
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one content span, found {len(matches)}")
    return matches[0]


def chat_input_ids(tokenizer, content: str, *, enable_thinking: bool) -> dict:
    user_content = INSTRUCTION + content
    encoded = tokenizer.apply_chat_template(
        [{"role": "user", "content": user_content}],
        tokenize=True,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
        return_tensors="pt",
    )
    content_ids = tokenizer(user_content, add_special_tokens=False).input_ids
    input_ids = encoded.input_ids
    content_start = find_subsequence(input_ids[0].tolist(), content_ids)
    return {
        "input_ids": input_ids.cuda(),
        "content_start": content_start,
        "content_end": content_start + len(content_ids),
    }


def extract(
    model, tokenizer, final_norm, unembedding, norm_gain, content: str, *, enable_thinking=True
) -> dict:
    chat = chat_input_ids(tokenizer, content, enable_thinking=enable_thinking)
    input_ids = chat["input_ids"]
    residuals, logits = trajectory(model, input_ids, final_norm)
    persistence_start = chat["content_end"] - PERSISTENCE_POSITIONS
    residuals_by_position = residuals[:, persistence_start:chat["content_end"]].permute(1, 0, 2)
    basis, selected, scores_by_position = persistent_suppressed_activation_subspace(
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
        "selected_by_position": [
            [tokenizer.decode([int(token_id)]) for token_id in scores.topk(RANK).indices]
            for scores in scores_by_position
        ],
        "persistence_token_ids": selected[0].tolist(),
        "persistence_scores_by_position": scores_by_position[:, selected[0]].tolist(),
        "persistence_input_tokens": [
            tokenizer.decode([int(token_id)])
            for token_id in input_ids[0, persistence_start:chat["content_end"]]
        ],
        "rendered_prompt": tokenizer.decode(input_ids[0], skip_special_tokens=False),
        "content_start": chat["content_start"],
        "content_end": chat["content_end"],
    }


def residuals_from_output(output, raw_final: torch.Tensor) -> torch.Tensor:
    return torch.stack([hidden[0] for hidden in output.hidden_states[:-1]] + [raw_final[0]])


def cached_trajectories(model, final_norm, blocks, prompt_ids, forced_ids, hooks) -> list[torch.Tensor]:
    raw_final: list[torch.Tensor] = []

    def save_raw_final(_module, inputs):
        raw_final.append(inputs[0].detach())

    handle = final_norm.register_forward_pre_hook(save_raw_final)
    try:
        with layer_hooks(blocks, hooks), torch.no_grad():
            output = model(input_ids=prompt_ids, output_hidden_states=True, use_cache=True)
            trajectories = [residuals_from_output(output, raw_final[-1])]
            cache = output.past_key_values
            for token_id in forced_ids:
                output = model(
                    input_ids=torch.tensor([[token_id]], device=prompt_ids.device),
                    past_key_values=cache,
                    output_hidden_states=True,
                    use_cache=True,
                )
                trajectories.append(residuals_from_output(output, raw_final[-1]))
                cache = output.past_key_values
    finally:
        handle.remove()
    return trajectories


def readout(residuals, tokenizer, unembedding, norm_gain) -> list[str]:
    _, selected = suppressed_activation_subspace(
        residuals[:, -1][None],
        unembedding,
        norm_gain,
        early_layer=EARLY_LAYER,
        peak_layer=PEAK_LAYER,
        output_layer=OUTPUT_LAYER,
        rank=RANK,
        normalize_unembedding_rows=True,
    )
    return [tokenizer.decode([int(token_id)]) for token_id in selected[0]]


def persistent_readout(residuals, content_end, tokenizer, unembedding, norm_gain) -> dict:
    start = content_end - PERSISTENCE_POSITIONS
    residuals_by_position = residuals[:, start:content_end].permute(1, 0, 2)
    _, selected, scores_by_position = persistent_suppressed_activation_subspace(
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
        "selected": [tokenizer.decode([int(token_id)]) for token_id in selected[0]],
        "selected_by_position": [
            [tokenizer.decode([int(token_id)]) for token_id in scores.topk(RANK).indices]
            for scores in scores_by_position
        ],
        "scores_by_position": scores_by_position[:, selected[0]].tolist(),
    }


def projection_shares(residuals, basis) -> dict[str, float]:
    return {
        f"L{layer}": float(
            component(residuals[layer, -1].float(), basis).norm() / residuals[layer, -1].float().norm()
        )
        for layer in (EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER)
    }


def condition(
    model, tokenizer, final_norm, blocks, source, target, unembedding, norm_gain, forced_ids, strength: float
) -> dict:
    record: dict[int, dict] = {}
    hooks = intervention_hooks(
        source["basis"],
        target["basis"],
        target["residuals"],
        operation="replace",
        strength=strength,
        blocks_to_hook=[INTERVENTION_LAYER - 1],
        positions=POSITIONS,
        source_position=source["content_end"] - 1,
        target_position=target["content_end"] - 1,
        prefill_only=True,
        record=record,
    )
    trajectories = cached_trajectories(
        model, final_norm, blocks, source["input_ids"], forced_ids, hooks
    )
    return {
        "strength": strength,
        "readouts": [readout(x, tokenizer, unembedding, norm_gain) for x in trajectories],
        "source_projection_shares": [projection_shares(x, source["basis"]) for x in trajectories],
        "target_projection_shares": [projection_shares(x, target["basis"]) for x in trajectories],
        "top_tokens": [top_tokens(tokenizer, x[-1, -1].float() @ unembedding.float().T, k=5) for x in trajectories],
        "patch_record": record,
    }


def report(result: dict) -> str:
    rows = []
    for name, item in result["conditions"].items():
        for step, selected in enumerate(item["readouts"]):
            rows.append([
                name,
                "prompt" if step == 0 else f"forced {step}",
                repr(selected),
                f"{item['source_projection_shares'][step]['L32']:.4f}",
                f"{item['target_projection_shares'][step]['L32']:.4f}",
            ])
    table = tabulate(
        rows,
        headers=["condition", "state", "readout", "source share", "donor share"],
        tablefmt="pipe",
        disable_numparse=True,
    )
    return f"""# Delayed readout

Config: patch residual L{INTERVENTION_LAYER} at the last {POSITIONS} prompt positions. The
detector reads L{EARLY_LAYER}, L{PEAK_LAYER}, and L{OUTPUT_LAYER}. The Qwen template starts the
assistant thinking section in the input. Later states consume the same forced thought tokens with
no additional patch.

Forced continuation (`repr`):

```python
{result['forced_text']!r}
```

{table}

TODO validate: a donor-like delayed readout requires a change in the selected rows that persists
after identical continuation tokens. Projection shares alone do not establish semantic transfer.

Raw artifact: `result.json`.

-- Codex/gpt-5
"""


def replacement_hooks(source, target, layer: int, positions: int, strength: float, record=None):
    return intervention_hooks(
        source["basis"],
        target["basis"],
        target["residuals"],
        operation="replace",
        strength=strength,
        blocks_to_hook=[layer - 1],
        positions=positions,
        source_position=source["content_end"] - 1,
        target_position=target["content_end"] - 1,
        prefill_only=True,
        record=record,
    )


def token_distribution(tokenizer, logits, base_logits=None) -> list[dict]:
    logp = logits.float().log_softmax(-1)
    base_logp = base_logits.float().log_softmax(-1) if base_logits is not None else None
    rows = []
    for token_id in logp.topk(10).indices:
        row = {
            "token_id": int(token_id),
            "token": tokenizer.decode([int(token_id)]),
            "logp": float(logp[token_id]),
            "p": float(logp[token_id].exp()),
        }
        if base_logp is not None:
            row["delta_logp"] = float(logp[token_id] - base_logp[token_id])
        rows.append(row)
    return rows


def distribution_table(rows: list[dict]) -> str:
    include_delta = "delta_logp" in rows[0]
    values = []
    for rank, row in enumerate(rows, start=1):
        values.append([
            rank,
            repr(row["token"]),
            f'{row["logp"]:.3f}',
            f'{row["p"]:.6f}',
            *([f'{row["delta_logp"]:+.3f}'] if include_delta else []),
        ])
    headers = ["rank", "token", "log p", "p"]
    if include_delta:
        headers.append("change in log p")
    return tabulate(values, headers=headers, tablefmt="pipe", disable_numparse=True)


def persistence_score_table(tokens: list[str], scores_by_position: list[list[float]]) -> str:
    rows = []
    for index, token in enumerate(tokens):
        scores = [position[index] for position in scores_by_position]
        rows.append([repr(token), f"{min(scores):.3f}", *(f"{score:.3f}" for score in scores)])
    return tabulate(
        rows,
        headers=["token", "minimum", "position −3", "position −2", "position −1", "position 0"],
        tablefmt="pipe",
        disable_numparse=True,
    )


def persistence_diagnostics(source, target) -> list[dict]:
    rows = []
    for layer in SWEEP_LAYERS:
        source_end = source["content_end"]
        source_h = source["residuals"][layer, source_end - 4:source_end].float()
        target_h = target["residuals"][layer, target["content_end"] - 1].float()
        source_component = component(source_h, source["basis"])
        fixed_target_component = component(target_h, target["basis"]).expand_as(source_component)
        target_component = match_norm(fixed_target_component, source_component)
        delta = target_component - source_component

        def cosine_to_final(x):
            return torch.nn.functional.cosine_similarity(x, x[-1][None], dim=-1).tolist()

        rows.append({
            "layer": layer,
            "source_component_cosine_to_final": cosine_to_final(source_component),
            "target_component_cosine_to_final": cosine_to_final(target_component),
            "replacement_delta_cosine_to_final": cosine_to_final(delta),
            "C1_relative_perturbation_by_position": (
                delta.norm(dim=-1) / source_h.norm(dim=-1)
            ).tolist(),
        })
    return rows


def sweep_report(result: dict) -> str:
    sweep_rows = []
    for rank, row in enumerate(result["sweep"][:64], start=1):
        sweep_rows.append([
            rank,
            row["layer"],
            row["positions"],
            row["C"],
            f'{row["log_odds_shift"]:+.3f}',
            f'{row["p4"]:.6f}',
            f'{row["p8"]:.6f}',
            f'{row["relative_perturbation"]:.3f}',
        ])
    sweep_table = tabulate(
        sweep_rows,
        headers=["rank ↓", "layer", "positions", "C", "Δ log-odds ↑", "p(4) ↑", "p(8) ↓", "‖δ‖/‖h‖"],
        tablefmt="pipe",
        disable_numparse=True,
    )
    suffix_rows = []
    for row in result["persistence_diagnostics"]:
        suffix_rows.append([
            row["layer"],
            f'{min(row["source_component_cosine_to_final"]):+.3f}',
            f'{min(row["target_component_cosine_to_final"]):+.3f}',
            f'{min(row["replacement_delta_cosine_to_final"]):+.3f}',
            " ".join(f'{x:.3f}' for x in row["C1_relative_perturbation_by_position"]),
        ])
    suffix_table = tabulate(
        suffix_rows,
        headers=["layer", "min source cos", "min donor cos", "min delta cos", "C1 ‖δᵢ‖/‖hᵢ‖, oldest→last"],
        tablefmt="pipe",
        disable_numparse=True,
    )
    base = result["demo"]["base"]
    changed = result["demo"]["causal"]
    best = result["best"]
    return f"""# Layer × content length × C sweep

One score ranks all conditions:

```text
Δ log-odds = [log p(4) - log p(8)]intervention - [log p(4) - log p(8)]Base
```

The source and donor use the pinned Qwen chat template with thinking disabled. Extraction and
generation receive the same token IDs. This is a development sweep; the selected condition is
not held-out confirmation.

## Sweep: top 64 of {len(result['sweep'])}

{sweep_table}

## Is the selected readout persistent?

The basis contains the tokens with the highest minimum suppressed score across four user-content positions.
Each cosine compares a content position with the final content position. The donor direction is
fixed; only its norm is matched separately at each source position.

Source content tokens: `{result['source_persistence_input_tokens']!r}`

{persistence_score_table(base['readout'], result['source_persistence_scores_by_position'])}

Donor content tokens: `{result['target_persistence_input_tokens']!r}`

{persistence_score_table(result['target_readout'], result['target_persistence_scores_by_position'])}

{suffix_table}

## Base

Input to the model (`repr`):

```python
{result['source_rendered_prompt']!r}
```

Readout:

```python
{base['readout']!r}
```

Per-position readouts (oldest to last): `{base['readout_by_position']!r}`

Generation ({len(base['generation']['token_ids'])} tokens through EOS, verbatim):

```text
{base['generation']['text']}
```

{distribution_table(base['top_tokens'])}

## Best intervention selected by the sweep

Layer L{best['layer']}, last {best['positions']} prompt position(s), C={best['C']};
Δ log-odds={best['log_odds_shift']:+.3f}, ‖δ‖/‖h‖={best['relative_perturbation']:.3f}.

Input to the model (`repr`, unchanged):

```python
{result['source_rendered_prompt']!r}
```

Readout after intervention:

```python
{changed['readout']!r}
```

Per-position readouts (oldest to last): `{changed['readout_by_position']!r}`

Generation ({len(changed['generation']['token_ids'])} tokens through EOS, verbatim):

```text
{changed['generation']['text']}
```

{distribution_table(changed['top_tokens'])}

Donor input (`repr`):

```python
{result['target_rendered_prompt']!r}
```

TODO validate: a large selected log-odds shift can be answer-state steering without dog-semantic
transfer. Confirm the selected condition on prompts not used by this sweep.

Raw artifact: `result.json`.

-- Codex/gpt-5
"""


def run_sweep(output_dir: Path) -> None:
    torch.set_grad_enabled(False)
    output_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16
    ).cuda().eval()
    blocks = model.model.layers
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight
    source = extract(
        model, tokenizer, final_norm, unembedding, norm_gain, SOURCE_PROMPT,
        enable_thinking=False,
    )
    target = extract(
        model, tokenizer, final_norm, unembedding, norm_gain, TARGET_PROMPT,
        enable_thinking=False,
    )
    base_logits = source["logits"]
    source_id = one_token(tokenizer, "8")
    target_id = one_token(tokenizer, "4")
    base_logp = base_logits.log_softmax(-1)
    base_log_odds = float(base_logp[target_id] - base_logp[source_id])
    sweep_positions = (*SWEEP_POSITIONS, source["content_end"] - source["content_start"])
    rows = []
    for layer in SWEEP_LAYERS:
        for positions in sweep_positions:
            for strength in SWEEP_STRENGTHS:
                record = {}
                hooks = replacement_hooks(source, target, layer, positions, strength, record)
                logits = run_forward(model, source["input_ids"], blocks, hooks)
                logp = logits.log_softmax(-1)
                patch = record[layer]
                rows.append({
                    "layer": layer,
                    "positions": positions,
                    "C": strength,
                    "log_odds_shift": float(logp[target_id] - logp[source_id] - base_log_odds),
                    "p4": float(logp[target_id].exp()),
                    "p8": float(logp[source_id].exp()),
                    "relative_perturbation": patch["perturbation_norm"] / patch["residual_norm"],
                    "relative_perturbation_by_position": patch["relative_perturbation_by_position"],
                })
    rows.sort(key=lambda row: row["log_odds_shift"], reverse=True)
    best = rows[0]
    best_hooks = replacement_hooks(
        source, target, best["layer"], best["positions"], best["C"]
    )
    with layer_hooks(blocks, best_hooks):
        changed_residuals, changed_logits = trajectory(
            model, source["input_ids"], final_norm
        )
    changed_readout = persistent_readout(
        changed_residuals, source["content_end"], tokenizer, unembedding, norm_gain
    )
    base_generation = generate(
        model, tokenizer, source["input_ids"], blocks, {}, max_new_tokens=DEMO_TOKENS
    )
    changed_generation = generate(
        model, tokenizer, source["input_ids"], blocks, best_hooks, max_new_tokens=DEMO_TOKENS
    )
    result = {
        "config": {
            "model": MODEL,
            "revision": REVISION,
            "layers": SWEEP_LAYERS,
            "positions": sweep_positions,
            "basis_persistence_positions": PERSISTENCE_POSITIONS,
            "strengths": SWEEP_STRENGTHS,
            "metric": "change in target-vs-source log odds",
            "git": subprocess.run(
                ["git", "describe", "--always", "--dirty"], cwd=ROOT, check=True,
                text=True, capture_output=True,
            ).stdout.strip(),
        },
        "source_content": SOURCE_PROMPT,
        "target_content": TARGET_PROMPT,
        "source_rendered_prompt": source["rendered_prompt"],
        "target_rendered_prompt": target["rendered_prompt"],
        "target_readout": target["selected"],
        "source_input_ids": source["input_ids"][0].tolist(),
        "generation_input_ids": source["input_ids"][0].tolist(),
        "base_log_odds": base_log_odds,
        "source_persistence_input_tokens": source["persistence_input_tokens"],
        "target_persistence_input_tokens": target["persistence_input_tokens"],
        "source_persistence_scores_by_position": source["persistence_scores_by_position"],
        "target_persistence_scores_by_position": target["persistence_scores_by_position"],
        "persistence_diagnostics": persistence_diagnostics(source, target),
        "sweep": rows,
        "best": best,
        "demo": {
            "base": {
                "readout": source["selected"],
                "readout_by_position": source["selected_by_position"],
                "generation": base_generation,
                "top_tokens": token_distribution(tokenizer, base_logits),
            },
            "causal": {
                "readout": changed_readout["selected"],
                "readout_by_position": changed_readout["selected_by_position"],
                "generation": changed_generation,
                "top_tokens": token_distribution(tokenizer, changed_logits, base_logits),
            },
        },
    }
    (output_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "run.md").write_text(sweep_report(result))
    logger.info("wrote {}", output_dir / "run.md")


def main(output_dir: Path) -> None:
    torch.set_grad_enabled(False)
    output_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=torch.bfloat16).cuda().eval()
    blocks = model.model.layers
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight
    source = extract(model, tokenizer, final_norm, unembedding, norm_gain, SOURCE_PROMPT)
    target = extract(model, tokenizer, final_norm, unembedding, norm_gain, TARGET_PROMPT)
    generation_input_ids = source["input_ids"]
    assert torch.equal(source["input_ids"], generation_input_ids)
    forced_ids = generate(model, tokenizer, generation_input_ids, blocks, {}, max_new_tokens=FORCED_TOKENS)["token_ids"]
    result = {
        "config": {
            "model": MODEL,
            "revision": REVISION,
            "early_layer": EARLY_LAYER,
            "peak_layer": PEAK_LAYER,
            "output_layer": OUTPUT_LAYER,
            "intervention_layer": INTERVENTION_LAYER,
            "positions": POSITIONS,
            "forced_tokens": FORCED_TOKENS,
            "git": subprocess.run(
                ["git", "describe", "--always", "--dirty"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip(),
        },
        "source_content": SOURCE_PROMPT,
        "target_content": TARGET_PROMPT,
        "source_rendered_prompt": source["rendered_prompt"],
        "target_rendered_prompt": target["rendered_prompt"],
        "source_input_ids": source["input_ids"][0].tolist(),
        "generation_input_ids": generation_input_ids[0].tolist(),
        "target_input_ids": target["input_ids"][0].tolist(),
        "forced_token_ids": forced_ids,
        "forced_text": tokenizer.decode(forced_ids, skip_special_tokens=False),
        "conditions": {
            "base": condition(model, tokenizer, final_norm, blocks, source, target, unembedding, norm_gain, forced_ids, 0.0),
            "replace_C1": condition(model, tokenizer, final_norm, blocks, source, target, unembedding, norm_gain, forced_ids, 1.0),
            "replace_C4": condition(model, tokenizer, final_norm, blocks, source, target, unembedding, norm_gain, forced_ids, 4.0),
        },
    }
    (output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (output_dir / "run.md").write_text(report(result))
    logger.info("wrote {}", output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sweep", action="store_true")
    args = parser.parse_args()
    (run_sweep if args.sweep else main)(args.output_dir)
