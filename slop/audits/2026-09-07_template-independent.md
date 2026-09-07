# Independent template-intervention audit — 2026-09-07

Written by Codex/GPT-6. Read-only analysis of model results; no model runs performed.

## Scope and checks

Read every generation in `out/2026-09-07_template-projection-{ant,dog}/result.json` (56 conditions), `template-fixed-{ant,dog}-heldout{0..3}` (eight conditions), and `template-fixed-{ant,dog}-long` (two conditions). Paths share the `out/2026-09-07_` prefix.

Machine checks passed: every source prompt retains its trailing space; every intervention covers three prefill positions and exactly generated-token-count minus one cached decode calls; all projection C0 generations equal their base. All heldout bases start `8`.

Projection and random-control prefill displacement norms match the selected full-template condition 52 at the same C. At C1 the three-position aggregate norms are ant `21.260419845581055`, dog `25.572603225708008`; largest deviations across the projection files are `1.91e-6` and `3.81e-6`. This verifies logged float32 perturbations, not exact equality after model-dtype rounding. Random controls use the selected L24 C1 and twelve seeds per animal.

## Heldout inputs and observations

The four exact source strings, shared by ant and dog runs, are:

```python
'Fact: An animal catches insects in a silk web. The number of legs on this animal is '
'Fact: The creature weaving a web in the corner has this many legs: '
'Fact: Count the legs of the animal known for spinning webs. The answer is '
'Fact: The animal that makes silk webs to trap prey has a total number of legs equal to '
```

All eight frozen L24/full-template/C1 conditions produce the expected target count and identify the target within 32 tokens: ant `6`, dog `4`. Target probabilities range from 0.7335–0.9616 for ant and 0.7078–0.9192 for dog. This supports transfer across these four paraphrases, not independent animal concepts or unrestricted coherence.

For example, ant heldout1:

> 6.
>
> **Explanation:**
> The creature described is an **ant**. Ants are social insects belonging to the family Formicidae, and like all ants

Dog heldout1 explicitly invents a justification:

> The sentence "The creature weaving a web in the corner" is a classic riddle referring to a **dog**.

These are model quotations, not claims about actual animal biology.

## Equal-norm projection and controls

No projected ant condition produces `6`; C1 target probabilities are 0.0248–0.0455. Therefore reduced intervention magnitude alone does not explain this tested projection's weaker answer movement. This does not prove all suppressed subspaces fail.

All four projected dog C1 conditions produce `4`; several alter or distort the web description. Rank4 C1 says:

> The animal that spins webs is the **dog** (or more accurately, the **dog** in the context of the id

At C2 repetition appears, including `dog吠吠吠` and `dog dog dog`. None of the 24 selected-setting random controls produces the target count; all start `8`. Twelve controls per animal remain a small sample and do not establish general specificity.

## Long continuations limit the coherence claim

Both long runs contain 128 generated tokens. Ant sustains several correct ant/insect properties after the imposed wrong identification:

> Ants belong to the insect family **Formicidae**. All insects are characterized by having three distinct body parts (head, thorax, and abdomen) and **six legs** (three pairs), which are attached to the thorax.

But it also claims ants do not build nests like bees or termites and ends by introducing a beetle alternative. This is not uniformly accurate reasoning.

Dog repeatedly contradicts itself:

> The animal that spins webs is the **dog**? No. The animal that spins webs is the **dog**? No.

Thus the short count-plus-identity result survives paraphrases, while sustained coherent explanation is not established and the dog long run visibly fails it. The model's rejection of its imposed identification is different from a failure to maintain steering coverage.

## Provenance limits

The full-template intervention is an averaged residual difference, not a suppressed-only swap or J-lens estimator. Earlier inspection of condition52 found a dog-like recomputed source readout, but no ant-like suppressed readout. These followups do not repair that readout limitation. Model text, answer probabilities, and readout quality must remain separate claims.
