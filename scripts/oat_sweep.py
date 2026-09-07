# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""One-at-a-time intervention sweep. Written by Codex/gpt-5.6-sol."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, replace
from importlib.metadata import version
from pathlib import Path

import torch
import pyarrow.ipc as arrow_ipc
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
from scripts.prompt import assistant_prefill_input_ids
from scripts.demo import intervention_hooks, layer_hooks, one_token, trajectory
from suppressed_activation_subspace import (
    component,
    suppressed_activation_subspace,
    token_persistent_subspace,
    persistent_suppressed_activation_subspace,
    union_suppressed_activation_subspace,
)


@dataclass(frozen=True)
class Config:
    aggregation: str = "union"
    detector_layers: tuple[int, int, int] = (23, 25, 32)
    readout_positions: int = 4
    rank: int = 8
    intervention_layer: int | tuple[int, ...] = (24,)
    intervention_positions: int | str = 3
    strength: float = 2.5
    match_component_norm: bool = True
    restore_residual_norm: bool = True
    donor_position_offset: int = 0
    lexical_forms: str = "detector"
    lexical_divisor: int = 1
    continue_generation: bool = True
    persistent_rank: int = 0
    random_delta_seed: int = -1
    delta_component: str = "difference"
    coordinate_swap: bool = False
    source_dominant_only: bool = False
    template_contrast: bool = False
    template_clamp: bool = False
    future_coordinate: bool = False


DEFAULT = Config()


