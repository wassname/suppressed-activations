"""Test a sample-specific Spider→Ant intervention. Written by PI/gpt-5.4."""

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
    suppressed_activation_subspace,
)

MODEL = "Qwen/Qwen3.5-4B"
PROMPTS = {
    "spider": "Fact: The number of legs on the animal that spins webs is ",
    "byte": "Fact: The number of bits in one byte is ",
}
EARLY_LAYER = 23
PEAK_LAYER = 25
OUTPUT_LAYER = 32
INTERVENTION_LAYER = 26
RANK = 16
STRENGTH = 8.0
SOURCE_TOKEN = " spider"
TARGET_TOKEN = " ant"
ANIMAL_TARGETS = {"ant": (" ant", "6"), "dog": (" dog", "4"), "bird": (" bird", "2")}
TARGET_LEG_STRENGTHS = (1.0, 2.0, 4.0, 8.0, 12.0)
RANDOM_CONTROL_COUNT = 32
MAX_NEW_TOKENS = 64


def one_token(tokenizer, text):
    token_ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(token_ids) != 1:
        raise ValueError(f"{text!r} is {len(token_ids)} tokens: {token_ids}")
    return token_ids[0]


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
    output = model(input_ids=input_ids, output_hidden_states=True, use_cache=False)
    handle.remove()
    residuals = torch.stack(
        [hidden[0] for hidden in output.hidden_states[:-1]] + [raw_final["hidden"][0]]
    )
    return residuals, output.logits[0, -1].float()


def top_tokens(tokenizer, logits, k=10):
    logp = logits.log_softmax(-1)
    return [
        {
            "token_id": int(token_id),
            "token": tokenizer.decode([token_id]),
            "logp": float(logp[token_id]),
        }
        for token_id in logp.topk(k).indices
    ]


def top_label(metrics):
    maximum = metrics["top"][0]["logp"]
    tied = sorted(
        row["token"] for row in metrics["top"]
        if math.isclose(row["logp"], maximum, abs_tol=1e-7)
    )
    return tied[0] if len(tied) == 1 else f"{'/'.join(tied)} tie"


def dual_coordinates(h, directions):
    return torch.einsum("bsd,sqd->bsq", h, torch.linalg.pinv(directions))


def apply_coordinate_delta(h, directions, coordinate_delta, mask, restore_norm=True):
    delta = torch.einsum("bsq,sdq->bsd", coordinate_delta, directions)
    patched = h + delta * mask[None, :, None]
    if restore_norm:
        patched = patched * h.norm(dim=-1, keepdim=True) / patched.norm(dim=-1, keepdim=True)
    return patched


def coordinate_swap(h, directions, strength, mask, restore_norm=True):
    before = dual_coordinates(h, directions)
    coordinate_delta = strength * (before.flip(-1) - before)
    return apply_coordinate_delta(
        h, directions, coordinate_delta, mask, restore_norm=restore_norm
    )


def coordinate_swap_leg(
    h, directions, leg, mask, strength=1.0, restore_norm=True
):
    before = dual_coordinates(h, directions)
    coordinate_delta = strength * (before.flip(-1) - before)
    keep = torch.tensor(
        [leg == "source", leg == "target"],
        device=h.device,
        dtype=h.dtype,
    )
    return apply_coordinate_delta(
        h, directions, coordinate_delta * keep, mask, restore_norm=restore_norm
    )


def projected_pair(model, tokenizer, basis, target_token):
    language_model = model.model
    source_id = one_token(tokenizer, SOURCE_TOKEN)
    target_id = one_token(tokenizer, target_token)
    centered = model.lm_head.weight.float() - model.lm_head.weight.float().mean(0)
    gain = (1 + language_model.norm.weight).float()
    token_vectors = torch.stack([centered[source_id] * gain, centered[target_id] * gain])
    coordinates = torch.einsum("td,sdk->stk", token_vectors, basis)
    projected = torch.einsum("stk,sdk->std", coordinates, basis)
    projected = projected / projected.norm(dim=-1, keepdim=True)
    return projected.transpose(1, 2)


