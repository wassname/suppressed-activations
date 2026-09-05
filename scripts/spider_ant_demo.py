"""Two-pass Spider→Ant suppressed-coordinate test. Written by PI/gpt-5.4."""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import generate, layer_hooks, one_token, replace_output, top_tokens, trajectory
from suppressed_activation_subspace import matched_random_rotation, suppressed_activation_subspace

MODEL = "Qwen/Qwen3.5-4B"
PROMPT = "Fact: The number of legs on the animal that spins webs is "
BLOCKS = tuple(range(22, 30))
MATCHED_VARIANT_PAIRS = (
    ("Spider", "Ant"),
    (" Spider", " Ant"),
    (" spider", " ant"),
    (" spiders", " ants"),
)
L26_DOSES = (-4.0, -2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0)
L26_RANKS = (8, 16, 32, 64)
RANDOM_CONTROL_COUNT = 32

RUN_STARTED = datetime.now().astimezone()
RUN_CLOCK = time.monotonic()
RUN_GIT = subprocess.run(
    ["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True
).stdout.strip()
RUN_DIR = ROOT / "out" / f"{RUN_STARTED:%Y-%m-%d_%H%M%S}_spider-ant"
RUN_DIR.mkdir(parents=True)
RUN_CONFIG = {
    "git_describe_at_start": RUN_GIT,
    "started_at": RUN_STARTED.isoformat(),
    "argv": sys.argv,
    "model": MODEL,
    "prompt": PROMPT,
    "extraction_layers": [23, 25, 32],
    "intervention_residual_layers": [block + 1 for block in BLOCKS],
    "matched_variant_pairs": MATCHED_VARIANT_PAIRS,
    "l26_ranks": L26_RANKS,
    "l26_doses": L26_DOSES,
    "random_control_count": RANDOM_CONTROL_COUNT,
    "status": "running",
}
(RUN_DIR / "metadata.json").write_text(
    json.dumps(RUN_CONFIG, ensure_ascii=False, indent=2) + "\n"
)
(RUN_DIR / "log.md").write_text(
    f"# Spider→Ant run\n\nStatus: running\n\nSource: `{RUN_GIT}`\n"
)
print(f"output: {RUN_DIR.relative_to(ROOT)}")


def dual_coordinates(h, directions):
    return torch.einsum("bsd,sqd->bsq", h, torch.linalg.pinv(directions))


def coordinate_swap(h, directions, strength, mask, restore_norm=False):
    before = dual_coordinates(h, directions)
    swapped = before.unflatten(-1, (-1, 2)).flip(-1).flatten(-2)
    delta = torch.einsum("bsq,sdq->bsd", swapped - before, directions)
    patched = h + strength * delta * mask[None, :, None]
    if restore_norm:
        patched = patched * h.norm(dim=-1, keepdim=True) / patched.norm(dim=-1, keepdim=True)
    return patched


def hooks(directions, strength, mask, restore_norm=False, record=None, blocks=BLOCKS):
    def make_hook(block):
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            if hidden.shape[1] == 1:
                return output
            h = hidden.float()
            patched = coordinate_swap(h, directions, strength, mask, restore_norm=restore_norm)
            if record is not None:
                position = int(mask.nonzero()[-1].item())
                before = dual_coordinates(h, directions)[0, position]
                after = dual_coordinates(patched, directions)[0, position]
                record[block + 1] = {
                    "position": position,
                    "source_before": float(before[0]),
                    "target_before": float(before[1]),
                    "source_after": float(after[0]),
                    "target_after": float(after[1]),
                    "residual_norm": float(h[0, position].norm()),
                    "perturbation_norm": float((patched[0, position] - h[0, position]).norm()),
                }
            return replace_output(output, patched.to(hidden.dtype))
        return hook
    return {block: make_hook(block) for block in blocks}


def matched_random_hook(directions, strength, mask, seed):
    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if hidden.shape[1] == 1:
            return output
        h = hidden.float()
        target = coordinate_swap(h, directions, strength, mask, restore_norm=True)
        distance = (target - h).norm(dim=-1, keepdim=True)
        generator = torch.Generator(device=h.device).manual_seed(seed)
        random_direction = torch.randn(h.shape, device=h.device, generator=generator)
        patched = matched_random_rotation(h, random_direction, distance)
        return replace_output(output, patched.to(hidden.dtype))
    return hook


torch.set_grad_enabled(False)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
lm = model.model
ids = tokenizer(PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
residuals, clean_logits = trajectory(model, ids, lm.norm)
bases, selected = suppressed_activation_subspace(
    residuals.permute(1, 0, 2), model.lm_head.weight, 1 + lm.norm.weight,
    early_layer=23, peak_layer=25, output_layer=32, rank=8,
    normalize_unembedding_rows=True,
)
W = model.lm_head.weight.float()
gain = (1 + lm.norm.weight).float()
spider_id = one_token(tokenizer, "Spider")
variant_ids = [
    (one_token(tokenizer, source), one_token(tokenizer, target))
    for source, target in MATCHED_VARIANT_PAIRS
]
vector_sets = {
    "single": [(spider_id, one_token(tokenizer, " Ant"))],
    "matched_atomic": variant_ids,
}
all_positions = torch.ones(selected.shape[0], device=selected.device)
final_position = torch.zeros_like(all_positions)
final_position[-1] = 1
previous_position = torch.zeros_like(all_positions)
previous_position[-2] = 1
id6, id8 = one_token(tokenizer, "6"), one_token(tokenizer, "8")
clean_logp = clean_logits.log_softmax(-1)
clean_p = clean_logp.exp()
rows = []
projected_by_set = {}
raw_vectors_by_set = {}
for variant_set, pairs in vector_sets.items():
    token_ids = [token_id for pair in pairs for token_id in pair]
    vectors = torch.stack([(W[token_id] - W.mean(0)) * gain for token_id in token_ids])
    raw_vectors_by_set[variant_set] = vectors
    coordinates = torch.einsum("td,sdk->stk", vectors, bases)
    projected = torch.einsum("stk,sdk->std", coordinates, bases)
    projected_by_set[variant_set] = projected
    source_ids = torch.tensor([source for source, _ in pairs], device=selected.device)
    detected = (selected[..., None] == source_ids).any((-1, -2)).float()
    for normalized in (False, True):
        token_vectors = projected / projected.norm(dim=-1, keepdim=True) if normalized else projected
        directions = token_vectors.transpose(1, 2)
        for mask_name, mask in (("all", all_positions), ("spider_detected", detected)):
            for strength in (1.0, 2.0):
                hs = hooks(directions, strength, mask)
                with layer_hooks(lm.layers, hs):
                    intervened_residuals, logits = trajectory(model, ids, lm.norm)
                _, after_selected = suppressed_activation_subspace(
                    intervened_residuals[:, -1][None], model.lm_head.weight, 1 + lm.norm.weight,
                    early_layer=23, peak_layer=25, output_layer=32, rank=8,
                    normalize_unembedding_rows=True,
                )
                logp = logits.log_softmax(-1)
                generation = generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64)
                rows.append({
                    "variant_set": variant_set,
                    "normalized": normalized, "mask": mask_name, "strength": strength,
                    "top": top_tokens(tokenizer, logits, 10),
                    "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
                    "delta_logp6": float(logp[id6] - clean_logits.log_softmax(-1)[id6]),
                    "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
                    "selected_tokens_after": [tokenizer.decode([int(i)]) for i in after_selected[0]],
                    "generation": generation,
                })


def unit(x):
    return x / x.norm(dim=-1, keepdim=True)


def first_shared_direction(x):
    direction = torch.linalg.svd(x, full_matrices=False).Vh[:, 0]
    sign = torch.einsum("sd,sd->s", direction, x.mean(1)).sign()
    return direction * sign[:, None]


atomic = unit(projected_by_set["matched_atomic"])
source_variants, target_variants = atomic[:, 0::2], atomic[:, 1::2]
prototype_sets = {
    **{
        f"pair_{i + 1}": atomic[:, 2 * i:2 * i + 2]
        for i, _pair in enumerate(MATCHED_VARIANT_PAIRS)
    },
    "mean_atomic": torch.stack([
        unit(source_variants.mean(1)), unit(target_variants.mean(1))
    ], dim=1),
    "svd1_atomic": torch.stack([
        first_shared_direction(source_variants), first_shared_direction(target_variants)
    ], dim=1),
}
prototype_rows = []
for method, token_vectors in prototype_sets.items():
    directions = token_vectors.transpose(1, 2)
    for strength in (0.125, 0.25, 0.5, 1.0):
        hs = hooks(directions, strength, all_positions)
        with layer_hooks(lm.layers, hs):
            intervened_residuals, logits = trajectory(model, ids, lm.norm)
        _, after_selected = suppressed_activation_subspace(
            intervened_residuals[:, -1][None], model.lm_head.weight, 1 + lm.norm.weight,
            early_layer=23, peak_layer=25, output_layer=32, rank=8,
            normalize_unembedding_rows=True,
        )
        logp = logits.log_softmax(-1)
        prototype_rows.append({
            "method": method, "strength": strength,
            "top": top_tokens(tokenizer, logits, 10),
            "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
            "delta_logp6": float(logp[id6] - clean_logits.log_softmax(-1)[id6]),
            "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
            "selected_tokens_after": [tokenizer.decode([int(i)]) for i in after_selected[0]],
            "generation": generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64),
        })

