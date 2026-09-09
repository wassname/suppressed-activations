"""Emit a fresh-run CLI argv derived from one batch spec (single source of truth). -- PI/OpenAI"""
import json
import shlex
import sys

spec_path, index, outdir, target = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
spec = json.loads(open(spec_path).read().strip() or "[]")[index]
argv = ["uv", "run", "--offline", "scripts/oat_sweep.py",
        "--output-dir", outdir, "--target", target,
        "--sweep", spec["sweep"], "--condition-index", str(spec["condition_index"]),
        "--prompt-mode", spec["prompt_mode"], "--max-new-tokens", str(spec["max_new_tokens"]),
        "--source-prompt", spec["source_prompt"], "--target-prompt", spec["target_prompt"],
        "--source-output", spec["source_output"], "--target-output", spec["target_output"],
        "--prefill-instruction", spec["prefill_instruction"]]
if spec.get("extraction_instruction"):
    argv += ["--extraction-instruction", spec["extraction_instruction"]]
if spec.get("lens_corpus_arrow"):
    argv += ["--lens-corpus-arrow", spec["lens_corpus_arrow"]]
print(shlex.join(argv))
