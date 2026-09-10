# Synchronized donor brief: frozen vs state-updated donor at L20 C=1.5

Written and committed before the GPU run. PI[claude]. Tests the recovered state-dependent lead
(job 743: donor updating preserved ant identity where a frozen donor kept spider) under the
frozen candidate's settings, on the six development pairs.

## Equation and coordinate alignment (identical for both arms)

Both arms use the runner's existing `shared_replace` operation in the candidate's coordinate
system: the L20 template-attenuation span U (rank 4, detector layers (18, 20, 32), centered
unit-gain unembedding directions, aggregation union). At every patched position (last-3 prefill
positions and every cached decode step) and every generation step t:

    h'_t = h_t + C ( UUᵀ d_t − UUᵀ h_t ),   C = 1.5, shapes: h_t [1, pos, 2560],
    d_t [1, pos, 2560] donor state, U [2560, 4], UUᵀ the projector onto the L20 span.

The removal term −C·UUᵀh_t is the candidate's current-state removal, identical in both arms.
No component-norm matching, no residual renormalization (asserted by the runner's synchronized
branch). The orthogonal source residual is preserved exactly.

## The two arms (only d_t differs)

- **Frozen donor**: d_t = the donor's clean prefill state at the donor's readout position,
  constant across all steps and positions.
- **Synchronized donor**: d_t = the donor's CURRENT state when teacher-forced on the
  source-generated tokens (the runner's existing `generate_synchronized_donor`: the donor runs
  with its own KV cache on the source-selected tokens; `assert source_history == donor_history`
  verifies the donor consumed exactly the source's tokens).

## Donor token-history policy (explicit)

The donor conditions ONLY on its own prefill plus source-generated tokens. No donor
ground-truth answer token and no donor-preferred continuation token is ever fed: the donor's
input at step t is the source's actual generated token. The runner asserts
`source_history == donor_history` every step, so donor conditioning is wholly source-derived.

## Invariants asserted at runtime

1. **Prefill equality**: at step 0 the donor state is its clean prefill state in both arms, so
   the two arms' first sampled tokens must be equal; asserted per pair.
2. **C0 identity**: both arms at C=0 must reproduce clean source logits/token IDs exactly
   (runner-asserted).
3. **Full coverage**: teacher-forced steps cover every generated token (per-step records
   retained; 128-token cap, EOS or cap).
4. **Same basis**: both arms read the same U from the same template-attenuation fit; the fit is
   computed once per run from clean forwards.

If the composed recurrence breaks any invariant (e.g. prefill equality fails, or histories
diverge), I diagnose and report rather than silently changing the method.

## Conditions

Six development pairs (naming/legs/property-mammal × dog/ant; property-mammal-ant's expected
answer corrected to No -- the clean donor itself answers "1. No, it is not a mammal"), two arms
× {C=0, C=1.5} = 24 cells in one model load via --batch-spec. Reference: the retained fixed-L20
span-corrected candidate (a different equation: template-mean Δ with norm matching), reported
alongside from the replay; not asserted equal. Property-mammal-ant is a fact-preserving no-op
question (No -> No) and is labeled as such.

## Judgments (separate, full continuations)

Literal animal identity through the continuation; the numeric/yes-no answer; coherence
(self-contradiction, invented anatomy, repetition); formatting separately. The dog decision
pair confound (a decision-position token in the pair) does not arise here -- no pair selection
is involved; the donor direction is the full L20 attenuation span. No causal claim from a digit
alone; no claim that a null proves the detector inert.
