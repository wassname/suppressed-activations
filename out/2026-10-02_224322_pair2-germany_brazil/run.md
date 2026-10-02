---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v2_continent/germany_brazil_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text      | Expected properties   |   Tokens |   First-token 'Europe'→'South' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:-------------------|:----------------------|---------:|----------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Germany_to_Brazil: Base                           | Europe; EUR        | Europe; EUR           |        4 |                                       -0.0000 |                  0.9216 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224324_chat-causal-0/run.md |
| Germany_to_Brazil: raw J-coordinate exchange      | Europe; EUR        | South America; BRL    |        4 |                                        9.8125 |                  0.7611 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224324_chat-causal-0/run.md |
| Germany_to_Brazil: raw plain-coordinate exchange  | Europe; EUR        | South America; BRL    |        4 |                                       -0.0625 |                  0.9349 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224324_chat-causal-0/run.md |
| Germany_to_Brazil: matched-random delta           | Europe; EUR        | Europe; EUR           |        4 |                                        0.0625 |                  0.8977 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224324_chat-causal-0/run.md |
| Brazil_to_Germany: Base                           | South America; BRL | South America; BRL    |        6 |                                        0.0000 |                  0.9525 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224330_chat-causal-1/run.md |
| Brazil_to_Germany: raw J-coordinate exchange      | Europe; EUR        | Europe; EUR           |        4 |                                      -16.2500 |                  0.9604 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224330_chat-causal-1/run.md |
| Brazil_to_Germany: raw plain-coordinate exchange  | South America; BRL | Europe; EUR           |        6 |                                       -0.2500 |                  0.9594 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224330_chat-causal-1/run.md |
| Brazil_to_Germany: matched-random delta           | South America; BRL | South America; BRL    |        6 |                                       -0.0625 |                  0.9365 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224330_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even            | 4; even               |        4 |                                        0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224336_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even            | 4; even               |        4 |                                        0.4375 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224336_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even            | 4; even               |        4 |                                       -0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224336_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even            | 4; even               |        4 |                                       -0.0625 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224336_chat-causal-2/run.md |
