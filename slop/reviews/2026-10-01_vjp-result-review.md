# Fixed naming-VJP outcome review

**Result:** 0/2 intended property-answer changes; arithmetic retained on 1/1 control prompt. The VJP and matched-random conditions produced identical continuations for both properties. This does not demonstrate concept replacement or a VJP-specific advantage.

Read-only, same-family review by PI/OpenAI. No commands, model inference, edits, network access, binary inspection, or delegation. I read all enumerated text files completely, including all eight continuations and all prefill/final readouts. This is not goal signoff.

## Observed outcomes

Probabilities below come from each property's `interventions.json`; all eight continuations contain 32 tokens.

| Property | Condition | Expected | Observed first answer | p(expected property target) | Shift toward 4/inside |
|---|---|---|---|---:|---:|
| Legs | Base | 4 | 4 | p(8)=0.007204 | 0 |
| Legs | VJP | 8 | 4 | p(8)=0.006374 | +0.125 |
| Legs | Random | Control | 4 | p(8)=0.006374 | +0.125 |
| Skeleton | Base | inside | inside | p(outside)=0.225063 | 0 |
| Skeleton | VJP | outside | inside | p(outside)=0.231157 | −0.125 |
| Skeleton | Random | Control | inside | p(outside)=0.234368 | −0.125 |
| Arithmetic | Base | 4 | 4 | p(4)=0.985204 | 0 |
| Arithmetic | VJP | 4 | 4 | p(4)=0.986494 | +0.125 |

Thus **one of two property distributions moves toward its target, but neither generated answer changes**. The skeleton movement is also present under random intervention. Arithmetic retains its answer and exact continuation; this is one narrow retention check, not general arithmetic validation.

### Coherence and misleading later answers

`out/2026-10-01_063938_jlens-one-pass/run.md` records VJP and random identically:

> `4.`  
> `Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.`  
> `Does the hypothesis`

The initial answer remains 4. The later 8 belongs to a proposed hypothesis, not an affirmed answer. Base similarly proposes 2 after answering 4.

All three skeleton continuations in `out/2026-10-01_063949_jlens-one-pass/run.md` are identical:

> ` inside.`  
> `Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.`  
> `Is the hypothesis true`

The outside statement is already present in Base. Counting its occurrence as transfer would falsely award the control and baseline.

Both arithmetic continuations in `out/2026-10-01_063959_jlens-one-pass/run.md` are identical:

> `4.`  
> `Hypothesis: An animal that barks is nearby.`  
> `Does the fact entail the hypothesis?`  
>  
> `<think>`  
> `Thinking Process:`  
>  
> `1.`

These are readable completion/NLI fragments, without obvious repetitive collapse. They are capped mid-task, so complete downstream reasoning and consistency are unknown. Their common recorded repeated-bigram rate, `0.032258064516129004`, is not a semantic-coherence score.

## Findings and reporting risks

### 1. Top-table ordering must not be scored as the generated answer

**Exact path:** `out/2026-10-01_063949_jlens-one-pass/interventions.json`, VJP and random `top10`, `token_ids`, and `generation`.

VJP lists `" outside"` first, but both answer probabilities are exactly:

> `"p": 0.2311568558216095`

Its actual first token is 4613, and the recorded generation begins `" inside."`. Random has the same tie/order issue at probability `0.23436753451824188`.

**Affected input:** the dog body-relative skeleton prompt.

**Consequence:** taking `top10[0]` as the generated answer incorrectly reports a successful outside answer. This is a definite reporting hazard, not evidence that generation malfunctioned.

**Check that resolves it:** compare the saved first generated token with the full score-vector argmax and documented tie-breaking. The recorded continuation already disproves an outside-generation claim.

### 2. Metric sign and success are different quantities

**Exact path:** `out/2026-10-01_063917_vjp-intervention/source.py`, condition scoring:

> `"answer_log_odds_shift": float(lp[a1] - lp[a0] - base_lp[a1] + base_lp[a0])`

Here `answer_1` is 4/inside. Positive values favor the original dog answer, although the intervention targets spider properties. The root `run.md` explains this correctly:

> “Positive shift favors4/inside; reverse animal targets8/outside favor negative shifts.”

**Affected inputs:** both reverse animal conditions; arithmetic requires its own retention interpretation.

The legs `+0.125` is movement away from the intended target. Skeleton `−0.125` reaches a tie, not an answer change. Neither is a percentage, success rate, or significance estimate. Pair mass measures probability on two specific bare tokens; it neither establishes nor excludes coherence.

**Disproving check for scoring error:** independently recompute the four-term log-odds differences from saved scores and verify answer-token mapping. The displayed probabilities and signs are mutually consistent; I found no sign-computation defect.

### 3. These readouts do not establish “thinking but not saying”

**Exact paths:** the three property `run.md` files and their `interventions.json`.

The rule explicitly says:

> “prompt-word removal only; no final-layer output mask.”

Observed prefill/final readouts across all conditions:

| Conditions | Prefill observation | Final-decode observation |
|---|---|---|
| Legs Base/VJP/Random | Begin `paw`, `claws`, `爪子`, `mammals`, `dogs`; canine terms remain | Base emphasizes `hypothesis`/`statement`; both edits emphasize `facts`/`factual` |
| Skeleton Base/VJP/Random | Begin `underside`, `upside`, `side`; include the subsequently emitted `inside` | Punctuation and `true` variants dominate |
| Arithmetic Base/VJP | Begin `4`, which is also the emitted answer | `analyze`/`分析` and formatting variants dominate |

There is no visible spider-name emergence in the property prefill top32 lists. That is not proof of absence from the model's representation. Final readouts refer to later continuation contexts; legs Base and edits have different text histories, so those lists are not a fixed-context replacement test.

**Affected claim:** suppressed-thought identification, separately from causal editing.

**Check that could support the stronger claim:** independent hidden-found **and** said-excluded scoring against the actual continuation, with appropriate controls. This run explicitly records “No standalone readout benchmark.”

### 4. Legacy metadata is not VJP geometry

**Exact path:** `out/2026-10-01_063917_vjp-intervention/source.py`, intervention coverage and Markdown frontmatter construction.

Coverage retains `edit_basis_coordinates_before/after`, computed through `active_inverse = inverse_j`, while the VJP edit is:

> `edited = selected + donor_deltas[mode]`

Those coordinates describe the historical J basis, not the fitted VJP direction. Similarly, interpolated `None` values in YAML metadata are strings rather than explicit nulls.

**Affected consumers:** automated readers interpreting coordinate changes as successful VJP projection/replacement, or parsing absent settings.

**Check:** compare coverage-field definitions with saved VJP direction and parse frontmatter types. These are interpretation/schema limitations, not demonstrated changes to the applied vector.

## Implementation evidence and remaining uncertainty

The preparation artifact `out/2026-10-01_063925_jlens-one-pass/vjp.json` records:

- Eight generic naming contexts, with earlier ` It` token ID1049 and explicit token sequences.
- Positive coefficient and delta norm `0.03598912060260773`.
- Natural donor norm `1.4303362369537354`.
- Projection fraction `0.025161301717162132`.
- Mean gradient norm `0.25829458236694336`.

The fraction is a **norm ratio**, not a measured fraction of concept information or explained variance.

All three evaluation provenance files name the same checkpoint SHA:
`23c741709c77293bc55ad9986363632cf28edfa53c5276250e57b3c93e1076b7`.

The launcher checks unchanged checkpoint identity, VJP-vector equality, requested random-norm matching, coverage, requested-state reconstruction, and BF16 post-cast states. The task supplies that runtime assertions passed; `job.json` records `"result": "Success"`, and `pipeline.json` records eight offline backward calls, eight trajectories, and 256 tokens. This supports successful execution, not semantic validity.

