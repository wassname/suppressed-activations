# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8", "transformers>=5.5"]
# ///
"""CPU analysis of the bridge capture (NO forward, NO model): the production paired
basis builder (increment_union_basis — the same function run_with_bundle calls) on the
captured source/dog/ant trajectories. Saves: U4 + singular values + per-position
selected IDs/decoded tokens + ALL 33-point centered readout traces + the SVD column
contributions aggregated per 8-column position blocks (labeled basis overlap, not
causal effect). -- PI[glm-5p3-flash]"""
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import torch

from suppressed_activation_subspace import increment_scores
from scripts.oat_sweep import increment_union_basis

D = ROOT / "out" / "2026-09-13_bridge-capture-211809"
OUT = ROOT / "out" / "2026-09-13_bridge-basis-analysis"
CFG = SimpleNamespace(readout_positions=4, common_source_rank=8, common_donor_rank=8,
                      persistent_rank=4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.load(open(D / "manifest.json"))
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(manifest["model"], revision=manifest["revision"])
    unemb = torch.load(D / "unembedding.pt", weights_only=False).float()
    gain = torch.load(D / "norm_gain.pt", weights_only=False).float()

    samples = {}
    for name in ("source", "dog", "ant"):
        res = torch.load(D / f"{name}_residuals.pt", weights_only=False).float()
        ids = manifest_ids(manifest, name)
        # the manifest's saved ID hash must match the reconstruction from the bridge rows
        h = hashlib.sha256(torch.tensor(ids).numpy().tobytes()).hexdigest()
        entry = manifest["inputs"][name if name != "source" else "source"]
        assert h == entry["ids_sha256"], f"{name}: capture IDs != manifest hash"
        samples[name] = {"residuals": res, "content_end": len(ids), "ids": ids}

    # the ACTUAL production paired builder (the same function run_with_bundle calls)
    shared_dog, diag_dog = increment_union_basis(samples["source"], samples["dog"],
                                                 CFG, unemb, gain)
    shared_ant, diag_ant = increment_union_basis(samples["source"], samples["ant"],
                                                 CFG, unemb, gain)

    # per-input: selected IDs/labels + 33-point centered readout traces
    selected, traces = {}, {}
    for name, sample in samples.items():
        res, seq = sample["residuals"], sample["residuals"].shape[1]
        sc = increment_scores(res.permute(1, 0, 2), unemb, gain,
                              normalize_unembedding_rows=True)
        h = res[:, seq - CFG.readout_positions:, :].float()
        rms = (h.square().mean(-1) + 1e-6).sqrt()
        hn = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain
        lg = (hn @ unemb.T) / (gain * unemb).float().norm(dim=-1)
        dphi = lg[1:] - lg[:-1]
        dphi = dphi - dphi.mean(-1, keepdim=True)  # the production vocab centering
        sel = {}
        for qi, q in enumerate(range(seq - CFG.readout_positions, seq)):
            ids8 = sc[q].topk(CFG.common_source_rank).indices.tolist()
            sel[str(q)] = {"labels": [tok.decode([t]) for t in ids8],
                           "decoded_input_token": tok.decode([sample["ids"][q]]),
                           "scores": [float(sc[q, t]) for t in ids8],
                           "readout_levels_uncentered": {t: [round(x, 4) for x in lg[:, qi, t].tolist()]
                                      for t in ids8},
                           "increments_vocabcentered": {t: [round(x, 4) for x in dphi[:, qi, t].tolist()]
                                          for t in ids8}}
        selected[name] = sel
        traces[name] = lg  # full (33, V) per input, sliced per token above

    # SVD column contributions per 8-column position block (BASIS OVERLAP — the share
    # of each U4 direction inside each position's basis block; NOT a causal effect)
    blocks = {}
    for pair, shared in (("source_dog", shared_dog), ("source_ant", shared_ant)):
        per_pos = []
        for name, sample in (("source", samples["source"]),
                             ("dog" if pair == "source_dog" else "ant",
                              samples["dog" if pair == "source_dog" else "ant"])):
            res = sample["residuals"]
            seq = res.shape[1]
            sc = increment_scores(res.permute(1, 0, 2), unemb, gain,
                                  normalize_unembedding_rows=True)
            h = res[:, seq - CFG.readout_positions:, :].float()
            rms = (h.square().mean(-1) + 1e-6).sqrt()
            hn = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6) * gain
            for q in range(seq - CFG.readout_positions, seq):
                ids8 = sc[q].topk(CFG.common_source_rank).indices.tolist()
                Qpos = (unemb[ids8].float() * gain).T          # (d, 8) orthonormal block
                Qpos, _ = torch.linalg.qr(Qpos)
                per_pos.append(Qpos)
        contrib = []
        for i in range(shared.shape[1]):
            u = shared[:, i]
            contrib.append([float((blk.T @ u).square().sum()) for blk in per_pos])
        blocks[pair] = contrib  # sum((Qpos.T@U4)^2) per position block: the basis overlap share
    torch.save({"U4_source_dog": shared_dog, "U4_source_ant": shared_ant},
               OUT / "basis_U4.pt")
    (OUT / "analysis.json").write_text(json.dumps(
        {"diag": {"source_dog": diag_dog, "source_ant": diag_ant},
         "selected": selected, "block_overlaps": blocks}, indent=1) + "\n")
    for n in ("source", "dog", "ant"):
        print(n, "selected labels:")
        for q, v in selected[n].items():
            print(f"  pos {q} (input token {v['decoded_input_token']!r}):", v["labels"])


def manifest_ids(manifest, name):
    bridge = ROOT / "out" / "2026-09-13_bridge-matrix-193115"
    tag = "dog-att-h20" if name == "source" else f"{name}-att-h20"
    run = json.load(open(bridge / tag / "result.json"))
    ri = run["rendered_inputs"]
    return ri["source" if name == "source" else "donor"]["input_ids"]


if __name__ == "__main__":
    main()
