# Oracle opinion: readouts for "thought but not said"

**Model: Muse Spark.** Using only the brief above. Observations = given; inferences = mine.

## Most diagnostic observation

> Removing top-5/20 final-layer words barely changes translation F1 but collapses English v4 F1 (.184 → .061).

Inference: in translation, hidden vs. spoken are separated by a large, generic feature — language ID / script / token-language statistics. In all-English two-hop, hidden (Sweden, Thursday) and spoken (Stockholm, Friday) are same-language semantic neighbors, often co-activated. Any method that scores by "English tokens present mid-network but absent at output" will transfer poorly because it learned language detection, not suppression. This is corroborated by: plain lens works in translation (.446) but not English (.056); J-lens lists contain same-category alternatives; generic variance subspaces read as punctuation.

Secondary diagnostic: without output filtering, spoken answer is in top-8 for 11/16 (plain) and 14/16 (J-lens). So in English the problem is *exclusion of speech*, not recall of thought. The current score (top-k contains hidden, excludes spoken/input) rewards language filters and punishes semantically correct neighborhoods.

Framing concern: "the hidden word" assumes a single lexicalized intermediate. The Thor → Thursday failure (reads Norse/Odin/Loki at "Thor") shows compositional cases have distributed/noisy intermediates. Top-k exact-match F1 against one string will underrate a correct subspace that surfaces a cluster (Thursday + weekday manifold) and overrate a language detector. I would add a secondary metric: rank of hidden minus rank of spoken, plus category-level credit (e.g., hidden in top-k *after projecting out the output direction*, see below).

## Proposals, priority order

**1. Output-orthogonalized Jacobian readout.**
Construction, no inference labels: offline, collect final-layer predicted top-m tokens on fitting prompts (WikiText + translation prompts, ~300–1000 texts). Let $U_S$ = span of their unembedding rows. $P = I - U_S(U_S^TU_S)^{-1}U_S^T$ (or whitened variant). Readout: $\text{logits} = W_U \, \text{norm}(P J_{29} h_{29})$.
Fitted on: unlabeled WikiText + held-out translation inputs; output words come from the model's own final predictions, not labels.
Why transfers: it directly attacks the diagnosed failure — speech dominates late-layer J-lens lists. Unlike deleting top-5/20 discrete tokens (which also deletes semantic neighbors like Thursday when Friday is removed), subspace projection removes the *shared* output direction while preserving orthogonal within-category variance (Thursday ⟂ Friday-shared-weekday-direction, ideally).
Falsifier: compute cosine between hidden-word and spoken-word unembedding rows projected through $P$; if median cosine stays >0.7, or translation F1 survives but English F1 stays ~0 while hidden rank is high pre-projection and low post-projection, kill it.

**2. Suppression-vector (causal rise-then-fall) readout.**
Construction: for each fitting prompt, compute per-token logit-lens deltas $\Delta^+ = \ell_{27}-\ell_{22}$ (rise) and $\Delta^- = \ell_{32}-\ell_{27}$ (fall). Define suppressed set $S$ = tokens in top-rise ∩ top-fall *that are also predicted by a linear probe of $h_{27}\to(h_{32}-h_{27})$*, i.e., fit ridge $A$: $h_{27} \to \Delta h$ on WikiText, keep fall explained by $A$ (model-driven suppression) vs. noise. Readout at test: rank by $\min(\Delta^+,-\Delta^-)$ restricted to $A$-explained fall.
Fitted on: WikiText activations only, no language labels.
Why transfers: generic rise-and-fall failed (top-32 F1 .164→0) because any token decaying looks the same. Conditioning on *predictable* suppression isolates active erasure (late MLP/attention undoing an intermediate), which should occur for Sweden→Stockholm as much as English→Chinese.
Falsifier: if $A$ predicts $\Delta h$ with $R^2\approx 0$ on held-out English two-hop prompts, or if $S$ on translation is dominated by source-language tokens rather than the English bridge (check: is French input also rise-and-fall?), reject.

**3. Cross-lingual invariant (contrastive) subspace.**
Construction: take translation prompts sharing the same hidden English word but different source languages (French→Chinese vs. Spanish→Chinese, or French→Chinese vs. French→Arabic). Compute $d = h_{27}^{(a)} - h_{27}^{(b)}$ at last prompt token; the *nuisance* subspace = top-PCs of $d$ across pairs; keep orthogonal complement $Q$. Readout: logit/J-lens in $Q$: $W_U\,\text{norm}(Q J h)$ or $W_U\,\text{norm}(Qh)$ via tuned lens.
Fitted on: translation pairs only, language labels used only to form pairs offline, never at inference.
Why transfers: subtracting across source languages cancels source-language ID while preserving shared English bridge. Unlike Cov(h27)−Cov(h32), which kept generic high-variance punctuation, this explicitly removes language variance, forcing the remainder toward content.
Falsifier: if within-hidden-pair distance ≈ across-hidden-pair distance in $Q$ (no clustering by hidden word on held-out pairs), or if $Q$ readout top-k is still script-pure (all-Chinese/all-French), reject.

**4. Clue-position-anchored, output-residualized probe.**
Construction: read at end-of-clue ("Gothenburg"), not last prompt token. Offline fit linear ranker $w_t$ per candidate from $h_{27}^{clue}$ on translation data with distant supervision (hidden = dictionary English gloss), then at test score $s_t = w_t^T h - \alpha \cdot \cos(e_t, \hat{y}_{final})$ where $\hat{y}$ = final-layer prediction direction. Evaluate at clue position.
Why transfers: brief shows clue-position helps for attribute hops (Sweden) — the hidden item is cleanest before the composition step overwrites it. Residualizing against the final output handles cases where clue and output positions merge.
Falsifier: if clue-position hidden rank on compositional English items (Thor→Thursday) is at chance, the method reduces to entity-attribute lookup; test attribute vs. compositional split — no gain on compositional ⇒ demote to special case.

I would test in order 1, 3, 2, 4. Total compute: only cached $h$, $Jh$, $W_U$ products plus small SVDs/ridge fits — minutes on 24GB.

— Muse Spark