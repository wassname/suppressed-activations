"""H2: per-layer yes/no decodability probe (train-free logit-lens).

For each layer L, take the answer-position residual difference (target - source) from clean
forwards of the property prompts, apply final_norm + unembedding (logit-lens), report the
Yes - No logit gap. Question: at which layer does the answer difference first become visible
to the unembedding, and is it after L20?

Usage: uv run --with pyarrow --with loguru --with accelerate scripts/h2_layer_probe.py
       [--target dog|ant] [--out h2_dog.json]
"""
import sys, json, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import torch
from scripts.oat_sweep import load_bundle
from scripts.demo import trajectory
from scripts.prompt import assistant_prefill_input_ids

INS = "Answer the question with the answer first. Then describe the animal in three sentences."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="dog")
    ap.add_argument("--target-prompt", required=True)
    ap.add_argument("--source-prompt", required=True)
    ap.add_argument("--out", default="h2_layer.json")
    args = ap.parse_args()

    b = load_bundle()
    model, tokenizer = b["model"], b["tokenizer"]
    final_norm = b["final_norm"]
    unembed = b["unembedding"]
    norm_gain = b["norm_gain"]
    device = b["device"]

    yes_id = tokenizer.encode(" Yes", add_special_tokens=False)[0]
    no_id = tokenizer.encode(" No", add_special_tokens=False)[0]

    # one source + one target forward for the property prompts.
    # FIX (supervisor): index res[:, end-1, :] (full vector), not res[:, end-1, 0].
    def capture(prompt):
        pre = assistant_prefill_input_ids(tokenizer, prompt, device=device, instruction=INS)
        with torch.no_grad():
            res = trajectory(model, pre["input_ids"], final_norm)[0]  # [layers+1, 1, D]
        end = pre["content_end"]
        return res[:, end - 1, :].float()  # full answer-position residual per layer [L+1, D]

    src = capture(args.source_prompt)
    tgt = capture(args.target_prompt)

    def logit_gap(vec):
        # final-norm + unembedding of a RAW residual vector (no diff, no RMS-rescale of diff)
        v = vec.view(1, -1)
        v = v * torch.rsqrt(v.square().mean(-1, keepdim=True) + 1e-6)
        v = v * norm_gain.float()
        logits = v @ unembed.float().T
        return float(logits[0, yes_id] - logits[0, no_id])

    results = []
    L = src.shape[0]
    for layer in range(L):
        gap_src = logit_gap(src[layer])
        gap_tgt = logit_gap(tgt[layer])
        diff_norm = float((tgt[layer] - src[layer]).norm())
        results.append({"layer": layer, "gap_source": gap_src, "gap_target": gap_tgt,
                        "gap_target_minus_source": gap_tgt - gap_src, "diff_norm": diff_norm})
        print(f"  layer {layer:2d}: gap_tgt={gap_tgt:+.4f} gap_src={gap_src:+.4f} tgt-src={gap_tgt-gap_src:+.4f} diff_norm={diff_norm:.3f}")
    # last-layer diff_norm sanity: O(1) or more, not 0.001
    last = results[-1]["diff_norm"]
    out = {"target": args.target, "layers": results, "n_layers": len(results),
           "last_layer_diff_norm": last,
           "L20_gap_tgt_minus_src": results[20]["gap_target_minus_source"] if len(results) > 20 else None}
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(f"last layer diff_norm={last:.3f} (sanity: should be O(1) not 0.001); wrote {args.out}")


if __name__ == "__main__":
    main()
