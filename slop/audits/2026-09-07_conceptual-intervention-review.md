# Conceptual intervention review

Written by Codex/GPT-6. Read-only review of experimental code and results; no new GPU run.

## Objective and conclusion

Wassname wants suppressed, unspoken intermediate concepts to be readable and causally editable, with coherent downstream computation. Changing a digit alone does not establish this. The translation result in README is evidence for a detector; the selected dog experiment adds limited causal evidence. Ant failure does not identify which construction step fails.

The current implementation has not tested corpus-averaged future Jacobians. Its persistence heuristic aggregates suppression scores over past prompt positions. Its union heuristic takes the maximum score over positions and selects eight vocabulary rows, rather than constructing the union of per-position spans.

## Primary sources

- [Core detector](../../suppressed_activation_subspace.py): lines 12–35 score rise/fall; 48–50 construct vocabulary basis; 99–100 define persistence; 128–129 define union; 164–169 implement replacement.
- [Sweep](../../scripts/oat_sweep.py): 245–265 selects on past positions; generation logits provide the answer metric; changed readout comes from a separate uncached trajectory.
- [Hooks](../../scripts/demo.py): 103–201. The explicit target position at 156–158 broadcasts one donor vector across all patched positions. Source subtraction is recomputed at each position and layer.
- [Ant log](../../out/2026-09-07_183000_chat-ant-donor-check/conditions/000_default_default/run.md), read in full.
- [Research journal](../../RESEARCH_JOURNAL.md), read in full. README still presents an older raw-input L26 experiment; notebook and ant use assistant prefill. README also says last three tokens before describing the final-token patch. It is user-modified and was not edited.
- Gurnee et al., authors' own paper, [Methods](https://transformer-circuits.pub/2026/workspace/index.html). Local full text: `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`, lines 158–174, 214–222, 1183–1197, 1307–1317. The paper says it averages Jacobians over current/future positions and a corpus. Appendix default targets the penultimate residual. Template lens instead centers per-concept activation means against other concepts and applies inverse covariance. These are different constructions.

## What was actually swept

- `out/2026-09-06_200525_normalization-strength-sweep/result.json`: 20 conditions; strengths 4–64 crossed with both norm options, at L1/all positions. This is not the current L24 assistant-prefill comparison.
- `out/2026-09-06_210907_layer-position-strength-sweep/result.json`: 150 conditions; ten layers, 1/2/4 positions, strengths 1/2/4/8/16. Historical script at the recorded commit calls instructed user-message chat rendering, not assistant prefill.
- `out/2026-09-06_211653_layer-combo-raw/result.json` and `211800_layer-combo-chat-fact`: 32 each; L24, L26, L24+26, L23–26; 1/4 positions; C=1/2/4/8. Raw and user-message chat respectively.
- `out/2026-09-06_212901_persistent-generation-chat-fact/result.json`: 32 conditions continuing intervention during decode, user-message chat.
- Current ant: fixed assistant prefill with C=2/2.5/3/4. No broad layer/token/normalization ant comparison established by these artifacts.

## Findings and open bugs

1. No sign or layer-index error found in the inspected ant replacement path. This is static inspection, not a numerical identity test.
2. Ant log records relative perturbations `[0.4718598, 0.3035629, 0.4325863, 0.5468502]`. Normalization did not erase the intervention. With residual norm restoration, large C asymptotically approaches the normalized displacement; increasing C is not indefinitely increasing displacement.
3. Replacement subtracts a source projection and adds a projection of another sample onto another subspace. It does not set coordinates in one shared space. At four positions, even self-donor replacement need not be identity because it broadcasts the final donor state. Target addition can overlap the source subspace.
4. Vocabulary-row normalization precedes vocabulary centering in the score. Basis construction centers unnormalized rows. The effective score directions and patch directions therefore differ. Impact is unmeasured.
5. The displayed readout is a newly ranked rise/fall score across layers/positions, not the decoded patched component at the final position. It can respond to the intervention's imposed rise/fall itself. This limits semantic interpretation even when recomputed correctly.
6. Confirmed ancillary bug: `scripts/delayed_readout.py:249` unembeds raw final residuals without final RMSNorm. Current sweep uses generation scores and does not use this value.
7. Missing validation: compare cached generation prefill logits with the uncached trajectory used for readout. The existing argmax check compares generation to its own scores. Notebook uses separate uncached probabilities and cached generation too.
8. Continuing-generation hook records overwrite earlier records; the saved norm can represent the last decode step. Some delayed-report text still describes obsolete hard-min persistence.

