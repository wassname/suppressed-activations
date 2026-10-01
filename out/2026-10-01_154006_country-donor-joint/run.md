---
generic_prefills: 8
conditions: 9
config: data/sweden_japan_joint_chat_v1.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Natural donor addition; random matches its norm. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                         | Observed text   | Expected properties   |   Tokens |   First-token 'Stock'→'Tok' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:-----------------------------------------|:----------------|:----------------------|---------:|-------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Sweden_to_Japan: Base                    | Stockholm; SEK  | Stockholm; SEK        |        5 |                                    -0.0000 |                  0.8042 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154019_chat-causal-0/run.md |
| Sweden_to_Japan: role-aligned donor      | Stockholm; SEK  | Tokyo; JPY            |        5 |                                    -0.0000 |                  0.8236 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154019_chat-causal-0/run.md |
| Sweden_to_Japan: matched-random delta    | Stockholm; SEK  | Stockholm; SEK        |        5 |                                    -0.2500 |                  0.8071 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154019_chat-causal-0/run.md |
| Japan_to_Sweden: Base                    | Tokyo; JPY      | Tokyo; JPY            |        6 |                                     0.0000 |                  0.9879 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154025_chat-causal-1/run.md |
| Japan_to_Sweden: role-aligned donor      | Tokyo; JPY      | Stockholm; SEK        |        6 |                                     0.1250 |                  0.9876 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154025_chat-causal-1/run.md |
| Japan_to_Sweden: matched-random delta    | Tokyo; JPY      | Tokyo; JPY            |        6 |                                    -0.1250 |                  0.9872 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154025_chat-causal-1/run.md |
| arithmetic_control: Base                 | 4; even         | 4; even               |        4 |                                     0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154030_chat-causal-2/run.md |
| arithmetic_control: role-aligned donor   | 4; even         | 4; even               |        4 |                                     0.0312 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154030_chat-causal-2/run.md |
| arithmetic_control: matched-random delta | 4; even         | 4; even               |        4 |                                    -0.1250 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_154030_chat-causal-2/run.md |
