<!-- Draft README section for wassname's edit. PI/OpenAI, 2026-10-02. Not inserted into README.md. -->

## Can we change the hidden country?

To give the capital and currency of "the country containing Toronto", the model has to think "Canada" without saying it. We change that hidden "Canada" into "Australia" inside the model and check that both answers move together.

The edit swaps the two countries' coordinates along their Jacobian-lens directions at layer 15, at every prompt position and every generated token (generated tokens at quarter strength). It is one forward pass: the only fixed inputs are the J-lens token directions for " Canada" and " Australia". Editing only the last prompt token changed nothing; the country is read from the city token.

### Base

Input (`repr`):

```text
"<|im_start|>system\nAnswer briefly. Do not explain.<|im_end|>\n<|im_start|>user\nFor the country containing Toronto, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout at layer 24 (“what it is thinking”): `[' Ottawa', 'Canada', ' Montreal', 'London', ' Montréal', ' Canada', ' Winnipeg', ' London']`

Generation:

```text
Ottawa; CAD<|im_end|>
```

| token | log p | p |
|---|---:|---:|
| **O** | −0.027 | **0.973** |
| < | −4.027 | 0.018 |
| Toronto | −6.027 | 0.002 |
| Ont | −6.402 | 0.002 |
| Canada | −6.777 | 0.001 |

### Causal intervention

Same input. Readout after the edit: `['London', ' London', ' Canberra', ' Melbourne', '伦敦', ' Jakarta', ' Londres', ' Sydney']`

Generation:

```text
Canberra; AUD<|im_end|>
```

| token | log p | p | Δ log p |
|---|---:|---:|---:|
| **Can** | −0.812 | **0.444** | +9.28 |
| < | −1.312 | 0.269 | +2.72 |
| Sy | −1.937 | 0.144 | +12.15 |
| Australia | −3.687 | 0.025 | +10.28 |
| *O* | −4.312 | *0.013* | −4.29 |

```python
V = [J15.T @ (g * W[" Canada"]), J15.T @ (g * W[" Australia"])]   # fixed token directions
c = pinv(V) @ h                                                   # at every position
h = h + s * V @ (flip(c) - c)                                     # s = 1 on the prompt, 0.25 per generated token
```

Selection: the method was fixed on Sweden/Japan (1 of 2 directions worked), after the same swap at the last token alone failed. It was then run unchanged on five new pairs fixed in advance. This example is the first pair alphabetically.

| | target capital and currency | another single country | unchanged |
|---|---:|---:|---:|
| J-lens swap, 10 new directions | **7** | 2 (Israel; ILS, Mexico City; MXN) | 1 |
| same swap with plain unembedding directions | 0 | 0 | 10 |
| random edit of equal size | 0 | 0 | 10 |

Limits: one prompt template and well-known countries; the edit is 5–6% of the activation norm at the prompt. Arithmetic (`4; even`) was unchanged in every condition. Logs: `out/2026-10-02_165038_pair-canada_australia/run.md` and the four sibling `pair-*` runs.
