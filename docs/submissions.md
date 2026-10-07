# Submit a method

Both leaderboards use the same pinned Qwen model, translation prompts, top-8 word selection and F1 calculation. The distinction is what the method may use, not where its code is hosted.

## Geometry-only

Use the provided input embeddings (before the first transformer layer), residual activations (layers 16–32, all prompt tokens), model weights as matrices, and the supplied unlabelled calibration data: 300 WikiText texts and Russian-to-Korean dev prompts without target answers. Fitting PCA or other geometry on those activations is allowed. The method chooses or combines layers from the activations and returns one residual vector.

Do not use token identities/scores, language filters, external fitting data, pretrained readout models, or additional forward/backward model calls. Fixed settings may be developed on the dev pair; do not choose a fixed layer using labelled per-layer scores. The evaluator alone reads the returned vector through the output head.

Add a file to [methods/](../src/unspoken_concepts/methods/) with a `@geometry` function taking `(hs, embeddings, state, *settings)`, and add its module to `load_methods()` in that directory’s `__init__.py`. `hs` contains layers 16–32; `embeddings` contains layer 0. Both have every prompt position, and neither includes token identities or scores. Related variants can share a file. Shared fits go in [calibration.py](../src/unspoken_concepts/calibration.py); method-specific fitting helpers stay beside their method. Then run `just score`. Submit the resulting `out/*_leaderboard/leaderboard.md`, evidence file and code revision.

## Unrestricted methods

Token scoring, dev-selected layers, gradients, J-lens, contrastive training, additional data and additional model calls are allowed. Each row lists external data, fitting/training and other extras. External data means anything beyond the supplied calibration data and pinned base model, including data used to fit a downloaded lens or checkpoint.

Keep the implementation in a branch or external repository if convenient. Provide a Python adapter:

```python
METADATA = {
    "name": "my method",
    "author": "your name",
    "data": "provided calibration",
    "external_data": "none, or dataset/checkpoint links and versions",
    "training": "none, or objective, supervision and fitting procedure",
    "extras": "e.g. gradients, J-lens, extra model calls, dev-selected layer",
    "output": "vector",  # Or "scores" for one score per vocabulary token. — PI/OpenAI
    "code": "https://github.com/you/repository",
    "revision": "full commit hash",
    "settings": {"rank": 128, "seed": 0},
    "overlap": "known overlap with test prompts/concepts, or unknown",
}

def calibrate(model, tokenizer, texts):
    ...  # Calibration strings; load disclosed external data here. — PI/OpenAI
    return state

def method(model, tokenizer, prompt, state):
    ...  # One prompt, without evaluator labels or target answers. — PI/OpenAI
    return output
```

Run `just score-unrestricted /absolute/path/to/adapter.py`. Autograd is enabled for both calls. Return a finite floating-point tensor: `[d]` in the base model's residual coordinates for `vector`, or `[vocab]` in its tokenizer order for `scores`. The shared evaluator applies the output head to vectors, then uses the same top-8 selection and scoring for either format. `unspoken_concepts.model.forward()` provides the existing residual capture if needed.

The runner writes `out/*_unrestricted/run.md`, per-prompt results, metadata and a copy/hash of the adapter. Submit these with the pinned source and dependency instructions. State external data/checkpoint provenance, contrastive-pair construction, training labels, settings tried and compute requirements. No paired prompt is required for each test question.

## Shared test conditions

Freeze fitting and settings before testing; develop on the Russian-to-Korean dev pair, not test scores. Do not give the method test intermediate labels, target answers or benchmark lookup tables, or select answers using language/script filters. Language markers already in the prompt remain visible. External labelled training data is permitted only in the unrestricted category and its overlap must be disclosed; a public test cannot establish unseen-concept generalisation when those concepts occur in training.

Keep fitted state fixed across test prompts. Keep the supplied model weights, tokenizer and evaluation mode unchanged; use a separate copy for training or interventions. The evaluator uses the original model and output head. Python adapters are not sandboxed: only execute code you trust. Submission review checks these conditions; it is not an extra score or a separate method category.

## Hardware and runtime

The built-in methods ran on one NVIDIA RTX 3090 with 24 GB VRAM. Recorded times with cached model/data downloads:

| command | wall time | includes |
|:--------|----------:|:---------|
| `just score` | 3 min 30 s | model loading, calibration and both method categories |
| `uv run --with matplotlib nbs/layer_readouts.py` | 6 min 30 s | calibration, demo readouts and layer diagnostics |

These timings exclude queue waits and initial downloads. Their start/end records are preserved in the [leaderboard](../results/leaderboard.json.gz) and [layer-plot](../results/layer_plot.json.gz) evidence. The latest leaderboard run peaked at 14.99 GiB of PyTorch-allocated GPU memory; this excludes allocations outside PyTorch. Minimum VRAM and full CPU-inference time were not measured. Use 24 GB as the tested configuration, not a measured minimum; unrestricted training or gradients may need more memory and time.

Tables and figures can be rebuilt from saved evidence on CPU without loading Qwen. One warm run on an AMD Ryzen 9 5900X took 5.41 s for `just results` and 6.57 s for `just plot-layers`. The earlier Matplotlib schematic took 0.70 s; the current schematic uses SVG rendering. The code also has a CPU inference fallback, but no full-evaluation CPU timing is available. Explore [the notebook](../nbs/layer_readouts.py) in a Python notebook editor or run the command above.

## Published files

[Leaderboards](leaderboard/README.md) are rebuilt by `just results` from [leaderboard evidence](../results/leaderboard.json.gz). `just plot-layers` redraws the figure from [layer-plot evidence](../results/layer_plot.json.gz). Each compressed JSON records its source run and contains the data needed for that output. These are the selected published results; `out/` remains ignored local experiment history.

The schematic's editable source is [`figs/cartoon.svg`](../figs/cartoon.svg). `just plot-cartoon` uses Chromium and the installed DejaVu Sans, Noto Sans Arabic and Noto Sans CJK SC fonts to render the PNG shown in the README.

To publish a new run, replace the corresponding named evidence file with the run's `leaderboard.json.gz` or `layer_plot.json.gz`, then run `just results`, `just plot-layers`, `just plot-cartoon` and `just docs`. README rendering files and Markdown includes are under `docs/readme/`; edit `README.qmd`, not the generated `README.md`. The measured demo and its 14 trial prompts are in [spider-demo evidence](../results/spider_demo.json).

<!-- PI/OpenAI: submission instructions and publication paths, from wassname's requested distinction. -->
