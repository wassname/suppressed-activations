# SVD token persistence experiments

Written by Codex/GPT-6. User request: test a suppressed space shared across tokens, then intervene there.

## Finding

The SVD implementation changes answers, but the tested ant result is explained largely by source removal. At rank 1, L24, last four tokens, C=12, no norm restoration:

| [condition](../../out/2026-09-07_svd-ant-parts/run.md) | swap log-odds↑ | p(6)↑ | p(8)↓ |
|---|---:|---:|---:|
| source removal only | **6.125** | **0.793350** | **0.107368** |
| combined difference | 5.375 | 0.672073 | 0.192552 |
| donor addition only | 0.000 | 0.014840 | 0.918103 |

Both first rows generate exactly:

```text
6.

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class **Arachnida** (along
```

The zero-effect donor addition and stronger removal-only effect support source suppression as the main explanation for this selected condition. They do not establish all donor components are ineffective. The removal uses the shared source/donor span, so even this control's span depends on the donor.

## Construction and checks

The core function `token_persistent_subspace` in [suppressed_activation_subspace.py](../../suppressed_activation_subspace.py) concatenates each token's orthonormal suppressed basis and takes a thin SVD. The left singular vectors are eigenvectors of the average projector; persistence is squared singular value divided by token count. Source and donor persistence are estimated separately. Their retained bases are joined with rank-revealing SVD. The patch is the projected difference between token-mean donor and source residuals, constant across patched positions and computed separately at each intervention layer. There is no component or residual norm restoration in SVD conditions.

The initial ant source/donor maximum persistence values were approximately .51/.55, so the retained directions were partly shared, not present in every token's space. The rank sweep deliberately also included less persistent directions. This is past-token averaging, not future Jacobian estimation.

Tests passed for unit persistence with identical token spaces, fixed displacement across patched positions, unchanged unpatched prefix, and unchanged orthogonal content. In real runs all C=0 conditions assert exact logits and token-ID equality with Base. [Tests](../../scripts/test.py).

The initial separate readout and generation passes differed even at C=0. Jobs 490/491 stopped on the strict assertion before completing. Rather than interpreting this discrepancy as harmless, the runner now captures hidden states from the actual generation prefill for extraction and intervention readout. The source of the old separate-pass numerical difference remains unisolated. No fabricated zero-error metric is reported. The displayed readout remains the explicitly labelled suppression-score ranking; it is not a direct label for SVD vectors.

Also corrected older delayed token tables to apply final RMSNorm, corrected their stale hard-min aggregation description/calculation, and preserved prefill intervention norms instead of overwriting them during decode. README and its user edits were not changed. Existing notebook was not regenerated with a selected SVD condition.

## Complete run inventory

All commands use `uv run scripts/oat_sweep.py --prompt-mode chat-assistant-prefill --sweep NAME --target TARGET --output-dir DIR`. All use the pinned Qwen3.5-4B revision recorded in each result.json. Every condition generates up to 32 tokens, including failures. The root report links every condition's exact inputs, readouts, probabilities, configuration, and continuation.