strong_rows = []
for method in ("pair_3", "mean_atomic", "svd1_atomic"):
    directions = prototype_sets[method].transpose(1, 2)
    for restore_norm in (False, True):
        for strength in (1.25, 1.5, 2.0, 3.0, 4.0, 8.0):
            hs = hooks(directions, strength, all_positions, restore_norm=restore_norm)
            with layer_hooks(lm.layers, hs):
                intervened_residuals, logits = trajectory(model, ids, lm.norm)
            _, after_selected = suppressed_activation_subspace(
                intervened_residuals[:, -1][None], model.lm_head.weight, 1 + lm.norm.weight,
                early_layer=23, peak_layer=25, output_layer=32, rank=8,
                normalize_unembedding_rows=True,
            )
            logp = logits.log_softmax(-1)
            strong_rows.append({
                "method": method, "restore_norm": restore_norm, "strength": strength,
                "top": top_tokens(tokenizer, logits, 10),
                "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
                "delta_logp6": float(logp[id6] - clean_logits.log_softmax(-1)[id6]),
                "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
                "selected_tokens_after": [tokenizer.decode([int(i)]) for i in after_selected[0]],
                "generation": generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64),
            })

localized_rows = []
directions = prototype_sets["mean_atomic"].transpose(1, 2)
for restore_norm in (False, True):
    for strength in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0):
        coordinate_record = {}
        hs = hooks(
            directions, strength, final_position,
            restore_norm=restore_norm, record=coordinate_record,
        )
        with layer_hooks(lm.layers, hs):
            _, logits = trajectory(model, ids, lm.norm)
        logp = logits.log_softmax(-1)
        p = logp.exp()
        top_id = int(logits.argmax())
        localized_rows.append({
            "method": "mean_atomic", "mask": "selected_final_position",
            "restore_norm": restore_norm, "strength": strength,
            "top": top_tokens(tokenizer, logits, 10),
            "rank6": int((logits > logits[id6]).sum()) + 1,
            "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
            "delta_logp6": float(logp[id6] - clean_logp[id6]),
            "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
            "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
            "entropy": float(-(p * logp).sum()),
            "coordinates_by_layer": coordinate_record,
            "generation": (
                generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64)
                if top_id == id6 else None
            ),
        })

