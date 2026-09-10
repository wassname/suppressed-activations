# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Clean trajectory bank for cross-token suppression analysis.

Saves, per prompt (source spider, donors dog/ant, same-form neutral control): full clean
residuals, per-position token labels, norm gain, per-position detector scores and bases at the
detector layers, and the clean first-answer log-probs. No intervention, no generation beyond the
clean answers. Lets all cross-token agreement analysis (pairwise cosines, norms, nulls,
peak-vs-early) run GPU-free and repeatably. Written by PI[claude].
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
    suppressed_activation_scores,
    suppressed_activation_subspace,
)

MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REAL_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
REVISION = os.environ.get("SUPPRESSED_REVISION") or (
    REAL_REVISION if MODEL == "Qwen/Qwen3.5-4B" else None
)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
EARLY_LAYER = int(os.environ.get("SUPPRESSED_EARLY_LAYER", "23"))
PEAK_LAYER = int(os.environ.get("SUPPRESSED_PEAK_LAYER", "25"))
OUTPUT_LAYER = int(os.environ.get("SUPPRESSED_OUTPUT_LAYER", "32"))
RANK = int(os.environ.get("SUPPRESSED_RANK", "8"))

PROMPTS = {
    "source": "Fact: The number of legs on the animal that spins webs is ",
    "dog": "Fact: The number of legs on the animal that barks and is called man's best friend is ",
    "ant": "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ",
    "control": "Fact: The number of legs on the animal that lives in the ocean is ",
}
ANSWER_TOKENS = {"source": "8", "dog": "4", "ant": "6"}
NAMED_WORDS = (" spider", " dog", " ant", " webs", " animal", " legs")


def one_token(tokenizer, text: str) -> int:
    ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(ids) != 1:
        raise ValueError(f"{text!r} is {len(ids)} tokens: {ids}")
    return ids[0]


