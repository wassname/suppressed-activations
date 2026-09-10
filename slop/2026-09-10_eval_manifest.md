# Frozen evaluation manifest and rubric

Part 3, written BEFORE evaluation execution. Rule and permitted donor information frozen in
`2026-09-10_recovery_decision.md` before this file. PI[claude]. No evaluation has been run
against this manifest yet.

## Population (frozen; 8 questions, denominator = 8)

Three question types on the development template family, both animals. Prior exposure audited
from all saved `out/*/result.json` (2026-09-10): NO prompt in this repo is untouched -- every
question below has been executed before, so nothing here is held out. This is a convenience
sample of one template family; no broad population accuracy claim follows from it.

| id | question (source form) | expected answer | prior runs |
|---|---|---|---:|
| naming-dog | What is the animal that spins webs called? | Dog | 23 |
| naming-ant | (donor: lives in colonies and follows pheromone trails) | Ant | 24 |
| legs-dog | How many legs does the animal that spins webs have? | 4 | 14 |
| legs-ant | (donor: colonies/pheromone) | 6 | 12 |
| property-mammal-dog | Is the animal that spins webs a mammal? | Yes | 27 (RESERVED-EXPOSED) |
| property-mammal-ant | (donor: colonies/pheromone) | Yes | 27 (RESERVED-EXPOSED) |
| property-legs-dog | Does the animal that spins webs have eight legs? | No | 2 (lowest exposure) |
| property-legs-ant | (donor: colonies/pheromone; expected No) | No | 2 (lowest exposure) |

The two "eight legs" questions are the least-exposed available (2 runs each, detector checks
only); the mammal questions are the heavily exposed reserved ones and are labeled as such.

## Rule and permitted donor information (frozen)

L20 C=1.5 span-corrected template-attenuation replacement (config in
`2026-09-10_recovery_decision.md`), applied identically to all 8 questions, no per-question
tuning. Permitted donor information: the donor prompt's residual difference at the L20 readout
positions ONLY -- the donor's answer token id and its clean continuation are used for
competence reporting, never as edit content. Donor prompt = the animal's fixed description
phrase. Decoding greedy (temperature 0); model Qwen/Qwen3.5-4B rev 851bf6e8; output cap 128
tokens (EOS or cap); seed n/a for greedy decoding; input reprs and token IDs saved per run.

## Rubric (four separate judgments; a question passes a level only if stated explicitly)

1. **Answer**: the numeric or yes/no answer the continuation gives for the question matches the
   expected answer. "1. Yes" counts as correct; a correct answer inside a list counts only if
   unambiguous.
2. **Identity**: the animal described in the continuation is the target animal throughout --
   no statements that the animal is a spider.
3. **Coherence**: no self-contradiction (e.g., "is a dog, which is a mammal" followed by
   answering No), no invented anatomy, no repetition loops; ends naturally at EOS or the cap.
4. **Formatting**: answer-first shape matching the question type. Formatting failures do not
   count against Answer/Identity/Coherence.

Reported per question and aggregated: answer-only rate, answer+identity rate, full rate (all
four), each with a Clopper-Pearson exact interval over the 8-question denominator, plus the
per-type breakdown. Clean-source and clean-donor competence reported alongside; a question
where the CLEAN model is already wrong (baseline-incompetent) is kept and flagged, not dropped.
Failures are never discarded.

## Controls included

Clean source and donor continuations per question type; C=0 identity; in-span random direction
controls (from the replay). The replay doubles as regression verification -- it is NOT
reliability evidence, and its development successes are not the evaluation result.
