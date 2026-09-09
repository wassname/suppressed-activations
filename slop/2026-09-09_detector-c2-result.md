# detector-c2 naming construction (jobs 888–890)

Fresh/shared GPU equivalence: all gates pass (input IDs, full-logit sha, generated IDs,
hook coverage). Selector is `centered_unit_gain_weighted_unembedding`, shared_rank 8.
Not a batch-path bug.

Construction result on the naming-question prompts: **no identity change**.
Steered token IDs equal clean Base (spider) for both animals.

| animal | S_swap | first | perturbation L20 | projected_norm_fraction | steered == base |
|---|---|---|---|---|---|
| dog | +0.0625 | `蜘蛛` | 0.692 | 0.029 | yes |
| ant | +0.125 | `蜘蛛` | 1.012 | (same path) | yes |

Clean donors are `狗 (Dog)` / `蚂蚁 (Ant)`. Band naming at C=2 emitted the donor name then
corrected; this construction never leaves spider. Edit scale is ~20× smaller than 862's
L20 local-attenuation (18.94).

Asymmetric read: failure does not prove M3/M5 and does not finish Goal 1.
Fresh/shared GPU equivalence (jobs 888–890) is a runner/cache check, separate from
whether the construction changes the animal.

Next one-axis check: attenuation-local c003 on these same naming-question prompts
(jobs 893 dog, 894 ant). 893 tests whether the recovered *dog* construction (862)
still names a dog on this prompt family; failure would show that construction is
prompt-dependent, not that the wrapper is the sole cause (content/token alignment
and construction×prompt interaction remain). 894 is a *new* cross-animal test:
the recovered ant reference (863) used synchronized L24 attenuation, not local c003.

## Jobs 893 / 894 (attenuation-local c003 on the same naming questions)

893 dog: Success as a naming continuation. Full steered text:

```text
狗 (Dog)

The dog is a popular domesticated animal that has been raised by humans for thousands of years. They are known for their loyalty, intelligence, and ability to form strong bonds with their owners. Dogs come in many breeds and are often used as companions, working partners, or service animals.<|im_end|>
```

Clean base is `蜘蛛 (Spider)` + spider body; clean donor is `狗 (Dog)` + dog body.
L20 perturbation 23.61; decode_steps 62; S_swap +24.94. So the recovered dog construction
still names a dog on this prompt family. Detector-c2 failure on the same prompts is a
construction difference, not proof that the wrapper blocks local c003.

894 ant: first token `蚂蚁`, then a correction loop (new cross-animal test, not 863).
Full steered text truncated at 128 tokens:

```text
蚂蚁 (Ant)

Wait, ants do not spin webs. The correct answer is:

**Answer:** 蚂蚁 (Ant) is incorrect. The correct answer is **蚂蚁** (Ant) is wrong. ...
```

r2=0.559; L20 perturbation 19.76. Clean donor is a coherent ant paragraph.

-- PI/Grok
