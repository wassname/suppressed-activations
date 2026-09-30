## Inherited decisions
- Both goals remain open: coherent dog→spider replacement producing **8 and outside**, using one frozen method and no current-question preparation or future-layer feedback.
- Approved prerequisite: eight matched pairs/16 prefills maximum, zero generations, frozen \(u,c\), all-position raw layer16 states. No answer-conditioned threshold/dose fitting.

## Diagnosis
The negative conclusion is justified **for the tested reflection**, not for every use of its direction.

Both runs faithfully implement conditional reflection at block15 output. Preparation uses residual16; the later observer does not control editing. Coverage is one prefill plus31 cached decode calls.

At the answer-producing position, dog/spider margins are:
- Legs: **1.0815/1.1533**
- Skeleton: **1.1946/1.4159**

Both sources therefore receive **zero prefill update**. Reflection retains `4` and `inside`, with unchanged first-token distributions. Later updates occur on8/7 calls; “reflection never activates” would be incorrect.

Positive target-minus-source differences preserve ordering on these two comparisons, but do not establish a transferable semantic coordinate. Full-donor addition produces `outside`, yet subsequently explicitly discusses the dog; legs still starts `4`. That is not coherent replacement. Numerical verification is not semantic certification.

## Drift / contradiction check
Donors all end in token1049, ` It`; causal inputs end in token220, space, or279, ` the`. Preparation mismatch, application position, and semantic sufficiency are distinct hypotheses.

The installed Qwen3.5 implementation starts from unscaled token embeddings and uses additive residual connections (`modeling_qwen3_5.py:1168,1202,765–794`). Thus subtracting the current embedding removes a genuine direct residual contribution—not all token/context dependence.

## Recommendation
**Yes: preregister embedding subtraction as exactly one paired candidate**, not an established correction:

\[
a_{\mathrm{emb}}=(h-c)u+(e_{\mathrm{It}}-e_{\mathrm{current}})u,\qquad
h'=h-2\min(a_{\mathrm{emb}},0)u.
\]

Keep the old \(u,c\); do not subtract embeddings from the update itself. During decoding, “current” means the token being processed, not the predicted next token.

For matched pairs sharing the final token, this correction shifts both margins equally: **it cannot repair their ordering**. At ` It`, it must reproduce raw margins exactly. These are useful falsification checks.

### Exact prerequisite
Cross two referent styles with four endings: **eight dog/spider pairs**.

Prefix: `"The record concerns {referent}"`

Referents:
- Explicit: `"a dog"` / `"a spider"`
- Indirect: `"the animal that barks"` / `"the animal that spins silk webs"`

Endings:
1. `". It"`
2. `". This animal"`
3. `". A note about it is "`
4. `". The observer describes the"`

These are generic referent contexts, not causal-question paraphrases. Preserve exact strings, token IDs, embeddings, and all-position raw layer16 states. Report raw/corrected final-position margins and pair differences; earlier positions are diagnostic only.

### Outcome → next causal decision
- **Corrected dog<0<spider in all eight pairs:** proceed to one frozen corrected-reflection test on both causal relations, retaining layer16, final-position prefill, continuous decode and unit strength. Compare Base/raw/corrected/random; require both requested answers and coherent continuations. Raw performance is reported, not used to tune the correction.
- **Any corrected failure:** do not launch that candidate causally or rerun already-failed raw midpoint unchanged. Ordering failures implicate direction/context transfer; preserved ordering without bracketing implicates centering. Earlier-only separation implicates position, but does not authorize retrospective position selection.

## Risks
Contextual residual terms can still dominate. Eight pairs provide a prerequisite, not generalisation evidence. Random controls are not trajectory-matched after divergence. Successful bracketing cannot establish causal semantic sufficiency.

## Need from main agent
None within approved scope. No implementation handoff warranted.

— **PI/OpenAI**