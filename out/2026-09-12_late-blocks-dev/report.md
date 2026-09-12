# [ALTERNATE-WRAPPER DIAGNOSTIC: captured with the runner-default wrapper, NOT the exact dev-batch instruction — see ../vector-map/wrapper_mismatch_note.json]
# Late-blocks table on the 12 development questions (CPU from extracted residuals)

Written 2026-09-12 by PI[claude]. Residuals: task 1127 (`scripts/dev_residual_bank.py`, 24
no-intervention prefill forwards, no generation), table: `scripts/late_blocks_table.py` →
`late_blocks_table.json` (72 prompt:projector groups = 24 prompts × union/top8/per_token).

## Indexing (exact)

Model Qwen3.5-4B: 32 blocks (0–31), hidden 2560, tied unembedding. Residual index l holds
h_l = residual ENTERING block l: h_0 = embeddings, h_l = output of block l−1 (l ≥ 1), h_32 =
final residual before the final norm/tied head. Block l writes Δh_l = h_{l+1} − h_l.
**Last three blocks = 29, 30, 31 (outputs h_30, h_31, h_32).**

Late selector — actual code (`suppressed_activation_scores` at early=29, peak=30, output=32):
`rise = logit_i(h_30) − logit_i(h_29)`, `fall = logit_i(h_30) − logit_i(h_32)`, both
vocab-mean-centered, then `score_i = torch.minimum(rise.clamp_min(0), fall.clamp_min(0))`,
with RMS+gain readout and row-normalized unembedding. Scope: this selects components that
RISE at block 29 (h_29→h_30) and then fall in readout across blocks 30 and 31 — it is NOT a
detector of all forms of last-three suppression (e.g. components built earlier and only
removed later, or written by block 31 itself, are not selected). Per-token rank-8
bases = QR of centered gain-scaled unembedding rows (top-8 scores per position); window =
end-aligned last-4; combined by support-filtered temporal union (SVD left vectors) and top8.
Union support on dev: 29–32/32 (three prompts at 29–31, rest 32) — all within-support for top8.

## Where the late-suppressed components live (union projector, means over 24 prompts)

| h_l | 0 | 8 | 16 | 20 | 23 | 25 | 27 | 28 | 29 | 30 | 31 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fraction E_l/‖h_l‖² | 0.148* | 0.007 | 0.009 | 0.013 | 0.014 | 0.019 | 0.019 | 0.026 | 0.024 | **0.039** | 0.032 | 0.024 |
| block ΔE (written by block l) | — | | | +0.70 | +3.71 | +2.16 | +11.31 | +9.53 | **+45.0** | +6.39 | **+36.4** | |

*h_0 fraction is a small-denominator artifact (‖h_0‖ ≈ 1), not semantic presence.

- Peak at h_30; the biggest single builder is block 29 (+45.0), i.e. the component that
  h_30 carries is written by block 29 and persists through block 30.
- Selected tokens' readouts (per position, n=768): rise h29→h30 mean **+4.58**, fall
  h30→h32 mean **−8.57** (readout drops for 768/768 positions).

## Numerator loss vs denominator growth vs span energy (the distinctions the user asked for)

Raw gain-weighted numerator n_i(l) = ⟨h_l, u_i·gain⟩ and RMS denominator rms(l) for the
selected (position, token) pairs (n = 768 = 24 prompts × 4 positions × 8 tokens):

| quantity | h29 | h30 | h32 |
|---|---:|---:|---:|
| numerator (mean) | 2.47 | 5.45 | **0.87** |
| RMS denominator (mean) | 0.84 | 0.93 | 1.46 |

The readout fall h30→h32 is dominated by NUMERATOR LOSS (−84%; 753/768 pairs lose), not
denominator growth (+57%). So the earlier "dilution" reading is WITHDRAWN: the selected
coordinates genuinely lose their readout component. At the same time total absolute energy in
the union span RISES (E: 86.9 → 129.7; 23/24 prompts) — i.e. energy in OTHER directions of P
grows while the selected coordinates fall: the span content rotates/rebuilds rather than the
span being diluted or emptied. (Caveat: selection favors readout rise/fall, so the 768/768
fall is not independent validation of the criterion.)

On the canonical bank Fact prompts the regime differs: block 31 removes absolute span energy
(source −20.7, control −3.2; fraction to 24–38% of peak) while dog grows (+11.6).
Prompt-format-dependent regimes; both are the operating regimes of the respective experiments.

Verification: exact decomposition E_{l+1} − E_l = 2⟨Ph_l, PΔh_l⟩ + ‖PΔh_l‖² holds on all
groups (max abs err 1.3e-4 on values ~100, float32 noise).

## Implication for intervention-site choice (inference, labelled)

If the dev-question "suppression" is dilution rather than removal, an early (L3) geometric
edit to these components fights a stream that keeps growing them; the build-peak site
(block 29 / h_30) is where the components are largest and most recently written; L25 is
mid-rise; L32 is post-suppression reference. This motivates the location comparison below —
it does not by itself predict which site transfers (early components could still steer
downstream computation; that is a causal question).

## Proposed small location comparison (NOT queued — awaiting mapping check)

Same procedure, one axis (location), one construction: **top8_union** (valid support, moved
at L25); projector = FIXED late-selected per-token bases (criterion 29/30/32, window last-4,
support-corrected); C = 1.5; positions 3 + continuous decode; donor residual d_p taken at the
ACTUAL intervention layer L (already the runner's behavior: `donor_states = target
residuals[layer]`); C0 once; descriptive random_shared8 per location.

| arm | layer | rationale |
|---|---|---|
| A | L3 | user's explicit early site |
| B | L25 | mid-rise reference (previous batch's layer) |
| C | L30 | post-build / pre-fall (peak h_30, written by block 29) |
| D | L32 | late reference; an edit here is an IMMEDIATE FINAL-READOUT edit (h_32 feeds the final norm/head), NOT evidence of downstream propagation |

Cells: 4 locations × 12 questions (construction) + 4 × 12 (random_shared8) + 12 (C0) =
108 cells, one model load ≈ 17 min. Diagnostics per call: per-call edit/residual norm
fraction (descriptive only — total norms across trajectories do not establish magnitude
matching, and no binding-blocker claim is made from them); downstream persistence at the
answer position reports BOTH ‖edited−clean‖ AND ‖P(edited−clean)‖, each relative to the
clean norm — P-only cannot establish persistence outside P. The diagnostic is PREFILL ONLY:
token histories are identical before the first generated token; decode histories diverge
after sampling and no cached edited-vs-clean state comparison is implied. Both animals;
full 128-token continuations.
