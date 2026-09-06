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

from scripts.demo import generate, intervention_hooks, layer_hooks, top_tokens, trajectory
from suppressed_activation_subspace import component, suppressed_activation_subspace

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
FORCED_TOKENS = 4


def chat_input_ids(tokenizer, content: str) -> torch.Tensor:
    encoded = tokenizer.apply_chat_template(
        [{"role": "user", "content": INSTRUCTION + content}],
        tokenize=True,
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt",
    )
    return encoded.input_ids.cuda()


def extract(model, tokenizer, final_norm, unembedding, norm_gain, content: str) -> dict:
    input_ids = chat_input_ids(tokenizer, content)
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
        "rendered_prompt": tokenizer.decode(input_ids[0], skip_special_tokens=False),
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


def projection_share(residuals, basis) -> float:
    h = residuals[INTERVENTION_LAYER, -1].float()
    return float(component(h, basis).norm() / h.norm())


def condition(
    model, tokenizer, final_norm, blocks, source, target, unembedding, norm_gain, forced_ids, strength: float
) -> dict:
    hooks = intervention_hooks(
        source["basis"],
        target["basis"],
        target["residuals"],
        operation="replace",
        strength=strength,
        blocks_to_hook=[INTERVENTION_LAYER - 1],
        positions=POSITIONS,
        prefill_only=True,
    )
    trajectories = cached_trajectories(
        model, final_norm, blocks, source["input_ids"], forced_ids, hooks
    )
    return {
        "strength": strength,
        "readouts": [readout(x, tokenizer, unembedding, norm_gain) for x in trajectories],
        "source_projection_share": [projection_share(x, source["basis"]) for x in trajectories],
        "target_projection_share": [projection_share(x, target["basis"]) for x in trajectories],
        "top_tokens": [top_tokens(tokenizer, x[-1, -1].float() @ unembedding.float().T, k=5) for x in trajectories],
    }


def report(result: dict) -> str:
    rows = []
    for name, item in result["conditions"].items():
        for step, selected in enumerate(item["readouts"]):
            rows.append([
                name,
                "prompt" if step == 0 else f"forced {step}",
                repr(selected),
                f"{item['source_projection_share'][step]:.4f}",
                f"{item['target_projection_share'][step]:.4f}",
            ])
    table = tabulate(
        rows,
        headers=["condition", "state", "readout", "source share", "donor share"],
        tablefmt="pipe",
        disable_numparse=True,
    )
    return f"""# Delayed readout

Config: patch residual L{INTERVENTION_LAYER} at the last {POSITIONS} prompt positions. The
detector reads L{EARLY_LAYER}, L{PEAK_LAYER}, and L{OUTPUT_LAYER}. Later states consume the same
forced tokens with no additional patch.

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


def main(output_dir: Path) -> None:
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
    main(parser.parse_args().output_dir)
