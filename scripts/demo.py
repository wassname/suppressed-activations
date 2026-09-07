# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Replace one sample's suppressed component with another's. Written by PI/gpt-5.4."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch import Tensor
from transformers import AutoModelForCausalLM, AutoTokenizer

from suppressed_activation_subspace import (
    matched_random_rotation,
    random_basis_like,
    remove,
    replace,
    suppressed_activation_subspace,
)

MODEL = "Qwen/Qwen3.5-4B"
EARLY_LAYER = 23
PEAK_LAYER = 25
OUTPUT_LAYER = 32
RANK = 8
CONTROL_STRENGTH = 2.0
RANDOM_CONTROL_COUNT = 256
INTERVENTION_BLOCKS = range(22, 30)  # block 22 writes residual L23
MAX_NEW_TOKENS = 64
SOURCE_PROMPT = "Fact: The number of legs on the animal that spins webs is "
TARGET_PROMPT = "Fact: The number of legs on the animal that barks and is called man's best friend is "
SOURCE_HIDDEN_WORD = "spider"
TARGET_HIDDEN_WORD = "dog"
SOURCE_OUTPUT = "8"
TARGET_OUTPUT = "4"


def one_token(tokenizer, text: str) -> int:
    ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(ids) != 1:
        raise ValueError(f"{text!r} is {len(ids)} tokens: {ids}")
    return ids[0]


def replace_output(output, hidden: Tensor):
    return (hidden, *output[1:]) if isinstance(output, tuple) else hidden


@contextmanager
def layer_hooks(blocks, hook_by_layer: dict[int, object]):
    handles = [blocks[layer].register_forward_hook(hook) for layer, hook in hook_by_layer.items()]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


def trajectory(model, input_ids: Tensor, final_norm) -> tuple[Tensor, Tensor]:
    raw_final: dict[str, Tensor] = {}
    handle = final_norm.register_forward_pre_hook(
        lambda _module, inputs: raw_final.__setitem__("hidden", inputs[0].detach())
    )
    with torch.no_grad():
        output = model(input_ids=input_ids, output_hidden_states=True, use_cache=False)
    handle.remove()
    residuals = torch.stack(
        [hidden[0] for hidden in output.hidden_states[:-1]] + [raw_final["hidden"][0]]
    )
    return residuals, output.logits[0, -1].float()


def top_tokens(tokenizer, logits: Tensor, k: int = 5) -> list[dict]:
    logp = logits.float().log_softmax(-1)
    return [
        {"token_id": int(token_id), "token": tokenizer.decode([token_id]), "logp": float(logp[token_id])}
        for token_id in logp.topk(k).indices
    ]


def metrics(tokenizer, logits: Tensor, clean_logits: Tensor, source_id: int, target_id: int) -> dict:
    logp = logits.float().log_softmax(-1)
    clean_logp = clean_logits.float().log_softmax(-1)
    clean_p = clean_logp.exp()
    return {
        "top": top_tokens(tokenizer, logits),
        "p_source": float(logp[source_id].exp()),
        "p_target": float(logp[target_id].exp()),
        "log_odds_target_vs_source": float(logp[target_id] - logp[source_id]),
        "kl_from_clean": float(torch.sum(clean_p * (clean_logp - logp))),
    }


