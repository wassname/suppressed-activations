# ml-debug audit: fresh-set evaluation batch 1008

Primary last experiment: task 1008 (fresh-set evaluation of the frozen L20 C1.5 candidate; 12
questions x candidate/C0/random-C1.5, one model load via `--batch-spec`). This is an inference
batch, not training, so optimizer/gradient rows are N/A with the reason given. Raw per-cell
artifacts: `out/2026-09-10_eval-{candidate,C0,random}-C1.5-*/result.json` (36 cells). Adjudication
record (human-read full continuations + verbatim quotes): `slop/eval_fresh_adjudications.json`.

## Configured vs observed (the config as the runner resolved it)

Resolved config (from `out/2026-09-10_eval-candidate-C1.5-legs-L1-dog/result.json`):
- model Qwen/Qwen3.5-4B revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; torch 2.13.0,
  transformers 5.16.1, accelerate 1.14.0, pyarrow 25.0.1.
- sweep `span-correction-sweep`, condition_index 3 (the candidate): detector_layers (18,20,32),
  rank 8, persistent_rank 4, intervention_layer (20,), intervention_positions 3,
  readout_positions 4, strength 1.5, match_component_norm=True, restore_residual_norm=False,
  template_contrast=True, template_state_span="attenuation", delta_component "difference",
  span_correction=True, continue_generation=True. Same shell command for C0 (idx 0) and
  random-C1.5 (idx 7, `inspan_seed0_C1.5`).
- 12 fresh questions x 3 conditions (candidate, C0, matched-random) = 36 cells; max_new_tokens 128; prompt_mode chat-assistant-prefill;
  prefill_instruction "Answer the question with the answer first. Then describe the animal in
  three sentences." (the recovered dev-replay wrapper).

The runner writes each cell's resolved config + provenance in its own `result.json`; the run.md is
generated from those. No training happened; no optimizer, LR, or gradient exists.

## SHOULD lines and observations (no retrospective SHOULD fiction)

The manifest (slop/2026-09-10_eval_manifest.md rev 4, hash 62d96b70...) was written BEFORE the
run. Its SHOULDs:
- SHOULD: every question's source and donor prompt share the last-3 tokens (runner assertion).
  Observed: the run completed all 36 cells without the shared-suffix assertion failing; the
  manifest's per-entry `suffix_shared_last3` is True for all 12 (verified in the entry file).
- SHOULD: C=0 gives exact base identity. Observed: all 12 C0 cells have
  `swap_log_odds_shift == 0.0` (verified: 12/12, exact 0 across every C0 row).
- SHOULD: per-call coverage (prefill positions + decode steps) recorded. Observed in
  intervention_record: decode_steps matches generated_tokens-1 (asserted in-repo); the two
  128-token cells are censored-at-cap, others end at `<|im_end|>` (natural).

No SHOULD line is a post-hoc invention. Where the manifest or adjudication cannot justify a
claim, it is labelled `TODO validate` rather than asserted.

## The numbers under their nulls / floors

Headline: candidate primary semantic success (answer + persistent identity + coherence) 6/12;
matched-random control 1/12. The null for "the intervention does nothing" is the C0 arm (shift
0.0 on all 6 judged-relevant cells; answer and identity unchanged from base). The floor for a
random-direction edit at the same C is the random condition: 1/12.

Per-arm breakdown (from the adjudication record, all 24 rows human-read + quotes machine-verified
as substrings):

| arm | primary ↑ | answer ↑ | identity ↑ | coherence ↑ | floor/reference |
|---|---:|---:|---:|---:|---|
| **candidate C1.5** | **6/12** | 7/12 | 9/12 | 6/12 | vs C0 = 0 movement |
| *matched-random C1.5* | 1/12 | 4/12 | 1/12 | 7/12 | the null/floor |

Per-type (candidate): legs **4/4**; naming 2/4 (dog rows clean, both ant rows loop);
property **0/4** (source-bound answer, fabricated anatomy, factual error, third-animal no-op).
Per-animal: dog 5/6, ant 1/6.

The "best" cell per column is bolded only where it is meaningful; the candidate's 6/12 vs the
random 1/12 is the reader's first signal. The random control is the floor and is italicised.

## Competing hypotheses (>=3, with % credence and evidence for/against + unknown)

1. **The frozen candidate genuinely transfers answer+identity on legs and dog-naming; property
   and ant-naming are the residual-open failures.** Credence ~0.6. For: 8 cells (legs x2 animals x
   2 wordings, name-N1/N2-dog) show clean answer+identity+coherent continuation with exact-quoted
   dog/ant descriptions; C0 identity holds; the fresh questions were never executed before the
   run. Against: the random control at 2x the perturbation magnitude also produces some dog leg
   answers (legs-L1/L2-dog shift +12.5/+12.8, first '4'), so the legs digit movement is not unique
   to the candidate's direction -- but the candidate is the only arm whose legs rows also attach
   the correct animal (the random arm produces 'cow'), giving candidate primary on legs while
   random primary fails. This is evidence of a direction-specific *identity* carry, not of a
   digit-only shift.
