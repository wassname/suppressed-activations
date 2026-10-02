---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v1/spain_mexico_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text    | Expected properties   |   Tokens |   First-token 'Madrid'→'Mexico' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:-----------------|:----------------------|---------:|-----------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Spain_to_Mexico: Base                             | Madrid; EUR      | Madrid; EUR           |        4 |                                        -0.0000 |                  0.7658 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165242_chat-causal-0/run.md |
| Spain_to_Mexico: raw J-coordinate exchange        | Mexico City; MXN | Mexico City; MXN      |        6 |                                        18.4375 |                  0.9695 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165242_chat-causal-0/run.md |
| Spain_to_Mexico: raw plain-coordinate exchange    | Madrid; EUR      | Mexico City; MXN      |        4 |                                         0.2500 |                  0.7457 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165242_chat-causal-0/run.md |
| Spain_to_Mexico: matched-random delta             | Madrid; EUR      | Madrid; EUR           |        4 |                                         0.3125 |                  0.6475 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165242_chat-causal-0/run.md |
| Mexico_to_Spain: Base                             | Mexico City; MXN | Mexico City; MXN      |        6 |                                         0.0000 |                  0.8942 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165249_chat-causal-1/run.md |
| Mexico_to_Spain: raw J-coordinate exchange        | Mexico City; MXN | Madrid; EUR           |        6 |                                        -5.1875 |                  0.9020 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165249_chat-causal-1/run.md |
| Mexico_to_Spain: raw plain-coordinate exchange    | Mexico City; MXN | Madrid; EUR           |        6 |                                         0.1875 |                  0.9128 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165249_chat-causal-1/run.md |
| Mexico_to_Spain: matched-random delta             | Mexico City; MXN | Mexico City; MXN      |        6 |                                        -0.1250 |                  0.8877 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165249_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even          | 4; even               |        4 |                                         0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165254_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even          | 4; even               |        4 |                                         0.4219 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165254_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even          | 4; even               |        4 |                                         0.0469 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165254_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even          | 4; even               |        4 |                                        -0.1094 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165254_chat-causal-2/run.md |
