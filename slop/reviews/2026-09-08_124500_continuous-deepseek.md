**Strongest misconception**  
The core error is the belief that a static linear intervention—computed from a small-corpus gradient average and applied uniformly to *every* token of an autoregressive generation—can implement a coherent, continuous concept replacement. The method assumes that swapping the two-dimensional coordinates (or equivalently applying the derived matrix) across all positions will yield a stable counterfactual. In practice, the edit’s effect accumulates and interacts with the model’s nonlinear dynamics, leading to retractions, riddles, and semantic collapse. The reported failures (dog becomes a riddle, ant reverts to spider) are direct evidence of this overshoot and non-stationarity. The misconception is not the estimator’s validity per se, but the extrapolation from a local linear approximation to a persistent, arbitrary edit across an entire generation.

**Concrete alternative**  
Instead of a fixed edit that blindly swaps coefficients at every step, constrain the intervention to match a *measured margin* from clean donor contexts. For a given concept pair, compute the typical coordinate contrast (e.g., donor coefficient minus source coefficient) observed in clean completions about the donor. Then, during generation, apply the minimal-norm change that brings the current state to that margin—only if the state drifts dangerously close to the source side. This can be done by:
1. Estimate clean donor contrast $m$ on a held‑out set of donor‑prompt completions.
2. At each token, compute the current projection onto the source‑donor direction.
3. If the signed distance to the target side is below $m$, edit with a soft or clipped push, not an exact swap, to avoid overshoot.

This preserves more of the native model dynamics while still steering away from the source concept. It is still a lexical bias, because the margin is derived from lexical co‑occurrences, but it is less likely to force the model into incoherent extrapolation. A more distinct intervention would apply edits only at layers where source‑donor separability is highest (e.g., a single middle layer) and let the model’s recurrent processing propagate the change, combined with a run‑time detector that pauses editing if the source concept re‑emerges.

**Cheapest matched discriminator**  
The cheapest discriminator that directly targets the listed failure modes (reversals, wrong biology, repetition) is a simple token‑set blacklist. After generation, scan the output for the presence of any token from the *source* concept’s vocabulary: “spider,” “web,” “8,” “eight,” “arachnid,” etc. If any appears, the intervention is judged a failure—no expensive parsing or model‑based evaluation needed. This can be extended to a token‑by‑token run‑time check to abort generation early, preserving compute.

---

**Marked‑up pseudocode**  
The following highlights genuinely doubtful lines (not missing plumbing) with `# ❗` marks.

```python
# ❗ The entire patch regime assumes a static coordinate‑swap edit will remain coherent;
# the generational failures are directly caused by this overshoot.
def edit(h):
    coordinates = h @ pinv(pair).T          # ❗ Pseudo‑inverse may amplify noise in low‑rank subspace
    delta = coordinates.flip(-1) - coordinates
    # ❗ Swapping coefficients produces a d = source‑target vector; applying full delta causes
    #   threefold extrapolation when C² is large, destabilizing semantics.
    if source_dominant_gate:
        delta *= coordinates[source] > coordinates[target]
    return h + strength * delta @ pair.T    # ❗ Fixed strength and full delta ignore clean donor margin

patch_last_three_prompt_tokens(edit)        # ❗ Assuming a 3‑token static edit suffices for distinct concepts
patch_every_generated_token(edit)           # ❗ Applies identical transformation to all positions, ignoring
                                            #   autoregressive state evolution and residual buildup.

# Proposed replacement with donor‑margin control (conceptual):
margin = measured_clean_donor_contrast(pair)   # e.g., average (coordinate_donor - coordinate_source) in clean donor contexts
def edit_constrained(h):
    c = h @ pinv(pair).T
    current_margin = c[target] - c[source]
    if current_margin < margin:
        needed = margin - current_margin
        # Minimal‑norm change along d = target - source direction:
        d = pair[:, target] - pair[:, source]
        h = h + (needed / (d @ d)) * d   # ❗ Still assumes linear push; margin must be validated on OOD editing
    return h
```

The alternative avoids the coordinate swap and instead enforces a local margin derived from clean donor behavior. It remains to be validated whether this merely imposes a weaker lexical bias or genuinely preserves semantic coherence.