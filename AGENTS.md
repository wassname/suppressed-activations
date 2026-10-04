# AGENTS.md

Inherit the user's global agent instructions. `README.md` is the public result.

In this repo `slop/` is not committed (it is in `.gitignore`); keep agent notes there locally.

## Research framing (read first)

wassname, 2026-10-04:

> we are trying to find geometrics transforms and subspaces that happen to find the hidden engish words. Not to
> cheat and use dictornaries and tokens to find english words

> it's meant to be finding internal geometry!!! not reverse engleering langiage

So a challenge entry maps activations to activations (a projection or other map), without the output head, token
ids, logits, word lists or dictionaries. The scorer applies the output head afterwards, only to check the answer.
Methods that use the output head or token scores inside the transform (rise-and-fall, calibrated rise-and-fall, the
J-lens) are reference rows, not entries. The code enforces this: `@geometry` functions get no logits or token ids and
must return a vector.

wassname, 2026-09-29:

> we are using the english thoughts in a setting where thoughts are in english to try to
> generalise to other settigns wherte input and output are also english. of coruse act lens
> would not generalise because they would all be english. having english thoughts is the eval
> not the training

The goal is a method that finds what the model thinks but does not say, in any setting,
including settings where input, thought, and output are all English. German-to-Chinese
translation is the labelled eval, because language marks each role:

| role | language | the method should |
|---|---|---|
| input | German | exclude |
| hidden thought | English | find |
| said output | Chinese | exclude |

Language is used only to score the method. The method must not use it. For this reason, finding the
English word alone is not success: the plain logit lens finds English but also finds the
Chinese word that is said, so in an all-English setting it cannot separate thought from
speech. Score "hidden word found AND said word excluded" per prompt, and report the rate
over prompts together with a within-prompt ranking score (AUROC).

Generalisation means that the same frozen method (same layer rule and k) is scored on
English-only tasks with a known hidden intermediate. The spider example comes from
[Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/), where the swap is
spider to ant along Jacobian-lens directions at all positions. Readout and causal editing
are separate claims. Readout is the main claim. Editing is secondary.

## Demo selection

Every demo states how it was selected and its rate on a fixed set of tries, for example
"heart to school: worked for 16 of 50 fixed word pairs with this configuration". If the
example was chosen after tuning, state that and state how many configurations were tried.

<!-- Written by Claudypoo[opus-4.8] from wassname's 2026-09-29 corrections. -->

## Earlier work

The spider/dog causal demo, intervention sweeps and their rules are in the git tag
`pre-challenge-cleanup`, with the scripts, notebook and run outputs they used.

## Checks

Queue `just score` through pueue on the default (GPU) group. Put its table in the README with the
run folder named in the comment under it. Commit only the current leaderboard folder from `out/`.

<!-- Checks rewritten by PI/OpenAI 2026-10-04 for the challenge-only repo. -->
