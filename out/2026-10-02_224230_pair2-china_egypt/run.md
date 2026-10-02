---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v2_continent/china_egypt_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text   | Expected properties   |   Tokens |   First-token 'Asia'→'Africa' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:----------------|:----------------------|---------:|---------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| China_to_Egypt: Base                              | Asia; CNY       | Asia; CNY             |        5 |                                       0.0000 |                  0.5813 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224242_chat-causal-0/run.md |
| China_to_Egypt: raw J-coordinate exchange         | Africa; ZAR     | Africa; EGP           |        5 |                                       6.0000 |                  0.5992 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224242_chat-causal-0/run.md |
| China_to_Egypt: raw plain-coordinate exchange     | Asia; CNY       | Africa; EGP           |        5 |                                       0.3750 |                  0.5813 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224242_chat-causal-0/run.md |
| China_to_Egypt: matched-random delta              | <Asia>; CNY     | Asia; CNY             |        6 |                                      -0.1250 |                  0.4596 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224242_chat-causal-0/run.md |
| Egypt_to_China: Base                              | Africa; EGP     | Africa; EGP           |        5 |                                       0.0000 |                  0.7628 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224249_chat-causal-1/run.md |
| Egypt_to_China: raw J-coordinate exchange         | Asia; CNY       | Asia; CNY             |        5 |                                      -9.0625 |                  0.7666 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224249_chat-causal-1/run.md |
| Egypt_to_China: raw plain-coordinate exchange     | Africa; EGP     | Asia; CNY             |        5 |                                      -0.1875 |                  0.7432 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224249_chat-causal-1/run.md |
| Egypt_to_China: matched-random delta              | Africa; EGP     | Africa; EGP           |        5 |                                      -0.2500 |                  0.7375 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224249_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even         | 4; even               |        4 |                                       0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224254_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even         | 4; even               |        4 |                                       0.6875 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224254_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even         | 4; even               |        4 |                                      -0.0625 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224254_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even         | 4; even               |        4 |                                      -0.0938 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224254_chat-causal-2/run.md |
