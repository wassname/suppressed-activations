---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: data/english_hidden_words_v2.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
answer_alias_audit_json: data/english_v2_answer_alias_audit.json
k: 32
elapsed_seconds: 23.23
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: Sixteen new probes fixed before their first run: eight geography and eight animals, with no concept repeated from v1. Same factual prefix and no trailing space. Freeze J at residual24, plain controls at24/27, final position, k32, prompt mask and greedy-next-token word mask (max_n1). Layer24 was selected in earlier development; mask1 was selected after comparing caps20 and1 on v1. No model-output filtering or retries. Labels are plausible intermediates, not proof the model computes them. Report every case and the expected-answer subset separately. Posthoc scoring annotations: Posthoc annotations of four definite translated-answer leaks seen among J-lens passes. This is incomplete semantic coverage, not a new held-out set. Original prompts and aliases remain unchanged in english_hidden_words_v2.json. These aliases affect scoring only; never the readout or output erasure. Remaining passes are not verified exhaustive semantic exclusions. Translation benchmarks intentionally separate representations of the same meaning by language, so this stronger English bridge-concept criterion must not be conflated with translation-role isolation. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                  | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| Spain     | J-lens                  | False         |           0.730303 |            62 |                      2 | False          | False        |
| Spain     | plain lens              | False         |           0.627879 |         32546 |                    382 | False          | False        |
| Spain     | end-pass J-lens         | False         |           0.833333 |            59 |                      1 | False          | False        |
| Spain     | end-pass plain24        | False         |           0.722424 |         32543 |                    382 | False          | False        |
| Spain     | end-pass plain27        | False         |           0.892121 |           657 |                     40 | False          | False        |
| Spain     | end-pass erased J-lens  | False         |           0.693333 |           235 |                     14 | False          | False        |
| Spain     | end-pass erased plain24 | False         |           0.684848 |         57736 |                    264 | False          | False        |
| Spain     | end-pass erased plain27 | False         |           0.847273 |          4876 |                     68 | False          | False        |
| Portugal  | J-lens                  | False         |           0.858852 |             1 |                      0 | False          | False        |
| Portugal  | plain lens              | False         |           0.748804 |          1349 |                      0 | False          | False        |
| Portugal  | end-pass J-lens         | True          |           1        |             0 |             1000000000 | True           | False        |
| Portugal  | end-pass plain24        | False         |           0.978469 |          1345 |             1000000000 | False          | False        |
| Portugal  | end-pass plain27        | False         |           0.976077 |           385 |             1000000000 | False          | False        |
| Portugal  | end-pass erased J-lens  | True          |           0.992823 |             6 |             1000000000 | True           | True         |
| Portugal  | end-pass erased plain24 | False         |           0.978469 |          2961 |             1000000000 | False          | False        |
| Portugal  | end-pass erased plain27 | False         |           0.970096 |           400 |             1000000000 | False          | False        |
| Germany   | J-lens                  | False         |           0.808571 |             2 |                      0 | False          | False        |
| Germany   | plain lens              | False         |           0.791429 |           440 |                      7 | False          | False        |
| Germany   | end-pass J-lens         | True          |           1        |             1 |             1000000000 | True           | False        |
| Germany   | end-pass plain24        | False         |           0.991429 |           437 |             1000000000 | False          | False        |
| Germany   | end-pass plain27        | True          |           1        |            16 |             1000000000 | True           | False        |
| Germany   | end-pass erased J-lens  | True          |           0.991429 |             0 |             1000000000 | True           | True         |
| Germany   | end-pass erased plain24 | False         |           0.977143 |          6322 |             1000000000 | False          | False        |
| Germany   | end-pass erased plain27 | False         |           0.997143 |          1412 |             1000000000 | False          | False        |
| Greece    | J-lens                  | False         |           0.853333 |             5 |                      0 | False          | False        |
| Greece    | plain lens              | False         |           0.803333 |            21 |                     17 | False          | False        |
| Greece    | end-pass J-lens         | True          |           1        |             4 |             1000000000 | True           | True         |
| Greece    | end-pass plain24        | True          |           0.99     |            20 |             1000000000 | True           | True         |
| Greece    | end-pass plain27        | True          |           1        |             2 |             1000000000 | True           | True         |
| Greece    | end-pass erased J-lens  | False         |           0.96     |            96 |             1000000000 | False          | False        |
| Greece    | end-pass erased plain24 | False         |           0.983333 |           159 |             1000000000 | False          | False        |
| Greece    | end-pass erased plain27 | False         |           1        |            98 |             1000000000 | False          | False        |
| Austria   | J-lens                  | False         |           0.871212 |             4 |                      0 | False          | False        |
| Austria   | plain lens              | False         |           0.738636 |           366 |                     17 | False          | False        |
| Austria   | end-pass J-lens         | True          |           1        |             3 |             1000000000 | True           | False        |
| Austria   | end-pass plain24        | False         |           0.939394 |           364 |             1000000000 | False          | False        |
| Austria   | end-pass plain27        | True          |           1        |             7 |             1000000000 | True           | False        |
| Austria   | end-pass erased J-lens  | True          |           0.973485 |            12 |             1000000000 | True           | True         |
| Austria   | end-pass erased plain24 | False         |           0.924242 |          4459 |             1000000000 | False          | False        |
| Austria   | end-pass erased plain27 | True          |           0.996212 |             8 |             1000000000 | True           | False        |
| Norway    | J-lens                  | False         |           0.885621 |             3 |                      0 | False          | False        |
| Norway    | plain lens              | False         |           0.888889 |            78 |                      7 | False          | False        |
| Norway    | end-pass J-lens         | True          |           1        |             2 |             1000000000 | True           | True         |
| Norway    | end-pass plain24        | False         |           1        |            77 |             1000000000 | False          | False        |
| Norway    | end-pass plain27        | True          |           1        |             1 |             1000000000 | True           | True         |
| Norway    | end-pass erased J-lens  | True          |           0.980392 |            14 |             1000000000 | True           | True         |
| Norway    | end-pass erased plain24 | False         |           0.993464 |           970 |             1000000000 | False          | False        |
| Norway    | end-pass erased plain27 | True          |           1        |            17 |             1000000000 | True           | True         |
| Thailand  | J-lens                  | False         |           0.909091 |             4 |                      0 | False          | False        |
| Thailand  | plain lens              | False         |           0.909091 |          2215 |                     88 | False          | False        |
| Thailand  | end-pass J-lens         | True          |           0.970455 |             3 |             1000000000 | True           | False        |
| Thailand  | end-pass plain24        | False         |           0.943182 |          2214 |             1000000000 | False          | False        |
| Thailand  | end-pass plain27        | False         |           0.998864 |           489 |             1000000000 | False          | False        |
| Thailand  | end-pass erased J-lens  | False         |           0.790909 |           210 |             1000000000 | False          | False        |
| Thailand  | end-pass erased plain24 | False         |           0.814773 |         18755 |             1000000000 | False          | False        |
| Thailand  | end-pass erased plain27 | False         |           0.859091 |          1803 |             1000000000 | False          | False        |
| Kenya     | J-lens                  | False         |           0.920635 |             1 |                      0 | False          | False        |
| Kenya     | plain lens              | False         |           0.904762 |            40 |                      0 | False          | False        |
| Kenya     | end-pass J-lens         | True          |           1        |             0 |             1000000000 | True           | True         |
| Kenya     | end-pass plain24        | False         |           1        |            39 |             1000000000 | False          | False        |
| Kenya     | end-pass plain27        | True          |           1        |             0 |             1000000000 | True           | True         |
| Kenya     | end-pass erased J-lens  | False         |           0.944444 |            61 |             1000000000 | False          | False        |
| Kenya     | end-pass erased plain24 | False         |           0.984127 |          1313 |             1000000000 | False          | False        |
| Kenya     | end-pass erased plain27 | False         |           1        |            34 |             1000000000 | False          | False        |
| horse     | J-lens                  | True          |           0.929338 |             1 |             1000000000 |                |              |
| horse     | plain lens              | False         |           0.731664 |            37 |             1000000000 |                |              |
| horse     | end-pass J-lens         | True          |           0.929338 |             1 |             1000000000 |                |              |
| horse     | end-pass plain24        | False         |           0.731664 |            37 |             1000000000 |                |              |
| horse     | end-pass plain27        | True          |           0.968694 |             0 |             1000000000 |                |              |
| horse     | end-pass erased J-lens  | True          |           0.924866 |             1 |             1000000000 |                |              |
| horse     | end-pass erased plain24 | False         |           0.719141 |            43 |             1000000000 |                |              |
| horse     | end-pass erased plain27 | True          |           0.968694 |             0 |             1000000000 |                |              |
| cow       | J-lens                  | True          |           0.816667 |            41 |                     77 | False          | True         |
| cow       | plain lens              | False         |           0.412667 |         24092 |                   3937 | False          | False        |
| cow       | end-pass J-lens         | True          |           0.838    |            41 |                     77 | False          | True         |
| cow       | end-pass plain24        | False         |           0.474    |         24090 |                   3937 | False          | False        |
| cow       | end-pass plain27        | False         |           0.636    |             0 |                      1 | False          | False        |
| cow       | end-pass erased J-lens  | True          |           0.847333 |            47 |                     78 | False          | True         |
| cow       | end-pass erased plain24 | False         |           0.482    |         37235 |                   5221 | False          | False        |
| cow       | end-pass erased plain27 | False         |           0.646667 |             0 |                      1 | False          | False        |
| goat      | J-lens                  | True          |           0.977273 |             3 |                     55 | True           | True         |
| goat      | plain lens              | False         |           0.795455 |          9977 |                   5403 | False          | False        |
| goat      | end-pass J-lens         | True          |           1        |             3 |                     54 | True           | True         |
| goat      | end-pass plain24        | False         |           0.943182 |          9977 |                   5403 | False          | False        |
| goat      | end-pass plain27        | False         |           0.943182 |            32 |                   1224 | False          | False        |
| goat      | end-pass erased J-lens  | True          |           1        |             4 |                     58 | True           | True         |
| goat      | end-pass erased plain24 | False         |           0.943182 |         11232 |                   5643 | False          | False        |
| goat      | end-pass erased plain27 | False         |           0.931818 |           116 |                   2110 | False          | False        |
| duck      | J-lens                  | False         |           0.808271 |            38 |                   2513 | False          | False        |
| duck      | plain lens              | False         |           0.830827 |           146 |                   1065 | False          | False        |
| duck      | end-pass J-lens         | False         |           0.808271 |            38 |                   2513 | False          | False        |
| duck      | end-pass plain24        | False         |           0.830827 |           146 |                   1065 | False          | False        |
| duck      | end-pass plain27        | True          |           0.800752 |            29 |                    381 | True           | True         |
| duck      | end-pass erased J-lens  | False         |           0.819549 |            33 |                   2612 | False          | False        |
| duck      | end-pass erased plain24 | False         |           0.836466 |           160 |                   1190 | False          | False        |
| duck      | end-pass erased plain27 | True          |           0.800752 |            31 |                    383 | True           | True         |
| cat       | J-lens                  | False         |           0.892754 |            30 |                      1 | False          | False        |
| cat       | plain lens              | False         |           0.765217 |         12091 |                    178 | False          | False        |
| cat       | end-pass J-lens         | True          |           1        |            28 |             1000000000 | True           | False        |
| cat       | end-pass plain24        | False         |           1        |         12082 |             1000000000 | False          | False        |
| cat       | end-pass plain27        | False         |           1        |           293 |             1000000000 | False          | False        |
| cat       | end-pass erased J-lens  | False         |           0.994203 |          1619 |             1000000000 | False          | False        |
| cat       | end-pass erased plain24 | False         |           0.976812 |         36002 |             1000000000 | False          | False        |
| cat       | end-pass erased plain27 | False         |           0.969565 |         16096 |             1000000000 | False          | False        |
| chicken   | J-lens                  | False         |           0.488415 |           614 |                    797 | False          | False        |
| chicken   | plain lens              | False         |           0.42561  |         40921 |                 230691 | False          | False        |
| chicken   | end-pass J-lens         | False         |           0.488415 |           614 |                    797 | False          | False        |
| chicken   | end-pass plain24        | False         |           0.42561  |         40921 |                 230690 | False          | False        |
| chicken   | end-pass plain27        | False         |           0.540244 |          3408 |                 173850 | False          | False        |
| chicken   | end-pass erased J-lens  | False         |           0.504268 |           846 |                  11970 | False          | False        |
| chicken   | end-pass erased plain24 | False         |           0.414024 |         36185 |                 206827 | False          | False        |
| chicken   | end-pass erased plain27 | False         |           0.542683 |          3825 |                 202395 | False          | False        |
| octopus   | J-lens                  | False         |           0.114286 |          3933 |                  14621 | False          | False        |
| octopus   | plain lens              | False         |           0.457143 |         89133 |                 246314 | False          | False        |
| octopus   | end-pass J-lens         | False         |           0.114286 |          3932 |                  14620 | False          | False        |
| octopus   | end-pass plain24        | False         |           0.457143 |         89133 |                 246313 | False          | False        |
| octopus   | end-pass plain27        | False         |           0.428571 |        110300 |                 245847 | False          | False        |
| octopus   | end-pass erased J-lens  | False         |           0.171429 |          8668 |                 135255 | False          | False        |
| octopus   | end-pass erased plain24 | False         |           0.457143 |         70521 |                 242128 | False          | False        |
| octopus   | end-pass erased plain27 | False         |           0.428571 |        111647 |                 246140 | False          | False        |
| penguin   | J-lens                  | False         |           0.497186 |          7170 |                   2905 | False          | False        |
| penguin   | plain lens              | False         |           0.531895 |           645 |                 149141 | False          | False        |
| penguin   | end-pass J-lens         | False         |           0.497186 |          7169 |                   2905 | False          | False        |
| penguin   | end-pass plain24        | False         |           0.531895 |           645 |                 149141 | False          | False        |
| penguin   | end-pass plain27        | False         |           0.413696 |          2035 |                 143813 | False          | False        |
| penguin   | end-pass erased J-lens  | False         |           0.503752 |          9565 |                  54014 | False          | False        |
| penguin   | end-pass erased plain24 | False         |           0.525328 |           649 |                 125976 | False          | False        |
| penguin   | end-pass erased plain27 | False         |           0.427767 |          2005 |                 183220 | False          | False        |

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

