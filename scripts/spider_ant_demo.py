"""Two-pass Spider→Ant suppressed-coordinate test. Written by PI/gpt-5.4."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import generate, layer_hooks, one_token, replace_output, top_tokens, trajectory
from suppressed_activation_subspace import suppressed_activation_subspace

MODEL = "Qwen/Qwen3.5-4B"
PROMPT = "Fact: The number of legs on the animal that spins webs is "
BLOCKS = tuple(range(22, 30))
MATCHED_VARIANT_PAIRS = (
    ("Spider", "Ant"),
    (" Spider", " Ant"),
    (" spider", " ant"),
    (" spiders", " ants"),
)


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


def hooks(directions, strength, mask, restore_norm=False, record=None):
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
    return {block: make_hook(block) for block in BLOCKS}


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
id6, id8 = one_token(tokenizer, "6"), one_token(tokenizer, "8")
clean_logp = clean_logits.log_softmax(-1)
clean_p = clean_logp.exp()
rows = []
projected_by_set = {}
for variant_set, pairs in vector_sets.items():
    token_ids = [token_id for pair in pairs for token_id in pair]
    vectors = torch.stack([(W[token_id] - W.mean(0)) * gain for token_id in token_ids])
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

geometry = {}
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
    "metadata": {
        "git_describe": subprocess.run(
            ["git", "describe", "--always", "--dirty"],
            check=True, text=True, capture_output=True,
        ).stdout.strip(),
        "model": MODEL,
        "extraction_layers": [23, 25, 32],
        "intervention_residual_layers": [block + 1 for block in BLOCKS],
        "matched_variant_pairs": MATCHED_VARIANT_PAIRS,
    },
    "prompt": PROMPT,
    "prompt_tokens": [tokenizer.decode([int(i)]) for i in ids[0]],
    "spider_detected_positions": (selected == spider_id).any(-1).nonzero().flatten().tolist(),
    "selected_tokens_at_final": [tokenizer.decode([int(i)]) for i in selected[-1]],
    "clean": top_tokens(tokenizer, clean_logits, 10),
    "rows": rows,
    "prototype_rows": prototype_rows,
    "strong_rows": strong_rows,
    "localized_rows": localized_rows,
    "geometry": geometry,
}
Path("data/spider_ant_demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print("prompt tokens:", result["prompt_tokens"])
print("Spider selected at positions:", result["spider_detected_positions"])
for row in rows:
    print({k: row[k] for k in ("variant_set", "normalized", "mask", "strength", "p6", "p8", "delta_logp6", "log_odds_6_vs_8")}, "top=", row["top"][0]["token"])
    print(row["generation"]["text"])
print("geometry:", geometry)
for row in prototype_rows:
    print({k: row[k] for k in ("method", "strength", "p6", "p8", "delta_logp6", "log_odds_6_vs_8")}, "top=", row["top"][0]["token"])
    print(row["generation"]["text"])
for row in strong_rows:
    print({k: row[k] for k in ("method", "restore_norm", "strength", "p6", "p8", "delta_logp6", "log_odds_6_vs_8")}, "top=", row["top"][0]["token"])
    print(row["generation"]["text"])
for row in localized_rows:
    print({k: row[k] for k in ("method", "mask", "restore_norm", "strength", "rank6", "p6", "p8", "log_odds_6_vs_8", "kl_from_clean", "entropy")}, "top=", row["top"][0]["token"])
    print("coordinates:", row["coordinates_by_layer"])
    if row["generation"] is not None:
        print(row["generation"]["text"])