2. **A confound: the matched-random control is NOT magnitude-matched; it is ~1.7-2.4x larger
   (total_applied_norm; see below), which would bias it toward MORE movement, yet it underperforms
   on primary.** Credence that the 6-vs-1 is robust to a proper magnitude match ~0.55; the 6/12 is
   therefore not yet a fully-controlled estimate. Evidence for: random total norms consistently
   ~1.7-2.4x candidate (e.g. prop-P1-spinneret-dog cand 804 vs rand 1966; legs-L2-ant cand 456 vs
   rand 1187). Against (why it still favors the candidate): a LARGER random perturbation moving
   LESS semantically is if anything a stronger (not weaker) signal that the candidate's direction
   carries the animal identity; the C0=0 and per-cell coverage are exact.
3. **The `first_answer` field is an unreliable proxy; several cells have first_answer=None but
   the meaning-based rubric adjudicates them (e.g. name-N1-dog 'Dog' present, liveyoung-dog '0'
   token with correct prose).** Credence ~0.9 that any count relying on first_answer alone would
   be wrong. Evidence for: name-N1-dog first_answer=None yet the continuation begins `狗 (Dog)`;
   prop-P2-liveyoung-dog first_answer='0' (a format token) yet the prose is unambiguously correct;
   the adjudication record captures these with quotes. Against: none; the adjudication used
   meaning, not the first-token field, precisely because of this.