J-lens: [' Barcelona', ' Paris', ' Madrid', ' Berlin', ' Dublin', ' London', ' Munich', ' Lisbon', ' Vienna', ' Budapest', ' Rome', ' Jerusalem', ' Prague', ' Frankfurt', ' Amsterdam', ' Istanbul', ' Zurich', ' Stockholm', ' Buenos', 'Paris', ' Stuttgart', ' Bangkok', ' Vatican', ' Brussels', 'Madrid', ' Athens', ' Tehran', 'Barcelona', ' Oslo', ' Helsinki', ' Marseille', ' Chicago']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

plain lens: ['više', '遥遥', '过神', 'ẩm', 'urin', ' unic', 'に行ってきました', ' Luân', 'rome', '先到', '马拉', 'located', ' ogs', 'olz', ' NOT', 'nota', 'agus', '来ました', ' catholic', ' Catholic', '...*', 'also', '现任', '现', ' dát', '万国', 'not', ' selfies', '省会', '金斯', 'NULL', 'EMP']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass J-lens: [' Paris', ' Madrid', ' Berlin', ' Dublin', ' London', ' Munich', ' Lisbon', ' Vienna', ' Rome', ' Budapest', ' Jerusalem', ' Prague', ' Frankfurt', ' Amsterdam', ' Zurich', ' Istanbul', ' Stockholm', ' Buenos', 'Paris', ' Vatican', ' Bangkok', ' Stuttgart', ' Brussels', ' Athens', 'Madrid', ' Tehran', ' Oslo', ' Helsinki', '巴黎', ' Taipei', ' Chicago', ' Marseille']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass plain24: ['više', '遥遥', '过神', 'ẩm', 'urin', ' unic', 'に行ってきました', ' Luân', 'rome', '先到', '马拉', 'located', ' ogs', 'olz', ' NOT', 'nota', 'agus', '来ました', ' catholic', ' Catholic', '...*', 'also', '现任', '现', ' dát', '万国', 'not', ' selfies', '省会', '金斯', 'NULL', 'EMP']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass plain27: ['celona', '北京', ' també', 'agues', '巴塞罗那', ' capitals', ' NOT', '编辑于', 'rome', 'nici', '过神', ' Roses', 'NOT', '.cat', ' Capitals', 'ague', 'also', 'หาง', 'usal', ' cath', ' Lle', '台北', '少儿', ' biro', '้ม', ' Vatican', 'atri', '不完全统计', ' бази', ' catal', 'lah', ' Rome']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass erased J-lens: [' Paris', ' Vatican', ' Rome', ' Berlin', ' Dublin', ' Vienna', ' London', ' Jerusalem', ' Munich', '.\\', ' Lisbon', ' Zurich', ' Prague', ' Frankfurt', ' Madrid', ' City', ' Oslo', ' Naples', ' Stuttgart', ' Istanbul', ' San', ' Heidelberg', ' Budapest', ' France', ' Taipei', ' Germany', ' Toronto', ' Italy', ' Brussels', ' Athens', ' Jakarta', ' Switzerland']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass erased plain24: ['više', '过神', '遥遥', 'ẩm', ' unic', 'urin', 'rome', '先到', 'に行ってきました', 'located', ' NOT', '马拉', ' Luân', '现', ' ogs', 'not', ' catholic', '现任', 'olz', ' Catholic', 'nota', 'agus', 'also', '来ました', '金斯', '...*', 'NULL', '担', '现为', '落成', ' selfies', ' lions']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Sagrada Familia is'

Baseline: ' Barcelona.\nQuestion: What is the'

end-pass erased plain27: [' NOT', ' també', '北京', 'agues', '...', ' capitals', 'NOT', 'rome', 'atri', ' cath', 'also', 'lah', 'not', '过神', '编辑于', 'หาง', ' NULL', 'ague', '灯火', 'nici', 'usal', '้ม', '少儿', '____', '布拉', 'celona', ' тоже', ' Capitals', ' Roses', '泼', '不完全统计', ' 수도']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

J-lens: [' Lisbon', ' Portugal', ' Jakarta', ' Madrid', ' London', ' Paris', ' Amsterdam', ' Lisboa', ' Berlin', ' Brussels', ' Rome', ' Vienna', ' Portuguese', ' Buenos', ' Dublin', ' Brasília', ' Athens', ' Porto', ' Istanbul', ' Rotterdam', ' Portland', ' Bogotá', ' Washington', ' Brazil', ' Venice', ' Moscow', '葡萄牙', ' Barcelona', ' Ankara', ' Johannesburg', ' Caracas', ' Frankfurt']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

