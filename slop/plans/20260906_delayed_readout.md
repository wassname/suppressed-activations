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

-- Codex/gpt-5
