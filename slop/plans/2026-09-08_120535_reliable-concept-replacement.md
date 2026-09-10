# Reliable suppressed-concept replacement

> "in the end shuld coherenty do dog and ant demo and continue coherenctly" -- wassname

- [ ] goal: one restricted intervention coherently replaces spider with dog and ant across questions.
  - [x] Keep the rule fixed at raw rank-four contrast-energy attenuation, L22--24, C=2, with continuous synchronized steering.
  - [x] Test legs, naming, and one property for dog and ant. Leg questions are coherent; naming self-corrects; dog mammal stays spider; ant antennae has target prose but no explicit Yes.
  - [x] Run eight per-layer rank-matched random spans for each animal. Random spans can exceed the selected digit movement while continuing as spider.
  - [ ] Add only `donor_conditioning={source_token,donor_token}`. Keep U, C, layers, prompt wrapper, positions, and decoding fixed. Run paired dog/ant naming questions.
  - failure mode: donor-token conditioning changes fluency or first digits but still corrects to spider.
  - deliverable: paired full continuations and a predeclared identity rubric for both conditioning modes.

- [ ] goal: distinguish prompt-phase mismatch from a weak method.
  - [x] Repair and GPU-test the user-message generation boundary. Clean source and donor prose are correct, but the intervention stays spider.
  - [ ] Log the first answer-token offset and first-token top distribution in every condition.
  - [ ] If donor-token conditioning fails, run one answer-first user-message control that retains the question in the user message. Do not change the selector at the same time.
  - failure mode: a wrapper comparison changes both answer phase and method inputs, so no causal diagnosis follows.
  - deliverable: a paired wrapper table with prompt representation, answer-token offset, full continuation, and hook coverage.

- [ ] goal: make semantic success measurable rather than inferring it from a digit.
  - [ ] Add a deterministic continuation rubric before the next GPU run: target identity present, source identity absent, expected target property present, and no explicit correction.
  - [ ] Score every existing selected and random continuation with this rubric and retain the raw text beside it.
  - [ ] Keep `swap_log_odds_shift`, `bare_answer_mass`, and repetition as diagnostics only.
  - failure mode: a random edit gets the expected digit or a high log-odds shift and is counted as concept replacement.
  - deliverable: one table linking every score to its complete continuation.

- [ ] goal: validate the suppressed readout separately from generation.
  - [x] Run selected-component and full-state transport; neither validates the delayed lexical detector.
  - [ ] Evaluate a frozen readout on clean spider, dog, and ant prompts plus held-out templates before interpreting any post-edit tokens.
  - failure mode: the readout changes because it shares the intervention construction, not because it measures animal state.
  - deliverable: clean calibration records, capture locations, and held-out accuracy or an explicit failed validation.

## UAT / Verification

| scenario | what it looks like | how we catch it |
|---|---|---|
| success | both naming continuations identify the target through EOS; selected conditions pass the identity rubric; random controls do not | full `result.json` continuations plus the rubric table |
| likely failure | first token moves, then the output says spider or corrects itself | target/source identity and correction checks over the full continuation |
| sneaky failure | a wrapper or random span produces a target digit without target computation | compare fixed paired runs, answer-token offsets, and all matched-random continuations |

Run `just notebook-smoke` before any GPU code change, queue each GPU run through the default pueue group, then read the complete condition logs and apply `ml-debug` plus an independent review. The full audit of jobs 767--779 is [here](../docs/slop/audits/2026-09-09_fixed-band-random-and-wrapper.md).

-- Codex/GPT-6
