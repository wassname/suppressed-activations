# Selector comparison on exact inputs: 3-snapshot vs positive-increment candidate

2026-09-12, PI[claude]. CPU on the exact-input bank (task 1174: pinned revision, exact
wrapper, 24/24 rendered-ID equality vs the actual runs). Script:
`scripts/selector_comparison.py` → `selector_comparison.json`. Windows: build = b13..b23
(the hypothesis window, declared); cut = exactly the last-3 writes b29/b30/b31; both
selectors center over vocab BEFORE rectification; top-k = largest scores; same per-token →
QR → temporal-union downstream.

## Result: the selectors pick essentially DIFFERENT tokens

**Jaccard(selected window sets, 3-snapshot vs increment candidate): mean 0.026, min 0.000,
max 0.158** over 24 prompts.

What each picks (source prompt, last window position, decoded):

- legs question — 3-snapshot: `_disc, هام, cream, laba, Disc, _target, Ủy, 爬到` (debris);
  increment candidate: **`legs, leg, _leg, GOODMAN, 土産, -legged, …`** — the TOPIC
  vocabulary (leg-related tokens).
- naming question — both pick debris, but DIFFERENT debris (snapshot: `reels, Δη, råde…`;
  candidate: `倡廉, HUD, インストール…`).

Score magnitudes (last position, top values): snapshot ~5.4–5.8; increment ~13.3–14.8 —
the increment form finds LARGER, cleaner build+cut structure on the same readouts.

## Interpretation (labeled)

The leg-topic tokens' readouts rise EARLY (inside b13–b23 — consistent with the user's
build-window hypothesis) and are cut in the last-3 writes; the 3-snapshot selector's rise
window (23→25) sees only tokens still rising at L23–25, which on these prompts is debris —
the topic tokens were already built by then. This is SELECTOR SENSITIVITY to the added
trajectory evidence (per the recovery report's scoping: NOT yet evidence that the 3-snapshot
version "lost useful information" — that requires held-out specificity or behavioral
differences, not yet run).

Caveats: build window is the hypothesis's own (edges ±3 sensitivity not yet swept); the
increment form credits oscillation (the sawtooth caveat in the recovery report); the
topic-token reads are TOKEN READOUTS (decode of selected IDs), not established semantics;
single prompt family (12 pairs), alternate-wrapper bank analyses elsewhere remain labeled.

## Next (smallest, still CPU)

Sweep the build-window edges (b10..b26) for the Jaccard/stability curve — if the candidate's
topic-token selection is window-robust, the next step is the bounded specificity battery
(donor-answer-token presence, cross-prompt same-concept overlap distributions, matched-random
controls) before any intervention. No GPU.
