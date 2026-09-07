# Improve coherent suppressed-concept intervention

Written by Codex/GPT-6. Review the method and propose a short sequence of high-information
experiments. No tools needed: this brief contains the experiment and evidence. Under700
words plus annotated pseudocode. Return central assumptions, confounds and controls,
annotated pseudocode, mathematical issues, and one prioritized next experiment.

Goal: Qwen3.5-4B,32 layers, implicit spider concept replaced with ant/dog while original
prompt stays fixed. We want target leg-count6/4, corresponding recomputed suppression
readout, and coherent continuation. Use official assistant-prefill chat template:
`Fact: The number of legs on the animal that spins webs is `.
Clean ant donor describes colony/pheromone trails; clean dog donor describes barking.
Clean source produces8 p=.943; ant donor6 p=.900. Same pinned model/tokenizer throughout.

Current extraction and intervention:
```python
scores[t] = suppressed_vocab_scores(hidden_layers[:, t])
# score = min(relu(logit_peak-logit_early), relu(logit_peak-logit_output))
# logits use RMS norm gain, centered normalized vocab directions
B[t] = span(top_vocab_directions(scores[t]))
# Actual patch bases use centered UNNORMALIZED unembedding rows times norm gain.
P = mean(B[t] @ B[t].T for t in last_prompt_tokens)
U = leading_eigenvectors(P)  # implemented with thin SVD of concatenated B

V = normalize_columns([v_spider, v_target])  # optionally projected into shared U
c = pinv(V) @ h
h += C * V @ (reverse(c) - c)

# Candidate: source-dominant-only swap
d = max(c.spider - c.target, 0)
h += C * d * (v_target - v_spider)  # alternative, NOT additional to current swap
```
v_spider and v_target are centered unembedding rows times final RMS gain, normalized
to unit length. They are NOT J-lens vectors. P is from last4 prompt tokens, shared
source/donor span retained4+4 directions. Raw V bypasses suppression-space projection.
At L24, patch last3 prompt tokens and ALL31 cached decode steps predicting32 outputs.
No residual renormalization. C0 exact identity and hook coverage verified. Float32
coordinate equation errors <7e-6; traces are before bf16 cast. C1 is a reflection;
larger C extrapolates. It can reverse target-dominant states back toward source.

Full grid24: two animal targets, raw/projected directions, C0,.25,.5,1,2,4.
Raw ant C4: p6=.0286, p8=.8344, readout ant variants; full continuation:
`8.\n\n**Explanation:**\nThe animal that spins webs is an **ant**. Ants belong to the class *Insecta* (insects).`
Raw dog C2: p4=.4633,p8=.4088; full continuation:
`4.\n\n**Explanation:**\nThe animal that spins webs is a **dog** (specifically, a spider). Spiders are classified as arachn`
Projected ant C4 gives2 and punctuation readout; projected dog C4 p4=.608 but mixed
dog/spider. Three dog conditions give4, no ant condition6. These are development
prompts. Positive digit alone is not success. No fresh random controls for this grid.

Earlier fixed displacement in shared U (mean donor minus mean source) gives ant6
but social spider/bee wording; source-removal alone stronger than donor replacement.
Thus neither operator nor named direction estimator is well-established.

NOW QUEUED: raw named swaps L4,8,12,16,20,24 x C0,.25,.5,1,2,4, same continuous
coverage, each animal36 conditions. Approx2s/condition after load. GPU shared queue.

Assess next choices: source-dominant-only swap; modest edits over layer bands;
recompute suppression space per generated token with a clean shadow forward pass;
estimate concept directions via average future-effect VJPs (J-lens idea) over diverse
contexts; donor coordinate clamping with aligned tokens; template/covariance lens.
We need actual reliable behavior, not a benchmark report of failures. Distinguish a
method misconception from missing controls. Recommend minimal implementations and
tests. Consider whether expected factual consistency should be defined conditional
on changed animal identity despite the unchanged web clue. Don't conflate correcting
the original prompt with intervention incoherence. Avoid just telling us to sweep.
