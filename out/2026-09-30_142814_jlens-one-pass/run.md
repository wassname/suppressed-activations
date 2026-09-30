---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: data/english_hidden_words_v4.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 17.52
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: Eight new English prompts fixed before inference, after the blinded v3 audit localized all seven J joint passes to geography. Test the unchanged primary J residual24/final-position/k32/prompt+greedy masks/output erasure0.5 on non-geography relations before modifying masking. Same prefix, generation cap and controls. These hidden labels are absent from English v1/v2/v3 targets, not necessarily from earlier translation prompts. Labels are hypothesized intermediates, not proof of use. All cases and wrong/unscorable answers remain. Common aliases are predeclared but incomplete; semantic input/output review remains separate from lexical scoring. No output-based replacement or filtering. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Historical cached continuations are regenerated with the same eight-token cap. Scoring definitions are unchanged. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                     | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:---------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| December  | J-lens                     | False         |           0.725926 |             2 |                      0 | False          | False        |
| December  | plain lens                 | False         |           0.542593 |         35042 |                   2477 | False          | False        |
| December  | end-pass J-lens            | True          |           0.866667 |             1 |             1000000000 | True           | True         |
| December  | end-pass plain24           | False         |           0.701852 |         35037 |             1000000000 | False          | False        |
| December  | end-pass plain27           | True          |           0.992593 |             2 |             1000000000 | True           | True         |
| December  | end-pass erased1 J-lens    | False         |           0.818519 |          7988 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 J-lens  | False         |           0.853704 |            71 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain24   | False         |           0.635185 |        163572 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain24 | False         |           0.662963 |        102410 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain27   | False         |           0.985185 |            34 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain27 | True          |           0.994444 |            23 |             1000000000 | True           | True         |
| Thursday  | J-lens                     | False         |           0.85098  |             1 |                      3 | False          | False        |
| Thursday  | plain lens                 | False         |           0.882353 |           478 |                  10923 | False          | False        |
| Thursday  | end-pass J-lens            | True          |           0.94902  |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass plain24           | False         |           0.909804 |           478 |             1000000000 | False          | False        |
| Thursday  | end-pass plain27           | True          |           0.964706 |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass erased1 J-lens    | False         |           0.862745 |           151 |             1000000000 | False          | False        |
| Thursday  | end-pass erased0.5 J-lens  | True          |           0.92549  |             3 |             1000000000 | True           | True         |
| Thursday  | end-pass erased1 plain24   | False         |           0.896078 |           718 |             1000000000 | False          | False        |
| Thursday  | end-pass erased0.5 plain24 | False         |           0.907843 |           577 |             1000000000 | False          | False        |
| Thursday  | end-pass erased1 plain27   | True          |           0.939216 |             9 |             1000000000 | True           | True         |
| Thursday  | end-pass erased0.5 plain27 | True          |           0.95098  |             7 |             1000000000 | True           | True         |
| autumn    | J-lens                     | False         |           0.656471 |             6 |                      0 | False          | False        |
| autumn    | plain lens                 | False         |           0.685882 |           154 |                      5 | False          | False        |
| autumn    | end-pass J-lens            | True          |           0.934118 |             2 |             1000000000 | True           | False        |
| autumn    | end-pass plain24           | False         |           0.901176 |           153 |             1000000000 | False          | False        |
| autumn    | end-pass plain27           | True          |           0.985882 |             9 |             1000000000 | True           | True         |
| autumn    | end-pass erased1 J-lens    | False         |           0.924706 |           437 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 J-lens  | False         |           0.934118 |            50 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain24   | False         |           0.882353 |          6427 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 plain24 | False         |           0.890588 |          1127 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain27   | True          |           0.985882 |            66 |             1000000000 | False          | True         |
| autumn    | end-pass erased0.5 plain27 | True          |           0.985882 |            23 |             1000000000 | True           | True         |
| apple     | J-lens                     | False         |           0.6125   |            25 |                      0 | False          | False        |
| apple     | plain lens                 | False         |           0.711111 |          1374 |                     86 | False          | False        |
| apple     | end-pass J-lens            | True          |           0.894444 |            23 |             1000000000 | True           | False        |
| apple     | end-pass plain24           | False         |           0.983333 |          1367 |             1000000000 | False          | False        |
| apple     | end-pass plain27           | True          |           1        |            27 |             1000000000 | True           | False        |
| apple     | end-pass erased1 J-lens    | True          |           0.891667 |             9 |             1000000000 | True           | True         |
| apple     | end-pass erased0.5 J-lens  | True          |           0.9      |            11 |             1000000000 | True           | False        |
| apple     | end-pass erased1 plain24   | False         |           0.972222 |          1898 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain24 | False         |           0.977778 |          1646 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain27   | True          |           1        |             8 |             1000000000 | True           | True         |
| apple     | end-pass erased0.5 plain27 | True          |           1        |             7 |             1000000000 | True           | True         |
| violin    | J-lens                     | True          |           0.854396 |             0 |                   3354 | True           | True         |
| violin    | plain lens                 | False         |           0.892857 |           304 |                    951 | False          | False        |
| violin    | end-pass J-lens            | True          |           0.854396 |             0 |                   3352 | True           | True         |
| violin    | end-pass plain24           | False         |           0.892857 |           302 |                    949 | False          | False        |
| violin    | end-pass plain27           | True          |           0.972528 |             2 |                     12 | False          | False        |
| violin    | end-pass erased1 J-lens    | True          |           0.876374 |             1 |                   3314 | True           | True         |
| violin    | end-pass erased0.5 J-lens  | True          |           0.865385 |             0 |                   3184 | True           | True         |
| violin    | end-pass erased1 plain24   | False         |           0.899725 |           646 |                   1033 | False          | False        |
| violin    | end-pass erased0.5 plain24 | False         |           0.901099 |           450 |                    963 | False          | False        |
| violin    | end-pass erased1 plain27   | True          |           0.975275 |             2 |                     10 | False          | False        |
| violin    | end-pass erased0.5 plain27 | True          |           0.972528 |             1 |                     11 | False          | False        |
| Hamlet    | J-lens                     | False         |           0.842424 |            98 |                      0 | False          | False        |
| Hamlet    | plain lens                 | False         |           0.712121 |          2291 |                      2 | False          | False        |
| Hamlet    | end-pass J-lens            | False         |           0.912121 |            96 |                      0 | False          | False        |
| Hamlet    | end-pass plain24           | False         |           0.751515 |          2291 |                      2 | False          | False        |
| Hamlet    | end-pass plain27           | False         |           0.818182 |           179 |                      2 | False          | False        |
| Hamlet    | end-pass erased1 J-lens    | False         |           0.878788 |           330 |                      0 | False          | False        |
| Hamlet    | end-pass erased0.5 J-lens  | False         |           0.884848 |           155 |                      0 | False          | False        |
| Hamlet    | end-pass erased1 plain24   | False         |           0.739394 |          2479 |                      3 | False          | False        |
| Hamlet    | end-pass erased0.5 plain24 | False         |           0.743939 |          2345 |                      3 | False          | False        |
| Hamlet    | end-pass erased1 plain27   | False         |           0.80303  |           361 |                      2 | False          | False        |
| Hamlet    | end-pass erased0.5 plain27 | False         |           0.812121 |           257 |                      2 | False          | False        |
| hydrogen  | J-lens                     | False         |           0.647059 |           129 |                     17 | False          | False        |
| hydrogen  | plain lens                 | False         |           0.372549 |         30834 |                   2056 | False          | False        |
| hydrogen  | end-pass J-lens            | False         |           0.69281  |           129 |                     17 | False          | False        |
| hydrogen  | end-pass plain24           | False         |           0.601307 |         30831 |                   2055 | False          | False        |
| hydrogen  | end-pass plain27           | False         |           0.620915 |          2126 |                      0 | False          | False        |
| hydrogen  | end-pass erased1 J-lens    | False         |           0.705882 |           220 |                     28 | False          | False        |
| hydrogen  | end-pass erased0.5 J-lens  | False         |           0.705882 |           169 |                     22 | False          | False        |
| hydrogen  | end-pass erased1 plain24   | False         |           0.601307 |         34827 |                   2672 | False          | False        |
| hydrogen  | end-pass erased0.5 plain24 | False         |           0.601307 |         32356 |                   2330 | False          | False        |
| hydrogen  | end-pass erased1 plain27   | False         |           0.633987 |          4697 |                      0 | False          | False        |
| hydrogen  | end-pass erased0.5 plain27 | False         |           0.627451 |          3037 |                      0 | False          | False        |
| triangle  | J-lens                     | True          |           0.990476 |             6 |                    386 | True           | True         |
| triangle  | plain lens                 | True          |           1        |           103 |                  91628 | False          | True         |
| triangle  | end-pass J-lens            | True          |           0.990476 |             6 |                    386 | True           | True         |
| triangle  | end-pass plain24           | True          |           1        |           103 |                  91628 | False          | True         |
| triangle  | end-pass plain27           | True          |           1        |             7 |                   3462 | True           | True         |
| triangle  | end-pass erased1 J-lens    | True          |           0.998095 |             6 |                   3417 | True           | True         |
| triangle  | end-pass erased0.5 J-lens  | True          |           0.994286 |             6 |                   1117 | True           | True         |
| triangle  | end-pass erased1 plain24   | True          |           1        |            84 |                  38531 | False          | True         |
| triangle  | end-pass erased0.5 plain24 | True          |           1        |            94 |                  61992 | False          | True         |
| triangle  | end-pass erased1 plain27   | True          |           1        |             7 |                  12523 | True           | True         |
| triangle  | end-pass erased0.5 plain27 | True          |           1        |             7 |                   6599 | True           | True         |

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

