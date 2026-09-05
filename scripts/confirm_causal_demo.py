"""Confirm the fixed single-site causal demo selected by job 149. Written by PI/gpt-5.4."""

import json
import math
import subprocess
import sys
import time
from contextlib import contextmanager, nullcontext
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

from suppressed_activation_subspace import (
    matched_random_rotation,
    replace,
    suppressed_activation_subspace,
)

MODEL = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
SOURCE_PROMPTS = {
    "spider": "Fact: The number of legs on the animal that spins webs is ",
    "byte": "Fact: The number of bits in one byte is ",
}
TARGETS = {
    "ant": ("Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ", "6"),
    "dog": ("Fact: The number of legs on the animal that barks and is called man's best friend is ", "4"),
    "three_plus_three": ("Fact: The result of adding three and three is ", "6"),
    "two_plus_two": ("Fact: The result of adding two and two is ", "4"),
}
EARLY_LAYER = 23
PEAK_LAYER = 25
OUTPUT_LAYER = 32
INTERVENTION_LAYER = 26
RANK = 8
STRENGTH = 4.0
RANDOM_CONTROL_COUNT = 256
MAX_NEW_TOKENS = 64
REALIZED_DISTANCE_ATOL = 0.1


def replace_output(output, hidden):
    return (hidden, *output[1:]) if isinstance(output, tuple) else hidden


@contextmanager
def layer_hook(layer, hook):
    handle = layer.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


def trajectory(model, input_ids, final_norm):
    raw_final = {}
    handle = final_norm.register_forward_pre_hook(
        lambda _module, inputs: raw_final.__setitem__("hidden", inputs[0].detach())
    )
    try:
        output = model(input_ids=input_ids, output_hidden_states=True, use_cache=False)
    finally:
        handle.remove()
    residuals = torch.stack(
        [hidden[0] for hidden in output.hidden_states[:-1]] + [raw_final["hidden"][0]]
    )
    return residuals, output.logits[0, -1].float()


def extract(model, tokenizer, prompt):
    ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    language_model = model.model
    residuals, logits = trajectory(model, ids, language_model.norm)
    basis, selected = suppressed_activation_subspace(
        residuals[:, -1][None],
        model.lm_head.weight,
        1 + language_model.norm.weight,
        early_layer=EARLY_LAYER,
        peak_layer=PEAK_LAYER,
        output_layer=OUTPUT_LAYER,
        rank=RANK,
        normalize_unembedding_rows=True,
    )
    return {
        "prompt": prompt,
        "input_ids": ids,
        "prompt_tokens": [tokenizer.decode([int(token_id)]) for token_id in ids[0]],
        "residuals": residuals,
        "logits": logits,
        "basis": basis[0],
        "selected": [
            {"token_id": int(token_id), "token": tokenizer.decode([int(token_id)])}
            for token_id in selected[0]
        ],
    }


def one_token(tokenizer, text):
    ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(ids) != 1:
        raise ValueError(f"{text!r} is {len(ids)} tokens: {ids}")
    return ids[0]


def top_tokens(tokenizer, logits, k=20):
    logp = logits.log_softmax(-1)
    return [
        {
            "token_id": int(token_id),
            "token": tokenizer.decode([int(token_id)]),
            "logp": float(logp[token_id]),
            "p": float(logp[token_id].exp()),
        }
        for token_id in logp.topk(k).indices
    ]


def score(tokenizer, logits, clean_logits, expected, other):
    expected_id = one_token(tokenizer, expected)
    other_id = one_token(tokenizer, other)
    id8 = one_token(tokenizer, "8")
    digit_ids = torch.tensor([one_token(tokenizer, str(i)) for i in range(10)], device=logits.device)
    logp = logits.log_softmax(-1)
    clean_logp = clean_logits.log_softmax(-1)
    p = logp.exp()
    clean_p = clean_logp.exp()
    digit_p = p[digit_ids]
    return {
        "top": top_tokens(tokenizer, logits),
        "expected": expected,
        "other_target_digit": other,
        "expected_rank": int((logits > logits[expected_id]).sum()) + 1,
        "p_expected": float(p[expected_id]),
        "p_8": float(p[id8]),
        "p_other_target_digit": float(p[other_id]),
        "log_odds_expected_vs_8": float(logp[expected_id] - logp[id8]),
        "log_odds_expected_vs_other": float(logp[expected_id] - logp[other_id]),
        "digit_mass": float(digit_p.sum()),
        "digit_conditional_probabilities": {
            str(i): float(value) for i, value in enumerate(digit_p / digit_p.sum())
        },
        "entropy": float(-(p * logp).sum()),
        "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
    }


