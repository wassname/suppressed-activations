# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Cross-token signed-cosine agreement of suppressed activation components.

`token_persistent_subspace` picks eigenvectors of the *average projector* (sign-invariant span
overlap). This script instead measures whether the actual projected residual components
c_p = component(residual_p, B_p) agree in sign across token positions, then compares a
shared-coordinate replacement chosen by the signed-agreement direction vs the avg-projector
span, against a perturbation-norm-matched random control. Semantic success is judged from the
full continuation: a changed digit with unchanged identity is NOT a transfer.
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
from torch import Tensor

from suppressed_activation_subspace import (
    component,
    cross_position_covariance,
    suppressed_activation_subspace,
    token_persistent_subspace,
)

# Real-model defaults; overridable by SUPPRESSED_* env for the tiny CPU smoke model.
MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REAL_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
REVISION = os.environ.get("SUPPRESSED_REVISION") or (
    REAL_REVISION if MODEL == "Qwen/Qwen3.5-4B" else None
)
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
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    blocks = model.model.layers
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight

    # Reuse the verified trajectory/generate from the demonstration script.
    from scripts import demo as demo_mod

    trajectory = demo_mod.trajectory
    generate = demo_mod.generate

    source_ids = tokenizer(SOURCE_PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
    target_ids = tokenizer(target_prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
    source_residuals, source_logits = trajectory(model, source_ids, final_norm)
    target_residuals, target_logits = trajectory(model, target_ids, final_norm)

    source_id = one_token(tokenizer, SOURCE_OUTPUT)
    target_id = one_token(tokenizer, target_output)
    base_logp = source_logits.log_softmax(-1)
    source_p = float(base_logp.exp()[source_id])
    target_p_base = float(base_logp.exp()[target_id])

    # Each prompt gets its own end-aligned window; prompts of different length must not share
    # absolute positions.
    def extract(residuals: Tensor) -> dict:
        end = residuals.shape[1]
        window = slice(max(0, end - READOUT_POSITIONS), end)
        positions = list(range(window.start, window.stop))
        bases, ids_sel = suppressed_activation_subspace(
            residuals[:, window].permute(1, 0, 2), unembedding, norm_gain,
            early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER, rank=RANK,
            normalize_unembedding_rows=True,
        )
        components = torch.stack([
            component(residuals[INTERVENTION_LAYER, p].float(), bases[i])
            for i, p in enumerate(positions)
        ])
        return {
            "window": [window.start, window.stop], "positions": positions,
            "bases": bases, "ids_sel": ids_sel, "components": components,
        }

    source_ex = extract(source_residuals)
    target_ex = extract(target_residuals)
    positions_list = source_ex["positions"]

    # Cross-prompt baseline: a same-form neutral prompt tests whether within-prompt agreement is
    # concept-specific or a shared mean / syntax edge.
    control_ex = None
    if control_prompt is not None:
        control_ids = tokenizer(control_prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
        control_residuals, _ = trajectory(model, control_ids, final_norm)
        control_ex = extract(control_residuals)

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
        cent = _mean_signed_cosine(components - mean_dir)
        drop = None
        if components.shape[0] > 2:
            keep_mask = torch.ones(components.shape[0], dtype=torch.bool)
            keep_mask[components.norm(dim=-1).argmax()] = False
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
            principal.append(torch.linalg.svdvals(q1.T @ q2).tolist())
        return {
            "avg_projector_spectrum": spectrum,
            "principal_angle_cosines_between_consecutive": principal,
            "top_avg_projector_value": float(spectrum[0]),
        }

    # Rank-1 behavioral basis selectors (shape [hidden, 1] for component()).
    signed_dir = source_ex["components"].mean(dim=0)
    signed_dir = signed_dir / signed_dir.norm()
    signed_basis = signed_dir.reshape(-1, 1)
    support, _, _ = token_persistent_subspace(
        source_residuals[:, slice(*source_ex["window"])].permute(1, 0, 2), unembedding, norm_gain,
        persistent_rank=1,
        early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
        rank=RANK, normalize_unembedding_rows=True,
    )
    avg_basis = support / support.norm()
    generator = torch.Generator(device=DEVICE).manual_seed(0)
    random_dir = torch.linalg.qr(
        torch.randn(avg_basis.shape, device=DEVICE, generator=generator), mode="reduced"
    ).Q

    residual_layer = INTERVENTION_LAYER
    target_position = target_residuals.shape[1] - 1

    # Shared-coordinate replacement WITHOUT component-norm matching: with one shared rank-1
    # basis, norm matching rescales the donor onto the source's own magnitude, which makes
    # equal-sign edits a no-op and opposite-sign edits a reflection -- exactly the distinction
    # under test. Donor magnitude is therefore kept, and perturbation/residual norms are logged
    # per call so norm growth is visible rather than hidden.
    def edit_hook(basis: Tensor, *, record: dict | None = None, matched_norms: dict | None = None,
                  strength: float = STRENGTH):
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            active = 1 if hidden.shape[1] == 1 else POSITIONS
            start = hidden.shape[1] - active
            h = hidden[:, start:].float()
            target_h = target_residuals[residual_layer, target_position].reshape(1, 1, -1).expand(h.shape).float()
            delta = component(target_h, basis) - component(h, basis)
            if matched_norms is not None:
                # kind-aware matching: prefill matches per-position semantic norms; each decode
                # call matches the semantic edit's mean decode-call norm.
                if hidden.shape[1] > 1:
                    ref = torch.as_tensor(matched_norms["prefill"][:active],
                                          device=h.device).float()
                else:
                    ref = torch.full((1,), matched_norms["decode_mean"], device=h.device)
                scale = ref / delta.norm(dim=-1).clamp_min(1e-12)
                delta = delta * scale.unsqueeze(-1)
                # the reference norms are post-strength semantic perturbations; applying strength
                # again would square it, so the matched control adds the scaled delta directly.
                patched = h + delta
            else:
                patched = h + strength * delta
            if record is not None:
                record.setdefault("calls", []).append({
                    "seq_len": int(hidden.shape[1]), "active": active,
                    "positions": list(range(start, hidden.shape[1])),
                    "perturbation_norm_by_position": (patched - h).norm(dim=-1)[0].tolist(),
                    "residual_norm_by_position_before": h.norm(dim=-1)[0].tolist(),
                    "residual_norm_by_position_after": patched.norm(dim=-1)[0].tolist(),
                })
            full = torch.cat([hidden[:, :start], patched.to(hidden.dtype),
                              hidden[:, start + active:]], dim=1)
            return (full, *output[1:]) if isinstance(output, tuple) else full
        return {residual_layer - 1: hook}

    def run_selector(name: str, basis: Tensor, *, generate_too: bool, strength: float = STRENGTH,
                     matched_norms: dict | None = None):
        record: dict = {}
        hooks = edit_hook(basis, record=record, matched_norms=matched_norms, strength=strength)
        logits = demo_mod.run_forward(model, source_ids, blocks, hooks)
        generation = None
        if generate_too:
            generation = generate(model, tokenizer, source_ids, blocks, hooks,
                                  max_new_tokens=MAX_NEW_TOKENS)
            record["generation_token_ids"] = generation["token_ids"]
        if strength == 0:
            torch.testing.assert_close(logits, source_logits.float(), rtol=0, atol=0)
            record["zero_strength_identity"] = "logits identical to base"
        if generate_too:
            prefill = [c for c in record["calls"] if c["seq_len"] > 1]
            decode = [c for c in record["calls"] if c["seq_len"] == 1]
            assert prefill and prefill[0]["active"] == POSITIONS, f"{name}: prefill coverage {prefill}"
            assert len(decode) >= len(generation["token_ids"]) - 1, f"{name}: decode coverage short"
            record["coverage"] = {
                "prefill_positions": prefill[0]["positions"],
                "decode_calls": len(decode),
                "generated_tokens": len(generation["token_ids"]),
            }
        record["strength"] = strength
        record["matched_to"] = "semantic avg_projector per-position norms" if matched_norms else None
        return logits, generation, record

    # Semantic edits first; their per-position perturbation norms calibrate the random control.
    semantic_norms = None
    rows = []
    for name, basis, gen in (("signed_agreement", signed_basis, True),
                             ("avg_projector", avg_basis, True)):
        logits, generation, record = run_selector(name, basis, generate_too=gen)
        if name == "avg_projector":
            prefill_calls = [c for c in record["calls"] if c["seq_len"] > 1]
            decode_calls = [c for c in record["calls"] if c["seq_len"] == 1]
            semantic_norms = {
                "prefill": prefill_calls[0]["perturbation_norm_by_position"],
                "decode_mean": (sum(c["perturbation_norm_by_position"][0] for c in decode_calls)
                                / max(len(decode_calls), 1)),
            }
        rows.append({"selector": name, "logits": logits, "generation": generation, "record": record})
    logits_r, generation_r, record_r = run_selector(
        "matched_random", random_dir, generate_too=True, matched_norms=semantic_norms)
    rows.append({"selector": "matched_random", "logits": logits_r,
                 "generation": generation_r, "record": record_r})
    # zero-strength identity check
    _, _, record_zero = run_selector("zero_strength", avg_basis, generate_too=False, strength=0.0)

    # Unembedding probe: does applying each direction (RMSNorm + gain-weighted unembedding)
    # raise the target concept token logit? A linear readout diagnostic, not a causal claim.
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

    logit_probes = {n: logit_probe(b) for n, b in
                    (("signed_agreement", signed_basis), ("avg_projector", avg_basis),
                     ("matched_random", random_dir))}

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

    def ex_summary(ex, residuals):
        return {
            "window": ex["window"], "positions": ex["positions"],
            "selected_tokens": [{"position": ex["positions"][i], "token_id": int(t),
                                 "token": tokenizer.decode([int(t)])}
                                for i, t in enumerate(ex["ids_sel"][:, 0])],
            "signed_agreement": signed_agreement_summary(ex["components"]),
            "subspace_overlap": subspace_overlap_summary(ex["bases"]),
            "component_norms": [float(n) for n in ex["components"].norm(dim=-1)],
            "component_norm_fraction": [
                float(n / r) for n, r in zip(
                    ex["components"].norm(dim=-1),
                    [residuals[INTERVENTION_LAYER, p].float().norm() for p in ex["positions"]])],
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
            "target_output": target_output, "control_prompt": control_prompt,
            "replacement": "shared-coordinate, no component-norm matching, no residual-norm restore",
            "random_control": "rank-1 random basis, perturbation norms matched to avg_projector prefill per position",
            "git_describe": subprocess.run(
                ["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True
            ).stdout.strip(),
        },
        "per_prompt": {
            "source": ex_summary(source_ex, source_residuals),
            "donor": ex_summary(target_ex, target_residuals),
            **({"control": ex_summary(control_ex, control_residuals)} if control_ex else {}),
        },
        "unembedding_logit_probe": logit_probes,
        "base": {"p_source": source_p, "p_target": target_p_base},
        "zero_strength_identity": record_zero.get("zero_strength_identity"),
        "rows": [
            {"selector": r["selector"], "metrics": summarize(r["logits"]),
             "generation": r["generation"],
             "coverage": r["record"].get("coverage"),
             "matched_to": r["record"].get("matched_to"),
             "first_call_perturbation_norm_by_position": r["record"]["calls"][0]["perturbation_norm_by_position"]}
            for r in rows
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "source_mean_signed_cosine": result["per_prompt"]["source"]["signed_agreement"]["mean_signed_cosine"],
        "source_mean_centered_signed_cosine": result["per_prompt"]["source"]["signed_agreement"]["mean_centered_signed_cosine"],
        "donor_mean_signed_cosine": result["per_prompt"]["donor"]["signed_agreement"]["mean_signed_cosine"],
        "avg_projector_top_source": result["per_prompt"]["source"]["subspace_overlap"]["top_avg_projector_value"],
        "zero_strength_identity": result["zero_strength_identity"],
        "rows": [{"selector": r["selector"], "p_source": r["metrics"]["p_source"],
                  "p_target": r["metrics"]["p_target"],
                  "log_odds": r["metrics"]["log_odds_target_vs_source"],
                  "coverage": r["coverage"],
                  "generation": (r["generation"] or {}).get("text", "")[:160]}
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
