# Template transfer audit

Written by Codex/GPT-6. Observations below come from stored result.json files, not
the selected examples alone. Jobs520/521:136 generations;536/537:56;538–545:8;
526/531:2 long steered continuations. All were read, including unique-string
grouping that retained every condition ID. No result promoted to README.

- Config/log: Qwen3.5-4B pinned revision in each artifact; template contrasts,
  last3 prompt positions and every cached decode call. L24 C1 selected on the
  original prompt, then frozen for the four predeclared heldout prompts.
- SHOULD checks: code asserts C0 exact logits/token equality and decode calls
  equal generated length minus1. All completed grids pass. Independent reviewer
  verified prefill3/decode31 and C0 for all136 template-grid rows.
- Null/init: original base p8=.943160, p6=.015245, p4=.028481. Clean donor is
  an ordinary animal-specific prompt; its generation is in every condition log.
- Dummy: twelve isotropic random directions per animal, matched at selected
  L24 C1 displacement size, all answer8. Ant max p6=.159686; dog max p4=.356460.
  Selected template direction gives .977210 and .920561. These are selected-prompt
  controls, not heldout control estimates.
- Heldout: all4 base prompts answer8 and identify spider. All4 ant interventions
  answer6 and name ant; all4 dog interventions answer4 and name dog. Ant p6 ranges
  .733537–.961645; dog p4 .707797–.919234. All are32-token truncations.
- Schedule: no training, LR, losses or gradients; inference edits only.
- Full sample: [ant128](../../out/2026-09-07_template-fixed-ant-long/run.md),
  [dog128](../../out/2026-09-07_template-fixed-dog-long/run.md).
- Worst sample: dog128 repeats `The animal that spins webs is the **dog**? No.`;
  repeated bigram fraction .488. Ant128 says `six legs`/`Formicidae` but also
  falsely claims ants do not build nests like bees or termites, then introduces
  a beetle aside. No sustained-coherence pass assigned.
- Surprise: strength-only raw dog edits frequently output6, not4. Chasing
  direction/context specificity, not simply weak dose. Strong L24 ends in loops.
- Surprise: projected ant direction fails even at full-delta norm. Ant ranks4–32
  retain .198–.278 of delta norm before rescaling; equal norm does not recover6.
  This narrows the failure to these detected spans, not all suppressed subspaces.
- Missing: heldout128, other concept consequences, readout that identifies ant,
  clean-target intervention stability, null concept direction with similar semantics.
- Diagnoses (subjective, overlapping mechanisms partitioned for next test):
  context-independent decode oversteering40%; source-clue re-reading35%; wrong
  semantic direction15%; hook bug3%; evaluation bug2%; unknown5%. For the first
  two, short target transfer then correction loops supports both; current logs do
  not separate them. Exact hooks/C0 oppose broad hook failure. Numeric success
  with bad long text opposes a metric-only success claim.
- Fresh review (`swap_review`): `No runtime or donor-contamination bug found in
  these artifacts.` Also: `Template contexts explicitly name the animal. Their
  success does not validate the suppression detector.`
- Cheapest discriminator: bounded coordinate clamp plus clean-donor control
  (jobs547/548). If target-side saturation helps, long source continuation improves
  and clean donor changes little. If source KV conflict dominates, source still
  corrects itself despite preserving donor. Absolute-threshold syntax confounding
  predicts substantial clean-donor edits/degradation.
- Runtime: template grids133s/approximately same for dog; projections66/67s;
  each heldout16–17s; long31/28s, excluding queue. Peak memory stored in result.json.
  Reusing loaded models across prompts would reduce repeated initialization.

Execution bug: jobs527–530 and532–535 fail argparse before inference. Full527 log
contains `unrecognized arguments: An animal catches insects ...`. Shell quotes
were consumed before pueue's second parse. Corrected by passing the whole quoted
command as one argument. Retry538–545 preserves exact prompt strings including
trailing spaces. Failed jobs are not counted as negative model outcomes.

The idea remains open: this template estimator shows count/identity transfer, but
unrestricted vector addition does not yet meet sustained coherence. A success on
32 tokens cannot prove a success on128; a poor vocabulary-based projected span
cannot disprove data-derived persistent concept directions.