def coordinate_swap_configs():
    return [("coordinate_swap", f"rank{rank}_C{strength}", replace(
        DEFAULT, coordinate_swap=True, persistent_rank=rank, strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for rank in (0, 4) for strength in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)]


def coordinate_layer_configs():
    return [("coordinate_layer", f"L{layer}_C{strength}", replace(
        DEFAULT, coordinate_swap=True, intervention_layer=(layer,), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (4, 8, 12, 16, 20, 24)
        for strength in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)]


def coordinate_layer_strong_configs():
    return [("coordinate_strong", f"L{layer}_C{strength}", replace(
        DEFAULT, coordinate_swap=True, intervention_layer=(layer,), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (4, 8, 12, 16, 20, 24)
        for strength in (6.0, 8.0, 12.0, 16.0, 24.0, 32.0)]


def coordinate_band_configs():
    layers = [(8,), (12,), (16,), (20,), (24,), tuple(range(8, 13)),
              tuple(range(12, 17)), tuple(range(16, 21)), tuple(range(20, 25))]
    return [("coordinate_band", f"L{band}_C{strength}", replace(
        DEFAULT, coordinate_swap=True, source_dominant_only=True,
        intervention_layer=band, strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for band in layers for strength in (0.0, 0.25, 0.5, 1.0, 2.0)]


def template_contrast_configs():
    rows = [("template_contrast", f"L{layer}_rank{rank}_C{strength}", replace(
        DEFAULT, template_contrast=True, persistent_rank=rank,
        intervention_layer=(layer,), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (4, 8, 12, 16, 20, 24) for rank in (0, 4)
        for strength in (0.0, 0.5, 1.0, 2.0, 4.0)]
    rows.extend(("template_random", str(seed), replace(
        DEFAULT, template_contrast=True, intervention_layer=(16,), strength=2.0,
        random_delta_seed=seed, match_component_norm=False, restore_residual_norm=False,
    )) for seed in range(8))
    return rows


def template_projection_configs():
    rows = [("template_projection", f"rank{rank}_C{strength}", replace(
        DEFAULT, template_contrast=True, persistent_rank=rank,
        strength=strength, match_component_norm=True, restore_residual_norm=False,
    )) for rank in (4, 8, 16, 32) for strength in (0.0, 0.5, 1.0, 2.0)]
    rows.extend(("template_selected_random", str(seed), replace(
        DEFAULT, template_contrast=True, strength=1.0,
        random_delta_seed=seed, match_component_norm=False, restore_residual_norm=False,
    )) for seed in range(12))
    return rows


def template_clamp_configs():
    return [("template_clamp", f"L{layer}_C{strength}", replace(
        DEFAULT, template_contrast=True, template_clamp=True,
        intervention_layer=(layer,), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (12, 16, 20, 24) for strength in (0.0, 0.25, 0.5, 1.0)]


def template_scope_configs():
    rows = [("template_scope", f"L{layer}_positions{positions}_C{strength}", replace(
        DEFAULT, template_contrast=True, intervention_layer=(layer,),
        intervention_positions=positions, strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (16, 20, 24) for positions in (3, "all")
        for strength in (0.0, 0.5, 1.0, 2.0)]
    rows.extend(("template_scope_band", f"positions{positions}_C{strength}", replace(
        DEFAULT, template_contrast=True, intervention_layer=tuple(range(16, 21)),
        intervention_positions=positions, strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for positions in (3, "all") for strength in (0.0, 0.125, 0.25, 0.5))
    return rows


def template_band_strength_configs():
    baseline = replace(DEFAULT, template_contrast=True, intervention_layer=tuple(range(16, 21)),
                       intervention_positions=3, match_component_norm=False, restore_residual_norm=False)
    return [("template_band_strength", f"C{strength}", replace(baseline, strength=strength))
            for strength in (0.0, 0.5, 0.625, 0.75, 1.0, 1.5, 2.0)]


def future_coordinate_configs():
    return [("future_coordinate", f"L{layer}_rank{rank}_C{strength}", replace(
        DEFAULT, coordinate_swap=True, future_coordinate=True, persistent_rank=rank,
        intervention_layer=(layer,), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer in (12, 16, 20, 24) for rank in (0, 4)
        for strength in (0.0, 0.5, 1.0, 2.0, 4.0)]


def future_gated_configs():
    return [("future_gated", f"L{layer}_rank{rank}_C{strength}_gate{gate}", replace(
        DEFAULT, coordinate_swap=True, future_coordinate=True, persistent_rank=rank,
        intervention_layer=(layer,), strength=strength, source_dominant_only=gate,
        match_component_norm=False, restore_residual_norm=False,
    )) for layer, rank in ((12, 0), (16, 0), (24, 4))
        for strength in (1.0, 2.0) for gate in (False, True)]


def future_template_configs():
    return [("future_template", f"L{layer}_{projection}_C{strength}", replace(
        DEFAULT, template_contrast=True, future_coordinate=projection != "full",
        intervention_layer=(layer,), strength=strength,
        match_component_norm=projection == "matched", restore_residual_norm=False,
    )) for layer in (16, 20) for projection in ("full", "projected", "matched")
        for strength in (0.0, 0.5, 1.0, 2.0)]


def fit_future_rows(model, tokenizer, corpus_path, output_dir):
    """Contract the official mean-J estimator with three vocabulary rows. -- Codex/GPT-6"""
    texts = arrow_ipc.open_stream(corpus_path).read_all()["text"].to_pylist()
    texts = random.Random(0).sample([text.strip() for text in texts if len(text.strip()) >= 600], 16)
    assert len(texts) == 16
    layers = (12, 16, 20, 24)
    words = (" spider", " dog", " ant")
    output_rows = model.lm_head.weight[[one_token(tokenizer, word) for word in words]].float()
    samples, corpus, derivative_checks = [], [], []
    model.requires_grad_(False)
    for index, text in enumerate(texts):
        content = tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)[:128])
        chat = assistant_prefill_input_ids(tokenizer, content)
        ids = chat["input_ids"]
        valid = torch.arange(max(16, chat["content_start"]), chat["content_end"] - 1, device=ids.device)
        assert len(valid) > 0
        corpus.append({"text": content, "input_ids": ids[0].tolist(), "valid_positions": valid.tolist(),
                       "rendered": tokenizer.decode(ids[0], skip_special_tokens=False)})
        def grad_leaf(_module, _inputs, output):
            return output.requires_grad_(True)
        with torch.enable_grad(), layer_hooks(model.model.layers, {11: grad_leaf}):
            output = model(input_ids=ids, use_cache=False, output_hidden_states=True)
            hidden = tuple(output.hidden_states[layer] for layer in layers)
            target = output.hidden_states[31]
            per_word = []
            for word_index, row in enumerate(output_rows):
                scalar = (target[0, valid].float() @ row).sum()
                gradients = torch.autograd.grad(scalar, hidden, retain_graph=word_index < 2)
                per_word.append(torch.stack([g[0, valid].float().mean(0) for g in gradients]))
                if index == 0 and word_index == 0:
                    probe_gradient = gradients[0][0, valid[0]].detach().float()
            samples.append(torch.stack(per_word).detach())
        del output, hidden, target, gradients, scalar
        if index == 0:
            direction = probe_gradient / probe_gradient.norm()
            for epsilon in (0.125, 0.5, 2.0):
                values = []
                for sign in (-1, 1):
                    def perturb(_module, _inputs, output):
                        changed = output.clone()
                        changed[0, valid[0]] = (output[0, valid[0]].float() + sign * epsilon * direction).to(output.dtype)
                        return changed
                    with layer_hooks(model.model.layers, {11: perturb}):
                        perturbed = model(input_ids=ids, use_cache=False, output_hidden_states=True)
                        values.append(float((perturbed.hidden_states[31][0, valid].float() @ output_rows[0]).sum()))
                    del perturbed
                derivative_checks.append({"epsilon": epsilon, "finite_difference": (values[1]-values[0])/(2*epsilon),
                                          "autograd": float(probe_gradient.norm())})
        logger.info("future lens corpus {}/16", index + 1)
    stacked = torch.stack(samples)
    assert torch.isfinite(stacked).all()
    means = stacked.mean(0)
    vectors = {layer: means[:, i].T for i, layer in enumerate(layers)}
    provenance = {"estimator": "mean_source_sum_current_future_raw_penultimate_vjp",
                  "official_reference_commit": "581d398613e5602a5af361e1c34d3a92ea82ba8e",
                  "corpus_sampling": "16 eligible records without replacement, Python random seed0",
                  "corpus_path": str(corpus_path), "corpus_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
                  "words": words, "target_residual_layer": 31, "source_residual_layers": layers,
                  "per_prompt_vector_norms": stacked.norm(dim=-1).tolist(),
                  "split_half_cosines": torch.nn.functional.cosine_similarity(
                      stacked[:8].mean(0), stacked[8:].mean(0), dim=-1).tolist(),
                  "finite_difference_checks": derivative_checks, "corpus": corpus}
    (output_dir / "future_lens.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2))
    torch.save(vectors, output_dir / "future_lens_vectors.pt")
    return vectors, {key: value for key, value in provenance.items() if key != "corpus"}


CONCEPT_TEMPLATES = (
    "A photograph is labeled '{animal}'. The animal is ",
    "I noticed something labeled '{animal}' nearby. That animal is ",
    "Someone wrote '{animal}' as the creature's name. The animal is ",
    "The story mentions an animal called '{animal}'. That animal is ",
    "Imagine an animal identified as '{animal}'. This animal is ",
    "We are discussing the animal '{animal}'. The creature is ",
    "A drawing depicts an animal labeled '{animal}'. This creature is ",
    "I read about the animal '{animal}' yesterday. That creature is ",
)


def svd_configs():
    rows = [("default", "default", DEFAULT)]
    for rank in (1, 2, 4, 8, 16):
        for strength in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
            rows.append(("svd_rank_strength", f"rank={rank},C={strength:g}", replace(
                DEFAULT, persistent_rank=rank, strength=strength,
                restore_residual_norm=False, match_component_norm=False,
            )))
    return rows


def svd_refine_configs():
    rows = [("default", "default", DEFAULT)]
    for rank in (1, 2, 4):
        for strength in (0.0, 6.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0):
            rows.append(("svd_refine", f"rank={rank},C={strength:g}", replace(
                DEFAULT, persistent_rank=rank, strength=strength,
                restore_residual_norm=False, match_component_norm=False,
            )))
    return rows


def svd_detector_configs():
    rows = [("default", "default", DEFAULT)]
    for detector in ((8, 16, 32), (12, 20, 32), (16, 24, 32), (20, 28, 32)):
        for rank in (1, 2, 4):
            for strength in (2.0, 4.0, 8.0, 16.0):
                rows.append(("svd_detector", f"detector={detector},rank={rank},C={strength:g}", replace(
                    DEFAULT, detector_layers=detector, persistent_rank=rank, strength=strength,
                    restore_residual_norm=False, match_component_norm=False,
                )))
    return rows


def svd_band_configs():
    rows = [("default", "default", DEFAULT)]
    for layers in ((24,), (22, 23, 24), (24, 25, 26)):
        for ongoing in (False, True):
            for strength in (2.0, 4.0, 8.0, 12.0):
                rows.append(("svd_band", f"layers={layers},decode={ongoing},C={strength:g}", replace(
                    DEFAULT, persistent_rank=1, strength=strength,
                    intervention_layer=layers, continue_generation=ongoing,
                    restore_residual_norm=False, match_component_norm=False,
                )))
    return rows


def svd_control_configs():
    candidate = replace(DEFAULT, persistent_rank=1, strength=12.0,
                        restore_residual_norm=False, match_component_norm=False)
    return [("svd_control", "selected", candidate),
            ("svd_control", "zero", replace(candidate, strength=0.0))] + [
        ("svd_control", f"random={seed}", replace(candidate, random_delta_seed=seed))
        for seed in range(16)
    ]


def svd_tokens_configs():
    rows = [("default", "default", DEFAULT)]
    for tokens in (2, 8, 12):
        for rank in (1, 2):
            for strength in (4.0, 8.0, 12.0):
                rows.append(("svd_tokens", f"tokens={tokens},rank={rank},C={strength:g}", replace(
                    DEFAULT, readout_positions=tokens, persistent_rank=rank, strength=strength,
                    restore_residual_norm=False, match_component_norm=False,
                )))
    return rows


def svd_candidates_configs():
    rows = [("default", "default", DEFAULT)]
    for candidates in (32, 64):
        for rank in (1, 2, 4):
            for strength in (4.0, 8.0, 12.0):
                rows.append(("svd_candidates", f"candidates={candidates},rank={rank},C={strength:g}", replace(
                    DEFAULT, rank=candidates, persistent_rank=rank, strength=strength,
                    restore_residual_norm=False, match_component_norm=False,
                )))
    return rows


def svd_parts_configs():
    return [("svd_parts", part, replace(
        DEFAULT, persistent_rank=1, strength=12.0, delta_component=part,
        restore_residual_norm=False, match_component_norm=False,
    )) for part in ("difference", "source_remove", "target_add")]


def svd_continuous_configs():
    rows = []
    for rank in (1, 2, 4):
        for part in ("difference", "source_remove", "target_add"):
            for strength in (0.0, 2.0, 4.0, 8.0, 12.0):
                rows.append(("svd_continuous", f"rank={rank},part={part},C={strength:g}", replace(
                    DEFAULT, persistent_rank=rank, strength=strength, delta_component=part,
                    intervention_positions=3, continue_generation=True,
                    restore_residual_norm=False, match_component_norm=False,
                )))
    return rows


def svd_continuous_refine_configs():
    return [("svd_continuous_refine", f"rank={rank},C={strength:g}", replace(
        DEFAULT, persistent_rank=rank, strength=strength, intervention_positions=3,
        continue_generation=True, restore_residual_norm=False, match_component_norm=False,
    )) for rank, strengths in ((1, (9.0, 10.0, 11.0)), (2, (9.0, 10.0, 11.0)),
                              (4, (5.0, 6.0, 7.0))) for strength in strengths]


def persistent_shared_basis(source, target, cfg, unembedding, norm_gain):
    bases, diagnostics = [], {"basis_geometry": "centered_unit_gain_weighted_unembedding"}
    for name, sample in (("source", source), ("target", target)):
        end = sample["content_end"]
        basis, persistence, ids = token_persistent_subspace(
            sample["residuals"][:, end-cfg.readout_positions:end].permute(1, 0, 2),
            unembedding, norm_gain, persistent_rank=cfg.persistent_rank,
            early_layer=cfg.detector_layers[0], peak_layer=cfg.detector_layers[1],
            output_layer=cfg.detector_layers[2], rank=cfg.rank,
            normalize_unembedding_rows=True,
        )
        bases.append(basis)
        diagnostics[name] = {"persistence": persistence.tolist(), "token_ids": ids.tolist()}
    vectors, singular_values, _ = torch.linalg.svd(torch.cat(bases, dim=1), full_matrices=False)
    shared = vectors[:, singular_values > 1e-5]
    diagnostics["shared_rank"] = shared.shape[1]
    return shared, diagnostics


def persistent_delta(source, target, cfg, unembedding, norm_gain, layers):
    shared, diagnostics = persistent_shared_basis(source, target, cfg, unembedding, norm_gain)
    deltas = {}
    for layer in layers:
        means = [sample["residuals"][layer, sample["content_end"]-cfg.readout_positions:
                  sample["content_end"]].float().mean(0) for sample in (source, target)]
        displacement = {"difference": means[1] - means[0],
                        "source_remove": -means[0], "target_add": means[1]}[cfg.delta_component]
        deltas[layer] = component(displacement, shared)
        if cfg.random_delta_seed >= 0:
            generator = torch.Generator(device=shared.device).manual_seed(cfg.random_delta_seed + layer)
            direction = torch.randn(means[0].shape, device=shared.device, generator=generator)
            deltas[layer] = direction * deltas[layer].norm() / direction.norm()
    return deltas, diagnostics


TARGET_PRESETS = {
    "dog": (TARGET_PROMPT, "4"),
    "ant": (
        "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ",
        "6",
    ),
    "ant-anthill": ("Fact: The number of legs on the animal that builds anthills is ", "6"),
}
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


def demo_configs() -> list[tuple[str, str, Config]]:
    return [("default", "default", DEFAULT)]


def chat_strength_configs() -> list[tuple[str, str, Config]]:
    return [
        ("strength", f"C={strength:g}", replace(DEFAULT, strength=strength))
        for strength in (2.0, 2.5, 3.0, 4.0)
    ]


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


def persistent_direction_configs() -> list[tuple[str, str, Config]]:
    rows = []
    for aggregation in ("persistent", "union"):
        for intervention_layers in ((24,), (24, 26)):
            for strength in (1.0, 2.0, 4.0):
                layers = "+".join(map(str, intervention_layers))
                value = f"aggregation={aggregation},L={layers},C={strength:g}"
                rows.append((
                    "persistent_direction",
                    value,
                    replace(
                        DEFAULT,
                        aggregation=aggregation,
                        intervention_layer=intervention_layers,
                        intervention_positions=1,
                        strength=strength,
                    ),
                ))
    return rows


def first_answer(text: str, answers: tuple[str, ...]) -> str | None:
    alternatives = "|".join(re.escape(answer) for answer in answers)
    match = re.search(rf"(?<!\d)({alternatives})(?!\d)", text)
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


def named_suppression_diagnostics(sample, cfg, scores, token_ids, centered_rows, *, post_edit=False):
    """Separate absent, already-written, and unsuppressed concepts. -- Codex/GPT-6"""
    start = sample["content_end"] - cfg.readout_positions
    h = sample["residuals"][list(cfg.detector_layers), start:sample["content_end"]].float()
    h = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
    logits = h @ centered_rows.T
    named_scores = scores[:, token_ids]
    ranks = (scores[:, :, None] > named_scores[:, None, :]).sum(1) + 1
    patch_start = (sample["content_start"] if cfg.intervention_positions == "all"
                   else sample["content_end"] - cfg.intervention_positions)
    return [{"position": start + position, "patched": post_edit and start + position >= patch_start, "concepts": {
        word: {"token_id": token_ids[i], "centered_logits_early_peak_output": logits[:, position, i].tolist(),
               "rise": float(logits[1, position, i] - logits[0, position, i]),
               "fall": float(logits[1, position, i] - logits[2, position, i]),
               "suppression_score": float(named_scores[position, i]),
               "suppression_rank_min_ties": int(ranks[position, i])}
        for i, word in enumerate((" spider", " dog", " ant"))
    }} for position in range(cfg.readout_positions)]


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


def generate_with_first_logits(model, tokenizer, input_ids, blocks, hooks, residual_capture=None, max_new_tokens=32) -> tuple[dict, torch.Tensor]:
    raw_final = []
    def capture_final(_module, inputs):
        if not raw_final:
            raw_final.append(inputs[0].detach())
        elif len(raw_final) == 1:
            raw_final.append(inputs[0].detach())
        else:
            raw_final[1] = inputs[0].detach()
    handle = model.model.norm.register_forward_pre_hook(capture_final)
    with layer_hooks(blocks, hooks), torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True,
            return_dict_in_generate=True,
            output_scores=True,
            output_hidden_states=residual_capture is not None,
        )
    handle.remove()
    if residual_capture is not None:
        residual_capture.append(torch.stack(
            [hidden[0] for hidden in output.hidden_states[0][:-1]] + [raw_final[0][0]]
        ))
        residual_capture.append(torch.stack(
            [hidden[0] for hidden in output.hidden_states[-1][:-1]] + [raw_final[-1][0]]
        ))
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
            "top_tokens", "generation", "donor_generation", "readout", "base_readout", "target_readout", "config",
            "intervention_record", "persistence", "base_generation", "base_top_tokens", "readout_by_position", "clamped_donor",
            "named_suppression_diagnostics",
        }
    )
    return f"""---
{frontmatter}
---

# {row['condition_id']}

Expected Base answer: `{row['source_output']}`. Expected donor-directed answer:
`{row['target_output']}`. A digit match alone does not establish concept replacement;
inspect the readout and full continuation below.

Steering continues during generation: `{row['config']['continue_generation']}`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

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

Unmodified donor generation ({row['donor_generation_tokens']} tokens, verbatim):

```text
{row['donor_generation']['text']}
```

Base suppression readout:

```python
{row['base_readout']!r}
```

Base generation (verbatim):

```text
{row['base_generation']['text']}
```

Base next-token distribution:

{distribution_table(row['base_top_tokens'])}

Suppression-score readout at prompt prefill ({row['config']['aggregation']} detector, not SVD basis labels):

```python
{row['readout']!r}
```

Per-position readout (the union above can include an unpatched earlier token):

```json
{json.dumps(row['readout_by_position'], ensure_ascii=False, indent=2)}
```

Fixed-concept diagnostic (same normalized scoring geometry; vocabulary-centered logits).
Columns follow detector early/peak/output layers. Rank is one plus the number of strictly
greater scores, so tied zero scores can share a rank. No ant suppression is implied by an
ant continuation: a missing rise or fall also gives a zero suppression score.

```json
{json.dumps(row['named_suppression_diagnostics'], ensure_ascii=False, indent=2)}
```

Readout at the last decode step (the state predicting the final generated token):

```python
{row['last_decode_readout']!r}
```

Clean-donor clamp control (when applicable):

```json
{json.dumps(row['clamped_donor'], ensure_ascii=False, indent=2)}
```

Unmodified donor readout:

```python
{row['target_readout']!r}
```

Measured intervention norms:

```json
{json.dumps(row['intervention_record'], ensure_ascii=False, indent=2)}
```

SVD persistence diagnostics (eigenvalues of average token projectors):

```json
{json.dumps(row['persistence'], ensure_ascii=False, indent=2)}
```

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation ({row['generation_tokens']} tokens, verbatim):

```text
{row['generation']['text']}
```

{distribution_table(row['top_tokens'])}

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
"""


def run(
    output_dir: Path,
    sweep: str,
    prompt_mode: str,
    target_prompt: str,
    source_output: str,
    target_output: str,
    source_prompt: str = SOURCE_PROMPT,
    condition_index: int | None = None,
    max_new_tokens: int = 32,
    lens_corpus_arrow: Path | None = None,
    target_concept: str = "dog",
) -> None:
    started = time.monotonic()
    git_state = subprocess.run(
        ["git", "describe", "--always", "--dirty"], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    code_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in (
        "scripts/oat_sweep.py", "scripts/demo.py", "scripts/prompt.py",
        "scripts/delayed_readout.py", "scripts/results.py", "suppressed_activation_subspace.py",
    )}
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
    named_ids = [one_token(tokenizer, word) for word in (" spider", " dog", " ant")]
    normalized_rows = unembedding.float() * norm_gain.float()
    normalized_rows = normalized_rows / normalized_rows.norm(dim=-1, keepdim=True)
    named_centered_rows = normalized_rows[named_ids] - normalized_rows.mean(0)
    del normalized_rows

    def sample(content, generate=True):
        if prompt_mode == "raw":
            input_ids = tokenizer(
                content, add_special_tokens=False, return_tensors="pt"
            ).input_ids.cuda()
            chat = {"input_ids": input_ids, "content_start": 0, "content_end": input_ids.shape[1]}
        elif prompt_mode == "chat-fact":
            chat = chat_input_ids(tokenizer, content, enable_thinking=False, instruction="")
        elif prompt_mode == "chat-instructed":
            chat = chat_input_ids(tokenizer, content, enable_thinking=False)
        elif prompt_mode == "chat-assistant-prefill":
            chat = assistant_prefill_input_ids(tokenizer, content)
        else:
            raise ValueError(prompt_mode)
        if not generate:
            residuals, logits = trajectory(model, chat["input_ids"], final_norm)
            return {**chat, "residuals": residuals, "logits": logits}
        captured = []
        generation, logits = generate_with_first_logits(model, tokenizer, chat["input_ids"], blocks, {}, captured, max_new_tokens)
        return {**chat, "residuals": captured[0], "logits": logits, "generation": generation}

    source = sample(source_prompt)
    target = sample(target_prompt)
    source_id = one_token(tokenizer, source_output)
    target_id = one_token(tokenizer, target_output)
    base_generation, base_generation_logits = source["generation"], source["logits"]
    donor_generation, donor_generation_logits = target["generation"], target["logits"]
    base_logp = base_generation_logits.log_softmax(-1)
    donor_logp = donor_generation_logits.log_softmax(-1)
    base_log_odds = float(base_logp[target_id] - base_logp[source_id])
    special_ids = set(tokenizer.all_special_ids)
    source_rendered = tokenizer.decode(source["input_ids"][0], skip_special_tokens=False)
    target_rendered = tokenizer.decode(target["input_ids"][0], skip_special_tokens=False)
    sweep_configs = {
        "demo": demo_configs,
        "coordinate-swap": coordinate_swap_configs,
        "coordinate-layer": coordinate_layer_configs,
        "coordinate-layer-strong": coordinate_layer_strong_configs,
        "coordinate-band": coordinate_band_configs,
        "template-contrast": template_contrast_configs,
        "template-projection": template_projection_configs,
        "template-clamp": template_clamp_configs,
        "template-scope": template_scope_configs,
        "template-band-strength": template_band_strength_configs,
        "future-coordinate": future_coordinate_configs,
        "future-gated": future_gated_configs,
        "future-template": future_template_configs,
        "svd": svd_configs,
        "svd-refine": svd_refine_configs,
        "svd-detector": svd_detector_configs,
        "svd-band": svd_band_configs,
        "svd-control": svd_control_configs,
        "svd-tokens": svd_tokens_configs,
        "svd-candidates": svd_candidates_configs,
        "svd-parts": svd_parts_configs,
        "svd-continuous": svd_continuous_configs,
        "svd-continuous-refine": svd_continuous_refine_configs,
        "chat-strength": chat_strength_configs,
        "oat": configs,
        "normalization-strength": normalization_strength_configs,
        "lexical-surface": lexical_configs,
        "layer-position-strength": layer_position_strength_configs,
        "layer-combo": layer_combo_configs,
        "persistent-generation": persistent_generation_configs,
        "persistent-direction": persistent_direction_configs,
    }[sweep]()
    indexed_configs = list(enumerate(sweep_configs))
    if condition_index is not None:
        indexed_configs = [indexed_configs[condition_index]]
    future_vectors, future_provenance = {}, {}
    if any(cfg.future_coordinate for _, (_, _, cfg) in indexed_configs):
        future_vectors, future_provenance = fit_future_rows(model, tokenizer, lens_corpus_arrow, output_dir)

    template_deltas, template_provenance, template_targets = {}, [], {}
    if any(cfg.template_contrast for _, (_, _, cfg) in indexed_configs):
        differences, target_means = [], []
        for template in CONCEPT_TEMPLATES:
            pair = [sample(template.format(animal=animal), generate=False)
                    for animal in ("spider", target_concept)]
            source_end, target_end = [item["content_end"] for item in pair]
            torch.testing.assert_close(pair[0]["input_ids"][0, source_end-3:source_end],
                                       pair[1]["input_ids"][0, target_end-3:target_end])
            differences.append((pair[1]["residuals"][:, target_end-3:target_end].float()
                                - pair[0]["residuals"][:, source_end-3:source_end].float()).mean(1))
            target_means.append(pair[1]["residuals"][:, target_end-3:target_end].float().mean(1))
            template_provenance.append([
                tokenizer.decode(item["input_ids"][0], skip_special_tokens=False) for item in pair
            ])
        template_deltas = dict(enumerate(torch.stack(differences).mean(0)))
        template_targets = dict(enumerate(torch.stack(target_means).mean(0)))
    rows = []
    for index, (axis, value, cfg) in indexed_configs:
        _, base_ids, base_scores = subspace(source, cfg, unembedding, norm_gain)
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
        fixed_deltas, persistence = (None, {})
        coordinate_directions = None
        if cfg.coordinate_swap:
            target_word = " " + target_concept
            ids = [one_token(tokenizer, word) for word in (" spider", target_word)]
            coordinate_directions = ((unembedding[ids].float() - unembedding.float().mean(0)) * norm_gain.float()).T
            raw_norms = coordinate_directions.norm(dim=0)
            persistence = {"concept_tokens": [" spider", target_word], "direction_estimator": "centered_unembedding"}
            if cfg.future_coordinate:
                coordinate_directions = future_vectors[intervention_layers[0]][:, [0, {"dog": 1, "ant": 2}[target_concept]]]
                raw_norms = coordinate_directions.norm(dim=0)
                persistence = {"concept_tokens": [" spider", target_word], "direction_estimator": "future_vjp", **future_provenance}
            if cfg.persistent_rank:
                shared, diagnostics = persistent_shared_basis(source, target, cfg, unembedding, norm_gain)
                coordinate_directions = shared @ (shared.T @ coordinate_directions)
                persistence.update(diagnostics)
                persistence["direction_estimator"] = "persistent_projected_future_vjp" if cfg.future_coordinate else "persistent_projected_centered_unembedding"
            persistence["retained_norm_fraction"] = (coordinate_directions.norm(dim=0) / raw_norms).tolist()
            coordinate_directions = coordinate_directions / coordinate_directions.norm(dim=0)
            assert torch.linalg.matrix_rank(coordinate_directions) == 2
            persistence["pair_singular_values"] = torch.linalg.svdvals(coordinate_directions).tolist()
            persistence["direction_cosine"] = float(coordinate_directions[:, 0] @ coordinate_directions[:, 1])
        elif cfg.template_contrast:
            fixed_deltas = {layer: template_deltas[layer] for layer in intervention_layers}
            persistence = {"direction_estimator": "matched_template_mean_difference",
                           "rendered_template_pairs": template_provenance}
            if cfg.future_coordinate:
                assert not cfg.persistent_rank
                projected = {}
                retained = {}
                for layer, delta in fixed_deltas.items():
                    vectors = future_vectors[layer][:, [0, {"dog": 1, "ant": 2}[target_concept]]]
                    assert torch.linalg.matrix_rank(vectors) == 2
                    basis = torch.linalg.qr(vectors, mode="reduced").Q
                    projected[layer] = component(delta, basis)
                    retained[layer] = float(projected[layer].norm() / delta.norm())
                    if cfg.match_component_norm:
                        projected[layer] = projected[layer] * delta.norm() / projected[layer].norm()
                        torch.testing.assert_close(projected[layer].norm(), delta.norm())
                fixed_deltas = projected
                persistence.update(direction_estimator="future_projected_template_mean_difference",
                                   future_provenance=future_provenance,
                                   projected_norm_fraction=retained)
            if cfg.persistent_rank:
                shared, diagnostics = persistent_shared_basis(source, target, cfg, unembedding, norm_gain)
                projected = {layer: component(delta, shared) for layer, delta in fixed_deltas.items()}
                persistence["projected_norm_fraction"] = {
                    layer: float(projected[layer].norm() / delta.norm())
                    for layer, delta in fixed_deltas.items()
                }
                if cfg.match_component_norm:
                    projected = {layer: projected[layer] * delta.norm() / projected[layer].norm()
                                 for layer, delta in fixed_deltas.items()}
                    for layer, delta in fixed_deltas.items():
                        torch.testing.assert_close(projected[layer].norm(), delta.norm())
                fixed_deltas = projected
                persistence.update(diagnostics)
            if cfg.random_delta_seed >= 0:
                for layer, delta in fixed_deltas.items():
                    generator = torch.Generator(device=delta.device).manual_seed(cfg.random_delta_seed + layer)
                    random_delta = torch.randn(delta.shape, device=delta.device, generator=generator)
                    fixed_deltas[layer] = random_delta * delta.norm() / random_delta.norm()
        elif cfg.persistent_rank:
            fixed_deltas, persistence = persistent_delta(
                source, target, cfg, unembedding, norm_gain, intervention_layers
            )
            for name in ("source", "target"):
                persistence[name]["tokens"] = [
                    [tokenizer.decode([token]) for token in ids]
                    for ids in persistence[name]["token_ids"]
                ]
        target_coordinates = {layer: template_targets[layer] @ (delta / delta.norm())
                              for layer, delta in fixed_deltas.items()} if cfg.template_clamp else None
        hooks = intervention_hooks(
            source_basis,
            target_basis,
            target["residuals"],
            operation="coordinate_clamp" if cfg.template_clamp else ("coordinate_swap" if cfg.coordinate_swap else ("fixed_delta" if cfg.persistent_rank or cfg.template_contrast else "replace")),
            target_coordinates=target_coordinates,
            coordinate_directions=coordinate_directions,
            source_dominant_only=cfg.source_dominant_only,
            fixed_deltas=fixed_deltas,
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
        captured = []
        generation, generation_logits = generate_with_first_logits(
            model, tokenizer, source["input_ids"], blocks, hooks, captured, max_new_tokens
        )
        changed_residuals = captured[0]
        _, last_ids = suppressed_activation_subspace(
            captured[-1][:, -1][None], unembedding, norm_gain,
            early_layer=cfg.detector_layers[0], peak_layer=cfg.detector_layers[1],
            output_layer=cfg.detector_layers[2], rank=cfg.rank, normalize_unembedding_rows=True,
        )
        _, changed_ids, changed_scores = subspace(
            {**source, "residuals": changed_residuals}, cfg, unembedding, norm_gain
        )
        readout = [tokenizer.decode([int(token_id)]) for token_id in changed_ids]
        position_scores, position_ids = changed_scores.topk(cfg.rank, dim=-1)
        readout_by_position = [{
            "position": source["content_end"] - cfg.readout_positions + i,
            "patched": i >= cfg.readout_positions - positions,
            "tokens": [tokenizer.decode([token]) for token in ids],
            "scores": scores,
        } for i, (ids, scores) in enumerate(zip(position_ids.tolist(), position_scores.tolist()))]
        target_readout = [tokenizer.decode([int(token_id)]) for token_id in target_ids]
        logp = generation_logits.log_softmax(-1)
        if cfg.continue_generation:
            for patch in intervention_record.values():
                assert patch["decode_steps"] == len(generation["token_ids"]) - 1
                assert patch["prefill_positions"] == list(range(
                    source["content_end"] - positions, source["content_end"]
                ))
        if cfg.strength == 0:
            torch.testing.assert_close(generation_logits, base_generation_logits, rtol=0, atol=0)
            assert generation["token_ids"] == base_generation["token_ids"]
        condition_id = re.sub(r"[^A-Za-z0-9_.=-]+", "_", f"{index:03d}_{axis}_{value}")
        condition_dir = output_dir / "conditions" / condition_id
        condition_dir.mkdir(parents=True)
        clamped_donor = None
        if cfg.template_clamp:
            donor_record = {}
            donor_hooks = intervention_hooks(
                source_basis, target_basis, target["residuals"], operation="coordinate_clamp",
                fixed_deltas=fixed_deltas, target_coordinates=target_coordinates,
                blocks_to_hook=[layer - 1 for layer in intervention_layers],
                positions=positions, source_position=target["content_end"] - 1,
                target_position=target["content_end"] - 1, strength=cfg.strength,
                restore_norm=False, record=donor_record,
            )
            donor_changed, _ = generate_with_first_logits(
                model, tokenizer, target["input_ids"], blocks, donor_hooks,
                max_new_tokens=max_new_tokens,
            )
            for patch in donor_record.values():
                assert patch["decode_steps"] == len(donor_changed["token_ids"]) - 1
            if cfg.strength == 0:
                assert donor_changed == donor_generation
            clamped_donor = {"generation": donor_changed, "intervention_record": donor_record}
        row = {
            "model": MODEL,
            "target_concept": target_concept,
            "revision": REVISION,
            "git": git_state,
            "code_sha256": code_hashes,
            "condition_id": condition_id,
            "axis": axis,
            "value": value,
            "is_default": axis == "default",
            "readout_from_generation": True,
            "expected_base_answer": source_output,
            "expected_steered_answer": target_output,
            "persistence": persistence,
            "swap_log_odds_shift": float(logp[target_id] - logp[source_id] - base_log_odds),
            "valid_answer_mass": float(logp[target_id].exp() + logp[source_id].exp()),
            "source_output": source_output,
            "target_output": target_output,
            "donor_p_target": float(donor_logp[target_id].exp()),
            "donor_first_answer": first_answer(donor_generation["text"], (target_output,)),
            "donor_generation_tokens": len(donor_generation["token_ids"]),
            "p_target": float(logp[target_id].exp()),
            "p_source": float(logp[source_id].exp()),
            "repeated_bigram_fraction": repetition_bigram_fraction(
                generation["token_ids"], special_ids
            ),
            "generation_tokens": len(generation["token_ids"]),
            "first_token": tokenizer.decode(generation["token_ids"][:1]),
            "first_answer": first_answer(generation["text"], (source_output, target_output)),
            "mentions_spins_webs": "spins webs" in generation["text"],
            "readout_overlap": len(set(readout) & set(target_readout)) / cfg.rank,
            "intervention_record": intervention_record,
            "log": str((condition_dir / "run.md").relative_to(output_dir)),
            "config": asdict(cfg),
            "readout": readout,
            "readout_by_position": readout_by_position,
            "named_suppression_diagnostics": {
                "detector_layers": cfg.detector_layers,
                "base": named_suppression_diagnostics(source, cfg, base_scores, named_ids, named_centered_rows),
                "post_edit": named_suppression_diagnostics(
                    {**source, "residuals": changed_residuals}, cfg, changed_scores, named_ids, named_centered_rows,
                    post_edit=True,
                ),
            },
            "clamped_donor": clamped_donor,
            "base_readout": [tokenizer.decode([int(token)]) for token in base_ids],
            "last_decode_readout": [tokenizer.decode([int(token)]) for token in last_ids[0]],
            "target_readout": target_readout,
            "generation": generation,
            "base_generation": base_generation,
            "base_top_tokens": token_distribution(tokenizer, base_generation_logits, base_generation_logits),
            "donor_generation": donor_generation,
            "top_tokens": token_distribution(tokenizer, generation_logits, base_generation_logits),
        }
        (condition_dir / "run.md").write_text(
            condition_report(row, source_rendered, target_rendered)
        )
        rows.append(row)
        logger.info("{}/{} {}", index + 1, len(sweep_configs), condition_id)

    result = {
        "model": MODEL,
        "elapsed_seconds": time.monotonic() - started,
        "peak_gpu_memory_bytes": torch.cuda.max_memory_allocated(),
        "argv": sys.argv,
        "revision": REVISION,
        "git": git_state,
        "code_sha256": code_hashes,
        "package_versions": {name: version(name) for name in ("torch", "transformers", "accelerate", "pyarrow")},
        "default": asdict(DEFAULT),
        "prompt_mode": prompt_mode,
        "source_prompt": source_prompt,
        "target_prompt": target_prompt,
        "target_concept": target_concept,
        "lexical_pairs": LEXICAL_PAIRS if sweep == "lexical-surface" else None,
        "base": {
            "source_output": source_output,
            "target_output": target_output,
            "p_target": float(base_logp[target_id].exp()),
            "p_source": float(base_logp[source_id].exp()),
            "generation": base_generation,
        },
        "donor_base": {
            "target_output": target_output,
            "p_target": float(donor_logp[target_id].exp()),
            "generation": donor_generation,
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
            "demo", "chat-strength", "oat", "normalization-strength", "lexical-surface",
            "coordinate-swap",
            "coordinate-layer",
            "coordinate-layer-strong",
            "coordinate-band",
            "template-contrast",
            "template-projection",
            "template-clamp",
            "template-scope",
            "template-band-strength",
            "future-coordinate",
            "future-gated",
            "future-template",
            "svd",
            "svd-refine",
            "svd-detector",
            "svd-band",
            "svd-control",
            "svd-tokens",
            "svd-candidates",
            "svd-parts",
            "svd-continuous",
            "svd-continuous-refine",
            "layer-position-strength", "layer-combo",
            "persistent-generation",
            "persistent-direction",
        ),
        default="demo",
    )
    parser.add_argument(
        "--prompt-mode",
        choices=("raw", "chat-fact", "chat-instructed", "chat-assistant-prefill"),
        default="raw",
    )
    parser.add_argument("--target-prompt")
    parser.add_argument("--source-prompt", default=SOURCE_PROMPT)
    parser.add_argument("--condition-index", type=int)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--lens-corpus-arrow", type=Path)
    parser.add_argument("--source-output", default="8")
    parser.add_argument("--target-output")
    parser.add_argument("--target", choices=TARGET_PRESETS, default="dog")
    args = parser.parse_args()
    preset_prompt, preset_output = TARGET_PRESETS[args.target]
    if args.target_prompt is None:
        args.target_prompt = preset_prompt
    if args.target_output is None:
        args.target_output = preset_output
    run(
        args.output_dir,
        args.sweep,
        args.prompt_mode,
        args.target_prompt,
        args.source_output,
        args.target_output,
        args.source_prompt,
        args.condition_index,
        args.max_new_tokens,
        args.lens_corpus_arrow,
        {"dog": "dog", "ant": "ant", "ant-anthill": "ant"}[args.target],
    )
