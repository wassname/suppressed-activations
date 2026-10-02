---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v2_continent/france_india_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text   | Expected properties   |   Tokens |   First-token 'Europe'→'Asia' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:----------------|:----------------------|---------:|---------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| France_to_India: Base                             | Europe; EUR     | Europe; EUR           |        4 |                                       0.0000 |                  0.8981 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224303_chat-causal-0/run.md |
| France_to_India: raw J-coordinate exchange        | Asia; INR       | Asia; INR             |        5 |                                      14.5625 |                  0.4551 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224303_chat-causal-0/run.md |
| France_to_India: raw plain-coordinate exchange    | Europe; EUR     | Asia; INR             |        4 |                                      -0.0625 |                  0.8882 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224303_chat-causal-0/run.md |
| France_to_India: matched-random delta             | Europe; EUR     | Europe; EUR           |        4 |                                       0.0000 |                  0.8471 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224303_chat-causal-0/run.md |
| India_to_France: Base                             | Asia; INR       | Asia; INR             |        5 |                                       0.0000 |                  0.8358 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224310_chat-causal-1/run.md |
| India_to_France: raw J-coordinate exchange        | Europe; EUR     | Europe; EUR           |        4 |                                     -15.3125 |                  0.9723 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224310_chat-causal-1/run.md |
| India_to_France: raw plain-coordinate exchange    | Asia; INR       | Europe; EUR           |        5 |                                      -0.4375 |                  0.8168 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224310_chat-causal-1/run.md |
| India_to_France: matched-random delta             | Asia; INR       | Asia; INR             |        5 |                                       0.3125 |                  0.8056 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224310_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even         | 4; even               |        4 |                                       0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224315_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even         | 4; even               |        4 |                                       0.7500 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224315_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even         | 4; even               |        4 |                                       0.0469 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224315_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even         | 4; even               |        4 |                                      -0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224315_chat-causal-2/run.md |
