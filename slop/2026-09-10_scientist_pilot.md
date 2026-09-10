Explain this pseudocode in your own words. Name what is missing or underspecified. State
what claims you would refuse to make from it alone. Do not propose a conclusion or try to
guess the parent's question.

```python
Δ = U (Uᵀ (μ_target - μ_spider))       # project template mean difference into U-span
Δ = Δ * ‖μ_target - μ_spider‖ / ‖Δ‖     # norm-match
# generation path, every decode step at the edited position:
    span = U (Uᵀ h)                      # live source component, P h
    patched = h + C (Δ - span)
    # U-span:  P h' = (1-C) P h + C Δ
    #   C=0 -> P h ; C=1 -> Δ ; C=2 -> 2Δ - P h (reflection about Δ)
# random control: random_delta norm-matched; patched = h + C (random_delta - span)
```

h is a live residual vector at an edited layer position; U is an orthonormal projector basis
(rank 4); Δ is a template attenuation delta; C is a scalar strength; span is the live source
component projected into the U-span.
