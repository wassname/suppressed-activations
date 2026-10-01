---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
block_index: 15
n_prompts: 8
---
# Offline donor calibration

Written by PI/OpenAI.

Four fixed generic templates per animal, no leg-count question or answer labels. Raw last-position residual means; no normalisation or fitted strength. No experimental input was run.

SHOULD: means differ. Observed difference norm=1.957303. This does not establish useful steering.

| concept   | input repr                                                                             |   residual norm |
|:----------|:---------------------------------------------------------------------------------------|----------------:|
| spider    | 'A field note describes an animal that suspends sticky silk threads to trap flies. It' |         9.96437 |
| spider    | 'A field note describes an animal that wraps captured insects in silk. It'             |        10.1554  |
| spider    | 'A story mentions an animal that suspends sticky silk threads to trap flies. It'       |         9.20807 |
| spider    | 'A story mentions an animal that wraps captured insects in silk. It'                   |         9.31343 |
| dog       | 'A field note describes an animal that retrieves thrown sticks for its owner. It'      |        10.0639  |
| dog       | 'A field note describes an animal that is trained to sniff luggage at customs. It'     |         9.80029 |
| dog       | 'A story mentions an animal that retrieves thrown sticks for its owner. It'            |         9.283   |
| dog       | 'A story mentions an animal that is trained to sniff luggage at customs. It'           |         9.18747 |

Checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/donors.pt
run.md: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/run.md