def replacement_patch(source_h, source_basis, target_h, target_basis, strength, model_dtype):
    patched = replace(
        source_h,
        source_basis,
        target_h,
        target_basis,
        strength=strength,
        restore_norm=True,
    )
    applied = patched.to(model_dtype).float()
    applied_distance = (applied - source_h).norm()
    return patched, {
        "residual_norm_before": float(source_h.norm()),
        "residual_norm_after_fp32": float(patched.norm()),
        "perturbation_norm_fp32": float((patched - source_h).norm()),
        "applied_residual_norm": float(applied.norm()),
        "applied_perturbation_norm": float(applied_distance),
        "applied_perturbation_over_residual": float(applied_distance / source_h.norm()),
    }


def random_patch(source_h, distance, seed):
    generator = torch.Generator(device=source_h.device).manual_seed(seed)
    direction = torch.randn(source_h.shape, device=source_h.device, generator=generator)
    return matched_random_rotation(source_h, direction, distance.reshape(1))


def patch_hook(expected_h, patched_h, position=-1, prefill_only=False):
    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if prefill_only and hidden.shape[1] == 1:
            return output
        index = position % hidden.shape[1]
        torch.testing.assert_close(hidden[0, index].float(), expected_h, atol=2e-2, rtol=2e-2)
        replacement = patched_h.reshape(1, 1, -1).to(hidden.dtype)
        updated = torch.cat([hidden[:, :index], replacement, hidden[:, index + 1 :]], dim=1)
        return replace_output(output, updated)

    return hook


def run_logits(model, input_ids, layer, expected_h, patched_h, position=-1):
    with layer_hook(layer, patch_hook(expected_h, patched_h, position)), torch.no_grad():
        return model(input_ids=input_ids, use_cache=False).logits[0, -1].float()


def generate(model, tokenizer, input_ids, layer=None, expected_h=None, patched_h=None, position=-1):
    context = (
        layer_hook(layer, patch_hook(expected_h, patched_h, position, prefill_only=True))
        if layer is not None
        else nullcontext()
    )
    with context, torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            do_sample=False,
            max_new_tokens=MAX_NEW_TOKENS,
            min_new_tokens=MAX_NEW_TOKENS,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    ids = output[0, input_ids.shape[1] :].tolist()
    return {"token_ids": ids, "text": tokenizer.decode(ids, skip_special_tokens=False)}


