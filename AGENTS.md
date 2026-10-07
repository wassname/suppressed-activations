# AGENTS.md

Inherit the user's global agent instructions. `README.md` is the public result.

In this repo `slop/` is not committed (it is in `.gitignore`); keep agent notes there locally.

## Research framing (read first)

wassname, 2026-10-04:

> we are trying to find geometrics transforms and subspaces that happen to find the hidden engish words. Not to
> cheat and use dictornaries and tokens to find english words

> it's meant to be finding internal geometry!!! not reverse engleering langiage

Current submission rules are in `docs/submissions.md`. Geometry-only methods map activations to a vector and
may use model weights as matrices, but not individual token scores, token identities, word lists or dictionaries.
The scorer applies the output head afterwards. Methods using token scores, gradients, pretrained lenses or external
fitting data belong in the unrestricted leaderboard and disclose those resources.

The geometry interface is `method(hs, embeddings, state, *settings)`: `hs` contains residual layers 16–32,
`embeddings` contains the actual input states before layer 1, and both retain all prompt positions. Do not call
`hs[0]` the embedding: it is layer 16. Calibration state is separate. Python methods are not sandboxed.

<!-- PI/OpenAI: current two-category rules and explicit embedding input. -->

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

Run `just check` before pushing. For presentation changes, rebuild with `just results`,
`just plot-layers`, `just plot-cartoon`, and `just docs`; these use published evidence without model inference.
For inference changes, queue `just score` or `uv run --with matplotlib nbs/layer_readouts.py` through pueue.
Keep selected published evidence in the named files under `results/`; leave `out/` as ignored local history.
Methods live in `src/unspoken_concepts/methods/`; related variants may share a file.

<!-- PI/OpenAI: checks and paths updated for the current entry points. -->
