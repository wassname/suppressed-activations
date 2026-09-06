# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""One-at-a-time intervention sweep. Written by Codex/gpt-5.6-sol."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import torch
from loguru import logger
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.delayed_readout import (
    MODEL,
    REVISION,
    SOURCE_PROMPT,
    TARGET_PROMPT,
    chat_input_ids,
    distribution_table,
    token_distribution,
)
from scripts.demo import intervention_hooks, layer_hooks, one_token, trajectory
from suppressed_activation_subspace import (
    persistent_suppressed_activation_subspace,
    union_suppressed_activation_subspace,
)


@dataclass(frozen=True)
class Config:
    aggregation: str = "union"
    detector_layers: tuple[int, int, int] = (23, 25, 32)
    readout_positions: int = 4
    rank: int = 8
    intervention_layer: int = 1
    intervention_positions: int | str = "all"
    strength: float = 4.0
    match_component_norm: bool = True
    restore_residual_norm: bool = True
    donor_position_offset: int = 0


DEFAULT = Config()
AXES = {
    "aggregation": ["persistent", "union"],
    "detector_layers": [(8, 16, 24), (12, 20, 28), (16, 24, 32), (20, 26, 32), (23, 25, 32)],
    "readout_positions": [1, 2, 4, 8],
    "rank": [4, 8, 16, 32],
    "intervention_layer": list(range(1, 33)),
    "intervention_positions": [1, 2, 3, 4, 8, "all"],
    "strength": [0.25, 0.5, 1.0, 2.0, 4.0, 8.0],
    "match_component_norm": [False, True],
    "restore_residual_norm": [False, True],
    "donor_position_offset": [0, 1, 2, 3],
}


def configs() -> list[tuple[str, str, Config]]:
    rows = [("default", "default", DEFAULT)]
    for axis, values in AXES.items():
        for value in values:
            candidate = replace(DEFAULT, **{axis: value})
            if candidate != DEFAULT:
                rows.append((axis, str(value), candidate))
    return rows


def subspace(sample, cfg: Config, unembedding, norm_gain):
    end = sample["content_end"]
    residuals = sample["residuals"][:, end - cfg.readout_positions:end].permute(1, 0, 2)
    selector = {
        "persistent": persistent_suppressed_activation_subspace,
        "union": union_suppressed_activation_subspace,
    }[cfg.aggregation]
    basis, token_ids, scores = selector(
        residuals,
        unembedding,
        norm_gain,
        early_layer=cfg.detector_layers[0],
        peak_layer=cfg.detector_layers[1],
        output_layer=cfg.detector_layers[2],
        rank=cfg.rank,
        normalize_unembedding_rows=True,
    )
    return basis[0], token_ids[0], scores


def repetition_bigram_fraction(token_ids: list[int], special_ids: set[int]) -> float:
    ids = [token_id for token_id in token_ids if token_id not in special_ids]
    bigrams = list(zip(ids, ids[1:]))
    return 0.0 if not bigrams else 1 - len(set(bigrams)) / len(bigrams)


def generate_with_first_logits(model, tokenizer, input_ids, blocks, hooks) -> tuple[dict, torch.Tensor]:
    with layer_hooks(blocks, hooks), torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            do_sample=False,
            max_new_tokens=32,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
            return_dict_in_generate=True,
            output_scores=True,
        )
    token_ids = output.sequences[0, input_ids.shape[1]:].tolist()
    first_logits = output.scores[0][0].float()
    if token_ids[0] != int(first_logits.argmax()):
        raise ValueError("generated first token differs from cached prefill argmax")
    return {
        "token_ids": token_ids,
        "text": tokenizer.decode(token_ids, skip_special_tokens=False),
    }, first_logits