def intervention_hooks(
    source_basis: Tensor,
    target_basis: Tensor,
    target_residuals: Tensor,
    *,
    operation: str,
    strength: float = 1.0,
    blocks_to_hook=INTERVENTION_BLOCKS,
    random_seed: int = 0,
    matched_distances: dict[int, float] | None = None,
    prefill_only: bool = False,
    positions: int = 1,
    source_position: int | None = None,
    target_position: int | None = None,
    match_component_norm: bool = True,
    restore_norm: bool = True,
    record: dict[int, dict] | None = None,
    fixed_deltas: dict[int, Tensor] | None = None,
    coordinate_directions: Tensor | None = None,
    source_dominant_only: bool = False,
) -> dict[int, object]:
    random_source = random_basis_like(source_basis, random_seed)
    random_target = random_basis_like(target_basis, random_seed + 1)

    def hook_for(block: int):
        residual_layer = block + 1

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            if prefill_only and hidden.shape[1] == 1:
                return output
            source_end = (
                hidden.shape[1]
                if source_position is None or hidden.shape[1] == 1
                else source_position + 1
            )
            active_positions = 1 if hidden.shape[1] == 1 else positions
            source_start = source_end - active_positions
            if source_start < 0 or source_end > hidden.shape[1]:
                raise ValueError(
                    f"cannot patch positions [{source_start}:{source_end}] in length {hidden.shape[1]}"
                )
            h = hidden[:, source_start:source_end].float()
            if target_position is None:
                if active_positions > target_residuals.shape[1]:
                    raise ValueError(f"target has only {target_residuals.shape[1]} positions")
                target_h = target_residuals[
                    residual_layer, -active_positions:
                ].unsqueeze(0).float()
            else:
                target_h = target_residuals[residual_layer, target_position].reshape(1, 1, -1)
                target_h = target_h.expand(h.shape[0], h.shape[1], -1).float()
            if operation == "coordinate_swap":
                coordinates = h @ torch.linalg.pinv(coordinate_directions).T
                coordinate_delta = coordinates.flip(-1) - coordinates
                if source_dominant_only:
                    coordinate_delta = coordinate_delta * (coordinates[..., :1] > coordinates[..., 1:])
                patched = h + strength * coordinate_delta @ coordinate_directions.T
                assert not restore_norm
            elif operation == "fixed_delta":
                patched = h + strength * fixed_deltas[residual_layer]
                if restore_norm:
                    patched = patched * h.norm(dim=-1, keepdim=True) / patched.norm(dim=-1, keepdim=True)
            elif operation == "replace":
                patched = replace(
                    h, source_basis, target_h, target_basis,
                    strength=strength,
                    match_component_norm=match_component_norm,
                    restore_norm=restore_norm,
                )
            elif operation == "random":
                if matched_distances is None:
                    raise ValueError("random controls require semantic perturbation norms")
                random_delta = replace(h, random_source, target_h, random_target) - h
                distance = torch.full_like(h[..., :1], matched_distances[residual_layer] * abs(strength))
                patched = matched_random_rotation(h, random_delta, distance)
            elif operation == "remove":
                patched = remove(h, source_basis, restore_norm=True)
            else:
                raise ValueError(operation)
            if record is not None and residual_layer not in record:
                residual_norms = h.norm(dim=-1)[0]
                perturbation_norms = (patched - h).norm(dim=-1)[0]
                record[residual_layer] = {
                    "prefill_positions": list(range(source_start, source_end)),
                    "decode_steps": 0,
                    "residual_norm": float(h.norm()),
                    "perturbation_norm": float((patched - h).norm()),
                    "relative_perturbation_by_position": (
                        perturbation_norms / residual_norms
                    ).tolist(),
                }
            if record is not None and hidden.shape[1] == 1:
                record[residual_layer]["decode_steps"] += 1
            if record is not None and operation == "coordinate_swap":
                record[residual_layer].setdefault("coordinate_trace", []).append({
                    "before": coordinates[0].tolist(),
                    "after": (patched @ torch.linalg.pinv(coordinate_directions).T)[0].tolist(),
                    "after_model_dtype": (patched.to(hidden.dtype).float() @ torch.linalg.pinv(coordinate_directions).T)[0].tolist(),
                })
            return replace_output(
                output,
                torch.cat(
                    [hidden[:, :source_start], patched.to(hidden.dtype), hidden[:, source_end:]],
                    dim=1,
                ),
            )

        return hook

    return {block: hook_for(block) for block in blocks_to_hook}


