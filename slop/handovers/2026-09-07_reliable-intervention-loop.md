# Active intervention research

Written by Codex/GPT-6. Goal remains active: get reliable concept intervention,
with recomputed suppressed readout and coherent target consequences. Do not call
word substitution alone success. Prompt stays implicit spider; ant expects6,
dog expects4. Steering covers last3 prompt tokens and all32 output predictions.

Last completed: jobs512/513, named raw/projected swaps at L24. Ant names ant but
still8; dog sometimes4 but dog/spider mixture. See named-coordinate-swap audit.

Current code: `8b95e55`. User changes README.md/.gitignore are untouched.
Research code in scripts/oat_sweep.py and scripts/demo.py; no public demo promoted.

Queued GPU jobs, all default lane with live pqf followers:

- 516 `coordinate-layer`, ant, out/2026-09-07_coordinate-layer-ant
- 517 `coordinate-layer`, dog, out/2026-09-07_coordinate-layer-dog
- 518 `coordinate-band`, ant, out/2026-09-07_coordinate-band-ant
- 519 `coordinate-band`, dog, out/2026-09-07_coordinate-band-dog
- 520 `template-contrast`, ant, out/2026-09-07_template-contrast-ant
- 521 `template-contrast`, dog, out/2026-09-07_template-contrast-dog

Each command is `uv run scripts/oat_sweep.py --sweep NAME --target ANIMAL
--prompt-mode chat-assistant-prefill --output-dir PATH`. 516/517 each36 conditions:
L4,8,12,16,20,24 x C0,.25,.5,1,2,4, raw named swaps. 518/519 each45:
source-dominant-only swaps at five single layers and four five-layer bands,
C0,.25,.5,1,2. 520/521 each68: eight matched explicit-animal templates without
leg counts, averaged target-source last3 suffix activations; six single layers,
full residual or persistent-space projected, C0,.5,1,2,4, plus8 matched randoms
at L16 C2. C1 in this method is the unnormalized mean matched-template difference.

Tests passed for nonorthogonal swaps, norm preservation, one-sided idempotence,
untouched prefixes, continuous decode; config counts checked. Template extraction
asserts exact same last3 token IDs. GPU execution remains unverified until jobs run.
New coordinate traces include after_model_dtype to audit bf16 realization.

The preceding shared GPU training job was515; do not interrupt other repo jobs.
User explicitly said: don't check every minute, attach followers and wait for end.
Follower exec session IDs:516=58379,517=89924,518=35363,519=92974,
520=90065,521=13699. Revalidate handles on continuation, don't restart jobs on timeout.

Scientist panel completed two rounds: KimiK3, DeepSeekV4Pro, Grok4.5, Inkling.
All artifacts in slop/reviews/intervention_*.md, brief and corrections same folder.
Round1 contained false objections (reflection nonorthogonality, nonorthonormal
projectors, missing C0/stale readouts). Round2 withdrew them. All favored matched
template contrasts before VJPs. Accepted: cross-task/held-out checks and fresh random
controls for selected conditions; static unembedding may not encode causal concept.
Rejected: QR-renaming named coordinates, stopping decode steering, using global
hidden cosine as semantic proof, arbitrary norm thresholds, DeepSeek's example
templates containing leg-count answers, unit-length C without a natural dose scale.

Next after results: inspect every generation and trace, compare actual joint
identity/count consistency. Use good conditions on predeclared held-out phrasings
and other consequences; add matched random controls at the selected layer/dose.
If none, adapt the next method using evidence, not a generic null verdict. Promising
untried mechanisms: dynamic per-generated-token suppression space (shadow forward),
layer-specific future-effect VJPs, matched-template coordinate clamping.

Before GPU execution: fixed normalized detector/basis geometry mismatch. Scored
direction is gain-weighted row normalized BEFORE vocabulary centering; basis now
matches. Tests verify invariance to positive row scaling and a two-dimensional
counterexample. Raw named directions unchanged. Projected queued runs use corrected
bases (`basis_geometry` diagnostic). Journal contains proof and limitations.

Added --source-prompt and --condition-index to rerun a fixed sweep condition on new
phrasing without selecting per-prompt settings. Four held-out prompts predeclared
in slop/research/2026-09-07_heldout-intervention-prompts.json before new outputs seen.
Wait orchestration cell635 follows all six job sessions until completion; it may
remain active across assistant actions. Never restart jobs due to an expired observer.
