# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Cross-token signed-cosine agreement of suppressed activation components.

`token_persistent_subspace` picks eigenvectors of the *average projector* (sign-invariant span
overlap). This script instead measures whether the actual projected residual components
c_p = component(residual_p, B_p) agree in sign across token positions, then compares a
`replace` edit chosen by the signed-agreement direction vs the avg-projector span, against a
matched-random control. Semantic success is judged from the full continuation: a changed
digit with unchanged identity is NOT a transfer.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
import transformers  # noqa: F401  (transitive via demo import below)

from suppressed_activation_subspace import (
    component,
    cross_position_covariance,
    suppressed_activation_subspace,
    token_persistent_subspace,
)

# Real-model defaults; overridable by SUPPRESSED_* env for the tiny CPU smoke model.
MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REVISION = os.environ.get("SUPPRESSED_REVISION", None)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
EARLY_LAYER = int(os.environ.get("SUPPRESSED_EARLY_LAYER", "23"))
PEAK_LAYER = int(os.environ.get("SUPPRESSED_PEAK_LAYER", "25"))
OUTPUT_LAYER = int(os.environ.get("SUPPRESSED_OUTPUT_LAYER", "32"))
INTERVENTION_LAYER = int(os.environ.get("SUPPRESSED_INTERVENTION_LAYER", "23"))
RANK = int(os.environ.get("SUPPRESSED_RANK", "8"))
STRENGTH = float(os.environ.get("SUPPRESSED_STRENGTH", "2.0"))
READOUT_POSITIONS = int(os.environ.get("SUPPRESSED_READOUT_POSITIONS", "3"))
POSITIONS = int(os.environ.get("SUPPRESSED_INTERVENTION_POSITIONS", "3"))
MAX_NEW_TOKENS = int(os.environ.get("SUPPRESSED_TOKENS", "32"))

SOURCE_PROMPT = os.environ.get(
    "SUPPRESSED_SOURCE_PROMPT",
    "Fact: The number of legs on the animal that spins webs is ",
)
SOURCE_OUTPUT = os.environ.get("SUPPRESSED_SOURCE_OUTPUT", "8")
TARGET_OUTPUT = os.environ.get("SUPPRESSED_TARGET_OUTPUT", "4")


def one_token(tokenizer, text: str) -> int:
    ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(ids) != 1:
        raise ValueError(f"{text!r} is {len(ids)} tokens: {ids}")
    return ids[0]