single_layer_rows = []
for block in BLOCKS:
    coordinate_record = {}
    hs = hooks(
        directions, 2.0, final_position,
        restore_norm=False, record=coordinate_record, blocks=(block,),
    )
    with layer_hooks(lm.layers, hs):
        _, logits = trajectory(model, ids, lm.norm)
    logp = logits.log_softmax(-1)
    p = logp.exp()
    single_layer_rows.append({
        "method": "mean_atomic", "mask": "selected_final_position",
        "residual_layer": block + 1, "restore_norm": False, "strength": 2.0,
        "top": top_tokens(tokenizer, logits, 10),
        "rank6": int((logits > logits[id6]).sum()) + 1,
        "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
        "delta_logp6": float(logp[id6] - clean_logp[id6]),
        "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
        "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
        "entropy": float(-(p * logp).sum()),
        "coordinates_by_layer": coordinate_record,
    })

l26_dose_rows = []
l26_block = 25
l26_digit_ids = torch.tensor(
    [one_token(tokenizer, str(i)) for i in range(10)], device=ids.device
)
l26_rank_directions = {}
for rank in L26_RANKS:
    rank_basis, _ = suppressed_activation_subspace(
        residuals.permute(1, 0, 2), model.lm_head.weight, 1 + lm.norm.weight,
        early_layer=23, peak_layer=25, output_layer=32, rank=rank,
        normalize_unembedding_rows=True,
    )
    rank_vectors = raw_vectors_by_set["matched_atomic"]
    rank_coordinates = torch.einsum("td,sdk->stk", rank_vectors, rank_basis)
    rank_projected = torch.einsum("stk,sdk->std", rank_coordinates, rank_basis)
    rank_atomic = unit(rank_projected)
    l26_rank_directions[rank] = rank_atomic[:, 4:6].transpose(1, 2)

