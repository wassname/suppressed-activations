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
k: 32
elapsed_seconds: 26.19
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: Sixteen new probes fixed before their first run: eight geography and eight animals, with no concept repeated from v1. Same factual prefix and no trailing space. Freeze J at residual24, plain controls at24/27, final position, k32, prompt mask and greedy-next-token word mask (max_n1). Layer24 was selected in earlier development; mask1 was selected after comparing caps20 and1 on v1. No model-output filtering or retries. Labels are plausible intermediates, not proof the model computes them. Report every case and the expected-answer subset separately. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method           | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:-----------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| Spain     | J-lens           | False         |           0.730303 |            62 |                      2 | False          | False        |
| Spain     | plain lens       | False         |           0.627879 |         32546 |                    382 | False          | False        |
| Spain     | end-pass J-lens  | False         |           0.833333 |            59 |                      1 | False          | False        |
| Spain     | end-pass plain24 | False         |           0.722424 |         32543 |                    382 | False          | False        |
| Spain     | end-pass plain27 | False         |           0.892121 |           657 |                     40 | False          | False        |
| Portugal  | J-lens           | False         |           0.858852 |             1 |                      0 | False          | False        |
| Portugal  | plain lens       | False         |           0.748804 |          1349 |                      0 | False          | False        |
| Portugal  | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | False        |
| Portugal  | end-pass plain24 | False         |           0.978469 |          1345 |             1000000000 | False          | False        |
| Portugal  | end-pass plain27 | False         |           0.976077 |           385 |             1000000000 | False          | False        |
| Germany   | J-lens           | False         |           0.808571 |             2 |                      0 | False          | False        |
| Germany   | plain lens       | False         |           0.791429 |           440 |                      7 | False          | False        |
| Germany   | end-pass J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| Germany   | end-pass plain24 | False         |           0.991429 |           437 |             1000000000 | False          | False        |
| Germany   | end-pass plain27 | True          |           1        |            16 |             1000000000 | True           | True         |
| Greece    | J-lens           | False         |           0.853333 |             5 |                      0 | False          | False        |
| Greece    | plain lens       | False         |           0.803333 |            21 |                     17 | False          | False        |
| Greece    | end-pass J-lens  | True          |           1        |             4 |             1000000000 | True           | True         |
| Greece    | end-pass plain24 | True          |           0.99     |            20 |             1000000000 | True           | True         |
| Greece    | end-pass plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| Austria   | J-lens           | False         |           0.871212 |             4 |                      0 | False          | False        |
| Austria   | plain lens       | False         |           0.738636 |           366 |                     17 | False          | False        |
| Austria   | end-pass J-lens  | True          |           1        |             3 |             1000000000 | True           | True         |
| Austria   | end-pass plain24 | False         |           0.939394 |           364 |             1000000000 | False          | False        |
| Austria   | end-pass plain27 | True          |           1        |             7 |             1000000000 | True           | False        |
| Norway    | J-lens           | False         |           0.885621 |             3 |                      0 | False          | False        |
| Norway    | plain lens       | False         |           0.888889 |            78 |                      7 | False          | False        |
| Norway    | end-pass J-lens  | True          |           1        |             2 |             1000000000 | True           | True         |
| Norway    | end-pass plain24 | False         |           1        |            77 |             1000000000 | False          | False        |
| Norway    | end-pass plain27 | True          |           1        |             1 |             1000000000 | True           | True         |
| Thailand  | J-lens           | False         |           0.909091 |             4 |                      0 | False          | False        |
| Thailand  | plain lens       | False         |           0.909091 |          2215 |                     88 | False          | False        |
| Thailand  | end-pass J-lens  | True          |           0.970455 |             3 |             1000000000 | True           | True         |
| Thailand  | end-pass plain24 | False         |           0.943182 |          2214 |             1000000000 | False          | False        |
| Thailand  | end-pass plain27 | False         |           0.998864 |           489 |             1000000000 | False          | False        |
| Kenya     | J-lens           | False         |           0.920635 |             1 |                      0 | False          | False        |
| Kenya     | plain lens       | False         |           0.904762 |            40 |                      0 | False          | False        |
| Kenya     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| Kenya     | end-pass plain24 | False         |           1        |            39 |             1000000000 | False          | False        |
| Kenya     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| horse     | J-lens           | True          |           0.929338 |             1 |             1000000000 |                |              |
| horse     | plain lens       | False         |           0.731664 |            37 |             1000000000 |                |              |
| horse     | end-pass J-lens  | True          |           0.929338 |             1 |             1000000000 |                |              |
| horse     | end-pass plain24 | False         |           0.731664 |            37 |             1000000000 |                |              |
| horse     | end-pass plain27 | True          |           0.968694 |             0 |             1000000000 |                |              |
| cow       | J-lens           | True          |           0.816667 |            41 |                     77 | False          | True         |
| cow       | plain lens       | False         |           0.412667 |         24092 |                   3937 | False          | False        |
| cow       | end-pass J-lens  | True          |           0.838    |            41 |                     77 | False          | True         |
| cow       | end-pass plain24 | False         |           0.474    |         24090 |                   3937 | False          | False        |
| cow       | end-pass plain27 | False         |           0.636    |             0 |                      1 | False          | False        |
| goat      | J-lens           | True          |           0.977273 |             3 |                     55 | True           | True         |
| goat      | plain lens       | False         |           0.795455 |          9977 |                   5403 | False          | False        |
| goat      | end-pass J-lens  | True          |           1        |             3 |                     54 | True           | True         |
| goat      | end-pass plain24 | False         |           0.943182 |          9977 |                   5403 | False          | False        |
| goat      | end-pass plain27 | False         |           0.943182 |            32 |                   1224 | False          | False        |
| duck      | J-lens           | False         |           0.808271 |            38 |                   2513 | False          | False        |
| duck      | plain lens       | False         |           0.830827 |           146 |                   1065 | False          | False        |
| duck      | end-pass J-lens  | False         |           0.808271 |            38 |                   2513 | False          | False        |
| duck      | end-pass plain24 | False         |           0.830827 |           146 |                   1065 | False          | False        |
| duck      | end-pass plain27 | True          |           0.800752 |            29 |                    381 | True           | True         |
| cat       | J-lens           | False         |           0.892754 |            30 |                      1 | False          | False        |
| cat       | plain lens       | False         |           0.765217 |         12091 |                    178 | False          | False        |
| cat       | end-pass J-lens  | True          |           1        |            28 |             1000000000 | True           | True         |
| cat       | end-pass plain24 | False         |           1        |         12082 |             1000000000 | False          | False        |
| cat       | end-pass plain27 | False         |           1        |           293 |             1000000000 | False          | False        |
| chicken   | J-lens           | False         |           0.488415 |           614 |                    797 | False          | False        |
| chicken   | plain lens       | False         |           0.42561  |         40921 |                 230691 | False          | False        |
| chicken   | end-pass J-lens  | False         |           0.488415 |           614 |                    797 | False          | False        |
| chicken   | end-pass plain24 | False         |           0.42561  |         40921 |                 230690 | False          | False        |
| chicken   | end-pass plain27 | False         |           0.540244 |          3408 |                 173850 | False          | False        |
| octopus   | J-lens           | False         |           0.114286 |          3933 |                  14621 | False          | False        |
| octopus   | plain lens       | False         |           0.457143 |         89133 |                 246314 | False          | False        |
| octopus   | end-pass J-lens  | False         |           0.114286 |          3932 |                  14620 | False          | False        |
| octopus   | end-pass plain24 | False         |           0.457143 |         89133 |                 246313 | False          | False        |
| octopus   | end-pass plain27 | False         |           0.428571 |        110300 |                 245847 | False          | False        |
| penguin   | J-lens           | False         |           0.497186 |          7170 |                   2905 | False          | False        |
| penguin   | plain lens       | False         |           0.531895 |           645 |                 149141 | False          | False        |
| penguin   | end-pass J-lens  | False         |           0.497186 |          7169 |                   2905 | False          | False        |
| penguin   | end-pass plain24 | False         |           0.531895 |           645 |                 149141 | False          | False        |
| penguin   | end-pass plain27 | False         |           0.413696 |          2035 |                 143813 | False          | False        |

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


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [J-lens](readout.json)     | 3/16                   |    0.762 | 1/11                     | 3/16             |          0 |
| [plain lens](readout.json) | 0/16                   |    0.705 | 0/11                     | 0/16             |          0 |

### End-of-pass readout (not for earlier edits)

| method                           | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [end-pass J-lens](readout.json)  | 10/16                  |    0.833 | 8/11                     | 11/16            |          0 |
| [end-pass plain27](readout.json) | 6/16                   |    0.842 | 5/11                     | 7/16             |          0 |
| [end-pass plain24](readout.json) | 1/16                   |    0.804 | 1/11                     | 1/16             |          0 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_110305_jlens-one-pass/run.md
