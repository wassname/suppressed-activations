# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""One-at-a-time intervention sweep. Written by Codex/gpt-5.6-sol."""

from __future__ import annotations

import argparse
import json
import re
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
    intervention_layer: int | tuple[int, ...] = 1
    intervention_positions: int | str = "all"
    strength: float = 4.0
    match_component_norm: bool = True
    restore_residual_norm: bool = True
    donor_position_offset: int = 0
    lexical_forms: str = "detector"
    lexical_divisor: int = 1
    continue_generation: bool = False


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


def normalization_strength_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for match_component_norm in (True, False):
        for restore_residual_norm in (True, False):
            for strength in (4.0, 8.0, 16.0, 32.0, 64.0):
                value = (
                    f"C={strength:g},component_norm={match_component_norm},"
                    f"residual_norm={restore_residual_norm}"
                )
                rows.append((
                    "normalization_strength",
                    value,
                    replace(
                        DEFAULT,
                        strength=strength,
                        match_component_norm=match_component_norm,
                        restore_residual_norm=restore_residual_norm,
                    ),
                ))
    return rows


LEXICAL_PAIRS = (
    ("Spider", "Dog"),
    (" Spider", " Dog"),
    (" spider", " dog"),
    (" spiders", " dogs"),
    ("\nspider", "\ndog"),
    ("\n spider", "\n dog"),
    ("\nSpider", "\nDog"),
)


def lexical_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for pair_index in range(len(LEXICAL_PAIRS)):
        for strength in (1.0, 2.0, 4.0, 8.0):
            value = f"pair={pair_index + 1},C={strength:g}"
            rows.append(("lexical_surface", value, replace(
                DEFAULT, lexical_forms=f"pair_{pair_index + 1}", strength=strength,
            )))
    for divisor in (1, 2, 4):
        for strength in (1.0, 2.0, 4.0, 8.0):
            value = f"union,C={strength:g},divide={divisor}"
            rows.append(("lexical_surface", value, replace(
                DEFAULT,
                lexical_forms="union",
                lexical_divisor=divisor,
                strength=strength / divisor,
            )))
    return rows


def layer_position_strength_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for intervention_layer in (8, 12, 16, 20, 23, 24, 26, 28, 30, 32):
        for intervention_positions in (1, 2, 4):
            for strength in (1.0, 2.0, 4.0, 8.0, 16.0):
                value = (
                    f"L={intervention_layer},positions={intervention_positions},"
                    f"C={strength:g}"
                )
                rows.append((
                    "layer_position_strength",
                    value,
                    replace(
                        DEFAULT,
                        intervention_layer=intervention_layer,
                        intervention_positions=intervention_positions,
                        strength=strength,
                    ),
                ))
    return rows


def layer_combo_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for intervention_layers in ((24,), (26,), (24, 26), (23, 24, 25, 26)):
        for intervention_positions in (1, 4):
            for strength in (1.0, 2.0, 4.0, 8.0):
                layers = "+".join(map(str, intervention_layers))
                value = f"L={layers},positions={intervention_positions},C={strength:g}"
                rows.append((
                    "layer_combo",
                    value,
                    replace(
                        DEFAULT,
                        intervention_layer=intervention_layers,
                        intervention_positions=intervention_positions,
                        strength=strength,
                    ),
                ))
    return rows


def persistent_generation_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for intervention_layers in ((24,), (26,), (24, 26), (23, 24, 25, 26)):
        for intervention_positions in (1, 4):
            for strength in (0.25, 0.5, 1.0, 2.0):
                layers = "+".join(map(str, intervention_layers))
                value = f"L={layers},positions={intervention_positions},C={strength:g}"
                rows.append((
                    "persistent_generation",
                    value,
                    replace(
                        DEFAULT,
                        intervention_layer=intervention_layers,
                        intervention_positions=intervention_positions,
                        strength=strength,
                        continue_generation=True,
                    ),
                ))
    return rows


def first_answer(text: str) -> str | None:
    match = re.search(r"(?<!\d)([48])(?!\d)", text)
    return None if match is None else match.group(1)


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