def record_coordinate_change(record, h, patched, directions, mask):
    position = int(mask.nonzero()[-1])
    before = dual_coordinates(h, directions)[0, position]
    after = dual_coordinates(patched, directions)[0, position]
    record.update({
        "position": position,
        "source_before": float(before[0]),
        "target_before": float(before[1]),
        "source_after": float(after[0]),
        "target_after": float(after[1]),
        "residual_norm_before": float(h[0, position].norm()),
        "residual_norm_after": float(patched[0, position].norm()),
        "perturbation_norm": float((patched[0, position] - h[0, position]).norm()),
    })


def target_hook(directions, strength, mask, record=None):
    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if hidden.shape[1] == 1:
            return output
        h = hidden.float()
        patched = coordinate_swap(h, directions, strength, mask)
        if record is not None:
            record_coordinate_change(record, h, patched, directions, mask)
        return replace_output(output, patched.to(hidden.dtype))

    return hook


def swap_leg_hook(directions, leg, mask, record=None, strength=1.0):
    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if hidden.shape[1] == 1:
            return output
        h = hidden.float()
        patched = coordinate_swap_leg(h, directions, leg, mask, strength=strength)
        if record is not None:
            record_coordinate_change(record, h, patched, directions, mask)
        return replace_output(output, patched.to(hidden.dtype))

    return hook


def random_hook(directions, strength, mask, seed, record=None):
    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if hidden.shape[1] == 1:
            return output
        h = hidden.float()
        target = coordinate_swap(h, directions, strength, mask)
        requested_distance = (target - h).norm(dim=-1, keepdim=True)
        generator = torch.Generator(device=h.device).manual_seed(seed)
        random_direction = torch.randn(h.shape, device=h.device, generator=generator)
        patched = matched_random_rotation(h, random_direction, requested_distance)
        if record is not None:
            position = int(mask.nonzero()[-1])
            record.update({
                "position": position,
                "residual_norm_before": float(h[0, position].norm()),
                "residual_norm_after": float(patched[0, position].norm()),
                "requested_distance": float(requested_distance[0, position]),
                "achieved_distance": float((patched[0, position] - h[0, position]).norm()),
            })
        return replace_output(output, patched.to(hidden.dtype))

    return hook


def score(tokenizer, logits, clean_logits, id6, id8, digit_ids):
    logp = logits.log_softmax(-1)
    p = logp.exp()
    clean_logp = clean_logits.log_softmax(-1)
    clean_p = clean_logp.exp()
    digit_mass = p[digit_ids].sum()
    return {
        "top": top_tokens(tokenizer, logits),
        "rank6": int((logits > logits[id6]).sum()) + 1,
        "p6": float(p[id6]),
        "p8": float(p[id8]),
        "digit_mass": float(digit_mass),
        "digit_conditional_p6": float(p[id6] / digit_mass),
        "digit_conditional_p8": float(p[id8] / digit_mass),
        "digit_probabilities": {
            str(i): float(p[token_id]) for i, token_id in enumerate(digit_ids)
        },
        "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
        "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
        "entropy": float(-(p * logp).sum()),
    }


