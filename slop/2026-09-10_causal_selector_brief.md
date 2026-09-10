# Causal selector comparison brief: maximum-agreement pair vs consensus (L25)

Goal 1, third family. Written and committed before any GPU run. PI[claude].

## Question

Does patching along the maximum-agreement pair's rank-1 component span move the answer or the
animal identity where the all-post-prefix consensus rank-1 direction does not, under an identical
replacement equation, positions, coverage, and strengths, on both animals?

## Selection procedure (pre-registered, common to every prompt, no per-animal fallback)

Per prompt, on clean forwards at L25 with the existing detector (early 23, peak 25, output 32,
rank 8, centered unit-gain unembedding directions):

- components c_p = P_p h_p per position p, where P_p is the projector onto that position's own
  detected basis B_p, h_p = residual at L25, position p. Shapes: h_p [2560], B_p [2560, 8],
  c_p [2560].
- among positions AFTER the common prefix (index >= 10; positions 0-9 are the shared template
  prefix, identical surface tokens in all four prompts), take all unordered pairs (i < j) and
  their signed cosines cos(c_i, c_j);
- select the pair with maximum cosine; ties broken by smaller i, then smaller j (deterministic);
- u_pair = unit top left-singular vector of the 2x2560 component matrix at the selected pair.
  Called maximum-agreement pair even when the source's maximum is only +0.102.

Known selections from the bank (analysis.json, L25): source (' spins'@10, ' '@13) +0.101;
dog (' called'@14, ' '@20) +0.854; ant ('om'@17, 'one'@18) +0.584. The runner recomputes these
from its own clean forwards; agreement with the bank is a check, not an input.

## Comparator

Consensus selector, same position domain (all post-prefix positions): u_cons = unit top
left-singular vector of the stacked post-prefix components, per prompt; donor target averaged
over all post-prefix positions. Same equation, positions, coverage, strengths.

## Replacement equation (identical across selectors; no component-norm matching)

At every patched position (last-3 prefill positions, then every cached decode step), with
h [1, pos, 2560] the L25 residual entering the block, u_src and u_don unit [2560] directions
built from the SOURCE's and the DONOR's own selections, and t [2560] the donor residual at L25
averaged over the donor's own selected positions (its pair for the pair selector, all
post-prefix positions for the consensus selector):

    h' = h + C * ( (t . u_don) u_don  -  (h . u_src) u_src )

The donor pair enters twice: its selection defines u_don, and its positions supply t. The edit
lies in span{u_src, u_don}, so the orthogonal source residual is preserved exactly. No rank-1
component-norm matching (it was shown to be a no-op at equal signs and a reflection at opposite
signs). The source input string is never modified; only activations are patched. C = 0 is exact
identity (asserted against clean logits); C = 1 and C = 2 are applied to every selector and
animal, no per-animal tuning.

## Conditions

Per animal (dog, ant): clean source continuation; clean donor continuation; C=0 identity;
{pair, consensus} x {C=1, C=2}; and one matched-random control per semantic condition (random
unit direction, distinct seed), its per-position prefill and per-step decode perturbation norms
matched to THAT condition's actual recorded norms. Trajectories that end at different lengths
are declared and logged as partial coverage, not forced to match. Generation cap 64 tokens
(above the 32-token notebook preview); full text and token IDs saved; complete per-call records
(every prefill position and every decode step), not just the first call.

## Judgments kept separate

Literal animal identity in the continuation; correct numeric answer; coherence and factual
contradiction; formatting. No causal claim from a digit alone: the dog syntax pair (' called'/
' and'/' '@20) and the ant subword pair ('om'/'one' of 'pheromone') are potential confounds, and
a moved digit with unchanged identity is the historical failure mode, not a success.

## Decision rule (no predeclared inertness)

If the pair selector moves answers or identity and the consensus selector does not, under
identical everything-else, that supports pair-local structure carrying target information. If
neither moves anything at C=2 while matched-random controls also do not, the descriptive limit
is that these rank-1 selectors, at these strengths, on this template, did not move behavior --
strengths, positions, direction mapping, and readout validity remain open alternatives, and the
detector is not pronounced causally inert.

## Process

Existing runner hooks and generation path; smoke on the tiny CPU model with deliberately
different prompt lengths and unequal layer/sequence dimensions (the shape guard asserts the
layer slice is on the layer axis). Queue through pueue even when the GPU is free; inspect the
saved command; arm a completion watcher whose exit is only a wake-up. Brief, config, and code
committed before GPU.

Note: the earlier attribution of prefix ULP differences to SDPA block sizes is an inference from
magnitudes, not a tested fact; labelled as such in the report.
