**Central assumptions**  
The implicit concept “spider” is represented linearly in the hidden states at the last prompt tokens.  
A vector difference between a clean source run and a donor run captures the direction that shifts the concept, and a simple addition to the hidden state can flip the model’s implied animal while preserving fluency.  
The suppression space (from vocabulary scores) is intended to isolate components that control the concept, but this is unvalidated.  

**Confounds and missing controls**  
- **Unembedding‑row directions** – Using centered unembedding rows times RMS gain is weak; a control is to compare with random directions or directions from unrelated animals.  
- **Intervention scope** – Applying the patch to *all* generated tokens recursively modifies the context and degrades coherence. A control is to patch only the prompt tokens (e.g., the last three) and let the model decode freely.  
- **Magnitude calibration** – The same scaling C is used everywhere; no baseline is given for “natural” coefficient ranges. Test with C=1 on a *non‑target* animal (e.g., “cat”) to ensure specificity.  
- **Donor contamination** – Explicit‑prompt donor directions may carry unwanted associations (social insects, barking). Orthogonalizing against the source direction should be tested.  
- **Factual inconsistency** – The web‑spinning prompt contradicts the ant/dog identity. Coherence may require the model to override the clue; this inherent tension should be measured separately (e.g., by asking the model to explain the contradiction).  

**Mathematical issues**  
- **Coefficient extraction** `c = pinv(V) @ h` is not robust when the two columns of V are correlated. Use orthogonal projection (`P_V h`), then extract coordinates after orthogonalizing the basis.  
- **Reflection operator** swaps both coordinates; it can over‑correct when the target coefficient is already larger. The source‑dominant‑only swap (`d = max(c_spider - c_target, 0)`) is safer.  
- **No renormalization** after the additive patch; large C values (2,4) cause norm inflation and likely degrade quality.  
- **Unembedding‑based v vectors** – The unembedding rows (even after RMS gain) may reside in a different subspace than the hidden states at layer 24. A better proxy is the **mean activation difference** from explicit counterfactual prompts.  

**Prioritized next experiment**  
*Objective*: Achieve a stable ant‑leg‑count (6) with a coherent ant/non‑spider continuation, without the “social spider/bee” leakage reported earlier.  
*Approach*: Use the hidden‑state difference between an explicit spider prompt and an explicit ant prompt, **orthogonalized** to the source prompt’s hidden state, and **apply it only to the prompt tokens** at a single late layer.

*Why this fixes earlier failures*:  
- The explicit‑prompt difference isolates the animal‑identity shift more cleanly than unembedding rows.  
- Orthogonalization removes the component that simply reinforces the spider direction, preventing the “social spider” leakage.  
- Restricting the patch to the prompt tokens avoids recursive perturbation of the autoregressive stream.

---

**Annotated pseudocode for the proposed intervention**

```python
# 1. Collect hidden states from a clean source run on the *implicit* prompt
h_src = hidden_states_at_prompt_tokens(source_implicit_run)  # [n_tok, d_model]
# Use the average over the last 3 prompt tokens as the source concept vector
v_src = normalize(mean(h_src[-3:], dim=0))                   # unit length

# 2. Run explicit prompts that name the animal directly
#    e.g., "Fact: The number of legs on a spider is"
#          "Fact: The number of legs on an ant is"
h_spider_exp = hidden_state_last_token(spider_exp_prompt)    # [d_model]
h_ant_exp    = hidden_state_last_token(ant_exp_prompt)       # [d_model]

# 3. Donor direction = ant - spider, then remove projection onto v_src
v_donor_raw = normalize(h_ant_exp - h_spider_exp)            # unit rough shift
v_donor_clean = normalize(v_donor_raw - dot(v_donor_raw, v_src) * v_src)  # orthogonal to spider

# 4. Intervention: add a scaled version of the cleaned donor direction
#    to the hidden states of the last prompt tokens at layer L, then resume generation
C = 1.0   # initial test value
hidden_state_prompt[L, -3:] += C * v_donor_clean   # only on 3 final prompt positions

# 5. Continue autoregressive decoding without further patches.
#    Measure leg‑count probability (target p6), readout, and full continuation text.
```

*Ablation controls for this experiment*:
- Replace `v_donor_clean` with a random orthogonal direction (same norm) to confirm specificity.
- Test C ∈ {0.5, 1.0, 2.0} to find a magnitude that gives reliable leg counts without garbling.
- Repeat with dog donor to see if 4‑leg output emerges cleanly.

This design avoids sweeping over every layer combination, directly addresses the earlier “social spider” leakage, and respects the constraint of minimal changes to the existing pipeline.