J-lens: [' January', ' Months', ' December', ' February', ' months', '月份', 'Months', 'months', ' November', ' Year', 'January', ' April', '-month', ' Januari', '月份的', ' Calendar', ' October', '次年', ' Monthly', ' calendar', ' September', 'calendar', 'February', ' winter', ' Ramadan', 'December', ' Spring', '_month', ' Winter', ' Easter', '(month', ' July']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

plain lens: [' called', '眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', '志愿服务队', ' наступ', ' kolej', ' называется', '問わず', 'ถัด', '人も多い', 'FOUND', 'orate', 'called', ' Fucking', '{name', 'ullo', ' kalt', '新社', '下一章', ' ули', '球迷们', 'CALE', 'Called', '.getMonth', ' appelé', '谤', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass J-lens: [' Months', ' December', ' February', ' months', '月份', 'Months', 'months', ' November', ' Year', '-month', ' April', ' Januari', '月份的', ' Calendar', ' October', '次年', ' Monthly', ' calendar', ' September', 'February', 'calendar', ' winter', ' Ramadan', 'December', ' Spring', ' Winter', '_month', ' Easter', '(month', ' July', ' year', ' called']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass plain24: [' called', '眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', '志愿服务队', ' наступ', ' kolej', ' называется', '問わず', 'ถัด', '人も多い', 'FOUND', 'orate', 'called', ' Fucking', '{name', 'ullo', ' kalt', '新社', '下一章', ' ули', '球迷们', 'CALE', 'Called', '.getMonth', ' appelé', '谤', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass plain27: [' called', 'called', '_Dec', ' December', ' Januari', ' termed', ' Boxing', ' называется', ' usually', 'Called', 'usually', 'December', '眯眯', '称为', ' Ро', '-Jan', 'winter', '展望', '谓之', ' typically', '新的一年', 'uary', ' Dec', '____', ' referred', ' appelé', 'known', 'áno', ' জান', ' known', ' ژ', '.Dec']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased1 J-lens: [' Months', '.\\', '...', 'Months', '____', ' months', ' called', '月份', '__.', 'months', '___', '.*', '________', ' Calendar', '....', '__', ' Next', ' Year', ' calendar', '\\.', '...*', '...\\', 'calendar', 'next', '_____', '.…', ' next', '日历', '.[', '…', '闰', 'Next']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased0.5 J-lens: [' Months', ' months', 'Months', '月份', 'months', ' Year', ' Calendar', '-month', '.\\', ' called', '____', ' calendar', '次年', 'calendar', '月份的', ' Monthly', '___', ' Ramadan', '__.', '日历', ' Next', ' Spring', '...\\', ' Easter', '闰', '________', '...', '(month', ' bulan', '.…', '...*', '_month']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased1 plain24: [' called', 'رداد', ' termed', '眯眯', ' Folg', ' preceded', ' kolej', ' invariably', ' наступ', 'unie', ' называется', 'ถัด', ' Fucking', '志愿服务队', 'called', '問わず', 'FOUND', '人も多い', 'ullo', '{name', 'orate', ' ули', '下一章', '球迷们', ' appelé', ' kalt', 'CALE', 'Called', '说过', '谤', '新社', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased0.5 plain24: [' called', '眯眯', 'رداد', ' Folg', ' termed', 'unie', ' preceded', ' invariably', ' kolej', ' наступ', ' называется', '志愿服务队', 'ถัด', '問わず', '人も多い', 'FOUND', ' Fucking', 'called', 'orate', '{name', 'ullo', ' ули', ' kalt', '下一章', ' appelé', '球迷们', '新社', 'CALE', 'Called', '谤', '说过', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased1 plain27: [' called', 'called', ' termed', '_Dec', ' называется', '____', ' Boxing', 'Called', 'usually', '...', ' usually', '称为', '展望', ' referred', ' appelé', ' typically', '眯眯', 'known', ' Ро', '________', ' known', '谓之', 'áno', '{}.', 'typically', 'BufferSize', ' معمول', ' appel', 'อธิ', ' Called', '_____', 'spy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass erased0.5 plain27: [' called', 'called', '_Dec', ' termed', ' называется', ' Boxing', 'Called', 'usually', ' usually', '称为', '____', '展望', '眯眯', ' referred', ' typically', ' Ро', ' appelé', '谓之', 'known', ' Januari', 'áno', ' known', '...', ' Dec', '新的一年', 'typically', 'BufferSize', '{}.', '________', ' معمول', 'spy', ' ژ']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

J-lens: [' Tuesday', ' Thursday', ' Monday', ' Saturday', ' Friday', ' Wednesday', ' Sunday', ' Mondays', ' tomorrow', ' Tues', ' monday', ' Thurs', ' Fridays', 'Monday', ' Thanksgiving', ' weekend', ' Sundays', ' Saturdays', ' Days', 'Tuesday', ' weekdays', ' days', ' weekends', ' Christmas', 'Thursday', ' Halloween', ' morning', ' today', 'Saturday', ' yesterday', 'days', ' friday']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

plain lens: [' called', 'always', 'called', ' الني', ' preceded', '除恶', 'pras', '现代的', '为己', 'lands', ' Dici', 'eve', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', 'leid', '诞辰', 'wand', 'svc', 'ủy', 'IVERY', '酬', '动感', 'forth', ' Lapangan', ' supposed', '又快', '个大', ' lucr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass J-lens: [' Tuesday', ' Thursday', ' Monday', ' Saturday', ' Wednesday', ' Sunday', ' Mondays', ' tomorrow', ' Tues', ' monday', 'Monday', ' Thurs', ' Thanksgiving', ' weekend', ' Saturdays', ' Sundays', ' Days', 'Tuesday', ' weekdays', ' weekends', ' days', ' Christmas', 'Thursday', ' Halloween', ' morning', 'Saturday', ' today', ' yesterday', 'days', ' called', ' sunday', 'Wednesday']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass plain24: [' called', 'always', 'called', ' الني', ' preceded', '除恶', 'pras', '现代的', '为己', 'lands', ' Dici', 'eve', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', 'leid', '诞辰', 'wand', 'svc', 'ủy', 'IVERY', '酬', '动感', 'forth', ' Lapangan', ' supposed', '又快', '个大', ' lucr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass plain27: [' среда', ' Wednesday', ' Thursday', ' Thurs', 'called', ' wed', 'uesday', ' Чет', 'Monday', ' Monday', ' Wed', ' Thu', ' called', ' среду', 'FR', 'Wednesday', 'Thursday', ' Tuesday', '除恶', 'gios', 'always', '_FR', '금', '又快', 'Tuesday', 'сре', '饱和度', 'nesday', ' Saturday', 'agna', ' среды', 'bru']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased1 J-lens: [' called', '____', '___', ' Days', ' days', '.\\', ' Iceland', ' Thanksgiving', '________', '...', '称为', ' tomorrow', ' Halloween', '_____', 'days', ' daylight', ' Christmas', '__', ' today', ' ____', ' holidays', '....', '这一天', '_________', ' ______', ' Denmark', 'called', ' Norway', '__.', ' daytime', '北欧', ' weekdays']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased0.5 J-lens: [' Tuesday', ' Monday', ' tomorrow', ' Days', ' Thursday', ' Thanksgiving', ' called', ' Saturday', ' days', ' Mondays', ' Wednesday', ' Sunday', ' Halloween', ' Christmas', '____', ' weekdays', 'days', ' Iceland', ' weekend', ' today', ' Tues', ' weekends', ' Sundays', ' daylight', ' monday', '这一天', ' Thurs', ' morning', ' Saturdays', ' Tomorrow', '___', ' holidays']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased1 plain24: [' called', 'always', 'called', ' الني', ' preceded', '除恶', '现代的', 'pras', '为己', 'lands', 'eve', ' Dici', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', 'wand', 'leid', 'svc', 'ủy', '诞辰', '酬', 'IVERY', '动感', 'forth', ' supposed', ' Lapangan', '又快', '个大', '开放']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased0.5 plain24: [' called', 'always', 'called', ' الني', ' preceded', '除恶', 'pras', '现代的', '为己', 'lands', ' Dici', 'eve', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', '诞辰', 'wand', 'IVERY', 'leid', 'svc', '酬', 'ủy', '动感', 'forth', ' supposed', ' Lapangan', '又快', '个大', ' lucr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased1 plain27: ['...', 'called', ' среда', ' wed', ' called', ' Чет', 'always', 'gios', 'FR', ' Thu', ' Wed', '又快', '除恶', '금', ' Þ', 'NOT', 'agna', '饱和度', ' среду', '称为', 'ued', 'bru', '.....', ' thu', 'rides', 'sson', '瑞典', 'vat', ' среды', 'mon', '_FR', '赔']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass erased0.5 plain27: ['called', ' среда', ' wed', ' Чет', ' called', '...', ' Wed', ' Thu', 'FR', 'always', 'gios', ' среду', '除恶', 'uesday', ' Thurs', '又快', '금', '饱和度', 'agna', 'NOT', '_FR', ' Þ', 'bru', 'ued', 'сре', ' среды', 'rides', '称为', ' thu', '瑞典', 'Thứ', 'Monday']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

J-lens: [' winter', ' summer', 'winter', ' seasons', ' winters', ' Winter', ' autumn', '冬季', ' rainy', ' spring', ' warmer', '春季', ' summers', 'summer', '___', ' Summer', ' seasonal', '季节', 'Winter', '__.', '____', ' Spring', '夏季', '雨季', '冬天', ' Autumn', ' primavera', '-season', '...\\', ' called', ' Seasons', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

plain lens: [' preceded', ' наступ', 'spring', ' called', '紧接着', ' seasons', 'winter', ' invariably', '到来', 'called', '是一年', ' называется', 'rollers', 'orate', 'unno', '.navigationBar', 'summer', ' termed', '鸟语', ' قائ', ' followed', "').'", 'nam', '个字', '{name', 'dess', '問わず', '叫做', 'のことを', ' always', 'angat', 'beg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass J-lens: [' summer', ' seasons', ' autumn', '冬季', ' rainy', ' spring', ' warmer', '春季', ' summers', 'summer', '___', ' seasonal', ' Summer', '季节', '__.', ' Spring', '____', '雨季', '夏季', '冬天', ' Autumn', ' primavera', '-season', '...\\', ' Seasons', ' called', '________', 'spring', '春天', ' drought', '旺季', ' colder']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass plain24: [' preceded', ' наступ', 'spring', ' called', '紧接着', ' seasons', ' invariably', '到来', 'called', ' называется', '是一年', 'rollers', 'orate', '.navigationBar', 'unno', ' termed', 'summer', "').'", ' قائ', '鸟语', ' followed', 'nam', '个字', '{name', '問わず', 'dess', 'のことを', '叫做', ' always', 'angat', '休止', 'beg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass plain27: ['spring', 'Spring', 'pring', ' spring', ' Spring', ' summer', 'summer', ' springs', '春', ' autumn', '.spring', ' verano', ' primavera', ' Summer', '春天', '春意', 'Summer', ' наступ', 'fall', '\tSpring', ' summers', ' called', ' printemps', '.Spring', '春的', ' verão', '夏', ' preceded', 'ommer', ' FALL', ' vinter', '春季']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased1 J-lens: ['___', '____', '__', '________', '__.', ' called', '.\\', '...', '_____', '...\\', '…', ' ___', '_________', ' ________', ' warmer', ' ______', ' rainy', ' ____', ' __', '_.', ' seasons', '叫', '叫做', '____________', '.…', 'called', '__:', '……', '称为', '__)', ' _____', '\\.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased0.5 J-lens: ['___', '____', ' seasons', '__.', ' rainy', '________', ' warmer', ' called', '__', '...\\', '.\\', '_____', ' ___', '_________', ' ________', '季节', ' ____', '雨季', ' ______', ' summers', '_.', '叫做', ' drought', '__:', '____________', ' __', '__)', '.…', '春季', ' summer', '...', ' Seasons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased1 plain24: [' preceded', ' наступ', ' called', '紧接着', 'called', '到来', ' invariably', ' называется', '...', 'nam', ' followed', 'orate', '鸟语', "').'", ' termed', '名', ' قائ', 'spring', '是一年', '叫做', 'beg', '{name', ' always', 'dess', ' analogous', '幕', 'unno', '个字', 'のことを', '.navigationBar', ' typically', ' characterized']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased0.5 plain24: [' preceded', ' наступ', ' called', '紧接着', 'spring', ' invariably', '到来', 'called', ' называется', ' seasons', 'orate', ' termed', '是一年', ' followed', "').'", '鸟语', 'nam', ' قائ', 'rollers', 'unno', '.navigationBar', '叫做', '个字', '{name', 'dess', ' always', 'beg', '名', 'のことを', '幕', '問わず', '...']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased1 plain27: ['spring', 'pring', 'Spring', ' Spring', ' spring', ' springs', ' called', ' наступ', ' preceded', '.spring', ' characterized', '春', 'fall', 'called', '春意', '...', ' termed', '\tSpring', ' primavera', ' الرب', 'ommer', 'ใบ', '.Spring', '上传者', 'othermal', ' вес', ' называется', 'unno', '叫', ' FALL', '.Sum', 'omers']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass erased0.5 plain27: ['spring', 'Spring', 'pring', ' spring', ' Spring', ' springs', '春', ' called', ' наступ', '.spring', 'summer', '春意', 'fall', ' preceded', ' primavera', ' summer', ' verano', '\tSpring', ' characterized', '.Spring', '春天', 'ommer', ' summers', ' autumn', ' printemps', 'called', '夏', ' Summer', '春的', ' verão', ' الرب', ' FALL']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

J-lens: [' red', ' purple', '红色', ' pink', ' blue', 'pink', ' black', ' green', ' Purple', ' violet', ' strawberry', 'purple', ' poisonous', ' Pink', ' yellow', ' orange', '(red', ' berries', '蓝色', ' rouge', 'red', '红色的', ':red', ' strawberries', '粉红色', ' blonde', ' crimson', ' apple', '_red', 'blue', '-red', ' brown']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

plain lens: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', 'aches', '红色', '惨叫', 'atrices', "').'", '分享到朋友圈', '史蒂', 'canf', '_red', 'мали', 'attended', 'シャー', '目瞪', 'pozn', '빨', '永远的', '_integration', '对白', 'ряда', ' })).', '白金', '红红的', ' Bái', 'maid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass J-lens: [' purple', '红色', ' pink', ' blue', 'pink', ' black', ' green', ' Purple', ' violet', ' strawberry', 'purple', ' Pink', ' poisonous', ' yellow', '(red', ' orange', ' berries', '蓝色', ' rouge', ':red', '红色的', ' strawberries', '粉红色', ' blonde', ' apple', ' crimson', '_red', 'blue', '-red', ' brown', ' красный', ' Strawberry']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass plain24: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', 'aches', '红色', '惨叫', 'atrices', "').'", '分享到朋友圈', '史蒂', 'canf', '_red', 'мали', 'attended', 'シャー', '目瞪', 'pozn', '빨', '永远的', '_integration', '对白', 'ряда', ' })).', '白金', '红红的', ' Bái', 'maid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass plain27: ['红色', ' poisoning', '_red', ':red', '红了', '红', '中毒', ' красный', '紅色', '.apple', '紅', '红线', ' poisonous', '.red', '致命', ' rojo', '红红的', '(red', '红梅', '绯', '毒', 'мали', '-red', ' الأحمر', '的红', ' đỏ', '红色的', 'apple', '红的', '通红', 'Apple', ' apple']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased1 J-lens: [' poisonous', ' berries', ' strawberry', ' strawberries', ' purple', 'pink', ' poisoning', ' Purple', ' Strawberry', '...**', '白雪', ' apple', ' violet', ' berry', ' pink', ' brunette', ' Apfel', ' Pink', ' blonde', ' Roses', 'purple', ' BLACK', '__.', 'apple', ' roses', ' apples', '.".', ' lipstick', '».**', ').\\', 'berries', '/color']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased0.5 J-lens: [' purple', ' poisonous', ' pink', 'pink', ' berries', ' strawberry', ' Purple', ' violet', ' strawberries', ' Pink', 'purple', ' apple', ' Strawberry', ' blue', ' blonde', '蓝色', ' black', '粉红色', ' poisoning', ' berry', ' BLACK', '白雪', '红色', ' green', ' apples', ' brunette', 'Pink', ' orange', ' yellow', ' roses', ' rouge', ' Roses']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased1 plain24: [' Eventi', '眯眯', '红颜', 'меется', '全文数据库', '目瞪', 'bourg', '分享到朋友圈', 'canf', '惨叫', "').'", 'atrices', 'aches', 'シャー', ' Bái', 'pozn', ' **)&', '頂けます', 'dling', '永远的', ' })).', '史蒂', '_integration', 'будьте', 'ряда', 'мали', '对白', '😀', 'angsa', ' эксперти', 'attended', '-Nazi']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased0.5 plain24: ['红颜', ' Eventi', 'меется', '眯眯', '全文数据库', 'bourg', 'canf', '分享到朋友圈', 'atrices', '惨叫', "').'", '目瞪', 'aches', '史蒂', 'シャー', 'pozn', 'мали', ' Bái', ':red', '对白', 'attended', ' })).', '_integration', '永远的', ' **)&', 'ряда', '白金', 'dling', '頂けます', 'angsa', ' эксперти', '金奖']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased1 plain27: [' poisoning', '中毒', ' poisonous', '致命', '.apple', 'мали', '毒', ' Apfel', '.po', ' APPLE', '致命的', 'apple', ' Eventi', 'pozn', '-po', 'prs', 'abelle', 'Apple', 'レード', '臉色', '解毒', '蘋', '[].', '毒药', '苹果', '{name', '应有尽有', '白雪', ' ябло', '全文数据库', '{}".', '毒性']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass erased0.5 plain27: [' poisoning', '中毒', ' poisonous', '.apple', '致命', '毒', 'мали', 'apple', '致命的', '-po', '.po', ' Apfel', ' APPLE', 'Apple', 'pozn', '解毒', '绯', ':red', 'abelle', '蘋', '苹果', 'レード', ' Eventi', 'prs', '白雪', '红梅', ' apple', '毒性', '臉色', '红了', '毒药', '[].']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

J-lens: [' violin', ' Piano', ' piano', ' called', ' known', ' composed', ' comprised', '钢琴', ' Guitar', ' analogous', '.\\', ' guitar', ' similar', ' guitars', ' percussion', '提琴', ' flute', '乐器', ' instrumental', '...\\', ' identical', ' musicians', ' jazz', ' Jazz', ' Instruments', ' Mozart', ' trumpet', ' auditory', ':\\', '.\\"', 'ดนตรี', ' consisted']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

plain lens: ['ходу', '木有', ' theirs', ' comprised', ' descended', "').'", '폐', ' percussion', '除外', '_pipe', 'ungi', '很好奇', 'dataProvider', 'više', '其中之一', '吵闹', '创建于', 'aner', '树人', 'eppe', 'adă', 'emies', ' spok', ' المكان', 'members', '教体', '_family', 'pipe', 'เดียวกับ', '那般', 'stadt', '小编为大家整理的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass J-lens: [' violin', ' Piano', ' piano', ' called', ' known', ' composed', ' comprised', '钢琴', ' Guitar', ' analogous', '.\\', ' guitar', ' similar', ' guitars', ' percussion', '提琴', ' flute', '乐器', ' instrumental', '...\\', ' identical', ' musicians', ' jazz', ' Jazz', ' Instruments', ' Mozart', ' trumpet', ' auditory', ':\\', '.\\"', 'ดนตรี', ' consisted']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass plain24: ['ходу', '木有', ' comprised', ' descended', "').'", '除外', '폐', ' percussion', 'dataProvider', '_pipe', 'ungi', '很好奇', 'više', '其中之一', '吵闹', 'aner', '创建于', '树人', 'eppe', ' spok', 'adă', 'emies', ' المكان', 'members', '教体', '那般', '_family', 'pipe', 'เดียวกับ', 'stadt', 'ốn', '小编为大家整理的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass plain27: [' instruments', ' instrumental', ' violin', ' Instruments', ' percussion', 'Viol', ' viol', '键盘', 'struments', ' instrumentos', '弦', ' flute', 'strings', 'keyboard', ' instrumentation', ' trumpet', '小提琴', '提琴', ' piano', ' drums', ' Viol', ' sax', 'pipe', ' Piano', ' viola', '-viol', 'wind', 'viol', ' trump', ' guitars', 'стру', 'string']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased1 J-lens: [' Piano', ' violin', ' piano', ' comprised', '钢琴', ' Guitar', ' guitars', '提琴', ' composed', ' analogous', ' guitar', ' percussion', '乐器', '...\\', ' flute', ' called', '.\\', 'ดนตรี', ' Instruments', ' known', ' musicians', ' instrumental', '.\\"', ' jazz', ' Mozart', ' trumpet', ' consisted', ' Jazz', ' auditory', '古筝', ').\\', ' similar']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased0.5 J-lens: [' violin', ' Piano', ' piano', ' comprised', '钢琴', ' Guitar', ' called', ' composed', ' guitars', ' analogous', ' known', ' guitar', '提琴', '.\\', ' percussion', ' flute', '乐器', '...\\', ' similar', ' instrumental', ' musicians', ' Instruments', 'ดนตรี', ' jazz', ' Jazz', ' trumpet', ' Mozart', '.\\"', ' auditory', ' identical', ' consisted', '古筝']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased1 plain24: ['ходу', '木有', ' comprised', "').'", ' descended', ' spok', 'više', '폐', 'adă', 'dataProvider', '很好奇', '除外', 'ungi', 'eppe', '頂けます', '_pipe', ' percussion', '树人', ' Eventi', 'aner', 'conde', '其中之一', '准确性和合法性', '创建于', '吵闹', ' гале', 'に行ってきました', ' pressi', '教体', '小编为大家整理的', 'GRP', '树一']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased0.5 plain24: ['ходу', '木有', ' comprised', ' descended', "').'", '폐', 'više', ' spok', '除外', '_pipe', ' percussion', '很好奇', 'ungi', 'dataProvider', 'adă', 'eppe', '吵闹', '创建于', '树人', '其中之一', 'aner', 'emies', '教体', ' Eventi', '頂けます', ' المكان', ' pressi', '小编为大家整理的', 'members', '树一', 'conde', 'GRP']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased1 plain27: [' instruments', ' Instruments', ' violin', ' instrumental', ' percussion', 'Viol', ' viol', '键盘', 'struments', ' instrumentos', 'strings', '弦', ' flute', '提琴', 'keyboard', '小提琴', ' instrumentation', '-viol', ' viola', ' trumpet', 'pipe', ' drums', ' Viol', ' Piano', ' آلات', ' sax', 'viol', 'wind', ' piano', 'стру', ' guitars', ' trump']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass erased0.5 plain27: [' instruments', ' violin', ' instrumental', ' Instruments', ' percussion', 'Viol', ' viol', '键盘', 'struments', ' instrumentos', '弦', 'strings', ' flute', 'keyboard', ' instrumentation', '提琴', ' trumpet', '小提琴', '-viol', ' drums', 'pipe', ' Viol', ' viola', ' sax', ' piano', ' Piano', 'viol', 'wind', ' trump', 'стру', ' آلات', ' guitars']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

J-lens: [' Shakespeare', ' William', ' Robert', ' playwright', ' Henry', ' Elizabeth', 'akespeare', '莎士比亚', ' Dickens', ' Richard', ' John', ' Charles', ' George', ' Aristotle', ' Harry', ' Julius', ' Edward', ' Henrik', ' Shakespe', ' Jane', ' Margaret', ' Romeo', ' Stephen', ' Samuel', ' Christopher', ' Edmund', ' James', ' novelist', ' Daniel', ' Thomas', ' Tolkien', ' Nobel']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

plain lens: [' credited', '虚构', ' Shakespeare', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' supposed', ' fiction', ' unbek', 'ulis', 'ργο', ' playwright', '桂冠', '原作者', ' corpus', ' مسرح', ' spis', ' spok', '屠', 'igin', '不详', '推理', 'stad', 'っきり', '伟大的', ' canon', '托']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass J-lens: [' Shakespeare', ' Robert', ' playwright', ' Henry', ' Elizabeth', 'akespeare', '莎士比亚', ' Dickens', ' Richard', ' John', ' Charles', ' George', ' Harry', ' Aristotle', ' Julius', ' Henrik', ' Edward', ' Shakespe', ' Jane', ' Romeo', ' Margaret', ' Stephen', ' Samuel', ' Christopher', ' novelist', ' Edmund', ' James', ' Thomas', ' Daniel', ' Tolkien', ' Nobel', ' Matthew']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass plain24: [' credited', '虚构', ' Shakespeare', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' supposed', ' fiction', ' unbek', 'ulis', 'ργο', ' playwright', '桂冠', '原作者', ' corpus', ' مسرح', ' spis', ' spok', '屠', 'igin', '不详', '推理', 'stad', 'っきり', '伟大的', ' canon', '托']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass plain27: ['akespeare', ' playwright', ' Shakespeare', ' Shakespe', '莎士比亚', ' مسرح', '莎士', ' شك', ' credited', ' dramat', ' onstage', '-play', ' dram', '舞台上', '屠', ' المسرح', ' Plays', 'ælde', ' shakes', ' traged', '鲨', '署', ' teatrale', '劇', '/play', ' tragedia', '羽', ' lago', ' autoria', ' 셰', ' théâtre', 'plays']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased1 J-lens: [' Shakespeare', ' playwright', ' Dickens', 'akespeare', ' Shakespe', '莎士比亚', ' novelist', ' Aristotle', ' Tolkien', ' Henrik', ' Rowling', ' Romeo', ' Dumbledore', ' Unknown', ' Claud', ' Snape', '________', ' Elizabeth', 'unknown', ' authored', '____', ' Nobel', ' Gutenberg', ' Mozart', ' Edmund', '___', ' Denmark', ' Anonymous', ' Homer', '丹麦', ' Jane', ' unknown']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased0.5 J-lens: [' Shakespeare', ' playwright', 'akespeare', ' Dickens', '莎士比亚', ' Elizabeth', ' Shakespe', ' Aristotle', ' Robert', ' Henrik', ' novelist', ' Romeo', ' Tolkien', ' Henry', ' Richard', ' Julius', ' Rowling', ' Jane', ' Dumbledore', ' Claud', ' Edmund', ' Unknown', ' Nobel', ' Harry', ' John', '________', ' Denmark', 'unknown', ' Margaret', ' Marcus', ' Homer', ' Duncan']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased1 plain24: [' credited', '虚构', '佚', ' Shakespeare', ' greve', 'akespeare', '…]', ' السير', ' fictional', ' autoria', 'orden', ' fiction', ' supposed', 'ulis', ' unbek', 'ργο', ' playwright', '桂冠', '原作者', ' spis', ' corpus', ' مسرح', ' spok', 'igin', '屠', '不详', 'stad', '托', '推理', '頂けます', 'っきり', '...(']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased0.5 plain24: [' credited', '虚构', '佚', ' Shakespeare', ' greve', 'akespeare', '…]', ' fictional', ' السير', ' autoria', 'orden', ' fiction', ' supposed', ' unbek', 'ulis', 'ργο', '原作者', ' playwright', '桂冠', ' corpus', ' spis', ' مسرح', ' spok', 'igin', '屠', '不详', 'stad', 'っきり', '推理', '托', '頂けます', ' canon']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased1 plain27: ['akespeare', ' playwright', ' Shakespe', ' Shakespeare', '莎士比亚', ' onstage', ' مسرح', ' شك', '莎士', ' المسرح', ' dramat', '-play', ' credited', ' dram', ' Plays', 'ælde', '舞台上', '屠', ' traged', '鲨', ' shakes', '署', ' teatrale', ' autoria', ' lago', '羽', '劇', ' tragedia', ' 셰', '/play', 'plays', 'icide']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass erased0.5 plain27: ['akespeare', ' playwright', ' Shakespeare', ' Shakespe', '莎士比亚', ' مسرح', ' شك', '莎士', ' onstage', ' dramat', '-play', ' credited', ' المسرح', ' dram', ' Plays', '舞台上', '屠', 'ælde', ' shakes', ' traged', '鲨', '署', ' teatrale', '/play', ' autoria', '劇', '羽', ' lago', ' tragedia', ' 셰', ' théâtre', 'plays']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

J-lens: [' liquids', ' liquid', ' Liquid', '液态', 'liquid', ' vapor', '________', ' lique', ' Vapor', '__.', '___', ' gases', '液体', '_________', '____', '?\\', 'Liquid', ' gas', '_____', ' fluids', ' Gas', ' fluid', ' ________', ' Liqu', '____________', '...\\', '...**', '.\\', ' usually', '常温', ' Fluid', 'gas']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

plain lens: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', 'फल', '工作状态', ' liquids', '英文名称', ' usually', '固体', ' theirs', 'udiant', 'omers', ' состояния', ' quyển', 'otope', '[state', ' kwest', '常态', '.initState', ' газо', '通常为', 'liquid', ' invariably']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass J-lens: [' liquids', ' liquid', ' Liquid', '液态', 'liquid', ' vapor', '________', ' lique', ' Vapor', '__.', '___', ' gases', '液体', '_________', '____', '?\\', 'Liquid', ' gas', '_____', ' fluids', ' Gas', ' fluid', ' ________', ' Liqu', '____________', '...\\', '...**', '.\\', ' usually', '常温', ' Fluid', 'gas']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass plain24: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', 'फल', '工作状态', ' liquids', '英文名称', ' usually', '固体', ' theirs', 'udiant', 'omers', ' состояния', ' quyển', 'otope', '[state', ' kwest', '常态', '.initState', ' газо', '通常为', 'liquid', ' invariably']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass plain27: [' gas', '气体', ' gases', 'gas', '的气体', ' Gas', '气体的', '气', 'Gas', '固态', '_gas', ' газо', '固体', ' газ', 'liquid', ' газа', 'solid', ' gás', ' solid', '液态', ' liquid', ' GAS', ' الغاز', ' liquids', '气和', ' gaz', ' solids', '氣體', '的气', ' rắn', '气了', ' solide']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased1 J-lens: [' liquids', '液态', ' Liquid', 'liquid', ' liquid', ' lique', ' Vapor', '__.', ' vapor', '________', ' gases', '_________', '?\\', '液体', 'Liquid', '___', '...**', '…**', ' fluids', '...\\', ' Liqu', '_____', '____', ' liquide', '____________', ' ________', '—.', '常温', '.".', ' Gas', '固态', ' Fluid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased0.5 J-lens: [' liquids', '液态', ' liquid', ' Liquid', 'liquid', ' lique', ' vapor', ' Vapor', '________', '__.', ' gases', '液体', '___', '_________', '?\\', 'Liquid', '____', ' fluids', '...**', ' Liqu', '...\\', '_____', '____________', ' Gas', '…**', ' ________', ' gas', ' fluid', '常温', ' liquide', ' Fluid', 'gas']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased1 plain24: ['สถานะ', '固态', '液态', ' الحالة', 'ั', 'usually', '状态的', '态', '{name', '常温', 'फल', '的状态', '工作状态', '的气体', '英文名称', ' liquids', ' theirs', 'udiant', '.initState', ' kwest', ' quyển', '固体', 'omers', '[state', ' invariably', ' газо', ' состояния', ' usually', 'otope', 'liquid', '常态', '通常为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased0.5 plain24: ['สถานะ', '固态', '液态', ' الحالة', 'ั', 'usually', '态', '状态的', '{name', '常温', '的状态', 'फल', '的气体', '工作状态', '英文名称', ' liquids', ' theirs', '固体', 'udiant', ' usually', 'omers', ' quyển', ' kwest', '.initState', '[state', ' состояния', ' газо', ' invariably', 'otope', 'liquid', '常态', '通常为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased1 plain27: [' gas', '气体', ' gases', 'gas', '的气体', '气体的', ' Gas', '固态', 'Gas', '_gas', '气', ' газо', ' газ', '固体', 'liquid', ' газа', ' gás', 'solid', '液态', ' الغاز', ' GAS', '气和', '氣體', ' liquids', ' liquid', ' rắn', ' gaz', ' solids', '气了', ' solid', ' solide', '的气']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass erased0.5 plain27: [' gas', '气体', ' gases', 'gas', '的气体', '气体的', ' Gas', '固态', 'Gas', '气', '_gas', ' газо', ' газ', '固体', 'liquid', ' газа', ' gás', 'solid', '液态', ' الغاز', ' GAS', ' liquid', '气和', ' solid', ' liquids', '氣體', ' gaz', ' solids', ' rắn', '的气', '气了', ' solide']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

J-lens: [' always', ' ALWAYS', 'always', '.\\', '...\\', ' equal', ' triangle', '?\\', ' Always', ' triangles', ' invariably', '___', ' equals', ' triangular', ' exactly', '__.', 'Always', '____', ').\\', '.\\"', '_____', 'equal', ' polygon', ' depends', ' Triangle', ' polygons', '固定的', ' triang', '。\\', '\\.', '________', '_.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

plain lens: ['always', ' always', 'aner', 'फल', ' ALWAYS', 'više', ' Always', ' دائماً', ' indetermin', 'Always', ' exactly', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', ' دائمًا', 'oplan', ' triangles', ' greater', '固定的', 'rapper', ' Siempre', '脸的', ' selalu', '{}".', 'FACE', ' _$', ' zawsze', 'omers', ' polygons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass J-lens: [' always', ' ALWAYS', 'always', '.\\', '...\\', ' equal', ' triangle', '?\\', ' Always', ' triangles', ' invariably', '___', ' equals', ' triangular', ' exactly', '__.', 'Always', '____', ').\\', '.\\"', '_____', 'equal', ' polygon', ' depends', ' Triangle', ' polygons', '固定的', ' triang', '。\\', '\\.', '________', '_.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', 'više', ' Always', ' دائماً', ' indetermin', 'Always', ' exactly', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', ' دائمًا', 'oplan', ' triangles', ' greater', '固定的', 'rapper', ' Siempre', '脸的', ' selalu', '{}".', 'FACE', ' _$', ' zawsze', 'omers', ' polygons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', '三角形', ' sempre', ' всегда', ' دائمًا', '总是', ' 항상', '永远', ' zawsze', 'ilateral', ' دائماً', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', ' invariably', 'сегда', '必ず', ' determined', ' exactly', ' luôn', '永远不会', ' siempre', ' Triangle']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased1 J-lens: [' ALWAYS', ' always', 'always', '...\\', '?\\', '.\\', ' triangle', ' invariably', ' triangles', ' Always', ' equal', ' .**', ').\\', '.\\"', '__.', ' دائماً', 'Always', '___', ' triangular', 'equal', ' equals', '...**', ' polygons', ' دائمًا', '\\.', ' polygon', '_____', ' Triangle', ' Depends', ' exactly', '?<', '。\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased0.5 J-lens: [' always', ' ALWAYS', 'always', '...\\', '.\\', '?\\', ' triangle', ' equal', ' Always', ' triangles', ' invariably', ').\\', '__.', '.\\"', '___', 'Always', ' triangular', ' equals', 'equal', ' دائماً', ' exactly', ' .**', '_____', ' polygon', '____', ' depends', ' polygons', ' Triangle', '\\.', '固定的', '。\\', ' triang']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased1 plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', ' exactly', ' Always', ' indetermin', '三角形的', 'više', 'Always', ' uniquely', 'ilateral', ' دائماً', ' invariably', ' greater', 'ilater', ' triangles', '所大学', '固定的', 'oplan', ' دائمًا', ' selalu', 'rapper', ' polygons', '{}".', ' Siempre', '脸的', 'omers', ' zawsze', 'FACE', '必ず']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased0.5 plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', ' Always', 'više', ' indetermin', ' exactly', ' دائماً', 'Always', '三角形的', ' uniquely', 'ilateral', ' invariably', '所大学', 'ilater', ' greater', ' triangles', ' دائمًا', 'oplan', '固定的', 'rapper', ' selalu', ' Siempre', '脸的', '{}".', 'FACE', ' polygons', ' zawsze', '必ず', 'omers']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased1 plain27: [' always', 'always', ' Always', 'Always', ' ALWAYS', ' triangles', '三角形的', ' triangle', ' sempre', '三角形', ' всегда', ' دائمًا', ' 항상', ' دائماً', '总是', ' zawsze', 'ilateral', 'triangle', 'Triangle', '永远', ' alltid', ' selalu', '常に', ' invariably', 'сегда', '必ず', ' Siempre', '永远不会', ' siempre', ' luôn', ' determined', ' exactly']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass erased0.5 plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', ' sempre', '三角形', ' всегда', ' دائمًا', ' 항상', '总是', ' دائماً', ' zawsze', '永远', 'ilateral', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', ' invariably', 'сегда', '必ず', ' determined', ' exactly', '永远不会', ' siempre', ' luôn', ' Triangle']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [J-lens](readout.json)     | 2/8                    |    0.750 | 1/7                      | 2/8              |          0 |
| [plain lens](readout.json) | 1/8                    |    0.706 | 1/7                      | 1/8              |          0 |

### End-of-pass readout (not for earlier edits)

| method                                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:-------------------------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [end-pass erased0.5 plain27](readout.json) | 6/8                    |    0.899 | 5/7                      | 6/8              |          0 |
| [end-pass plain27](readout.json)           | 5/8                    |    0.895 | 4/7                      | 6/8              |          0 |
| [end-pass erased1 plain27](readout.json)   | 5/8                    |    0.904 | 4/7                      | 5/8              |          0 |
| [end-pass J-lens](readout.json)            | 4/8                    |    0.858 | 3/7                      | 6/8              |          0 |
| [end-pass erased1 J-lens](readout.json)    | 3/8                    |    0.853 | 2/7                      | 3/8              |          0 |
| [end-pass erased0.5 J-lens](readout.json)  | 3/8                    |    0.857 | 2/7                      | 4/8              |          0 |
| [end-pass plain24](readout.json)           | 1/8                    |    0.816 | 1/7                      | 1/8              |          0 |
| [end-pass erased1 plain24](readout.json)   | 1/8                    |    0.812 | 1/7                      | 1/8              |          0 |
| [end-pass erased0.5 plain24](readout.json) | 1/8                    |    0.814 | 1/7                      | 1/8              |          0 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_142814_jlens-one-pass/run.md
