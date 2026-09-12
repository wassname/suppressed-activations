# Late-selector location OAT results (task 1132, criterion 29/30/32, 108 cells)

2026-09-12, PI[claude]. Run: pueue 1132, `slop/common_basis_location_late_batch.json` (each
spec carried `expected_detector_layers=[29,30,32]`; the runtime assertion verified the
resolved config — mechanism smoke-tested pass+fail on the tiny model). Identical site design
to 1130 (L3/L25/L30/L32 = blocks 2/24/29/31; top8_union + random_shared8 + C0; C=1.5;
positions 3 + continuous decode; donor residual at the actual intervention layer). Raw:
`out/2026-09-12_cb-loc-late/{cond}-{cell}/result.json`.

## Site table (late-selected bases; swap means over 12; splits 4 cells)

| site | swap ↑ | legs | naming | property | ρ | ρ_P | capped |
|---|---:|---:|---:|---:|---:|---:|---:|
| L3 | −0.06 | +0.06 | −0.24 | −0.00 | 0.063 | 0.004 | 0/12 |
| L25 | +1.49 | +1.03 | +3.51 | −0.08 | 0.121 | 0.035 | 0/12 |
| L30 | +1.84 | +3.88 | +3.41 | −1.78 | 0.235 | 0.101 | 2/12 |
| L32 | +2.19 | +7.47 | +3.85 | −4.76 | 0.182 | 0.110 | 5/12 |
| randoms | −0.11..+0.02 | | | | | | |
| C0 | 0.00 exact | | | | | | |

## Semantic adjudication (the discriminator; full continuations read)

The late selector's legs movement is DEGENERATE, not transfer (plan rubric: "a changed digit
followed by spider/eight-leg correction fails semantic transfer"; loops fail coherence):

- L30 legs-ant (both cells, swap +5.5): digit flips to the donor answer `6`, then
  `The six-legged six-six-six-six-…` repetition loop to the 128 cap.
- L32 legs-ant (both cells, swap +10.8/+12.2): `6 six six six …` loop to cap.
- L32 legs-L1-dog (swap +4.8): `4` then `The animal is a spider … having 4 legs instead
  of 6` — incoherent (spider identity, wrong digit asserted as correction).
- L25 legs: clean spider/8 everywhere (no effect).
- Naming: 0/4 persistent donor identity at every site (L25 name-N1-dog transient `狗 (Dog)`
  flip then self-correction; L32 name-N1-dog `狗 dog dog dog …` loop; L30 both pure spider).

**Combined verdict across BOTH selectors and all four sites: the top8-union projector
replacement under this equation never produces persistent coherent identity transfer.**
Observed behavioral ceiling: transient first-token effects (bank selector, L25 naming),
degenerate digit/word loops (late selector, L30/L32 legs), or nothing (L3 everywhere,
L20 everywhere). Randoms ≈ 0 at every site/selector (descriptive controls, norms not
matched). C0 exact identity everywhere; coverage asserted.

## Selector comparison (bank 23/25/32 vs late 29/30/32, same sites)

Aggregate site ordering is similar (both peak by L25–L32 within ±0.7); the late selector
shifts movement toward legs (at L30/L32) and makes property NEGATIVE (−1.78/−4.76), with
more caps (5/12 at L32 vs 4/12). Consistent with the normalization-sensitivity result:
the specific basis is selector-sensitive while the phenomenon (late readout fall) is not.
No selector/site combination passed semantic transfer, so the selector question does not
change the behavioral conclusion.

## Status of the bet table

H1 (late-block removal) rejected; H2 rotation supported (angles); H3 propagation yes /
behavior no; H4 no site achieves persistent identity (both selectors, semantic outcomes);
H5 readout-level only; H6 normalization sensitivity (not replication); H7 (per-decode
donor state), H8 (+10.01 anomaly), H9 (magnitude-matched randoms) remain open. The
equation-level hypotheses that remain untested: interval-wise re-correction and
generation-dependent donor updates (supervisor's candidates, not queued).
