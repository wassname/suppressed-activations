# One-layer sample-component replacement predictions

Question: can one consistent whole sample-component operation produce Spider→Ant→6 and Spider→Dog→4 at a single residual layer?

For each target, run its own prompt through Qwen3.5-4B and independently extract a rank-16 suppressed subspace with the fixed L23/L25/L32 rise-and-fall rule. At residual L26 and the final source-prompt token, replace the Spider projection with the norm-matched target-sample projection. Use the same fixed C∈{1,2,4,8,12} grid for Ant and Dog, restore residual norm, and score the first token. Generate 64 tokens only at the smallest unique expected-digit crossing.

| possibility | prior | expected observation |
|---|---:|---|
| usable common sample-component mode | 45% | Ant crosses to 6 and Dog crosses to 4 before either curve degrades |
| single-layer edit too weak | 35% | expected probabilities rise but remain below 8 through the local range |
| target components transport decoder-aligned noise | 35% | both targets converge on one digit or selected target tokens predict repeated lexical output |

This differs from the earlier Dog result, which repeated the same rank-8 basis intervention across L23–L30. A single L26 intervention is cleaner because the residual stream is shared. The result that preserves the public two-demo goal is both distinct crossings under this one operation.

Written by PI/gpt-5.4.
