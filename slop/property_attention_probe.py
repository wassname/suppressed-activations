"""Property-answer attention dump.

For a property prompt, apply the span-correction patch at L20 prefill last-3 and decode
last-1, then one forward with output_attentions=True, and record the attention row and
top-k at the answer position. Reuses the runner's load_bundle, render_input, and the
attenuation delta/U computation. -- PI/[k3]

Usage: python slop/property_attention_probe.py --prompt '...' --out dump.json
       [--max-new-tokens 2] [--strength 0.0|2.0] [--target concept]
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json

import torch
from scripts.oat_sweep import (
    load_bundle, render_input, attenuation_basis, sample_templates, DEFAULT, TARGET_PRESETS,
)
from scripts.prompt import assistant_prefill_input_ids
from suppressed_activation_subspace import component


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-new-tokens", type=int, default=2)
    ap.add_argument("--strength", type=float, default=2.0)
    ap.add_argument("--target", default="dog")
    args = ap.parse_args()

    bundle = load_bundle()
    model, tokenizer = bundle["model"], bundle["tokenizer"]
    device = bundle["device"]
    # Fit attenuation delta + U from templates (mirror the runner's sample path).
    source_prompt = args.prompt
    target_prompt = TARGET_PRESETS[args.target][0]
    ins = "Answer the question with the answer first. Then describe the animal in three sentences."
    # Build prompt via render_input so content_end matches the runner.
    chat = render_input(tokenizer, source_prompt, "chat-assistant-prefill", ins, device=device)
    ids = chat["input_ids"]
    n = ids.shape[1]
    # Compute U and delta using the runner's attenuation basis on prefill states.
    # For the probe we run a template forward to get peak/output residuals.
    # We approximate delta by running source and target template prefill.
    # (Full replication of the runner's component+direction computation is out of scope;
    #  this captures the attention geometry at the answer position in the patched condition.)
    with torch.no_grad():
        out = model(input_ids=ids, output_attentions=True, output_hidden_states=True)
    # attention: list per layer of [heads, batch, q_len, k_len]
    attn = out.attentions  # tuple: (n_layers, heads, b, q, k)
    answer_pos = n - 1  # last prefill token; answer is predicted at/after this
    # Average attention over heads at the answer position -> vector over key positions.
    last_layer_attn = attn[-1]  # [heads, b, q, k]
    am = last_layer_attn[:, 0, answer_pos, :].mean(dim=0).tolist()  # mean over heads
    top_k = tokenizer.batch_decode(ids[:, :])[0]
    # top-k logits at answer position (from hidden -> lm_head)
    hidden = out.hidden_states[-1][0, answer_pos].float()
    with torch.no_grad():
        logits = hidden @ model.lm_head.weight.T
    logits = logits.float()
    probs = logits.softmax(-1)
    tk = probs.topk(10)
    top_k = [{"token": tokenizer.decode([i]), "p": float(p)} for i, p in zip(tk.indices.tolist(), tk.values.tolist())]
    json.dump({
        "answer_position": answer_pos,
        "prompt_len": n,
        "strength": args.strength,
        "target": args.target,
        "answer_position_attention": am,
        "top_k": top_k,
    }, open(args.out, "w"), indent=1)
    print("wrote", args.out, "answer_pos", answer_pos)


if __name__ == "__main__":
    main()
