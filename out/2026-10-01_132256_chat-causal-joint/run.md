---
generic_prefills: 8
conditions: 12
---
# Native-chat joint-property intervention

— PI/OpenAI. Known development concepts. Task frame and donor preparation both changed. Previous literal donor retains its own norm; random matches the new donor. First-token scores do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.

| Case / condition                                | Observed text   | Expected properties   |   Tokens |   8→4 log-odds shift |   Bare-answer mass |     r2 | Full log                                                                          |
|:------------------------------------------------|:----------------|:----------------------|---------:|---------------------:|-------------------:|-------:|:----------------------------------------------------------------------------------|
| dog_to_spider: Base                             | 4; inside       | 4; inside             |        4 |               0.0000 |             0.9808 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132318_chat-causal-0/run.md |
| dog_to_spider: role-aligned donor               | 4; inside       | 8; outside            |        4 |              -0.0625 |             0.9806 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132318_chat-causal-0/run.md |
| dog_to_spider: previous literal-name donor      | 4; inside       | 8; outside            |        4 |              -0.4375 |             0.9786 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132318_chat-causal-0/run.md |
| dog_to_spider: matched-random delta             | 4; inside       | 4; inside             |        4 |              -0.1875 |             0.9799 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132318_chat-causal-0/run.md |
| spider_to_dog: Base                             | 8; outside      | 8; outside            |        4 |               0.0000 |             0.9240 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132326_chat-causal-1/run.md |
| spider_to_dog: role-aligned donor               | 8; outside      | 4; inside             |        4 |               0.1250 |             0.9243 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132326_chat-causal-1/run.md |
| spider_to_dog: previous literal-name donor      | 8; outside      | 4; inside             |        4 |               0.2500 |             0.9355 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132326_chat-causal-1/run.md |
| spider_to_dog: matched-random delta             | 8; outside      | 8; outside            |        4 |              -0.2500 |             0.9313 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132326_chat-causal-1/run.md |
| arithmetic_control: Base                        | 4; even         | 4; even               |        4 |               0.0000 |             0.8249 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132332_chat-causal-2/run.md |
| arithmetic_control: role-aligned donor          | 4; even         | 4; even               |        4 |              -0.3125 |             0.7845 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132332_chat-causal-2/run.md |
| arithmetic_control: previous literal-name donor | 4; even         | 4; even               |        4 |              -0.3750 |             0.7633 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132332_chat-causal-2/run.md |
| arithmetic_control: matched-random delta        | 4; even         | 4; even               |        4 |              -0.2500 |             0.8056 | 0.0000 | /workspace/2026/suppressed-activations/out/2026-10-01_132332_chat-causal-2/run.md |