def forced_generation(model, tokenizer, input_ids, first_token):
    first_id = one_token(tokenizer, first_token)
    prefixed = torch.cat([input_ids, torch.tensor([[first_id]], device=input_ids.device)], dim=1)
    with torch.no_grad():
        output = model.generate(
            input_ids=prefixed,
            do_sample=False,
            max_new_tokens=MAX_NEW_TOKENS - 1,
            min_new_tokens=MAX_NEW_TOKENS - 1,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    ids = [first_id] + output[0, prefixed.shape[1] :].tolist()
    return {"token_ids": ids, "text": tokenizer.decode(ids, skip_special_tokens=False)}


def evaluate_condition(model, tokenizer, source, target, expected, other, strength, position=-1):
    source_h = source["residuals"][INTERVENTION_LAYER, position].float()
    target_h = target["residuals"][INTERVENTION_LAYER, -1].float()
    patched_h, geometry = replacement_patch(
        source_h,
        source["basis"],
        target_h,
        target["basis"],
        strength,
        source["residuals"].dtype,
    )
    layer = model.model.layers[INTERVENTION_LAYER - 1]
    logits = run_logits(model, source["input_ids"], layer, source_h, patched_h, position)
    metrics = score(tokenizer, logits, source["logits"], expected, other)
    clean_metrics = score(tokenizer, source["logits"], source["logits"], expected, other)
    metrics["delta_log_odds_expected_vs_8"] = (
        metrics["log_odds_expected_vs_8"] - clean_metrics["log_odds_expected_vs_8"]
    )
    return {
        "strength": strength,
        "position": position,
        "metrics": metrics,
        "geometry": geometry,
        "patched_h": patched_h,
        "source_h": source_h,
    }


def render_log(metadata, sources, targets, conditions, random_summary, generations):
    primary_rows = []
    for name in ("spider_clean", "ant_C1", "ant_C4", "dog_C1", "dog_C4"):
        row = conditions[name]
        metrics = row["metrics"]
        geometry = row.get("geometry", {})
        primary_rows.append([
            name,
            metrics["top"][0]["token"],
            metrics["p_expected"],
            metrics["p_8"],
            metrics["log_odds_expected_vs_8"],
            metrics.get("delta_log_odds_expected_vs_8", 0.0),
            geometry.get("applied_perturbation_over_residual", 0.0),
        ])
    primary = tabulate(
        primary_rows,
        headers=["condition", "top", "p(expected)", "p(8)", "log odds expected/8", "Δ log odds", "distance/residual"],
        tablefmt="pipe",
        floatfmt=".4f",
    )
    control_rows = []
    for name, row in conditions.items():
        if name in {"spider_clean", "ant_C1", "ant_C4", "dog_C1", "dog_C4"}:
            continue
        metrics = row["metrics"]
        control_rows.append([
            name,
            metrics["top"][0]["token"],
            metrics["p_expected"],
            metrics["p_8"],
            metrics["log_odds_expected_vs_8"],
            metrics.get("delta_log_odds_expected_vs_8", 0.0),
        ])
    controls = tabulate(
        control_rows,
        headers=["condition", "top", "p(expected)", "p(8)", "log odds expected/8", "Δ log odds"],
        tablefmt="pipe",
        floatfmt=".4f",
    )
    readout_rows = [
        [name, ", ".join(row["token"] for row in sample["selected"])]
        for name, sample in (sources | targets).items()
    ]
    readouts = tabulate(readout_rows, headers=["sample", "selected vocabulary rows"], tablefmt="pipe")
    random_rows = tabulate(
        [[name, values["below"], RANDOM_CONTROL_COUNT, values["percentile"], values["random_top_expected"]]
         for name, values in random_summary.items()],
        headers=["target", "random effects below", "n", "percentile", "random top expected"],
        tablefmt="pipe",
        floatfmt=".4f",
    )
    generation_text = "\n\n".join(
        f"### {name}\n\n```text\n{row['text']}\n```" for name, row in generations.items()
    )
    config = json.dumps(metadata, ensure_ascii=False, indent=2)
    return f"""# Fixed L26/C4 causal confirmation

## Result

{primary}

## Resolved configuration

```json
{config}
```

## Selected vocabulary rows

{readouts}

## Matched-random controls

{random_rows}

## Other controls

{controls}

## Exact 64-token continuations

{generation_text}

## Artifacts

- [`result.json`](result.json)
- [`metadata.json`](metadata.json)

Written by PI/gpt-5.4.
"""


def main():
    torch.set_grad_enabled(False)
    started = datetime.now().astimezone()
    git_describe = subprocess.run(
        ["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True
    ).stdout.strip()
    output_dir = ROOT / "out" / f"{started:%Y-%m-%d_%H%M%S}_causal-confirmation"
    output_dir.mkdir(parents=True)
    metadata = {
        "git_describe_at_start": git_describe,
        "started_at": started.isoformat(),
        "argv": sys.argv,
        "model": MODEL,
        "model_revision": REVISION,
        "tokenizer_revision": REVISION,
        "source_prompts": SOURCE_PROMPTS,
        "target_prompts": {name: prompt for name, (prompt, _) in TARGETS.items()},
        "extraction_layers": [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER],
        "intervention_layer": INTERVENTION_LAYER,
        "intervention_position": "final source-prompt token",
        "rank": RANK,
        "strength": STRENGTH,
        "random_control_count": RANDOM_CONTROL_COUNT,
        "random_seeds": {"first": 0, "last": RANDOM_CONTROL_COUNT - 1},
        "max_new_tokens": MAX_NEW_TOKENS,
        "realized_random_distance_atol": REALIZED_DISTANCE_ATOL,
        "status": "running",
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    (output_dir / "log.md").write_text(f"# Fixed L26/C4 causal confirmation\n\nStatus: running\n\nSource: `{git_describe}`\n")
    print(f"output: {output_dir.relative_to(ROOT)}/log.md")

    clock = time.monotonic()
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16
    ).cuda().eval()
    layer = model.model.layers[INTERVENTION_LAYER - 1]
    sources = {name: extract(model, tokenizer, prompt) for name, prompt in SOURCE_PROMPTS.items()}
    targets = {name: extract(model, tokenizer, prompt) for name, (prompt, _) in TARGETS.items()}
    spider = sources["spider"]
    byte = sources["byte"]

    clean_metrics = score(tokenizer, spider["logits"], spider["logits"], "8", "6")
    conditions = {"spider_clean": {"metrics": clean_metrics}}
    for name, other in (("ant", "4"), ("dog", "6")):
        expected = TARGETS[name][1]
        conditions[f"{name}_C0"] = evaluate_condition(
            model, tokenizer, spider, targets[name], expected, other, 0.0
        )
        torch.testing.assert_close(
            conditions[f"{name}_C0"]["metrics"]["top"][0]["logp"],
            score(tokenizer, spider["logits"], spider["logits"], expected, other)["top"][0]["logp"],
        )
        conditions[f"{name}_C1"] = evaluate_condition(
            model, tokenizer, spider, targets[name], expected, other, 1.0
        )
        conditions[f"{name}_C4"] = evaluate_condition(
            model, tokenizer, spider, targets[name], expected, other, STRENGTH
        )
        conditions[f"{name}_penultimate_C4"] = evaluate_condition(
            model, tokenizer, spider, targets[name], expected, other, STRENGTH, position=-2
        )
        conditions[f"byte_{name}_C4"] = evaluate_condition(
            model, tokenizer, byte, targets[name], expected, other, STRENGTH
        )

    for name, other in (("three_plus_three", "4"), ("two_plus_two", "6")):
        expected = TARGETS[name][1]
        conditions[f"{name}_C4"] = evaluate_condition(
            model, tokenizer, spider, targets[name], expected, other, STRENGTH
        )

    random_controls = {}
    random_summary = {}
    for name, other in (("ant", "4"), ("dog", "6")):
        expected = TARGETS[name][1]
        primary = conditions[f"{name}_C4"]
        source_h = primary["source_h"]
        distance = torch.tensor(
            primary["geometry"]["applied_perturbation_norm"], device=source_h.device
        )
        clean_target_metrics = score(tokenizer, spider["logits"], spider["logits"], expected, other)
        rows = []
        for seed in range(RANDOM_CONTROL_COUNT):
            patched_h = random_patch(source_h, distance, seed)
            applied_distance = float((patched_h.to(spider["residuals"].dtype).float() - source_h).norm())
            distance_error = abs(applied_distance - float(distance))
            if distance_error > REALIZED_DISTANCE_ATOL:
                raise ValueError(
                    f"random seed {seed} applied distance error {distance_error:.4f} "
                    f"exceeds {REALIZED_DISTANCE_ATOL:.4f}"
                )
            logits = run_logits(model, spider["input_ids"], layer, source_h, patched_h)
            metrics = score(tokenizer, logits, spider["logits"], expected, other)
            metrics["delta_log_odds_expected_vs_8"] = (
                metrics["log_odds_expected_vs_8"]
                - clean_target_metrics["log_odds_expected_vs_8"]
            )
            rows.append({
                "seed": seed,
                "applied_perturbation_norm": applied_distance,
                "distance_error": distance_error,
                "metrics": metrics,
            })
        random_controls[name] = rows
        primary_delta = primary["metrics"]["delta_log_odds_expected_vs_8"]
        below = sum(row["metrics"]["delta_log_odds_expected_vs_8"] < primary_delta for row in rows)
        random_summary[name] = {
            "below": below,
            "percentile": below / RANDOM_CONTROL_COUNT,
            "random_top_expected": sum(row["metrics"]["top"][0]["token"] == expected for row in rows),
        }

    generations = {
        "spider_clean": generate(model, tokenizer, spider["input_ids"]),
        "spider_ant_C4": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["ant_C4"]["source_h"], conditions["ant_C4"]["patched_h"],
        ),
        "spider_dog_C4": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["dog_C4"]["source_h"], conditions["dog_C4"]["patched_h"],
        ),
        "spider_random_ant_distance_seed0": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["ant_C4"]["source_h"],
            random_patch(
                conditions["ant_C4"]["source_h"],
                torch.tensor(
                    conditions["ant_C4"]["geometry"]["applied_perturbation_norm"],
                    device="cuda",
                ),
                0,
            ),
        ),
        "spider_random_dog_distance_seed0": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["dog_C4"]["source_h"],
            random_patch(
                conditions["dog_C4"]["source_h"],
                torch.tensor(
                    conditions["dog_C4"]["geometry"]["applied_perturbation_norm"],
                    device="cuda",
                ),
                0,
            ),
        ),
        "byte_clean": generate(model, tokenizer, byte["input_ids"]),
        "byte_ant_C4": generate(
            model, tokenizer, byte["input_ids"], layer,
            conditions["byte_ant_C4"]["source_h"], conditions["byte_ant_C4"]["patched_h"],
        ),
        "byte_dog_C4": generate(
            model, tokenizer, byte["input_ids"], layer,
            conditions["byte_dog_C4"]["source_h"], conditions["byte_dog_C4"]["patched_h"],
        ),
        "spider_three_plus_three_C4": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["three_plus_three_C4"]["source_h"], conditions["three_plus_three_C4"]["patched_h"],
        ),
        "spider_two_plus_two_C4": generate(
            model, tokenizer, spider["input_ids"], layer,
            conditions["two_plus_two_C4"]["source_h"], conditions["two_plus_two_C4"]["patched_h"],
        ),
        "ant_target_clean": generate(model, tokenizer, targets["ant"]["input_ids"]),
        "dog_target_clean": generate(model, tokenizer, targets["dog"]["input_ids"]),
        "spider_forced_6": forced_generation(model, tokenizer, spider["input_ids"], "6"),
        "spider_forced_4": forced_generation(model, tokenizer, spider["input_ids"], "4"),
    }
    assert all(len(row["token_ids"]) == MAX_NEW_TOKENS for row in generations.values())

    serializable_conditions = {
        name: {key: value for key, value in row.items() if key not in {"patched_h", "source_h"}}
        for name, row in conditions.items()
    }
    completed_metadata = metadata | {
        "status": "complete",
        "ended_at": datetime.now().astimezone().isoformat(),
        "elapsed_seconds": time.monotonic() - clock,
        "peak_gpu_memory_gib": torch.cuda.max_memory_allocated() / 2**30,
    }
    artifact = {
        "metadata": completed_metadata,
        "sources": {
            name: {key: value for key, value in row.items() if key not in {"input_ids", "residuals", "logits", "basis"}}
            for name, row in sources.items()
        },
        "targets": {
            name: {key: value for key, value in row.items() if key not in {"input_ids", "residuals", "logits", "basis"}}
            for name, row in targets.items()
        },
        "conditions": serializable_conditions,
        "random_controls": random_controls,
        "random_summary": random_summary,
        "generations": generations,
    }
    rendered_log = render_log(
        completed_metadata,
        artifact["sources"],
        artifact["targets"],
        serializable_conditions,
        random_summary,
        generations,
    )
    (output_dir / "metadata.json").write_text(
        json.dumps(completed_metadata, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "result.json").write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "log.md").write_text(rendered_log)
    print(tabulate(
        [[name, row["metrics"]["top"][0]["token"], row["metrics"]["delta_log_odds_expected_vs_8"]]
         for name, row in conditions.items() if name in {"ant_C4", "dog_C4"}],
        headers=["condition", "top", "Δ log odds expected/8"],
        tablefmt="pipe",
        floatfmt=".4f",
    ))
    print(f"output: {output_dir.relative_to(ROOT)}/log.md")
    print(f"run identity: {git_describe} | {completed_metadata['elapsed_seconds']:.1f}s")


if __name__ == "__main__":
    main()
