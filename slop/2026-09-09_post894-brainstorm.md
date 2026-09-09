# post-894 brainstorm comparison

Reports: `slop/reviews/2026-09-09_{kimi-k3_post894_kimi,glm-5.3-flash_post894_glm}.md`
Neither picks a winner. Offline check done here before GPU.

## Offline (GLM M1)

`template_vectors.pt` deltas at L18/20/24/32 have cosine **1.0** between detector-c2 and
local-c003 (same tensor). Detector-c2 is not a different template delta; it is the same
delta projected into a vocab-suppression span (`projected_norm_fraction` 0.029 at L20).
That rules out “c2 steered a different template direction.” It does not rule out a
wrong *span*.

## Hypothesis table

| id | source | mechanism | cheapest remaining check |
|---|---|---|---|
| M-A | kimi | ant token/position alignment | first-token margin 893 vs 894 (saved top-10 already: 893 `狗` first; 894 `蚂蚁` first — both flipped) |
| M-B | kimi | name logit vs concept; web contradiction drives loop | cannot drop “spins webs” from source (constraint) |
| M-C | kimi | ant not at L20; 863 was L24 | layer sweep, or first the recovered ant *method* on naming prompts |
| M-D | kimi | continuous steering limit cycle | one 894 rerun with decay after token 1 |
| M1 | glm | c2 under-steering | **done:** same delta, 3% in vocab span |
| M2 | glm | S_swap only first token | 894 text already shows `Wait, ants do not spin webs` immediately |
| M3 | glm | correction attractor | needs a construction that keeps source fixed |
| M5 | glm | donor-source mismatch | 894 already used question-family ant donor + c003 |

Test that most reduces uncertainty under “source unchanged, one rule later”:
**863’s method (synchronized-attenuation c011, L24) on 894’s ant naming question.**
Parallel to 893 (862’s method × naming questions). Isolates whether the recovered
ant method names an ant on this prompt, or ant naming loops regardless of method.

## Job 895 (sync L24 c011 × ant naming question)

Steered (89 tokens, L24 perturbation 31.89, S_swap +13.625, steer≠base):

```text
蚂蚁 (Ant)

Wait, that is incorrect. The animal that spins webs is a **spider**.

The spider is an arachnid known for its eight legs and ability to weave intricate webs to catch prey. They possess specialized silk glands that produce strong, flexible threads used for building their homes and capturing insects. Despite their reputation for being creepy, many species are harmless to humans and play a vital role in controlling pest populations.<|im_end|>
```

Clean base: `蜘蛛 (Spider)` + spider body. Clean donor: `蚂蚁 (Ant)` + ant/colonies/pheromones body.
Pattern matches earlier band naming (donor name, then correct to spider), not 894's 蚂蚁-is-wrong loop and not 863's coherent ant-on-legs.

So: recovered dog method × naming questions works (893); recovered ant method × naming questions does not (895).

Next one-axis job (existing sweep, no new code): synchronized-attenuation **L20 C2** (condition 8) on the same ant naming prompts — same method family as 895, same layer as 894/893.

## Job 898 (sync L20 C2 × ant naming)

First token `蜘蛛`, S_swap +2.97, L20 perturbation 6.08 (weaker than 894's 19.8).
Steered is still a spider paragraph (paraphrase of Base, IDs differ). Does not flip the name.

Ant naming so far: local L20 = name then loop; sync L24 = name then spider; sync L20 = spider throughout.
Next existing-sweep axis from 894: attenuation-local **peak 25** matchedTrue C2 (condition 11).

-- PI/Grok
