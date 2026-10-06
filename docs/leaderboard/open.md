# Open methods

This table is for methods using additional data, contrastive training, gradients, J-lens, or extra model calls. The model, test prompts, top-8 readout and F1 calculation are the same as in the geometry table. Resources differ, so report them alongside the score.

No open entries have been evaluated yet. Accepted entries will use these columns:

| method | F1↑ (90% CI) | by | data | access | supervision |
|:-------|------------:|:---|:-----|:-------|:------------|

Existing reference results remain on the [full leaderboard](README.md). They have not been audited or rerun as open submissions. In particular, a method returning vocabulary scores must be adapted to return a residual-stream vector before entering this table.

## Submit an adapter

Keep your implementation in a branch or external repository. Install its dependencies in your environment and give the runner a Python file with this interface:

```python
METADATA = {
    "name": "my method",
    "author": "your name",
    "data": "provided calibration + external labelled pairs",
    "access": "activations, weights, gradients, extra forward passes",
    "supervision": "known intermediate concepts in training pairs",
    "code": "https://github.com/you/repository",
    "revision": "full commit hash",
    "settings": {"rank": 128, "seed": 0},
    "overlap": "describe overlap with test prompts and concepts, or say unknown",
}

def calibrate(model, tokenizer, texts):
    # Unlabelled calibration strings; load disclosed external data here. — PI/OpenAI
    ...
    return state

def method(model, tokenizer, prompt, state):
    # One test prompt; return a finite residual-space tensor of shape [d]. — PI/OpenAI
    ...
    return vector
```

Run `just score-open /absolute/path/to/adapter.py` on one GPU. The runner enables autograd for both calls, then uses the shared evaluator to read and score the returned vector. `common.forward()` also works inside these calls if you want the existing residual capture. It writes a unique `out/*_open/run.md`, the adapter, metadata and per-prompt results. Submit the report and pinned code as an issue or PR; accepted rows are added here after review. The runner does not edit this table automatically.

Data should distinguish provided calibration, external unlabelled and external labelled data, with dataset links/versions. Access should list activations, weights, gradients, J-lens and extra forward passes as applicable. Include external checkpoints and their revisions. Describe how contrastive pairs are constructed and what their labels reveal. There is no required contrastive partner for a test prompt.

## Evaluation conditions

- Freeze training, settings and layer selection before testing. Develop on the Russian-to-Korean dev pair; do not choose methods or settings from test scores.
- Do not use test target answers, intermediate labels, benchmark dictionaries or language labels to identify the hidden word. Test language names already present in the prompt remain visible. Token scores and J-lens are permitted computation in this track, not permission to look up the test labels.
- Disclose known overlap between external data and test prompts or concepts. The public test cannot establish unseen-concept generalisation when those concepts occur in training.
- Keep the supplied model weights, tokenizer and evaluation mode unchanged. Use a separate copy for any training or intervention; return a vector in the supplied model's residual coordinates. The evaluator always uses the original output head.
- Keep fitted state fixed during testing; do not learn across test prompts. Report failed runs, selection attempts and computational requirements with the submission.

The adapter receives no evaluator labels. This is an interface convention, not a security sandbox: Python code can read local files, so compliance requires reviewing the submission. Only run code you trust.

<!-- PI/OpenAI: open submission contract and table, authorised by wassname. -->
