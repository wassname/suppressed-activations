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
from scripts.prompt import PREFILL_INSTRUCTION, assistant_prefill_input_ids, first_answer
from scripts.demo import intervention_hooks, layer_hooks, one_token, trajectory
from suppressed_activation_subspace import (
    component,
    suppressed_activation_scores,
    subspace_from_scores,
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
    shared_replacement: str = "none"
    source_dominant_only: bool = False
    template_contrast: bool = False
    contrastive_suppression: bool = False
    template_state_span: str = "none"
    discarded_fraction: float = 0.0
    normalize_selector_residuals: bool = False
    bee_correction: float = 0.0
    bee_correction_seed: int = -1
    bee_correction_only: bool = False
    project_bee_correction: bool = False
    transport_readout: bool = False
    template_clamp: bool = False
    future_coordinate: bool = False
    future_clamp: bool = False
    future_lexical_union: bool = False


DEFAULT = Config()

FUTURE_FORMS = {
    "spider": (" spider", " Spider", " spiders"),
    "dog": (" dog", " Dog", " dogs"),
    "ant": (" ant", " Ant", " ants"),
}


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
    rows = [("template_projection", f"L{layer}_rank{rank}_C{strength}", replace(
        DEFAULT, template_contrast=True, persistent_rank=rank,
        intervention_layer=(layer,),
        strength=strength, match_component_norm=True, restore_residual_norm=False,
    )) for layer in (20, 24) for rank in (4, 8, 16, 32) for strength in (0.0, 0.5, 1.0, 2.0)]
    rows.extend(("template_selected_random", str(seed), replace(
        DEFAULT, template_contrast=True, strength=1.0,
        random_delta_seed=seed, match_component_norm=False, restore_residual_norm=False,
    )) for seed in range(12))
    return rows


def template_detector_configs():
    return [("template_detector", f"D{early}_{peak}_{late}_matched{matched}", replace(
        DEFAULT, template_contrast=True, persistent_rank=4,
        detector_layers=(early, peak, late), intervention_layer=(20,), strength=2.0,
        match_component_norm=matched, restore_residual_norm=False,
    )) for early, peak, late in ((23, 25, 32), (8, 20, 32), (16, 20, 24))
        for matched in (False, True)]


def template_selector_configs():
    return [("template_selector", f"contrastive{contrastive}_matched{matched}_C{strength}", replace(
        DEFAULT, template_contrast=True, contrastive_suppression=contrastive,
        persistent_rank=4, intervention_layer=(20,), strength=strength,
        match_component_norm=matched, restore_residual_norm=False,
    )) for contrastive in (False, True) for matched in (False, True)
        for strength in (0.0, 2.0)]


def template_state_configs():
    return [("template_state", f"{span}_matched{matched}_C{strength}", replace(
        DEFAULT, template_contrast=True, template_state_span=span,
        persistent_rank=4, intervention_layer=(20,), strength=strength,
        match_component_norm=matched, restore_residual_norm=False,
    )) for span in ("peak", "update", "output") for matched in (False, True)
        for strength in (0.0, 2.0)]


def template_attenuation_configs():
    return [("template_attenuation", f"{span}_matched{matched}_C{strength}", replace(
        DEFAULT, template_contrast=True, template_state_span=span,
        persistent_rank=4, intervention_layer=(20,), strength=strength,
        match_component_norm=matched, restore_residual_norm=False,
    )) for span in ("peak_split", "attenuation") for matched in (False, True)
        for strength in (0.0, 2.0)]


def synchronized_attenuation_configs():
    return [("synchronized_attenuation", f"{mode}_L{layer}_C{strength}", Config(
        template_contrast=True, template_state_span="attenuation", persistent_rank=4,
        detector_layers=(layer-2, layer, 32), intervention_layer=(layer,),
        shared_replacement=mode, strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for mode in ("frozen", "synchronized") for layer in (20, 24) for strength in (0.0, 1.0, 2.0)]


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


def template_band_clamp_configs():
    return [("template_band_clamp", f"clamp{clamp}_C{strength}", replace(
        DEFAULT, template_contrast=True, template_clamp=clamp,
        intervention_layer=tuple(range(16, 21)), strength=strength,
        match_component_norm=False, restore_residual_norm=False,
    )) for clamp in (False, True) for strength in (0.0, 0.25, 0.5, 0.625, 0.75, 1.0)]


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


def future_union_configs():
    return [("future_union", f"union{union}_matched{matched}_C{strength}", replace(
        DEFAULT, template_contrast=True, future_coordinate=True, future_lexical_union=union,
        intervention_layer=(20,), strength=strength,
        match_component_norm=matched, restore_residual_norm=False,
    )) for union in (False, True) for matched in (False, True) for strength in (0.0, 1.0)]


def fit_span_transport(model, tokenizer, basis, layer, corpus_path, instruction, output_dir):
    """Central differences for the restricted source-mean/future-sum Jacobian. -- Codex/GPT-6"""
    texts = arrow_ipc.open_stream(corpus_path).read_all()["text"].to_pylist()
    texts = random.Random(0).sample([text.strip() for text in texts if len(text.strip()) >= 600], 16)
    estimates, corpus = [], []
    for text in texts:
        content = tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)[:128])
        chat = assistant_prefill_input_ids(tokenizer, content, instruction=instruction)
        ids = chat["input_ids"]
        valid = torch.arange(max(16, chat["content_start"]), chat["content_end"]-1, device=ids.device)
        assert len(valid) > 0
        corpus.append({"rendered": chat["rendered"], "valid_positions": valid.tolist()})
        scales = []
        for epsilon in (0.5, 1.0):
            columns = []
            for direction in basis.T:
                endpoints = []
                for sign in (-1, 1):
                    def patch(_module, _inputs, output):
                        changed = output.clone()
                        changed[:, valid] = (changed[:, valid].float() + sign*epsilon*direction).to(output.dtype)
                        return changed
                    with torch.no_grad(), layer_hooks(model.model.layers, {layer-1: patch}):
                        result = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                                       use_cache=False, output_hidden_states=True)
                    endpoints.append(result.hidden_states[31][0, valid].float().mean(0))
                    del result
                columns.append((endpoints[1]-endpoints[0]) / (2*epsilon))
            scales.append(torch.stack(columns, dim=1))
        estimates.append(torch.stack(scales))
    transports = torch.stack(estimates).mean(0)
    torch.save({"basis": basis.cpu(), "transports": transports.cpu()}, output_dir / "span_transport.pt")
    return transports[1], {"epsilons": [0.5, 1.0], "corpus": corpus,
                           "relative_scale_difference": float((transports[0]-transports[1]).norm()/transports[1].norm()),
                           "column_cosines": torch.nn.functional.cosine_similarity(transports[0], transports[1], dim=0).tolist()}


