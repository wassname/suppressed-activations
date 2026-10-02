---
generic_prefills: 0
raw_coordinate_exchange: true
conditions: 12
config: data/country_pairs_allpos_v2_continent/canada_australia_joint.json
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts; selection/configuration declared in the pinned inputs. Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. No reference run for Base parity. First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                   | Observed text        | Expected properties   |   Tokens |   First-token 'North'→'O' log-odds shift |   First-token pair mass |     r2 | Full log                                                                          |
|:---------------------------------------------------|:---------------------|:----------------------|---------:|-----------------------------------------:|------------------------:|-------:|:----------------------------------------------------------------------------------|
| Canada_to_Australia: Base                          | North America; CAD   | North America; CAD    |        5 |                                  -0.0000 |                  0.9006 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224131_chat-causal-0/run.md |
| Canada_to_Australia: raw J-coordinate exchange     | <North America>; AUD | Oceania; AUD          |        6 |                                  10.5000 |                  0.2310 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224131_chat-causal-0/run.md |
| Canada_to_Australia: raw plain-coordinate exchange | North America; CAD   | Oceania; AUD          |        5 |                                   0.1250 |                  0.9043 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224131_chat-causal-0/run.md |
| Canada_to_Australia: matched-random delta          | North America; CAD   | North America; CAD    |        5 |                                  -0.0625 |                  0.8981 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224131_chat-causal-0/run.md |
| Australia_to_Canada: Base                          | Oceania; AUD         | Oceania; AUD          |        6 |                                   0.0000 |                  0.3978 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224159_chat-causal-1/run.md |
| Australia_to_Canada: raw J-coordinate exchange     | North America; CAD   | North America; CAD    |        5 |                                 -16.8750 |                  0.9403 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224159_chat-causal-1/run.md |
| Australia_to_Canada: raw plain-coordinate exchange | Oceania; AUD         | North America; CAD    |        6 |                                  -0.6250 |                  0.4131 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224159_chat-causal-1/run.md |
| Australia_to_Canada: matched-random delta          | Oceania; AUD         | Oceania; AUD          |        6 |                                   0.1875 |                  0.2895 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224159_chat-causal-1/run.md |
| arithmetic_control: Base                           | 4; even              | 4; even               |        4 |                                   0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224206_chat-causal-2/run.md |
| arithmetic_control: raw J-coordinate exchange      | 4; even              | 4; even               |        4 |                                   0.3125 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224206_chat-causal-2/run.md |
| arithmetic_control: raw plain-coordinate exchange  | 4; even              | 4; even               |        4 |                                   0.0625 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224206_chat-causal-2/run.md |
| arithmetic_control: matched-random delta           | 4; even              | 4; even               |        4 |                                   0.0000 |                  0.0000 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-02_224206_chat-causal-2/run.md |
