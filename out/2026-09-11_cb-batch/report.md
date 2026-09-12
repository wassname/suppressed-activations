# Common-basis batch report (task 1072, 96 cells) — corrected per supervisor review

Written 2026-09-11 by PI[claude]; claims reworded after supervisor seq-45 review. Run: pueue
task 1072, `slop/common_basis_batch.json`, one model load, 918 s, model Qwen/Qwen3.5-4B rev
851bf6e8. 12 dev questions (the exposed fresh cells) × 8 conditions, 128-token continuations,
continuous last-3-prefill + decode coverage (asserted per cell), C=1.5, L20, window 4,
positions 3. Equation under test: `h' = h + C (P_d d_p − P_s h_p)`; recovered reference keeps
its own equation `h + C(δ − P_ref h)` (template-attenuation common rank-4, L20 historical and
distinct). Randoms are rank-matched seeded Gaussian projectors with real donor states —
DESCRIPTIVE controls, NOT applied-norm matched. Raw rows: `analysis.json`; per-cell
`result.json` (+ `run.md`, condition logs).

## Means split by question type (4 cells each)

| condition | legs swap ↑ | legs p_tgt | legs norm | naming swap ↑ | naming norm | property swap ↑ | property norm |
|---|---:|---:|---:|---:|---:|---:|---:|
| recovered-ref C1.5 | +10.31 | 0.971 | 539.0 | +20.05 | 891.9 | −0.34 | 904.7 |
| per_token C1.5 | +0.22 | 0.023 | 98.9 | +0.20 | 108.8 | +0.19 | 177.4 |
| full_union C1.5 — INVALID as union (null columns), superseded | (+0.22) | (0.026) | (241.9) | (+1.36) | (376.4) | (+0.20) | (711.0) |
| top8_union C1.5 | +0.38 | 0.032 | 108.1 | +0.32 | 123.8 | +0.06 | 224.5 |
| random_shared8 | +0.12 | 0.022 | 94.1 | +0.04 | 124.0 | +0.02 | 96.7 |
| C0 | 0.00 | 0.020 | 0.0 | 0.00 | 0.0 | 0.00 | 0.0 |

Overall means (all 12 cells): recovered-ref +10.01 (p_tgt 0.327, total norm 778.5, prefill
19.8 / decode 758.8); per_token +0.20 (128.4; 2.7/125.6); top8_union +0.25 (152.1; 3.1/149.0);
randoms +0.06/−0.03/−0.06; C0 0.00 exact identity. The full_union overall mean is NOT valid
as a union result (every cell included 1–8 arbitrary null columns); the support-corrected
replay (task 1073, `out/2026-09-11_cb-l25-batch/L20-fullunion-support-*`) gives
**+0.25 mean swap** (legs +0.22, naming +0.26, property +0.28) — use that as the L20
full_union baseline. Per-cell swap, per-call norms (total/prefill/decode/calls),
first_answer: `analysis.json`.

## Observed continuations (complete, verbatim)

recovered-ref C1.5, legs-L1-dog (66 tokens, COMPLETE generation; full text also at
`../2026-09-11_cb-batch/recovered-ref_C1.5-legs-L1-dog/result.json`):

```text
4

The animal is a dog, a popular domesticated breed known for its loyalty and friendly demeanor. Dogs typically have a thick coat of fur that comes in various colors and textures to suit different climates. They are excellent companions for families and often serve as working animals in roles such as hunting, herding, and assistance.<|im_end|>
```

per_token C1.5, legs-L1-dog (63 tokens):

```text
8

The spider is an arachnid that typically has eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing vibrations, and manipulating silk threads to build intricate webs. Despite their small size, spiders are powerful predators capable of injecting venom to subdue their prey.<|im_end|>
```

top8_union C1.5, name-N1-dog (62 tokens):

