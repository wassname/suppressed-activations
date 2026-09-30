---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: out/2026-09-30_090645_jlens-one-pass/forecast.pt
cases_json: data/english_hidden_words_v1.json
k: 32
elapsed_seconds: 37.38
---
# Offline output forecast and same-layer contrast

Written by PI/OpenAI.

Fit32 generic WikiText records, validate4; no task/language labels. Fit RMS-normalised source/final residual pairs by ridge regression toward the identity map (ridge=0.01*mean Gram diagonal), with an intercept. Current-input readout receives residual24 only. Score=max(p_J-p_forecast,0), excluding zero scores; compare J-minus-plain to isolate the fitted forecast's contribution. Same layer, final position, k32 and prompt mask as before. Selection: Sixteen new English probes fixed before their first model run: eight geography and eight animal questions. No output-based filtering or prompt retries. Raw J-lens and forecast contrast are frozen at residual24, final position, k32. The few-shot prefix and absence of trailing space follow the reference multi-hop example; this differs from the earlier development prompts. Labels describe a plausible intermediate, not proof that the model must compute it. All rows must be reported, including wrong answers. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: forecast beats plain held-out argmax agreement and KL; J-minus-forecast improves joint readout over both J and J-minus-plain. If oracle contrast also fails, output forecast error alone cannot explain that failure.

Calibration: {'fit_tokens': 4096, 'validation_tokens': 512, 'ridge_fraction': 0.01, 'plain_argmax_agreement_all_positions': 0.0703125, 'plain_argmax_agreement_final_positions': 0.0, 'plain_kl_nats_per_position': 8.13240110874176, 'plain_residual_mse': 1.3224719762802124, 'forecast_argmax_agreement_all_positions': 0.4609375, 'forecast_argmax_agreement_final_positions': 0.5, 'forecast_kl_nats_per_position': 1.6240774765610695, 'forecast_residual_mse': 0.5578553080558777}

| concept   | method                                      | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:--------------------------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| Paris     | J-lens                                      | False         |          0.848005  |            12 |                      0 | False          | False        |
| Paris     | plain lens                                  | False         |          0.75939   |          1225 |                      8 | False          | False        |
| Paris     | forecast                                    | False         |          0.828052  |            65 |                      0 | False          | False        |
| Paris     | final-layer oracle (not deployable)         | False         |          0.757629  |            19 |                      0 | False          | False        |
| Paris     | J minus plain lens                          | False         |          0.485916  |    1000000000 |                      0 | False          | False        |
| Paris     | J minus forecast                            | False         |          0.51115   |            19 |                      0 | False          | False        |
| Paris     | J minus final-layer oracle (not deployable) | False         |          0.558685  |            22 |                      0 | False          | False        |
| China     | J-lens                                      | False         |          0.919758  |             3 |                      0 | False          | False        |
| China     | plain lens                                  | False         |          0.887403  |            37 |                      6 | False          | False        |
| China     | forecast                                    | False         |          0.767903  |           178 |                      5 | False          | False        |
| China     | final-layer oracle (not deployable)         | False         |          0.844694  |             1 |                      0 | False          | False        |
| China     | J minus plain lens                          | False         |          0.569456  |             3 |                      0 | False          | False        |
| China     | J minus forecast                            | False         |          0.776532  |             2 |                      0 | False          | False        |
| China     | J minus final-layer oracle (not deployable) | False         |          0.735979  |            26 |                      0 | False          | False        |
| Egypt     | J-lens                                      | False         |          0.913979  |             1 |                      0 | False          | False        |
| Egypt     | plain lens                                  | False         |          0.938172  |            70 |                     98 | False          | False        |
| Egypt     | forecast                                    | False         |          0.846774  |            11 |                     30 | False          | False        |
| Egypt     | final-layer oracle (not deployable)         | False         |          0.924731  |             1 |                      0 | False          | False        |
| Egypt     | J minus plain lens                          | False         |          0.737903  |             1 |                      0 | False          | False        |
| Egypt     | J minus forecast                            | False         |          0.80914   |             1 |                      0 | False          | False        |
| Egypt     | J minus final-layer oracle (not deployable) | True          |          0.798387  |             1 |             1000000000 | True           | True         |
| India     | J-lens                                      | False         |          0.764706  |            17 |                    516 | True           | False        |
| India     | plain lens                                  | False         |          0.585621  |          6339 |                   9987 | False          | False        |
| India     | forecast                                    | False         |          0.537255  |            92 |                      8 | False          | False        |
| India     | final-layer oracle (not deployable)         | False         |          0.685621  |             2 |                      0 | False          | False        |
| India     | J minus plain lens                          | False         |          0.562092  |            17 |                    445 | True           | False        |
| India     | J minus forecast                            | False         |          0.696078  |            19 |                   2060 | True           | False        |
| India     | J minus final-layer oracle (not deployable) | False         |          0.543791  |            74 |             1000000000 | False          | False        |
| Canada    | J-lens                                      | False         |          0.906667  |             1 |                      2 | False          | False        |
| Canada    | plain lens                                  | True          |          0.900667  |             2 |                    384 | True           | True         |
| Canada    | forecast                                    | False         |          0.766667  |             6 |                     10 | False          | False        |
| Canada    | final-layer oracle (not deployable)         | False         |          0.821333  |             1 |                      0 | False          | False        |
| Canada    | J minus plain lens                          | False         |          0.622     |             1 |                      2 | False          | False        |
| Canada    | J minus forecast                            | False         |          0.687333  |             1 |                      2 | False          | False        |
| Canada    | J minus final-layer oracle (not deployable) | True          |          0.733333  |             1 |             1000000000 | True           | True         |
| Australia | J-lens                                      | False         |          0.912698  |             9 |                      1 | False          | False        |
| Australia | plain lens                                  | False         |          0.795518  |          2311 |                    132 | False          | False        |
| Australia | forecast                                    | False         |          0.777311  |           111 |                    298 | False          | False        |
| Australia | final-layer oracle (not deployable)         | False         |          0.856676  |             3 |                      0 | False          | False        |
| Australia | J minus plain lens                          | False         |          0.636788  |            10 |                      1 | False          | False        |
| Australia | J minus forecast                            | False         |          0.778245  |             9 |                      1 | False          | False        |
| Australia | J minus final-layer oracle (not deployable) | False         |          0.593371  |           102 |             1000000000 | False          | False        |
| Brazil    | J-lens                                      | True          |          0.858974  |            10 |                      1 | False          | False        |
| Brazil    | plain lens                                  | False         |          0.794872  |          1857 |                    682 | False          | False        |
| Brazil    | forecast                                    | False         |          0.807692  |            62 |                    232 | False          | False        |
| Brazil    | final-layer oracle (not deployable)         | False         |          0.833333  |             1 |                      0 | False          | False        |
| Brazil    | J minus plain lens                          | True          |          0.74359   |            10 |                      1 | False          | False        |
| Brazil    | J minus forecast                            | True          |          0.871795  |            10 |                      1 | False          | False        |
| Brazil    | J minus final-layer oracle (not deployable) | False         |          0.487179  |           216 |             1000000000 | False          | False        |
| Argentina | J-lens                                      | False         |          0.819608  |            90 |                     47 | False          | False        |
| Argentina | plain lens                                  | False         |          0.693137  |         43725 |                  13578 | False          | False        |
| Argentina | forecast                                    | False         |          0.737255  |          1222 |                    298 | False          | False        |
| Argentina | final-layer oracle (not deployable)         | False         |          0.817157  |           109 |                     58 | False          | False        |
| Argentina | J minus plain lens                          | False         |          0.611275  |            89 |                     48 | False          | False        |
| Argentina | J minus forecast                            | False         |          0.747059  |            83 |                     42 | False          | False        |
| Argentina | J minus final-layer oracle (not deployable) | False         |          0.733333  |           615 |                  87722 | False          | False        |
| sheep     | J-lens                                      | False         |          0.842857  |             0 |                      7 | False          | False        |
| sheep     | plain lens                                  | True          |          0.9       |            29 |                     50 | True           | True         |
| sheep     | forecast                                    | False         |          0.842857  |             4 |                     30 | False          | False        |
| sheep     | final-layer oracle (not deployable)         | False         |          0.792857  |             2 |                      0 | False          | False        |
| sheep     | J minus plain lens                          | False         |          0.589286  |             0 |                      7 | False          | False        |
| sheep     | J minus forecast                            | False         |          0.664286  |             0 |                      7 | False          | False        |
| sheep     | J minus final-layer oracle (not deployable) | True          |          0.775     |             0 |             1000000000 | True           | True         |
| zebra     | J-lens                                      | False         |          0.195122  |        109314 |                    239 | False          | False        |
| zebra     | plain lens                                  | False         |          0.0731707 |        236652 |                 189779 | False          | False        |
| zebra     | forecast                                    | False         |          0.121951  |        127854 |                    122 | False          | False        |
| zebra     | final-layer oracle (not deployable)         | False         |          0.146341  |         53652 |                    610 | False          | False        |
| zebra     | J minus plain lens                          | False         |          0.585366  |         20295 |                    211 | False          | False        |
| zebra     | J minus forecast                            | False         |          0.390244  |        103851 |                    292 | False          | False        |
| zebra     | J minus final-layer oracle (not deployable) | False         |          0.317073  |        108258 |                    233 | False          | False        |
| elephant  | J-lens                                      | True          |          0.915385  |             1 |                    166 | True           | True         |
| elephant  | plain lens                                  | False         |          0.930769  |           300 |                   6077 | False          | False        |
| elephant  | forecast                                    | False         |          0.423077  |            94 |                   9381 | False          | False        |
| elephant  | final-layer oracle (not deployable)         | False         |          0.715385  |             5 |                      9 | False          | False        |
| elephant  | J minus plain lens                          | True          |          0.638462  |             1 |                    164 | True           | True         |
| elephant  | J minus forecast                            | True          |          0.896154  |             1 |                    156 | True           | True         |
| elephant  | J minus final-layer oracle (not deployable) | True          |          0.784615  |             3 |                 138405 | True           | True         |
| panda     | J-lens                                      | False         |          0.640152  |            39 |                      0 | False          | False        |
| panda     | plain lens                                  | False         |          0.666667  |          6680 |                    206 | False          | False        |
| panda     | forecast                                    | False         |          0.636364  |           894 |                     18 | False          | False        |
| panda     | final-layer oracle (not deployable)         | False         |          0.693182  |            86 |                      0 | False          | False        |
| panda     | J minus plain lens                          | False         |          0.556818  |            38 |                      0 | False          | False        |
| panda     | J minus forecast                            | False         |          0.543561  |            36 |                      0 | False          | False        |
| panda     | J minus final-layer oracle (not deployable) | False         |          0.541667  |            53 |                      0 | False          | False        |
| giraffe   | J-lens                                      | False         |                    |            30 |                    227 | True           | True         |
| giraffe   | plain lens                                  | False         |                    |             1 |                  34623 | True           | True         |
| giraffe   | forecast                                    | False         |                    |           327 |                  23034 | False          | False        |
| giraffe   | final-layer oracle (not deployable)         | False         |                    |             0 |                      2 | False          | False        |
| giraffe   | J minus plain lens                          | False         |                    |           320 |                    220 | False          | False        |
| giraffe   | J minus forecast                            | False         |                    |            32 |                    224 | False          | False        |
| giraffe   | J minus final-layer oracle (not deployable) | False         |                    |           346 |             1000000000 | False          | False        |
| lion      | J-lens                                      | False         |          0.887043  |            17 |                      0 | False          | False        |
| lion      | plain lens                                  | False         |          0.853821  |           179 |                      2 | False          | False        |
| lion      | forecast                                    | False         |          0.714286  |           189 |                    163 | False          | False        |
| lion      | final-layer oracle (not deployable)         | False         |          0.780731  |            19 |                      1 | False          | False        |
| lion      | J minus plain lens                          | False         |          0.69103   |            17 |                      0 | False          | False        |
| lion      | J minus forecast                            | False         |          0.870432  |            21 |                      0 | False          | False        |
| lion      | J minus final-layer oracle (not deployable) | False         |          0.734219  |           355 |                      0 | False          | False        |
| frog      | J-lens                                      | True          |          1         |             1 |                      7 | False          | False        |
| frog      | plain lens                                  | True          |          1         |            14 |                      0 | False          | False        |
| frog      | forecast                                    | False         |          1         |           354 |                    820 | False          | False        |
| frog      | final-layer oracle (not deployable)         | True          |          1         |             0 |                      1 | False          | False        |
| frog      | J minus plain lens                          | True          |          1         |             1 |                     84 | True           | True         |
| frog      | J minus forecast                            | True          |          1         |             1 |                      7 | False          | False        |
| frog      | J minus final-layer oracle (not deployable) | True          |          1         |             2 |             1000000000 | True           | True         |
| bee       | J-lens                                      | True          |          1         |            81 |                   3158 | False          | False        |
| bee       | plain lens                                  | False         |          0.865854  |          2254 |                 195991 | False          | False        |
| bee       | forecast                                    | False         |          0.789634  |           504 |                    413 | False          | False        |
| bee       | final-layer oracle (not deployable)         | False         |          0.920732  |            77 |                    258 | False          | False        |
| bee       | J minus plain lens                          | True          |          1         |            79 |                   1927 | False          | False        |
| bee       | J minus forecast                            | True          |          1         |            84 |                  15035 | False          | False        |
| bee       | J minus final-layer oracle (not deployable) | True          |          1         |            82 |                 241247 | False          | True         |

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

