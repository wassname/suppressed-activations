# Continuous concept replacement: scientist brief

Written by Codex/GPT-6. No tools needed: all relevant context is below. Review the method, not writing style. Return under700 words plus marked-up pseudocode. Identify the strongest misconception, a concrete alternative, and cheapest matched discriminator. Do not equate a changed first digit with success.

Goal from wassname: coherently replace the implicit spider concept with dog or ant, preserving continuous steering and coherent continuation. Suppressed-subspace causality and genuine post-edit source readout remain unproved. Do not substitute direct answer-token forcing. The unchanged prompt is `Fact: The number of legs on the animal that spins webs is `, in an official assistant-prefill template, with instruction to complete then explain. Clean base says8/spider; clean donors identify dog4 and ant6. Intended counterfactual identity is not itself incoherence; reversals, invented riddles, wrong unrelated biology and repetition are failures.

Current corrected estimator uses16 fixed WikiText records truncated to128 content tokens. Final raw residual L32 before RMSNorm. Gain-weighted output rows. Source positions exclude prefix and final token; future target positions are same valid set. Reference estimator sums later targets and averages sources. Three concept rows only, not full vocabulary J-lens. Raw final RMS denominator is not differentiated: contracted rows measure mean-J then gain-weighted unembedding, not local normalized logit gradients.

Evidence: corrected L12/L16 unprojected C1/C2 each makes the target digit top1. But all inspected full continuations fail: dog retracts or invents riddles; ant returns to spider/eight or becomes beetle. Gate does not fix them. L24 projected into rank4 suppressed span retains8. Full L12/16/20/24, ranks0/4, C0/.5/1/2/4 grid is running. Last3 prefill plus EVERY decode token through EOS/128tokens; coverage assertions and C0 identity pass. Model is bfloat16. Autograd33.2435 vs finite difference33.2150 at epsilon.5 on one corpus example; split-half cosines.868–.979. These validate estimator plausibility, not semantics.

Suppressed selector: vocabulary scores=min(positive centered rise from early to peak, positive centered fall from peak to output32). Per-position top8 gain-weighted unembedding rows yield orthonormal spans; average their projectors across last4tokens; retain rank4; union source/donor spans. A scan of8windows × last8positions × raw/unit-row scoring did not find named animal forms in top8 on question prompts; original fact dog donor has one cell, source and ant none. Thus this selector is doubtful. Earlier layer-local contrast attenuation plus species correction yielded selected coherent dog/ant examples but fails generalization. We do not want another animal-specific correction.

```python
# Current method; conceptual notation, not executable Python.
model = Qwen3_5_4B                         # 32 layers
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
            Jrow[text, layer, word] = mean(
                grad(objective, H[layer])[valid], axis=0
            )

V = mean(Jrow, axis="text")                # layer × word × hidden
check_finite_differences(V)
check_split_half_stability(Jrow)

for target in ["dog", "ant"]:
    pair = V[layer, ["spider", target]].T
    pair = normalize_columns(pair)
    if use_suppressed_projection:
        U = persistent_suppressed_span(source, donor)
        pair = normalize_columns(U @ U.T @ pair)

    def edit(h):
        coordinates = h @ pinv(pair).T
        delta = coordinates.flip(-1) - coordinates
        if source_dominant_gate:
            delta *= coordinates[source] > coordinates[target]
        return h + strength * delta @ pair.T

    patch_last_three_prompt_tokens(edit)
    patch_every_generated_token(edit)
    save_full_generation_and_edit_trace()
    evaluate_number_identity_contradictions_repetition()

# Proposed comparison: stop at a donor-derived contrast, not an overshoot.
margin = measured_clean_donor_contrast(pair)
edit_alternative = minimum_norm_change_to_reach(margin)
# Compare at fixed layer and corpus; do not count a forced digit as success.
```

For a unit two-column pair, pseudoinverse coefficient swap and dot-product swap are equivalent (Gram matrix commutes with exchange). d=source-target becomes(1-2C)d; C2 is threefold sign-reversing extrapolation. Gate prevents immediate re-edit of identical state but new tokens can recreate source dominance. These are checked algebra, not open bugs. Proposed donor margin is not implemented; discuss whether it preserves semantic state or merely another lexical bias. Also suggest a more distinct intervention if appropriate. Rank hypotheses and give falsifiable predictions, not an exhaustive checklist. Mark only genuinely doubtful pseudocode lines; do not call the sketch's omitted plumbing a code bug.