- Jobs 488/489: initial `svd` rank/strength scans, ant/dog, 41 conditions each. [Ant v1](../../out/2026-09-07_svd-ant-v1/run.md), [dog v1](../../out/2026-09-07_svd-dog-v1/run.md). Separate readout pass; superseded for provenance, retained as historical evidence.
- Jobs 490/491: failed separate-pass equality checks. No completed result table. Raw pueue logs retain both failures.
- Job 492: `svd-refine`, ant, 25 conditions. [Ant refinement](../../out/2026-09-07_svd-ant-v3/run.md).
- Job 493: `svd-detector`, ant, 49 conditions. [Detector windows](../../out/2026-09-07_svd-ant-detector-v2/run.md). Every condition starts with 8.
- Job 494: `svd-band`, ant, 25 conditions. [Layer bands and continued generation](../../out/2026-09-07_svd-ant-band/run.md). Continued edits produce social spiders, social networks, and repetition.
- Job 495: `svd-refine`, ant-anthill, 25 conditions. [Anthill wording](../../out/2026-09-07_svd-anthill/run.md). Development wording comparison, not held-out validation.
- Job 496: `svd-refine`, dog, 25 conditions. [Dog comparison](../../out/2026-09-07_svd-dog-v3/run.md). Rank4 C8 gives p4=.862182 and dog readout; several rank1/2 conditions give 6 instead.
- Job 497: `svd-control`, ant, 18 conditions including selected edit, zero, and 16 random directions with matched displacement norm. [Controls](../../out/2026-09-07_svd-ant-controls/run.md). One random edit exceeds selected log-odds movement and outputs 6. No formal significance or held-out claim.
- Job 498: `svd-tokens`, ant, 19 conditions. [Past-token windows](../../out/2026-09-07_svd-ant-tokens/run.md).
- Job 499: `svd-candidates`, ant, 19 conditions. [Per-token candidate ranks](../../out/2026-09-07_svd-ant-candidates/run.md).
- Job 500: `svd-parts`, ant, 3 conditions. [Source versus donor separation](../../out/2026-09-07_svd-ant-parts/run.md).

There are 208 completed conditions on the corrected generation-capture path, including repeated controls and settings. This is a development search, not 208 independent validation samples. Runs of 18–49 conditions took about 39–95 seconds including loading, with peak allocated GPU memory about 13.8 GB. Exact timings are in result.json. Condition cost is about two seconds including generation, not the old 0.15-second forward-only estimate.

## ML-debug audit

- Full data: reviewed JSON rows and unique exact continuations across all corrected batches; independent reviewer reviewed the first 205, main agent the final three as well.
- Configuration: resolved per row; no training. Same official assistant-prefill rendering for source, donor, readout, generation.
- SHOULD: `C=0 gives identical generation and logits because its displacement is zero.` Assertions passed wherever present. Synthetic projector/hook invariants also passed.
- Null: Base p6=.0152447615, p8=.9431601167; swap shift zero by definition. Donor ant itself correctly gives 6. Initial samples remain in every completed result.json.
- Baseline: old component replacement is the default comparison. It moves ant away from 6; SVD moves toward 6 in selected settings. Dummy random control seed15 gives p6=.799951, shift6.625 versus selected .672073, shift5.375.
- Held-out: none established in this development loop. Anthill wording was chosen after social-readout evidence. Dog also produces six, weakening target specificity.
- Schedule/gradients/loss: not applicable; fixed inference interventions.
- Full sample: above; complete input and top-token tables in linked condition logs. Generated strings are not agent prose.
- Worst condition: sustained band edits yield repeated Social. This is a coherence failure even when the first digit is 6.
- Surprise: donor-only shift is zero; removal-only exceeds combined edit. Explained for this setting by source-removal dominance; exact circuit remains unknown.
- Missing evidence: independent ant identity probe, transfer across several questions per concept, ant-specific direction, a repaired detector/writer with coherent concept transfer. Readout overlap is not that evidence.
- Diagnoses after parts test, subjective dominant-cause priorities: source-removal/feature confound 70%; detector geometry mismatch 20%; remaining implementation bug 5%; unknown 5%. Removal control supports first; different spans could change it. Social generation supports detector-content explanation; readout itself is method-dependent. Independent inspection and identity checks count against basic hook error, not against all bugs.
- Fresh review: independent Codex/GPT-6 found no new tensor/index bug and stated: `No coherent ant identity replacement is established.` It flagged dog-to-six and random-to-six controls. Same model family; not an external-family review.
- Cheapest next discriminator was source-only versus donor-only; completed above. A next research change should improve which donor content is extracted, not assume more C transfers ant.
- Reward-hacking count (`hack_s`) and ground-truth pass count (`gt_s`) from the journal skill are not defined for this inference experiment. No invented counts: digit matches and semantic interpretation remain separate.

The SVD implementation is tested and available for further research. The coherent ant concept demo remains unresolved.
