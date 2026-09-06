- [ ] goal: measure the patched state after the original readout boundary
  - format each source and donor as the same Qwen chat request for both extraction and generation
  - add a suffix-position replacement that patches the last four source tokens at L23, before the L25 peak used by the detector
  - use the matching last four donor residuals, not one donor vector copied four times
  - record the detector at the source final token after the patch
  - failure mode: the selected rows retain spider tokens because the detector still reads pre-edit layers
  - discriminator: L23, L25, and L32 used by the detector all follow the patched forward pass
  - deliverable: one artifact with Base and four-token patched readouts, token probabilities, and the exact hook configuration

- [ ] goal: distinguish a state change from text-feedback after decoding
  - cache the patched prompt forward pass, then force identical continuation tokens in Base and patched conditions
  - record residual trajectories after each forced token without later interventions
  - failure mode: different generated digits make later readouts differ even when cache state did not persist
  - discriminator: both conditions consume byte-identical forced tokens
  - deliverable: per-token detector rows and source/donor subspace projections

- [ ] goal: make formatting auditable
  - record the exact rendered chat token IDs and decoded template in the raw artifact
  - failure mode: extraction uses a chat prompt but generation uses the raw fact string
  - discriminator: both calls receive the identical `input_ids`
  - deliverable: a test that asserts the input IDs passed to extraction and generation are equal

## UAT / Verification

`just notebook-smoke` exercises the new positions path on the tiny model. A queued GPU run writes
`out/<timestamp>_delayed-readout/run.md` and raw JSON. The report states whether the readout
changed, remained spider-related, or could not be interpreted because a check failed.

## Layer and dose sweep

> “hone in on supressed acivaiton through layers, and persistant subspace through tokens” — wassname

1. [/] goal: Test a persistent suppressed readout before interpreting causal steering.
   - subtle failure mode: extraction reads assistant template tokens or unions unrelated per-position tokens.
   - discriminator: `run.md` names the exact four user-content tokens and reports every selected token's suppressed score at every position.
   - method: rank tokens by the minimum rise-and-fall suppressed score across the four positions, then construct one fixed rank-8 basis.
   - verify: the source and donor readout tables plus the recomputed post-intervention readout are present in the unique job log.

2. [/] goal: Separate direction persistence from intervention duration.
   - subtle failure mode: a longer intervention changes donor directions as well as source positions, so position count is uninterpretable.
   - discriminator: use the fixed donor component at its final user-content token for every patched source position.
   - verify: unit test checks explicit source and donor positions; job logs per-position perturbation norms.

3. [ ] goal: After the persistent default, independently compare representation and normalization.
   - representation: strict persistent set, union, and per-position directions.
   - normalization: component matching/full residual restoration, neither, and each separately.
   - subtle failure mode: a factorial sweep hides why a result moved.
   - discriminator: change one family per job and retain the same target-vs-source log-odds metric.

- [ ] goal: compare layer, suffix length, and C without changing prompt format
  - sweep all residual layers L1–L32, suffix lengths 1–4, and C in 0.25–8
  - rank only by change in `log p(4) - log p(8)` from Base
  - log per-position and aggregate perturbation sizes so C is not mistaken for an absolute dose
  - failure mode: selecting the maximum from 768 rows is presented as confirmation
  - discriminator: `run.md` labels the best row as development-selected and requires held-out confirmation
  - deliverable: a unique `run.md` with the complete Base and selected-intervention generations

Prediction: suffix length need not be monotonic because positions are edited separately. If the
old L26 effect is real under the chat-formatted prompt, L26/C4/one-position should have positive
log-odds shift. A negative value there would show that prompt formatting changed the phenomenon.

-- Codex/gpt-5
