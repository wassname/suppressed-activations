# Next experiment: frozen readout on eight native-chat v4 probes

**Recommend option 1:** test all eight known non-geography v4 probes with one uniform native-chat transformation. This directly tests whether the frozen readout’s useful geography behaviour extends across domains while producing inspectable answers. It is not unseen-concept evaluation or causal proof.

## Evidence and choice

The supplied `slop/reviews/2026-10-01_input-prefix-result-review.md` reports:

> “0/4 confirmed clean joint passes, with an unresolved bound of 0–2/4”

Yet J recovers Oman/Qatar identities **2/4**, versus **0/4** for either plain control; all four native-chat answers are correct. Preserve both observations: identifiable hidden candidates and incomplete exclusion.

`data/english_hidden_words_v4.json` supplies eight fixed non-geography probes. Their earlier completion result—J **3/8**, plain27 **6/8**, with NLI continuations—makes them useful for testing a different prompt frame, not an untouched benchmark.

| Option | What it tests | Decision |
|---|---|---|
| Eight native-chat v4 probes | Cross-domain readout behaviour and answer coherence | **Run next** |
| Four new geography same-answer pairs | Additional transfer within the successful domain | Defer; less direct evidence about the observed domain restriction |
| Reserved v5 | New matched-output contrasts | Keep reserved; its prospective gate has not passed |

The indirect-donor review reports no intended initial-answer changes for the candidate (**0/2**). Its literal-control skeleton change remains a separate partial positive. Neither motivates another causal parameter rescue here.

## Exact frozen design

I asked the supervisor whether to retain the complete 2686 configuration while changing only the probe/frame. Reply:

> “Freeze exact2686 readout/masks/layer/k/dtype (including knownovermask), noadditionalfilter.”

For each v4 case, in its existing order:

- User content is exactly `'Complete the fact with only the missing word or phrase:\n' + original_v4_case['prompt']`.
- Preserve the original prompt bytes, including its lack of trailing space.
- Omit the dataset’s Japan/Tokyo demonstration entirely.
- Render one user message using the pinned tokenizer’s native `apply_chat_template`, `enable_thinking=False`, `add_generation_prompt=True`.
- No system message, examples, case-specific instructions, or label-derived additions.
- Generate greedily once per case: **eight generations, at most 32 new tokens each**, EOS union **248044/248046**.

Capture readouts from those same trajectories, at the existing final-prefill position. Freeze J24, half-erasure, greedy-next-token mask1, k32, precision and all 2686 masking rules. Retain the old mask plus the existing complete-input-word prefix expansion, including known overmasking; no stemming, synonym additions, or answer-dependent filtering.

## Matched controls and measurements

On the identical captured states and rendered inputs, report:

1. Primary half-erased J24.
2. Equally processed half-erased plain24 and plain27.
3. Mask-only J24, retaining every other rule.

These are readout comparisons, not additional generations. Actual generated text is evaluation evidence only, never a new readout mask.

For every case retain exact rendered input, generated IDs/text, actual token count, all top32 lists, hidden ranks, mask exclusions and their originating words. Report:

- Correctness and coherent completion separately from hidden recovery.
- Frozen lexical joint scores over **all eight**, plus explicitly labelled answer-correct subsets.
- Clear hidden identity, definite input leaks, definite said leaks, and unresolved entries separately.
- The unchanged strict full-list clean-joint criterion and ambiguity bounds, without treating universal multilingual purity as a user-imposed gate.
- AUROC with masked-label/undefined-case qualifications; it cannot substitute for identity recovery.
- Paired per-case gains/losses against both plain controls.

Show one actual example using a declared selection rule—first clear primary identity recovery in dataset order, otherwise first case—and its fixed-set denominator. Do not hide failures.

## Diagnostic interpretation

- **Coherent answers plus J-specific identity recovery:** motivates a new cross-domain same-answer-pair test, subject to its prospective contract.
- **Coherent answers but plain ties/wins or J misses:** argues against blaming completion framing alone; next investigate a distinct representation hypothesis, not mask/layer/dose tuning.
- **Identity recovery with leaks:** retain the bounded positive example and exclusion failures; do not promote it to clean success.
- **NLI continuation, wrong answers or truncation:** the new frame has not supplied the intended behavioural assay; preserve all eight before selecting another task design.

Historical improvement would not isolate chat: the old demonstration disappears and prefix masking differs from old v4. Within-run matched controls are the valid comparison.

No experiment was executed. Primary neural logs, runtime and independent replication were not supplied; recommendations rely on the scoped records. Hidden-label recovery also cannot establish that an intermediate was necessary.

— **PI/OpenAI**