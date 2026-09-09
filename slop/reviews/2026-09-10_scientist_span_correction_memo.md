# Scientist memo: span-correction identity vs attribute transfer

Question: does the span-correction intervention transfer animal identity but not bound
attributes because the U-span encodes a name/concept pointer without attribute bindings, or
because the C=2 reflection overshoots attribute coordinates?

Scope: span_corrected_delta, L20, rank-4 U, C=2, continuous. Model Qwen/Qwen3.5-4B
rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a, batchwork shared-model-batch branch.
Selected development prompts only. Reserved strings (spinneret naming, limb count, live
birth) NOT used.

Roster: pass-1 scientists GLM 5.3 Flash (`z-ai/glm-5.3-flash`), DeepSeek V4 Pro
(`deepseek/deepseek-v4-pro-0813`), Kimi K3 (`moonshotai/kimi-k3`). Seminar pass: same three
families, each shown the two other unedited pass-1 reports. One discussion pass. No fallbacks,
no split audit/brainstorm tracks. Gated by a cheap comprehension pilot (GLM read the
pseudocode; confirmed the C=2 reflection semantics; no definition patch needed).

Primary evidence paths (batchwork): `out/2026-09-09_span-corr-{dog,ant}-{C0,C2}`,
`out/2026-09-09_span-legs-{dog,ant}-{C0,C2,rand}`,
`out/2026-09-09_span-prop-{dog,ant}-{C0,C2,rand}`. Result files under `result.json`.

## Observations (direct from the continuations)

- Naming (912): both animals named coherently to EOS, no loop. C=0 identity held
  (steered == Base). Naming random controls applied ~8x larger norms (208.5 vs 26.8) and
  produced garbage.
- legs-ant-C2: first `6`, coherent red-ant colony text. Identity AND correct digit.
- legs-dog-C2: first `2` (neither source-8 nor target-4), text "The animal is a dog ...
  Dogs typically have four legs ... standard number of legs for a dog is four, not two".
  Identity moved; digit wrong; text self-corrects. `answer=None` (parsing flag).
- legs-dog-RAND: first `4` (target correct), text "The animal is known as a spider".
  Digit moved, identity kept (spider).
- legs-ant-RAND: first `8`, "the spider" (no transfer).
- prop-dog-C2: first `No`, text "The animal that spins webs is a dog ... Dogs are mammals",
  answered `No` to "is it a mammal" (self-contradiction). spin=True is a prompt-restatement
  artifact, not spider identity.
- prop-ant-C2: first `No`, names ant, then loops (r2=0.370): "Unlike ants, the ant is a tiny,
  black insect ...".
- prop-dog-RAND / prop-ant-RAND: numbered-list/spider/garbage.

## Inferences (labelled, from the reviewers)

- **Leading hypothesis (spider-binding answer head)** — GLM promoted Kimi's I2 to default:
  both C=2 property answers are exactly spider-correct (spider not a mammal -> No; spider no
  antennae -> No). The yes/no head may evaluate a proposition whose entity binding is still
  spider, while prose positions read the edited coordinates. Overshoot does not predict
  source-correct answers.
- **Objection (DeepSeek seminar)**: the `No` could be a pragmatic default under uncertainty
  (forced answer slot), not a retained spider binding, since prose says "Dogs are mammals"
  immediately. Under this view the answer slot is uninformative, not spider-correct.
- **Alternative framing (Kimi seminar)**: the U-span may be a lexical/vocabulary anchor
  (name + collocational field) rather than a concept pointer. Predicts names/prose transfer but
  relational/forced-choice judgments do not; the binding search should be later layers reading
  unedited positions, not another L20 subspace.
- **legs-ant-C2 correct-target** undermines a pure "attributes never transfer" claim; the
  dissociation is dog-specific or prompt-specific, not universal.
- **The `2`** matches neither 8 nor 4; naive scalar reflection over digit coords gives
  nonsense for both animals, so leg count is not linearly encoded in the span. DeepSeek
  suggests a template-side artifact (anthropomorphic dog descriptions pair dogs with humans ->
  "two legs").
- **Random control is two-axis confounded**: `random_delta = randn_like(Δ)` is drawn in full D,
  not projected into U. It differs from real Δ in direction AND subspace membership (almost all
  its norm in the orthogonal complement), adding an off-span term real Δ never has. The
  legs-dog-RAND digit movement may be orthogonal-complement disruption, not matched-subspace
  steering.

## Parent decisions (separate from reviewer claims)

Selected next bounded test, one-at-a-time discipline (C is the varied axis; everything else
at 912 defaults):

1. C-sweep {0, 0.5, 1, 1.5, 2} on legs and property, dog and ant, L20 span-correction.
   C=1 (P h' = Δ) is the decisive cell: if it transfers name without attribute, reflection
   overshoot is dead.
2. In-span random controls: `random_delta = U(Uᵀ randn)`, then norm-matched to Δ, at C=1 and
   C=2. This is the control fix; current RAND is two-axis confounded.
3. Mirrored-property development prompt: source=Yes, target=No, e.g.
   "Does the animal that spins webs have eight legs?" with ant target (ant has 6 -> No).
   If it stays Yes (source-correct) under C=2, spider-binding confirmed; overshoot predicts a
   different pattern. This is a NEW development string, not a reserved one.
4. Read answers via logits at the answer position, not only sampled first tokens (all current
   claims rest on sampled first tokens; legs-dog-C2 answer=None already flags parsing
   fragility).

Next measurement confidence: the C-sweep is the single largest-information missing cell.
C=1 in-particular. If C=1 also yields name-without-attribute, the reflection-overshoot
hypothesis is falsified by construction (nothing is reflected at C=1).

## Links

- Pseudocode: `batchwork/docs/pseudocode/2026-09-10_span_correction.py`
- Brief: `batchwork/slop/2026-09-10_scientist_span_correction_brief.md`
- Pilot: `slop/reviews/2026-09-09_glm-5.3-flash_span_pilot_glm.md`
- Pass-1: `slop/reviews/2026-09-09_{glm-5.3-flash_span_pass1_glm,deepseek-v4-pro-0813_span_pass1_deepseek,kimi-k3_span_pass1_kimi}.md`
- Seminar: `slop/reviews/2026-09-09_{glm-5.3-flash_span_seminar_glm,deepseek-v4-pro-0813_span_seminar_deepseek,kimi-k3_span_seminar_kimi}.md`

-- PI/[k3]