J-lens: [' France', 'France', ' Germany', ' Belgium', '法国', ' Italy', ' French', ' Switzerland', ' Canada', ' FRANCE', ' Europe', ' Spain', ' Francia', ' Paris', ' Austria', ' England', ' france', ' Poland', ' Britain', ' Romania', ' Denmark', ' Russia', 'ustria', ' Portugal', ' Франция', 'Germany', ' Greece', ' Australia', ' Netherlands', ' Deutschland', '巴黎', ' Hungary']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

plain lens: [' called', ' democr', '简称', 'called', ' sovere', '法国', ' называется', 'više', 'France', 'located', '法兰', ' zuständig', '法网', '邻', ' France', 'ponsible', '名胜', '现', ' referred', '_recipe', ' located', 'adou', '教体', ' nicknamed', '铁塔', 'wser', '叫什么', '{name', '...).', '...*', '日电', ' França']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

forecast: [' France', ' ', ' a', ' one', ' located', '\n', '\n\n', ' on', ' __', ' called', '...', ' not', ' in', ' ___', ' an', ' "', ' Belgium', " '", ' no', ' at', ' ...', ' ____', ' \n', ' (', ' and', ' known', ' In', ' referred', ' -', ' that', ' usually', ' Germany']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

final-layer oracle (not deployable): [' France', ' called', ' known', ' located', ' not', ' also', ' in', ' a', ' named', ' Germany', ' French', '...', ' different', ' part', ' __', ' often', ' referred', ' ______', ' to', ' Paris', ' situated', ':', ' ', ' ____', ' currently', ' one', ' Europe', ' ___', ' Belgium', ' now', ' famous', '\n']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

J minus plain lens: [' France', 'France', ' Germany', ' Belgium', ' Italy', ' French', ' Switzerland', ' Europe', ' Canada', ' Spain', ' Austria', ' England', ' Denmark', ' Portugal', ' Britain', ' Netherlands', ' Francia', ' Russia', ' Hungary', ' Sweden', ' Ireland', ' Poland', ' Argentina', ' Scotland', ' Australia', ' Italia', ' Slovakia', ' Deutschland', ' Norway', ' Europa', ' European', ' Belgian']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

J minus forecast: [' France', 'France', '法国', ' Germany', ' FRANCE', ' French', ' Francia', ' france', ' Франция', 'ustria', 'Germany', ' Deutschland', '巴黎', ' Франции', 'Italy', 'French', ' França', ' فرنسا', 'Canada', 'Paris', 'フランス', ' 프랑스', ' Frankreich', 'Spain', '法國', 'England', '法语', ' french', ' Prancis', 'Europe', ' француз', 'ฝรั่งเศส']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The country containing the city where the Eiffel Tower stands is'

Baseline: ' France.\nQuestion: Is the capital'

J minus final-layer oracle (not deployable): [' France', 'France', ' Belgium', '法国', ' Germany', ' Italy', ' Francia', ' FRANCE', 'ustria', 'Germany', ' Франция', ' Romania', ' Deutschland', '巴黎', ' Britain', ' Франции', ' Portugal', 'Italy', ' Poland', 'French', ' França', 'Canada', 'Paris', ' فرنسا', 'Spain', '法语', 'reland', ' Countries', ' Croatia', ' Belgique', 'フランス', 'England']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

J-lens: [' Beijing', ' Berlin', ' Moscow', ' China', ' London', ' Seoul', ' Rome', ' Madrid', ' Tehran', ' Paris', ' Taipei', '北京', ' Shanghai', ' Prague', ' Pyongyang', ' Bangkok', ' Budapest', ' Jakarta', ' Vienna', ' Cairo', ' Istanbul', ' Ankara', ' Toronto', ' Delhi', ' Warsaw', ' Jerusalem', ' Russia', ' Washington', 'China', ' Athens', ' Brussels', ' cities']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

