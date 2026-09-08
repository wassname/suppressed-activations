# Reliable suppressed-concept replacement

> "in the end shuld coherenty do dog and ant demo and continue coherenctly" -- wassname
> "you should not have stopped" -- wassname, about steering through generation

- [ ] Goal: one understandable method replaces spider with dog or ant.
  - Ant versus bee is a diagnostic comparison, not the goal; both have six legs, so leg count cannot distinguish them.
  - [ ] Keep the successful examples as references, not proof of reliability.
  - [ ] Return to source/donor replacement in a shared, layer-local suppressed subspace; do not add another animal-specific correction.
  - [ ] Separate vocabulary rise-and-fall suppression from contrast-energy attenuation. The latter is a candidate selector, not an equivalent definition.
  - [ ] Select persistent directions across aligned prompt tokens; fit at the layer where the edit is applied.
  - [x] Full-state final-layer replacement exactly reproduces both donors (734/735); this is a decoder control, not subspace evidence.
  - [x] Frozen versus synchronized rank8 replacement both remain spider at L12/L20 (736/737).
  - [x] Full selected vocabulary support, ranks51–56, also remains spider at C1/C2 (738/739).
  - [ ] Test stronger doses without normalization (740/741), then the previously useful layer-local attenuation selector with coordinate replacement (742/743).
  - Failure mode: an unrestricted direction or a hand-tuned species correction changes the answer while the claimed suppressed replacement does not.
  - Deliverable: exact construction, resolved settings, and paired logs for both animals, with in-subspace and out-of-subspace edit norms.

- [ ] Goal: the readout measures the changed source computation.
  - [ ] Validate clean spider, dog and ant readouts before interpreting steered ones.
  - [ ] Capture after the edit and subsequent computation, using the same chat-template path as generation.
  - [ ] Check C=0 identity, hook ordering, aligned positions and agreement with generation's first-token logits.
  - [x] Synchronized decoder C=0 matches generation exactly in job 731; retain these assertions in subsequent runs.
  - Failure mode: the readout shows the donor, a pre-edit state, or a classifier that must move because it shares the steering direction.
  - Deliverable: clean and post-edit source readouts with capture locations and controls; keep failures visible.

- [ ] Goal: replacement survives different questions and continuous generation.
  - [ ] Use one fixed rule for both animals; keep species-specific strength tuning out of the final transfer test.
  - [ ] Test naming, leg count and another distinguishing property only where clean source/donor answers are correct.
  - [ ] Steer the last prompt positions and every generated token through EOS or the declared limit; log full continuations.
  - [ ] Compare no edit, donor, matched-random edits and the unrestricted reference. Inspect contradictions, not just target log odds.
  - [ ] On failure, use ml-debug and independent review to distinguish code, prompt and method errors; fix or change the construction, then repeat the paired tests.
  - Failure mode: the first answer changes but the continuation reverses it, invents facts, or repeats; test prompts select the configuration.
  - Deliverable: all conditions in unique timestamped logs, with development and frozen-setting follow-ups identified.

## UAT / Verification

- Open one notebook with complete Base and Causal intervention demos for dog and ant: exact prompt, post-edit readout, verbatim generation and token probabilities.
- Open the linked results table and inspect every frozen follow-up, including failures. A correct number alone is not a pass.
- Verify continuous-hook coverage and C=0 assertions in the logs. Run the notebook smoke test, queued notebook execution and project checks before handoff.
- Terra follows queued jobs to completion; report finished results or actionable failures, not repeated unchanged status.

Written by Codex/GPT-6. This plan does not mark the research goal complete.