```text
蜘蛛 (Spider)

The spider is an arachnid that lives in various environments, from forests to urban areas. It spins intricate webs to trap prey, using silk to create a sticky net that catches flying insects. Despite their small size, spiders play a crucial role in ecosystems by controlling insect populations.<|im_end|>
```

C0, legs-L1-dog (63 tokens): byte-identical answer/identity to the per_token cell above
(full text in `C0-legs-L1-dog/result.json`). Across all 36 common-basis + random + C0 cells
the answer and identity stay at clean-source level; no repetition loops (r2 ≤ 0.12), EOS
terminations, coverage asserted (decode_steps = tokens − 1, trace = prefill + decode).
Largest single movement: full_union name-N1-dog +2.41, no answer change.

## Edit scale (norm fractions, NOT energy fractions)

| condition | donor-proj norm mean | donor-state norm mean | proj/state (norm fraction) | prefill edit norm mean |
|---|---:|---:|---:|---:|
| per_token | 0.95 | 15.35 | 0.062 | 2.7 |
| full_union *(invalid)* | 3.18 | 15.35 | 0.207 | 8.8 |
| top8_union | 1.14 | 15.35 | 0.074 | 3.1 |
| random_shared8 | 0.78 | 15.35 | 0.051 | 3.0 |
| recovered-ref (selected component) | 9.39 | — | — | 19.8 |

Observed: the prefill edit norms differ (2.7 / 3.1 / 8.8 vs reference 19.8) and the projected
donor components are small norm fractions of the donor state. This is an observation about
scale, NOT an established cause: magnitude, direction, and injection site can all explain the
behavioral difference, and they are not yet separated. The L25 OAT (task 1073, running) tests
the site axis; the support-corrected replay tests union validity; per-call magnitude
normalization is deferred until after the matched layer comparison.

## Union support audit (by unique cells and sides)

22 (cell, side) flags over 12 unique full_union cells — every full_union cell has at least one
numerical-null column (donor side flagged 12/12, source side 10/12; s_min ~1e-7 vs s1 ~1.4;
support 24–31 of 32; effective rank 18.9–31.3). A full_union projector that includes
arbitrary null columns is INVALID as a union, so **all 12 full_union L20 cells are excluded
from union conclusions**; their artifacts are preserved and a support-corrected replay at L20
is queued in task 1073. top8_union uses only the first 8 columns, within support everywhere
(min support 24 > 8), so top8 rows stand. The earlier "44 flags" counted each (cell, side)
twice (full_union and top8 rows share spectra); the analysis script now flags only full_union
rows. Effective ranks and per-cell support are in `analysis.json` rows.

The runner now support-filters the union basis (tolerance `max(shape)·eps·s1`), records
`union_support` in persistence, and never conceals a changed rank (tiny smoke re-passed).

## What this batch establishes (observations) and what it does not

Established: at L20/C1.5 with this equation, none of the three constructions moves answer or
identity above the descriptive randoms, while the historical L20 reference does on legs and
naming. Not established: WHY — magnitude (per-call norms differ ~2–7×), direction (projected
donor components vs template delta), and site (L20 precedes the detector's measured rise) are
confounded and unseparated. Next authorized comparisons (task 1073, one model load):
per_token/full_union/top8 at L25 with the same construction, C0 and rank-matched randoms,
full outputs, state/projection norms recorded at BOTH L20 and L25; plus the support-corrected
L20 full_union replay (12 cells). After the matched layer comparison, decide whether per-call
magnitude normalization is informative.

## Provenance

- Spec: `slop/common_basis_batch.json` (96 entries, condition indices 0–7).
- Per-cell: `out/2026-09-11_cb-batch/{cond}-{cell}/result.json` (+ `run.md`).
- Analysis: `scripts/analyze_cb_batch.py` → `analysis.json` (flags now full_union-only).
- Guard: support-filtered `union_basis` in `scripts/oat_sweep.py` (post-run commit 2a3724d).
- Follow-up: `slop/common_basis_l25_batch.json` (96 cells: 84 L25 + 12 replay), task 1073.
