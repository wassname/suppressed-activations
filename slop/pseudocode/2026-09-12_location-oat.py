# Location OAT for common per-token subspace replacement — Qwen3.5-4B (32 blocks)
# Question (user's): the last three blocks (29,30,31) suppress a readout-selected
# component set. Should the replacement edit happen EARLY (h3), mid-rise (h25),
# post-build (h30), or at the final readout (h32)?  One construction, one varied
# axis: the site.                                            -- PI[claude]

# ── indexing ─────────────────────────────────────────────────────────────────
# h_l := residual entering block l;  h_0 = embeddings;  h_l = output of block l−1
# h_32 = final residual (feeds final-norm + tied head).  block l writes:
Δ_l = h_{l+1} − h_l
# so site L edits h_L via hooking block L−1: L3/L25/L30/L32 → blocks 2/24/29/31.

# ── ACTUAL RUNNING DESIGN (task1130): bank-selector bases ───────────────────
# readout at layer l (RMS + gain, row-normalized unembedding U ∈ R^(V×d)):
ϕ_i(l) = ⟨ĥ_l, u_i⟩ / ‖u_i·g‖          # ĥ = h·g/RMS(h);  g = 1 + final_norm.weight
# suppressed_activation_scores with (early, peak, output) = (23, 25, 32):
rise_i  = ϕ_i(25) − ϕ_i(23)            # written by block 24
fall_i  = ϕ_i(25) − ϕ_i(32)            # readout FALL (not proven removal) over 25..32
score_i = torch.minimum(rise_i.clamp_min(0), fall_i.clamp_min(0))
#                              ↑ actual code; both terms vocab-mean-centered first
# per position t (end-aligned last-4 window):
B_t = QR({u_i·g : i ∈ top8(score_t)})  # (d, 8) orthonormal
# temporal union over window (support-corrected):
M = [B_t1 | … | B_t4]                  # (d, 32)
U_s, σ = SVD(M);  keep columns σ > max(shape)·ε·σ₁     # source projector cols
U_d = same construction on donor prompt window          # donor projector cols
# ACTUAL applied projector for the "top8_union" condition, declared explicitly:
U_s8 = U_s[:, :8];  U_d8 = U_d[:, :8]  # NOT the full union; top8 is the arm
P_s = U_s8 U_s8ᵀ;  P_d = U_d8 U_d8ᵀ    # fixed thereafter, same at every site
# (the full-union projector U_s U_sᵀ was a separate L20-only condition; its
#  unguarded version was invalid and is excluded from conclusions)

# ── replacement at site L (the ONLY varied axis in 1130) ─────────────────────
# source positions: last 3 prompt tokens + every decode call (continuous coverage)
# donor state at the ACTUAL intervention layer, end-aligned offset o:
d_o = h_L^donor[end−o]                 # frozen final-prefill donor state at decode
h' = h + C·(P_d d_o − P_s h)           # C = 1.5;  remove source span, add donor span
# decode projectors, verified in code (scripts/oat_sweep.py construction):
#   top8_union / random_shared: decode_src = U_s8 (SAME common projector as prefill)
#   per_token condition only:   decode_src = B_last (per-token last-position basis)
# controls: C0 (exact identity, asserted); random_shared8 = seeded Haar-random
# rank-8 cols for U_s8/U_d8, REAL donor states — descriptive, not magnitude-matched

# ── PLANNED VARIANT (approved, not yet run): late-selector bases ─────────────
# identical site design; only the selector layers change: (early,peak,output) =
# (29,30,32): rise at block 29, readout fall across blocks 30,31. A runtime
# assertion now ties each saved config's detector_layers to the requested spec.

# ── measured diagnostics (descriptive; no semantic-strength claims from norms) ─
# per call: ‖h'−h‖ / ‖h‖;  totals over trajectories NOT comparable across arms
# prefill persistence at answer position (same token history ONLY there):
ρ      = ‖h32^edit − h32^clean‖ / ‖h32^clean‖           # full-space change
ρ_P    = ‖P(h32^edit − h32^clean)‖ / ‖h32^clean‖        # within-P change
# block energy table (fixed P): E_l = ‖P h_l‖²,  frac_l = E_l/‖h_l‖²,
# E_{l+1} − E_l = 2⟨Ph_l, PΔ_l⟩ + ‖PΔ_l‖²   (exact; verified ≤1.3e-4)
# selected-token readout decomposition, h30→h32 on 12 dev questions (n=768 pairs
# = 24 prompts × 4 positions × 8 tokens; signed numerators, zeros included):
#   numerator n_i(l) = ⟨h_l, u_i·g⟩ (raw): 5.45 → 0.87, −84% = (n32−n30)/n30
#   pairs losing numerator (n32 < n30): 753/768
#   RMS denominator: 0.93 → 1.46, +57%
#   source tables: out/2026-09-12_late-blocks-dev/{report.md,late_blocks_table.json}
#   total E_P RISES 87→130 (23/24 prompts) while selected numerators collapse —
#   consistent with energy growth in OTHER P directions; direction change is a
#   labeled hypothesis, not measured (no cross-layer basis correspondence).

# ── known measured facts (L20/L25 batches, 12 dev questions each) ────────────
# same construction at L20: swap +0.20 / +0.25 (support-corrected full_union
#   replay; the original +0.60 full_union was INVALID — arbitrary null columns —
#   and is excluded) / +0.25; randoms +0.06/−0.03/−0.06; C0 exact identity
# at L25: +1.95 / +2.85 / +2.22; naming-dog split +5.4..+6.3, cells to +13.9
#   behavior: FIRST answer token flips to donor (狗) then self-corrects to spider
#   ant/property cells unmoved; randoms at L25 ≈ 0 (norms 184-417 vs 533-787)
# historical recovered reference (DIFFERENT equation h+C(δ−P_ref h), template
#   delta, L20): swap +10.01, primary 6/12 fresh. Why it differs from the
#   projector-replacement is NOT established.