def run_forward(model, input_ids: Tensor, blocks, hooks: dict[int, object]) -> Tensor:
    with layer_hooks(blocks, hooks), torch.no_grad():
        return model(input_ids=input_ids, use_cache=False).logits[0, -1].float()


def generate(
    model,
    tokenizer,
    input_ids: Tensor,
    blocks,
    hooks: dict[int, object],
    *,
    max_new_tokens: int = MAX_NEW_TOKENS,
) -> dict:
    with layer_hooks(blocks, hooks), torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    ids = output[0, input_ids.shape[1]:].tolist()
    return {"token_ids": ids, "text": tokenizer.decode(ids, skip_special_tokens=False)}


def main(output_path: Path) -> None:
    torch.set_grad_enabled(False)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
    language_model = model.model
    blocks = language_model.layers
    final_norm = language_model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight

    source_ids = tokenizer(SOURCE_PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    target_ids = tokenizer(TARGET_PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    source_residuals, clean_logits = trajectory(model, source_ids, final_norm)
    target_residuals, _ = trajectory(model, target_ids, final_norm)

    source_basis, source_selected = suppressed_activation_subspace(
        source_residuals[:, -1][None], unembedding, norm_gain,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
        normalize_unembedding_rows=True,
    )
    target_basis, target_selected = suppressed_activation_subspace(
        target_residuals[:, -1][None], unembedding, norm_gain,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
        normalize_unembedding_rows=True,
    )
    source_basis, target_basis = source_basis[0], target_basis[0]
    source_output_id = one_token(tokenizer, SOURCE_OUTPUT)
    target_output_id = one_token(tokenizer, TARGET_OUTPUT)

    semantic_record: dict[int, dict] = {}
    replace_hooks = intervention_hooks(
        source_basis, target_basis, target_residuals,
        operation="replace", strength=CONTROL_STRENGTH, record=semantic_record,
    )
    with layer_hooks(blocks, replace_hooks):
        replaced_residuals, replace_logits = trajectory(model, source_ids, final_norm)
    _, replaced_selected = suppressed_activation_subspace(
        replaced_residuals[:, -1][None], unembedding, norm_gain,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
        normalize_unembedding_rows=True,
    )
    matched_distances = {
        layer: values["perturbation_norm"] for layer, values in semantic_record.items()
    }

    rows = [
        {"condition": "base", "metrics": metrics(
            tokenizer, clean_logits, clean_logits, source_output_id, target_output_id
        )},
        {"condition": "replace", "metrics": metrics(
            tokenizer, replace_logits, clean_logits, source_output_id, target_output_id
        )},
    ]
    random_hooks = {}
    random_record: dict[int, dict] = {}
    for seed in range(RANDOM_CONTROL_COUNT):
        record = random_record if seed == 0 else None
        hooks = intervention_hooks(
            source_basis, target_basis, target_residuals,
            operation="random", random_seed=seed,
            matched_distances=matched_distances, record=record,
        )
        if seed == 0:
            random_hooks = hooks
        logits = run_forward(model, source_ids, blocks, hooks)
        rows.append({
            "condition": f"random_seed={seed}",
            "metrics": metrics(tokenizer, logits, clean_logits, source_output_id, target_output_id),
        })

    remove_record: dict[int, dict] = {}
    remove_hooks = intervention_hooks(
        source_basis, target_basis, target_residuals,
        operation="remove", record=remove_record,
    )
    remove_logits = run_forward(model, source_ids, blocks, remove_hooks)
    rows.append({"condition": "remove", "metrics": metrics(
        tokenizer, remove_logits, clean_logits, source_output_id, target_output_id
    )})

    strengths = (-0.5, -0.25, -0.125, 0.125, 0.25, 0.5, 1.0, 2.0)
    strength_hooks = {
        strength: intervention_hooks(
            source_basis, target_basis, target_residuals,
            operation="replace", strength=strength,
        )
        for strength in strengths
    }
    for strength, hooks in strength_hooks.items():
        logits = replace_logits if strength == CONTROL_STRENGTH else run_forward(model, source_ids, blocks, hooks)
        rows.append({
            "condition": f"replace_C={strength:+g}",
            "metrics": metrics(tokenizer, logits, clean_logits, source_output_id, target_output_id),
        })

    generation_hooks = {
        "base": {},
        "replace": intervention_hooks(
            source_basis, target_basis, target_residuals,
            operation="replace", strength=CONTROL_STRENGTH, prefill_only=True,
        ),
        "random": intervention_hooks(
            source_basis, target_basis, target_residuals,
            operation="random", matched_distances=matched_distances, prefill_only=True,
        ),
        "remove": intervention_hooks(
            source_basis, target_basis, target_residuals,
            operation="remove", prefill_only=True,
        ),
    }
    generations = [
        {"condition": name, **generate(model, tokenizer, source_ids, blocks, hooks)}
        for name, hooks in generation_hooks.items()
    ]
    dose_generations = [
        {
            "condition": f"replace_C={strength:+g}",
            **generate(model, tokenizer, source_ids, blocks, hooks),
        }
        for strength, hooks in strength_hooks.items()
    ]
    diagnostics = {
        "replace": semantic_record,
        "random": random_record,
        "remove": remove_record,
    }

    result = {
        "metadata": {
            "git_describe": subprocess.run(
                ["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True
            ).stdout.strip(),
            "model": MODEL,
            "early_layer": EARLY_LAYER,
            "peak_layer": PEAK_LAYER,
            "output_layer": OUTPUT_LAYER,
            "intervention_residual_layers": [block + 1 for block in INTERVENTION_BLOCKS],
            "rank": RANK,
            "control_strength": CONTROL_STRENGTH,
            "random_control_count": RANDOM_CONTROL_COUNT,
            "score": "rise-and-fall divided by effective LM-head row norm",
            "max_new_tokens": MAX_NEW_TOKENS,
            "source_prompt": SOURCE_PROMPT,
            "target_prompt": TARGET_PROMPT,
            "source_hidden_word": SOURCE_HIDDEN_WORD,
            "target_hidden_word": TARGET_HIDDEN_WORD,
            "source_output": SOURCE_OUTPUT,
            "target_output": TARGET_OUTPUT,
        },
        "source_selected_tokens": [
            {"token_id": int(token_id), "token": tokenizer.decode([token_id])}
            for token_id in source_selected[0]
        ],
        "target_selected_tokens": [
            {"token_id": int(token_id), "token": tokenizer.decode([token_id])}
            for token_id in target_selected[0]
        ],
        "replaced_selected_tokens": [
            {"token_id": int(token_id), "token": tokenizer.decode([token_id])}
            for token_id in replaced_selected[0]
        ],
        "interventions": rows,
        "generations": generations,
        "dose_generations": dose_generations,
        "diagnostics": diagnostics,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    print("source selected:", [row["token"] for row in result["source_selected_tokens"]])
    print("target selected:", [row["token"] for row in result["target_selected_tokens"]])
    print("after replacement:", [row["token"] for row in result["replaced_selected_tokens"]])
    for row in rows:
        m = row["metrics"]
        print(
            f"{row['condition']:>16}: top={m['top'][0]['token']!r} "
            f"p({SOURCE_OUTPUT})={m['p_source']:.4f} p({TARGET_OUTPUT})={m['p_target']:.4f} "
            f"log p({TARGET_OUTPUT})/p({SOURCE_OUTPUT})="
            f"{m['log_odds_target_vs_source']:+.2f} KL={m['kl_from_clean']:.3f}"
        )
    print("\nprompt-only causal generations:")
    for row in generations:
        print(f"\n[{row['condition']}]\n{row['text']}")
    print("\npersistent steering generations:")
    for row in dose_generations:
        print(f"\n[{row['condition']}]\n{row['text']}")
    print(f"\noutput: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/causal_demo.json"))
    main(parser.parse_args().output)