plain lens: ['ปัก', 'ijing', '北京', 'otope', 'aidu', '现', ' Beijing', '...\\', ' Capitals', '北京的', 'located', ' dumps', 'halte', ' ALSO', 'ruhe', 'agin', ' capitals', '名胜', ' populous', 'stad', 'više', ' selfies', ' Hauptstadt', '}`).', '先到', '长城', '…]', ' capitale', 'nici', ' Mete', '...**', '雾霾']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

forecast: [' a', ' __', ' ', ' at', '\n', ' Beijing', ' ___', ' not', ' an', '...', '\n\n', ' .', ' also', ' no', ' ?', ' Moscow', ' that', ' ...', ' #', ' in', ' ____', ' ______', ' N', ' (', ' its', ' @', ' _', ' another', ' this', ' one', ' \n', ' his']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

final-layer oracle (not deployable): [' Beijing', ' China', ' P', ' also', ' X', ' Be', ' not', '...', ' in', ' Xi', ' Chang', ' North', ' located', ' a', ' __', ' now', ' Tian', ' Berlin', ' ______', ' ___', ' Shanghai', ' Seoul', ' Nan', ' currently', ' an', ' (', ' Chinese', ' Hang', ' still', ' N', ' Pe', ' [']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

J minus plain lens: [' Beijing', ' Berlin', ' Moscow', ' China', ' London', ' Seoul', ' Madrid', ' Rome', ' Tehran', ' Taipei', ' Paris', ' Shanghai', ' Prague', ' Bangkok', ' Budapest', ' Pyongyang', ' Jakarta', ' Cairo', ' Vienna', ' Istanbul', ' Toronto', ' Ankara', ' Delhi', ' Jerusalem', ' Warsaw', ' Russia', ' Washington', ' Athens', 'China', ' Brussels', ' Romania', ' Kyoto']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

J minus forecast: [' Beijing', ' Berlin', ' China', ' Moscow', ' London', ' Seoul', ' Madrid', ' Tehran', ' Taipei', ' Rome', ' Paris', '北京', ' Shanghai', ' Pyongyang', ' Budapest', ' Jakarta', ' Prague', ' Cairo', ' Bangkok', ' Istanbul', ' Ankara', ' Toronto', ' Jerusalem', 'China', ' Washington', ' Delhi', ' Athens', ' Cities', '北京的', ' Brussels', '.\\', ' Vienna']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Great Wall is'

Baseline: ' Beijing.\nQuestion: Is the capital'

J minus final-layer oracle (not deployable): [' Beijing', ' Berlin', ' Moscow', ' London', ' Seoul', ' Madrid', ' Rome', ' Tehran', ' Taipei', ' Paris', '北京', ' Prague', ' Budapest', ' Bangkok', ' Jakarta', ' Pyongyang', ' Shanghai', ' Vienna', ' Cairo', ' Istanbul', ' Ankara', ' Toronto', ' Warsaw', ' Delhi', ' Jerusalem', ' Russia', 'China', ' Athens', ' Washington', '北京的', ' cities', ' Brussels']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

J-lens: [' Cairo', ' Egypt', ' London', ' Paris', ' Alexandria', ' Berlin', ' Nairobi', ' Riyadh', ' Dubai', ' Madrid', ' Baghdad', ' Rome', ' Jerusalem', ' Bangkok', ' Vienna', ' Moscow', ' Tehran', ' Athens', ' Beijing', ' Ankara', ' Johannesburg', ' Istanbul', 'Paris', 'London', ' Prague', ' Budapest', ' Beirut', ' Brasília', ' Jakarta', ' Dakar', ' Islamabad', ' Memphis']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

plain lens: ['先到', '名胜', ' القاهرة', 'otope', ' dumps', '现', 'više', '现任', 'umed', '…]', '遥遥', 'located', '古都', '...\\', '.python', 'ẹo', '北京', '}`).', ' Fai', ' selfies', 'ถัด', '俑', 'üste', ' correc', ' Luân', 'Python', ' Capitals', '北京的', 'postav', ' greve', 'currently', '名城']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

forecast: [' a', ' ', ' not', '\n', ' one', ' another', '\n\n', ' no', ' .', ' an', ' its', ' Egypt', ' Paris', ' located', ' that', ' (', ' New', '...', ' Berlin', ' Rome', ' \n', ' #', ' ...', ' N', ' Moscow', ' Nairobi', ' "', ' at', ' Beijing', " '", ' Cairo', ' London']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

final-layer oracle (not deployable): [' Cairo', ' Egypt', ' not', ' Alexandria', '...', ' in', ' also', ' C', ' Kh', ' ___', ' a', ' __', ' London', ' G', ' Paris', ' located', ' different', ' now', ' an', ' Memphis', ' ______', ' ...', ' either', ' Abu', ' Lux', ' ancient', '\n', ' K', ' Tehran', ' Washington', '.', ' on']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

J minus plain lens: [' Cairo', ' Egypt', ' London', ' Paris', ' Berlin', ' Alexandria', ' Nairobi', ' Riyadh', ' Dubai', ' Madrid', ' Baghdad', ' Rome', ' Jerusalem', ' Bangkok', ' Vienna', ' Moscow', ' Tehran', ' Athens', ' Beijing', ' Ankara', ' Johannesburg', ' Istanbul', 'Paris', ' Prague', 'London', ' Budapest', ' Beirut', ' Brasília', ' Jakarta', ' Dakar', ' Islamabad', ' Memphis']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

J minus forecast: [' Cairo', ' Egypt', ' London', ' Paris', ' Alexandria', ' Berlin', ' Nairobi', ' Riyadh', ' Dubai', ' Madrid', ' Baghdad', ' Jerusalem', ' Rome', ' Bangkok', ' Vienna', ' Tehran', ' Athens', ' Ankara', ' Johannesburg', ' Istanbul', 'Paris', ' Moscow', 'London', ' Beijing', ' Budapest', ' Prague', ' Beirut', ' Brasília', ' Jakarta', ' Islamabad', ' Bogotá', ' Memphis']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the pyramids of Giza is'

Baseline: ' Cairo.\nQuestion: Is the capital'

J minus final-layer oracle (not deployable): [' London', ' Egypt', ' Paris', ' Berlin', ' Alexandria', ' Nairobi', ' Riyadh', ' Dubai', ' Madrid', ' Baghdad', ' Rome', ' Jerusalem', ' Vienna', ' Bangkok', ' Moscow', ' Tehran', ' Athens', ' Beijing', ' Ankara', ' Johannesburg', ' Istanbul', 'Paris', 'London', ' Prague', ' Budapest', ' Brasília', ' Beirut', ' Jakarta', ' Dakar', ' Islamabad', ' Bogotá', ' Brussels']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

J-lens: [' Delhi', ' Mumbai', ' London', ' Kolkata', ' Paris', ' Tehran', ' Cairo', ' Islamabad', ' Jakarta', ' Bangkok', ' Hyderabad', ' Istanbul', ' Riyadh', ' Madrid', ' Karachi', ' Bombay', ' Beijing', ' India', ' Nairobi', ' Amsterdam', ' Dubai', ' Berlin', ' Chennai', ' Baghdad', ' Moscow', ' Pakistan', ' Lahore', ' Budapest', ' Bangalore', ' Vienna', 'Paris', 'London']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

plain lens: ['现', '}`).', 'located', '马拉', 'više', '名胜', '...**', '先到', ' Capitals', '粉底', '檀', ' selfies', '...\\', ' dumps', '…]', '...”', 'ẹo', '...*', ' fais', '____', ' fools', 'hatian', ' freaking', 'DIC', '北京', 'orden', '教体', '现为', '...).', 'اضرة', '...]', ' إسلام']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

forecast: ['\n', ' ', ' not', " '", ' a', ' in', '\n\n', ' ...', ' at', ' New', ' __', ' located', '...', ' .', ' on', ' (', ' North', ' \n', ' ___', ' Sur', ' its', ' Delhi', ' #', ' In', ' Not', ' also', ' that', ' N', ' _', ' his', ' Paris', ' ?']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

final-layer oracle (not deployable): [' New', ' Delhi', ' India', ' in', ' Dh', ' not', ' Mumbai', ' A', '...', ' Kolkata', ' now', ' unknown', ' ...', ' called', ' known', ' Islamabad', ' ______', ' different', ' also', ' Hyderabad', ' __', ' M', ' a', ' located', ' ___', ' Ja', ' Del', ' on', '.', ' Tehran', '?', ' new']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

