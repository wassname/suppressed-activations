---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/sweden_japan_joint_chat_v2_allpos.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. Base tokens, top10 and prefill readout reproduce the pinned reference. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text   | Expected properties   |   Tokens |   First-token 'Stock'→'Tok' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:----------------|:----------------------|---------:|-------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Sweden_to_Japan: Base                             | Stockholm; SEK  | Stockholm; SEK        |        5 |                                    -0.0000 |                  0.8042 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154604_chat-causal-0/run.md |
| Sweden_to_Japan: raw J-coordinate exchange        | Tokyo; JPY      | Tokyo; JPY            |        6 |                                    27.2500 |                  0.9913 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154604_chat-causal-0/run.md |
| Sweden_to_Japan: raw plain-coordinate exchange    | Stockholm; SEK  | Tokyo; JPY            |        5 |                                     0.0625 |                  0.8036 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154604_chat-causal-0/run.md |
| Sweden_to_Japan: matched-random delta             | Stockholm; SEK  | Stockholm; SEK        |        5 |                                     0.2500 |                  0.8169 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154604_chat-causal-0/run.md |
| Japan_to_Sweden: Base                             | Tokyo; JPY      | Tokyo; JPY            |        6 |                                     0.0000 |                  0.9879 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154615_chat-causal-1/run.md |
| Japan_to_Sweden: raw J-coordinate exchange        | Tokyo; JPY      | Stockholm; SEK        |        6 |                                    -3.0000 |                  0.9529 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154615_chat-causal-1/run.md |
| Japan_to_Sweden: raw plain-coordinate exchange    | Tokyo; JPY      | Stockholm; SEK        |        6 |                                     0.0000 |                  0.9878 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154615_chat-causal-1/run.md |
| Japan_to_Sweden: matched-random delta             | Tokyo; JPY      | Tokyo; JPY            |        6 |                                    -0.1250 |                  0.9870 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154615_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even         | 4; even               |        4 |                                     0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154624_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even         | 4; even               |        4 |                                     1.0938 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154624_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even         | 4; even               |        4 |                                     0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154624_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even         | 4; even               |        4 |                                     0.1719 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_154624_chat-causal-2/run.md |
