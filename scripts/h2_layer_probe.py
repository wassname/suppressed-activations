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

    # one source + one target forward for the property prompts
    def capture(prompt):
        pre = assistant_prefill_input_ids(tokenizer, prompt, device=device, instruction=INS)
        with torch.no_grad():
            res = trajectory(model, pre["input_ids"], final_norm)[0]  # [layers+1, 1, D]
        end = pre["content_end"]
        return res[:, end - 1, 0].float()  # answer-position residual per layer

    src = capture(args.source_prompt)
    tgt = capture(args.target_prompt)

    results = []
    L = src.shape[0]
    for layer in range(L):
        diff = (tgt[layer] - src[layer])
        # logit lens matching the runner: RMS-normalize, scale by norm_gain, then unembedding
        hn = diff * torch.rsqrt(diff.square().mean(-1, keepdim=True) + 1e-6)
        hn = hn * norm_gain.float()
        logits = hn @ unembed.float().T
        gap = float(logits[yes_id] - logits[no_id])
        results.append({"layer": layer, "yes_minus_no_logit_gap": gap,
                        "diff_norm": float(diff.norm())})
        print(f"  layer {layer:2d}: Yes-No logit gap = {gap:+.4f} (diff_norm {float(diff.norm()):.3f})")
    # find first layer where gap > 0 (answer difference visible to unembedding)
    first_positive = next((r["layer"] for r in results if r["yes_minus_no_logit_gap"] > 0), None)
    out = {"target": args.target, "first_layer_yes_logit_gap_positive": first_positive,
           "layers": results, "n_layers": len(results), "L20_gap": results[20]["yes_minus_no_logit_gap"] if len(results) > 20 else None}
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(f"first layer with Yes>No logit gap: {first_positive}; wrote {args.out}")


if __name__ == "__main__":
    main()
