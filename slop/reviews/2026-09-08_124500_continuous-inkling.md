Strongest misconception: treating a corpus-derived two-column gradient contrast as a causally steerable “spider→dog/ant” concept axis. The arithmetic checks (autograd vs. FD ~33.24 vs ~33.21; split-half cos ~0.87–0.98) validate gradient estimation, not semantics. L12/L16 unprojected C1/C2 do push digit 4/6 to top-1, but full generations fail: dog retracts or invents riddles; ant returns to spider/eight or becomes beetle; L24 projected into the rank-4 “suppressed” span retains 8. The selector scan (8 windows × 8 positions × raw/unit rows) never retrieved named animals; the span is likely noise. The gate (`coordinates[source]>coordinates[target]`) compares interpolation coefficients, not semantic readouts, and allows regeneration of source dominance on new tokens. Continuous injection on every decode token therefore looks like local logit bias, not preserved-state causality.

Concrete alternative: abandon per-token coefficient-flip overshoot (C2 is 3× sign-reversing: d→(1-2C)d). First, use causal tracing/path-patching to locate the actual readout head/circuit for “spins webs” → spider (likely near L24, not L12/16). Apply a single discrete donor-margin patch there—minimum-norm projection to the clean donor mean, not overshoot—only when a semantic discriminator detects source presence. Restrict to that point; let autoregression propagate. If that fails, the axis is lexical, not conceptual. A more distinct fallback is direct counterfactual framing at the prompt level (excluded by design, but mechanistically honest).

Cheapest matched discriminator: do not score digit change alone. Pair-edited vs. clean-donor runs, then regex-extract (digit; animal nouns; “web/spin/spider” leakage; “riddle/retract/actually”; leg-property consistency). Success requires digit-animal-property alignment, zero source leakage, and coherent explanation—else failure. This is deterministic, cheaper than an LLM judge, and tests the claimed semantic preservation.

Ranked falsifiable predictions:
1. Single-point donor-margin patch at L24 yields coherent dog/ant continuations without retraction; if not, the axis is bias.
2. Suppressed-span projection reduces source retention; observed L24 retention of 8 already falsifies.
3. Gate fails: source coefficient dominance recurs on decode tokens 4–10, explaining reversions.
4. The regex discriminator classifies all current C1/C2/C0/C.5/C1/C2/C4 runs as failures despite correct first digit.

```python
# Marked-up pseudocode; #?? flags genuinely doubtful logic only.
model = Qwen3_5_4B
words = [" spider", " dog", " ant"]
layers = [12, 16, 20, 24]
corpus = fixed_wikitext_sample(16)
gain = 1 + final_norm.weight
rows = unembedding[words] * gain

for text in corpus:
    tokens = official_assistant_prefill(text[:128_tokens])
    valid = content_positions_except_final(tokens)
    H = forward_with_grad(tokens)
    for word in words:
        objective = sum(H[32, valid] @ rows[word])
        for layer in layers:
            #?? gradient averaged over mixed positions; validates arithmetic,
            #   not that H[layer] carries causal concept geometry
            Jrow[text, layer, word] = mean(
                grad(objective, H[layer])[valid], axis=0
            )

V = mean(Jrow, axis="text")
check_finite_differences(V)
check_split_half_stability(Jrow)

for target in ["dog", "ant"]:
    pair = V[layer, ["spider", target]].T
    pair = normalize_columns(pair)
    if use_suppressed_projection:
        #?? selector never retrieved named animals in scan; span likely noise
        U = persistent_suppressed_span(source, donor)
        #?? L24 projected retains 8; projection does not suppress source
        pair = normalize_columns(U @ U.T @ pair)

    def edit(h):
        coordinates = h @ pinv(pair).T
        #?? coefficient flip is 3x overshoot/sign-reversing for unit pair
        delta = coordinates.flip(-1) - coordinates
        #?? gate compares interpolation weights, not semantic dominance;
        #   new tokens recreate source dominance, causing reversion
        if source_dominant_gate:
            delta *= coordinates[source] > coordinates[target]
        return h + strength * delta @ pair.T

    #?? continuous injection on every token decays; generations retract
    patch_last_three_prompt_tokens(edit)
    patch_every_generated_token(edit)
    save_full_generation_and_edit_trace()
    #?? digit-only check misses retraction, invented riddles, leakage
    evaluate_number_identity_contradictions_repetition()

# Proposed comparison (untested):
#?? unimplemented; may still be lexical bias, not semantic state
margin = measured_clean_donor_contrast(pair)
edit_alternative = minimum_norm_change_to_reach(margin)
# Compare at fixed layer/corpus; do not count forced digit as success.
```

Proposed donor-margin edit is conceptually cleaner than C2 overshoot but remains unproven; without the causal-tracing locator and the regex discriminator, it risks being another lexical interpolation. The method’s core error is geometric optimism—assuming a mean-gradient pair defines a continuous concept—while the generation dynamics and suppressed-selector failure show it does not.