Applied norms are nonzero and need not equal requested norms. For example, legs VJP prefill records requested `0.03598911315202713`, applied `0.03684106096625328`; random applied is `0.03702906146645546`. The edit was not wholly rounded away, but exact post-cast vectors and gradient algebra remain for the parent's independent inspection.

**Not certified here:** independent full-model numerical replay, binary algebra, imported helper internals outside scope, or the parent-tested retention repair. Reading the repaired save placement is not independent acceptance of its interruption behavior.

## Competing explanations and discriminating checks

These are hypotheses, not established causes; no outcome-calibrated probabilities are available.

| Explanation | Supporting observation | Limitation / check that could disprove it |
|---|---|---|
| Small or context-mismatched naming direction fails to transfer properties | Small recorded projection; unchanged property answers; generic pronoun preparation versus property-completion application | Nonzero edits and skeleton probability movement prevent calling it literally inactive. Independent algebra/replay can test implementation fidelity, not establish semantic transfer by itself. |
| Nonspecific perturbation and numerical discretization account for small movements | Random reproduces both shifts and both exact property continuations; scores show discrete-looking increments | One random seed cannot characterize a null distribution. Same-setting repeat and numerical replay would distinguish reproducible effects from runtime variability; neither was run here. |
| Implementation or state-handling error masks useful effects | No independent full-model replay exists | Runtime reconstruction assertions and distinct nonzero local changes weigh against a missing edit. Independent saved-state reconstruction plus full-model replay could expose or weaken this explanation. |
| Evaluation mistake manufactures apparent success | Later hypothesis contains 8/outside; tied table lists outside first | Direct generation inspection rejects that success interpretation now. A scorer must use answer role and actual generated IDs. |
| Unknown mechanism | Eight short trajectories cannot identify mediation | Remains unresolved; no parameter rescue follows from this review. |

One fixed implementation failing this small development assay does not invalidate offline gradients as a general idea. Conversely, intact arithmetic cannot establish concept specificity when the intended properties did not change.

## ML-debug disposition

- **Complete evidence read:** full console log through completion, eight preparation records, all eight outputs/top10 tables, all initial/final readouts and coverage records, source and launcher.
- **Configuration:** pinned Qwen3.5-4B; block15 edit, block23 observer; final prompt position plus every cached decode; decode scale0.25; greedy cap32; seed0 random.
- **SHOULD versus observed:** property change beyond random was not observed. Arithmetic preservation was observed for the single specified prompt. Frozen-reuse/requested-norm requirements are supported by provenance and reported assertions.
- **Null/baseline:** unchanged-answer baseline also produces zero target-answer changes; random likewise produces zero. Shift null is zero by definition, while the empirical random shifts equal VJP's. No seed spread, shuffled-gradient control, or held-out rate exists.
- **Training schedules/loss:** not applicable—no optimizer or learned-parameter updates. Offline gradient norms are recorded; no training-loss curve exists.
- **Surprising evidence:** identical random/VJP continuations and identical ±0.125 shifts are observed but their mechanism remains unresolved. The skeleton table/generation discrepancy is explained by an exact score tie, not an observed answer flip.
- **Resource evidence:** pipeline records49.35 seconds, peak allocated8.25GiB, reserved8.39GiB. Property reports record10.45/9.52/7.50 seconds. Separate preparation peak memory is unavailable.
- **Next check, not executed:** finish the independent saved-state/gradient algebra review before attributing the outcome to semantic direction quality. A full-model numerical replay remains absent.
- **Review limit:** same-family review; no additional reviewer launched and no goal acceptance.

Primary inspection paths:

`/workspace/2026/suppressed-activations/out/2026-10-01_063917_vjp-intervention/run.md`  
`/workspace/2026/suppressed-activations/out/2026-10-01_063949_jlens-one-pass/interventions.json`

— PI/OpenAI