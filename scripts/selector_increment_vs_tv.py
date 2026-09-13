# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8", "transformers>=5.5"]
# ///
"""ACTUAL-selector comparison on the exact-input bank (CPU, no model calls).

Baseline = the production `increment_scores` (whole-trajectory: normalized readout at
every layer, vocab-centered per-increment, build = sum of positive increments over the
40-70% window, cut = sum over exactly the last-3 writes, score = min(build, cut)).
Probe = total positive variation of the normalized readout over ALL layers (oscillation
permissive; documented as a probe — NOT a deleted-energy claim). Reports top-32
overlap, one sampled token's complete 33-point traces (normalized readout, per-write
increment, residual RMS, unit-projected energy), and saves the primary arrays.
Input: out/2026-09-12_exact-input-bank-att3/legs-L1-dog-source_residuals.pt
(hash in the bank manifest). -- PI[glm-5p3-flash]"""
import hashlib
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from suppressed_activation_subspace import increment_scores

D = ROOT / "out" / "2026-09-12_exact-input-bank-att3"
OUT = ROOT / "out" / "2026-09-13_selector-increment-vs-tv"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = torch.load(D / "legs-L1-dog-source_residuals.pt", weights_only=False).float()
    U = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()
    input_sha = hashlib.sha256((D / "legs-L1-dog-source_residuals.pt").read_bytes()).hexdigest()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B",
                                        revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    # production call shape: (seq, layers, hidden)
    sc = increment_scores(res.permute(1, 0, 2), U, gain, normalize_unembedding_rows=True)
    edited = [res.shape[1] - 3, res.shape[1] - 2, res.shape[1] - 1]
    # probe: total positive variation of the normalized readout, all layers, vocab-centered
    h = res.permute(1, 0, 2).float()
    h_norm = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain.float()
    logits = h_norm @ U.float().T
    rown = (U * gain.float()).norm(dim=-1)
    logits = logits / rown
    dphi = logits[:, 1:] - logits[:, :-1]
    dphi = dphi - dphi.mean(-1, keepdim=True)
    tv = dphi.relu().sum(1)                          # (seq, V) per-position total variation
    sc_win = sc[edited].sum(0)                       # production selection over the window
    tv_win = tv[edited].sum(0)
    top_inc = set(sc_win.topk(32).indices.tolist())
    top_tv = set(tv_win.topk(32).indices.tolist())
    print(f"top-32 overlap production-increment vs total-variation: {len(top_inc & top_tv)}/32")

    tok_id = sc_win.topk(1).indices[0].item()
    pos = edited[-1]
    h1 = res[:, pos, :].float()                      # (33, hidden): all layers, one position
    rms = h1.square().mean(-1).sqrt()
    hn = h1 * torch.rsqrt(h1.square().mean(-1, keepdim=True) + 1e-6) * gain.float()
    lg = ((hn @ U.float().T) / rown)[0]                # (33,) readout at this token
    direction = (U[tok_id] * gain) / rown[tok_id]          # unit row direction (hidden,)
    unit_e = direction @ h1.T                              # unit-projected energy/layer
    dphi_t = lg[1:] - lg[:-1]
    dphi_t = dphi_t - dphi_t.mean(-1, keepdim=True)
    trace = {"token_id": tok_id, "token": tok.decode([tok_id]), "position": pos,
             "normalized_readout": lg.tolist(), "increment_dphi": dphi_t.tolist(),
             "residual_rms": rms.tolist(), "unit_projected_energy": unit_e.tolist()}
    torch.save({"scores_increment_per_position": sc, "scores_tv": tv,
                "trace": trace, "input_sha256": input_sha,
                "top32_increment": sorted(top_inc), "top32_tv": sorted(top_tv)},
               OUT / "selector_comparison_arrays.pt")
    print(f"sampled token {tok_id} ({tok.decode([tok_id])!r}) at position {pos}:")
    print("  normalized readout (33):", [round(x, 3) for x in lg.tolist()])
    print("  per-write increment (32):", [round(x, 3) for x in dphi_t.tolist()])
    print("  residual RMS (33):", [round(x, 2) for x in rms.tolist()])
    print("  unit-projected energy (33):", [round(x, 3) for x in unit_e.tolist()])
    (OUT / "summary.json").write_text(json.dumps(
        {"overlap": len(top_inc & top_tv), "sampled_token": trace["token"],
         "token_id": tok_id, "input_sha256": input_sha}, indent=1) + "\n")
    print(f"arrays: {OUT / 'selector_comparison_arrays.pt'}")

if __name__ == "__main__":
    main()
