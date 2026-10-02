---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v2_continent/spain_mexico_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text      | Expected properties   |   Tokens |   First-token 'Europe'→'North' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:-------------------|:----------------------|---------:|----------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Spain_to_Mexico: Base                             | Europe; EUR        | Europe; EUR           |        4 |                                        0.0000 |                  0.9536 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224345_chat-causal-0/run.md |
| Spain_to_Mexico: raw J-coordinate exchange        | North America; MXN | North America; MXN    |        6 |                                       18.6250 |                  0.8352 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224345_chat-causal-0/run.md |
| Spain_to_Mexico: raw plain-coordinate exchange    | Europe; EUR        | North America; MXN    |        4 |                                        0.1875 |                  0.9433 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224345_chat-causal-0/run.md |
| Spain_to_Mexico: matched-random delta             | Europe; EUR        | Europe; EUR           |        4 |                                       -0.1875 |                  0.9304 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224345_chat-causal-0/run.md |
| Mexico_to_Spain: Base                             | North America; MXN | North America; MXN    |        6 |                                        0.0000 |                  0.7907 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224351_chat-causal-1/run.md |
| Mexico_to_Spain: raw J-coordinate exchange        | North America; MXN | Europe; EUR           |        6 |                                       -4.3125 |                  0.7372 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224351_chat-causal-1/run.md |
| Mexico_to_Spain: raw plain-coordinate exchange    | North America; MXN | Europe; EUR           |        6 |                                        0.3125 |                  0.7943 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224351_chat-causal-1/run.md |
| Mexico_to_Spain: matched-random delta             | North America; MXN | North America; MXN    |        6 |                                        0.0625 |                  0.8246 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224351_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even            | 4; even               |        4 |                                        0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224357_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even            | 4; even               |        4 |                                        0.6250 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224357_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even            | 4; even               |        4 |                                        0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224357_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even            | 4; even               |        4 |                                        0.0938 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224357_chat-causal-2/run.md |