def fit_future_rows(
    model, tokenizer, corpus_path, output_dir, *, lexical_union=False, instruction=PREFILL_INSTRUCTION,
):
    """Contract final-residual mean-J with gain-weighted vocabulary rows. -- Codex/GPT-6"""
    texts = arrow_ipc.open_stream(corpus_path).read_all()["text"].to_pylist()
    texts = random.Random(0).sample([text.strip() for text in texts if len(text.strip()) >= 600], 16)
    assert len(texts) == 16
    layers = (12, 16, 20, 24)
    words = (" spider", " dog", " ant")
    if lexical_union:
        words += tuple(word for forms in FUTURE_FORMS.values() for word in forms[1:])
    output_rows = model.lm_head.weight[[one_token(tokenizer, word) for word in words]].float()
    output_rows = output_rows * (1.0 + model.model.norm.weight.float())
    samples, corpus, derivative_checks = [], [], []
    model.requires_grad_(False)
    for index, text in enumerate(texts):
        content = tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)[:128])
        chat = assistant_prefill_input_ids(tokenizer, content, instruction=instruction)
        ids = chat["input_ids"]
        valid = torch.arange(max(16, chat["content_start"]), chat["content_end"] - 1, device=ids.device)
        assert len(valid) > 0
        corpus.append({"text": content, "input_ids": ids[0].tolist(), "valid_positions": valid.tolist(),
                       "rendered": tokenizer.decode(ids[0], skip_special_tokens=False)})
        def grad_leaf(_module, _inputs, output):
            return output.requires_grad_(True)
        final_residual = []
        def capture_final(_module, _inputs, output):
            final_residual.append(output)
        with torch.enable_grad(), layer_hooks(model.model.layers, {11: grad_leaf, 31: capture_final}):
            output = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, output_hidden_states=True)
            hidden = tuple(output.hidden_states[layer] for layer in layers)
            target = final_residual.pop()
            per_word = []
            for word_index, row in enumerate(output_rows):
                scalar = (target[0, valid].float() @ row).sum()
                gradients = torch.autograd.grad(scalar, hidden, retain_graph=word_index < len(output_rows) - 1)
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
                    with torch.no_grad(), layer_hooks(model.model.layers, {11: perturb, 31: capture_final}):
                        perturbed = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False)
                        values.append(float((final_residual.pop()[0, valid].float() @ output_rows[0]).sum()))
                    del perturbed
                derivative_checks.append({"epsilon": epsilon, "finite_difference": (values[1]-values[0])/(2*epsilon),
                                          "autograd": float(probe_gradient.norm())})
        logger.info("future lens corpus {}/16", index + 1)
    stacked = torch.stack(samples)
    assert torch.isfinite(stacked).all()
    means = stacked.mean(0)
    vectors = {layer: means[:, i].T for i, layer in enumerate(layers)}
    provenance = {"estimator": "mean_source_sum_current_future_raw_final_gain_weighted_vjp",
                  "official_reference_commit": "581d398613e5602a5af361e1c34d3a92ea82ba8e",
                  "corpus_sampling": "16 eligible records without replacement, Python random seed0",
                  "corpus_path": str(corpus_path), "corpus_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
                  "words": words, "target_residual_layer": 32, "source_residual_layers": layers,
                  "output_row_weighting": "lm_head rows times Qwen RMSNorm gain (1 + norm.weight); no RMS denominator",
                  "attention_mask_policy": "all ones: prompts are unpadded",
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


def clean_selector_audit(samples, tokenizer, unembedding, norm_gain):
    """Compare clean detector windows without fitting an intervention. — Codex/GPT-6."""
    forms = [form for animal in ("spider", "dog", "ant") for form in FUTURE_FORMS[animal]]
    named_ids = [one_token(tokenizer, form) for form in forms]
    rows, prompts, curves = [], {}, []
    for side, sample in samples.items():
        end = sample["content_end"]
        start = max(sample["content_start"], end - 8)
        states = sample["residuals"][:, start:end].permute(1, 0, 2)
        prompts[side] = {
            "rendered": tokenizer.decode(sample["input_ids"][0], skip_special_tokens=False),
            "generation": sample["generation"],
        }
        for normalized in (False, True):
            directions = unembedding.float() * norm_gain.float()
            if normalized:
                directions = directions / directions.norm(dim=-1, keepdim=True)
            named_directions = directions[named_ids] - directions.mean(0)
            scaled_states = states.float() * torch.rsqrt(states.float().square().mean(-1, keepdim=True) + 1e-6)
            named_logits = scaled_states @ named_directions.T
            for offset in range(end - start):
                curves.append({"side": side, "normalize_unembedding_rows": normalized,
                               "position": start + offset,
                               "centered_logits_by_layer": {form: named_logits[offset, :, i].tolist()
                                                            for i, form in enumerate(forms)}})
            del directions
            for peak in (4, 8, 12, 16, 20, 24, 28, 31):
                window = (max(0, peak - 2), peak, 32)
                scores = suppressed_activation_scores(
                    states, unembedding, norm_gain, early_layer=window[0],
                    peak_layer=peak, output_layer=32,
                    normalize_unembedding_rows=normalized,
                )
                values, ids = scores.topk(8, dim=-1)
                named_scores = scores[:, named_ids]
                ranks = (scores[:, :, None] > named_scores[:, None, :]).sum(1) + 1
                for offset in range(end - start):
                    position = start + offset
                    rows.append({
                        "side": side, "normalize_unembedding_rows": normalized,
                        "detector_layers": window, "position": position,
                        "content_offset": position - sample["content_start"],
                        "token": tokenizer.decode([int(sample["input_ids"][0, position])]),
                        "top": [{"token_id": i, "token": tokenizer.decode([i]), "score": value}
                                for i, value in zip(ids[offset].tolist(), values[offset].tolist())],
                        "named": {form: {"token_id": token_id, "score": score, "rank_min_ties": rank}
                                  for form, token_id, score, rank in zip(
                                      forms, named_ids, named_scores[offset].tolist(), ranks[offset].tolist())},
                    })
    return {"prompts": prompts, "rows": rows, "named_layer_curves": curves,
            "interpretation": "Named animal scores are diagnostics, not evidence of causal replacement; zero scores have tied ranks."}


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
    h = sample["residuals"][:, start:sample["content_end"]].float()
    h = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
    layer_logits = h @ centered_rows.T
    logits = layer_logits[list(cfg.detector_layers)]
    named_scores = scores[:, token_ids]
    ranks = (scores[:, :, None] > named_scores[:, None, :]).sum(1) + 1
    patch_start = (sample["content_start"] if cfg.intervention_positions == "all"
                   else sample["content_end"] - cfg.intervention_positions)
    return [{"position": start + position, "patched": post_edit and start + position >= patch_start, "concepts": {
        word: {"token_id": token_ids[i], "centered_logits_early_peak_output": logits[:, position, i].tolist(),
               "centered_logits_by_residual_layer": layer_logits[:, position, i].tolist(),
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
            attention_mask=torch.ones_like(input_ids),
            do_sample=False,
            max_new_tokens=max_new_tokens,
            eos_token_id=[tokenizer.eos_token_id, tokenizer.pad_token_id],
            pad_token_id=tokenizer.pad_token_id,
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


def generate_synchronized_donor(model, tokenizer, source, target, basis, layer, strength,
                                positions, record, residual_capture, max_new_tokens):
    """Teacher-force the donor on source-selected tokens with separate caches. — Codex/GPT-6."""
    def forward(ids, mask_length, cache, hooks):
        raw_final = []
        handle = model.model.norm.register_forward_pre_hook(
            lambda _module, inputs: raw_final.append(inputs[0].detach()))
        try:
            with layer_hooks(model.model.layers, hooks), torch.no_grad():
                output = model(
                    input_ids=ids, attention_mask=ids.new_ones((1, mask_length)),
                    past_key_values=cache, use_cache=True, output_hidden_states=True,
                    logits_to_keep=1,
                )
        finally:
            handle.remove()
        states = torch.stack([h[0] for h in output.hidden_states[:-1]] + [raw_final[0][0]])
        return output.logits[0, -1].float(), output.past_key_values, states

    source_ids, donor_ids = source["input_ids"], target["input_ids"]
    source_length, donor_length = source_ids.shape[1], donor_ids.shape[1]
    source_cache = donor_cache = None
    token_ids, donor_history, source_history = [], [], []
    for step in range(max_new_tokens):
        donor_logits, donor_cache, donor_states = forward(donor_ids, donor_length + step, donor_cache, {})
        hooks = intervention_hooks(
            basis, basis, donor_states, operation="shared_replace", strength=strength,
            blocks_to_hook=[layer - 1], positions=positions,
            source_position=source["content_end"] - 1,
            target_position=target["content_end"] - 1 if step == 0 else 0,
            match_component_norm=False, restore_norm=False, record=record,
        )
        logits, source_cache, states = forward(source_ids, source_length + step, source_cache, hooks)
        if step == 0:
            first_logits = logits
            residual_capture.append(states)
        last_states = states
        token = int(logits.argmax())
        if layer == len(model.model.layers) and basis.shape[1] == basis.shape[0] and strength == 1:
            assert token == int(donor_logits.argmax()), "full final-layer replacement differs from synchronized donor"
        token_ids.append(token)
        if token in (tokenizer.eos_token_id, tokenizer.pad_token_id):
            break
        source_ids = source_ids.new_tensor([[token]])
        donor_ids = donor_ids.new_tensor([[token]])
        source_history.append(token)
        donor_history.append(int(donor_ids[0, 0]))
        assert source_history == donor_history
    residual_capture.append(last_states)
    record[layer]["synchronized_history"] = {
        "source_tokens": source_history, "donor_tokens": donor_history,
        "donor_conditioning": "unchanged donor prompt followed by source-selected tokens",
    }
    return {"token_ids": token_ids, "text": tokenizer.decode(token_ids, skip_special_tokens=False)}, first_logits


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

Readout status (applies to all readouts below): {row['readout_status']}.

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

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `{row['condition_id']}`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
{row['last_decode_readout']!r}
```

Unmodified donor readout:

```python
{row['target_readout']!r}
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`{row['condition_id']}`. These records are retained without truncation.

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
    prefill_instruction: str = PREFILL_INSTRUCTION,
    extraction_instruction: str | None = None,
    selector_audit: bool = False,
) -> None:
    if extraction_instruction is None:
        extraction_instruction = prefill_instruction
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

    def sample(content, generate=True, instruction=prefill_instruction):
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
            chat = assistant_prefill_input_ids(tokenizer, content, instruction=instruction)
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
    extraction_source = sample(source_prompt, generate=False, instruction=extraction_instruction)
    extraction_target = sample(target_prompt, generate=False, instruction=extraction_instruction)
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
    if selector_audit:
        audit_started = time.monotonic()
        audit = clean_selector_audit({"source": source, "target": target}, tokenizer, unembedding, norm_gain)
        audit.update(model=MODEL, revision=REVISION, git=git_state, code_sha256=code_hashes,
                     argv=sys.argv, prefill_instruction=prefill_instruction,
                     elapsed_seconds=time.monotonic() - audit_started)
        (output_dir / "selector_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
        summary = ["# Clean selector diagnostic", "",
                   "TODO validate: find a common animal-related window before intervening; animal presence alone is not causal evidence.", "",
                   "[Full position/window scores and exact clean demos](selector_audit.json). [Run provenance](result.json).", ""]
        for side in ("source", "target"):
            for normalized in (False, True):
                group = [row for row in audit["rows"] if row["side"] == side and row["normalize_unembedding_rows"] == normalized]
                expected = "spider" if side == "source" else target_concept
                hits = {animal: sum(any(item["score"] > 0 and item["rank_min_ties"] <= 8
                                       for form, item in row["named"].items() if form in FUTURE_FORMS[animal])
                                    for row in group) for animal in ("spider", "dog", "ant")}
                summary.append(f"- {side}, unit rows={normalized}, expected={expected}: top-eight position/window counts {hits}, denominator={len(group)}.")
        summary.extend(["", "— Codex/GPT-6", ""])
        (output_dir / "selector_audit.md").write_text("\n".join(summary))
        logger.info("clean selector diagnostic: {} ({} rows)", output_dir / "selector_audit.md", len(audit["rows"]))
    sweep_configs = {
        "selector-clean": lambda: [("strength", "C0", replace(DEFAULT, strength=0.0))],
        "demo": demo_configs,
        "coordinate-swap": coordinate_swap_configs,
        "coordinate-layer": coordinate_layer_configs,
        "coordinate-layer-strong": coordinate_layer_strong_configs,
        "coordinate-band": coordinate_band_configs,
        "template-contrast": template_contrast_configs,
        "template-projection": template_projection_configs,
        "template-detector": template_detector_configs,
        "template-selector": template_selector_configs,
        "template-state": template_state_configs,
        "template-attenuation": template_attenuation_configs,
        "synchronized-attenuation": synchronized_attenuation_configs,
        "attenuation-coverage": lambda: [("attenuation_coverage", f"L{layer}_positions{positions}_C{strength}", replace(
            template_attenuation_configs()[7][2], intervention_layer=(layer,),
            intervention_positions=positions, strength=strength,
        )) for layer in (12, 16, 20) for positions in (3, "all") for strength in (0.0, 1.0, 2.0)],
        "attenuation-local": lambda: [("attenuation_local", f"peak{peak}_positions{positions}_matched{matched}_C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, peak, 32),
            intervention_positions=positions, match_component_norm=matched, strength=strength,
        )) for peak in (20, 25) for positions in (3, "all") for matched in (False, True) for strength in (0.0, 2.0)],
        "attenuation-rank": lambda: [("attenuation_rank", f"rank{rank}_C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            persistent_rank=rank, strength=strength,
        )) for rank in (1, 2, 4) for strength in (0.0, 1.0, 2.0, 3.0, 4.0)],
        "attenuation-complement": lambda: [("attenuation_complement", f"discarded{fraction}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            discarded_fraction=fraction,
        )) for fraction in (0.0, 0.25, 0.5, 0.75, 1.0)],
        "attenuation-isolation": lambda: [("attenuation_isolation", f"{part}_C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            delta_component="discarded" if part == "discarded" else "difference",
            discarded_fraction=1.0 if part == "full" else 0.0,
            match_component_norm=False, strength=strength,
        )) for part in ("selected", "discarded", "full") for strength in (0.0, 2.0)],
        "attenuation-rank-expanded": lambda: [("attenuation_rank_expanded", f"rank{rank}_matched{matched}_C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            persistent_rank=rank, match_component_norm=matched, strength=strength,
        )) for rank in (4, 6, 8, 12) for matched in (False, True) for strength in (0.0, 2.0)],
        "attenuation-scale": lambda: [("attenuation_scale", f"normalized{normalized}_matched{matched}_C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            normalize_selector_residuals=normalized, match_component_norm=matched, strength=strength,
        )) for normalized in (False, True) for matched in (False, True) for strength in (0.0, 2.0)],
        "shared-replacement": lambda: [("shared_replacement", f"C{strength}", Config(
            detector_layers=(18, 20, 32), intervention_layer=(20,),
            persistent_rank=4, shared_replacement="frozen", strength=strength,
            match_component_norm=False, restore_residual_norm=False,
        )) for strength in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0)],
        "synchronized-replacement": lambda: [("synchronized_replacement", f"{mode}_L{layer}_C{strength}", Config(
            detector_layers=(max(0, layer-2), layer, 32), intervention_layer=(layer,),
            persistent_rank=0 if mode == "full_synchronized" else 4,
            shared_replacement=mode, strength=strength,
            match_component_norm=False, restore_residual_norm=False,
        )) for mode in ("frozen", "synchronized", "full_synchronized")
            for layer in ((12, 20, 32) if mode == "full_synchronized" else (12, 20)) for strength in (0.0, 1.0)],
        "synchronized-support": lambda: [("synchronized_support", f"L{layer}_rank{rank}_C{strength}", Config(
            detector_layers=(layer-2, layer, 32), intervention_layer=(layer,),
            persistent_rank=rank, shared_replacement="synchronized", strength=strength,
            match_component_norm=False, restore_residual_norm=False,
        )) for layer in (12, 20) for rank in (4, 32) for strength in (0.0, 1.0, 2.0)],
        "synchronized-dose": lambda: [("synchronized_dose", f"L{layer}_C{strength}", Config(
            detector_layers=(layer-2, layer, 32), intervention_layer=(layer,),
            persistent_rank=32, shared_replacement="synchronized", strength=strength,
            match_component_norm=False, restore_residual_norm=False,
        )) for layer in (20, 24) for strength in (0.0, 1.0, 2.0, 4.0, 8.0, 16.0)],
        "attenuation-bee-selector": lambda: [("attenuation_bee_selector", f"C{strength}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            template_state_span="attenuation_bee", strength=strength,
        )) for strength in (0.0, 2.0)],
        "attenuation-bee-correction": lambda: [("attenuation_bee_correction", f"correction{correction}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            bee_correction=correction,
        )) for correction in (0.0, 0.25, 0.5, 1.0, 2.0)],
        "bee-correction-controls": lambda: [("bee_correction_controls", f"seed{seed}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            bee_correction=0.25, bee_correction_seed=seed,
        )) for seed in range(-1, 16)],
        "bee-correction-alone": lambda: [("bee_correction_alone", f"only{only}_correction{correction}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            bee_correction=correction, bee_correction_only=only,
        )) for only in (False, True) for correction in (0.25, 0.5, 1.0)],
        "bee-correction-projected": lambda: [("bee_correction_projected", f"projected{projected}_correction{correction}", replace(
            template_attenuation_configs()[7][2], detector_layers=(18, 20, 32),
            bee_correction=correction, project_bee_correction=projected,
        )) for projected, correction in (
            [(projected, correction) for projected in (False, True)
             for correction in (0.25, 0.5, 1.0, 2.0, 4.0)]
            + [(True, correction) for correction in (1.25, 1.5, 1.75)]
        )],
        "template-transport": lambda: [("template_transport", "attenuation", replace(
            template_attenuation_configs()[7][2], transport_readout=True))],
        "template-clamp": template_clamp_configs,
        "template-scope": template_scope_configs,
        "template-band-strength": template_band_strength_configs,
        "template-band-clamp": template_band_clamp_configs,
        "future-coordinate": future_coordinate_configs,
        "future-gated": future_gated_configs,
        "future-clamp": lambda: [("future_clamp", f"L{layer}_C{strength}", replace(
            DEFAULT, coordinate_swap=True, future_coordinate=True, future_clamp=True,
            persistent_rank=0, intervention_layer=(layer,), intervention_positions=3,
            continue_generation=True, strength=strength, restore_residual_norm=False,
            match_component_norm=False,
        )) for layer in (12, 16, 20, 24) for strength in (0.0, 0.5, 1.0)],
        "future-template": future_template_configs,
        "future-union": future_union_configs,
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
        future_vectors, future_provenance = fit_future_rows(
            model, tokenizer, lens_corpus_arrow, output_dir,
            lexical_union=any(cfg.future_lexical_union for _, (_, _, cfg) in indexed_configs),
            instruction=extraction_instruction,
        )
    future_clamp_axes, future_clamp_calibration = {}, {}
    if any(cfg.future_clamp for _, (_, _, cfg) in indexed_configs):
        for layer, vectors in future_vectors.items():
            pair = vectors[:, [0, {"dog": 1, "ant": 2}[target_concept]]]
            pair = pair / pair.norm(dim=0)
            axis = pair[:, 1] - pair[:, 0]
            axis_norm = axis.norm()
            axis = axis / axis_norm
            source_score = source["residuals"][layer, source["content_end"]-1].float() @ axis
            donor_score = target["residuals"][layer, target["content_end"]-1].float() @ axis
            future_clamp_axes[layer] = axis
            future_clamp_calibration[layer] = {
                "source": float(source_score), "donor": float(donor_score),
                "threshold": float(donor_score), "axis_norm_before_normalization": float(axis_norm),
                "donor_minus_source": float(donor_score-source_score),
                "donor_above_source": bool(donor_score > source_score),
            }
        future_provenance["clamp_calibration"] = future_clamp_calibration
        lens_path = output_dir / "future_lens.json"
        lens_document = json.loads(lens_path.read_text())
        lens_document["clamp_calibration"] = future_clamp_calibration
        lens_path.write_text(json.dumps(lens_document, ensure_ascii=False, indent=2))

    template_deltas, template_provenance, template_targets = {}, [], {}
    template_suffixes = []
    bee_suffixes, bee_prompts = [], []
    if any(cfg.template_contrast for _, (_, _, cfg) in indexed_configs):
        differences, target_means = [], []
        for template in CONCEPT_TEMPLATES:
            pair = [sample(template.format(animal=animal), generate=False, instruction=extraction_instruction)
                    for animal in ("spider", target_concept)]
            source_end, target_end = [item["content_end"] for item in pair]
            if any(cfg.contrastive_suppression or cfg.template_state_span != "none"
                   for _, (_, _, cfg) in indexed_configs):
                template_suffixes.append(torch.stack([
                    item["residuals"][:, item["content_end"]-3:item["content_end"]]
                    for item in pair
                ]))
            if any(cfg.template_state_span != "none" for _, (_, _, cfg) in indexed_configs):
                bee = sample(template.format(animal="bee"), generate=False, instruction=extraction_instruction)
                torch.testing.assert_close(pair[1]["input_ids"][0, target_end-3:target_end],
                                           bee["input_ids"][0, bee["content_end"]-3:bee["content_end"]])
                bee_suffixes.append(bee["residuals"][:, bee["content_end"]-3:bee["content_end"]])
                bee_prompts.append(tokenizer.decode(bee["input_ids"][0], skip_special_tokens=False))
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
        torch.save({"deltas": torch.stack(differences).mean(0).cpu(),
                    "targets": torch.stack(target_means).mean(0).cpu()},
                   output_dir / "template_vectors.pt")
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
        assert cfg.shared_replacement in ("none", "frozen", "synchronized", "full_synchronized")
        if cfg.shared_replacement != "none":
            assert not (cfg.coordinate_swap or cfg.template_clamp or cfg.bee_correction or cfg.future_clamp)
            if cfg.template_contrast:
                assert cfg.template_state_span == "attenuation" and cfg.shared_replacement in ("frozen", "synchronized")
                assert len(intervention_layers) == 1 and cfg.detector_layers[1] == intervention_layers[0]
                assert not (cfg.match_component_norm or cfg.restore_residual_norm or cfg.normalize_selector_residuals)
                assert cfg.random_delta_seed == -1 and cfg.discarded_fraction == 0 and cfg.delta_component == "difference"
            assert cfg.continue_generation and cfg.donor_position_offset == 0
            torch.testing.assert_close(
                source["input_ids"][0, source["content_end"]-positions:source["content_end"]],
                target["input_ids"][0, target["content_end"]-positions:target["content_end"]],
            )
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
                span_singular_values = {}
                forms = (FUTURE_FORMS["spider"] + FUTURE_FORMS[target_concept]
                         if cfg.future_lexical_union else (" spider", " " + target_concept))
                columns = [future_provenance["words"].index(word) for word in forms]
                for layer, delta in fixed_deltas.items():
                    vectors = future_vectors[layer][:, columns]
                    assert torch.linalg.matrix_rank(vectors) == len(columns)
                    span_singular_values[layer] = torch.linalg.svdvals(vectors).tolist()
                    basis = torch.linalg.qr(vectors, mode="reduced").Q
                    projected[layer] = component(delta, basis)
                    retained[layer] = float(projected[layer].norm() / delta.norm())
                    if cfg.match_component_norm:
                        projected[layer] = projected[layer] * delta.norm() / projected[layer].norm()
                        torch.testing.assert_close(projected[layer].norm(), delta.norm())
                fixed_deltas = projected
                persistence.update(direction_estimator="future_projected_template_mean_difference",
                                   future_provenance=future_provenance,
                                   future_span_words=forms, future_span_singular_values=span_singular_values,
                                   projected_norm_fraction=retained)
            if cfg.persistent_rank:
                if cfg.template_state_span != "none":
                    suffixes = torch.stack(template_suffixes).float()
                    if cfg.normalize_selector_residuals:
                        suffixes = suffixes / suffixes.square().mean(-1, keepdim=True).sqrt()
                    contrasts = suffixes[:, 1] - suffixes[:, 0]
                    if cfg.template_state_span == "attenuation_bee":
                        assert target_concept == "ant"
                        bee_states = torch.stack(bee_suffixes).float()
                        if cfg.normalize_selector_residuals:
                            bee_states = bee_states / bee_states.square().mean(-1, keepdim=True).sqrt()
                        contrasts = suffixes[:, 1] - bee_states
                    peak = contrasts[:, cfg.detector_layers[1]].flatten(0, 1)
                    output = contrasts[:, cfg.detector_layers[2]].flatten(0, 1)
                    split = cfg.template_state_span in ("peak_split", "attenuation", "attenuation_bee")
                    fit_count = peak.shape[0] // 2 if split else peak.shape[0]
                    if cfg.template_state_span in ("attenuation", "attenuation_bee"):
                        columns = torch.cat([peak[:fit_count].T, output[:fit_count].T], dim=1)
                        vectors, _, _ = torch.linalg.svd(columns, full_matrices=False)
                        joint = vectors[:, :torch.linalg.matrix_rank(columns)]
                        peakJ, outputJ = peak[:fit_count] @ joint, output[:fit_count] @ joint
                        energy_difference = (peakJ.T @ peakJ - outputJ.T @ outputJ) / fit_count
                        values, eigenvectors = torch.linalg.eigh(energy_difference)
                        assert (values > 0).sum() >= cfg.persistent_rank
                        shared = joint @ eigenvectors[:, -cfg.persistent_rank:].flip(1)
                    else:
                        columns = {"peak": peak, "peak_split": peak[:fit_count],
                                   "update": peak-output, "output": output}[cfg.template_state_span].T
                        vectors, values, _ = torch.linalg.svd(columns, full_matrices=False)
                        assert torch.linalg.matrix_rank(columns) >= cfg.persistent_rank
                        shared = vectors[:, :cfg.persistent_rank]
                    diagnostics = {"selector": ("unit_rms" if cfg.normalize_selector_residuals else "raw") + "_template_contrast_" + cfg.template_state_span,
                                   "selector_contrast": [target_concept, "bee" if cfg.template_state_span == "attenuation_bee" else "spider"],
                                   "selector_residual_geometry": "unit_rms" if cfg.normalize_selector_residuals else "raw",
                                   "spectrum": values.tolist(),
                                   "fit_template_indices": list(range(fit_count // 3)),
                                   "peak_projected_contrast_norm": float((peak @ shared).norm(dim=-1).mean()),
                                   "output_projected_contrast_norm": float((output @ shared).norm(dim=-1).mean())}
                    if split:
                        for name, section in (("fit", slice(None, fit_count)), ("heldout", slice(fit_count, None))):
                            for endpoint, states in (("peak", peak), ("output", output)):
                                coordinates = states[section] @ shared
                                diagnostics[f"{name}_{endpoint}_mean_square"] = coordinates.square().mean(0).tolist()
                                diagnostics[f"{name}_{endpoint}_signed_mean"] = coordinates.mean(0).tolist()
                elif cfg.contrastive_suppression:
                    suffixes = torch.stack(template_suffixes).permute(1, 0, 3, 2, 4)
                    scores = suppressed_activation_scores(
                        suffixes.flatten(0, 2), unembedding, norm_gain,
                        early_layer=cfg.detector_layers[0], peak_layer=cfg.detector_layers[1],
                        output_layer=cfg.detector_layers[2], normalize_unembedding_rows=True,
                    ).reshape(2, -1, unembedding.shape[0]).mean(1)
                    contrast = scores[1] - scores[0]
                    signed_scores = torch.stack([-contrast, contrast]).clamp_min(0)
                    assert (signed_scores > 0).sum(1).min() >= cfg.persistent_rank
                    bases, ids = subspace_from_scores(
                        signed_scores, unembedding, norm_gain, rank=cfg.persistent_rank,
                        normalize_unembedding_rows=True,
                    )
                    directions = bases.permute(1, 0, 2).flatten(1)
                    assert torch.linalg.matrix_rank(directions) == directions.shape[1]
                    shared = torch.linalg.qr(directions, mode="reduced").Q
                    diagnostics = {"selector": "matched_template_suppression_difference",
                                   "selected_token_ids_source_target": ids.tolist(),
                                   "selected_tokens": [tokenizer.decode([i]) for i in ids.flatten().tolist()],
                                   "source_scores": scores[0, ids].tolist(),
                                   "target_scores": scores[1, ids].tolist(),
                                   "score_difference": contrast[ids].tolist()}
                else:
                    shared, diagnostics = persistent_shared_basis(source, target, cfg, unembedding, norm_gain)
                if cfg.template_state_span != "none":
                    template_coordinates = torch.stack(template_suffixes).float()[:, :, intervention_layers[0]] @ shared
                    centroids = template_coordinates[:4].mean(dim=(0, 2))
                    identity_axis = centroids[1] - centroids[0]
                    identity_axis = identity_axis / identity_axis.norm()
                    midpoint = centroids.mean(0)
                    diagnostics["clean_identity_separation"] = {
                        "method": "signed distance from midpoint of first-four-template centroids; positive is target; not independent steering evidence",
                        "template_scores_source_target_position": ((template_coordinates-midpoint) @ identity_axis).tolist(),
                        "bee_template_prompts": bee_prompts,
                        "bee_template_scores": ((torch.stack(bee_suffixes).float()[:, intervention_layers[0]] @ shared-midpoint) @ identity_axis).tolist(),
                        "heldout_template_indices": [i for i in range(4, 8) if i not in diagnostics["fit_template_indices"]],
                        "implicit_scores": {
                            name: ((sample["residuals"][intervention_layers[0], sample["content_end"]-3:sample["content_end"]].float() @ shared-midpoint) @ identity_axis).tolist()
                            for name, sample in (("source", source), ("donor", target))
                        },
                        "implicit_extraction_instruction_scores": {
                            name: ((sample["residuals"][intervention_layers[0], sample["content_end"]-3:sample["content_end"]].float() @ shared-midpoint) @ identity_axis).tolist()
                            for name, sample in (("source", extraction_source), ("donor", extraction_target))
                        },
                    }
                projected = {layer: component(delta, shared) for layer, delta in fixed_deltas.items()}
                if cfg.delta_component == "discarded":
                    assert cfg.discarded_fraction == 0.0
                    projected = {layer: delta-projected[layer] for layer, delta in fixed_deltas.items()}
                persistence["projected_norm_fraction"] = {
                    layer: float(projected[layer].norm() / delta.norm())
                    for layer, delta in fixed_deltas.items()
                }
                if cfg.discarded_fraction:
                    assert cfg.template_state_span != "none"
                    projected = {layer: projected[layer] + cfg.discarded_fraction * (delta-projected[layer])
                                 for layer, delta in fixed_deltas.items()}
                persistence["discarded_fraction_before_norm_matching"] = cfg.discarded_fraction
                if cfg.match_component_norm:
                    projected = {layer: projected[layer] * delta.norm() / projected[layer].norm()
                                 for layer, delta in fixed_deltas.items()}
                    for layer, delta in fixed_deltas.items():
                        torch.testing.assert_close(projected[layer].norm(), delta.norm())
                persistence["per_token_component_norms_after_strength"] = {
                    layer: {"selected": float(cfg.strength * component(delta, shared).norm()),
                            "discarded": float(cfg.strength * (delta-component(delta, shared)).norm())}
                    for layer, delta in projected.items()
                }
                fixed_deltas = projected
                persistence.update(diagnostics)
            if cfg.bee_correction:
                assert target_concept == "ant" and cfg.template_state_span != "none"
                persistence["base_component_norms_before_correction"] = persistence.pop("per_token_component_norms_after_strength")
                correction = (torch.stack(template_suffixes)[:, 1].float() - torch.stack(bee_suffixes).float()).mean(dim=(0, 2))
                if cfg.project_bee_correction:
                    correction = (correction @ shared) @ shared.T
                if cfg.bee_correction_seed >= 0:
                    generator = torch.Generator(device=correction.device).manual_seed(cfg.bee_correction_seed)
                    random_correction = torch.randn(correction.shape, device=correction.device, generator=generator)
                    correction = random_correction * correction.norm(dim=-1, keepdim=True) / random_correction.norm(dim=-1, keepdim=True)
                persistence["bee_correction"] = {
                    "method": "matched-norm random correction" if cfg.bee_correction_seed >= 0 else ("selected-span ant-minus-bee template mean" if cfg.project_bee_correction else "unrestricted ant-minus-bee template mean; not suppressed-only"),
                    "coefficient_after_strength": cfg.strength * cfg.bee_correction,
                    "projected_to_selected_span": cfg.project_bee_correction,
                    "per_token_norm_after_strength": {
                        layer: float((cfg.strength * cfg.bee_correction * correction[layer]).norm())
                        for layer in intervention_layers
                    },
                }
                fixed_deltas = {layer: (torch.zeros_like(delta) if cfg.bee_correction_only else delta) + cfg.bee_correction * correction[layer]
                                for layer, delta in fixed_deltas.items()}
            if cfg.random_delta_seed >= 0:
                for layer, delta in fixed_deltas.items():
                    generator = torch.Generator(device=delta.device).manual_seed(cfg.random_delta_seed + layer)
                    random_delta = torch.randn(delta.shape, device=delta.device, generator=generator)
                    fixed_deltas[layer] = random_delta * delta.norm() / random_delta.norm()
        elif cfg.shared_replacement != "none":
            assert len(intervention_layers) == 1
            if cfg.shared_replacement == "full_synchronized":
                shared = torch.eye(unembedding.shape[1], device=unembedding.device, dtype=torch.float32)
                persistence = {"direction_estimator": "full_residual_positive_control",
                               "interpretation": "donor-context transfer control, not suppressed-subspace replacement"}
            else:
                assert cfg.persistent_rank
                shared, persistence = persistent_shared_basis(source, target, cfg, unembedding, norm_gain)
                persistence["direction_estimator"] = "shared_persistent_donor_coordinate_replacement"
            source_basis = target_basis = shared
            persistence["decode_target"] = ("frozen final donor prompt coordinates" if cfg.shared_replacement == "frozen"
                                            else "donor conditioned on same source-generated token history")
        elif cfg.persistent_rank:
            fixed_deltas, persistence = persistent_delta(
                source, target, cfg, unembedding, norm_gain, intervention_layers
            )
        if cfg.template_contrast and cfg.shared_replacement != "none":
            source_basis = target_basis = shared
            fixed_deltas = None
            persistence["direction_estimator"] = "template_attenuation_donor_coordinate_replacement"
            persistence["template_delta_projected_norm_fraction"] = persistence.pop("projected_norm_fraction")
            persistence["edit_measurement"] = "intervention_record replacement_trace; template delta is not applied"
            persistence["decode_target"] = ("frozen final donor prompt coordinates" if cfg.shared_replacement == "frozen"
                                            else "donor conditioned on same source-generated token history")
        if cfg.persistent_rank and not cfg.template_contrast and not cfg.coordinate_swap:
            for name in ("source", "target"):
                persistence[name]["tokens"] = [
                    [tokenizer.decode([token]) for token in ids]
                    for ids in persistence[name]["token_ids"]
                ]
        target_coordinates = {layer: template_targets[layer] @ (delta / delta.norm())
                              for layer, delta in fixed_deltas.items()} if cfg.template_clamp else None
        if cfg.future_clamp:
            for layer in intervention_layers:
                calibration = future_clamp_calibration[layer]
                assert calibration["donor_above_source"], f"future clamp L{layer}: donor={calibration['donor']} <= source={calibration['source']}"
            fixed_deltas = {layer: future_clamp_axes[layer] for layer in intervention_layers}
            target_coordinates = {layer: future_clamp_calibration[layer]["threshold"] for layer in intervention_layers}
            persistence["clamp_calibration"] = future_clamp_calibration
        hooks = intervention_hooks(
            source_basis,
            target_basis,
            target["residuals"],
            operation="shared_replace" if cfg.shared_replacement != "none" else ("coordinate_clamp" if cfg.template_clamp or cfg.future_clamp else ("coordinate_swap" if cfg.coordinate_swap else ("fixed_delta" if cfg.persistent_rank or cfg.template_contrast else "replace"))),
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
        if cfg.shared_replacement in ("synchronized", "full_synchronized"):
            generation, generation_logits = generate_synchronized_donor(
                model, tokenizer, source, target, shared, intervention_layers[0], cfg.strength,
                positions, intervention_record, captured, max_new_tokens,
            )
        else:
            generation, generation_logits = generate_with_first_logits(
                model, tokenizer, source["input_ids"], blocks, hooks, captured, max_new_tokens
            )
        changed_residuals = captured[0]
        if cfg.shared_replacement == "full_synchronized" and intervention_layers == (32,) and cfg.strength == 1:
            assert generation["token_ids"] == donor_generation["token_ids"], "full final-layer control differs from clean donor generation"
        if cfg.template_state_span != "none":
            span_readouts = {}
            layer = intervention_layers[0]
            if cfg.transport_readout:
                assert prompt_mode == "chat-assistant-prefill"
                transport, transport_diagnostics = fit_span_transport(
                    model, tokenizer, shared, layer, lens_corpus_arrow, extraction_instruction, output_dir,
                )
                persistence["transport_diagnostics"] = transport_diagnostics
            for name, states in (("base", source["residuals"]), ("donor", target["residuals"]),
                                 ("intervened", changed_residuals), ("last_decode", captured[-1])):
                h = states[layer, -1].float()
                h = h * torch.rsqrt(h.square().mean() + 1e-6)
                decoded = transport @ (h @ shared) if cfg.transport_readout else component(h, shared)
                scores = (decoded * norm_gain.float()) @ unembedding.float().T
                values, ids = scores.topk(cfg.rank)
                span_readouts[name] = {"tokens": [tokenizer.decode([i]) for i in ids.tolist()],
                                       "scores": values.tolist()}
            persistence["span_readout"] = {"method": "RMS-scaled fitted-span coordinates, optionally transported by mean-J to L31, then gain-weighted unembedding; not probabilities",
                                           "transported_to_layer31": cfg.transport_readout,
                                           "layer": layer, **span_readouts}
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
        if cfg.template_clamp or cfg.future_clamp:
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
            "attention_mask_policy": "all ones: prompts are unpadded",
            "prefill_instruction": prefill_instruction,
            "extraction_instruction": extraction_instruction,
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
            "readout_status": "computed; semantic validity not established",
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
        if cfg.detector_layers[1] == cfg.detector_layers[2]:
            row["readout_status"] = "unavailable: peak_layer equals output_layer (all fall scores are zero)"
            row["readout_overlap"] = None
            for field in ("base_readout", "target_readout", "readout", "last_decode_readout"):
                row[field] = []
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
        "selector_audit": "selector_audit.md" if selector_audit else None,
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
    if selector_audit:
        with (output_dir / "run.md").open("a") as report:
            report.write("\n[Clean selector diagnostic](selector_audit.md).\n")
    logger.info("wrote {}", output_dir / "run.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--sweep",
        choices=(
            "selector-clean",
            "demo", "chat-strength", "oat", "normalization-strength", "lexical-surface",
            "coordinate-swap",
            "coordinate-layer",
            "coordinate-layer-strong",
            "coordinate-band",
            "template-contrast",
            "template-projection",
            "template-detector",
            "template-selector",
            "template-state",
            "template-attenuation",
            "synchronized-attenuation",
            "attenuation-coverage",
            "attenuation-local",
            "attenuation-rank",
            "attenuation-complement",
            "attenuation-isolation",
            "attenuation-rank-expanded",
            "attenuation-scale",
            "attenuation-bee-correction",
            "attenuation-bee-selector",
            "shared-replacement",
            "synchronized-replacement",
            "synchronized-support",
            "synchronized-dose",
            "bee-correction-controls",
            "bee-correction-alone",
            "bee-correction-projected",
            "template-transport",
            "template-clamp",
            "template-scope",
            "template-band-strength",
            "template-band-clamp",
            "future-coordinate",
            "future-gated",
            "future-clamp",
            "future-template",
            "future-union",
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
    parser.add_argument("--prefill-instruction", default=PREFILL_INSTRUCTION)
    parser.add_argument("--extraction-instruction")
    parser.add_argument("--selector-audit", action="store_true")
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
        args.prefill_instruction,
        args.extraction_instruction,
        args.selector_audit,
    )
