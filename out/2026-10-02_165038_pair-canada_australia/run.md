---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v1/canada_australia_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                   | Observed text   | Expected properties   |   Tokens |   First-token 'O'→'Can' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:---------------------------------------------------|:----------------|:----------------------|---------:|---------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Canada_to_Australia: Base                          | Ottawa; CAD     | Ottawa; CAD           |        6 |                                -0.0000 |                  0.9735 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165042_chat-causal-0/run.md |
| Canada_to_Australia: raw J-coordinate exchange     | Canberra; AUD   | Canberra; AUD         |        5 |                                13.5625 |                  0.4575 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165042_chat-causal-0/run.md |
| Canada_to_Australia: raw plain-coordinate exchange | Ottawa; CAD     | Canberra; AUD         |        6 |                                 0.0625 |                  0.9729 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165042_chat-causal-0/run.md |
| Canada_to_Australia: matched-random delta          | Ottawa; CAD     | Ottawa; CAD           |        6 |                                 0.4375 |                  0.9610 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165042_chat-causal-0/run.md |
| Australia_to_Canada: Base                          | Canberra; AUD   | Canberra; AUD         |        5 |                                 0.0000 |                  0.6882 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165055_chat-causal-1/run.md |
| Australia_to_Canada: raw J-coordinate exchange     | Ottawa; CAD     | Ottawa; CAD           |        6 |                               -18.5625 |                  0.9853 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165055_chat-causal-1/run.md |
| Australia_to_Canada: raw plain-coordinate exchange | Canberra; AUD   | Ottawa; CAD           |        5 |                                -0.1875 |                  0.6871 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165055_chat-causal-1/run.md |
| Australia_to_Canada: matched-random delta          | Canberra; AUD   | Canberra; AUD         |        5 |                                -0.6250 |                  0.6313 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165055_chat-causal-1/run.md |
| arithmetic_control: Base                           | 4; even         | 4; even               |        4 |                                 0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165106_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange      | 4; even         | 4; even               |        4 |                                -0.2500 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165106_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange  | 4; even         | 4; even               |        4 |                                -0.2500 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165106_chat-causal-2/run.md |
| arithmetic_control: matched-random delta           | 4; even         | 4; even               |        4 |                                 0.0937 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_165106_chat-causal-2/run.md |
