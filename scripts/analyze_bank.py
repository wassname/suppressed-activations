# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""GPU-free cross-token agreement analysis over a saved clean trajectory bank.

Implements the statistics and nulls fixed after the first screen's over-reads:
- norm-standardized top singular value of the component matrix, with a basis-respecting null
  (random unit vectors drawn inside each position's own basis);
- position-locked cross-prompt signed cosines (source vs donor/control at the same position),
  with a position-permutation null;
- position-class interaction: concept positions (animal, property, identity) vs syntax
  positions ("is", "Fact") vs the trivial same-surface control ("animal");
- peak-vs-early comparison at EARLY/PEAK/OUTPUT layers;
- mirrored-selector comparison: same agreement statistics from the fall-then-rise control
  bases. Agreement equal for mirrored and detector bases means mid-layer geometry, not the
  suppression detector.

Written by PI[claude]. Runs on CPU from scripts/trajectory_bank.py output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import torch
from torch import Tensor

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from suppressed_activation_subspace import component

PROMPTS = ("source", "dog", "ant", "control")
# position classes by token-label substring; "animal" is the trivial same-surface control
CONCEPT_CLASSES = {"legs": "property", "webs": "identity", "web": "identity",
                   " animal": "same-surface-control"}
SYNTAX_CLASSES = {" is": "syntax", "Fact": "syntax", " number": "syntax", " the": "syntax"}


def position_class(label: str) -> str:
    for key, cls in {**CONCEPT_CLASSES, **SYNTAX_CLASSES}.items():
        if key in label:
            return cls
    return "other"


def load_bank(bank_dir: Path) -> dict:
    bank = {"manifest": json.loads((bank_dir / "manifest.json").read_text())}
    for name in PROMPTS:
        entry = {"residuals": torch.load(bank_dir / f"{name}_residuals.pt", weights_only=False),
                 "detector": torch.load(bank_dir / f"{name}_detector.pt", weights_only=False),
                 "mirrored": torch.load(bank_dir / f"{name}_mirrored_detector.pt", weights_only=False)}
        entry["labels"] = bank["manifest"]["entries"][name]["token_labels"]
        bank[name] = entry
    return bank


def components_at(residuals: Tensor, basis: Tensor, layer: int) -> Tensor:
    """c_p for every position p at measurement `layer` using each position's own basis."""
    n_pos = basis.shape[0]
    return torch.stack([
        component(residuals[layer, p].float(), basis[p]) for p in range(n_pos)
    ])


def pairwise_cosines(components: Tensor) -> Tensor:
    norms = components.norm(dim=-1).clamp_min(1e-12)
    cos = (components / norms.unsqueeze(-1)) @ (components / norms.unsqueeze(-1)).T
    return cos.fill_diagonal_(0.0)


def consensus_ratio(components: Tensor) -> float:
    return float(components.mean(0).norm() / components.norm(dim=-1).mean())


def sigma1_norm_standardized(components: Tensor, basis: Tensor, n_null: int = 2000) -> dict:
    """Top singular value of per-position unit vectors, against a basis-respecting null.

    Null draws a random unit vector inside each position's own basis (respecting each basis's
    spectrum), so rejection means alignment beyond what the bases themselves permit.
    """
    unit = components / components.norm(dim=-1).clamp_min(1e-12).unsqueeze(-1)
    observed = float(torch.linalg.svdvals(unit).squeeze()[0])  # svdvals is descending: [0] is the top
    nulls = torch.empty(n_null)
    k = basis.shape[-1]
    for i in range(n_null):
        draw = torch.stack([
            basis[p] @ torch.randn(k, 1).squeeze(-1) for p in range(basis.shape[0])
        ])
        draw = draw / draw.norm(dim=-1).clamp_min(1e-12).unsqueeze(-1)
        nulls[i] = float(torch.linalg.svdvals(draw).squeeze()[0])
    return {"sigma1_observed": observed, "sigma1_null_mean": float(nulls.mean()),
            "sigma1_null_p95": float(nulls.quantile(0.95)), "sigma1_above_null": bool(observed > float(nulls.quantile(0.95)))}


def position_locked_cross_cosines(bank: dict, layer: int, selector: str = "detector") -> dict:
    """cos(c_p^a, c_p^b) at positions aligned by the shared template (same suffix structure and
    semantic role, labels shown from the source side). Not a same-token-identity criterion:
    donor prompts do not contain the source's tokens. Nulls are rank-limited sensitivity
    checks, not calibrated covariance tests."""
    out = {}
    comps = {name: components_at(bank[name]["residuals"], bank[name][selector]["basis"], layer)
             for name in PROMPTS}
    n = min(c.shape[0] for c in comps.values())
    for a, b in (("source", "dog"), ("source", "ant"), ("source", "control"),
                 ("dog", "ant"), ("dog", "control")):
        ua = comps[a][:n] / comps[a][:n].norm(dim=-1).clamp_min(1e-12).unsqueeze(-1)
        ub = comps[b][:n] / comps[b][:n].norm(dim=-1).clamp_min(1e-12).unsqueeze(-1)
        cos = (ua * ub).sum(-1)
        # permutation null: break position locking, keep each side's marginal structure
        nulls = torch.empty(2000)
        for i in range(2000):
            perm = torch.randperm(n)
            nulls[i] = float((ua * ub[perm]).sum(-1).mean())
        out[f"{a}_vs_{b}"] = {
            "null_kind": "position-permutation sensitivity check (rank-limited), not calibrated covariance",
            "mean_cosine": float(cos.mean()),
            "per_position": [float(c) for c in cos],
            "labels": bank["source"]["labels"][:n],
            "null_mean": float(nulls.mean()), "null_p95": float(nulls.quantile(0.95)),
            "above_null": bool(float(cos.mean()) > float(nulls.quantile(0.95))),
        }
    return out


def main(bank_dir: Path, output_path: Path) -> None:
    bank = load_bank(bank_dir)
    layers = bank["manifest"]["detector_layers"]
    result = {"bank": str(bank_dir), "layers": layers, "per_prompt": {}, "cross_prompt": {},
              "mirrored": {}}

    for name in PROMPTS:
        entry = bank[name]
        per_layer = {}
        for layer in layers:
            comps = components_at(entry["residuals"], entry["detector"]["basis"], layer)
            cos = pairwise_cosines(comps)
            stats = {
                "mean_pairwise_cosine": float(cos[cos != 0].mean()) if comps.shape[0] > 1 else None,
                "consensus_ratio": consensus_ratio(comps),
                "consensus_ratio_null_orthogonal": 1.0 / comps.shape[0] ** 0.5,
                "component_norms": [float(n) for n in comps.norm(dim=-1)],
                "avg_projector_top": float(torch.linalg.svdvals(
                    entry["detector"]["basis"].permute(1, 0, 2).flatten(1)).max().item() ** 2
                    / entry["detector"]["basis"].shape[0]),
                "avg_projector_top_null_orthogonal": 1.0 / entry["detector"]["basis"].shape[0],
            }
            stats.update(sigma1_norm_standardized(comps, entry["detector"]["basis"]))
            # NOTE (scope): a named-basis vs detector-basis disagreement is a DISCRIMINATOR to
        # investigate, not a verdict -- named vocabulary directions may be poor semantic probes.
        # position-class table: mean within-prompt cosine by class (needs >=2 positions/class)
            classes: dict[str, list[int]] = {}
            for p, label in enumerate(entry["labels"]):
                classes.setdefault(position_class(label), []).append(p)
            class_table = {}
            for cls, positions in classes.items():
                if len(positions) >= 2:
                    sub = cos[positions][:, positions]
                    vals = sub[sub != 0]
                    if vals.numel():
                        class_table[cls] = {"positions": positions, "mean_cosine": float(vals.mean())}
            stats["position_class_cosines"] = class_table
            per_layer[layer] = stats
        result["per_prompt"][name] = per_layer

    for layer in layers:
        result["cross_prompt"][layer] = position_locked_cross_cosines(bank, layer)
        # mirrored-selector comparison at the same layer: same statistics, control bases
        result["mirrored"][layer] = {}
        for name in PROMPTS:
            mcomps = components_at(bank[name]["residuals"], bank[name]["mirrored"]["basis"], layer)
            mcos = pairwise_cosines(mcomps)
            vals = mcos[mcos != 0]
            result["mirrored"][layer][name] = {
                "mean_pairwise_cosine": float(vals.mean()) if vals.numel() else None,
                "consensus_ratio": consensus_ratio(mcomps),
            }

    # detector score health: near-zero or tied selections make the basis arbitrary
    for name in PROMPTS:
        tv = bank[name]["detector"]["scores_top64_values"]
        result.setdefault("detector_score_health", {})[name] = {
            "min_top64": float(tv.min()), "max_top64": float(tv.max()),
            "frac_near_zero": float((tv < 1e-6).float().mean()),
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    # console summary: peak-vs-early, observed vs nulls
    for name in PROMPTS:
        row = result["per_prompt"][name]
        print(f"{name:8s} " + " | ".join(
            f"L{L}: cos={row[L]['mean_pairwise_cosine']:+.3f} sigma1={row[L]['sigma1_observed']:.3f}"
            f"(null {row[L]['sigma1_null_p95']:.3f}{',' if row[L]['sigma1_above_null'] else ' BELOW'})"
            f" consensus={row[L]['consensus_ratio']:.3f}(null {row[L]['consensus_ratio_null_orthogonal']:.3f})"
            for L in layers))
    print(f"\noutput: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main(args.bank_dir, args.output)
