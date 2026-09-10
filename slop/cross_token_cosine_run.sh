#!/usr/bin/env bash
# Cross-token signed-cosine measurement + behavioral comparison for one animal.
# Usage: cross_token_cosine_run.sh dog|ant   (prompts live here, so saved argv stays quote-safe)
# Written by PI[claude].
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export HF_HUB_OFFLINE=1

concept="${1:?usage: cross_token_cosine_run.sh dog|ant}"
case "$concept" in
  dog)
    target_prompt="Fact: The number of legs on the animal that barks and is called man's best friend is "
    target_output="4" ;;
  ant)
    target_prompt="Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is "
    target_output="6" ;;
  *) echo "unknown concept: $concept" >&2; exit 2 ;;
esac

out_dir="out/2026-09-10_crosstoken_${concept}"
mkdir -p "$out_dir"
uv run scripts/cross_token_cosine.py \
  --output "$out_dir/result.json" \
  --target-prompt "$target_prompt" \
  --target-concept "$concept" \
  --target-output "$target_output" \
  --control-prompt "Fact: The number of legs on the animal that lives in the ocean is "
echo "DONE $concept -> $out_dir/result.json"
