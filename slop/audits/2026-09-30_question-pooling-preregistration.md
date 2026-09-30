# One question-position pooling attempt

PI/OpenAI. Contract: `slop/reviews/2026-09-30_after-token-kl-next-test.md`, settled by supervisor dialogue with58d27bd2. Both goals remain open. Token-KL and the failed2628 coordinate stay retired unchanged.

## Question and method

Does a hidden bridge appear while its clue is being processed, rather than at the final answer position? Keep existing probability excess, fixed layers and k32; change aggregation over positions only.

```python
I = non_special_tokens_fully_inside_case_text(full_prompt_offsets, prefix_length)
p_R = softmax(readout(states[I]), dim=vocabulary)
q = softmax(final_layer_state_at_last_prompt_position)
s = max(p_R, dim=position) - q
s[s <= 0] = -inf
s[full_prompt_word_mask | greedy_final_word_mask] = -inf
selected = stable_descending_token_id_order(s)[:32]  # finite entries only -- PI/OpenAI
```

The full prompt is tokenized once with offsets and used unchanged for generation/masking. Boundary-straddling tokens are excluded; the final prompt token must be included. No language labels, hidden aliases, generated words or clue annotations determine the span or ranking. Final-LAST distribution is constant across positions; position-local final distributions are NOT used. The prefix's contextual effect remains, even though its positions cannot win pooling.

J24, plain24 and plain27 receive identical pooling. Controls are stable-ranked last-position probability excess, pooled cyclic-next-case final subtraction with current-case masks, and pooled unsubtracted probability. Half-erased plain27 remains visible as the incumbent, never composed with pooling. Stable score ties use token IDs; peak-position ties use earliest eligible position.

## Budget and parity

One default-queue local job:300s TERM plus15s kill grace. Eight existing v4 development prompts, each one <=8-token generation, at most64 tokens. No intervention, fitting or preliminary current-input pass. `generate_readout` already captures the full prefill during the scored generation; now persist it instead of discarding earlier positions. Model/backbone guards reject any transformer call during the subsequent scoring phase.

Before interpreting results, generated IDs and all three last states must equal `out/2026-09-30_142814_jlens-one-pass`. The launcher requires all168 existing readout rows to reproduce `out/2026-09-30_151032_jlens-one-pass`. Unchanged historical scoring retains its defects; fix only misleading report labels/replay wording. No source prompt or alias edits.

Main, launcher and case JSON are copied from the frozen commit. The launcher checks fixed hashes of five imported project helpers before execution, checks again afterward and copies their bytes into the run. Artifacts: full prefill states, boundaries/offsets/input IDs, generation coverage, masks, selected and scored-alias peak positions/probabilities/final comparator/scores, per-case metrics, summary and prospective selection. Full-vocabulary optimality is tested on synthetic data, not independently reconstructed from the production component subset.

## Decision

Select the pooled representation with highest alias-checked joint count; ties plain27 > J24 > plain24. Numeric screen: >=7/8, strictly above its own last-position and mismatched controls. AUROC/evaluable denominators stay unchanged; wrong/unscorable cases remain. Before new examples, require symmetric blinded semantic review with no definite input/said leakage among the selected winner's counted passes. No switching winner. Comparable unsubtracted performance blocks a subtraction-benefit claim. Hidden-only improvement is not success; no window/layer/k tuning after a failure.

## Expectations and checks

- Location limitation (roughly55%): earlier peaks should add hidden bridges such as Hamlet/hydrogen while leaving generations unchanged. This does not predict the joint gate necessarily passes.
- Broader topic/input/answer collection (roughly70%, overlapping): hidden-only hits increase but leakage grows; mismatch/unsubtracted controls may tie. That rejects this candidate, not all positional readouts.
- Arithmetic/dataflow error (roughly3% after CPU checks): mismatched states, old-row drift or local-final substitution. Reference equality and saved peak provenance distinguish it.
- Unknown mechanisms remain plausible; eight dependent, repeatedly examined cases are development, not a generalisation result. Generic sparse-clamp reproduction remains deferred because the reference executable is unavailable.

`2026-09-30_question-pooling-check.py` passed seeds0/1: full-vocabulary score reconstruction, constant comparator, singleton identity, shift invariance, masks/stable sorting; tiny real32-layer hybrid Qwen with pinned tokenizer, actual capture/I/O and all12 production pooling branches; exact legacy last scores and rejection of changed reference states. Final process proc_005b exited0 after114s; this also covers exact token/position ties, fewer-than32 eligible tokens, model/backbone scoring guards and saved failure evidence before parity assertions. Full main and full-size BF16 parity are still untested and fail closed in this run. No GPU result yet.
