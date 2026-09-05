# Job 140 fresh crash review

- The minimal repair at `scripts/spider_ant_demo.py:269`, `clean_h = residuals[INTERVENTION_LAYER][None].float()`, is correct. The intervention hooks also convert hidden states to FP32, and projected directions originate from FP32 weights. Coordinate and pseudoinverse calculations should remain FP32.
- Exact cause: the failed run passed a captured BF16 residual and FP32 directions into `einsum`. The traceback ends with `RuntimeError: expected scalar type BFloat16 but found Float`. The minimal reproduction gives the same error.
- The next likely failure was an unbracketed equal-distance search. Dog and Bird assumed that `C=64` could reach the Ant perturbation distance, then required equality within `1e-3`. The code should check that endpoint before bisection.
- Job 140 provides no scientific result. It failed before metrics were persisted. The partial output contains only `metadata.json` and a placeholder `log.md`, both marked `running`.
- Cheapest preflight: assert equal FP32 dtype and device, run one `coordinate_swap`, and check the bisection endpoint before the model forwards.

Verdict: the FP32 cast is correct. Rerun only after the dtype and distance-bracketing checks.

— reviewer subagent, fresh context
