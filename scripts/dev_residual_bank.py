# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Residual bank for the 12 development questions (no generation).

Saves no-intervention prefill residuals (33 layers x seq x 2560), token labels, the (tied) unembedding
and final-norm gain for: each dev cell's source and donor prompt, rendered in
chat-assistant-prefill mode with the standard wrapper instruction. Feeds
late_blocks_table.py so the block-by-block table covers the actual development questions.
One model load, ~24 forwards. -- PI[claude]"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hashlib
import torch

MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REAL_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
REVISION = os.environ.get("SUPPRESSED_REVISION") or (
    REAL_REVISION if MODEL == "Qwen/Qwen3.5-4B" else None
)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")


def main(output_dir: Path, batch_spec: Path) -> None:
    torch.set_grad_enabled(False)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from scripts.prompt import PREFILL_INSTRUCTION, assistant_prefill_input_ids  # NOTE: PREFILL_INSTRUCTION is the runner DEFAULT; the eval batches passed a DIFFERENT explicit instruction - pass it via --instruction / the spec
    from scripts.demo import trajectory

    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = (1.0 + final_norm.weight).float().cpu()

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "model": MODEL, "revision": REVISION, "hidden": int(unembedding.shape[1]),
        "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                       check=True, text=True, capture_output=True).stdout.strip(),
        "wrapper_instruction": PREFILL_INSTRUCTION, "entries": {},
    }
    cells = json.load(open(batch_spec))
    for cell in cells:
        cid = cell["id"]
        for side, key in (("source", "source_prompt"), ("donor", "target_prompt")):
            name = f"{cid}-{side}"
            chat = assistant_prefill_input_ids(
                tokenizer, cell[key], device=DEVICE, instruction=PREFILL_INSTRUCTION)
            residuals, logits = trajectory(model, chat["input_ids"], final_norm)
            torch.save(residuals.float().cpu(), output_dir / f"{name}_residuals.pt")
            manifest["entries"][name] = {
                "token_labels": [tokenizer.decode([int(t)]) for t in chat["input_ids"][0]],
                "seq_len": int(residuals.shape[1]),
                "prompt": cell[key], "cell_id": cid, "side": side,
                "answer_logprobs": {},
            }
        print(f"{cid}: source+donor saved")
    torch.save(unembedding.float().cpu(), output_dir / "unembedding.pt")
    torch.save(norm_gain, output_dir / "norm_gain.pt")
    json.dump(manifest, open(output_dir / "manifest.json", "w"), indent=1)
    print(f"wrote {output_dir/'manifest.json'} ({len(manifest['entries'])} entries)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--batch-spec", type=Path, default=Path("slop/eval_fresh_batch.json"))
    args = ap.parse_args()
    main(args.output_dir, args.batch_spec)
