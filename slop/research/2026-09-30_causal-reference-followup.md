# Causal reference distinctions to retain in the next decision

— PI/OpenAI. Read while2642 waits; no new method approved or inference queued.

Source: the existing local paper copy `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`, not newly checked against the live publication. Earlier audit: `slop/reviews/2026-09-30_reference-intervention-comparison.md`.

At line220 the paper copy specifies the two-direction writing operation:

> Given a source token $s$ and target token $t$, we form $V = [v_s\; v_t]$, read the lens coordinates $c = V^\dagger h$ (where $V^\dagger$ is the pseudoinverse of $V$), and set $h_{\text{patched}} = h + V(\sigma(c) - c)$, where $\sigma$ swaps the two entries of $c$ (optionally scaled by a factor $\alpha$). The component of $h$ orthogonal to $\text{span}\{v_s, v_t\}$ is unchanged.

At line196 sparse decomposition is a different operation:

> Given an activation (or a steering vector, or an SAE feature direction), we solve for a sparse nonnegative combination of $k$ J-lens vectors that approximate it well using gradient pursuit

At line358 the paper uses that decomposition on broader learned intermediate probes, not only two selected token directions. At line366, the complementary-component control is described as:

> with the J-space coordinates of the intermediate concept\footnote{Defined as the tokens comprising the intermediate concept probe's J-space component, and the token directly naming the concept if not already present.} clamped to their clean-pass values, it falls to 6\%.

That clean-pass control is not automatically admissible under our no-preliminary-current-input-pass rule. Do not conflate it, sparse decomposition, a pair-coordinate swap, and an invented current-state clamp.

The earlier review already noted that our swap directions were unit-normalized, an additional choice not specified in the quoted writing equation. Our raw-score swap is also not a raw-coordinate swap. This is not a newly discovered bug: it is an unresolved implementation-choice boundary. The supplied executable reference still does not specify the complete causal procedure; no faithful-reproduction claim follows.

The paper copy's line1416 also says:

> Swaps on country facts redirect the model's answer almost perfectly. Swaps on months succeed partially, animals rarely, and number relations never succeed at $\alpha$ = 1.

These are author-reported results from a different model and experiment. They argue against treating repeated spider/dog failures as a universal verdict on the method. They do not justify a selected strength/layer rescue, nor establish an English hidden-intermediate method: explicit-argument country swaps in that section are a different assay from recovering a country absent from the input.

Possible future decision, not an approved test: a bounded hidden-country transfer across two distinct properties may be more informative than another animal spelling/strength variant. It would need fixed implicit cues, unspoken target identities, correct baselines, offline/current-layer-only editing, the same intervention across properties, and matched controls. Settle the actual algorithm and timing first; do not invent sparse/clamping details from these excerpts.
