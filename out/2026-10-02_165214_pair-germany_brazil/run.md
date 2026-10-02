---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v1/germany_brazil_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                  | Observed text    | Expected properties   |   Tokens |   First-token 'Berlin'→'Br' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:--------------------------------------------------|:-----------------|:----------------------|---------:|-------------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Germany_to_Brazil: Base                           | Berlin; EUR      | Berlin; EUR           |        4 |                                    -0.0000 |                  0.6207 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165218_chat-causal-0/run.md |
| Germany_to_Brazil: raw J-coordinate exchange      | Mexico City; MXN | Brasília; BRL         |        6 |                                     9.8125 |                  0.0003 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165218_chat-causal-0/run.md |
| Germany_to_Brazil: raw plain-coordinate exchange  | Berlin; EUR      | Brasília; BRL         |        4 |                                    -0.1875 |                  0.6210 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165218_chat-causal-0/run.md |
| Germany_to_Brazil: matched-random delta           | Berlin; EUR      | Berlin; EUR           |        4 |                                     0.2500 |                  0.5443 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165218_chat-causal-0/run.md |
| Brazil_to_Germany: Base                           | Brasilia; BRL    | Brasília; BRL         |        7 |                                     0.0000 |                  0.9404 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165226_chat-causal-1/run.md |
| Brazil_to_Germany: raw J-coordinate exchange      | Berlin; EUR      | Berlin; EUR           |        4 |                                   -15.6875 |                  0.9085 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165226_chat-causal-1/run.md |
| Brazil_to_Germany: raw plain-coordinate exchange  | Brasilia; BRL    | Berlin; EUR           |        7 |                                    -0.1875 |                  0.9341 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165226_chat-causal-1/run.md |
| Brazil_to_Germany: matched-random delta           | Brasilia; BRL    | Brasília; BRL         |        7 |                                    -0.0625 |                  0.9426 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165226_chat-causal-1/run.md |
| arithmetic_control: Base                          | 4; even          | 4; even               |        4 |                                     0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165232_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange     | 4; even          | 4; even               |        4 |                                     0.5938 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165232_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange | 4; even          | 4; even               |        4 |                                    -0.0156 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165232_chat-causal-2/run.md |
| arithmetic_control: matched-random delta          | 4; even          | 4; even               |        4 |                                    -0.1250 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165232_chat-causal-2/run.md |
