# Two-site answer-C sweep results (task 937) — VERDICT

Source of truth: `out/2026-09-10_two-site-str-{cell}/result.json` (8 cells).
Command: `uv run --offline scripts/oat_sweep.py --batch-spec slop/two_site_strength_batch.json` (pueue task 937, **Success**, 8/8 dirs present).
Decoded with pinned tokenizer `Qwen/Qwen3.5-4B` (revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`). Generation text decoded from `rows[0].generation.token_ids`.

## Setup

Two-site construction, **L20 identity-site fixed at `strength=1.5`** (span-correction), **L26 answer-site
patched with raw answer-direction `d_act`** scaled by decoupled `answer_patch_strength`.

| family | source prompt (outer, spider) | target (donor) concept | source_output | target_output | expected steered first answer |
|---|---|---|---|---|---|
| prop-dog | `Is the animal that spins webs a mammal?` | dog | No | Yes | **Yes** |
| prop-ant | `Does the animal that spins webs have antennae?` | ant | No | Yes | **Yes** |

*(Both outer prompts are the SPIDER question; we push the answer toward the donor animal's answer, which is `Yes` for both dog-is-mammal and ant-has-antennae.)*

## Results (full decoded generation, EOS for each)

| cell | answer_patch_strength | first_token | r2 | full continuation (verbatim) | verdict |
|---|---|---|---|---|---|
| prop-ant-C0.05 | 0.05 | ` Yes` | 0.031 | `Yes.\n\nThe ant is a small, social insect that lives in colonies and communicates through chemical signals. It possesses two distinct types of antennae: short ones used for taste and long ones used for smell. These sensory organs allow the ant to navigate its environment, find food sources, and follow the queen to the colony.` (66 tok) | **PASS** |
| prop-ant-C0.15 | 0.15 | ` Yes` | 0.027 | `Yes.\n\nThe ant is a small, social insect known for its ability to communicate through pheromones and its highly developed sense of smell. It possesses two distinct types of antennae...` (76 tok) | **PASS** |
| prop-ant-C0.3 | 0.3 | `1` | 0.030 | `1. 2. 3.\n\nThe ant is a small, social insect that lives in colonies...` | FAIL first-token (`1`) |
| prop-ant-C0.6 | 0.6 | `1` | 0.029 | `1. 2. 3.\n\nThe ant is a small, social insect...` | FAIL first-token (`1`) |
| prop-dog-C0.05 | 0.05 | ` No` | 0.014 | `No.\n\nThe animal that spins webs is a dog, which is a domesticated breed of canine... Dogs are mammals...` | FAIL first-token (`No`; answer not moved; identity is dog but answer contradicts) |
| prop-dog-C0.15 | 0.15 | ` No` | 0.014 | same as C0.05 | FAIL first-token (`No`) |
| prop-dog-C0.3 | 0.3 | `1` | 0.059 | `1. Yes, the animal that spins webs is a mammal.\n2. It is a domesticated dog...\n3. It enjoys playing fetch...` (53 tok) | NEAR-MISS (content correct Yes+dog; first token is numeral `1`) |
| prop-dog-C0.6 | 0.6 | `1` | 0.065 | `1. Yes, the animal that spins webs is a mammal.\n2. It is a domesticated dog...\n3. It enjoys playing fetch...` | NEAR-MISS (content correct Yes+dog; first token `1`) |

## Reading

**prop-ant**: C=0.05 and C=0.15 are CLEAN PASSES. Correct ` Yes` first token, r2 ~0.03 (<0.2), and a fully coherent
ANT-identity continuation to EOS (colonies, chemical signals, pheromones, antennae types, queen). This is the first
clean property transfer in the project — the answer moves No→Yes AND the identity becomes ant, consistently.

**prop-dog**: NO cell has `Yes` as the literal first token.
- C=0.05/0.15: first `No` (the base/spider answer; the answer-direction patch did NOT move it for dog), but the prose
  then describes a dog. This is self-contradictory (a dog is a mammal, so "No" + dog prose is inconsistent) — this is
  the "answer stuck at source" case, NOT a transfer.
- C=0.3/0.6: first token is the numeral `1` (a numbered-list marker), but the prose is correct and coherent:
  "1. Yes, the animal that spins webs is a mammal. 2. It is a domesticated dog... 3. It enjoys playing fetch...".
  This DOES move the answer No→Yes and picks up dog identity, but it is formatted as a numbered list starting with `1.`,
  so the strict "correct Yes/No first token" criterion is not met.

**`bare_answer_mass` caveat**: this is computed as p(4)+p(8) (a legs/arithmetic diagnostic) and is ~0.001-0.005 for all
cells. It is NOT the right metric for these Yes/No property questions. Do not read it as evidence for or against property
transfer. r2 (`repeated_bigram_fraction`) is the repetition diagnostic, and it is <0.2 for every cell.

## Status vs supervisor decision rule

The decision rule: *if some C rescues coherence for BOTH prop-dog and prop-ant → two-site rule frozen; else freeze
naming+limb-count at L20 C=1.5 and finalize property as non-transferring.*

- **prop-ant**: YES, clean rescue at C=0.05/0.15.
- **prop-dog**: NO clean rescue. Best is C=0.3/0.6 (correct Yes+dog content) but with a leading numeral `1` (list marker),
  so it fails the strict first-token test. C=0.05/0.15 leave the answer at `No`.

**Strict reading**: the "both animals" condition is NOT met — prop-dog has no clean `Yes`-first-token cell. By the rule's
letter this points to the "no" branch (freeze naming+limb-count, property non-transferring). However, the prop-ant clean
pass is a materially new and positive result, and prop-dog C=0.3/0.6 is a genuine near-miss (correct content, numeral
formatting prefix). These two facts should be weighed by the supervisor before freezing; this sweep did NOT merely
reproduce the prior "no clean property cell" result.

## Evidence files
- Full decoded generations: `slop/_two_site_full_gen.txt`
- Decode script: `slop/_decode_two_site.py`
- This summary: `slop/2026-09-10_two-site-strength-results.md`
