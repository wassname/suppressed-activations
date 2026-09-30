---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
k: 32
forward_passes: 5
generations: 0
elapsed_seconds: 16.83
---
# Read with the same unit directions used for editing

Written by PI/OpenAI.

One changed axis: divide each token's lens score by its residual-space direction norm. Layer, position, k and prompt mask are unchanged. This differs from the reference's raw J-lens. Hypothesis: high-norm punctuation directions dominate raw scores; unit directions improve hidden-word ranks. Negative control: apply the same normalisation to the plain lens. The four country cases and the spider case were previously selected; this is development data, not a success rate.

| concept   | readout                |   hidden rank |   answer rank | joint pass   | top8                                                                                                            |
|:----------|:-----------------------|--------------:|--------------:|:-------------|:----------------------------------------------------------------------------------------------------------------|
| Bulgaria  | J-lens                 |           879 |          5002 | False        | ['____', '________', ' ______', ' ___', ' ____', '___', '？**', ' __']                                          |
| Bulgaria  | plain lens             |         15450 |        204256 | False        | ['____', ' cherchez', ' Multimedia', 'あた', '琦', '团团', ' squirt', 'bourg']                                  |
| Bulgaria  | J-lens unit directions |           594 |          4579 | False        | ['这座城市', ' miasta', ' столиц', ' Cities', 'located', '的城市', 'Cities', '城市']                            |
| Bulgaria  | plain unit directions  |         22003 |        204100 | False        | ['____', ' Multimedia', '________', '\ta', ' banjir', ' Poder', '____________', ':a']                           |
| Iceland   | J-lens                 |          3596 |          4706 | False        | ['____', ' ______', '________', ' ___', ' ____', '？**', ' __', '___']                                          |
| Iceland   | plain lens             |          9260 |         44705 | False        | [' cherchez', '____', ' Multimedia', '团团', '候选', 'VERN', 'כה', 'apult']                                     |
| Iceland   | J-lens unit directions |          4949 |          3344 | False        | ['这座城市', ' miasta', ' столиц', ' Cities', 'located', ' şehir', ' CITY', '_city']                            |
| Iceland   | plain unit directions  |         15668 |         61285 | False        | ['____', ' cherchez', ' Multimedia', '________', 'Nota', '____________', ' banjir', '必ず']                     |
| Turkey    | J-lens                 |          1841 |           432 | False        | [' presidential', ' presidents', ' presidency', '-president', '____', ' governor', '总统', ' Barack']           |
| Turkey    | plain lens             |         53513 |         17069 | False        | ['Dummy', '大道', 'hood', ' opposition', 'ella', 'Geral', ' dura', ' bald']                                     |
| Turkey    | J-lens unit directions |          1871 |           535 | False        | ['-president', ' presidente', ' presidents', ' presidency', ' presidential', '总统', ' Präsident', ' governor'] |
| Turkey    | plain unit directions  |         55882 |         16486 | False        | ['Dummy', ' opposition', '橡胶', ' vacancy', '大道', '智库', ' хү', ' bald']                                    |
| Congo     | J-lens                 |          1284 |         33720 | False        | [' presidential', ' presidents', '____', '-president', ' presidency', ' governor', '.\\"', '________']          |
| Congo     | plain lens             |         31426 |         22197 | False        | ['hood', 'Geral', ' chief', '宝座', ' emer', ' interim', '____', '任期']                                        |
| Congo     | J-lens unit directions |          1404 |         35245 | False        | ['-president', ' presidente', ' presidents', ' presidential', ' presidency', ' governor', ' chairman', '总统']  |
| Congo     | plain unit directions  |         32128 |         24866 | False        | ['____', '近年来', ' annually', ' chief', '宝座', ' interim', '橡胶', ' vacancy']                               |
| spider    | J-lens                 |         21706 |            52 | False        | ['\\"', '____', ' \\"', '___', ' ___', ' ______', '__', '\\n']                                                  |
| spider    | plain lens             |         96656 |         93366 | False        | [' saura', '医疗健康', 'ļa', ' усо', ' scientifically', '__;', '/=', '主食']                                    |
| spider    | J-lens unit directions |         21676 |            20 | False        | ['_number', '数量', '数', '(number', ' \\$', '号', '\\$', '3']                                                  |
| spider    | plain unit directions  |         93019 |         95159 | False        | ['医疗健康', ' усо', 'ļa', '主食', ' scientifically', '_audio', '____', ' ______']                              |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_082225_jlens-one-pass/run.md
