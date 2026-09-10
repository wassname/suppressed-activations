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

## Rev 3 (append-only correction; rev 2 retained above for provenance)

Rev 2 is NOT approved and had five defects, fixed here:

1. `eval_fresh_batch.json` did not exist. It now does: 12 machine-readable entries with exact
   source and target prompt strings, both expected answers, fact-change flags, and per-entry
   verification fields (`suffix_shared_last3`, `answer_single_token`, `*_previously_executed`).
2. prop-spinneret's two sides asked DIFFERENT predicates (egg-case silk vs have spinnerets).
   Fixed: the predicate lives in the template and is IDENTICAL on both sides; only the
   descriptor slot is replaced.
3. Descriptors were not unambiguous ("produces silk", "builds nests underground"). Fixed
   descriptors: spider "spinning webs to catch insects"; dog "barking while living as a
   domesticated pet"; ant "living in six-legged colonies and following pheromone trails". The
   question WORDING varies between N1/N2, L1/L2; the descriptor identifies the animal.
4. Ground truth is independent animal facts (spinnerets: spiders yes, dogs no, ants no; live
   birth: dogs yes, spiders and ants no; legs 8/4/6; the names). The clean model's answer is a
   reported competence measurement, not the ground truth.
5. Binomial intervals removed. For a fully evaluated fixed convenience set the success fraction
   is an OBSERVED descriptive rate (n/N), not a sample from a population: the CP interval in
   rev 2 assumed independent Bernoulli sampling, and the paired animal rows violate
   independence. Reported instead: descriptive n/N per level, per-wording and per-animal
   variation, and judgment/censoring uncertainty (which rows were capped, which judgments were
   ambiguous), stated simply.

Verification run on the final entries: shared last-3 tokens on every pair (runner assertion
holds), single-token answers on every expected answer, and ZERO prior execution of the final
exact strings. The fresh evaluation still has not run; nothing is scored against this manifest.

## Rev 4 (pre-run correction, authorized): descriptor answer-cue removed

The ant descriptor "living in six-legged colonies and following pheromone trails" leaked the
leg-count answer into the donor prompt. Replaced everywhere with "living in colonies and
following pheromone trails" (6 entries updated; previous descriptor preserved per-entry as
`donor_descriptor_prev`). All 12 rows re-verified on final strings: shared last-3 tokens,
single-token answers, zero prior execution. Frozen before GPU:

    sha256 62d96b706f68e4a8256bae29f82e4aa8866aecef52ed87849966d40c37e04f4e  slop/eval_fresh_batch.json

Continuation instruction and chat wrapper identical to the recovered dev replay
("Answer the question with the answer first. Then describe the animal in three sentences.",
chat-assistant-prefill); full rendered input reprs and token IDs saved per run; if identity is
not observable from a continuation it is labeled unknown, not scored a pass. Candidate frozen:
recovered L20 C1.5 span-corrected template-attenuation, fixed donor term, current-state removal,
original generation/coverage settings; no synchronization, no retuning after evaluation.
Controls: clean source/donor (in-run), C=0, and the C=1.5 in-span random; ACTUAL edit norms
compared per condition (same C is not magnitude matching) and any residual mismatch labeled.
No new intervention variants; no retuning on this set.
