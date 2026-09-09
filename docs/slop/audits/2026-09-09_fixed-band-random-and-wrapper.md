# Fixed-band transfer, random controls, and wrapper audit

Scope: completed pueue jobs 767--779. This is an audit, not a success claim.

## Provenance

All eleven jobs returned `Success` in the earlier `pueue status --json` check.
Correction, PI/OpenAI: my initial empty-stdout statement was false. I had read pueue's
metadata display, not the redirected output. I have now read all eleven saved logs:
job 769 has 25 lines/1950 bytes, including loading, the condition table, and
`wrote out/2026-09-08_134000_fixed-band-dog-name/run.md`.
The complete copies are in [saved job logs](../../../slop/audits/2026-09-09_job-logs/).
Full generated text remains in each `result.json`, not these stdout summaries.

All persisted conditions identify Qwen/Qwen3.5-4B revision
`851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, with source state
`v0.1.1-332-ga49e4cf-dirty` and hashes for the six executed modules. The recovery check
compared the six stored hashes in the fixed leg and naming runs with `git show a49e4cf:<module>`:
all match. The dirty label alone does not invalidate executable provenance. Older
local/synchronized runs have different hashes and still need historical source recovery.
See [recovered references](../../../slop/audits/2026-09-09_recovered-references.md).

The fixed configuration is raw rank-four contrast-energy attenuation at layers 22, 23,
and 24, C=2, no component or residual norm restoration. It patches the final three
prompt positions and every cached decode step, while a donor cache consumes the
source-selected tokens. The complete construction is summarized in
[`docs/pseudocode/2026-09-09_synchronized_attenuation_replacement.py`](../pseudocode/2026-09-09_synchronized_attenuation_replacement.py).

## Judgment corrections

PI/OpenAI: judge complete semantic answers, not an exact initial spelling. Job 773's
ant continuation says `a pair of antennae used for sensing the environment`; it answers
the property question despite starting `1.`. Both user-message donors correctly answer
in prose although `first_answer` is null. Job 768 maintains dog identity but claims
`two of which are used for running and jumping while the other two support their weight`;
that is a factual defect, so it is not an unqualified coherent-description pass.
The naming corrections and unchanged dog-mammal output remain failures.

The hypotheses and proposed donor-own-token test below are initial agent suggestions,
not a completed independent review or a selected experiment. That test changes token
histories and may destroy semantic alignment. The approved plan instead requires broad
first-principles brainstorming and historical comparisons before choosing a family.
The reviewer timed out after 1200000ms; its partial trace contains reads, not a final verdict.

## Stage table

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| job 767 full-state transport readout | test whether selected-component transport omitted ant readout information | coherent ant leg output, but both source and donor delayed readouts remain labelled unvalidated | unclear | [condition log](../../out/2026-09-08_133700_full-state-transport-ant/conditions/001_synchronized_transport_L24_C2/run.md) | validated clean readout | no readout claim |
| jobs 768 and 771 fixed leg transfer | dog/ant donor answer plus coherent identity through EOS | `4`/dog and `6`/ant, with no repeated bigrams | yes | [dog](../../out/2026-09-08_134000_fixed-band-dog-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md), [ant](../../out/2026-09-08_134000_fixed-band-ant-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | independent prompts | two development demonstrations only |
| jobs 769 and 772 fixed naming transfer | donor animal name persists | both begin with the donor name, then explicitly correct to spider | no | [dog](../../out/2026-09-08_134000_fixed-band-dog-name/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181), [ant](../../out/2026-09-08_134000_fixed-band-ant-name/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181) | time-to-correction / state alignment measure | coherent transfer does not generalize to naming |
| jobs 770 and 773 fixed properties | dog mammal and ant antennae answers transfer | dog remains `No`/spider; ant produces an ant description but not the expected explicit `Yes` answer | no / partial | [dog](../../out/2026-09-08_134000_fixed-band-dog-property/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L180), [ant](../../out/2026-09-08_134000_fixed-band-ant-property/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181) | answer parser for this response format | no common property transfer claim |
| jobs 775 and 776 matched random spans | random rank-four spans, matched at each position, should distinguish generic digit movement from selected semantics | several random spans move log odds and digits, but all random target-digit continuations remain spider | no for digit specificity; yes for the narrower continuation contrast | [dog sweep](../../out/2026-09-08_134200_matched-random-band-dog/run.md#L16), [ant sweep](../../out/2026-09-08_134200_matched-random-band-ant/run.md#L16) | preregistered semantic evaluator and larger random denominator | first-token swap is not selective evidence |
| jobs 778 and 779 repaired user-message boundary | valid clean controls and a meaningful intervention test | clean source/donor prose is correct; steered output stays spider with swaps -0.000 and +0.125 nats | clean yes; transfer no | [dog](../../out/2026-09-08_151650_user-boundary-dog-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181), [ant](../../out/2026-09-08_151650_user-boundary-ant-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181) | semantic answer token position | method depends on assistant-prefilled digit format |
| persistence and artifact storage | 3 prefill positions plus N-1 decode edits; result and per-condition logs | condition logs state continuous steering and result JSON retains traces, 32-token previews, and full continuations | yes | [runner](../../scripts/oat_sweep.py#L913), [hook](../../scripts/demo.py#L181) | compact coverage assertion in the result frontmatter | no evidence of a prompt-only accidental control |

## Primary observations

The comparison has direct, byte-preserved outputs. The dog legs intervention says:

> `4\n\nThe animal you are likely thinking of is the dog, which is a popular domestic pet known for its loyalty and friendly demeanor. Dogs typically have four legs`

Source: [`dog legs run.md:181-186`](../../out/2026-09-08_134000_fixed-band-dog-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181). This is a condition log generated by the runner from persisted model token IDs.

The ant legs intervention says:

> `6\n\nThe animal is an ant, a small insect known for its six legs and distinct body segments. Despite their tiny size, ants are incredibly strong and can`

Source: [`ant legs run.md:181-186`](../../out/2026-09-08_134000_fixed-band-ant-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181). This is the corresponding primary condition log.

The generalization failure is explicit rather than inferred from a score. The dog naming
output begins with Dog, then says:

> `Wait, that is incorrect. The animal that spins webs is a **spider**.`

Source: [`dog naming run.md:181-186`](../../out/2026-09-08_134000_fixed-band-dog-name/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L181). The ant naming run contains the same correction with "called a **spider**" at the matching location.

The dog property condition is a direct unchanged source answer:

> `No.\n\nThe animal that spins webs is a spider, which belongs to the class Arachnida rather than the class Mammalia.`

Source: [`dog property run.md:180-185`](../../out/2026-09-08_134000_fixed-band-dog-property/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L180).

The random sweep is not quiet. Three random dog spans have swap shifts `+8.688`, `+6.125`,
and `+5.750` nats and first token `4`, compared with `+4.375` for the selected row
([dog random table:18-21](../../out/2026-09-08_134200_matched-random-band-dog/run.md#L18)).
Reading each full continuation in `result.json` shows those three remain spider
continuations. One random ant span has first token `6` and `+5.375`, slightly higher than
the selected span's `+5.250`; it also remains a spider continuation
([ant random table:18-19](../../out/2026-09-08_134200_matched-random-band-ant/run.md#L18)).

The repaired user-message run removes the prior invalid-control concern but is a negative
transfer result. It records a correct dog donor statement, "has four legs", then the
intervened source remains "the spider, has eight legs" ([dog wrapper run.md:114,181-184](../../out/2026-09-08_151650_user-boundary-dog-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md#L114)). The ant analogue has its correct clean donor and the same unchanged spider output.

Finally, the readout cannot carry any semantic inference. Every selected run says
`computed; semantic validity not established`, and the displayed tokens include unrelated
multilingual fragments rather than a clean source/donor separation. The full-state
transport condition 767 also retains that status.

## Hypotheses

### H1 [method | Likely | 70%]

- **Mechanism:** The band can force the immediate digit-state trajectory in the
  assistant-prefilled legs format, but it does not replace the source animal representation
  strongly enough to survive an identity-conflict question.
- **Evidence:** The same fixed setting produces two animal-consistent legs continuations,
  while both naming generations state, `Wait, that is incorrect. The animal that spins webs
  is ... spider.` The contrast is within fixed settings, not across a retuned strength.
- **Contrary evidence:** The ant antenna property produces an ant description, so the
  method sometimes transfers more than an immediate digit.
- **Discriminating test:** Keep the selected U and C fixed; change only donor cache
  conditioning from source-selected tokens to its own donor-selected tokens after prefill.
  If H1 is right, this should reduce or delay the naming correction while retaining dog/ant
  identity. If source-token synchrony is essential, it should degrade both legs and names.
- **Fix/action:** Add one explicit `donor_conditioning` axis and run a paired dog/ant naming
  comparison with unchanged wrapper, U, C, and prompt positions.
- **Interpretability:** partial. It supports a format-specific behavioral intervention, not
  reliable concept replacement.

### H2 [measurement | Likely | 65%]

- **Mechanism:** `swap_log_odds_shift` measures digit movement rather than coherent target
  computation.
- **Evidence:** A random dog span achieves `+8.688` nats and `p(4)=0.9604`, larger than the
  selected condition's `+4.375`, but its complete continuation says spider. The ant random
  seed 1 similarly exceeds the selected log-odds shift while remaining spider.
- **Contrary evidence:** Neither the coherent selected output nor the random output is scored
  by an independent semantic evaluator, so the apparent continuation distinction is manual
  inspection of only this small set.
- **Discriminating test:** Define a deterministic continuation rubric before further tuning:
  target identity must be present, source identity absent, expected target property present,
  and no explicit correction. Score all existing 18 random/selected continuations and every
  future run.
- **Fix/action:** Retain log odds as a local diagnostic, but make the rubric and full
  continuation the acceptance measure.
- **Interpretability:** yes for the digit statistic; no for digit statistic as semantic transfer.

### H3 [method | Likely | 60%]

- **Mechanism:** The intervention is aligned to an assistant-prefilled immediate answer token.
  In the repaired user template, the first generated token is natural-language `The`; the
  leg answer appears later, so the same final-three-position, same-layer intervention is not
  acting at an equivalent answer state.
- **Evidence:** Jobs 778/779 have correct clean source and donor prose but no behavioral
  movement, whereas jobs 768/771 begin directly with `4`/`6`.
- **Contrary evidence:** The continuous decode hook still patches every step, so position
  alone cannot explain all of the lack of effect.
- **Discriminating test:** On the valid user-message path, add an answer-first constrained
  template that makes `4`/`6` the first token without moving the question to assistant text.
  The current method predicts a recovered effect; H1 predicts later correction or no target
  identity despite the digit.
- **Fix/action:** Do not call jobs 778/779 a code regression. Treat them as a phase-alignment
  test and log where the first answer token occurs.
- **Interpretability:** yes for this wrapper-specific negative result.

### H4 [measurement | Highly likely | 85%]

- **Mechanism:** The delayed lexical detector is not a validated measurement of hidden animal
  state and its post-edit movement is entangled with the construction.
- **Evidence:** The logs themselves state `semantic validity not established`; source/donor
  readouts show unrelated fragments, and job 767 did not repair that limitation.
- **Contrary evidence:** The original spider public example used readable vocabulary, so this
  detector can be readable under another construction.
- **Discriminating test:** Evaluate a frozen readout on clean spider/dog/ant prompts and
  separate held-out templates before using it after an intervention.
- **Fix/action:** Keep the field labelled unvalidated and exclude it from method success.
- **Interpretability:** no for readout semantics; yes for it being a captured numerical output.

### H5 [bug | Unlikely | 30%]

- **Mechanism:** A cache, hook, or random-control implementation error creates the observed
  success/failure pattern.
- **Evidence:** The synchronized runner maintains separate source/donor caches and asserts
  equal source-token histories. The random operation computes a random projection of the
  current donor-minus-source state and rescales it to the semantic edit norm
  ([`scripts/demo.py:181-252`](../../scripts/demo.py#L181)). The result records continuous
  per-layer traces.
- **Contrary evidence:** These are implementation assertions, not a complete reference
  implementation comparison; the provenance is dirty.
- **Discriminating test:** Add a tiny deterministic cache trace test where `source` and
  `donor` token histories and every hook position are compared against a manual one-step
  forward calculation, then run the actual user-message condition once.
- **Fix/action:** Add that test only if the donor-conditioning comparison does not explain
  the naming failure; it is lower information gain than H1's experiment.
- **Interpretability:** partial pending the test.

## Decision

1. **Resolve-condition verdict:** jobs 768--773 asked to "validate common L22-24 C2" and
   resolve with "correct clean controls and consistent transfer on plain questions." **Not
   met.** The clean assistant-prefilled controls are good, but two naming failures and dog
   property identity establish non-consistency. Jobs 778--779's narrower clean-control
   condition is **met**, while their transfer condition is **not met**. Jobs 775--776's
   norm-matching condition is **met** as an implementation record, but it rejects the
   interpretation that a digit swap is selective.
2. **Prediction check:** no pre-run predictions beyond pueue `why/resolve` labels were
   recorded. Future runs need an explicit prediction and rejection condition in `run.md`.
3. **Earliest unsupported link:** `selected attenuation span -> replaces a source animal
   representation`. The full continuations and random controls do not support it. A
   nonselected independent target identity rubric across held-out questions would.
4. **Validity:** define invalid as a broken intervention, missing control, or an output that
   cannot be traced to the stated configuration. I estimate `P(invalid) ≈ 0.25--0.40` for
   the narrow behavior records because provenance is dirty and no independent cache trace was
   rerun, but the coherent legs and explicit failures are credible observations. Overall
   scientific classification: **inconclusive**, not a credible general positive.
5. **Three highest-information clues:** (a) both name conditions self-correct, which directly
   rejects persistent identity transfer; (b) random spans exceed the selected digit effect
   while remaining spider, which separates digit movement from coherence; (c) valid user-role
   clean controls retain no transfer, which rejects the earlier wrapper explanation.
6. **Missing metrics, ordered:** deterministic continuation rubric; answer-token offset under
   each template; a frozen clean readout calibration; independent held-out questions; a
   reference cache/hook trace.
7. **Bugs requiring code changes:** none localized. Add cache trace instrumentation only if
   the donor-conditioning experiment cannot explain the failure.
8. **Misconceptions requiring reinterpretation:** `swap_log_odds_shift`, `bare_answer_mass`,
   and a correct first digit cannot be described as reliable animal replacement. The leg
   demonstrations are development-selected behavioral examples.
9. **What would change the verdict:** coherent dog and ant identity on naming and property
   questions under a fixed setting, surpassing a predeclared random control rubric, would
   materially increase confidence. Another correction loop after donor-own-token conditioning
   would lower confidence that cache alignment is the key limitation.
10. **Revised sequence:** reproduce earlier local dog naming and synchronized ant cases,
    comparing exact original prompts before calling later failures regressions. Use the
    recovered evidence in a bounded MoA brainstorm, then choose a small discriminating
    experiment. Preserve full continuations and judge meaning, including factual defects.
    Donor-own-token conditioning is only one candidate and is not selected.

-- Codex/GPT-6
