"""M2 projection ratio: ||U Uᵀ d_answer|| / ||d_answer||.

d_answer = unembedding(Yes_token) - unembedding(No_token) [pure weight math].
U = span-correction attenuation span (rank 4) from template contrasts, replicating the
runner's template_state_span="attenuation" path. Forward over CONCEPT_TEMPLATES, extract
L20 peak / L32 output contrasts, attenuation_basis(4). Reports the ratio (fraction of the
yes/no decision direction carried by the U-span) per target animal, for the dog/ant
asymmetry.

Usage: uv run --with pyarrow --with loguru --with accelerate scripts/m2_projection.py
       [--targets dog ant] [--out m2_projection.json] [--model tiny|real]
"""
import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import torch
from scripts.oat_sweep import load_bundle, attenuation_basis, CONCEPT_TEMPLATES, render_input
from scripts.demo import trajectory
from scripts.prompt import assistant_prefill_input_ids

INS = "Complete the following fact. Then describe the animal in three sentences."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", nargs="+", default=["dog", "ant"])
    ap.add_argument("--out", default="m2_projection.json")
    ap.add_argument("--peak-layer", type=int, default=20)
    ap.add_argument("--output-layer", type=int, default=32)
    args = ap.parse_args()

    b = load_bundle()
    model, tokenizer = b["model"], b["tokenizer"]
    final_norm = b["final_norm"]
    device = b["device"]

    def embed_diff(tok):
        ids = tokenizer.encode(tok, add_special_tokens=False)
        return (model.lm_head.weight[ids[0]]).float()
    d_space = embed_diff(" Yes") - embed_diff(" No")
    d_bare = embed_diff("Yes") - embed_diff("No")
    print("d_answer norm (spaces):", float(d_space.norm()))

    def build_U(target):
        peaks, outs = [], []
        for tmpl in CONCEPT_TEMPLATES:
            pair = []
            for animal in ("spider", target):
                content = tmpl.format(animal=animal)
                pre = assistant_prefill_input_ids(tokenizer, content, device=device, instruction=INS)
                with torch.no_grad():
                    res = trajectory(model, pre["input_ids"], final_norm)[0]
                end = pre["content_end"]
                seg = res[:, end - 3:end].float()
                pair.append((seg[args.peak_layer].mean(0), seg[args.output_layer].mean(0)))
            peaks.append(pair[1][0] - pair[0][0])
            outs.append(pair[1][1] - pair[0][1])
        P, O = torch.stack(peaks), torch.stack(outs)
        U, values = attenuation_basis(P, O, 4)
        return U, values

    results = {}
    for tgt in args.targets:
        U, values = build_U(tgt)
        UU = U @ U.T
        ratio = (UU @ d_space).norm() / (d_space.norm() + 1e-12)
        ratio_b = (UU @ d_bare).norm() / (d_bare.norm() + 1e-12)
        results[tgt] = {"ratio_YesNo_spaces": float(ratio), "ratio_YesNo_bare": float(ratio_b),
                        "d_answer_norm": float(d_space.norm()), "U_spectrum_le4": [float(v) for v in values[-4:]],
                        "U_shape": list(U.shape)}
        print(f"{tgt}: ratio( Yes vs  No) = {float(ratio):.4f}; bare = {float(ratio_b):.4f}")
    Path(args.out).write_text(json.dumps(results, indent=1) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