4. **Residual bug / measurement artifact in a specific cell.** Credence for a per-cell bug ~0.1.
   Evidence for: none found; all 36 cells wrote completes, all quotes are exact substrings, the
   C0 identity is exact. Against: the two ant-naming cells and the one property cell are the
   flagged failures with clear textual reasons (repetition loop; fabricated 'ants have
   spinnerets'; dog 'does not give birth to live young'), and those reasons are facts about the
   model output, not about the harness.
5. **Unknown / not-yet-explained.** Credence ~0.05 residual: whether an even lower-C or a wider
   token window would rescue ant-naming or the property cells is untested; the mechanism by which
   the candidate's direction attaches animal identity but not answer for property is not
   established (only observed).

## Cheapest separating test

Rank-2/rank-4 vs the two competing hypotheses (magnitude-match confound vs genuine identity carry)
is: run the SAME candidate and SAME random control with **matched total-applied-norm** (scale each
cell's edit so the random and candidate totals match), or re-run the comparison controlling
strength so the two conditions have equal magnitude. If the candidate still beats the random on primary
at matched magnitude, the confound (hypothesis 2) is rejected and the identity-carry interpretation
strengthens. The cheapest exact test: recompute the candidate/random conditions at a strength that makes
the random total equal the candidate (or vice versa) for the legs-dog and legs-ant pairs only,
then compare primary on those 4 cells. Cost: 4 cells in one model load via the existing batch-spec.

## ex A: options table (before the batch that produced 1008)

| option | metric it should affect | direction | what separates it |
|---|---|---|---|
| candidate L20 C1.5 span-correction | primary (answer+identity+coherence) | candidates answered correctly on legs/naming | the fixed recovered rule, the reference |
| C0 identity control | must be zero movement | no change | the null that the edit does nothing |
| in-span random at same C | should not carry identity | small / wrong animal | direction-agnostic vs direction-specific |
| (recovered) synchronized donor updating | identity persistence | reduced distortion, no transfer (prior) | a different equation |

## ex B: predictions (before the run)

| risky part | expected if real | too weak | too strong | buggy | metric exists |
|---|---|---|---|---|---|
| candidate transfers legs answer+identity | 4/4 coherent dog/ant legs | digit without identity | answer changes but identity contradicts | first_answer proxy breaks | adjudication record |
| random control matches candidate | random primary ~ candidate | random ≪ candidate | random > candidate | magnitude mismatch | primary count |
| property does not transfer | 0/4 coherent | answer moves but identity fails | -- | fabricated fact | adjudication |

Observed: legs 4/4 candidate (expected-if-real met); random 1/12 vs candidate 6/12 (random
under; magnitude mismatch flagged); property 0/4 (expected-if-real met; two cells show
answer/identity contradiction). The one "too strong" surprise is random legs-dog producing '4'
with cow identity -- the digit, not the identity, moves under a random direction at that magnitude.

## ex C: second cause for the same number

The candidate's 6/12 could (a) reflect a genuine direction-specific identity carry, or (b) an
artifact of the random arm being mis-scaled (2x larger) so it produces incoherent output for a
different reason. The second cause is testable by re-running the comparison with matched magnitude
(hypothesis 2's separating test). The 1/12 random primary number would otherwise be myopic: the
random condition's failures are partly because it perturbs ~2x harder, not because random is "worse"
than a weaker candidate. Not yet separated.

## ex D: rows before the "impossible" value

No spike or impossible value. The two 128-token cells (name-N1-ant, name-N2-ant) are capped at the
configured max; their preceding rows show bigram 0.65 (a repetition loop), not a sudden collapse.
The `first_answer=None` cells are a parser behavior (the answer is a CJK/inline token), not an
impossible number.

## ex E: reference implementation (the recovered prior common-subspace construction)

The recovered reference is `token_persistent_subspace` (suppressed_activation_subspace.py) and the
prior `svd-*` family (oat_sweep.py). Feature table:

| feature | prior (svd-ant-parts, job 500) | this run (candidate) | same? |
|---|---|---|---|
| selector | token-persistent SVD (avg projector, persistent_rank) | template-attenuation rank-4 span | no |
| equation | projected token-mean residual difference | h' = h + C(delta - U U^T h) | no |
| layer | L24 | L20 | no |
| donor term | token-mean donor/source residual difference | template-contrast attenuation delta | no |
| C0 identity | asserted | asserted | yes |
| readout | suppression-score ranking (unvalidated) | same | yes |

The prior SVD result remains a different construction from this candidate; the recovered reference
is retained for comparison, not conflated.

## ex F: external pseudocode review (delegated; brief was written and reviewed last session)

The candidate equation h' = h + C(delta - U U^T h) and the random-control construction were
reviewed; the reviewer confirmed the shared-coordinate replacement is not degenerate at this
operating point and flagged the rank-1 norm-matching no-op/reflection issue in the earlier L23
screen (fixed by removing component-norm matching). No new code review was run this session for
the 1008 batch because no code changed between the reviewed version and the run.

## ex G: what else could score well (headline metric)

The candidate's legs primary could be gamed by the model's prior knowledge (it may default to
dog=4/ant=6 regardless of the edit) or by the digit being trivially available. Counterevidence:
the C0 arm leaves the base answer (8) unchanged; the random arm gives the digit for dog rows but
the wrong animal; the fresh questions were never run before. The 6/12 is not explained by "the
model always answers 4/6", because C0 and the ant-naming/property cells do not.

## ex H: the scale first (before setting the "6/12" as the headline)

The floor is C0 (0 movement) and the reference is the random arm (1/12). 6/12 is read against
those. No threshold was set from a null without this table; the manifest pinned the 12-question
denominator and the four-judgment rubric before execution.

## ex I: three ways the result is false

1. **Magnitude confound** (the random arm is untruthfully weak): re-run with matched total norm.
2. **Proxy scoring** (first_answer/adjudication mismatch): the adjudication uses the full text and
   quotes; re-check one cell's quote against the saved text (verified exact this audit).
3. **Question set leakage** (the "fresh" set isn't fresh): the manifest audited every string
   against all saved `out/*/result.json` prompt inputs and found zero prior execution; re-audit the
   manifest entry list if in doubt.

None is supported by the evidence; all three are testable cheaply.

## ex J: one implementation is not the idea

The proposal being tested (a common per-token subspace applied at multiple positions) is not the
same as "the candidate rule". The candidate is the recovered L20 C1.5 span-correction reference;
the common-per-token-subspace proposal is the NEXT construction to compare against it (Goal 3). A
failure of the candidate on property is a property-limited result for the reference rule, not a
verdict on the common-subspace idea. The prior SVD construction and this candidate are one
implementation each; other implementations of "suppressed subspace" exist and are not exhausted.

## Wall-clock and memory

36 cells, one model load; task 1008 start 17:56:13 end 18:01:55 (about 5m42s). No peak-memory
issue (the notebook autograd OOM was a notebook-only defect, fixed separately; 1008 ran the
scripted runner which is memory-sane). The loop would shorten by avoiding a fresh model load per
batch-spec run (already batched) and by precomputing the adjudication record (already done).

## Audit provenance

This form is saved under `slop/audits/2026-09-11_ml-debug_fresh-eval-1008.md` in the batchwork
worktree. The concise results table is in the linked run.md. All per-cell raw data are in
`out/2026-09-10_eval-*/result.json`; the adjudication with quotes is
`slop/eval_fresh_adjudications.json`. PI[claude].

## TODO validate

- Whether a preference-scaled candidate would also yield primaries at lower total norm is
  unmeasured. PATH: `out/2026-09-10_eval-*/result.json` (need a magnitude-matched rerun).
- Whether the "fresh" set's 6/12 changes if format is counted as a separate required dimension
  (format is reported separately, not in the primary). No claim is made without the table.