plain lens: ['lis', 'rome', '...**', '...\\', 'reis', '...”', '心惊', 'ẩm', ' Lus', '...*', ' Goed', '…]', 'AMAN', ' Luân', ' ogs', ' Fras', '葡', ".'.", ' Lisbon', ').(', '.".', '日游', '...).', 'lima', '...)', '先到', 'lah', '现为', ' الرس', ' greve', ' ALSO', ' correc']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass J-lens: [' Portugal', ' Jakarta', ' Madrid', ' Paris', ' London', ' Amsterdam', ' Lisboa', ' Berlin', ' Brussels', ' Rome', ' Vienna', ' Portuguese', ' Buenos', ' Athens', ' Dublin', ' Brasília', ' Porto', ' Istanbul', ' Bogotá', ' Washington', ' Portland', ' Rotterdam', ' Brazil', ' Venice', ' Moscow', '葡萄牙', ' Barcelona', ' Ankara', ' Caracas', ' Johannesburg', ' Frankfurt', ' Prague']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass plain24: ['rome', '...**', '...\\', '...”', 'reis', '心惊', 'ẩm', ' Lus', '...*', ' Goed', '…]', 'AMAN', ' Luân', ' ogs', ' Fras', '葡', ".'.", ').(', '.".', '...).', '日游', 'lima', '...)', 'lah', '先到', '现为', ' الرس', ' ALSO', ' correc', ' greve', '�', '}`).']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass plain27: ['里斯', ' capitale', ' capitals', ' Capitals', 'リス', ' Bras', '-capital', 'rome', ' Hauptstadt', '资本', '首都', ' thủ', ' پای', 'หลวง', '布拉', ' capitalist', ' العاصمة', '我也去', ' 수도', ' lus', ' капит', ' Washington', 'bras', '葡萄牙', ' Lus', 'сто', ' Fras', ' lim', '})",', 'lima', '資本', '亚马']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass erased J-lens: [' Paris', ' London', ' Jakarta', ' Washington', '...', ' Rome', ' Amsterdam', ' Portugal', ' Philadelphia', ' City', ' Berlin', ' Brazil', ' Buenos', ' Madrid', ' Toronto', '.\\', ' Boston', ' Porto', ' Miami', ' São', ' Frankfurt', ' Brussels', '.', '杭州', ' Rio', ' Vienna', ' Mexico', ' Sydney', ' Seattle', ' Port', ' Portland', ' Barcelona']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass erased plain24: ['rome', '...”', '...**', '...\\', '心惊', 'reis', 'ẩm', '...*', '...)', '____', 'also', ' Goed', ' also', ' NOT', '�', '现为', ".'.", '...).', '.".', '先到', '...', '...(', 'not', ' ogs', ' democr', 'AMAN', 'nota', 'lah', ' Lus', ' фо', ' сов', ' dumps']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Belem Tower is'

Baseline: ' Lisbon.\nHypothesis: The'

end-pass erased plain27: [' capitals', '里斯', ' capitale', ' Bras', ' Capitals', '资本', 'rome', 'リス', '-capital', ' lim', '首都', '布拉', ' پای', ' capitalist', ' thủ', ' 수도', ' капит', ' Washington', ' Hauptstadt', 'หลวง', 'lim', '我也去', '...”', 'сто', ' NOT', 'forth', 'bras', '...)', '})",', ' lame', '直流', ' Liz']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

J-lens: [' Berlin', ' Paris', ' Germany', ' London', ' Frankfurt', ' Munich', ' Vienna', 'Berlin', ' Prague', ' Moscow', ' Brussels', ' Budapest', ' Amsterdam', ' Madrid', ' Rome', 'Paris', ' berlin', ' Stockholm', ' Hamburg', ' Beijing', ' Stuttgart', ' Leipzig', ' Warsaw', ' Heidelberg', ' Düsseldorf', 'London', '巴黎', 'Germany', ' Copenhagen', ' Jakarta', '柏林', ' Athens']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

