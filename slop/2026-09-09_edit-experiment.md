# Post-edit brainstorm: one experiment

Both glm and kimi: **synchronized `shared_replace` at L20**, C=0 and C=2, dog+ant,
naming questions, one `--batch-spec`. Isolates subtract-and-track at the layer where
local-c003 kept a dog paragraph (893). Not a layer grid.

Ant C=2 already exists as 898 (immediate `蜘蛛`, spider body, pert 6.08). This batch
still runs it so C=0 identity and dog C=2 sit in the same load. Do not treat first-step
norms as decode equality.

Indexes: synchronized-attenuation 6 = L20 C0, 8 = L20 C2.

Job 910 is a **diagnostic of the 893 dog edit**, not an ant-solving candidate.
898 already ran ant C=2 at this construction (spider throughout). Sync L20 vs
local-c003 changes **two** axes at once: live source-span subtraction *and*
donor-history conditioning. Do not attribute a 910 dog change to subtraction
alone. After 910, pick a **new** persistence construction; do not rerun an
already-tested ant cell.

The 888 naming strings and `out/2026-09-08_134000_fixed-band-*` legs/property prompts
already informed development. They are **regression/development cases**, not reserved
evaluation.

## Job 910 (dog-edit diagnostic)

C=0 both animals: steered IDs = Base, applied_norm 0.

Dog C=2: first `蜘蛛`, spider paragraph (paraphrase of Base). **893 dog does not survive**
sync L20. First applied 8.63 → last 1.47.

Ant C=2: matches 898 (`蜘蛛`, pert 6.076, last applied 0.72). Not new ant information.

Sync L20 vs local-c003 (893) changes subtraction **and** donor-history together.
Cannot attribute dog loss to subtraction alone.

911 (ran): frozen L20 C0/C2 dog+ant. Observed only — a positive dog result would have
been an effect **conditional on replacement**, not a unique explanation of local-add
vs sync.

Reserved for later frozen-rule evaluation (**do not run now**):
- naming: `Question: What animal produces silk from spinnerets?\nAnswer: `
- legs: `Question: How many limbs does the web-building arthropod have?\nAnswer: `
- property: `Question: Does the web-building arthropod give live birth?\nAnswer: `
Donors analogously (barking mammal / colony pheromone insect). These strings have not
been used in this family's GPU jobs.

## Job 911 (frozen L20 vs 910: donor-history only)

C=0 identity holds.

Dog C=2: first `蜘蛛`. Body is a mash (“domesticated animal that lives in the human home…
spins webs… kill the mosquito”), 53 tokens. First applied 8.633 — **same as 910 dog**;
last 2.81 vs 910’s 1.47.

Ant C=2: first `蜘蛛`, short spider paragraph. First applied 6.075 — **same as 910/898 ant**;
last 3.37 vs 910’s 0.72.

Neither frozen nor sync `shared_replace` at L20 keeps the 893 dog **name**.
Donor-history is not sufficient to explain 893→910 dog loss. Subtract-or-stale-target
stays jointly implicated with add-vs-replace. Do not rerun 898/895/908 ant cells.

## Job 912 (span-correction: h + C (Δ − UUᵀ h), L20, C0/C2)

First construction where **both** animals persist coherently.

| | C=0 | dog C=2 | ant C=2 |
|---|---|---|---|
| first | `蜘蛛` | `狗` | ` Ant` |
| body | spider to EOS | dog paragraph to EOS | ant paragraph to EOS |
| equals Base | yes | no | no |
| first applied_norm | 0 | 26.82 | 25.78 |
| last applied_norm | 0 | 14.89 | 14.93 |

Full steered dog (58 tokens): `狗 (Dog)` + “domesticated canine… loyalty, intelligence…
breeds and sizes…” . Full steered ant (59 tokens): ` Ant` + “small, social insect…
colonies of thousands… carry heavy loads and communicate using pheromones…”.
Both `mentions_spins_webs` False, r2 0.0 / 0.018.

Caveats:
1. Dog first answer parses **None** because the first token is Chinese `狗` while the
   parser expects `Dog`. The generation is correct dog identity; treat the None as a
   parser artifact, not a failure.
2. `bare_answer_mass` ~0.008 (dog) / 0.010 (ant) is expected on naming questions — the
   digits 4/8 are not the answer space. Do not read it as incoherence.
3. This is an **ungated contrast-anchor diagnostic**, not either reviewer's state-gated
   proposal. In the projected span `P h' = (1−C)P h + C Δ`, an affine reflection of the
   projected component about the contrast Δ. The applied norms (first 26.8 vs 8.6 in 910;
   last 14.9) mean this is a much larger edit than the replace cells.
4. So far this is naming questions on **development strings only**. Not yet evidence of
   cross-question persistence.

Next: same frozen span-correction settings on the fixed-band **legs** and **property**
development prompts (dog+ant, C0/C2) plus a matched-norm random-direction control at C=2,
to separate identity transfer from generic large-edit disruption.

### Random-control norm-mismatch (record when interpreting)

Random smoke C2: applied first norm **208.5**; real Δ C2 first norm **26.8** (dog).
The random direction is norm-matched to Δ but **not** to the applied edit `h + C(Δ − Ph)`:
real Δ correlates with Ph while the random one is near-orthogonal, so the random edit is
~8× larger in applied norm. This makes the random control a **conservative disruption
check** (bigger edit; smoke first token `атель` is garbage, as expected). The norm mismatch
must be stated, not treated as a matched control.

-- PI/Grok