J minus plain lens: [' Mumbai', ' Delhi', ' London', ' Kolkata', ' Paris', ' Tehran', ' Cairo', ' Jakarta', ' Bangkok', ' Islamabad', ' Hyderabad', ' Istanbul', ' Riyadh', ' Karachi', ' Madrid', ' Bombay', ' Beijing', ' India', ' Amsterdam', ' Nairobi', ' Dubai', ' Berlin', ' Chennai', ' Baghdad', ' Moscow', ' Pakistan', ' Lahore', ' Budapest', ' Bangalore', ' Vienna', 'Paris', 'London']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

J minus forecast: [' Mumbai', ' Delhi', ' London', ' Kolkata', ' Paris', ' Tehran', ' Cairo', ' Islamabad', ' Jakarta', ' Bangkok', ' Hyderabad', ' Riyadh', ' Istanbul', ' Karachi', ' Madrid', ' Bombay', ' Beijing', ' Amsterdam', ' Dubai', ' India', ' Nairobi', ' Chennai', ' Baghdad', ' Berlin', ' Pakistan', ' Lahore', ' Moscow', ' Budapest', ' Bangalore', ' Vienna', 'London', 'Paris']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing the Taj Mahal is'

Baseline: ' New Delhi.\nQuestion: What is'

J minus final-layer oracle (not deployable): [' Mumbai', ' London', ' Kolkata', ' Paris', ' Tehran', ' Cairo', ' Jakarta', ' Bangkok', ' Islamabad', ' Hyderabad', ' Riyadh', ' Istanbul', ' Madrid', ' Karachi', ' Bombay', ' Beijing', ' Amsterdam', ' Nairobi', ' Dubai', ' Berlin', ' Chennai', ' Baghdad', ' Moscow', ' Pakistan', ' Budapest', ' Lahore', ' Bangalore', ' Vienna', 'Paris', 'London', ' Ankara', ' Bogotá']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

J-lens: [' Toronto', ' Canada', ' Ottawa', ' Montreal', 'Canada', 'Toronto', ' Quebec', ' London', ' Vancouver', ' Ontario', ' canada', ' Canadian', ' Québec', ' Winnipeg', ' Montréal', ' Canberra', ' Calgary', ' Washington', ' Canadians', ' Bogotá', ' Paris', ' Berlin', ' Sydney', ' Edmonton', ' Kanada', 'uckland', ' Canadá', ' Australia', ' Beijing', 'London', ' Manitoba', ' Dublin']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

