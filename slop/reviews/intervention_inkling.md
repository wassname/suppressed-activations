**Central assumptions**
- Unembedding-row·RMS-gain directions (`v_sp`, `v_t`) are causal in hidden-state space, not just vocabulary correlates.
- Span `U` from the last 4 prompt tokens captures all geometry needed for 31 decode steps.
- Linear coefficient reversal `reverse(c)−c` achieves coherent substitution; `C>1` is interpretable extrapolation, not noise amplification.
- Leg-token (`6/4/8`) proxies concept identity; coherence means identity–leg alignment *despite* the fixed prompt “spins webs” (don’t treat “corrects to spider/8” as failure).
- Continuous patching (prompt + all cached steps) is necessary and accumulates no semantic/norm drift.
- Projection into `U` is either harmless or sufficient; conditioning of `V` is ignored.

**Confounds and controls missing**
- **No null/random-direction arm**: can’t separate hook artifact from causal effect. Add `u_null` ∈ span(`U`) and identity hook (`C=0`).
- **Suppression vs injection not separated**: source-removal alone outperforms donor addition. Run suppression-only (`v_t=0`) and injection-only (`v_sp=0`) arms at L24.
- **Prompt/decode interaction confounded**: patching both hides whether failure is initial-state shift or autoregressive drift. Dissect coverage: `prompt3` only, `decode1–10` only, full.
- **Static `U/V` assumption**: concept coordinates likely shift after token 1. Measure `c_t` per step via a shadow clean forward; if it drifts >20%, static patch is the misconception.
- **Contradictory prompt fixed**: define success conditionally—(A) model resists → spider/8; (B) adopts ant/dog with correct legs, accepting contradiction. Mixed (`ant` + `8`, `dog` + `spider` wording) is incoherence, not correction. Measure identity mention, leg token, web mention separately.
- **Norm drift unmeasured**: `h += Δ` is applied pre-RMSNorm; effective strength becomes `C/||h+Δ||`. Check `||h||` pre/post; if mean drift >0.05, rescale or apply post-norm correction.
- **Conditioning of `V`**: `pinv(V)` unstable if `v_sp ≈ v_t`. Compute κ(`V`); if >1e3, regularize.
- **Projection loss**: check `||v_proj||/||v_raw||`; if <0.7 for either vector, projection discards signal.

**Annotated pseudocode (minimal L24 arms)**
```python
# V = [v_sp | v_t] centered, unnormalized*gain, unit cols, float32
# U = thin-SVD(B) span, 8-dim; h is pre-RMSNorm hidden state

def c_coords(h, V):
    # Least-squares in span(V); unstable if collinear—check κ(V)
    return np.linalg.pinv(V) @ h   # [c_sp, c_t]

def update(h, mode, C, v_sp, v_t, U, V):
    c = c_coords(h, V)
    if mode == "null":           # control: random direction in U
        u = precomputed_rand_unit(U)
        return h + C * u
    if mode == "identity": return h
    if mode == "supp_only":      # remove spider only
        d = max(c[0], 0)
        return h - C * d * v_sp
    if mode == "inj_only":       # inject target only
        d = max(c[1], 0)
        return h + C * d * v_t
    if mode == "full_swap":      # current linear reversal
        rev = np.array([c[1], c[0]])
        return h + C * (V @ (rev - c))
    if mode == "dom_only":       # source-dominant only
        d = max(c[0] - c[1], 0)  # non-smooth; avoid C>2
        return h + C * d * (v_t - v_sp)

# Hook wrapper: apply at L24 to selected tokens/steps,
# record ||h||_pre/post, apply before bf16 cast.
# Coverage modes: "prompt3", "decode1-10", "full" — do NOT mix.
```
**Shadow readout (optional, 2× cost)**: after generating token `s`, run clean forward from cached state to `L24`, compute `c(s)`. If `c(s)` diverges from `c(0)`, static `V/U` is inadequate.

**Mathematical issues**
- Normalized `v` loses magnitude; if true effect vector is small, normalization amplifies noise.
- `P = mean(BB^T)` is an output-vocabulary covariance, not hidden-state covariance; `U` may miss the intervention tangent space.
- Update is linear in `h` but `h` lives pre-RMSNorm; post-update normalization makes the effective step `Δ / ||h+Δ||`, so scaling is state-dependent and non-linear in `C`.
- Source-dominant `d` introduces a ReLU discontinuity at `c_sp = c_t`; can cause token-level trajectory jumps.
- At `C=1`, `reverse(c)−c` is a reflection through the `c_sp=c_t` line; `C>1` extrapolates past it, explaining projected-ant-C4 yielding digit `2` (overshoot into noise quadrant).

**Prioritized next experiment (do this, not the 6-layer sweep)**
Run **L24 only**, raw `V` (no `U` projection first), with discrete coverage (`prompt3`, `decode1-10`, `full`), conditions: `identity`, `null`, `supp_only`, `inj_only`, `full_swap` (`C=0.5,1`), `dom_only` (`C=0.5,1,2`). Metrics per run: (1) `P(6/4/8)` first token; (2) identity string match (`ant`/`dog`/`spider`) in first 30 tokens; (3) leg–identity consistency (`ant`→6, `dog`→4); (4) `web` mention; (5) mean norm drift `||h||`; (6) κ(`V`) and projection ratio.

**Interpretation rules**: If `dom_only` outperforms `full_swap` on consistency without drift >0.05, the misconception is over-correction by linear reversal. If `null` ≈ `full_swap`, `V/U` lacks causal effect. If `supp_only` ≈ full, donor injection is redundant/harmful. If `c(s)` drifts in shadow, prioritize dynamic `U` recomputation next. Do not run the queued 6-layer grid until this L24 disentanglement establishes which operator actually moves the state coherently.