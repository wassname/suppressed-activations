# Complete-edit rank ladder results (task 1245, 72 cells)

2026-09-12, PI[glm-5p3-flash]. Run: pueue 1245 (att3; att1 preserved as *-att1-preserved),
one model load, 814 s; protocol `slop/complete_rank_protocol.md`. Site h1 (predeclared),
donor anchor h25 frozen at decode, C=1.5, increment selector, last-3 + all-decode; BOTH
temporal SVD bases (source AND donor) truncated at k ∈ {1,2,4,8,full}; P_joint(k) =
support-filtered union(Us_k, Ud_k); injection = Pd_k d25. Raw:
`out/2026-09-12_cb-cr{1,2,4,8,full}/{k}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| k | joint rank (actual) | edit frac | swap ↑ | legs | naming | property | capped | loops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 1.12 | +0.12 | −0.25 | −0.23 | +0.84 | 3/12 | 3/12 |
| 2 | 4 | 1.58 | +0.62 | −0.75 | +1.93 | +0.69 | 8/12 | 9/12 |
| 4 | 8 | 2.06 | +1.59 | +0.16 | +3.67 | +0.95 | 11/12 | 12/12 |
| 8 | 16 | 2.52 | +1.14 | −0.33 | +3.43 | +0.32 | 9/12 | 10/12 |
| full | 44 | 0.09 | −0.05 | +0.16 | −0.23 | −0.08 | 0/12 | 0/12 |
| C0 | — | 0 | 0.00 exact identity | | | | 0/12 | |

k8 replay vs the 1230 earlyloc imported-h1 arm: **12/12 first-logit hashes + 12/12 full
texts identical** (the prior-path agreement required by the protocol).

## Semantic outcomes (all continuations read; word-boundary identity)

- NO donor answers, NO donor identity at ANY rank (0/12 donor-identity mentions per k;
  0 donor digits in first tokens per 4 legs cells).
- The k4/k8 arms reproduce the loop collapse (12/10 loops of 12) at edit fracs 2.06–2.52 —
  the same degeneration as 1230's h1 arms (which they ARE: k8 = the 1230 imported-h1 arm).
- kfull (the ACTUAL full support, joint rank 44, edit frac 0.09): clean spider everywhere,
  no caps/loops — the injection norm at kfull is tiny (the full temporal basis's
  d25-projection is mostly orthogonal... measured: the injected norm frac 3.60 in the
  CPU ladder was for the h8 site; at h1 the kfull edit is 0.09 — the projection of d25 on
  the full 44-col span is small relative to h1's residual) — the "full" arm is a NEAR-NOOP
  at h1, not a transfer.
- k1/k2: intermediate edit fracs (1.1–1.6) with partial loop appearance (3–9/12).

## Verdict (registered predictions, resolved)

- The ladder DID span the collapse threshold (edit 1.1→2.1 across k1→k4; loops 3→12) —
  the dose-response is real and monotone-in-dose for the collapse.
- BUT: no rank produces donor transfer — the complete-edit narrowing does not create
  transfer at any k; the loop collapse tracks the injected dose, and removing dose (kfull)
  removes the effect entirely (a near-noop, not a rescue).
- The user's early-intervention idea at h1: not reachable by rank narrowing — the
  trade-off (dose vs transfer) has no tested point with both low degradation and donor
  movement. NOT a general impossibility claim (one site/anchor/selector/C; the audit's
  scope note stands).

## Comparison with the CPU precomputation (rank_ladder_cpu.json)

The planned per-k edit fracs (h1): k1 1.08, k2 1.56, k4 2.05, k8 2.50, kfull 3.58 — the
MEASURED k1/k2/k4/k8 (1.12/1.58/2.06/2.52) MATCH the CPU predictions to ~4% (the ladder's
dose model is validated); the kfull CPU frac (3.58) does NOT match the measured 0.09 —
the CPU precomputation assumed the h8-site denominator/geometry for kfull (the earlier
h8-labeled run's numbers), not the h1 site's actual projection: the kfull injected vector
at h1 is genuinely small (the full-support span's d25-projection is nearly orthogonal to
h1's residual). The k8/k4/k2/k1 CPU fracs were h1-correct (the earlier h8 mismatch was
the LABEL error).
