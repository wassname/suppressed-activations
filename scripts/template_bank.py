# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Minimal extraction for the reference-delta vector map: the CONCEPT_TEMPLATES corpus
(8 templates x {spider, dog, ant}) rendered exactly as the sweep renders them
(chat-assistant-prefill, same wrapper instruction), saving the last-3-position residual
suffixes per layer. Feeds the same-question vector/procedure table. One model load,
24 forwards, no generation. -- PI[claude]"""

from __future__ import annotations

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
    REAL_REVISION if MODEL == "Qwen/Qwen3.5-4B" else None)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.oat_sweep import CONCEPT_TEMPLATES
from scripts.prompt import PREFILL_INSTRUCTION, assistant_prefill_input_ids  # NOTE: PREFILL_INSTRUCTION is the runner DEFAULT; the eval batches passed a DIFFERENT explicit instruction - pass it via --instruction / the spec
from scripts.demo import trajectory


def main(output_dir: Path) -> None:
    torch.set_grad_enabled(False)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    final_norm = model.model.norm
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"model": MODEL, "revision": REVISION,
                "wrapper_instruction": PREFILL_INSTRUCTION,
                "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                               check=True, text=True,
                                               capture_output=True).stdout.strip(),
                "templates": list(CONCEPT_TEMPLATES), "entries": {}}
    for ti, template in enumerate(CONCEPT_TEMPLATES):
        for animal in ("spider", "dog", "ant"):
            name = f"t{ti}-{animal}"
            chat = assistant_prefill_input_ids(
                tokenizer, template.format(animal=animal), device=DEVICE,
                instruction=PREFILL_INSTRUCTION)
            residuals, _ = trajectory(model, chat["input_ids"], final_norm)
            suf = residuals[:, chat["content_end"] - 3:chat["content_end"]].float().cpu()
            torch.save(suf, output_dir / f"{name}_suffix.pt")
            manifest["entries"][name] = {
                "template_index": ti, "animal": animal,
                "token_labels": [tokenizer.decode([int(t)]) for t in chat["input_ids"][0][-3:]],
                "content_end": chat["content_end"],
            }
        print(f"template {ti} done")
    json.dump(manifest, open(output_dir / "manifest.json", "w"), indent=1)
    print(f"wrote {output_dir/'manifest.json'}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    main(ap.parse_args().output_dir)
