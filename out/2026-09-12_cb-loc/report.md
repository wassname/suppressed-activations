# Location OAT results (task 1130, bank-selector bases, 108 cells)

Written 2026-09-12 by PI[claude]. Run: pueue 1130, `slop/common_basis_location_batch.json`,
one model load, ~18 min, Qwen3.5-4B rev 851bf6e8. Design: ONE construction (top8_union from
bank-criterion (23,25,32) per-token bases, window last-4, support-corrected; see pseudocode
`slop/pseudocode/2026-09-12_location-oat.py`), the SITE as the only varied axis:
L3/L25/L30/L32 = blocks 2/24/29/31. C=1.5, positions 3 + continuous decode, donor residual
at the actual intervention layer. 12 dev questions × {top8, random_shared8} per site + C0.
Randoms are descriptive (rank-matched, NOT magnitude-matched).

## Site comparison (swap log-odds means over 12 cells; splits are 4 cells)

| site (block) | swap ↑ | legs | naming | property | ρ (full) | ρ_P (in P) | capped |
|---|---:|---:|---:|---:|---:|---:|---:|
| L3 (block 2) | −0.02 | +0.03 | −0.12 | +0.04 | 0.047 | 0.003 | 1/12 |
| L25 (block 24) | +2.22 | +0.25 | +6.23 | +0.18 | 0.249 | 0.072 | 2/12 |
| L30 (block 29) | +1.63 | +0.06 | +4.67 | +0.16 | 0.189 | 0.094 | 0/12 |
| L32 (block 31) | +1.95 | +0.12 | +6.05 | −0.33 | 0.155 | 0.081 | 4/12 |
| randoms (all sites) | −0.11..+0.02 | | | | | | |
| C0 | 0.00 exact | | | | | | |

naming-dog cells (swap, first generation chars): L25-top8 `+11.4 '蜘蛛 (Spider)'`,
`+12.9 '狗 (Dog)

Wai'`; L30-top8 `+8.7/+10.0 '蜘蛛'`; L32-top8 `+9.2 '蜘蛛'`,
`+12.8 '狗狗狗狗狗狗狗狗狗狗狗狗'` (repetition loop to cap).

## Readings (observations first)

1. **L3 does nothing** at this C and construction: no behavioral movement and the smallest
   final-state change (ρ 0.047 vs 0.25 at L25; ρ_P 0.003). The user's early-site framing is
   weakened FOR THIS CONSTRUCTION — with the caveat that site and donor-state content
   co-vary (an h3 donor residual carries different content than an h25 one).
2. **The leverage gradient is step-shaped, not monotonic**: the jump is L20→L25 (prior
   batches: +0.2 → +2.2); L25/L30/L32 are within ±0.6 of each other. Reaching the
   build region (blocks 24–29) is what matters; going later does not add.
3. **L30 does not beat L25** despite block 31 being the suppressor (CPU checks below):
   "post-build placement alone is insufficient" — matching the plan's stated prediction for
   the post-build framing.
4. **L32 = immediate final-readout edit** (no downstream blocks): produces answer-token
   flips AND a new degenerate mode (狗-dog repetition loops, 4/12 capped). Readout-level
   effect without persistent identity, as the plan's output-readout framing predicted.
5. **Direction-specific at every site**: randoms ≈ 0 everywhere (norms not matched —
   descriptive caveat stands).

## CPU checks the seminar requested (from existing dev-bank residuals)

- **Per-block fixed-basis numerator trace** ⟨h_l, u_i·g⟩ for selected (position, token)
  pairs: rises to +5.45 at h_30, collapses ONLY across block 31 (h31→h32 −3.6; no other
  block drops >1.0). The suppressor block, when "suppression" means readout-numerator loss,
  is block 31 — the FINAL block.
- **Signed block decomposition** (2⟨Ph_l, PΔ_l⟩ vs ‖PΔ_l‖²; means over 24 prompts):
  blocks 27/28/29 AMPLIFY (+13.9/+10.8/+66.9 cross-term, positive = write along the
  existing component); blocks 30/31 write AGAINST it (−5.4/−80.6 cross-term with +10.6/+104.5
  norm terms) — the rotation signature. "Suppression" at the end is a counter-write that
  rotates span content, not an emptying.
- **Top8-complement projection**: the h30→h32 energy rise lives in the DISCARDED union
  directions: complement +142.3 vs top8 +29.0 (complement share 0.49 → 0.60). The top8
  edit targets directions that are mildly amplified while the new energy goes elsewhere in
  the union — a rank/rank-coverage problem for late sites, not a site problem.

## Bottom line

The site axis is settled for this construction: L3 is inert; L25 is the measured best
(and cheapest in failures); L30/L32 add nothing and L32 adds a repetition mode. The
mechanism picture changed: block 31 actively counter-writes (rotates) the span; the
component set the top8 projector edits is not where late-block energy goes. The
late-selector (29/30/32) variant (task 1132, queued) tests whether selector-site matching
changes this; magnitude normalization and multi-site/interval edits remain untested
candidates pending that result.

Raw: `out/2026-09-12_cb-loc/{condition}-{cell}/result.json` (+ run.md); this report's
numbers recompute from those files. MoA-science memo: `slop/reviews/2026-09-12_moa-science_location_oat.md`.