plain lens: ['北京', '到北京', '是北京', '北京的', 'ẩm', 'aches', ' Luân', '在北京', ' Berlin', 'više', ' dumps', ' pano', ' Capitals', '先到', 'located', 'ruhe', ' خاک', 'halte', '.idea', ' Pots', 'otope', ' ogs', 'also', 'spo', 'ปัก', 'ॅ', 'stad', 'кови', '美术学院', '...\\', '議', ' boo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass J-lens: [' Paris', ' Germany', ' London', ' Frankfurt', ' Munich', ' Vienna', ' Moscow', ' Prague', ' Brussels', ' Budapest', ' Amsterdam', ' Madrid', ' Rome', 'Paris', ' Stockholm', ' Stuttgart', ' Beijing', ' Hamburg', ' Warsaw', ' Leipzig', ' Düsseldorf', ' Heidelberg', '巴黎', 'London', ' Copenhagen', '柏林', 'Germany', ' Jakarta', ' Athens', ' Karlsruhe', ' German', ' Austria']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass plain24: ['北京', '到北京', '是北京', '北京的', 'ẩm', 'aches', ' Luân', 'više', '在北京', ' dumps', ' pano', ' Capitals', '先到', 'located', 'ruhe', ' خاک', 'halte', '.idea', ' Pots', 'otope', ' ogs', 'also', 'spo', 'stad', 'ॅ', 'ปัก', 'кови', '美术学院', '議', '...\\', '...**', ' boo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass plain27: ['柏林', '北京', ' Pots', ' Bonn', '北京的', '是北京', ' capitals', 'prs', ' Бер', '到北京', '京', '_dc', ' Washington', '在北京', 'Frank', ' Capitals', ' German', '德国', ' Germany', ' Washing', '法兰克福', ' Beijing', '直流', 'Москва', '_ber', ' Hauptstadt', ' Frankfurt', ' thủ', ' Rome', 'DC', '京城', '杭州']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass erased J-lens: [' Germany', ' Austria', '.\\', ' Vienna', ' France', ' Luxembourg', ' Heidelberg', ' Romania', ' Brussels', ' Prague', ' Denmark', ' Frankfurt', ' Italy', ' Budapest', ' Poland', ' Munich', ' Netherlands', '____', ' Rome', ' Belgium', ' Paris', ' Hungary', ' Athens', ' Switzerland', ' Karlsruhe', ' Düsseldorf', ' Greece', ' Croatia', ' Russia', ' City', 'Germany', ' Copenhagen']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass erased plain24: ['aches', 'ẩm', ' dumps', '先到', ' pano', 'halte', 'više', 'ruhe', 'located', '.idea', ' Luân', ' خاک', '北京', 'also', 'stad', 'otope', '教体', '議', 'spo', 'ॅ', ' Capitals', ' ogs', '...\\', ' boo', '心惊', '美术学院', '到北京', 'кови', '...**', ' Fras', 'ẹo', ' NOT']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Brandenburg Gate is'

Baseline: ' Berlin.\nHypothesis: The'

end-pass erased plain27: [' Pots', 'prs', ' capitals', 'Frank', '...', ' Washing', '不来', 'Pr', '马克', '焰', ' reun', '北京', '�', '_dc', 'zap', 'واب', ' NOT', ' Capitals', '风向', '布拉', '魏', ' Bonn', 'also', ' Charl', ' thủ', '赖', '想知道', 'Bad', ' Pru', ' خاک', ' Hauptstadt', ' also']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

J-lens: [' London', ' Athens', ' Paris', ' Rome', ' Berlin', ' Greece', ' Madrid', 'London', 'Paris', ' Istanbul', ' Vienna', ' Dublin', ' Brussels', ' Lisbon', ' Amsterdam', ' Alexandria', ' Londres', ' Italy', ' Budapest', ' Cairo', '巴黎', '伦敦', ' Moscow', ' Barcelona', ' Venice', ' France', ' Munich', ' Jerusalem', ' Prague', ' Jakarta', ' Tehran', ' Ankara']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

plain lens: ['现', '名胜', '先到', ' dumps', ' Luân', 'located', '现任', ' NOT', '美术学院', ' Rome', '.idea', ' geweest', 'više', '现为', ' democr', '希腊', '北京', ' ALSO', ' Athens', '历史文化', 'hatian', 'acre', 'gree', 'currently', ' freaking', '}`).', ' Greece', 'aches', 'ẩm', '…]', '讹', 'olon']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass J-lens: [' London', ' Paris', ' Rome', ' Berlin', ' Greece', ' Madrid', 'London', 'Paris', ' Vienna', ' Istanbul', ' Dublin', ' Brussels', ' Lisbon', ' Amsterdam', ' Alexandria', ' Londres', ' Italy', ' Budapest', ' Cairo', '巴黎', ' Moscow', '伦敦', ' Barcelona', ' Venice', ' France', ' Munich', ' Jerusalem', ' Prague', ' Jakarta', ' Tehran', ' Ankara', ' England']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass plain24: ['现', '名胜', '先到', ' dumps', ' Luân', 'located', '现任', ' NOT', '美术学院', ' Rome', '.idea', ' geweest', 'više', '现为', ' democr', '希腊', '北京', ' ALSO', 'hatian', '历史文化', 'currently', 'acre', 'gree', ' freaking', ' Greece', '}`).', 'aches', 'ẩm', '…]', 'olon', '讹', '...\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass plain27: ['雅典', '希腊', ' Greece', ' Greek', ' Aten', '北京', 'Greek', ' أث', ' Athena', ' Rome', '古希腊', ' Pir', ' Ancient', ' Griechen', 'gree', ' London', ' ancient', 'reece', ' demokrat', 'กรี', ' Greeks', ' democr', 'rome', ' гр', ' NOT', ' Paris', ' Hauptstadt', ' Olympia', 'θή', ' Washington', '第一中学', ' Berlin']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass erased J-lens: [' London', ' Paris', ' Berlin', ' Rome', ' Madrid', ' France', 'London', 'Paris', ' Italy', ' Washington', ' Vienna', ' Vatican', ' City', ' England', '.\\', ' Amsterdam', ' Westminster', ' Barcelona', ' Dublin', '巴黎', ' Roman', '...', '伦敦', ' Philadelphia', ' Istanbul', ' Brussels', ' Budapest', ' Boston', ' Roma', ' Jerusalem', ' Frankfurt', ' Germany']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass erased plain24: ['现', ' dumps', '先到', ' NOT', 'located', '名胜', '现任', '美术学院', '北京', 'currently', '历史文化', '现为', '____', '.idea', ' Luân', ' supposed', ' democr', 'acre', 'aches', ' geweest', ' freaking', 'not', 'also', ' also', ' located', '}`).', ' ALSO', 'igin', '_not', '讹', '古迹', '...\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Parthenon is'

Baseline: ' Athens.\nHypothesis: The'

end-pass erased plain27: ['...', '北京', ' ', ':', "'", ' Pir', ' NOT', '…', '现', '希腊', ' ancient', '存在', 'A', '.', '`', '"', '**', '\r\n', '?', '____', '-', 'now', ' Washington', ' Ancient', '新', '贞', '}', '现在', ' located', '\n', ' not', ' London']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

J-lens: [' Vienna', ' Berlin', ' Prague', ' Munich', ' Austria', ' Brussels', ' Paris', ' Germany', ' Madrid', ' Budapest', ' Frankfurt', ' Lisbon', ' Luxembourg', '维也纳', ' London', ' Belgium', ' Dublin', ' Rome', ' Salzburg', ' Amsterdam', ' Heidelberg', ' France', ' Stuttgart', ' Copenhagen', ' Bruxelles', 'ustria', 'Berlin', ' Portugal', 'Paris', ' Moscow', ' Karlsruhe', ' Hamburg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

plain lens: ['ogl', '现', 'located', ' ogs', '先到', '้ม', 'halte', '现任', ' dumps', 'ẹo', '现为', 'više', 'spo', '}`).', ' spo', '美术学院', 'ถัด', ' Vienna', '...\\', ' nota', ' Capitals', '…]', ' Fras', '现车', '...**', '名胜', ' none', '历任', ' แฟ', ' NOT', '适', 'aches']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass J-lens: [' Berlin', ' Prague', ' Munich', ' Austria', ' Brussels', ' Paris', ' Germany', ' Budapest', ' Frankfurt', ' Madrid', ' Lisbon', ' Luxembourg', ' Belgium', '维也纳', ' London', ' Dublin', ' Rome', ' Salzburg', ' Amsterdam', ' Heidelberg', ' France', ' Stuttgart', ' Copenhagen', ' Bruxelles', 'ustria', 'Berlin', ' Portugal', 'Paris', ' Moscow', ' Hamburg', ' Karlsruhe', ' Italy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass plain24: ['ogl', '现', 'located', ' ogs', '้ม', '先到', 'halte', '现任', ' dumps', '现为', 'ẹo', 'više', 'spo', '}`).', ' spo', '美术学院', 'ถัด', '...\\', ' nota', ' Capitals', '…]', '...**', '现车', ' Fras', '名胜', ' แฟ', ' none', '历任', ' NOT', '适', 'に行ってきました', 'aches']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass plain27: ['Vi', '维也纳', ' Wien', ' Viên', ' Wiener', ' Vi', '北京', ' Aust', '杭州', ' capitals', ' Graz', ' Inns', '...', 'Wi', ' Austria', ' Austrian', '奥地利', 'više', ' Berlin', ' Rome', ' Capitals', 'เวียน', ' aust', ' Від', '京城', ' Hauptstadt', '京师', 'กรุง', 'vi', 'VI', 'Invalid', '_vi']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass erased J-lens: [' Berlin', ' Germany', ' Paris', ' France', ' Frankfurt', ' Luxembourg', ' Brussels', ' Portugal', ' Belgium', ' Munich', ' Madrid', ' London', ' Austria', ' Rome', ' Italy', ' Amsterdam', ' Heidelberg', ' Dublin', ' Prague', ' Denmark', '.\\', ' Stuttgart', ' German', ' Budapest', ' Lisbon', ' Bruxelles', ' Barcelona', ' Netherlands', ' Deutschland', ' Bav', ' München', ' Washington']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass erased plain24: ['ogl', '现', 'located', '้ม', '先到', '现任', ' spo', ' dumps', 'halte', ' NOT', '...', ' nota', '现为', 'spo', '适', ' none', '美术学院', 'also', '...\\', 'not', ' ogs', 'ẹo', '}`).', ' graz', 'ถัด', ' also', 'slug', ' kap', 'aches', '隶', '历任', 'otope']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Schonbrunn Palace is'

Baseline: ' Vienna.\nHypothesis: The'

end-pass erased plain27: ['...', '北京', ' capitals', 'Vi', 'W', 'V', '杭州', ':', ' Aust', 'Invalid', ' Graz', '…', 'w', ' NOT', 'DC', '____', '`', ' Wien', 'not', '....', ' ...', ' called', ' Wars', '蹦', ' Pest', ' Viên', ' Inns', 'NOT', ' aust', 'Wi', ' پای', '?']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

J-lens: [' Oslo', ' Berlin', ' Stockholm', ' Norway', ' Copenhagen', ' Paris', ' Amsterdam', ' Denmark', ' Helsinki', ' London', ' Vienna', ' Sweden', ' Seoul', ' Zurich', ' Germany', ' Frankfurt', ' Rotterdam', ' Munich', ' Brussels', ' Edinburgh', ' NYC', ' Bogotá', ' Hamburg', ' Jakarta', ' Johannesburg', ' Heidelberg', ' Moscow', ' Toronto', ' Switzerland', ' Madrid', ' Lisbon', ' Prague']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

plain lens: ['urin', 'located', 'also', ' ogs', 'hatian', 'otope', 'više', ' Oslo', '现', 'stad', ' also', ' democr', ' сов', ' eget', '小编为大家整理的', '同样', '人名', ' pano', '遥遥', ' Haga', '威士', 'agin', ' NOT', '人受伤', 'emies', 'AGENT', '金属材料', ' ALSO', ' også', '镐', '现为', ' likewise']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass J-lens: [' Berlin', ' Stockholm', ' Norway', ' Copenhagen', ' Paris', ' Amsterdam', ' Denmark', ' Helsinki', ' London', ' Vienna', ' Sweden', ' Seoul', ' Zurich', ' Germany', ' Frankfurt', ' Rotterdam', ' Munich', ' NYC', ' Brussels', ' Edinburgh', ' Bogotá', ' Hamburg', ' Jakarta', ' Heidelberg', ' Johannesburg', ' Moscow', ' Toronto', ' Switzerland', ' Madrid', ' Stuttgart', ' Prague', ' Lisbon']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass plain24: ['urin', 'located', 'also', ' ogs', 'hatian', 'otope', 'više', '现', 'stad', ' also', ' democr', ' сов', ' eget', '小编为大家整理的', '同样', '人名', ' pano', '遥遥', ' Haga', '威士', 'agin', ' NOT', '人受伤', 'emies', 'AGENT', '金属材料', ' også', ' ALSO', '现为', '镐', ' mates', ' likewise']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass plain27: [' Haga', ' Norway', ' hoved', 'stad', 'Os', '奥斯', ' нор', ' norsk', ' Norwegian', ' eget', ' trondheim', 'NOT', ' NOT', 'Nor', 'じめて', '现', '不详', ' stavanger', ' ALSO', 'ovre', ' kristiansand', '挪威', ' Trom', ' også', 'iania', ' norway', '精彩内容', 'Ups', 'asjon', ' Scandin', 'ctl', 'flate']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass erased J-lens: [' Berlin', ' Germany', ' Paris', ' London', ' Denmark', ' France', ' Amsterdam', ' Vienna', ' Sweden', ' New', ' Frankfurt', ' Hamburg', ' Netherlands', ' Switzerland', ' Norway', ' Stockholm', ' City', '.\\', ' Munich', ' Copenhagen', ' Brussels', ' NYC', ' Heidelberg', ' Toronto', ' Austria', ' Rotterdam', ' Portland', ' San', ' Italy', ' Belgium', ' Barcelona', ' Philadelphia']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass erased plain24: ['also', 'located', ' also', '现', 'urin', '同样', 'otope', ' NOT', ' сов', 'hatian', ' democr', '人名', 'više', ' eget', ' likewise', ' terletak', ' ogs', 'name', '小编为大家整理的', 'stad', ' located', ' dudes', 'not', ' mates', ' pano', '�', '现为', '相同的', 'agin', '金属材料', ' feminism', 'NOT']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Vigeland Sculpture Park is'

Baseline: ' Oslo.\nHypothesis: The'

end-pass erased plain27: [' NOT', '现', ' hoved', 'NOT', '同样', ' Haga', '不详', 'stad', ' called', '同一个', '相同的', ' eget', '卑', 'Not', 'called', 'also', ' også', '同上', 'Nor', 'Ups', ' Christianity', 'not', 'ctl', ' Christian', '精彩内容', 'じめて', ' ders', ' Trom', ' Vest', '也称为', ' 역시', '.prototype']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

J-lens: [' Bangkok', ' Jakarta', ' Kuala', ' Nairobi', ' Thailand', ' Taipei', ' Honolulu', ' Seoul', ' London', ' Brasília', ' Manila', ' Bogotá', 'Jakarta', ' Islamabad', ' Berlin', ' Budapest', ' Beijing', ' Cairo', ' Riyadh', ' Stockholm', ' Dubai', ' Singapore', '曼谷', ' Athens', ' Canberra', ' Madrid', ' Mumbai', ' Tehran', ' Helsinki', ' Caracas', ' Paris', ' Ankara']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

plain lens: ['现', '现在的', 'now', '-now', '现在', 'NOW', 'currently', '现为', '现在有', ' now', '现今', '现任', ' nowadays', ' kini', ' maintenant', 'reis', '他现在', '目前的', '現在的', 'ernen', '現在', '名胜', '現', '现价', ' الآن', '.".', '现代化', 'current', '现已', '她现在', ' celu', ' NOW']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass J-lens: [' Jakarta', ' Kuala', ' Nairobi', ' Thailand', ' Taipei', ' Honolulu', ' Seoul', ' London', ' Brasília', ' Manila', ' Bogotá', 'Jakarta', ' Budapest', ' Islamabad', ' Berlin', ' Beijing', ' Cairo', ' Riyadh', ' Dubai', ' Stockholm', '曼谷', ' Singapore', ' Athens', ' Madrid', ' Canberra', ' Mumbai', ' Tehran', ' Helsinki', ' Caracas', ' Paris', ' Ankara', ' Amsterdam']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass plain24: ['现', '现在的', 'now', '-now', '现在', 'NOW', 'currently', '现为', '现在有', ' now', '现今', '现任', ' nowadays', ' kini', ' maintenant', 'reis', '他现在', '目前的', '現在的', 'ernen', '現在', '名胜', '現', '现价', ' الآن', '.".', '现代化', 'current', '现已', '她现在', ' celu', ' NOW']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass plain27: ['currently', 'now', '现在的', ' capitale', '现在', '他现在', ' capitals', ' Hauptstadt', ' currently', '现任', ' nowadays', '现为', '现在是', '如今的', ' kini', ' Capitals', 'angkok', '现', '現在的', ' now', ' Băng', ' Fras', '现今', '现在有', '現在', '-now', '她现在', ' obecnie', '現在の', '我现在', 'NOW', '现已']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass erased J-lens: [' now', 'now', '现在', '现在的', ' Jakarta', ' City', '.\\', ' Now', '.', ' London', '现', ' Berlin', ' Kuala', ' Paris', ' currently', '...', '现在是', 'city', '?', ' New', ' Toronto', ' Singapore', ' today', ' cities', ' city', ' Cairo', ' modern', ' San', ' Brasília', ' Stockholm', ' Washington', ' Dubai']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass erased plain24: ['现', '现在的', 'now', '现在', ' now', '-now', 'NOW', '现为', 'currently', '现今', '现任', '现在有', ' nowadays', ' maintenant', ' kini', '他现在', '現在', '目前的', 'current', '現', 'reis', '现价', '现代化', 'Now', '現在的', '现已', 'ernen', '今', ' currently', '现行', ' NOW', '名胜']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country formerly called Siam is'

Baseline: ' Bangkok.\nQuestion: What is the'

end-pass erased plain27: ['now', '现在', '现在的', 'currently', ' now', ' currently', '他现在', '现', '现任', ' capitals', ' capitale', '现在是', '现为', '现今', ' nowadays', 'current', '現在', '如今', '我现在', '目前', '如今的', '现已', ' kini', '她现在', '现在有', ' сейчас', '目前的', 'NOW', '現在的', '你现在', '現在の', 'Currently']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

J-lens: [' Nairobi', ' Kenya', ' Johannesburg', ' Vienna', ' Dublin', ' Prague', ' London', ' Dubai', ' Denver', ' Tanzania', ' Bangkok', ' Cairo', ' Budapest', ' Canberra', ' Lagos', ' Ankara', ' Toronto', ' Melbourne', ' Bogotá', ' Brisbane', ' Uganda', ' Riyadh', ' Berlin', ' Kansas', ' Madrid', ' Munich', ' Chicago', ' Jakarta', ' Miami', ' Birmingham', ' Manchester', ' Auckland']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

plain lens: [' Nairobi', ' pano', 'hatian', '}`).', '遥遥', '…]', ' biro', '布拉', '省会', ' scares', 'ẹo', 'otope', ' Büro', '...**', 'ถัด', 'više', '先到', '้ม', 'lima', ' сов', ' lions', ' ogs', 'auss', ' spoilers', 'located', 'urin', 'umed', ' nauk', ' correc', 'igans', ' gunmen', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass J-lens: [' Kenya', ' Johannesburg', ' Vienna', ' Prague', ' Dublin', ' London', ' Dubai', ' Denver', ' Tanzania', ' Bangkok', ' Cairo', ' Budapest', ' Canberra', ' Lagos', ' Ankara', ' Toronto', ' Melbourne', ' Bogotá', ' Brisbane', ' Uganda', ' Riyadh', ' Berlin', ' Kansas', ' Madrid', ' Munich', ' Chicago', ' Jakarta', ' Miami', ' Birmingham', ' Manchester', ' Lisbon', ' Auckland']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass plain24: [' pano', 'hatian', '}`).', '遥遥', '…]', ' biro', '布拉', '省会', ' scares', 'ẹo', 'otope', '先到', ' Büro', '...**', 'ถัด', 'više', '้ม', 'lima', ' сов', ' lions', ' ogs', ' spoilers', 'auss', 'located', 'urin', ' nauk', 'umed', 'igans', ' correc', ' gunmen', ').(', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass plain27: [' Kenya', '肯尼亚', 'airobi', 'Ken', '首都', ' wilde', '内', '镰', ' Kamp', ' safari', 'KE', '肯', ' keny', 'KAN', 'anyak', '首府', 'K', ' Най', ' capitals', '<K', ' Moi', ' capitale', ' Kis', 'lim', ' Ken', '\tK', ' Washing', 'aken', '的内', '_K', '贞', ' Voi']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass erased J-lens: ['.', ' London', '...', ' New', '.\\', ' Berlin', ':', ' San', ' Vienna', ' Manchester', ' Dublin', '?', ' Chicago', ' City', ' Birmingham', ' Kansas', ' Toronto', ' England', ' South', ' Dubai', '____', '**', ' Paris', ' Germany', ' Denver', ' Prague', '\\', ' Australia', '\xa0', ',', ' Melbourne', '.*']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass erased plain24: ['...', '____', '布拉', ' pano', 'PO', '遥遥', '}`).', '的首', 'also', '担', 'otope', 'hatian', ' сов', 'not', '先到', 'nam', ' scares', '省会', '__', 'located', ' NOT', ' lions', ' fictional', ' also', ' Büro', ' called', 'ถัด', ' biro', '\\n', '้ม', ' spoilers', ' politician']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Maasai Mara National Reserve is'

Baseline: ' Nairobi.\nHypothesis: The'

end-pass erased plain27: ['K', '...', '内', ' K', ' ', '首都', 'lim', '\xa0', '镰', 'U', ' Ker', '肯', '_K', 'M', 'KE', '凯', '-K', ' lim', ' capitals', '____', ' Dod', '(K', 'anyak', 'DK', '的内', ' Kil', 'W', '在内', '…', '.', ' Kus', ' Kamp']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

J-lens: [' horses', ' horse', ' Horse', 'horse', ' rabbits', ' Pony', ' goats', ' kittens', ' elephants', ' лоша', '小马', ' unicorn', ' wolves', ' sheep', ' deer', ' puppies', ' elephant', ' rabbit', '兔子', ' kitten', ' livestock', ' pony', ' pigs', ' Mustang', ' animals', ' wolf', ' Unicorn', ' puppy', '的马', ' lions', ' goat', '___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

plain lens: ['AWN', '..........', '小马', ' biro', '与方法', '.........', '骤', '尼西亚', '...', '工作站', '马拉', '的马', '問わず', '个字', '馬', '克难', ' gir', 'forth', 'shed', '套件', '在马', '�', ' trots', '........', 'hin', '肾炎', '麒', 'cape', 'zana', ' eit', ' nai', 'amel']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass J-lens: [' horses', ' horse', ' Horse', 'horse', ' rabbits', ' Pony', ' goats', ' kittens', ' elephants', ' лоша', '小马', ' unicorn', ' wolves', ' sheep', ' deer', ' puppies', ' elephant', ' rabbit', '兔子', ' kitten', ' livestock', ' pony', ' pigs', ' Mustang', ' animals', ' wolf', ' Unicorn', ' puppy', '的马', ' lions', ' goat', '___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass plain24: ['AWN', '..........', '小马', ' biro', '与方法', '.........', '骤', '尼西亚', '...', '工作站', '马拉', '的马', '問わず', '个字', '馬', '克难', ' gir', 'forth', 'shed', '套件', '在马', '�', ' trots', '........', 'hin', '肾炎', '麒', 'cape', 'zana', ' eit', ' nai', 'amel']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass plain27: [' horse', 'horse', '马', ' horses', '小马', '馬', '的马', ' Horse', ' лоша', '和马', '匹马', '在马', ' caballo', 'orses', ' equ', ' ngựa', ' kuda', 'ม้า', ' cavalry', '驹', ' Pferd', '上马', '赛马', 'Equ', ' Pony', ' pony', ' cavallo', ' pon', ' cheval', ' HOR', '匹', ' Pfer']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass erased J-lens: [' horses', ' horse', ' Horse', 'horse', ' rabbits', ' Pony', ' kittens', ' elephants', ' goats', ' лоша', '小马', ' wolves', ' unicorn', ' puppies', '兔子', ' kitten', ' sheep', ' deer', ' livestock', ' pigs', ' elephant', ' rabbit', ' Mustang', ' pony', ' Unicorn', ' wolf', '的马', ' animals', 'deer', ' caballo', ' lions', ' puppy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass erased plain24: ['AWN', ' biro', '..........', '小马', '尼西亚', '与方法', '問わず', '工作站', '马拉', '骤', '.........', '的马', '克难', ' trots', '个字', 'shed', '套件', 'forth', 'zana', '馬', 'ovem', '在马', '志愿服务队', ' nai', '麒', '肾炎', '经济学院', 'amel', 'wana', ' eit', 'hin', 'cape']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that neighs and is ridden using a saddle is'

Baseline: ' a colt.\nQuestion: What'

end-pass erased plain27: [' horse', 'horse', ' horses', '马', '小马', '馬', '的马', ' Horse', ' лоша', '和马', '匹马', '在马', ' caballo', 'orses', ' kuda', 'ม้า', ' ngựa', ' Pferd', '驹', '上马', ' cavalry', '赛马', ' equ', ' cavallo', 'Equ', ' Pony', ' Pfer', ' cheval', ' pony', ' HOR', '匹', '马可']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

J-lens: [' goats', ' cows', ' rabbits', ' sheep', ' puppies', ' pigs', ' baby', ' pups', ' Sheep', ' wolves', ' goat', ' livestock', ' puppy', ' cattle', ' babies', 'baby', '仔猪', ' rabbit', ' lamb', ' Baby', ' milk', ' Goat', ' newborn', ' dogs', ' mammals', ' mice', ' Puppy', ' chickens', ' called', ' bunny', ' wolf', ' Milk']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

plain lens: ['..........', ' called', ' laik', ' моло', '<<<<<<<', ' называется', 'AWN', '不绝', '😀', '叫我', '........', '...........', 'ovem', '异响', '叫什么', '叫', 'دة', '回声', '.........', 'shed', 'trasound', 'FAULT', '皱', ' ECONOM', '领头羊', 'called', '叫你', '\ufeff', '志愿服务队', ' Bethlehem', '文化广场', '\u200b\u200b']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass J-lens: [' goats', ' cows', ' rabbits', ' sheep', ' puppies', ' pigs', ' baby', ' pups', ' Sheep', ' wolves', ' goat', ' livestock', ' puppy', ' cattle', ' babies', 'baby', '仔猪', ' rabbit', ' lamb', ' Baby', ' milk', ' Goat', ' newborn', ' dogs', ' mammals', ' mice', ' Puppy', ' chickens', ' called', ' bunny', ' wolf', ' Milk']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass plain24: ['..........', ' called', ' laik', ' моло', '<<<<<<<', ' называется', 'AWN', '不绝', '😀', '叫我', '........', '...........', 'ovem', '异响', '叫什么', '叫', 'دة', '回声', '.........', 'shed', 'trasound', 'FAULT', '皱', ' ECONOM', '领头羊', 'called', '叫你', '\ufeff', '志愿服务队', ' Bethlehem', '文化广场', '\u200b\u200b']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass plain27: [' cow', ' calf', ' calves', ' milk', ' called', ' lamb', '牛', ' sheep', ' cows', '羊', '�', '羊羊', '牛的', ' Cow', '小牛', '奶牛', 'attle', '羔', 'Cow', '领头羊', '�', 'cow', ' молоко', ' cattle', '...', ' моло', 'called', 'iao', ' Dairy', 'born', ' dairy', ' lam']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass erased J-lens: [' goats', ' cows', ' rabbits', ' puppies', ' pigs', ' sheep', ' pups', ' Sheep', ' wolves', ' baby', ' livestock', ' goat', ' puppy', ' cattle', ' babies', '仔猪', 'baby', ' Goat', ' Puppy', ' mammals', ' rabbit', ' newborn', 'dogs', ' lamb', ' kittens', 'deer', ' dogs', ' chickens', '羔', ' Baby', ' mice', ' milk']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass erased plain24: ['..........', ' laik', ' моло', '<<<<<<<', ' called', '😀', ' называется', 'AWN', 'ovem', '不绝', '异响', '叫我', '...........', 'shed', 'FAULT', '叫什么', '........', 'دة', '领头羊', '回声', 'trasound', ' ECONOM', '志愿服务队', '.........', '🙂', '皱', '叫', '文化广场', ' Bethlehem', '叫你', ' biro', 'called']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal that moos is'

Baseline: ' a calf.\nQuestion: What is'

end-pass erased plain27: [' cow', ' calf', ' calves', ' milk', ' lamb', '牛', ' cows', ' sheep', '羊羊', '小牛', '�', ' called', '领头羊', '牛的', '羊', '奶牛', '羔', 'attle', ' молоко', 'Cow', 'cow', ' Cow', ' моло', '�', ' Dairy', 'called', ' cattle', 'iao', ' laine', 'born', ' laik', '�']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

J-lens: [' pigs', ' goats', ' pork', '仔猪', ' goat', ' chickens', ' livestock', ' Pork', ' rabbits', ' puppies', ' cattle', ' pig', ' Pig', ' baby', '猪', ' sheep', ' rabbit', ' barn', ' cows', ' puppy', '小猪', '生猪', ' kittens', ' Goat', ' Baby', ' Sheep', ' porc', ' pups', '养猪', ' Puppy', ' chicks', 'pig']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

plain lens: ['...', ':', '\ufeff', ' Rhodes', ' laik', '这个小', 'lay', '..........', 'دة', '…', '..', 'द्ध', ' breeds', '_', '__', '头上的', '........', ' genetically', ' скорее', 'shed', '\xa0', 'informatics', '.........', '孽', 'omencl', '出栏', '异响', '�', ' biro', '"', '................', ' pigs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass J-lens: [' pigs', ' goats', ' pork', '仔猪', ' goat', ' chickens', ' livestock', ' Pork', ' rabbits', ' puppies', ' cattle', ' pig', ' Pig', ' baby', '猪', ' sheep', ' rabbit', ' barn', ' cows', ' puppy', '小猪', '生猪', ' kittens', ' Goat', ' Baby', ' Sheep', ' porc', ' pups', '养猪', ' Puppy', ' chicks', 'pig']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass plain24: ['...', ':', '\ufeff', ' Rhodes', ' laik', '这个小', 'lay', '..........', 'دة', '…', '..', 'द्ध', ' breeds', '_', '__', '头上的', '........', ' genetically', ' скорее', 'shed', '\xa0', 'informatics', '.........', '孽', 'omencl', '出栏', '异响', '�', ' biro', '"', '................', ' pigs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass plain27: [' sheep', '...', ' lamb', '�', ' calves', ':', ' pig', '牛', ' cow', '羊', '羊羊', ' lam', '小牛', 'эм', '领头羊', ' ox', '…', '牛的', '_', ' cattle', 'attle', '�', '__', '克难', ' cows', ' steer', '那头', '/she', 'born', ' pigs', '羔', '这个小']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass erased J-lens: [' pigs', ' pork', ' goats', ' chickens', ' goat', ' rabbits', ' Pork', ' livestock', '仔猪', ' pig', ' Pig', '猪', ' puppies', ' baby', ' barn', ' rabbit', ' sheep', '小猪', ' cattle', '生猪', ' Baby', ' Sheep', ' puppy', ' bunny', ' kittens', ' cows', ' Goat', ' porc', '兔子', ' bacon', ' breeds', '养猪']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass erased plain24: ['...', ':', '\ufeff', ' Rhodes', ' laik', '这个小', '..', '…', 'lay', '_', '..........', 'دة', 'द्ध', '\xa0', '__', ' breeds', '........', '头上的', ' скорее', '"', ' genetically', 'informatics', '.........', " '", 'shed', ' "', 'omencl', '................', '孽', '�', '异响', '<<<<<<<']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal with a beard and curved horns is'

Baseline: ' calf.\nHypothesis: The'

end-pass erased plain27: ['...', ':', '_', '…', '-', ' sheep', ' "', '..', ' lamb', '__', '�', ' pig', '.', ';', '�', ' ', '\n', ' lam', '"', ' -', '\xa0', ' ox', '羊', '牛', '/', '(', '�', " '", 'эм', 'F', '____', ',']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

J-lens: [' sounds', '叫声', '叫', '叫做', ' louder', ' sounded', ' Sounds', ' noises', ' roar', ' loud', ' audible', '称为', '.wav', ' frogs', '.ogg', ' heard', ' crying', ' называется', ' noise', ' whisper', 'Sounds', ' vocal', ' noisy', 'noise', ' applause', ' scream', '.\\"', ' Noise', ' screams', '叫什么', 'sounds', ' sounding']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

plain lens: [' называется', '叫什么', '叫', '叫声', '叫她', ' sounded', '叫他', ' الآخر', '称为', ' Sounds', 'IKA', '惨叫', '的叫', ' sounds', '叫我', '异响', '叫做', 'mate', '呱', 'EEP', '称作', 'Sounds', ' warta', ' termed', '在水中', 'iphone', '悦耳', 'OUNDS', ' gunfire', '喵', 'chio', ' zove']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass J-lens: [' sounds', '叫声', '叫', '叫做', ' louder', ' sounded', ' Sounds', ' noises', ' roar', ' loud', ' audible', '称为', '.wav', ' frogs', '.ogg', ' heard', ' crying', ' называется', ' noise', ' whisper', 'Sounds', ' vocal', ' noisy', 'noise', ' applause', ' scream', '.\\"', ' Noise', ' screams', '叫什么', 'sounds', ' sounding']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass plain24: [' называется', '叫什么', '叫', '叫声', '叫她', ' sounded', '叫他', ' الآخر', '称为', ' Sounds', 'IKA', '惨叫', '的叫', ' sounds', '叫我', '异响', '叫做', 'mate', '呱', 'EEP', '称作', 'Sounds', ' warta', ' termed', '在水中', 'iphone', '悦耳', 'OUNDS', ' gunfire', '喵', 'chio', ' zove']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass plain27: ['称为', '喵', ' называется', '叫', '叫声', '咯咯', '叫什么', ' neigh', ' ducks', '鸭子', '呱', '鸣', ' chir', '呱呱', 'tweet', '叽叽', '叫做', 'Tweet', ' termed', '稱為', ' Ducks', '咕噜', '鳴', '嘎', '鸟语', '咕', '�', ' llamado', ' gọi', ' называют', 'duck', 'ước']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass erased J-lens: [' sounds', '叫声', '叫', ' louder', ' sounded', ' Sounds', '叫做', ' noises', ' roar', '.ogg', ' audible', '.wav', ' frogs', '称为', ' loud', ' называется', ' crying', 'Sounds', '.\\"', ' heard', 'noise', ' screams', ' applause', 'sounds', '叫什么', ' scream', ' whisper', ' noisy', ' Noise', ' grunt', '的叫', ' vocal']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass erased plain24: [' называется', '叫什么', '叫声', '叫她', '叫', ' sounded', '叫他', ' الآخر', '称为', 'IKA', '惨叫', ' Sounds', '的叫', ' warta', '异响', 'EEP', '叫我', '呱', '叫做', 'mate', ' sounds', 'Sounds', '称作', 'OUNDS', ' zove', 'vog', 'iphone', ' termed', ' gunfire', '悦耳', '在水中', 'chio']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the pond bird whose male is called a drake is'

Baseline: ' a quack.\nQuestion: What'

end-pass erased plain27: ['喵', ' называется', '称为', '叫声', '叫', '咯咯', ' neigh', '叫什么', ' ducks', '鸭子', '呱', '呱呱', '鸣', 'tweet', '叽叽', '稱為', '鳴', '鸟语', ' chir', 'Tweet', ' Ducks', '叫做', '咕噜', ' termed', '咕', '嘎', ' llamado', ' llamada', '�', 'ước', 'เรียกว่า', 'duck']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

J-lens: [' kittens', ' kitten', ' babies', ' baby', 'baby', ' puppies', ' pups', ' cats', ' puppy', ' Babies', ' Baby', 'Baby', ' gato', '小猫', ' kitty', '喵', ' newborn', '-cat', ' Puppy', ' bunny', ' Cats', ' gatos', '猫', ' called', ' paw', 'cats', ' fetus', ' toddler', '猫咪', ' cute', ' cat', '崽']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

plain lens: ['...', ' called', '<<<<<<<', '..........', '.........', ' называется', '…', '...........', ' kittens', '萌', ' commonly', 'called', '回声', 'ようだ', '........', '喵', '怀抱', '团团', 'Hibernate', '叫什么', '叫', '诞生', ' territorial', 'द्ध', ' eit', '分别为', '叫我', '喵喵', 'ັ', '轻声', 'τρό', '依次为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass J-lens: [' babies', ' baby', 'baby', ' puppies', ' pups', ' cats', ' puppy', ' Babies', ' Baby', 'Baby', '小猫', ' gato', '喵', ' kitty', ' newborn', '-cat', ' Puppy', ' bunny', ' Cats', ' gatos', '猫', ' called', ' paw', 'cats', ' fetus', ' toddler', '猫咪', ' cute', ' cat', '崽', '叫', ' babe']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass plain24: ['...', ' called', '<<<<<<<', '..........', '.........', ' называется', '…', '...........', '萌', 'called', ' commonly', '回声', 'ようだ', '........', '喵', '怀抱', '团团', 'Hibernate', '叫什么', ' territorial', '诞生', '叫', 'द्ध', ' eit', '叫我', '分别为', '喵喵', '轻声', 'ັ', '依次为', 'τρό', ' litter']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass plain27: [' baby', ' called', ' kits', '...', '幼', 'baby', 'called', '仔', 'Baby', ' litter', ' infancy', 'born', ' Baby', ' cub', '宝宝', '小猫', ' infant', ':', ' puppy', '…', ' hatch', '-kit', ' born', ' называется', '.........', ' fuzz', ' Kits', '之宝', ' fo', '__', '叫什么', ' newborn']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass erased J-lens: [' called', ' baby', '叫', ' babies', '“', ' Baby', '____', '.', '__', '称为', 'baby', '___', '________', ' pups', '叫做', '...', '?', '"', 'called', 'Baby', ' newborn', ' Babies', ' cute', ' offspring', ' bab', 'bab', ' paw', '叫什么', '叫声', ' belly', '."', '\\"']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass erased plain24: ['...', ' called', '…', ':', '"', '<<<<<<<', '.........', ' ...', ' commonly', '..........', '叫', ' называется', 'called', '...........', '........', '叫什么', ' "', '\xa0', '怀抱', '……', '萌', '..', '分别为', '诞生', 'द्ध', ' territorial', 'ようだ', '__', '回声', '团团', '轻声', '................']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the domestic animal that purrs is'

Baseline: ' kitten.\nHypothesis: The'

end-pass erased plain27: ['...', ':', ' called', ' "', '…', '"', ' baby', 'called', ' a', ' ', ' ...', '\xa0', '.', '仔', ' kits', ' litter', '幼', ' f', '“', '(', '__', ',', '-', ' m', '\n', 'born', ' c', '……', '叫', ' cub', '[', ' fo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

J-lens: ['.\\', ' typically', '.\\"', '...\\', '?\\', '___', ').\\', '__.', '____', '(number', ' five', ' four', ' seven', ' usually', ' fewer', '__', ' fourteen', '。\\', ' twelve', ' equal', ' numbered', '\\"', ' counted', '_.', ' six', '-number', ' twenty', ' three', ' eight', ' thirteen', ' fours', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

plain lens: ['通常为', ' typically', 'typically', ':number', '一数', '(number', '总数', '{}".', 'usually', ' usually', 'に行ってきました', '一般为', '_number', '沟村', '砰砰', '*>::', '通常情况下', '庄镇', '.numberOf', '.trailing', 'gues', 'omers', ' commonly', 'shed', ' Typically', '頂けます', ' 주장했다', 'عدد', '与我们联系', 'numberOf', '[number', 'いただけます']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass J-lens: ['.\\', ' typically', '.\\"', '...\\', '?\\', '___', ').\\', '__.', '____', '(number', ' five', ' four', ' seven', ' usually', ' fewer', '__', ' fourteen', '。\\', ' twelve', ' equal', ' numbered', '\\"', ' counted', '_.', ' six', '-number', ' twenty', ' three', ' eight', ' thirteen', ' fours', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain24: ['通常为', ' typically', 'typically', ':number', '一数', '(number', '总数', '{}".', 'usually', ' usually', 'に行ってきました', '一般为', '_number', '沟村', '砰砰', '*>::', '通常情况下', '庄镇', '.numberOf', '.trailing', 'gues', 'omers', ' commonly', 'shed', ' Typically', '頂けます', ' 주장했다', 'عدد', '与我们联系', 'numberOf', '[number', 'いただけます']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain27: [' typically', ' usually', 'typically', '通常为', 'usually', ' odd', '偶', '奇', ' greater', 'odd', '通常情况下', '多いです', ' exactly', ' commonly', ' Typically', 'always', ' always', '一般为', 'parity', '_odd', ' fewer', ' impar', 'عدد', ' sometimes', ' generally', 'greater', '通常是', ' ordinarily', '庄镇', 'normally', ' normally', ' traditionally']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased J-lens: ['.\\"', '.\\', ' typically', '...\\', ').\\', '?\\', '__.', '(number', '___', ' fourteen', ' five', ' seven', '。\\', ' fewer', '____', ' twelve', ' four', '-number', ' ALWAYS', ' fours', ' usually', ' numbered', ' thirteen', ' counted', ':number', '_.', ' equal', ' twenty', '.").', '通常为', '\\"\\', '__']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased plain24: ['通常为', ' typically', 'typically', ':number', '总数', '(number', ' usually', 'usually', '一数', '{}".', '一般为', '_number', 'に行ってきました', '砰砰', '通常情况下', ' commonly', '*>::', '沟村', '.numberOf', ' Typically', 'omers', '.trailing', '庄镇', 'shed', 'gues', ' exactly', 'عدد', 'numberOf', '与我们联系', 'いただけます', '[number', ' ordinarily']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the farm animal that clucks and lays eggs is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased plain27: [' typically', 'typically', ' usually', '通常为', 'usually', ' odd', '偶', '多いです', '奇', '通常情况下', 'odd', ' greater', ' commonly', ' Typically', ' exactly', 'always', '一般为', 'parity', ' always', '_odd', ' fewer', ' impar', 'عدد', '庄镇', '沟村', ' ordinarily', 'greater', ' sometimes', '通常是', 'normally', 'LOTS', ' generally']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

J-lens: [' unknown', ' zero', ' undefined', ' infinite', ' equal', ' unspecified', ' irrelevant', ' nonexistent', 'unknown', ' Unknown', ' unclear', ' unlimited', ' impossible', ' none', ' exactly', ' ZERO', ' infinity', 'zero', ' equals', ' Zero', ' identical', '未知', ' Undefined', ' never', ' unknow', 'undefined', 'Undefined', ' uncertain', '.unknown', ' ambiguous', '.undefined', 'equal']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

plain lens: ['{}".', ' indetermin', '数是', '数为', ' hereby', '(number', '总数', 'unknown', '頂けます', ' unknown', ' irrelevant', ' exactly', '一数', 'achsen', '卫生组织', 'gues', '无限的', ' nulla', ':number', 'UNKNOWN', '_number', '*>::', 'عدد', '砰砰', '数不清', '.trailing', '式设计', 'više', '.number', 'ächt', ' moot', '确定为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass J-lens: [' unknown', ' zero', ' undefined', ' infinite', ' equal', ' unspecified', ' irrelevant', ' nonexistent', 'unknown', ' Unknown', ' unclear', ' unlimited', ' impossible', ' none', ' exactly', ' ZERO', ' infinity', 'zero', ' equals', ' Zero', ' identical', '未知', ' Undefined', ' never', ' unknow', 'undefined', 'Undefined', ' uncertain', '.unknown', ' ambiguous', '.undefined', 'equal']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass plain24: ['{}".', ' indetermin', '数是', '数为', ' hereby', '(number', '总数', 'unknown', '頂けます', ' unknown', ' irrelevant', ' exactly', '一数', 'achsen', '卫生组织', 'gues', '无限的', ' nulla', ':number', 'UNKNOWN', '_number', '*>::', 'عدد', '砰砰', '数不清', '.trailing', '式设计', 'više', '.number', 'ächt', ' moot', '确定为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass plain27: [' zero', 'zero', ' ZERO', '无限的', ' infinity', ' unlimited', ' infinite', 'Zero', '-zero', ' exactly', ' undefined', ' Zero', '無限', 'undefined', ' limitless', ' indefinitely', ' unknown', '.zero', 'ZERO', ' zeroes', ' unclear', 'unknown', ' cero', '为零', 'ゼロ', ' indetermin', '零', '永远不会', '无穷的', ' infinitely', '无限', '_ZERO']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass erased J-lens: [' unknown', ' nonexistent', ' undefined', ' unspecified', ' infinite', 'unknown', ' zero', ' irrelevant', ' Unknown', ' equal', ' unclear', ' unlimited', ' ZERO', ' impossible', ' none', ' Undefined', ' infinity', '.undefined', '.unknown', 'zero', ' unknow', ' exactly', 'Undefined', '未知', ' UNKNOWN', ' unnamed', 'undefined', ' equals', ' Zero', ' unbek', 'equal', ' identical']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass erased plain24: [' indetermin', '数是', '{}".', '数为', ' hereby', '(number', ' exactly', '总数', ' unknown', 'unknown', ' irrelevant', '一数', 'achsen', '頂けます', '无限的', '_number', ' nulla', 'gues', '卫生组织', 'UNKNOWN', 'عدد', '.number', '数', ':number', '确定为', ' unclear', ' numero', ' moot', '*>::', '数不清', '永远不会', 'otope']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of arms on the species of Paul, the famous 2010 World Cup predictor, is'

Baseline: ' 0.\nHypothesis:'

end-pass erased plain27: [' zero', 'zero', ' ZERO', '无限的', ' unlimited', ' infinity', ' infinite', 'Zero', '-zero', ' undefined', ' Zero', ' exactly', '無限', 'undefined', ' limitless', ' indefinitely', ' unknown', '.zero', 'ZERO', ' zeroes', ' unclear', 'unknown', ' cero', 'ゼロ', '为零', '无穷的', '零', '永远不会', ' indetermin', ' infinitely', '无限', '_ZERO']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

J-lens: [' unknown', ' unspecified', ' unclear', ' exactly', ' ambiguous', ' infinite', 'unknown', ' seven', ' four', ' counted', ' undefined', ' three', ' five', ' nonexistent', '.\\', ' Unknown', ' typically', '?\\', ' missing', ' eight', ' count', ' uncertain', ' six', ' varies', ' equal', ' impossible', ' incorrect', 'ambiguous', ' unlimited', '(number', ' always', ' nine']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

plain lens: ['数为', '总数', '{}".', '数是', '一数', '(number', ' exactly', 'NumberOf', '.trailing', '_number', '通常为', ' typically', ' hereby', ' impar', '數', '总数的', 'lets', '_docs', '这个数字', '頂けます', '团团', '.numberOf', ' numero', 'omers', '的数量', '数', 'いただけます', ' NumberOf', 'gues', '传来了', 'numberOf', 'lobby']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass J-lens: [' unknown', ' unspecified', ' unclear', ' exactly', ' ambiguous', ' infinite', 'unknown', ' seven', ' four', ' counted', ' undefined', ' three', ' five', ' nonexistent', '.\\', ' Unknown', ' typically', '?\\', ' missing', ' eight', ' count', ' uncertain', ' six', ' varies', ' equal', ' impossible', ' incorrect', 'ambiguous', ' unlimited', '(number', ' always', ' nine']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass plain24: ['数为', '总数', '{}".', '数是', '一数', '(number', ' exactly', 'NumberOf', '.trailing', '_number', '通常为', ' typically', ' hereby', ' impar', '數', '总数的', 'lets', '_docs', '这个数字', '頂けます', '团团', '.numberOf', ' numero', 'omers', '的数量', '数', 'いただけます', ' NumberOf', 'gues', '传来了', 'numberOf', 'lobby']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass plain27: [' exactly', ' infinite', ' infinity', ' ZERO', ' zero', '无限的', ' typically', ' unlimited', 'NumberOf', ' not', '数为', 'zero', '通常为', '.trailing', ' unclear', '永远不会', ' traditionally', '(number', ' indefinitely', ' always', ' impar', 'veys', 'finite', '無限', ' odd', ' Infinite', ' ambiguous', '方も多い', ' finite', ' จำกัด', '{}".', '__).']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass erased J-lens: [' unknown', ' unspecified', ' unclear', ' ambiguous', ' infinite', ' exactly', 'unknown', ' nonexistent', ' counted', ' seven', '?\\', ' Unknown', ' undefined', ' four', ' five', '.\\"', '.\\', 'ambiguous', ' typically', ' three', ' uncertain', ' incorrect', ' eight', ' missing', '(number', ' unlimited', ' thirteen', ' ALWAYS', ').\\', ' TWO', ' impossible', ' varies']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass erased plain24: ['数为', '总数', '{}".', '数是', '一数', '(number', ' exactly', 'NumberOf', '.trailing', '_number', ' typically', '通常为', ' hereby', '數', ' impar', 'lets', '_docs', '总数的', '这个数字', '数', ' numero', '团团', '的数量', '.numberOf', 'omers', '頂けます', ' indetermin', 'いただけます', '永远不会', '数目', 'numberOf', ' NumberOf']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of wings on the bird depicted as Tux, the Linux mascot, is'

Baseline: ' 2.\nQuestion: How many'

end-pass erased plain27: [' exactly', ' infinite', ' infinity', ' ZERO', '无限的', ' zero', 'NumberOf', ' unlimited', ' typically', '.trailing', '数为', '通常为', 'zero', ' unclear', '永远不会', ' not', ' traditionally', '無限', ' impar', ' indefinitely', '(number', 'veys', '方も多い', 'finite', ' จำกัด', '__).', '{}".', ' always', ' Infinite', '很好奇', ' unspecified', ' odd']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [J-lens](readout.json)     | 3/16                   |    0.756 | 1/11                     | 3/16             |          0 |
| [plain lens](readout.json) | 0/16                   |    0.699 | 0/11                     | 0/16             |          0 |

### End-of-pass readout (not for earlier edits)

| method                                  | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:----------------------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [end-pass erased J-lens](readout.json)  | 7/16                   |    0.806 | 5/11                     | 7/16             |          0 |
| [end-pass J-lens](readout.json)         | 6/16                   |    0.825 | 4/11                     | 11/16            |          0 |
| [end-pass plain27](readout.json)        | 5/16                   |    0.833 | 4/11                     | 7/16             |          0 |
| [end-pass erased plain27](readout.json) | 3/16                   |    0.824 | 2/11                     | 4/16             |          0 |
| [end-pass plain24](readout.json)        | 1/16                   |    0.796 | 1/11                     | 1/16             |          0 |
| [end-pass erased plain24](readout.json) | 0/16                   |    0.783 | 0/11                     | 0/16             |          0 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_121804_jlens-one-pass/run.md
