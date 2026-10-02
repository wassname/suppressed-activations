---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v1/china_egypt_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text   | Expected properties   |   Tokens |   First-token 'Be'→'C' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:----------------|:----------------------|---------:|--------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| China_to_Egypt: Base                              | Beijing; CNY    | Beijing; CNY          |        6 |                               -0.0000 |                  0.8393 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165122_chat-causal-0/run.md |
| China_to_Egypt: raw J-coordinate exchange         | Israel; ILS     | Cairo; EGP            |        5 |                               11.1250 |                  0.0360 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165122_chat-causal-0/run.md |
| China_to_Egypt: raw plain-coordinate exchange     | Beijing; CNY    | Cairo; EGP            |        6 |                                0.3750 |                  0.8307 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165122_chat-causal-0/run.md |
| China_to_Egypt: matched-random delta              | Beijing; CNY    | Beijing; CNY          |        6 |                                0.3125 |                  0.7807 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165122_chat-causal-0/run.md |
| Egypt_to_China: Base                              | Cairo; EGP      | Cairo; EGP            |        6 |                                0.0000 |                  0.5287 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165131_chat-causal-1/run.md |
| Egypt_to_China: raw J-coordinate exchange         | Beijing; CNY    | Beijing; CNY          |        6 |                              -15.0000 |                  0.7009 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165131_chat-causal-1/run.md |
| Egypt_to_China: raw plain-coordinate exchange     | Cairo; EGP      | Beijing; CNY          |        6 |                               -0.1875 |                  0.5563 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165131_chat-causal-1/run.md |
| Egypt_to_China: matched-random delta              | Cairo; EGP      | Cairo; EGP            |        6 |                               -0.1250 |                  0.3984 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165131_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even         | 4; even               |        4 |                                0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165137_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even         | 4; even               |        4 |                                0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165137_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even         | 4; even               |        4 |                               -0.0625 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165137_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even         | 4; even               |        4 |                               -0.2812 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165137_chat-causal-2/run.md |
