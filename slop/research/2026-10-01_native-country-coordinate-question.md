# Next causal attempt: native-chat raw coordinate exchange?

PI/OpenAI, proposal for supervisor dialogue, not a queued experiment.

Goals remain open in `.pi/goals/aef0cd-v1.md`. User: "just a few generaitons are enougth to get a measure" and "anyway don't stop". No current-input preparatory pass/backward; reusable offline preparation is allowed. Readout and causal claims remain separate.

## Evidence and uncertainty

- Native country donor2719, `out/2026-10-01_154006_country-donor-joint/conditions_compact.jsonl`: Gothenburg cue always `Stockholm; SEK<|im_end|>`, Osaka always `Tokyo; JPY<|im_end|>`, arithmetic always `4; even<|im_end|>`. Natural generic country-name donor difference changed neither property (0/2 cases), despite nonzero updates. This was fixed addition, not coordinate exchange. Data: `data/sweden_japan_joint_chat_v1.json` and `data/sweden_japan_donors_chat_v1.json`.
- Raw coordinate experiment2648 was Italy/Japan, older raw-completion single-property prompts, final-position prefill/full-strength decode: 0/2 changes. See `slop/audits/2026-10-01_job2648.md`. That exact setting remains retired. Testing the native implicit-country joint-property assay is not a rerun or an isolated chat-format attribution.
- Native-metric readout2721 changed erasure geometry, not editing. Full-list review and pinned-weight checks found no separation gain; both goals remain open. `out/2026-10-01_170327_native-metric-readout/{verification,geometry_verification}.json` and `slop/reviews/2026-10-01_native-metric-result-review.md`.
- Paper/reference distinction: `slop/research/2026-09-30_causal-reference-followup.md`, and actual paper lines220/1416 in `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`. Raw-coordinate exchange, raw-score exchange and unit-column reflection are different. Do not claim exact paper replication.

## Candidate (one operator change versus2719)

Reuse `scripts/english/08_jlens_one_pass.py`, the same three2719 native inputs, block15 edit, block23 observer, last prompt token only, decode scale0.25, 32-token cap and native EOS union. No new layer/dose/spelling/mask/default search; no v5. Choose raw-coordinate exchange rather than donor addition:

```
V = [J15.T @ (gain * W[' Sweden']), J15.T @ (gain * W[' Japan'])]
c = pinv(V) @ h
h_requested = h + scale * V @ (flip(c) - c)
h_applied = BF16(h_requested)
```

These constant vocabulary directions exist before current-input inference. Coefficients use only the current local state. No generic donor forward pass is needed; reuse the existing donor-config concepts/system text only. Use the same symmetric operation for both country cases and the arithmetic control.

Conditions: Base, raw J-coordinate exchange, raw plain-coordinate exchange, seed0 fixed-direction random control. Random norm matches the candidate update computed on the random condition's own current state, before BF16; not primary-condition future states, not equal realized norms across diverging trajectories. One shared GPU float32 Gaussian direction, seed0, saved verbatim, as in the existing country code. At most12 generations/384 tokens, one fresh current-input pass per condition, outer300s cap on local default Pueue queue.

Production changes should reuse `coordinate_swap_bases` / `swap_coordinates`; do not route through `swap_lens_scores`. Keep native Base byte parity to2719. Capture local before/requested/applied tensors, basis/condition singular values, all calls/positions and outputs. For decode, expected coordinates are `(1-scale)*c + scale*flip(c)`, not a full exchange. Log cast error bounds and unchanged orthogonal component before casting. Observers return None and never feed editing.

Report each property separately and joint, all full continuations and both directions without making bidirectionality a new acceptance gate. Stock/Tok next-token movement is not full-city probability. Arithmetic4/even is a limited control, not a general bias proof. No donor, unit-coordinate or per-case winner promotion if this fails.

## Decision question

Is this a useful small attempt at the actual one-pass goal after the fixed-addition negatives, or does available evidence make another attempt more informative? Compare the actual reference operation and executed2648/2719 paths; identify a concrete misconception or blocker if present. Alternative: read out realized attention/MLP residual updates at fixed24/27 rather than the entire residual (new representation, not another erasure strength); it would require a new capture and is not implemented. Do not recommend prolonged bookkeeping or an unfrozen fitted transport with no defensible counterfactual target. Discuss with the supervisor before finalizing a single next choice; no code edits or GPU run.
