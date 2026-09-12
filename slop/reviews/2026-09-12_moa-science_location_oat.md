# MoA-science memo: intervention-site question for the common per-token subspace replacement

2026-09-12, written by PI[claude] (worker). Question, scope, roster, process:

- **Question (user's)**: identify what the last three blocks (29/30/31) suppress; should the
  intervention act early (their suggestion: L3), where components are built, after
  built/before suppressed, or at multiple layers? Raw norms across layers are not comparable
  semantic strengths.
- **Scope**: one method (common_replace h' = h + 1.5(P_d d − P_s h), fixed top8-union
  readout-selected projector, 12 dev questions), the intervention site as the varied axis.
- **Roster**: pilot GLM 5.3 Flash; pass-1 independent GLM 5.3 Flash + DeepSeek V4 Pro +
  Kimi K3 (3 families; supervisor capped at 3); seminar pass all three. One pass each; no
  fallbacks needed. Briefs carried pseudocode + verbatim code + measured numbers + the
  user's question; NO hypothesis list, NO candidate list from us.
- **Artifacts**: pseudocode `slop/pseudocode/2026-09-12_location-oat.py` (pasted to the
  supervisor before any call); exact briefs preserved in-repo:
  `slop/reviews/briefs/{brief_full,science_brief,seminar_glm,seminar_deepseek,seminar_kimi}.txt`;
  raw reports + traces `slop/reviews/2026-09-12_*science_{pass1,seminar}_*.md/.trace.jsonl`;
  measured sources `out/2026-09-11_cb-batch/`, `out/2026-09-11_cb-l25-batch/`,
  `out/2026-09-12_late-blocks-dev/`, `out/2026-09-12_cb-loc/`.
- **Partial-exposure disclosure**: pirev's 20KB input cap forced truncation of DeepSeek's
  section in the GLM and Kimi SEMINAR briefs (marked in-file; full pass-1 report linked).
  The DeepSeek seminar saw untruncated GLM+Kimi finals. Pass-1 briefs were complete for all
  three; the seminar evidence recap was compressed for all three.

## Observations (supplied material; model-independent)

- Site OAT (1130, now complete): L3 −0.02, L25 +2.22, L30 +1.63, L32 +1.95 (swap means);
  randoms ≈ 0 at every site; C0 exact. L3 has the smallest final-state change (ρ 0.047,
  ρ_P 0.003); L32 adds a 狗-repetition mode (4/12 capped).
- Late-block table: numerator ⟨h_l, u_i·g⟩ of selected pairs peaks at h_30 (+5.45) and
  collapses only across block 31 (−84% h30→h32, 753/768 pairs); RMS denominator +57%;
  total span energy rises (86.9→129.7; 23/24 prompts); signed decomposition: blocks 27–29
  amplify (positive cross-terms, block 29 +66.9), blocks 30–31 write against the component
  (−5.4/−80.6 with +10.6/+104.5 norm terms); the h30→h32 energy rise lives in the discarded
  top8-complement (+142.3 vs +29.0).

## Independent claims (pass 1 + seminar), attributed

- **GLM 5.3 Flash (pass 1 + seminar)**: the site inference "L25 is overwritten" rests on one
  flip-then-correct cell (n=1) — "the L25→L30 site inference is currently carrying more
  weight than its evidence supports". The denominator confound "cuts both ways": the +45/+36
  block writes may be unrelated norm drift, not remodeling. Proposed the complement
  projection as the single cheapest separator and the joint edit+trace dose-response framing
  ("where the model becomes committed").
- **DeepSeek V4 Pro (pass 1 + seminar)**: "do not commit to a site or to the suppression
  causal story"; leverage increases through at least L25; L3 unsupported. Donor-state
  quality is CONFOUNDED with site (an h3 donor residual carries less answer content) —
  "later site wins" ≠ "component built later". Requested the per-block numerator trace
  (ran, above) and block-31 ablation as the causal test.
- **Kimi K3 (pass 1 + seminar)**: the numerator collapse "is circular for the numerator" —
  it is the selection criterion restated; the load-bearing experiment is cross-layer
  subspace alignment. Framings added: this is the logit-lens vs tuned-lens problem (a fixed
  unembedding probe misreads mid-network); treat persistence ρ_P as the primary outcome
  ("half-life of an injected direction"), swap as a confounded proxy; the frozen-prefill
  donor state at decode makes self-correction expected MECHANICALLY ("repeatedly inject a
  stale state"), so per-decode donor updates are a distinct candidate; the +10.01 historical
  anomaly may mean the OLD measurement was less specific (inflated), not that the old
  equation was better. Proposed the signed write decomposition (ran, above: rotation
  signature at blocks 30–31).
- **Seminar convergence**: all three independently: (a) do not call blocks 29–31
  "suppressors" of a semantic component — the supported statement is readout-numerator
  loss + span-energy redistribution; (b) selection circularity must be broken with an
  independent criterion or held-out selection before believing late-selector comparisons;
  (c) norm-matched randoms are prerequisite to specificity claims; (d) no one endorses L3.

## Merged hypothesis / bet table

| # | hypothesis | bet (what it predicts) | status after 1130 + CPU checks |
|---|---|---|---|
| H1 | Late blocks REMOVE the component | fixed-basis numerator falls, span E falls | REJECTED in this form: E rises; numerator falls only at block 31; complement absorbs the rise (rotation signature measured) |
| H2 | Span content ROTATES within the union (blocks 30–31 counter-write) | negative cross-terms with positive norm terms; rise concentrated in top8-complement | SUPPORTED (measured signature); direction-level tracking still missing |
| H3 | Early edits (L3) propagate downstream | behavioral change at L3; nonzero downstream state change | PROPAGATION YES, BEHAVIOR NO (supervisor correction): ρ=0.047 is nonzero h32 state change from an L3 edit, but no behavioral transfer — the two are separated; do not call H3 rejected on behavior alone |
| H4 | Post-build site (L30) beats mid-rise (L25) | larger PERSISTENT-IDENTITY naming transfer at L30 | NOT JUDGED BY AGGREGATE SWAP (supervisor correction): adjudicated semantic outcomes — L25-top8 naming: 0/4 persistent donor identity (1 transient flip + 1 pure spider); L30-top8: 0/4 (1 mid-generation "These dogs" leak inside a spider description); L32-top8: 0/4 (2 degenerate loops). NO site achieves persistent transfer; 1.63<2.22 is not the discriminator |
| H5 | L32 readout edit can bypass suppression | stable donor answers at L32 | REJECTED: flips + repetition loops, no persistence; readout-level effect only |
| H6 | Selector circularity inflates "suppression" | independent-selection or unnormalized-logit selection changes the top8 / removes the fall | RAN (CPU): an unnormalized-numerator selector picks a largely DIFFERENT set (Jaccard 16%) with the SAME-magnitude late fall (≈8.7). WORDING (supervisor): BOTH selectors are fall-conditioned, so this is a sensitivity-to-normalization check, NOT independent replication of a selection-independent phenomenon; no further H6 runs |
| H7 | Frozen-prefill donor state at decode causes self-correction mechanically | per-decode donor-state variant reduces self-correction | OPEN — distinct candidate (supervisor: not bundled, not queued) |
| H8 | Historical +10.01 reference is inflated/less specific rather than better | matched measurement shows its effect is non-subspace | OPEN as a mechanism question but NOT an evidence gap: audited 6/12 semantic outcomes + raw generations already exist (fresh set, random control 1/12); reviewer "missing evidence" reflects the brief, not the record; do not reopen an inflation hunt |
| H9 | Specificity of the L25 effect is real | magnitude-matched random still ≈ 0 | OPEN — randoms currently norm-mismatched (descriptive only) |

## Parent decisions (separate from reviewer claims)

- 1130 kept as bank-selector OAT; the late-selector variant (1132) queued under the new
  selector assertion. Approved before the science pass; the seminar's selector-circularity
  objection now applies to ITS interpretation (H6).
- Per the supervisor: interval-wise correction and generation-dependent donor updates are
  untested candidates, not instructed experiments (H7 and the plan's interval candidate).

## Proposed next measurement (only because the independent evidence makes it useful)

All three scientists' cheapest checks ran (numerator trace, signed decomposition,
complement projection) and are reported above. The remaining cheap CPU item is H6
(independent/unnormalized selection + cross-layer subspace alignment from existing
residuals). Behavioral next steps (magnitude-matched randoms, per-decode donor state,
multi-site) are GPU and await the supervisor's choice after 1132.
