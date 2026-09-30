---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
k: 32
forward_passes: 0
generations: 0
cache_positions: out/2026-09-30_082225_jlens-one-pass
elapsed_seconds: 7.86
---
# Fixed-layer readout comparison

Written by PI/OpenAI.

One changed axis: maximum log probability across all prompt positions instead of the final position. Reuse the saved midpoint activations; compare raw J-lens and raw plain lens, with the same k and prompt mask. Hypothesis: the bridge is present near its clue even when absent at the final prompt position. The four country cases and the spider case were previously selected; this is development data, not a success rate.

| concept   | readout                 |   hidden rank |   answer rank | joint pass   | top8                                                                                                   |
|:----------|:------------------------|--------------:|--------------:|:-------------|:-------------------------------------------------------------------------------------------------------|
| Bulgaria  | J-lens                  |           879 |          5002 | False        | ['____', '________', ' ______', ' ___', ' ____', '___', '？**', ' __']                                 |
| Bulgaria  | plain lens              |         15450 |        204256 | False        | ['____', ' cherchez', ' Multimedia', 'あた', '琦', '团团', ' squirt', 'bourg']                         |
| Bulgaria  | J-lens max position     |           942 |          4020 | False        | ['?', ' **', '____', "?'", '_____', ' __', "'?", '‑']                                                  |
| Bulgaria  | plain lens max position |        112895 |         80563 | False        | ['",-', '")==', 'wide', '_handler', 'shaw', 'aux', 'whose', 'عهد']                                     |
| Iceland   | J-lens                  |          3596 |          4706 | False        | ['____', ' ______', '________', ' ___', ' ____', '？**', ' __', '___']                                 |
| Iceland   | plain lens              |          9260 |         44705 | False        | [' cherchez', '____', ' Multimedia', '团团', '候选', 'VERN', 'כה', 'apult']                            |
| Iceland   | J-lens max position     |            60 |          1022 | False        | ['?', ' **', '____', "?'", 's', '_____', ' __', '́']                                                    |
| Iceland   | plain lens max position |         80552 |          4173 | False        | ['",-', 'r', '")==', 'wide', ' cherchez', '-', 'i', '...']                                             |
| Turkey    | J-lens                  |          1841 |           432 | False        | [' presidential', ' presidents', ' presidency', '-president', '____', ' governor', '总统', ' Barack']  |
| Turkey    | plain lens              |         53513 |         17069 | False        | ['Dummy', '大道', 'hood', ' opposition', 'ella', 'Geral', ' dura', ' bald']                            |
| Turkey    | J-lens max position     |          5010 |           874 | False        | ['?', ' **', '____', "?'", '\u200e', '\\"', '¬', '_____']                                              |
| Turkey    | plain lens max position |          8385 |          6416 | False        | ['____', 'wide', '________', 'REDIT', '合法性', '实在', '团团', '至今']                                |
| Congo     | J-lens                  |          1284 |         33720 | False        | [' presidential', ' presidents', '____', '-president', ' presidency', ' governor', '.\\"', '________'] |
| Congo     | plain lens              |         31426 |         22197 | False        | ['hood', 'Geral', ' chief', '宝座', ' emer', ' interim', '____', '任期']                               |
| Congo     | J-lens max position     |             2 |         27676 | True         | [' **', '____', ' Congo', '_____', '\\"', '?\\', ' ____', ' ______']                                   |
| Congo     | plain lens max position |           167 |          2425 | False        | ['____', 'wide', ' incontourn', ' trasparen', 'IENTATION', 'ETTA', 'cribed', 'hood']                   |
| spider    | J-lens                  |         21706 |            52 | False        | ['\\"', '____', ' \\"', '___', ' ___', ' ______', '__', '\\n']                                         |
| spider    | plain lens              |         96656 |         93366 | False        | [' saura', '医疗健康', 'ļa', ' усо', ' scientifically', '__;', '/=', '主食']                           |
| spider    | J-lens max position     |           427 |           356 | False        | ['\\"', '____', '?\\', '_____', ' animals', ' **', ' ____', '\\n']                                     |
| spider    | plain lens max position |        136868 |        228652 | False        | [' Prem', 'ord', ' facts', 'oure', 'rophy', 'stuff', 'عهد', '(s']                                      |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_082747_jlens-one-pass/run.md