## Recommended next implementation, not yet run

First verify C=0 identity, aligned self-donor identity, exact patch sites, and cached/uncached agreement. Correct delayed probability reporting before using it as evidence.

Then separate two questions. Does the suppressed span contain useful causal content? Test an aligned common-span donor patch, `h' = h + C P(h_donor - h)`, with P spanning source and target selected directions, at matched token positions. At C=1 this sets the shared-space coordinates to the donor's and preserves the orthogonal remainder if residual rescaling is disabled. It is a control, not a guaranteed concept edit.

Can we identify a reusable concept direction? Preserve suppression as the candidate selector, but derive layer-specific causal directions using averaged downstream Jacobians over independent contexts. For a small concept vocabulary, vector-Jacobian products can estimate selected directions without materializing every d-by-d matrix. Averaging future hidden states alone would not reproduce J-lens. Compare present-only and future-inclusive estimates. Do not optimize gradients of the desired digit on the evaluation prompt, which would permit answer steering without concept transfer.

For writing, use named concept coordinates jointly (pseudoinverse for nonorthogonal directions), with a fixed clean-pass target across a layer band so repeated swaps cannot flip the concept back. Sweep fractional movement and modest bands at a matched perturbation budget. Test several questions about each animal, not just leg count, plus unrelated controls and held-out phrasings. Stronger effects across more sites need not mean fewer side effects.

## ML-debug form

- Log/config: complete ant condition log read; union, rank 8, detector (23,25,32), L24/four positions, C=2.5, both norm options true, assistant prefill, 32 generated tokens.
- SHOULD lines: none. Exact line: `TODO validate: semantic replacement requires a donor-like post-intervention readout and selective transfer beyond this development prompt.`
- Null for cited ant metric: base p6=0.0152447615, p8=0.9431601167, zero log-odds shift by definition. Intervention log says `swap_log_odds_shift: -0.625`.
- Initial sample: clean source answers 8; clean donor says `6.` and identifies an ant. No training or parameter updates.
- Dummy/baseline: unchanged source has higher target-vs-source log odds than every tested ant strength. This measures digit preference, not full semantic coherence.
- Held-out: ant C=2.5 was fixed from dog; other strengths are subsequent development. No held-out multi-question success estimate.
- Schedule: not applicable.
- Full sample: source/donor template and exact continuations in linked ant log. Intervened output begins `8.` and explains spider versus insect legs.
- Worst step: C=4 outputs 2 in strength sweep. No loss or gradients. Not evidence that a particular module is broken.
- Surprise: donor says ant/6, but readout starts `['Social', 'social'`. Explained as a detector/causal-content mismatch candidate; mechanism unconfirmed.
- Missing evidence: numerical hook identities, cached/uncached agreement, fixed concept probe, matched controls for current settings, generalization over functions.
- Diagnoses, rough subjective shares of dominant cause: concept/read-write mismatch 45%; position/projection construction 30%; hidden implementation bug 10%; eval/readout confound 10%; unknown 5%. First supported by donor readout, against: no independent concept measurement. Second supported by explicit broadcast code, against: dog worked under this construction. Implementation: ancillary bug exists, against: main metric uses actual generation scores. Eval: uncached readout differs operationally from generation, against: ant's actual first token is 8. These are priorities, not measured probabilities.
- Fresh review: independent Codex/GPT-6 subagent read code and ant log without the proposed diagnosis. Verdict: `no confirmed sign or layer-index bug in the current ant path`; independently found broadcast donor, score/basis mismatch, omitted delayed RMSNorm, and missing cache agreement test. Same model family, not external-family confirmation.
- Cheapest discriminator: aligned shared-span donor replacement versus existing replacement, after identity/cache checks. Recovery would implicate construction; failure with successful full-state patch would narrow toward subspace selection.
- Runtime/memory: prior summary reports 14–17 seconds per job; not independently timed here. GPU memory unavailable in condition log. No new inference run.

This audit diagnoses and proposes tests. It does not establish that the proposed alternative works.