def yaml_value(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def condition_report(row: dict, source_prompt: str, target_prompt: str) -> str:
    frontmatter = "\n".join(
        f"{key}: {yaml_value(value)}"
        for key, value in row.items()
        if key not in {"top_tokens", "generation", "readout", "target_readout", "config"}
    )
    return f"""---
{frontmatter}
---

# {row['condition_id']}

Resolved config:

```json
{json.dumps(row['config'], ensure_ascii=False, indent=2)}
```

Source input (`repr`):

```python
{source_prompt!r}
```

Donor input (`repr`):

```python
{target_prompt!r}
```

Readout after intervention:

```python
{row['readout']!r}
```

Unmodified donor readout:

```python
{row['target_readout']!r}
```

Generation ({row['generation_tokens']} tokens, verbatim):

```text
{row['generation']['text']}
```

{distribution_table(row['top_tokens'])}

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
"""


def run(output_dir: Path) -> None:
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

    def sample(content):
        chat = chat_input_ids(tokenizer, content, enable_thinking=False)
        residuals, logits = trajectory(model, chat["input_ids"], final_norm)
        return {**chat, "residuals": residuals, "logits": logits}

    source = sample(SOURCE_PROMPT)
    target = sample(TARGET_PROMPT)
    source_id = one_token(tokenizer, "8")
    target_id = one_token(tokenizer, "4")
    base_generation, base_generation_logits = generate_with_first_logits(
        model, tokenizer, source["input_ids"], blocks, {}
    )
    base_logp = base_generation_logits.log_softmax(-1)
    base_log_odds = float(base_logp[target_id] - base_logp[source_id])
    special_ids = set(tokenizer.all_special_ids)
    source_rendered = tokenizer.decode(source["input_ids"][0], skip_special_tokens=False)
    target_rendered = tokenizer.decode(target["input_ids"][0], skip_special_tokens=False)

    rows = []
    for index, (axis, value, cfg) in enumerate(configs()):
        source_basis, _, _ = subspace(source, cfg, unembedding, norm_gain)
        target_basis, target_ids, _ = subspace(target, cfg, unembedding, norm_gain)
        positions = (
            source["content_end"] - source["content_start"]
            if cfg.intervention_positions == "all"
            else cfg.intervention_positions
        )
        hooks = intervention_hooks(
            source_basis,
            target_basis,
            target["residuals"],
            operation="replace",
            strength=cfg.strength,
            blocks_to_hook=[cfg.intervention_layer - 1],
            positions=positions,
            source_position=source["content_end"] - 1,
            target_position=target["content_end"] - 1 - cfg.donor_position_offset,
            match_component_norm=cfg.match_component_norm,
            restore_norm=cfg.restore_residual_norm,
            prefill_only=True,
        )
        with layer_hooks(blocks, hooks):
            changed_residuals, logits = trajectory(model, source["input_ids"], final_norm)
        _, changed_ids, _ = subspace(
            {**source, "residuals": changed_residuals}, cfg, unembedding, norm_gain
        )
        readout = [tokenizer.decode([int(token_id)]) for token_id in changed_ids]
        target_readout = [tokenizer.decode([int(token_id)]) for token_id in target_ids]
        generation, generation_logits = generate_with_first_logits(
            model, tokenizer, source["input_ids"], blocks, hooks
        )
        logp = generation_logits.log_softmax(-1)
        condition_id = f"{index:03d}_{axis}_{value}".replace(" ", "_").replace("/", "-")
        condition_dir = output_dir / "conditions" / condition_id
        condition_dir.mkdir(parents=True)
        row = {
            "condition_id": condition_id,
            "axis": axis,
            "value": value,
            "is_default": axis == "default",
            "swap_log_odds_shift": float(logp[target_id] - logp[source_id] - base_log_odds),
            "valid_answer_mass": float(logp[target_id].exp() + logp[source_id].exp()),
            "p4": float(logp[target_id].exp()),
            "p8": float(logp[source_id].exp()),
            "repeated_bigram_fraction": repetition_bigram_fraction(
                generation["token_ids"], special_ids
            ),
            "generation_tokens": len(generation["token_ids"]),
            "first_token": tokenizer.decode(generation["token_ids"][:1]),
            "readout_overlap": len(set(readout) & set(target_readout)) / cfg.rank,
            "log": str((condition_dir / "run.md").relative_to(output_dir)),
            "config": asdict(cfg),
            "readout": readout,
            "target_readout": target_readout,
            "generation": generation,
            "top_tokens": token_distribution(tokenizer, generation_logits, base_generation_logits),
        }
        (condition_dir / "run.md").write_text(
            condition_report(row, source_rendered, target_rendered)
        )
        rows.append(row)
        logger.info("{}/{} {}", index + 1, len(configs()), condition_id)

    result = {
        "model": MODEL,
        "revision": REVISION,
        "git": subprocess.run(
            ["git", "describe", "--always", "--dirty"], cwd=ROOT, check=True,
            text=True, capture_output=True,
        ).stdout.strip(),
        "default": asdict(DEFAULT),
        "base": {
            "p4": float(base_logp[target_id].exp()),
            "p8": float(base_logp[source_id].exp()),
            "generation": base_generation,
        },
        "rows": rows,
    }
    (output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/results.py"), str(output_dir)], check=True
    )
    logger.info("wrote {}", output_dir / "run.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    run(parser.parse_args().output_dir)