l26_conditions = [
    ("mean_atomic_rank8", prototype_sets["mean_atomic"].transpose(1, 2),
     "selected_final_position", final_position),
    ("mean_atomic_rank8", prototype_sets["mean_atomic"].transpose(1, 2),
     "previous_is_position", previous_position),
    ("lowercase_space_rank8", l26_rank_directions[8],
     "previous_is_position", previous_position),
    *[
        (f"lowercase_space_rank{rank}", l26_rank_directions[rank],
         "selected_final_position", final_position)
        for rank in L26_RANKS
    ],
]
for method, l26_directions, mask_name, l26_mask in l26_conditions:
    for restore_norm in (False, True):
        for strength in L26_DOSES:
            coordinate_record = {}
            hs = hooks(
                l26_directions, strength, l26_mask,
                restore_norm=restore_norm, record=coordinate_record, blocks=(l26_block,),
            )
            with layer_hooks(lm.layers, hs):
                _, logits = trajectory(model, ids, lm.norm)
            logp = logits.log_softmax(-1)
            p = logp.exp()
            top_id = int(logits.argmax())
            digit_mass = p[l26_digit_ids].sum()
            l26_dose_rows.append({
                "method": method, "mask": mask_name,
                "residual_layer": 26, "restore_norm": restore_norm, "strength": strength,
                "top": top_tokens(tokenizer, logits, 10),
                "rank6": int((logits > logits[id6]).sum()) + 1,
                "p6": float(p[id6]), "p8": float(p[id8]),
                "digit_mass": float(digit_mass),
                "digit_conditional_p6": float(p[id6] / digit_mass),
                "digit_conditional_p8": float(p[id8] / digit_mass),
                "delta_logp6": float(logp[id6] - clean_logp[id6]),
                "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
                "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
                "entropy": float(-(p * logp).sum()),
                "coordinates_by_layer": coordinate_record,
                "generation": (
                    generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64)
                    if top_id == id6 else None
                ),
            })

l26_random_rows = []
l26_primary_directions = l26_rank_directions[8]
for strength in (dose for dose in L26_DOSES if dose > 0):
    for seed in range(RANDOM_CONTROL_COUNT):
        hs = {
            l26_block: matched_random_hook(
                l26_primary_directions, strength, final_position, seed
            )
        }
        with layer_hooks(lm.layers, hs):
            _, logits = trajectory(model, ids, lm.norm)
        logp = logits.log_softmax(-1)
        p = logp.exp()
        l26_random_rows.append({
            "method": "lowercase_space_rank8", "mask": "selected_final_position",
            "residual_layer": 26, "strength": strength, "seed": seed,
            "top_token": tokenizer.decode([int(logits.argmax())]),
            "rank6": int((logits > logits[id6]).sum()) + 1,
            "p6": float(p[id6]), "p8": float(p[id8]),
            "delta_logp6": float(logp[id6] - clean_logp[id6]),
            "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
            "kl_from_clean": float((clean_p * (clean_logp - logp)).sum()),
            "entropy": float(-(p * logp).sum()),
        })

geometry = {
    "l26_lowercase_by_rank": {
        str(rank): {
            "singular_values_at_final_position": torch.linalg.svdvals(
                l26_rank_directions[rank][-1]
            ).tolist(),
            "condition_number_at_final_position": float(
                torch.linalg.cond(l26_rank_directions[rank][-1])
            ),
        }
        for rank in L26_RANKS
    }
}
for normalization, token_vectors in (
    ("raw", projected_by_set["matched_atomic"]),
    ("unit", atomic),
):
    singular_values = torch.linalg.svdvals(token_vectors[-1].T)
    geometry[normalization] = {
        "singular_values_at_final_position": singular_values.tolist(),
        "condition_number_at_final_position": float(singular_values[0] / singular_values[-1]),
    }

