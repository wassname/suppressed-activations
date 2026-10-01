# Native-chat causal result review

PI/OpenAI. Same-family review, not independent-family approval. Read all named files completely, including all twelve outputs and readout lists. No commands, inference, edits or tensor reconstruction performed.

## Result

The role-aligned donor changes neither requested property on either animal input: leg-count transfer **0/2**, skeleton-position transfer **0/2**, joint transfer **0/2**. The previous literal-name donor also scores 0/2 on each. These are observations about this configuration, not universal completion criteria or a rejection of donor methods.

| Stage | Expected | Observed |
|---|---|---|
| Preparation | Distinct generic animal means | `difference_norm: 0.9205986857414246`; eight property-free prompts |
| Animal generations | Opposite animal’s two properties | Both donors retain both Base properties |
| Arithmetic | Preserve sum and parity | All four conditions retain `4; even` |
| Formatting/termination | Concise, complete responses | All twelve comply; four tokens including EOS |
| Coverage | Prefill plus three cached calls | Four coverage records per condition; reported total 56 forwards |
| Numerical validation | Independently reconstructed edits | Pending; not certified here |

Complete outputs, identical across Base, role-aligned donor, previous donor and random within each case:

- `out/2026-10-01_132318_chat-causal-0/interventions.json`: `"generation": "4; inside<|im_end|>"`, IDs `[19,26,4613,248046]`.
- `out/2026-10-01_132326_chat-causal-1/interventions.json`: `"generation": "8; outside<|im_end|>"`, IDs `[23,26,4732,248046]`.
- `out/2026-10-01_132332_chat-causal-2/interventions.json`: `"generation": "4; even<|im_end|>"`, IDs `[19,26,1442,248046]`.

Thus there are no capped responses, contradictions, refusals or later hypotheses to reinterpret. Arithmetic preservation is 1/1 per condition, not broad specificity. Zero repetition follows from these short outputs and does not establish transfer.

## Movement is not an answer change

Reported 8→4 log-odds shifts are:

| Input | Role-aligned | Previous donor | Random |
|---|---:|---:|---:|
| Dog | −0.0625 | −0.4375 | −0.1875 |
| Spider | +0.1250 | +0.2500 | −0.2500 |
| Arithmetic | −0.3125 | −0.3750 | −0.2500 |

Negative is the intended direction for dog→spider. The new donor moves less than random there. On spider→dog its movement has the intended sign, unlike random, but `p(4)` only moves 0.003321→0.003762. Dog `p(8)` moves 0.00001744→0.00001856. Arithmetic `p(4)` falls 0.824837→0.784508 despite unchanged output. Therefore “no effect” would overstate the negative finding.

Prefill and final-decode readouts are correctly separated. Dog prefill retains `dogs` under both donors; no spider identity appears. Spider prefill retains leading `spiders`, `蜘蛛`, `spider` across conditions, without dog identity. Final-decode lists are dominated by EOS/formatting tokens. Their reorderings demonstrate readout changes, not concept replacement. These prompt-only-masked lists are not a standalone hidden-versus-spoken readout evaluation.

## Findings and uncertainty

1. **Reporting defect:** all three case `run.md` files say, “skeleton uses its own word-answer pair, not the digit metric.” Here `answer_token_ids` remains `[23,19]`, and no skeleton-probability metric is supplied. This stale wording affects interpretation of both animal cases. Replace it with “joint skeleton outcome assessed from complete text.” A separately recorded skeleton metric could disprove this concern.

2. **Attribution limits:** preparation and task frame changed together. New/random requested norms are approximately 0.920599; previous donor norm is 1.430337. Direction and norm are confounded in that comparison. One random seed supplies no null distribution. Known concepts and prior partial-positive behavior informed selection; the records disclose development history but do not establish an exhaustive configuration denominator.

3. **Mechanism remains uncertain:** ineffective transfer, generic formatting perturbation, and an implementation defect remain distinguishable possibilities. Nonzero recorded edits and probability changes argue against a completely inactive hook; they do not certify signed vectors, BF16 application or downstream provenance.

## Next decision

Complete the pending saved-artifact numerical reconstruction first. If it agrees, retain this as a bounded negative joint-transfer result and do not promote or dose-tune this configuration. Correct the skeleton-metric wording. Any next causal attempt should receive a new prospective contract; neither goal is completed here.