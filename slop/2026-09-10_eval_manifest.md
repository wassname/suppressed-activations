# Frozen evaluation manifest and rubric (rev 2: ground-truth and exposure corrections)

Written BEFORE evaluation execution; supersedes rev 1 (its property-mammal-ant expected answer
was factually wrong, and its exposure claim was broader than its audit). Rule and permitted
donor information frozen in `2026-09-10_recovery_decision.md`. PI[claude].
Equation correction: the candidate's actual branch is h' = h + C(Delta - UU^T h) with NO
component-norm matching and NO residual renormalization (the span_corrected_delta branch never
reads match_component_norm); earlier "with norm matching" descriptions were config-field reads,
not branch reads.

## Ground-truth rule

Every question stores the exact source and donor strings, the source's expected clean answer,
and the donor's expected clean answer. Ground truth is the clean model's own verified answer
where checked (quoted in the manifest from saved donor generations) plus simple facts about the
animals; a question enters the semantic scoring only after its ground truth is correct. Donor
competence is a reported control, not assumed.

## Correction of record (rev 1 error)

Rev 1 listed property-mammal-ant with expected answer Yes. That is factually wrong: an ant is
not a mammal. The clean donor answers "1. No, it is not a mammal. It is an insect, specifically
an ant." (verified generation, `out/2026-09-10_replay-C1.5-property-ant/result.json`). The
mammal question for the ant donor is a FACT-PRESERVING NO-OP (No -> No) and is kept only as a
no-op control question, labeled as such. The historical runner configs that paired mammal
wording with expected Yes (and produced historical "Yes" transfers) had invalid ground truth:
they pushed an answer that is factually incorrect for the target animal.

## Development rows (regression evidence, NOT the primary reliability estimate)

The six dev questions and their replays (`out/2026-09-10_replay-*`) remain development
regression evidence: heavily exposed (12-29 runs each), used for tuning history. They are
reported separately from the fresh set and never merged into it.

## FRESH evaluation set (primary; frozen now)

All wordings below were verified NEVER executed as question inputs in any saved result.json
(spinneret, live-young, live-birth, gives-birth: zero prompt-input hits; the one historical grep
hit for "live young" was inside a generation string, not a prompt). Twelve questions: two fresh
wordings per type, both animals. Source descriptor is the spider phrase; donor descriptor the
animal phrase; both sides share the question template and its ending.

| id | template (source form; donor swaps the descriptor) | source -> donor expected | fact changes? |
|---|---|---|---|
| name-N1 dog/ant | Which animal catches insects in a web? / is a common pet that barks? / follows pheromone trails in colonies? | Spider -> Dog; Spider -> Ant | yes |
| name-N2 dog/ant | What creature produces silk to trap prey? / is bred as a companion and guards homes? / builds organized nests underground? | Spider -> Dog; Spider -> Ant | yes |
| legs-N1 dog/ant | How many legs does the animal that catches prey in a web have? / that is kept as a pet and barks have? / that follows pheromone trails have? | 8 -> 4; 8 -> 6 | yes |
| legs-N2 dog/ant | How many legs does the animal that produces silk have? / that is trained to guard homes have? / that builds nests underground have? | 8 -> 4; 8 -> 6 | yes |
| prop-spinneret dog/ant | Does the animal that produces silk with spinnerets also produce silk for egg cases? -> Does the animal that barks... have spinnerets? | dog: Yes -> No; ant: Yes -> No | yes (both) |
| prop-liveyoung dog | Does the animal that spins webs give birth to live young? / donor: barks... | No -> Yes | yes |
| prop-liveyoung ant | (donor: colonies/pheromone trails) | No -> No | NO-OP control |

Denominator: 12 fresh questions (the no-op prop-liveyoung-ant is included and labeled; excluding
it post hoc would be tuning). Exact strings, both sides, are in `eval_fresh_batch.json`
(runner-format), committed with this manifest.

## Scope and dependence (stated, not implied away)

This is a convenience sample: one template family, one model, one intervention construction.
The two animal rows of each wording are PAIRED (same template, same procedure) and their
outcomes are dependent, not 12 independent draws; exact binomial intervals are computed per
level and per type but do NOT confer population validity -- they quantify only the uncertainty
of this declared set.

## Rubric (four separate judgments)

1. **Answer**: the continuation's answer to the question matches the donor-side expected
   answer. "1. Yes" counts as correct; an answer inside a list counts only if unambiguous.
2. **Identity**: the animal described is the target (donor) animal throughout; no statements
   that it is a spider; third-animal substitutions fail.
3. **Coherence**: no self-contradiction (e.g. "is a dog, which is a mammal" followed by No), no
   invented anatomy or history, no repetition loops, ends at EOS or the cap. Anatomy/history
   errors are FLAGGED in the per-question record rather than silently accepted.
4. **Formatting**: answer-first shape; reported separately, NOT required in the primary rate.

Primary semantic success = Answer + Identity + Coherence (formatting separate). Reported per
question with all four judgments visible; every failure kept. Cap: 128 tokens; a continuation
that ends at the cap is CENSORING, not evidence of natural completion -- flagged per row.

## Controls (under the CURRENT frozen procedure, all at C=1.5)

Clean source and clean donor continuations; C=0 identity; in-span random direction control at
C=1.5 (matched to the candidate's actual perturbation norms -- the replay's C=2 random is NOT
reused, since strengths differ). No evaluation run has occurred against this manifest.
