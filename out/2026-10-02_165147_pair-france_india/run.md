---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v1/france_india_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text   | Expected properties   |   Tokens |   First-token 'Paris'→'New' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:----------------|:----------------------|---------:|-------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| France_to_India: Base                             | Paris; EUR      | Paris; EUR            |        4 |                                     0.0000 |                  0.9346 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165152_chat-causal-0/run.md |
| France_to_India: raw J-coordinate exchange        | New Delhi; INR  | New Delhi; INR        |        6 |                                    25.6250 |                  0.8353 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165152_chat-causal-0/run.md |
| France_to_India: raw plain-coordinate exchange    | Paris; EUR      | New Delhi; INR        |        4 |                                     0.3125 |                  0.9173 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165152_chat-causal-0/run.md |
| France_to_India: matched-random delta             | Paris; EUR      | Paris; EUR            |        4 |                                     0.6250 |                  0.8980 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165152_chat-causal-0/run.md |
| India_to_France: Base                             | New Delhi; INR  | New Delhi; INR        |        6 |                                     0.0000 |                  0.8827 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165200_chat-causal-1/run.md |
| India_to_France: raw J-coordinate exchange        | Paris; EUR      | Paris; EUR            |        4 |                                   -26.4375 |                  0.9885 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165200_chat-causal-1/run.md |
| India_to_France: raw plain-coordinate exchange    | New Delhi; INR  | Paris; EUR            |        6 |                                    -0.1250 |                  0.8740 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165200_chat-causal-1/run.md |
| India_to_France: matched-random delta             | New Delhi; INR  | New Delhi; INR        |        6 |                                    -0.1250 |                  0.8624 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165200_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even         | 4; even               |        4 |                                     0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165205_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even         | 4; even               |        4 |                                     0.2812 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165205_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even         | 4; even               |        4 |                                    -0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165205_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even         | 4; even               |        4 |                                    -0.0625 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165205_chat-causal-2/run.md |