def main(output_dir: Path) -> None:
    torch.set_grad_enabled(False)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = (1.0 + final_norm.weight).float().cpu()

    from scripts import demo as demo_mod

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "model": MODEL, "revision": REVISION, "detector_layers": [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER],
        "rank": RANK, "prompts": PROMPTS, "answer_tokens": ANSWER_TOKENS,
        "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                       check=True, text=True, capture_output=True).stdout.strip(),
        "entries": {},
    }
    for name, prompt in PROMPTS.items():
        ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
        residuals, logits = demo_mod.trajectory(model, ids, final_norm)
        seq_len = int(residuals.shape[1])
        logp = logits.log_softmax(-1)
        entry: dict = {
            "token_labels": [tokenizer.decode([int(t)]) for t in ids[0]],
            "seq_len": seq_len,
            "answer_logprobs": {a: float(logp[one_token(tokenizer, a)])
                                for a in {ANSWER_TOKENS["source"], *ANSWER_TOKENS.values()}},
            "named_token_ids": {w: one_token(tokenizer, w) for w in NAMED_WORDS},
        }
        torch.save(residuals.cpu(), output_dir / f"{name}_residuals.pt")
        # Detector scores and per-position bases, saved once (they do not depend on the
        # measurement layer). Components at EARLY/PEAK/OUTPUT are recomputed GPU-free from the
        # saved full residuals and this basis.
        scores = suppressed_activation_scores(
            residuals.permute(1, 0, 2), unembedding, 1.0 + final_norm.weight,
            early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
            normalize_unembedding_rows=True,
        ).float().cpu()
        top_scores, top_ids = scores.topk(64, dim=-1)
        named = {w: scores[:, one_token(tokenizer, w)].clone() for w in NAMED_WORDS}  # clone: views would drag the full vocab storage into the file
        basis, ids_sel = suppressed_activation_subspace(
            residuals.permute(1, 0, 2), unembedding, 1.0 + final_norm.weight,
            early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER, output_layer=OUTPUT_LAYER,
            rank=RANK, normalize_unembedding_rows=True,
        )
        torch.save({"scores_top64_values": top_scores, "scores_top64_ids": top_ids,
                    "named_scores": {w: v for w, v in named.items()},
                    "basis": basis.float().cpu(), "selected_ids": ids_sel.cpu()},
                   output_dir / f"{name}_detector.pt")
        # Mirrored-selector control (kill-or-rescue check): same construction with the
        # trajectory criterion inverted -- tokens that FALL early-to-peak then RISE peak-to-
        # output (rise<0 AND fall<0). Swapping layer roles would reproduce the identical
        # detector (the min-of-clamped form is symmetric), so the mirror is computed from the
        # signed rise/fall directly. If mirrored bases show the same peak-layer agreement,
        # agreement is mid-layer geometry, not the suppression detector.
        h3 = residuals[:, [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER]].float()
        h_norm = h3 * torch.rsqrt(h3.square().mean(-1, keepdim=True) + 1e-6)
        h_norm = h_norm * (1.0 + final_norm.weight).float()
        logits3 = h_norm @ unembedding.float().T
        rise = logits3[:, 1] - logits3[:, 0]
        fall = logits3[:, 1] - logits3[:, 2]
        rise = rise - rise.mean(-1, keepdim=True)
        fall = fall - fall.mean(-1, keepdim=True)
        mirrored_scores = (-torch.maximum(rise, fall)).clamp_min(0).float().cpu()
        m_top_values, m_top_ids = mirrored_scores.topk(64, dim=-1)
        from suppressed_activation_subspace import subspace_from_scores
        mirrored_basis, mirrored_ids = subspace_from_scores(
            mirrored_scores, unembedding, (1.0 + final_norm.weight).cpu(),
            rank=RANK, normalize_unembedding_rows=True,
        )
        torch.save({"top_values": m_top_values, "top_ids": m_top_ids,
                    "basis": mirrored_basis.float().cpu(), "selected_ids": mirrored_ids.cpu()},
                   output_dir / f"{name}_mirrored_detector.pt")
        # PCA of the residuals at each detector layer, for covariance-matched random nulls.
        # With only T token positions the covariance has rank at most T-1 after centering, so
        # we save exactly that many directions and record the rank; nulls built from these are
        # sensitivity checks against a rank-limited estimate, not a calibrated covariance.
        for layer in (EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER):
            centred = residuals[layer].float().cpu()
            centred = centred - centred.mean(0, keepdim=True)
            n_comp = min(centred.shape[0] - 1, 256)
            u, s, _ = torch.linalg.svd(centred.T, full_matrices=False)
            torch.save({"directions": u[:, :n_comp],
                        "values": s[:n_comp].square() / centred.shape[0],
                        "sample_positions": int(centred.shape[0]), "rank": int(n_comp)},
                       output_dir / f"{name}_pca_L{layer}.pt")
        manifest["entries"][name] = entry
        print(f"banked {name}: {seq_len} tokens, answers {entry['answer_logprobs']}")

    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    # Unembedding rows (centered, gain-weighted -- the exact form subspace_from_scores uses)
    # for the union of every prompt's selected ids plus the a-priori named tokens. Lets the
    # analysis rebuild any selection GPU-free: named-token bases (zero selection bias) and
    # held-out cross-prompt selection (the winner's-curse control).
    union_ids = set()
    for name in PROMPTS:
        det = torch.load(output_dir / f"{name}_detector.pt", weights_only=False)
        mir = torch.load(output_dir / f"{name}_mirrored_detector.pt", weights_only=False)
        union_ids.update(int(i) for i in det["scores_top64_ids"].flatten())
        union_ids.update(int(i) for i in mir["top_ids"].flatten())
    union_ids.update(int(v) for v in manifest["entries"]["source"]["named_token_ids"].values())
    union_ids = sorted(union_ids)
    dirs = unembedding[union_ids].float().cpu()
    dirs = dirs - dirs.mean(0, keepdim=True)
    dirs = dirs * (1.0 + final_norm.weight).float().cpu()
    # bf16 halves the file; the analysis casts to float32 before any SVD.
    torch.save({"ids": union_ids, "rows": dirs.to(torch.bfloat16)},
               output_dir / "selected_unembedding_rows.pt")
    print(f"bank: {output_dir} ({len(union_ids)} union unembedding rows saved)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    main(parser.parse_args().output_dir)
