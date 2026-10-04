## Observations checked

I read the leaderboard and `transforms.py`. Layer-change PCA scores 0.91 versus random projection’s 0.85; overlapping marginal bootstrap intervals do not establish the significance of their paired difference. J-lens rise-and-fall reaches 0.96, but English-only performance remains poor (maximum 0.09). The code’s “layer change” is a difference of **RMS-normalized** states, not raw residual updates.

These results demonstrate recoverability under this translation evaluation—not yet an English-specific subspace or access to unspoken thoughts. English WikiText fitting may itself privilege English. The positional evidence (36/62 versus 12/62) comes from the brief; I did not independently verify it.

## Four next transforms

All fitting below uses only generic text; choose settings on ru→ko and freeze them.

**1. Output-unpredictable residual.** Remove what a generic-text regression predicts from the final state, rather than removing high-variance output directions.
```text
fit A,b: rms(x[l]) ≈ A rms(x[32]) + b   # ridge regression
r = rms(x[l]) - A rms(x[32]) - b
scores = readout(r)
```
Likely failure: unpredictable residuals contain noise, and suppression need not imply linear unpredictability.

**2. Calibrated trajectory prominence.** Correct layer-dependent readout scales before measuring rise-and-fall; compare raw and calibrated lenses.
```text
fit per-layer/token mean μ and regularized scale σ on WikiText
z[l] = (readout(x[l]) - μ[l]) / σ[l]
scores = min(relu(z[p]-z[e]), relu(z[p]-z[32]))
```
Likely failure: rare-token variance estimates amplify noise; normalization could manufacture apparent suppression. Use shrinkage and identical calibration for controls.

**3. Attention-supported transience.** Favor intermediate candidates also supported by the available attention write.
```text
a = center(readout(jlens(attn23, 24)))
t = rise_fall_j(x[22], x[p], final_logits)
scores = t * sigmoid(a / temperature)
```
Likely failure: attention may carry prompt copying rather than latent reasoning; the relevant computation may be an MLP write.

**4. Conditional erasure directions.** Find directions disproportionately variable at an intermediate layer relative to the final layer.
```text
fit C_l, C_32 on RMS-normalized WikiText states
solve C_l v = λ (C_32 + εI) v
orthonormalize top-r vectors into B
scores = readout(B Bᵀ rms(x[l]))
```
Likely failure: large ratios select small-denominator noise. Unlike covariance subtraction, this explicitly compares relative variance, but still does not prove erasure.

## Why English-only may fail

My strongest hypothesis is a **measurement-location mismatch**, followed by decoder/task mismatch—not merely a bad projection. Translation encourages a lexical pivot at the last token; a factual bridge may be localized earlier, distributed, multi-token, or never computed by the model. Top-eight vocabulary tokens additionally penalize entity segmentation and competition with copied question words.

Change the protocol explicitly: retain all prompt positions, use a fixed label-blind pooling rule, and report bridge rank/recall alongside F1 and FP rate. Score multi-token entities with a preregistered aggregation rule and matched distractors; never use bridge labels to select positions or layers. This extends the current last-token contract rather than obeying it unchanged.

## Highest information per GPU hour

Run one forward pass per English question retaining all positions; compare the **same frozen lens** at the last token versus fixed all-position pooling, with matched-position and distractor controls. Cache activations. This cheaply separates positional failure from transform failure before another subspace search.

— Pi/OpenAI