plain lens: ['.tmp', ' treason', ' canada', ' also', 'urin', 'also', ' constitutional', ' Canada', '威士', 'ปัก', '心惊', ' ALSO', '少儿', '现', ' theirs', '国旗', 'orden', ' Capitals', 'rome', 'acre', ' institutes', '马拉', '枫叶', 'nici', '破冰', 'Canada', '.gc', ' scares', ' forests', '...**', '钰', ' democr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

forecast: [' ', '\n\n', '\n', ' part', ' __', ' ...', ' Canada', ' also', ' one', ' not', ' Ottawa', ' New', ' ___', ' .', '...', ' that', ' In', ' U', ' ____', ' Toronto', ' usually', ' at', ' located', ' no', ' _', ' O', ' *', ' Ok', ' Ontario', ' #', '\r\n', ' (']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

final-layer oracle (not deployable): [' Ottawa', ' Canada', ' Toronto', ' Vancouver', ' also', '...', ' Washington', ' Ontario', ' London', ' Canberra', ' Victoria', ' not', ' Quebec', ' Montreal', ' in', ' ...', ' New', ' Wellington', ' Osaka', ' Canadian', ' Kyoto', ' Beijing', ' Paris', ' Kingston', ' O', ' ______', ' now', ' __', ' Edmonton', ' an', ' Seoul', ' **']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

J minus plain lens: [' Toronto', ' Canada', ' Ottawa', ' Montreal', 'Canada', 'Toronto', ' Quebec', ' London', ' Vancouver', ' Ontario', ' Canadian', ' Québec', ' Winnipeg', ' Montréal', ' Canberra', ' Calgary', ' Washington', ' Canadians', ' Paris', ' Bogotá', ' Berlin', ' Edmonton', ' Sydney', ' Manitoba', 'London', ' Australia', ' Beijing', 'uckland', ' Alberta', ' Canadá', ' Saskatchewan', ' Boston']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

J minus forecast: [' Toronto', ' Canada', ' Ottawa', 'Canada', ' Montreal', 'Toronto', ' Quebec', ' London', ' Vancouver', ' canada', ' Québec', ' Winnipeg', ' Canadian', ' Canberra', ' Montréal', ' Calgary', ' Canadians', ' Bogotá', ' Kanada', 'uckland', ' Canadá', 'London', ' Sydney', ' Edmonton', ' Paris', ' Manitoba', ' Westminster', ' Saskatchewan', ' Dublin', 'Canadian', ' Newfoundland', '伦敦']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country with a maple leaf on its flag is'

Baseline: ' Ottawa.\nQuestion: What is the'

J minus final-layer oracle (not deployable): [' Toronto', ' Canada', 'Canada', ' Montreal', 'Toronto', ' Quebec', ' canada', ' Québec', ' Montréal', ' Winnipeg', ' Canadians', ' Calgary', ' Bogotá', ' London', ' Kanada', 'uckland', ' Canadá', 'London', ' Canadian', ' Dublin', ' Berlin', ' Manitoba', ' Boston', ' Belfast', 'Canadian', '.\\', ' Newfoundland', '伦敦', ' Westminster', ' Amsterdam', ' Minneapolis', ' Brasília']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

J-lens: [' London', ' Canberra', ' Sydney', ' Melbourne', ' Toronto', ' Paris', ' Bangkok', ' Jakarta', ' Berlin', ' Australia', ' Nairobi', ' Brisbane', ' Johannesburg', ' Seoul', ' Dublin', ' Madrid', ' Beijing', ' Taipei', ' Honolulu', ' Buenos', ' Vienna', ' Ottawa', ' Auckland', ' Athens', ' Tehran', 'London', ' Singapore', ' Moscow', ' Dubai', ' Riyadh', ' Rome', ' Washington']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

plain lens: ['otope', '遥遥', 'also', '先到', ' NOT', 'located', 'urin', ' ALSO', ' capitals', ' Goed', 'rome', ' also', ' capitale', '้ม', '}`).', '暂定', 'not', '锣', 'nota', 'auss', ' swearing', 'NOT', 'に行ってきました', '马拉', ' сов', 'жди', 'postav', '乌鲁', 'ถัด', ' terletak', ' nto', ' correc']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

forecast: [' not', ' ', ' also', ' a', ' .', ' __', '\n', '\n\n', ' New', ' ...', ' _', ' no', ' at', ' that', ' Berlin', ' in', ' located', " '", ' ___', ' ____', ' Melbourne', ' Bangkok', ' different', ' N', ' one', ' such', ' (', ' In', ' usually', ' Ok', ' "', ' M']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

final-layer oracle (not deployable): [' Canberra', ' Sydney', ' Melbourne', ' Australia', ' in', ' not', ' also', ' Brisbane', ' a', ' Seoul', '...', ' different', ' Singapore', ' known', ' London', ' Perth', ' New', ' Paris', ' Kyoto', ' Osaka', ' Berlin', ' Beijing', ' Wellington', ' Washington', ' called', ' located', ' Darwin', ' Ottawa', ' Adelaide', ' Jakarta', ' Rome', ' Bangkok']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

J minus plain lens: [' London', ' Canberra', ' Sydney', ' Melbourne', ' Toronto', ' Paris', ' Bangkok', ' Jakarta', ' Berlin', ' Nairobi', ' Australia', ' Brisbane', ' Johannesburg', ' Seoul', ' Dublin', ' Madrid', ' Taipei', ' Beijing', ' Honolulu', ' Vienna', ' Buenos', ' Auckland', ' Ottawa', ' Tehran', ' Athens', 'London', ' Dubai', ' Singapore', ' Moscow', ' Riyadh', ' Amsterdam', ' Washington']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

J minus forecast: [' London', ' Canberra', ' Sydney', ' Melbourne', ' Paris', ' Toronto', ' Jakarta', ' Bangkok', ' Berlin', ' Australia', ' Nairobi', ' Brisbane', ' Johannesburg', ' Seoul', ' Dublin', ' Madrid', ' Taipei', ' Honolulu', ' Buenos', ' Vienna', ' Beijing', ' Auckland', ' Tehran', ' Athens', 'London', ' Riyadh', ' Dubai', 'uckland', ' Amsterdam', '伦敦', ' Bogotá', ' Budapest']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country to which kangaroos are native is'

Baseline: ' Canberra.\nQuestion: Is the capital'

J minus final-layer oracle (not deployable): [' London', ' Toronto', ' Paris', ' Bangkok', ' Jakarta', ' Berlin', ' Nairobi', ' Johannesburg', ' Brisbane', ' Dublin', ' Melbourne', ' Madrid', ' Taipei', ' Vienna', ' Honolulu', ' Buenos', ' Tehran', ' Athens', 'London', ' Moscow', ' Auckland', ' Dubai', ' Riyadh', 'uckland', ' Amsterdam', '伦敦', ' Chicago', ' Seoul', ' Budapest', ' Bogotá', ' NYC', ' Montreal']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

J-lens: [' Bogotá', ' Brasília', ' Buenos', ' Jakarta', ' Berlin', ' Madrid', ' Paris', ' Lisbon', ' London', ' Caracas', ' Brazil', ' Johannesburg', ' Amsterdam', ' São', ' Seoul', ' Mexico', ' NYC', ' Ciudad', ' Oslo', ' Washington', ' Frankfurt', ' Bangkok', ' Nairobi', ' Vienna', ' Miami', ' City', ' Canberra', ' Cities', ' Curitiba', ' Portugal', ' Toronto', ' Barcelona']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

plain lens: ['urin', '...).', 'umed', 'lah', ')?$', '名胜', 'više', ' swearing', ' ogs', 'located', ' gunmen', '}`).', '...\\', '遥遥', 'lima', ' correc', ' zod', 'ẹo', 'вален', 'lis', '马拉', ' Luân', 'umus', 'alur', ' Edi', ' celu', ' greve', '心惊', '()?.', '้ม', 'AGENT', 'auss']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

forecast: ['\n', ' not', ' .', ' ', '\n\n', ' ...', ' a', ' New', ' _', ' U', '...', ' (', ' in', " '", ' another', ' ___', ' located', ' also', ' In', ' __', ' its', ' on', ' one', ' N', ' Berlin', ' at', ' ______', ' \n\n', ' ____', '<|im_end|>', ' about', ' \n']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

final-layer oracle (not deployable): [' Bras', ' Brazil', ' Brasília', ' São', ' Buenos', ' Br', ' Washington', ' not', '...', ' Sao', ' Bel', ' also', ' different', ' ______', ' a', ' __', ' Santiago', ' Beijing', ' located', ' Salvador', ' in', ' ', ' ...', ' called', ' currently', ' Braz', ' Brazilian', ' ___', ' Brussels', ' Lisbon', ' ____', ' known']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

J minus plain lens: [' Bogotá', ' Brasília', ' Buenos', ' Jakarta', ' Madrid', ' Berlin', ' Paris', ' Lisbon', ' London', ' Caracas', ' Brazil', ' Johannesburg', ' Amsterdam', ' São', ' Seoul', ' Mexico', ' NYC', ' Ciudad', ' Oslo', ' Frankfurt', ' Washington', ' Nairobi', ' Bangkok', ' Miami', ' Vienna', ' City', ' Canberra', ' Cities', ' Barcelona', ' Portugal', ' Toronto', ' Curitiba']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

J minus forecast: [' Bogotá', ' Brasília', ' Buenos', ' Jakarta', ' Madrid', ' Berlin', ' Paris', ' Lisbon', ' London', ' Caracas', ' Brazil', ' Johannesburg', ' Amsterdam', ' São', ' Seoul', ' Mexico', ' Ciudad', ' NYC', ' Oslo', ' Nairobi', ' Bangkok', ' Washington', ' Frankfurt', ' Vienna', ' Canberra', ' Miami', ' Cities', ' City', ' Portugal', ' Curitiba', ' Barcelona', 'Paris']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rio de Janeiro is'

Baseline: ' Brasilia.\nHypothesis:'

J minus final-layer oracle (not deployable): [' Bogotá', ' Buenos', ' Jakarta', ' Madrid', ' Berlin', ' Paris', ' Lisbon', ' London', ' Caracas', ' Johannesburg', ' Amsterdam', ' Seoul', ' Mexico', ' NYC', ' Ciudad', ' Oslo', ' Frankfurt', ' Nairobi', ' Bangkok', ' Miami', ' Vienna', ' City', ' Cities', ' Barcelona', ' Toronto', ' Portugal', ' Canberra', 'Paris', ' Curitiba', ' Naples', ' Lagos', ' Argentina']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

J-lens: [' Jakarta', ' Berlin', ' Singapore', ' Seoul', ' Taipei', ' Bangkok', ' London', ' Honolulu', ' Paris', ' Beijing', ' Thailand', ' Moscow', ' Hawaii', ' Toronto', ' Tehran', ' Germany', ' Madrid', '东京', ' Kyoto', ' Korea', ' Taiwan', ' Tokio', ' Mexico', ' Italy', ' Osaka', ' Malaysia', ' Australia', ' Vienna', ' Canberra', ' Denmark', ' Indonesia', ' Canada']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

plain lens: [' also', 'also', ' ALSO', 'otope', 'urin', 'located', 'ؤل', '/is', 'ปัก', ' ebenfalls', '马拉', 'に行ってきました', 'lets', ' likewise', 'mét', 'olate', '少儿', ' terletak', '小编为大家整理的', 'olation', 'hog', ' также', 'oglio', '...', '旅游目的地', ' ogs', ' тоже', ' również', 'conde', '齐齐', '遥遥', ' také']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

forecast: [' ', '\n', ' __', '\n\n', ' also', ' .', ' N', ' ___', ' a', ' ...', ' _', ' ____', ' In', ' not', ' ?', ' Ok', ' in', ' New', '...', ' (', ' *', ' \n', ' located', ' ______', ' at', ' **', ' that', ' "', ' \n\n', '\r\n', " '", ' $']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

final-layer oracle (not deployable): [' also', ' Seoul', ' Beijing', ' Kyoto', ' Osaka', ' Singapore', ' Taipei', ' Taiwan', ' Berlin', ' not', ' South', ' New', '...', ' Hong', ' Bangkok', ' Washington', ' China', ' Jakarta', ' London', ' Paris', ' Sydney', ' Shanghai', ' in', ' ___', ' ______', ' Hiro', ' Thailand', ' a', ' Hawaii', ' N', ' **', ' known']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

J minus plain lens: [' Jakarta', ' Berlin', ' Singapore', ' Seoul', ' Taipei', ' Bangkok', ' London', ' Honolulu', ' Paris', ' Beijing', ' Thailand', ' Moscow', ' Hawaii', ' Toronto', ' Tehran', ' Madrid', ' Germany', ' Kyoto', '东京', ' Korea', ' Taiwan', ' Tokio', ' Mexico', ' Italy', ' Osaka', ' Malaysia', ' Vienna', ' Australia', ' Denmark', ' Canberra', ' Indonesia', ' Canada']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

J minus forecast: [' Jakarta', ' Berlin', ' Singapore', ' Seoul', ' Taipei', ' Bangkok', ' London', ' Honolulu', ' Paris', ' Beijing', ' Thailand', ' Moscow', ' Toronto', ' Tehran', ' Germany', '东京', ' Madrid', ' Korea', ' Hawaii', ' Kyoto', ' Taiwan', ' Tokio', ' Italy', ' Australia', ' Malaysia', ' Canberra', ' Vienna', ' Denmark', ' Indonesia', ' Osaka', ' Mexico', ' Shanghai']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country whose flag features the Sun of May and two light blue horizontal bands is'

Baseline: ' Tokyo.\nQuestion: Is the capital'

J minus final-layer oracle (not deployable): [' Jakarta', ' Berlin', ' Honolulu', ' Bangkok', ' London', '东京', ' Taipei', ' Moscow', ' Toronto', ' Madrid', ' Tehran', ' Thailand', ' Tokio', ' Germany', ' Hawaii', ' Denmark', ' Paris', ' Italy', ' Malaysia', ' Korea', ' Netherlands', ' Dubai', ' Vienna', ' Iceland', ' Panama', ' Stockholm', ' Lisbon', '?\\', '.\\', ' Munich', ' Nairobi', ' Amsterdam']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

J-lens: [' sheep', '羊', ' Sheep', ' goats', '羔', '羊毛', ' goat', ' lamb', ' fleece', ' rabbits', ' flock', ' pups', ' Goat', ' kittens', ' baby', ' puppies', ' wolf', '羊水', ' wolves', ' rabbit', ' puppy', ' livestock', ' fetus', 'baby', ' newborn', ' breeds', ' bunny', '狼', ' laine', '仔猪', ' babies', ' Baby']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

plain lens: ['...', '\ufeff', '\xa0', '羊毛', '羔', ':', 'lay', '绒毛', '领头羊', ' laine', '..........', '.....', 'lambda', ' Rhodes', '羊羊', ' ...', '绒', '这个小', 'doll', '骤', 'AWN', '...........', 'ugen', '<<<<<<<', '产', '�', ' breeds', ' fleece', '那样的', ' sheep', '仔', '_RUNTIME']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

forecast: [' a', ' "', '\n', ' ', ' sheep', ' an', ' (', '\n\n', ' not', ' available', ' ...', ' usually', ' ,', ' also', ' such', ' made', ' used', ' that', ' **', ' provided', ' either', ' cotton', ' .', " '", ' one', ' -', ' qualified', ' after', ' only', ' found', ' lamb', ' simply']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

final-layer oracle (not deployable): [' lamb', ' a', " '", ' sheep', ' Lamb', ' lam', ' called', ' "', ' \\"', ' “', ':', ' not', ' ‘', '...', ' Lam', ' kid', ' ______', ' goat', ' different', ' __', ' L', ' ___', ' ...', ' ew', ' an', ' also', ' baby', ' llama', ' usually', ' often', ' ____', ' given']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

J minus plain lens: [' sheep', '羊', ' Sheep', ' goats', '羔', '羊毛', ' goat', ' lamb', ' fleece', ' rabbits', ' flock', ' pups', ' kittens', ' Goat', ' baby', ' puppies', ' wolf', ' wolves', '羊水', ' rabbit', ' puppy', ' livestock', 'baby', ' newborn', ' bunny', ' fetus', '狼', '仔猪', ' babies', ' pigs', ' Baby', ' kitten']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

J minus forecast: [' sheep', '羊', ' Sheep', ' goats', '羔', '羊毛', ' goat', ' lamb', ' fleece', ' rabbits', ' flock', ' pups', ' kittens', ' Goat', ' puppies', ' wolf', ' baby', '羊水', ' wolves', ' rabbit', ' puppy', ' livestock', 'baby', ' fetus', ' newborn', ' breeds', ' laine', '狼', ' bunny', '仔猪', ' babies', ' Baby']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the farm animal raised for its wool is'

Baseline: ' lamb.\nHypothesis: The'

J minus final-layer oracle (not deployable): [' sheep', '羊', ' Sheep', ' goats', '羔', '羊毛', ' goat', ' fleece', ' rabbits', ' flock', ' pups', ' kittens', ' Goat', ' puppies', '羊水', ' wolves', ' wolf', ' puppy', ' rabbit', ' baby', ' livestock', 'baby', ' fetus', ' breeds', '狼', ' laine', ' newborn', '仔猪', ' bunny', ' babies', ' pigs', '山羊']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

J-lens: ['.\\', '.\\"', ' seven', ' five', ' four', ' twelve', '?\\', ' twenty', ' fourteen', ' six', ' thirteen', ' eight', ' equals', ' equal', ' forty', ').\\', ' thirty', ' fifteen', ' nine', '___', '...\\', '。\\', ' sixteen', ' fewer', ' eleven', ' seventeen', '(number', ' exactly', ' three', 'five', '____', ' typically']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

plain lens: ['.numberOf', '很好奇', 'olate', '总数', '(number', 'いただけます', '.trailing', '頂けます', 'shed', ':number', 'otope', '_number', '砰砰', ' warta', 'lessness', '通常为', 'numberOf', 'variably', 'gues', 'wane', 'omers', 'Trail', 'usually', 'عدد', 'mane', '.EqualTo', '一数', 'NumberOf', '的好朋友', 'atriz', ' trots', '访客']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

forecast: [' ', ' four', ' not', ' one', ' usually', ' exactly', '\n\n', ' no', ' .', ' at', ' nine', ' six', ' \n\n', ' always', ' (', ' seven', ' equal', ' forty', ' in', ' five', ' three', ' between', ' either', ' two', ' __', ' equals', ' typically', ' about', ' $', ' eight', ' twenty', ' an']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

final-layer oracle (not deployable): [' ', ' four', ' eight', ' six', ' seven', ' five', ' three', ' two', ' zero', ' usually', ' not', ' equal', ' exactly', ' __', ' ten', ' odd', ' nine', ' always', ' unknown', ' one', ' even', ' typically', ':', ' less', ' ___', ' twelve', ' also', ' at', ' known', ' different', ' sixteen', ' ____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

J minus plain lens: ['.\\', '.\\"', ' seven', ' five', ' four', ' twelve', ' twenty', '?\\', ' fourteen', ' six', ' thirteen', ' equal', ' eight', ' equals', ' forty', ' thirty', ').\\', ' fifteen', ' nine', '___', '...\\', '。\\', ' sixteen', ' eleven', ' fewer', ' seventeen', ' three', 'five', '____', ' exactly', ' typically', '__.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

J minus forecast: ['.\\', '.\\"', ' seven', ' five', ' twelve', ' four', '?\\', ' twenty', ' fourteen', ' thirteen', ' six', ' eight', ' equals', ' equal', ' forty', ').\\', ' thirty', ' fifteen', '___', '...\\', ' nine', '。\\', ' sixteen', ' fewer', ' eleven', '(number', ' seventeen', 'five', '____', ' three', ' typically', '__.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal with black and white stripes that resembles a horse is'

Baseline: ' 4.\nQuestion: How many'

J minus final-layer oracle (not deployable): ['.\\', '.\\"', ' seven', ' twelve', ' five', '?\\', ' twenty', ' fourteen', ' thirteen', ' equals', ' forty', ').\\', ' thirty', ' fifteen', ' equal', '___', '...\\', '。\\', ' nine', ' fewer', '(number', ' seventeen', ' sixteen', ' eleven', 'five', '____', '__.', ' eighteen', ' horses', ' fifty', ' sixty', ' typically']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

J-lens: ['鼻子', ' elephant', ' elephants', ' noses', ' Elephant', '鼻', ' Mouth', '鼻梁', 'odont', ' horns', ' jaw', ' Teeth', ' Pork', ' cheeks', ' nasal', ' jaws', ' носа', ' Tooth', ' Jaw', ' Penis', '鼻尖', ' muzzle', ' pigs', ' cheek', ' panda', ' teeth', ' penis', ' Whale', ' Godzilla', ' claws', ' naso', '野猪']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

plain lens: [' biro', ' trump', ' noses', ' аук', '讹', '这名', '冲锋', ' descended', ' Fucking', '咆哮', 'hin', ' cari', '.hasMore', ' waj', '大吼', '随行', '再接', 'amah', ' mej', '很好吃', '鼻子', ' manus', 'derived', 'iphone', ' প্রশ', '前端', '...(', ' Nase', ' adaptations', ' laik', 'ρκ', 'umbo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

forecast: [' ', ' a', ' its', ' that', ' one', ' "', ' .', ' ``', '\n', ' both', ' Por', ' an', ' My', ' ...', " '", ' North', ' also', ' two', ' derived', ' ant', ' usually', ' either', ' all', ' Wh', ' saber', ' M', ' my', ' used', ' identified', ' :', ' in', ' not']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

final-layer oracle (not deployable): [' a', ' an', " '", ' called', ' rh', ' elephant', ' prob', ' "', ' “', ' trunk', ' \\"', ' Ivory', ' ‘', ' M', ' Tr', ' Mand', '...', ':', ' Rh', ' Elephant', ' ivory', ' known', ' *', ' Mam', ' mand', ' m', ' its', ' Africa', ' tr', ' hipp', ' Mor', ' t']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

J minus plain lens: ['鼻子', ' elephant', ' elephants', ' noses', ' Elephant', '鼻', ' Mouth', 'odont', ' horns', '鼻梁', ' jaw', ' Teeth', ' Pork', ' nasal', ' cheeks', ' jaws', ' носа', ' Tooth', ' Penis', ' Jaw', ' muzzle', '鼻尖', ' pigs', ' panda', ' Whale', ' penis', ' Godzilla', ' cheek', ' teeth', ' claws', ' naso', '野猪']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

J minus forecast: ['鼻子', ' elephant', ' elephants', ' noses', ' Elephant', '鼻', ' Mouth', 'odont', '鼻梁', ' horns', ' jaw', ' Teeth', ' cheeks', ' Pork', ' nasal', ' jaws', ' Tooth', ' носа', ' Jaw', ' Penis', '鼻尖', ' muzzle', ' pigs', ' teeth', ' Whale', ' panda', ' Godzilla', ' penis', ' cheek', ' claws', '野猪', ' naso']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name of the long flexible nose of the huge gray land animal with tusks is'

Baseline: ' a rhino.\nHypothesis'

J minus final-layer oracle (not deployable): ['鼻子', ' elephants', ' noses', ' elephant', '鼻', ' Elephant', ' Mouth', 'odont', '鼻梁', ' horns', ' jaw', ' Teeth', ' cheeks', ' Pork', ' nasal', ' jaws', ' носа', ' Tooth', ' Penis', ' Jaw', '鼻尖', ' muzzle', ' pigs', ' cheek', ' teeth', ' Godzilla', ' panda', ' Whale', ' penis', ' claws', ' naso', '野猪']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

J-lens: [' bamboo', ' berries', ' Bamboo', ' foods', '竹子', ' cabbage', ' vegetarian', ' meat', ' eating', ' diet', ' bananas', ' peanuts', ' rice', ' eaten', ' mushrooms', ' carniv', ' seafood', ' salmon', ' bread', ' sushi', ' potatoes', ' snacks', ' edible', ' vegetables', ' eats', ' starvation', ' plants', ' grass', ' eat', ' nuts', ' insects', ' cheese']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

plain lens: ['hardt', 'bestand', 'NUM', '�', ' principally', 'PLUS', ' chiefly', '一顿', ' primarily', 'द्ध', 'shit', '下山', '习性', '..', '顶级', '��', 'NOT', '上传者', 'NEY', 'mate', 'logger', '构', '素的', ' mainly', 'doc', '大王', 'PDF', 'logging', 'จำ', 'upan', ' turista', ' Hunters']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

forecast: [' on', ' ,', ' .', '\n\n', ' "', ' usually', ' wild', ' snow', ' unf', ' un', ' ...', ' outside', ' indigenous', ' in', ' green', ' grass', ' mostly', ' primarily', ' ___', ' bamboo', ' a', ' red', ' not', ' based', ' ______', ' ', ' that', ' (', ' mainly', ' as', ' olive', '\n']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

final-layer oracle (not deployable): [' bamboo', ' honey', ' fish', ' pine', ' berries', ' salmon', ' ac', ' tree', ' a', ' nuts', ' mushrooms', ' h', ' insects', ' roots', ' wild', ' p', ' snow', ' wal', ' meat', ' corn', ' wood', ' grass', ' chest', ' red', ' ants', ' rice', ' fungus', ' water', ' gr', ' rh', ' bark', ' plants']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

J minus plain lens: [' bamboo', ' berries', ' Bamboo', ' foods', '竹子', ' cabbage', ' vegetarian', ' meat', ' eating', ' diet', ' bananas', ' peanuts', ' rice', ' mushrooms', ' carniv', ' eaten', ' seafood', ' salmon', ' bread', ' potatoes', ' sushi', ' snacks', ' edible', ' vegetables', ' eats', ' grass', ' plants', ' eat', ' nuts', ' cheese', ' insects', ' fish']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

J minus forecast: [' bamboo', ' berries', ' Bamboo', ' foods', '竹子', ' cabbage', ' vegetarian', ' meat', ' eating', ' diet', ' bananas', ' peanuts', ' mushrooms', ' seafood', ' eaten', ' carniv', ' rice', ' salmon', ' sushi', ' potatoes', ' bread', ' snacks', ' edible', ' vegetables', ' eats', ' starvation', ' plants', ' eat', ' nuts', ' insects', ' carbohydrates', ' cheese']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The main food of the black and white bear native to China is'

Baseline: ' bamboo.\nHypothesis: The'

J minus final-layer oracle (not deployable): [' bamboo', ' Bamboo', ' foods', '竹子', ' cabbage', ' vegetarian', ' eating', ' diet', ' bananas', ' carniv', ' eaten', ' snacks', ' peanuts', ' sushi', ' seafood', ' bread', ' eats', ' edible', ' starvation', ' eat', ' vegetables', ' carbohydrates', ' diets', '的食物', ' potatoes', ' forests', ' bamb', ' tofu', ' cheese', ' غذ', ' vegetation', ' nutrition']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

J-lens: [' baby', ' babies', 'baby', ' kittens', ' elephant', ' elephants', '___', ' Baby', ' panda', ' lizard', ' dinosaur', ' turtles', ' kitten', ' newborn', ' snakes', ' puppies', ' chicks', ' peanuts', '____', '-neck', ' Babies', '________', ' turtle', ' bamboo', 'Baby', '_________', ' monkeys', ' puppy', ' pang', ' rabbits', ' zoo', ' gir']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

plain lens: ['伸长', ' gir', '拉长', ' biro', '........', '...', '.........', '..........', ' называется', '长度的', ' called', '................', '异响', 'draft', ' pearls', 'venirs', ' rekord', '营养价值', '叫我', 'द्ध', 'inky', '<<<<<<<', 'wana', '致远', '...........', '叫什么', '_override', ' Suites', '...(', 'правка', 'LENGTH', 'ardless']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

forecast: [' ', '\n', '\n\n', ' that', ' ...', '...', " '", ' (', ' .', ' not', ' in', ' its', ' "', ' an', ' -', ' usually', ' ?', ' such', ' **', ' one', ' to', ' found', ' called', ' derived', ' when', ' given', ' --', ':', ' their', ' also', '<|im_end|>', ' :']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

final-layer oracle (not deployable): [' gir', ' called', ' calf', " '", ' "', ' “', ' fo', ' baby', ' gaz', '...', ' an', ' ______', ' \\"', ' ok', ' Gir', ' k', ' ‘', ' cub', ' K', ':', ' ?', ' not', ' ...', ' __', ' neon', ' ___', ' col', ' tort', ' kitten', ' ostr', ' C', ' chick']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

J minus plain lens: [' baby', ' babies', 'baby', ' kittens', ' elephants', ' elephant', ' Baby', '___', ' panda', ' lizard', ' dinosaur', ' turtles', ' kitten', ' newborn', ' snakes', ' puppies', ' chicks', ' peanuts', '-neck', '____', ' Babies', '________', ' turtle', ' bamboo', 'Baby', ' monkeys', ' puppy', '_________', ' rabbits', ' pang', ' toddler', ' zoo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

J minus forecast: [' baby', ' babies', 'baby', ' kittens', ' elephants', ' elephant', '___', ' Baby', ' panda', ' lizard', ' dinosaur', ' turtles', ' kitten', ' newborn', ' snakes', ' puppies', ' chicks', '-neck', ' peanuts', '____', ' Babies', '________', 'Baby', ' turtle', ' bamboo', '_________', ' monkeys', ' pang', ' puppy', ' rabbits', ' toddler', ' zoo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the spotted animal with a very long neck is'

Baseline: ' giraffe.\nHypothesis:'

J minus final-layer oracle (not deployable): [' baby', ' babies', 'baby', ' kittens', ' elephants', ' elephant', '___', ' Baby', ' panda', ' dinosaur', ' lizard', ' turtles', ' newborn', ' kitten', ' snakes', ' puppies', ' chicks', ' peanuts', '-neck', '____', ' Babies', '________', 'Baby', ' bamboo', '_________', ' monkeys', ' puppy', ' pang', ' turtle', ' rabbits', ' toddler', ' zoo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

J-lens: [' roar', ' roaring', ' loud', ' sounds', '吼', '咆哮', ' lions', ' louder', ' sounded', ' Sounds', ' noises', ' screams', ' scream', ' tiger', ' audible', ' screaming', ' elephants', ' lion', ' loudly', '怒吼', '叫声', 'loud', ' chimpan', '________', ' yelling', ' elephant', '.\\', ' heard', ' applause', 'sounds', '老虎', ' noise']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

plain lens: [' sounded', 'wana', ' roar', '咆哮', 'opot', ' roaring', ' sav', '大王', '低沉', 'IKA', '吼', ' neigh', ' ogs', ' Sounds', '了一声', ' Afrika', 'jing', '........', ' الأسد', ' africa', ' sounds', '尖的', '几声', '异响', '喵', ' lions', 'OUNDS', '怒吼', '大吼', 'mane', '悶', ' accompanied']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

forecast: [' "', ' a', ' ', ' that', ' only', ' one', ' in', ' often', ' like', ' (', ' two', ' very', ' what', ' sounds', ' known', ' loud', ' iconic', ' r', ' usually', ' on', " '", ' it', ' no', ' different', ' being', ' as', '\n\n', ' -', ' matching', ' ch', ' called', ':']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

final-layer oracle (not deployable): [' a', ' roar', ' roaring', ' ro', ' grow', ' "', ' RO', ':', " '", ' called', ' Ro', ' similar', ' low', ' “', ' different', ' \\"', ' known', ' loud', ' often', ' lion', ' that', ' usually', ' very', ' an', ' described', ' heard', ' like', ' how', ' [', ' its', ' not', ' what']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

J minus plain lens: [' roar', ' roaring', ' loud', ' sounds', '吼', ' louder', ' lions', '咆哮', ' noises', ' screams', ' scream', ' tiger', ' audible', ' screaming', ' Sounds', ' elephants', ' loudly', ' lion', 'loud', ' chimpan', '________', '叫声', ' yelling', '.\\', ' elephant', ' applause', ' noise', '?\\', ' laughter', ' thunder', '___', '.\\"']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

J minus forecast: [' roar', ' roaring', ' loud', ' sounds', '吼', '咆哮', ' lions', ' louder', ' sounded', ' Sounds', ' noises', ' screams', ' scream', ' audible', ' elephants', ' tiger', ' loudly', '怒吼', '叫声', ' screaming', 'loud', ' lion', ' chimpan', '________', '.\\', ' applause', ' yelling', 'sounds', '老虎', ' claws', '.wav', '?\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sound made by the animal nicknamed the king of the jungle is'

Baseline: ' a roar.\nQuestion: What is'

J minus final-layer oracle (not deployable): [' roar', ' roaring', ' sounds', ' loud', '吼', '咆哮', ' lions', ' louder', ' sounded', ' Sounds', ' noises', ' screams', ' scream', ' audible', ' tiger', ' screaming', ' elephants', ' loudly', '怒吼', '叫声', 'loud', ' chimpan', '________', ' applause', '.\\', ' yelling', 'sounds', '老虎', ' claws', '.wav', '?\\', '___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

J-lens: [' frogs', ' frog', '青蛙', ' Frog', 'frog', '蝌', '蛙', ' tad', ' amphib', ' Ducks', ' trout', ' salam', ' bunny', '池塘', '呱呱', ' ducks', ' lizard', ' mosquitoes', ' puppies', ' kitten', ' rabbits', 'baby', ' Tad', ' aquatic', ' puppy', ' turtles', ' baby', ' babies', ' kittens', 'duck', ' rabbit', ' Splash']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

plain lens: [' tad', ' called', '叫', '呱呱', '呱', 'plash', '叫我', '跳水', '<<<<<<<', ' называется', 'called', ' territorial', '叫声', ' скорее', 'jie', 'frog', ' footprint', ' Waterproof', '蝌', '在水里', '跃进', 'HTML', ' frogs', '异响', '...', ' nai', ' leaps', ' commonly', 'ロード', 'ята', 'örn', ' splash']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

forecast: [' ', ' "', '\n\n', ' .', '\n', ' S', ' (', ' **', ' usually', ' G', ' D', ' Ch', ' -', ' a', ' K', ' its', ' one', ' “', ' P', ' ,', " '", ' found', ' __', ' ?', ' N', ' :', ' called', ' ...', ' in', ' typically', ' In', ' often']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

final-layer oracle (not deployable): [' frog', ' tad', ' a', ' Frog', ' to', ' "', " '", ' Tad', ' called', ' \\"', ' “', '...', ' known', ' T', ' not', ' Fro', ' new', ' frogs', ' To', ' turtle', ' t', ' F', ' baby', ' ‘', ' given', ' usually', ' also', ' lar', ' ...', ':', ' tiger', '\n']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

J minus plain lens: [' frogs', ' frog', '青蛙', ' Frog', 'frog', '蛙', '蝌', ' amphib', ' Ducks', ' salam', ' trout', ' bunny', ' ducks', ' lizard', ' mosquitoes', ' puppies', ' kitten', ' rabbits', ' puppy', ' turtles', 'baby', ' kittens', ' babies', ' baby', 'duck', ' rabbit', '池塘', ' duck', ' crab', ' Crab', ' nymph', ' toddlers']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

J minus forecast: [' frogs', ' frog', '青蛙', ' Frog', 'frog', '蝌', '蛙', ' tad', ' amphib', ' Ducks', ' salam', ' trout', ' bunny', '池塘', '呱呱', ' ducks', ' mosquitoes', ' lizard', ' puppies', ' kitten', 'baby', ' rabbits', ' Tad', ' aquatic', ' turtles', ' puppy', ' kittens', ' babies', 'duck', ' baby', ' Splash', ' rabbit']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The name for the young of the animal that croaks and jumps around ponds is'

Baseline: ' froglet.\nHypothesis:'

J minus final-layer oracle (not deployable): [' frogs', '青蛙', 'frog', '蛙', '蝌', ' amphib', ' Ducks', ' trout', ' salam', ' bunny', '池塘', '呱呱', ' ducks', ' mosquitoes', ' puppies', ' lizard', ' rabbits', 'baby', ' turtles', ' aquatic', ' kitten', ' puppy', ' kittens', ' babies', 'duck', ' Splash', ' rabbit', ' Crab', ' squirt', ' nymph', ' crab', ' Gecko']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

J-lens: [' ants', ' insects', '.\\', '___', ' six', '____', ' bees', ' spiders', ' typically', ').\\', ' four', '?\\', '蚂蚁', ' ___', '__', ' usually', ' five', ' twelve', ' seven', ' fours', '昆虫', ' eight', '蚁', ' ____', '...\\', '\\"\\', '。\\', ' __', '.\\"', ' divisible', '________', ' always']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

plain lens: [':number', '团团', ' Atta', 'instanc', ' licked', 'buzz', 'queen', 'conde', '[number', '惊人', 'digits', '(number', 'otope', ' divisible', 'води', ' ALWAYS', 'vester', ' _______,', 'worker', 'omers', '香甜', '通常为', 'Trail', 'shed', 'typically', '数', ' Panitia', '_routing', '头上的', '庄镇', 'nai', '分工']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

forecast: [' ', ' a', ' four', ' an', '\n\n', ' not', ' six', ' usually', ' __', ' one', ' no', '\n', ' (', ' .', ' three', ' ___', ' between', ' ____', ' "', ' :', ' always', ' two', ' what', ' exactly', ' only', ' about', ' very', ' \n\n', ' seven', ' five', ' **', ' P']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

final-layer oracle (not deployable): [' ', ' six', ' eight', ' __', ' usually', ' a', ' ______', ' not', ' ____', ' ___', ' always', ':', ' typically', '...', ' also', ' Six', ' (', ' an', ' **', ' four', ' different', ' generally', ' Ant', '\n', ' known', ' more', ' ?', ' about', ' equal', '\n\n', ' three', ' one']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

J minus plain lens: [' ants', ' insects', '.\\', ' six', '___', ' bees', '____', ' spiders', ' typically', ' four', ').\\', '?\\', '蚂蚁', '__', ' ___', ' usually', ' five', ' twelve', ' seven', ' fours', ' eight', '昆虫', '蚁', ' ____', '...\\', '\\"\\', '。\\', '.\\"', ' __', ' always', '________', ' butterflies']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

J minus forecast: [' ants', ' insects', '.\\', '___', ' six', ' bees', '____', ' spiders', ' typically', ').\\', '?\\', '蚂蚁', '__', ' ___', ' twelve', ' five', ' fours', '昆虫', ' seven', ' eight', ' usually', '蚁', '...\\', ' ____', '\\"\\', '。\\', '.\\"', ' divisible', '(number', '________', ' butterflies', '__.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that makes honey is'

Baseline: ' 6.\nQuestion: How many'

J minus final-layer oracle (not deployable): [' ants', ' insects', '.\\', '___', '____', ' bees', ' spiders', ').\\', ' typically', ' four', '?\\', '蚂蚁', '__', ' ___', ' twelve', ' five', ' fours', ' seven', '昆虫', '蚁', '...\\', '\\"\\', '。\\', '.\\"', ' divisible', '(number', '________', ' butterflies', '__.', ' insect', '四条', '\\n']


## Fixed-set readout results

Joint pass means a hidden alias is found and all lexical words in the eight-token continuation are excluded. Correct-answer columns condition on an expected answer alias appearing. Neither proves internal reasoning.

### Current-layer methods

| method                             | joint↑   |   AUROC↑ | correct-answer joint↑   |
|:-----------------------------------|:---------|---------:|:------------------------|
| [J-lens](readout.json)             | 4/16     |    0.828 | 2/12                    |
| [J minus plain lens](readout.json) | 4/16     |    0.669 | 2/12                    |
| [J minus forecast](readout.json)   | 4/16     |    0.749 | 2/12                    |
| [plain lens](readout.json)         | 3/16     |    0.776 | 2/12                    |
| [forecast](readout.json)           | 0/16     |    0.706 | 0/12                    |

### Evaluation-only future-information controls

| method                                                      | joint↑   |   AUROC↑ | correct-answer joint↑   |
|:------------------------------------------------------------|:---------|---------:|:------------------------|
| [J minus final-layer oracle (not deployable)](readout.json) | 6/16     |    0.689 | 4/12                    |
| [final-layer oracle (not deployable)](readout.json)         | 1/16     |    0.773 | 0/12                    |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_093037_jlens-one-pass/run.md