def main(output_path: Path, target_prompt: str, target_concept: str, target_output: str,
         control_prompt: str | None = None) -> None:
    torch.set_grad_enabled(False)
    tokenizer = __import__("transformers").AutoTokenizer.from_pretrained(MODEL)
    model = __import__("transformers").AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    blocks = model.model.layers
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight

    # Reuse the verified, calibrated intervention hooks from the demonstration script.
    from scripts import demo as demo_mod

    trajectory = demo_mod.trajectory
    run_forward = demo_mod.run_forward
    generate = demo_mod.generate
    intervention_hooks = demo_mod.intervention_hooks

    source_ids = tokenizer(SOURCE_PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
    target_ids = tokenizer(target_prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
    source_residuals, source_logits = trajectory(model, source_ids, final_norm)
    target_residuals, target_logits = trajectory(model, target_ids, final_norm)

    source_id = one_token(tokenizer, SOURCE_OUTPUT)
    target_id = one_token(tokenizer, target_output)
    source_p = float(source_logits.softmax(-1)[source_id])
    target_p_base = float(source_logits.softmax(-1)[target_id])

    # Per-position suppressed subspaces and actual projected components at the intervention layer.
    window = slice(max(0, source_residuals.shape[1] - READOUT_POSITIONS), source_residuals.shape[1])
    positions_list = list(range(window.start, window.stop))

    # Cross-prompt baseline: a same-form neutral prompt tests whether within-prompt agreement is
    # concept-specific or a shared mean / syntax edge.
    control_components = None
    if control_prompt is not None:
        control_ids = tokenizer(control_prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
        control_residuals, _ = trajectory(model, control_ids, final_norm)
        control_bases, _ = suppressed_activation_subspace(
            control_residuals[:, window].permute(1, 0, 2), unembedding, norm_gain,
            early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
            normalize_unembedding_rows=True,
        )
        control_components = torch.stack([
            component(control_residuals[INTERVENTION_LAYER, p].float(), control_bases[i])
            for i, p in enumerate(positions_list)
        ])

    # source_bases / target_bases: [positions, hidden, rank]; ids: [positions, rank].
    source_bases, source_ids_sel = suppressed_activation_subspace(
        source_residuals[:, window].permute(1, 0, 2), unembedding, norm_gain,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
        normalize_unembedding_rows=True,
    )
    target_bases, target_ids_sel = suppressed_activation_subspace(
        target_residuals[:, window].permute(1, 0, 2), unembedding, norm_gain,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
        normalize_unembedding_rows=True,
    )
    source_components = torch.stack([
        component(source_residuals[INTERVENTION_LAYER, p].float(), source_bases[i])
        for i, p in enumerate(positions_list)
    ])
    target_components = torch.stack([
        component(target_residuals[INTERVENTION_LAYER, p].float(), target_bases[i])
        for i, p in enumerate(positions_list)
    ])

    def _mean_signed_cosine(components: Tensor) -> float | None:
        if components.shape[0] < 2:
            return None
        norms = components.norm(dim=-1).clamp_min(1e-12)
        normalized = components / norms.unsqueeze(-1)
        cosines = (normalized @ normalized.T).fill_diagonal_(0.0)
        n_pairs = components.shape[0] * (components.shape[0] - 1)
        return float(cosines.sum() / n_pairs)

    def signed_agreement_summary(components: Tensor) -> dict:
        """components: [T, hidden]. Signed agreement of actual projected suppressed components.

        `component` is the projector h @ (B B^T), sign-invariant to basis flips, so these
        cosines are not corrupted by QR sign ambiguity. Mean-subtracted and drop-max-norm
        variants test the shared-mean / sink artifact: a high raw cosine on a shared mean is
        not concept evidence.
        """
        mean_dir = components.mean(dim=0)
        mean_component_norm = components.norm(dim=-1).mean()
        centered = components - mean_dir
        cent = _mean_signed_cosine(centered)
        drop = None
        if components.shape[0] > 2:
            keep = components.norm(dim=-1).argmax()
            keep_mask = torch.ones(components.shape[0], dtype=torch.bool)
            keep_mask[keep] = False
            drop = _mean_signed_cosine(components[keep_mask])
        cpc = cross_position_covariance(components[None])
        return {
            "signed_agreement_norm_mean_over_mean_norm": float(mean_dir.norm() / mean_component_norm),
            "mean_signed_cosine": _mean_signed_cosine(components),
            "mean_centered_signed_cosine": cent,
            "drop_max_norm_signed_cosine": drop,
            "mean_component_norm": float(mean_component_norm),
            "mean_agreement_vector_norm": float(mean_dir.norm()),
            "cross_position_covariance_mean_diagonal": float(cpc.diagonal().mean()),
            "mean_norm_is_zero": bool(mean_dir.norm() < 1e-8),
        }

    def subspace_overlap_summary(bases: Tensor) -> dict:
        """bases: [T, hidden, rank]. Sign-invariant span-overlap (the existing avg-projector view)."""
        vectors, singular_values, _ = torch.linalg.svd(bases.permute(1, 0, 2).flatten(1), full_matrices=False)
        spectrum = (singular_values.square() / bases.shape[0]).tolist()
        principal = []
        for i in range(bases.shape[0] - 1):
            q1 = torch.linalg.qr(bases[i], mode="reduced").Q
            q2 = torch.linalg.qr(bases[i + 1], mode="reduced").Q
            s = torch.linalg.svdvals(q1.T @ q2)
            principal.append(s.tolist())
        return {
            "avg_projector_spectrum": spectrum,
            "principal_angle_cosines_between_consecutive": principal,
            "top_avg_projector_value": float(spectrum[0]),
        }

    # Rank-1 behavioral basis selectors (shape [hidden, 1] for component()).
    signed_dir = source_components.mean(dim=0)
    signed_dir = signed_dir / signed_dir.norm()
    signed_basis = signed_dir.reshape(-1, 1)
    support, persistence, _ = token_persistent_subspace(
        source_residuals[:, window].permute(1, 0, 2), unembedding, norm_gain,
        persistent_rank=1,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
        rank=RANK, normalize_unembedding_rows=True,
    )
    # support: [hidden, 1]; make it an explicit rank-1 basis vector.
    avg_basis = support / support.norm()
    generator = torch.Generator(device=DEVICE).manual_seed(0)
    random_dir = torch.randn(avg_basis.shape, device=DEVICE, generator=generator)
    random_dir = torch.linalg.qr(random_dir, mode="reduced").Q

    blocks_to_hook = [INTERVENTION_LAYER - 1]
    target_position = target_residuals.shape[1] - 1

    def run_selector(basis, *, generate_too: bool):
        hooks = intervention_hooks(
            basis, basis, target_residuals, operation="replace", strength=STRENGTH,
            blocks_to_hook=blocks_to_hook, target_position=target_position,
            match_component_norm=True, restore_norm=True,
        )
        logits = run_forward(model, source_ids, blocks, hooks)
        generation = None
        if generate_too:
            generation = generate(model, tokenizer, source_ids, blocks, hooks,
                                  max_new_tokens=MAX_NEW_TOKENS)
        return logits, generation

    rows = []
    for selector, basis in (("signed_agreement", signed_basis),
                            ("avg_projector", avg_basis),
                            ("matched_random", random_dir)):
        logits, generation = run_selector(basis, generate_too=(selector != "matched_random"))
        rows.append({"selector": selector, "logits": logits, "generation": generation})

    # Unembedding probe: does applying each direction (RMSNorm + gain-weighted unembedding) raise
    # the target concept token logit? If none does, no scaling of that edit writes the target.
    def logit_probe(direction: Tensor) -> dict:
        d = direction.float().flatten()
        d_norm = d * torch.rsqrt(d.square().mean() + 1e-6) * norm_gain.float()
        vals = d_norm @ unembedding.float().T
        return {
            "source_token_logit": {t: float(vals[one_token(tokenizer, t)])
                                   for t in (" spider", SOURCE_OUTPUT)},
            "target_token_logit": {t: float(vals[one_token(tokenizer, t)])
                                   for t in (" " + target_concept, target_output)},
        }

    logit_probes = {
        "signed_agreement": logit_probe(signed_basis),
        "avg_projector": logit_probe(avg_basis),
        "matched_random": logit_probe(random_dir),
    }

    def summarize(logits):
        logp = logits.log_softmax(-1)
        return {
            "p_source": float(logp[source_id].exp()),
            "p_target": float(logp[target_id].exp()),
            "log_odds_target_vs_source": float(logp[target_id] - logp[source_id]),
            "top_tokens": [
                {"token_id": int(i), "token": tokenizer.decode([int(i)]), "logp": float(logp[i])}
                for i in logp.topk(10).indices
            ],
        }

    result = {
        "metadata": {
            "model": MODEL, "revision": REVISION, "device": DEVICE,
            "detector_layers": [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER],
            "intervention_layer": INTERVENTION_LAYER, "rank": RANK, "strength": STRENGTH,
            "readout_positions": READOUT_POSITIONS, "positions": POSITIONS,
            "max_new_tokens": MAX_NEW_TOKENS,
            "source_prompt": SOURCE_PROMPT, "target_prompt": target_prompt,
            "target_concept": target_concept, "source_output": SOURCE_OUTPUT,
            "target_output": target_output,
            "git_describe": subprocess.run(
                ["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True
            ).stdout.strip(),
        },
        "readout": {
            "source_tokens": [{"position": positions_list[i], "token_id": int(t),
                               "token": tokenizer.decode([int(t)])}
                              for i, t in enumerate(source_ids_sel[:, 0])],
            "target_tokens": [{"position": positions_list[i], "token_id": int(t),
                               "token": tokenizer.decode([int(t)])}
                              for i, t in enumerate(target_ids_sel[:, 0])],
        },
        "cross_token": {
            "source": signed_agreement_summary(source_components),
            "donor": signed_agreement_summary(target_components),
        },
        "subspace_overlap": {
            "source": subspace_overlap_summary(source_bases),
            "donor": subspace_overlap_summary(target_bases),
        },
        "component_magnitude": {
            "source_norms": [float(n) for n in source_components.norm(dim=-1)],
            "donor_norms": [float(n) for n in target_components.norm(dim=-1)],
            "source_residual_norms": [float(source_residuals[INTERVENTION_LAYER, p].float().norm())
                                       for p in positions_list],
            "donor_residual_norms": [float(target_residuals[INTERVENTION_LAYER, p].float().norm())
                                     for p in positions_list],
            "source_norm_fraction": [float(n / r.clamp_min(1e-12))
                                      for n, r in zip(source_components.norm(dim=-1),
                                                      [source_residuals[INTERVENTION_LAYER, p].float().norm() for p in positions_list])],
            "donor_norm_fraction": [float(n / r.clamp_min(1e-12))
                                     for n, r in zip(target_components.norm(dim=-1),
                                                     [target_residuals[INTERVENTION_LAYER, p].float().norm() for p in positions_list])],
        },
        "unembedding_logit_probe": logit_probes,
        "cross_prompt_baseline": (
            {
                "control_prompt": control_prompt,
                # Generic-syntax / shared-mean baseline (GLM Q2, Kimi Q2): mean cosine of each
                # source component with each same-form control component. If it rivals the
                # within-prompt mean signed cosine, agreement is a shared mean / syntax edge,
                # not a concept-specific reusable component.
                "mean_cross_prompt_cosine": None,
                "source_absolute_cross_prompt_cosine": None,
            }
            if control_components is not None else None
        ),
        "base": {"p_source": source_p, "p_target": target_p_base},
        "rows": [
            {"selector": row["selector"], "metrics": summarize(row["logits"]),
             "generation": row["generation"]}
            for row in rows
        ],
    }
    if control_components is not None:
        source_normed = source_components / source_components.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        control_normed = control_components / control_components.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        result["cross_prompt_baseline"]["mean_cross_prompt_cosine"] = float((source_normed @ control_normed.T).mean())
        result["cross_prompt_baseline"]["source_absolute_cross_prompt_cosine"] = float((source_normed @ control_normed.T).abs().mean())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "cross_token_source_mean_signed_cosine": result["cross_token"]["source"]["mean_signed_cosine"],
        "cross_token_source_agreement": result["cross_token"]["source"]["signed_agreement_norm_mean_over_mean_norm"],
        "avg_projector_top_source": result["subspace_overlap"]["source"]["top_avg_projector_value"],
        "rows": [{"selector": r["selector"], "p_source": r["metrics"]["p_source"],
                  "p_target": r["metrics"]["p_target"],
                  "log_odds_target_vs_source": r["metrics"]["log_odds_target_vs_source"],
                  "generation": (r["generation"] or {}).get("text", "")[:120]}
                 for r in result["rows"]],
    }, indent=2))
    print(f"\noutput: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-prompt", required=True)
    parser.add_argument("--target-concept", required=True)
    parser.add_argument("--target-output", required=True)
    parser.add_argument("--control-prompt", default=None,
                        help="same-form neutral prompt for a generic-syntax / shared-mean baseline")
    args = parser.parse_args()
    main(args.output, args.target_prompt, args.target_concept, args.target_output, args.control_prompt)
