# Bounded cross-depth donor spec (for review — NOT queued)

2026-09-12, PI[glm-5p3-flash]. Authorized scope (supervisor seq 2026-09-12): donor-state
EXTRACTION DEPTH as the missing axis, with the trajectory-selected (INCREMENT) basis.

- Frozen: INCREMENT selector (1182's), temporal top8 per prompt, JOINT removal (v
  contained asserted), site h8 ONLY, C=1.5, last-3 + all-decode, source/joint projectors
  IDENTICAL across all conditions — ONLY the donor vector construction changes.
- Donor anchor: **h25, PREDECLARED as the later-build reference** (not a proven peak:
  h30's projection is larger and unsampled depths exist — h25 is a declared anchor).
- Conditions (48 cells = 12 × 4):
  1. v8 replay: injection = Pd d8 (same-depth; the 1182 h8 null replay).
  2. imported v25: injection = Pd d25 (the donor's LATE-BUILT component projected on the
     same span, imported to h8).
  3. v8 rescaled: SAME v8 direction, rescaled per-offset to ‖v25_o‖ — the direction/size
     discriminator (same direction as #1, same size as #2).
  4. C0: identity.
- Decode: donor anchor frozen at offset-1 (v25_1/v8_1 for all decode steps).
- CAVEATS (explicit): cross-depth import changes the injected NORM (~14×: 0.26 → 3.74) —
  condition 3 is the size control; the h25 vector's coordinates are defined in the same
  span but its scale/meaning at h8 is not validated (cross-depth caveat); descriptive norm
  matching is INJECTION only, not total edit.
- Registered outcome branches: (i) v25 > equal-norm v8 on correct facts + persistent
  identity → supports a depth-direction benefit (the late-built component carries what the
  early projection lacks); (ii) both improve similarly → size contribution; (iii) both
  degrade → these levels/constructions insufficient (NOT the early idea impossible).
- Prior-art caution: search found no prior cross-depth donor injection — absence of
  evidence is not proof of novelty.
