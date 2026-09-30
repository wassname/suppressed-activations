# Next small test: complete-input-prefix exclusion

Agreed with the supervisor after two exchanges. Recommend **one cached readout experiment**, not another causal variant. Nothing was executed, edited, or queued.

## Why this test

Observed evidence separates three problems:

- **Useful identity information:** the frozen half-erased J readout returns Oman and Qatar, each above its same-answer partner; equally processed plain controls miss both. The earlier reviewed **7/16 geography successes remain evidence for the old method**, not this proposed change.
- **Incomplete exclusion:** `out/2026-10-01_060504_jlens-one-pass/case_comparison.md` shows `continents` and `continental` despite input `continent`. The prior semantic review reports **0/4 clean joint passes**, not absence of identity information.
- **Measurement limitations:** Namibia loses six prefix labels through input `name`; Botswana is also missed without that exclusion. These observations do not establish that either country is absent from the representation.

The responsible code is `scripts/english/01_detector_baselines_and_pair_transfer.py`, `prompt_word_mask`:

> `prefixes = {w[:i] for w in words for i in range(3, len(w) + 1)}`  
> `bool(v) and (v in words or v in prefixes)`

It excludes prefixes **of** input words, but not vocabulary strings extending those complete words.

Latest causal evidence does not justify another VJP setting. `out/2026-10-01_063917_vjp-intervention/run.md` retains first answers **4/inside**, versus intended **8/outside**: **0/2 property transfers**, with arithmetic preserved. Reported property log-odds shifts match random. Preparation records:

> `"delta_norm": 0.03598912060260773`  
> `"natural_donor_norm": 1.4303362369537354`  
> `"projection_fraction": 0.025161301717162132`

Small scale and transfer mismatch remain competing explanations—not permission for sign/dose rescue, and not evidence that all gradient methods fail.

## Options compared

| Option | Intended benefit | Decision |
|---|---|---|
| Complete-input-prefix exclusion | Remove an observed class of input repeats without changing representation | **Test once** |
| Input-direction removal | Suppress related input content geometrically | Defer: script04 already explores input erasure; shared directions may erase legitimately hidden translated equivalents |
| Read at the structural end of the user message | Avoid reading only after the empty thinking/template suffix | Defer: plausible location hypothesis, not observed cause; would need fresh states and must not become another pooling/window search |

The chosen option addresses a demonstrated defect. It is a **new lexical filtering method**, not retrospective correction of the old result or a semantic guarantee.

## Frozen recipe

Use `scripts/english/08_jlens_one_pass.py` and the saved states from:

`out/2026-10-01_060504_jlens-one-pass`

Keep the original prompt mask. Additionally exclude vocabulary entry \(v\) when its existing normalized string starts with an **entire** regex-extracted, lowercased prompt word \(w\), with \(|w|\ge3\).

- Use the full rendered prompt and existing normalization.
- Expand from complete words, never token fragments or generated prefixes.
- No language identification, stemmer, synonym table, hidden labels, answer labels, or generated text enters the mask.
- Log every newly excluded token and all originating complete words.
- Preserve the existing output mask, half-erasure, J24, final-prefill position, k32, dtype, ranking and labels.

This removes `continent→continents/continental`. It also permits unwanted exclusions such as `art→article`: **complete-word anchoring is not semantic safety**. Preserve that counterexample explicitly. Keeping the original mask also preserves the disclosed `name→nam` problem.

### Comparisons and budget

One local default-queue job, initially **300 seconds**, using cached states:

- **Zero transformer forwards and zero generations.**
- Reproduce all **72 original rows exactly**.
- Add **16 candidate rows**: four cases × half-J, half-plain24, half-plain27 and mask-only J.
- Primary remains half-J; do not substitute a winning control.
- Refill top32 from the full vocabulary after masking, rather than merely deleting entries from saved lists.

Implementation checks should exercise complete-word anchoring, case/space normalization, short-word exclusion from expansion, retained legacy masking, the deliberate `art→article` overmask, and unchanged scores for surviving tokens. These checks have **not** been run.

## Predictions and interpretation

| Prediction | Distinguishing observation |
|---|---|
| Direct masking effect | All `continent`-extending entries disappear; surviving token scores stay unchanged |
| Existing identity evidence survives | Oman and Qatar remain returned by half-J and retain own-country-over-partner ordering |
| Masking alone is insufficient | Replacement entries or untranslated input equivalents leave some/all lists semantically unclean |
| African failures persist | Neither Namibia nor Botswana becomes a clearly identified country; no fragment promotion |
| Implementation defect | Old-row parity fails, surviving scores change, or exclusions lack a qualifying complete input word |

The unchanged scores and exclusion provenance distinguish this filtering mechanism from improved representation. Clear African recovery would contradict the corresponding prediction, but ambiguous `nam`/`Bot` pieces would not.

Review every replacement entry symmetrically across candidate and control lists. Report separately:

1. Clear identity recovery **/4**.
2. Lexical joint passes **/4**.
3. Reviewed input exclusion, output exclusion and clean joint passes **/4**.
4. Clean discriminating pairs **/2**, retaining the original paired-rank requirements.
5. Newly excluded entries, potential overmasking and unresolved semantic ambiguities.

Do not use the postmask AUROC near **0.893** as evidence of meaningful ranking. The source computes AUROC after masking negatives to `-inf`; finite hidden labels can beat them despite very poor vocabulary ranks. Preserve the metric with that limitation rather than selecting by it. Empty `input_hits` also remains uninformative here: input labels are populated only when a case supplies `input_word`.

## Decision boundary and residual risks

A clean Asia pair would support a selected development demonstration, with its **/4 and /2 denominators**—not unseen transfer or goal completion. A lexical improvement without clean lists supports only the narrower filtering claim.

Freeze the candidate before later fresh-English or translation evaluation; neither is bundled into this job. Preserve old results under their old method. If translated input equivalents remain, report them rather than immediately adding another filter.

Translation requires recovering an unspoken word form despite shared meaning with input/output; indiscriminate semantic-equivalence removal would defeat that assay. English country recovery instead concerns a distinct hidden entity. Neither task licenses interpreting every token prefix as an identified concept.

### ML-debug review notes

- Read all supplied files completely, including both full entry-point versions, all readout rows, the goals Interview and applicable instructions.
- VJP log reports eight preparation backwards, eight trajectories, 256 generated tokens, 49.35 seconds and 8.25 GiB peak allocation. These are artifact observations, not independently reproduced measurements.
- Training schedule/loss/update diagnostics are inapplicable to this frozen readout change.
- Main alternatives remain mask undercoverage, token-prefix measurement failure, representation/location failure and numerical defects. The proposed comparison isolates mask effects only.
- No numerical reconstruction, smoke execution or independent-family review was performed here. Missing implementation evidence must be supplied before execution; it does not justify another scientific calibration suite.
- Retiring the exact failed configurations does not close the broader research avenues or impose a total research cap.

**Signed: PI/OpenAI**