def generate(model, tokenizer, input_ids, layer, hook=None, max_new_tokens=64):
    context = layer_hook(layer, hook) if hook is not None else nullcontext()
    with context:
        output = model.generate(
            input_ids=input_ids,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    token_ids = output[0, input_ids.shape[1]:].tolist()
    return {
        "token_ids": token_ids,
        "text": tokenizer.decode(token_ids, skip_special_tokens=False),
    }


def force_first_token(model, tokenizer, input_ids, token_id):
    forced_ids = torch.cat([
        input_ids,
        torch.tensor([[token_id]], device=input_ids.device, dtype=input_ids.dtype),
    ], dim=1)
    suffix = generate(
        model, tokenizer, forced_ids, model.model.layers[INTERVENTION_LAYER - 1],
        max_new_tokens=MAX_NEW_TOKENS - 1,
    )
    token_ids = [token_id, *suffix["token_ids"]]
    return {"token_ids": token_ids, "text": tokenizer.decode(token_ids, skip_special_tokens=False)}


def evaluate_prompt(model, tokenizer, prompt):
    language_model = model.model
    input_ids = tokenizer(
        prompt, return_tensors="pt", add_special_tokens=False
    ).input_ids.cuda()
    residuals, clean_logits = trajectory(model, input_ids, language_model.norm)
    basis, selected = suppressed_activation_subspace(
        residuals.permute(1, 0, 2), model.lm_head.weight, 1 + language_model.norm.weight,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
        rank=RANK, normalize_unembedding_rows=True,
    )

    directions = projected_pair(model, tokenizer, basis, TARGET_TOKEN)

    mask = torch.zeros(input_ids.shape[1], device=input_ids.device)
    mask[-1] = 1
    id6, id8 = one_token(tokenizer, "6"), one_token(tokenizer, "8")
    digit_ids = torch.tensor(
        [one_token(tokenizer, str(i)) for i in range(10)], device=input_ids.device
    )
    layer = language_model.layers[INTERVENTION_LAYER - 1]

    target_record = {}
    with layer_hook(layer, target_hook(directions, STRENGTH, mask, target_record)):
        targeted_residuals, targeted_logits = trajectory(model, input_ids, language_model.norm)
    _, targeted_selected = suppressed_activation_subspace(
        targeted_residuals.permute(1, 0, 2), model.lm_head.weight,
        1 + language_model.norm.weight,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
        rank=RANK, normalize_unembedding_rows=True,
    )

    with layer_hook(layer, target_hook(directions, -STRENGTH, mask)):
        _, opposite_logits = trajectory(model, input_ids, language_model.norm)

    random_rows = []
    for seed in range(RANDOM_CONTROL_COUNT):
        random_record = {}
        with layer_hook(
            layer, random_hook(directions, STRENGTH, mask, seed, random_record)
        ):
            _, random_logits = trajectory(model, input_ids, language_model.norm)
        random_rows.append({
            "seed": seed,
            "metrics": score(tokenizer, random_logits, clean_logits, id6, id8, digit_ids),
            "matching": random_record,
        })

    animal_targets = []
    if prompt == PROMPTS["spider"]:
        target_distance = target_record["perturbation_norm"]
        clean_h = residuals[INTERVENTION_LAYER][None].float()
        for animal, (target_token, expected_output) in ANIMAL_TARGETS.items():
            animal_directions = projected_pair(model, tokenizer, basis, target_token)
            assert clean_h.dtype == animal_directions.dtype == torch.float32
            assert clean_h.device == animal_directions.device
            exact_record = {}
            with layer_hook(
                layer, target_hook(animal_directions, 1.0, mask, exact_record)
            ):
                _, exact_logits = trajectory(model, input_ids, language_model.norm)
            exact_metrics = score(
                tokenizer, exact_logits, clean_logits, id6, id8, digit_ids
            )
            swap_legs = {}
            for leg in ("source", "target"):
                leg_record = {}
                with layer_hook(
                    layer, swap_leg_hook(animal_directions, leg, mask, leg_record)
                ):
                    _, leg_logits = trajectory(model, input_ids, language_model.norm)
                swap_legs[leg] = {
                    "metrics": score(
                        tokenizer, leg_logits, clean_logits, id6, id8, digit_ids
                    ),
                    "matching": leg_record,
                }
            target_doses = []
            for dose in TARGET_LEG_STRENGTHS:
                if dose == 1.0:
                    dose_metrics = swap_legs["target"]["metrics"]
                    dose_record = swap_legs["target"]["matching"]
                else:
                    dose_record = {}
                    with layer_hook(
                        layer,
                        swap_leg_hook(
                            animal_directions, "target", mask,
                            dose_record, strength=dose,
                        ),
                    ):
                        _, dose_logits = trajectory(
                            model, input_ids, language_model.norm
                        )
                    dose_metrics = score(
                        tokenizer, dose_logits, clean_logits, id6, id8, digit_ids
                    )
                target_doses.append({
                    "strength": dose,
                    "metrics": dose_metrics,
                    "matching": dose_record,
                })
            successful_doses = [
                row for row in target_doses
                if top_label(row["metrics"]) == expected_output
            ]
            first_success = None
            if successful_doses:
                first = successful_doses[0]
                first_success = {
                    "strength": first["strength"],
                    "generation": generate(
                        model, tokenizer, input_ids, layer,
                        swap_leg_hook(
                            animal_directions, "target", mask,
                            strength=first["strength"],
                        ),
                        MAX_NEW_TOKENS,
                    ),
                }
            if animal == "ant":
                strength = STRENGTH
            else:
                low, high = 0.0, 64.0
                endpoint = coordinate_swap(clean_h, animal_directions, high, mask)
                endpoint_distance = float((endpoint[:, -1] - clean_h[:, -1]).norm())
                if endpoint_distance < target_distance:
                    raise ValueError(
                        f"{animal} reaches distance {endpoint_distance:.4f}, "
                        f"below target {target_distance:.4f} at C={high:g}"
                    )
                for _ in range(24):
                    middle = (low + high) / 2
                    candidate = coordinate_swap(clean_h, animal_directions, middle, mask)
                    distance = float((candidate[:, -1] - clean_h[:, -1]).norm())
                    low, high = (middle, high) if distance < target_distance else (low, middle)
                strength = (low + high) / 2
            animal_record = {}
            animal_hook = target_hook(animal_directions, strength, mask, animal_record)
            with layer_hook(layer, animal_hook):
                animal_residuals, animal_logits = trajectory(
                    model, input_ids, language_model.norm
                )
            torch.testing.assert_close(
                torch.tensor(animal_record["perturbation_norm"]),
                torch.tensor(target_distance), atol=1e-3, rtol=0,
            )
            _, animal_selected = suppressed_activation_subspace(
                animal_residuals.permute(1, 0, 2), model.lm_head.weight,
                1 + language_model.norm.weight,
                early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER,
                output_layer=OUTPUT_LAYER, rank=RANK,
                normalize_unembedding_rows=True,
            )
            animal_metrics = score(
                tokenizer, animal_logits, clean_logits, id6, id8, digit_ids
            )
            p_expected = animal_metrics["digit_probabilities"][expected_output]
            p8 = animal_metrics["digit_probabilities"]["8"]
            random_odds = [
                math.log(row["metrics"]["digit_probabilities"][expected_output])
                - math.log(row["metrics"]["digit_probabilities"]["8"])
                for row in random_rows
            ]
            expected_odds = math.log(p_expected) - math.log(p8)
            animal_targets.append({
                "animal": animal,
                "target_token": target_token,
                "expected_output": expected_output,
                "strength": strength,
                "exact_swap": {
                    "metrics": exact_metrics,
                    "matching": exact_record,
                    "legs": swap_legs,
                    "target_doses": target_doses,
                    "first_success": first_success,
                },
                "metrics": animal_metrics,
                "p_expected": p_expected,
                "log_odds_expected_vs_8": expected_odds,
                "random_effects_below": sum(value < expected_odds for value in random_odds),
                "matching": animal_record,
                "thoughts_after": [
                    tokenizer.decode([int(token_id)]) for token_id in animal_selected[-1]
                ],
                "generation": generate(
                    model, tokenizer, input_ids, layer,
                    target_hook(animal_directions, strength, mask), MAX_NEW_TOKENS,
                ),
            })

    generations = {
        "clean": generate(model, tokenizer, input_ids, layer, max_new_tokens=MAX_NEW_TOKENS),
        "targeted": generate(
            model, tokenizer, input_ids, layer,
            target_hook(directions, STRENGTH, mask), MAX_NEW_TOKENS,
        ),
        "random_seed_0": generate(
            model, tokenizer, input_ids, layer,
            random_hook(directions, STRENGTH, mask, 0), MAX_NEW_TOKENS,
        ),
        "forced_6_without_intervention": force_first_token(
            model, tokenizer, input_ids, id6
        ),
    }
    return {
        "prompt": prompt,
        "prompt_tokens": [tokenizer.decode([int(token_id)]) for token_id in input_ids[0]],
        "thoughts_before": [tokenizer.decode([int(token_id)]) for token_id in selected[-1]],
        "thoughts_after": [
            tokenizer.decode([int(token_id)]) for token_id in targeted_selected[-1]
        ],
        "clean": score(tokenizer, clean_logits, clean_logits, id6, id8, digit_ids),
        "opposite": score(tokenizer, opposite_logits, clean_logits, id6, id8, digit_ids),
        "targeted": score(tokenizer, targeted_logits, clean_logits, id6, id8, digit_ids),
        "target_matching": target_record,
        "random_controls": random_rows,
        "animal_targets": animal_targets,
        "generations": generations,
        "targeted_matches_forced_6": (
            generations["targeted"]["token_ids"]
            == generations["forced_6_without_intervention"]["token_ids"]
        ),
    }


def render_log(metadata, results):
    sections = []
    summary_rows = []
    for name, result in results.items():
        targeted = result["targeted"]
        random_below = sum(
            row["metrics"]["log_odds_6_vs_8"] < targeted["log_odds_6_vs_8"]
            for row in result["random_controls"]
        )
        random_top6 = sum(
            row["metrics"]["top"][0]["token"] == "6"
            for row in result["random_controls"]
        )
        summary_rows.append([
            name, top_label(result["clean"]), top_label(targeted),
            targeted["p6"], targeted["p8"], targeted["log_odds_6_vs_8"],
            random_below, random_top6,
        ])
        condition_table = tabulate(
            [[
                label, top_label(row), row["p6"], row["p8"],
                row["log_odds_6_vs_8"], row["kl_from_clean"], row["entropy"],
            ] for label, row in (
                ("clean", result["clean"]),
                (f"C={-STRENGTH:g}", result["opposite"]),
                (f"C={STRENGTH:g}", targeted),
            )],
            headers=["condition", "top", "p(6)", "p(8)", "log p(6)/p(8)", "KL", "entropy"],
            tablefmt="pipe", floatfmt=".4f",
        )
        generations = "\n\n".join(
            f"### {name} → {label}\n\n```text\n{generation['text']}\n```"
            for label, generation in result["generations"].items()
        )
        animal_block = ""
        if result["animal_targets"]:
            exact_table = tabulate(
                [[
                    row["animal"], row["expected_output"],
                    top_label(row["exact_swap"]["metrics"]),
                    *[
                        row["exact_swap"]["metrics"]["digit_probabilities"][digit]
                        for digit in ("2", "4", "6", "8")
                    ],
                    row["exact_swap"]["matching"]["perturbation_norm"],
                ] for row in result["animal_targets"]],
                headers=[
                    "target", "expected", "C=1 top",
                    "p(2)", "p(4)", "p(6)", "p(8)", "distance",
                ],
                tablefmt="pipe", floatfmt=".4f",
            )
            leg_table = tabulate(
                [[
                    row["animal"], leg,
                    *[
                        row["exact_swap"]["legs"][leg]["metrics"]
                        ["digit_probabilities"][digit]
                        - result["clean"]["digit_probabilities"][digit]
                        for digit in ("2", "4", "6", "8")
                    ],
                    row["exact_swap"]["legs"][leg]["matching"]
                    ["perturbation_norm"],
                ]
                for row in result["animal_targets"]
                for leg in ("source", "target")],
                headers=[
                    "pair", "swap component",
                    "Δp(2)", "Δp(4)", "Δp(6)", "Δp(8)", "distance",
                ],
                tablefmt="pipe", floatfmt="+.4f",
            )
            dose_table = tabulate(
                [[
                    row["animal"], dose["strength"],
                    top_label(dose["metrics"]),
                    *[
                        dose["metrics"]["digit_probabilities"][digit]
                        for digit in ("2", "4", "6", "8")
                    ],
                    dose["matching"]["perturbation_norm"],
                ]
                for row in result["animal_targets"]
                for dose in row["exact_swap"]["target_doses"]],
                headers=[
                    "target", "target C", "top",
                    "p(2)", "p(4)", "p(6)", "p(8)", "distance",
                ],
                tablefmt="pipe", floatfmt=".4f",
            )
            success_generations = "\n\n".join(
                f"### {row['animal'].title()} target component, "
                f"C={row['exact_swap']['first_success']['strength']:g}\n\n"
                f"```text\n"
                f"{row['exact_swap']['first_success']['generation']['text']}\n"
                f"```"
                for row in result["animal_targets"]
                if row["exact_swap"]["first_success"] is not None
            )
            animal_table = tabulate(
                [[
                    row["animal"], row["expected_output"], row["strength"],
                    top_label(row["metrics"]), row["p_expected"],
                    row["log_odds_expected_vs_8"], row["random_effects_below"],
                    row["matching"]["perturbation_norm"],
                ] for row in result["animal_targets"]],
                headers=[
                    "target", "expected", "C", "top", "p(expected)",
                    "log p(expected)/p(8)", "random below / 32", "distance",
                ],
                tablefmt="pipe", floatfmt=".4f",
            )
            animal_readouts = "\n".join(
                f"[suppressed readout after Spider→{row['animal'].title()}: "
                f"{', '.join(row['thoughts_after'])}]"
                for row in result["animal_targets"]
            )
            animal_generations = "\n\n".join(
                f"### Spider→{row['animal'].title()}\n\n"
                f"```text\n{row['generation']['text']}\n```"
                for row in result["animal_targets"]
            )
            animal_block = f"""### C=1 swap endpoint

{exact_table}

### Separately norm-restored sides of the C=1 operation

{leg_table}

### Target-coordinate dose sweep

{dose_table}

{success_generations}

### Equal-distance animal extrapolations

{animal_table}

```text
{animal_readouts}
```

{animal_generations}
"""
        sections.append(f"""## {name}

Prompt: `{result['prompt']}`

```text
[thoughts before: {', '.join(result['thoughts_before'])}]
[thoughts after Spider→Ant: {', '.join(result['thoughts_after'])}]
```

{condition_table}

Target effect exceeded {random_below}/32 matched random effects; {random_top6}/32 random controls also placed `6` first. Targeted continuation equals the forced-`6` no-intervention continuation: `{result['targeted_matches_forced_6']}`.

{animal_block}
{generations}
""")
    summary = tabulate(
        summary_rows,
        headers=[
            "prompt", "clean top", "target top", "p(6)", "p(8)",
            "log p(6)/p(8)", "random below / 32", "random top-6 / 32",
        ],
        tablefmt="pipe", floatfmt=".4f",
    )
    config_json = json.dumps(metadata, ensure_ascii=False, indent=2)
    return f"""# Spider→Ant confirmation

## Result

{summary}

## Resolved configuration

```json
{config_json}
```

{''.join(sections)}
## Artifacts

- Full result: [`result.json`](result.json)
- Metadata: [`metadata.json`](metadata.json)

Written by PI/gpt-5.4.
"""


def main():
    torch.set_grad_enabled(False)
    started = datetime.now().astimezone()
    git_describe = subprocess.run(
        ["git", "describe", "--always", "--dirty"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()
    output_dir = ROOT / "out" / f"{started:%Y-%m-%d_%H%M%S}_spider-ant"
    output_dir.mkdir(parents=True)
    metadata = {
        "git_describe_at_start": git_describe,
        "started_at": started.isoformat(),
        "argv": sys.argv,
        "model": MODEL,
        "prompts": PROMPTS,
        "extraction_layers": [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER],
        "intervention_layer": INTERVENTION_LAYER,
        "rank": RANK,
        "strength": STRENGTH,
        "source_token": SOURCE_TOKEN,
        "target_token": TARGET_TOKEN,
        "target_leg_strengths": TARGET_LEG_STRENGTHS,
        "random_control_count": RANDOM_CONTROL_COUNT,
        "max_new_tokens": MAX_NEW_TOKENS,
        "status": "running",
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "log.md").write_text(
        f"# Spider→Ant confirmation\n\nStatus: running\n\nSource: `{git_describe}`\n"
    )
    print(f"output: {output_dir.relative_to(ROOT)}/log.md")

    clock = time.monotonic()
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
    results = {
        name: evaluate_prompt(model, tokenizer, prompt) for name, prompt in PROMPTS.items()
    }
    metadata |= {
        "ended_at": datetime.now().astimezone().isoformat(),
        "elapsed_seconds": time.monotonic() - clock,
        "peak_gpu_memory_gib": torch.cuda.max_memory_allocated() / 2**30,
        "model_revision": model.config._commit_hash,
        "status": "complete",
    }
    artifact = {"metadata": metadata, "prompts": results}
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "result.json").write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n"
    )
    (output_dir / "log.md").write_text(render_log(metadata, results))

    print("\n" + tabulate(
        [[
            name, top_label(result["clean"]),
            top_label(result["targeted"]),
            result["targeted"]["log_odds_6_vs_8"],
        ] for name, result in results.items()],
        headers=["prompt", "clean", "targeted", "log p(6)/p(8)"],
        tablefmt="pipe", floatfmt=".4f",
    ))
    print(f"output: {output_dir.relative_to(ROOT)}/log.md")
    print(f"run identity: {git_describe} | {metadata['elapsed_seconds']:.1f}s")


if __name__ == "__main__":
    main()
