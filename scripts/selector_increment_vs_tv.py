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
    pos48_rank = int((sc[pos] > sc[pos, tok_id]).sum())
    print(f"  chosen token: AGGREGATE-top across positions; rank at pos {pos} = {pos48_rank}")
    h1 = res[:, pos, :].float()                      # (33, hidden): all layers, one position
    rms = (h1.square().mean(-1) + 1e-6).sqrt()       # production eps
    direction = (U[tok_id] * gain) / rown[tok_id]    # unit row direction (hidden,)
    # SIGNED projection per layer (can be negative); normalized readout = that
    # projection divided by the per-layer residual RMS
    signed = direction @ h1.T                        # (33,)
    lg = signed / rms                                # (33,) token across layers
    assert lg.shape == (res.shape[0],), lg.shape
    energy = signed.square()                         # nonnegative projected energy
    assert float(energy.min()) >= 0.0
    # per-write increments from the FULL vocab readout, vocab-centered per write
    hn = h1 * torch.rsqrt(h1.square().mean(-1, keepdim=True) + 1e-6) * gain.float()
    full_lg = ((hn @ U.float().T) / rown)
    assert full_lg.shape == (res.shape[0], U.shape[0])
    torch.testing.assert_close(lg, full_lg[:, tok_id], rtol=1e-4, atol=1e-5)
    dphi_full = full_lg[1:] - full_lg[:-1]
    dphi_full = dphi_full - dphi_full.mean(-1, keepdim=True)
    dphi_t = dphi_full[:, tok_id]
    assert dphi_t.shape == (res.shape[0] - 1,), dphi_t.shape
    trace = {"token_id": tok_id, "token": tok.decode([tok_id]), "position": pos,
             "normalized_readout": lg.tolist(), "increment_dphi": dphi_t.tolist(),
             "residual_rms": rms.tolist(), "signed_projection": signed.tolist(),
             "projected_energy": energy.tolist()}
    torch.save({"scores_increment_per_position": sc, "scores_tv": tv,
                "trace": trace, "residual_tensor_file_sha256": input_sha,
                "top32_increment_aggregate_probe": sorted(top_inc),
                "top32_tv_aggregate_probe": sorted(top_tv)},
               OUT / "selector_comparison_arrays.pt")
    print(f"sampled token {tok_id} ({tok.decode([tok_id])!r}) at position {pos}:")
    print("  normalized readout (33):", [round(x, 3) for x in lg.tolist()])
    print("  per-write increment, vocab-centered (32):", [round(x, 3) for x in dphi_t.tolist()])
    print("  residual RMS (33):", [round(x, 2) for x in rms.tolist()])
    print("  signed projection (33):", [round(x, 3) for x in signed.tolist()])
    print("  projected energy = signed^2 (33):", [round(x, 3) for x in energy.tolist()])
    (OUT / "summary.json").write_text(json.dumps(
        {"overlap": len(top_inc & top_tv), "sampled_token": trace["token"],
         "token_id": tok_id, "input_sha256": input_sha}, indent=1) + "\n")
    print(f"arrays: {OUT / 'selector_comparison_arrays.pt'}")

if __name__ == "__main__":
    main()



def per_position_selection_counts():
    # Exhaustive final-write classification of ACTUAL production-selected tokens
    # (sc[pos] > 0 mask recorded; per-position). Inputs: the three DISTINCT legs
    # questions (spider source, dog donor, ANT DONOR; manifest-verified).
    # Signed prev/last classes partition exactly; energy compared last-vs-prev AND
    # last-vs-last-3-start separately. -- PI[glm-5p3-flash]
    D = ROOT / "out" / "2026-09-12_exact-input-bank-att3"
    U = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B",
                                        revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    manifest = json.load(open(D / "manifest.json"))
    for c in manifest["preflight"]["checks"]:
        if c["cell"] == "legs-L1-ant" and c["side"] == "donor":
            assert "colonies" in tok.decode(c["ids"]), "ant donor prompt mismatch"
    counts, records = {}, {}
    for name, stem in (("source_spider", "legs-L1-dog-source"),
                       ("dog_donor", "legs-L1-dog-donor"),
                       ("ant_donor", "legs-L1-ant-donor")):
        res = torch.load(D / (stem + "_residuals.pt"), weights_only=False).float()
        sc = increment_scores(res.permute(1, 0, 2), U, gain, normalize_unembedding_rows=True)
        seq = res.shape[1]
        cls = {"pos->neg": 0, "neg->pos": 0, "nonneg-increase": 0, "nonneg-decrease": 0,
               "nonpos-increase": 0, "nonpos-decrease": 0, "equal": 0}
        e_cmp = {"energy_last<prev": 0, "energy_last<start3": 0}
        pairs = []
        n_sel = 0
        for pos in (seq - 3, seq - 2, seq - 1):
            # actual production basis selection: top-k (rank 8) of the production score
            ids_sel = sc[pos].topk(8).indices.tolist()
            assert all(sc[pos, t] > 0 for t in ids_sel)
            h1 = res[:, pos, :].float()
            rms = (h1.square().mean(-1) + 1e-6).sqrt()
            hn = h1 * torch.rsqrt(h1.square().mean(-1, keepdim=True) + 1e-6) * gain.float()
            full_lg = (hn @ U.float().T) / (gain * U).float().norm(dim=-1)
            for tid in ids_sel:
                lg_t = full_lg[:, tid]
                signed = lg_t * rms
                prev, last = float(signed[-2]), float(signed[-1])
                if prev >= 0 and last < 0:
                    k = "pos->neg"
                elif prev < 0 and last >= 0:
                    k = "neg->pos"
                elif last > prev:
                    k = "nonneg-increase" if prev >= 0 else "nonpos-increase"
                elif last < prev:
                    k = "nonneg-decrease" if prev >= 0 else "nonpos-decrease"
                else:
                    k = "equal"
                cls[k] += 1
                n_sel += 1
                e_prev, e_last = prev ** 2, last ** 2
                e_start3 = float(signed[-4]) ** 2   # last-3 writes start at h29
                if e_last < e_prev:
                    e_cmp["energy_last<prev"] += 1
                if e_last < e_start3:
                    e_cmp["energy_last<start3"] += 1
                pairs.append({"pos": pos, "token_id": tid, "token": tok.decode([tid]),
                              "class": k, "signed_prev": prev, "signed_last": last,
                              "energy_prev": e_prev, "energy_last": e_last,
                              "energy_start3": e_start3,
                              "selected_score": float(sc[pos, tid])})
        assert sum(cls.values()) == n_sel, (cls, n_sel)
        counts[name] = {"classes": cls, "energy": e_cmp, "n_selected": n_sel,
                        "selected_per_position_top8": [8, 8, 8],
                        "score_positive_per_position": [int((sc[q] > 0).sum())
                                                        for q in (seq - 3, seq - 2, seq - 1)]}
        records[name] = pairs
        print(name, "n_selected", n_sel, "per-pos mask", counts[name]["selected_per_position_top8"], "|", cls, "|", e_cmp)
    (OUT / "per_position_class_counts.json").write_text(
        json.dumps({"counts": counts, "pairs": records}, indent=1) + "\n")
    print("saved:", OUT / "per_position_class_counts.json")
    return counts, records


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "counts":
    per_position_selection_counts()