result = {
    "metadata": RUN_CONFIG,
    "prompt": PROMPT,
    "prompt_tokens": [tokenizer.decode([int(i)]) for i in ids[0]],
    "spider_detected_positions": (selected == spider_id).any(-1).nonzero().flatten().tolist(),
    "selected_tokens_at_final": [tokenizer.decode([int(i)]) for i in selected[-1]],
    "clean": top_tokens(tokenizer, clean_logits, 10),
    "rows": rows,
    "prototype_rows": prototype_rows,
    "strong_rows": strong_rows,
    "localized_rows": localized_rows,
    "single_layer_rows": single_layer_rows,
    "l26_dose_rows": l26_dose_rows,
    "l26_random_rows": l26_random_rows,
    "geometry": geometry,
}
RUN_CONFIG |= {
    "ended_at": datetime.now().astimezone().isoformat(),
    "elapsed_seconds": time.monotonic() - RUN_CLOCK,
    "peak_gpu_memory_gib": torch.cuda.max_memory_allocated() / 2**30,
    "model_revision": model.config._commit_hash,
    "status": "complete",
}
result["metadata"] = RUN_CONFIG
(RUN_DIR / "metadata.json").write_text(
    json.dumps(RUN_CONFIG, ensure_ascii=False, indent=2) + "\n"
)
(RUN_DIR / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

primary_rows = [
    row for row in l26_dose_rows
    if row["method"] == "lowercase_space_rank8"
    and row["mask"] == "selected_final_position"
    and row["restore_norm"]
]
primary_table = tabulate(
    [[
        row["strength"], row["top"][0]["token"], row["p6"], row["p8"],
        row["log_odds_6_vs_8"], row["kl_from_clean"], row["entropy"],
    ] for row in primary_rows],
    headers=["C", "top", "p(6)", "p(8)", "log p(6)/p(8)", "KL", "entropy"],
    tablefmt="pipe", floatfmt=".4f",
)
top6_rows = [row for row in l26_dose_rows if row["top"][0]["token"] == "6"]
top6_table = tabulate(
    [[
        row["method"], row["mask"], row["restore_norm"], row["strength"],
        row["p6"], row["p8"], row["kl_from_clean"], row["entropy"],
    ] for row in top6_rows],
    headers=["method", "position", "norm", "C", "p(6)", "p(8)", "KL", "entropy"],
    tablefmt="pipe", floatfmt=".4f",
)
random_summary = []
for target in (row for row in primary_rows if row["strength"] > 0):
    controls = [row for row in l26_random_rows if row["strength"] == target["strength"]]
    random_summary.append([
        target["strength"], target["log_odds_6_vs_8"],
        sum(row["log_odds_6_vs_8"] < target["log_odds_6_vs_8"] for row in controls),
        sum(row["top_token"] == "6" for row in controls),
    ])
random_table = tabulate(
    random_summary,
    headers=["C", "target log odds", "random effects below target / 32", "random top-6 / 32"],
    tablefmt="pipe", floatfmt=".4f",
)
unique_generations = {}
for row in top6_rows:
    generation = row["generation"]
    key = tuple(generation["token_ids"])
    condition = f'{row["method"]}, {row["mask"]}, norm={row["restore_norm"]}, C={row["strength"]}'
    unique_generations.setdefault(key, {"text": generation["text"], "conditions": []})[
        "conditions"
    ].append(condition)
generation_blocks = "\n\n".join(
    f"Produced by {len(item['conditions'])} condition(s): {', '.join(item['conditions'])}\n\n"
    f"```text\n{item['text']}\n```"
    for item in unique_generations.values()
)
config_json = json.dumps(RUN_CONFIG, ensure_ascii=False, indent=2)
run_log = f"""# Spider→Ant run

## Resolved configuration

```json
{config_json}
```

## Input and readout

Prompt: `{PROMPT}`

```text
[thoughts before: {', '.join(result['selected_tokens_at_final'])}]
```

## Primary L26 dose sweep

{primary_table}

## Conditions that changed the first token from 8 to 6

{top6_table}

## Matched random controls for the primary condition

{random_table}

## Exact 64-token generations

{generation_blocks or 'No targeted condition produced top token 6.'}

## Artifacts

- Full result: [`result.json`](result.json)
- Metadata: [`metadata.json`](metadata.json)

## Final result

Targeted top-6 conditions: {len(top6_rows)}. Primary rank-8 C=12 random effects below target: {next(row[2] for row in random_summary if row[0] == 12.0)}/32.

Written by PI/gpt-5.4.
"""
(RUN_DIR / "log.md").write_text(run_log)
print(f"targeted top-6 conditions: {len(top6_rows)}")
print(f"output: {RUN_DIR.relative_to(ROOT)}/log.md")
print(f"run identity: {RUN_GIT} | {RUN_CONFIG['elapsed_seconds']:.1f}s")
