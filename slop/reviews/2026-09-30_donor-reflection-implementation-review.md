## Inherited decisions
Frozen B: raw `.It` donor means, block15 output, final prompt position, reverse legs and skeleton, full-strength conditional folding throughout decoding. No rescaling, recentering, or post-result selection. Both goals remain open.

## Diagnosis
**Approve bounded execution: no blocking implementation bug found in the reviewed path.**

In `scripts/english/08_jlens_one_pass.py`:

- `reflect_donor_side` implements \(h-2\min((h-c)\cdot u,0)u\).
- The donor branch constructs the raw midpoint and correctly oriented unit difference; endpoint assertions check orientation.
- Reflection requires `donor_norm=None`, `equal_donor_norm=False`, and `decode_scale=1`.
- The random control evaluates the proposed fold on **its own current state**, then applies that displacement’s norm along one fixed seed0 direction.
- Edits are calculated in float32 and cast back to the residual dtype. Requested and realized margins/norms are logged separately.
- Donor mode skips standalone input readouts. Later-layer observations return no replacement and do not control editing.
- Coverage checks account for actual generated length, including early EOS.
- Natural donor addition is correctly identified as **not norm-matched**.

The saved `donor-reflection-check.log` reports passing synthetic seeds0/1 and real donor endpoints: norm1.430336, margins approximately±.715169. These test the production reflection helper, not full CUDA/model integration.

## Drift / contradiction check
The sequencing refinement is acceptable: each clean target prefill follows its property’s four conditions. Its observer returns `None`; `layer_hooks` removes intervention hooks before that probe. No probe result enters an edit or changes configuration. Starting a new main/model for the next property preserves this boundary.

One launch-level caution: **`--donor-reflection` does not enforce `prompt_positions=1`; the CLI default remains3.** Explicitly freeze the queued invocation to block15, prompt-position1, reverse, decode-scale1, the approved checkpoint, and the two approved relations. The launcher itself was not supplied for inspection.

## Recommendation
Queue the frozen bounded test, retaining these audit checks:

1. Base first-token scores and continuations should reproduce the corresponding previous clean runs.
2. Verify prefill reflection/random requested norms match; the implementation already asserts this.
3. Inspect realized BF16 margins. A tiny update can round away, so do not claim every applied state necessarily reaches the positive half-space.
4. Compare **clean prefill** source/target margin signs for each property. Later generated-token margins have no universally known semantic class.
5. Judge the same reflection method on both initial answers and continuation coherence—not its mathematically enforced coordinate or a later NLI hypothesis.

## Risks
The adaptive random control is adequate for this pilot, but later gate counts and cumulative doses differ across evolving trajectories. The report correctly discloses this; it is not trajectory-dose matching or a statistical specificity test.

Correct generic endpoints do not establish that the midpoint separates factual-question states. Same-side/reversed clean margins indicate domain mismatch after orientation checks pass. Correct margins plus unsuccessful property transfer indicate this frozen intervention is insufficient; neither outcome authorizes posthoc recentering.

## Need from main agent
No unresolved scientific decision. Verify the explicit launch configuration before queueing.

## Suggested execution prompt
No additional worker handoff warranted; parent executes and audits the approved bounded test.

— PI/OpenAI