def lexical_subspaces(tokenizer, unembedding, norm_gain, lexical_forms: str):
    pairs = (
        LEXICAL_PAIRS
        if lexical_forms == "union"
        else (LEXICAL_PAIRS[int(lexical_forms.removeprefix("pair_")) - 1],)
    )
    centered = unembedding.float() - unembedding.float().mean(0)

    def basis(forms):
        token_ids_by_form = [
            tokenizer(form, add_special_tokens=False).input_ids for form in forms
        ]
        directions = torch.stack([
            (centered[token_ids] * norm_gain.float()).mean(0)
            for token_ids in token_ids_by_form
        ])
        return torch.linalg.qr(directions.T, mode="reduced").Q

    return basis([source for source, _ in pairs]), basis([target for _, target in pairs])


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
        if key not in {
            "top_tokens", "generation", "readout", "target_readout", "config",
            "intervention_record",
        }
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

Measured intervention norms:

```json
{json.dumps(row['intervention_record'], ensure_ascii=False, indent=2)}
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


def run(output_dir: Path, sweep: str, prompt_mode: str) -> None:
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
        if prompt_mode == "raw":
            input_ids = tokenizer(
                content, add_special_tokens=False, return_tensors="pt"
            ).input_ids.cuda()
            chat = {"input_ids": input_ids, "content_start": 0, "content_end": input_ids.shape[1]}
        elif prompt_mode == "chat-fact":
            chat = chat_input_ids(tokenizer, content, enable_thinking=False, instruction="")
        elif prompt_mode == "chat-instructed":
            chat = chat_input_ids(tokenizer, content, enable_thinking=False)
        else:
            raise ValueError(prompt_mode)
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

    sweep_configs = {
        "oat": configs,
        "normalization-strength": normalization_strength_configs,
        "lexical-surface": lexical_configs,
        "layer-position-strength": layer_position_strength_configs,
        "layer-combo": layer_combo_configs,
        "persistent-generation": persistent_generation_configs,
    }[sweep]()
    rows = []
    for index, (axis, value, cfg) in enumerate(sweep_configs):
        _, target_ids, _ = subspace(target, cfg, unembedding, norm_gain)
        if cfg.lexical_forms == "detector":
            source_basis, _, _ = subspace(source, cfg, unembedding, norm_gain)
            target_basis, _, _ = subspace(target, cfg, unembedding, norm_gain)
        else:
            source_basis, target_basis = lexical_subspaces(
                tokenizer, unembedding, norm_gain, cfg.lexical_forms
            )
        positions = (
            source["content_end"] - source["content_start"]
            if cfg.intervention_positions == "all"
            else cfg.intervention_positions
        )
        intervention_record = {}
        intervention_layers = (
            (cfg.intervention_layer,)
            if isinstance(cfg.intervention_layer, int)
            else cfg.intervention_layer
        )
        hooks = intervention_hooks(
            source_basis,
            target_basis,
            target["residuals"],
            operation="replace",
            strength=cfg.strength,
            blocks_to_hook=[layer - 1 for layer in intervention_layers],
            positions=positions,
            source_position=source["content_end"] - 1,
            target_position=target["content_end"] - 1 - cfg.donor_position_offset,
            match_component_norm=cfg.match_component_norm,
            restore_norm=cfg.restore_residual_norm,
            prefill_only=not cfg.continue_generation,
            record=intervention_record,
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
        condition_id = re.sub(r"[^A-Za-z0-9_.=-]+", "_", f"{index:03d}_{axis}_{value}")
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
            "first_answer": first_answer(generation["text"]),
            "source_fact_preserved": "spins webs" in generation["text"],
            "readout_overlap": len(set(readout) & set(target_readout)) / cfg.rank,
            "intervention_record": intervention_record,
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
        logger.info("{}/{} {}", index + 1, len(sweep_configs), condition_id)

    result = {
        "model": MODEL,
        "revision": REVISION,
        "git": subprocess.run(
            ["git", "describe", "--always", "--dirty"], cwd=ROOT, check=True,
            text=True, capture_output=True,
        ).stdout.strip(),
        "default": asdict(DEFAULT),
        "prompt_mode": prompt_mode,
        "lexical_pairs": LEXICAL_PAIRS if sweep == "lexical-surface" else None,
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
    parser.add_argument(
        "--sweep",
        choices=(
            "oat", "normalization-strength", "lexical-surface",
            "layer-position-strength", "layer-combo",
            "persistent-generation",
        ),
        default="oat",
    )
    parser.add_argument(
        "--prompt-mode",
        choices=("raw", "chat-fact", "chat-instructed"),
        default="chat-instructed",
    )
    args = parser.parse_args()
    run(args.output_dir, args.sweep, args.prompt_mode)
