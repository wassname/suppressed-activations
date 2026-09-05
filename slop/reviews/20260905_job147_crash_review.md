# Job 147 fresh crash review

Job 147 loaded Qwen3.5-4B and reached the new sample-component dose path.

Exact cause: `evaluate_prompt` created `mask` with default floating dtype. Earlier hooks multiplied by this 0/1 mask, which is valid. `sample_component_hook` used it as the condition to `torch.where`, which requires boolean dtype. The traceback ends:

> `RuntimeError: where expected condition to be a boolean tensor, but got a tensor with dtype Float`

Minimal fix: construct the position mask with `dtype=torch.bool` and set its final entry to `True`. Boolean multiplication remains valid in the prior paths.

The failure was not caught because `torch.where` is unique to the newly introduced sample-component hook. The partial artifact remains marked `running` and contains no result JSON; no scientific inference is possible.

A second operational problem is that exceptions leave partial metadata marked `running` and discard completed in-memory conditions. Failure-state persistence would make such directories self-describing, but it is separate from the minimal scientific rerun.

Verdict: fix the mask, add a hook-level test, and rerun without changing the experiment.

— reviewer subagent, fresh context
