---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: data/english_hidden_words_v3.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 43.54
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: Sixteen probes fixed before inference: eight geography and eight animal concepts not used as targets in v1/v2. Freeze primary method to J residual24, final position, k32, existing prompt and greedy-output masks, and output-direction erasure strength0.5. Strength was selected from0/0.5/1 on observed v2; full erasure and equally filtered plain24/27 remain controls, not alternate primary methods selected after this run. Same factual prefix and no trailing space. Common translated answer aliases are predeclared for every case, extending older scoring coverage; compare methods within this set. Alias coverage is not exhaustive. All cases remain, including wrong baseline answers and unscoreable labels. Labels are plausible intermediates, not proof of their computational use. No output filtering or retries. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Historical cached continuations are regenerated with the same eight-token cap. Scoring definitions are unchanged. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept     | method                     | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:------------|:---------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| Sweden      | J-lens                     | False         |           0.893333 |             1 |                      0 | False          | False        |
| Sweden      | plain lens                 | False         |           0.933333 |           102 |                     15 | False          | False        |
| Sweden      | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| Sweden      | end-pass plain24           | False         |           1        |           101 |             1000000000 | False          | False        |
| Sweden      | end-pass plain27           | True          |           1        |             1 |             1000000000 | True           | True         |
| Sweden      | end-pass erased1 J-lens    | True          |           1        |             2 |             1000000000 | True           | True         |
| Sweden      | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| Sweden      | end-pass erased1 plain24   | False         |           1        |           209 |             1000000000 | False          | False        |
| Sweden      | end-pass erased0.5 plain24 | False         |           1        |           211 |             1000000000 | False          | False        |
| Sweden      | end-pass erased1 plain27   | True          |           1        |             6 |             1000000000 | True           | True         |
| Sweden      | end-pass erased0.5 plain27 | True          |           1        |             1 |             1000000000 | True           | True         |
| Finland     | J-lens                     | False         |           0.869565 |             3 |                      0 | False          | False        |
| Finland     | plain lens                 | False         |           0.794466 |           177 |                    486 | False          | False        |
| Finland     | end-pass J-lens            | True          |           0.996047 |             2 |             1000000000 | True           | True         |
| Finland     | end-pass plain24           | False         |           0.988142 |           177 |             1000000000 | False          | False        |
| Finland     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| Finland     | end-pass erased1 J-lens    | True          |           0.98419  |            13 |             1000000000 | True           | True         |
| Finland     | end-pass erased0.5 J-lens  | True          |           0.996047 |             3 |             1000000000 | True           | True         |
| Finland     | end-pass erased1 plain24   | False         |           0.98419  |           758 |             1000000000 | False          | False        |
| Finland     | end-pass erased0.5 plain24 | False         |           0.988142 |           360 |             1000000000 | False          | False        |
| Finland     | end-pass erased1 plain27   | True          |           1        |             1 |             1000000000 | True           | True         |
| Finland     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| Denmark     | J-lens                     | False         |           0.908333 |             3 |                      0 | False          | False        |
| Denmark     | plain lens                 | False         |           0.894444 |          4135 |                    637 | False          | False        |
| Denmark     | end-pass J-lens            | True          |           0.997222 |             2 |             1000000000 | True           | True         |
| Denmark     | end-pass plain24           | False         |           0.997222 |          4133 |             1000000000 | False          | False        |
| Denmark     | end-pass plain27           | True          |           1        |            13 |             1000000000 | True           | False        |
| Denmark     | end-pass erased1 J-lens    | True          |           0.986111 |            12 |             1000000000 | True           | True         |
| Denmark     | end-pass erased0.5 J-lens  | True          |           0.997222 |             5 |             1000000000 | True           | True         |
| Denmark     | end-pass erased1 plain24   | False         |           1        |          3940 |             1000000000 | False          | False        |
| Denmark     | end-pass erased0.5 plain24 | False         |           1        |          3959 |             1000000000 | False          | False        |
| Denmark     | end-pass erased1 plain27   | True          |           1        |            10 |             1000000000 | True           | True         |
| Denmark     | end-pass erased0.5 plain27 | True          |           1        |            10 |             1000000000 | True           | False        |
| Netherlands | J-lens                     | False         |           0.771053 |             5 |                      0 | False          | False        |
| Netherlands | plain lens                 | False         |           0.736842 |          2934 |                   3567 | False          | False        |
| Netherlands | end-pass J-lens            | True          |           0.963158 |             4 |             1000000000 | True           | True         |
| Netherlands | end-pass plain24           | False         |           0.926316 |          2934 |             1000000000 | False          | False        |
| Netherlands | end-pass plain27           | True          |           0.977632 |            11 |             1000000000 | True           | False        |
| Netherlands | end-pass erased1 J-lens    | False         |           0.918421 |            31 |             1000000000 | False          | False        |
| Netherlands | end-pass erased0.5 J-lens  | True          |           0.952632 |             6 |             1000000000 | True           | True         |
| Netherlands | end-pass erased1 plain24   | False         |           0.915789 |         10116 |             1000000000 | False          | False        |
| Netherlands | end-pass erased0.5 plain24 | False         |           0.921053 |          5441 |             1000000000 | False          | False        |
| Netherlands | end-pass erased1 plain27   | True          |           0.971053 |           139 |             1000000000 | False          | True         |
| Netherlands | end-pass erased0.5 plain27 | True          |           0.976316 |            23 |             1000000000 | True           | True         |
| Switzerland | J-lens                     | True          |           1        |             4 |                    344 | True           | True         |
| Switzerland | plain lens                 | False         |           0.944444 |          7002 |                  11079 | False          | False        |
| Switzerland | end-pass J-lens            | True          |           1        |             4 |             1000000000 | True           | True         |
| Switzerland | end-pass plain24           | False         |           0.944444 |          7002 |             1000000000 | False          | False        |
| Switzerland | end-pass plain27           | True          |           1        |            32 |             1000000000 | False          | True         |
| Switzerland | end-pass erased1 J-lens    | True          |           1        |             5 |             1000000000 | True           | True         |
| Switzerland | end-pass erased0.5 J-lens  | True          |           1        |             4 |             1000000000 | True           | True         |
| Switzerland | end-pass erased1 plain24   | False         |           0.935185 |          8588 |             1000000000 | False          | False        |
| Switzerland | end-pass erased0.5 plain24 | False         |           0.944444 |          7755 |             1000000000 | False          | False        |
| Switzerland | end-pass erased1 plain27   | False         |           1        |            82 |             1000000000 | False          | False        |
| Switzerland | end-pass erased0.5 plain27 | False         |           1        |            47 |             1000000000 | False          | False        |
| Italy       | J-lens                     | False         |           0.867064 |             4 |                      2 | False          | False        |
| Italy       | plain lens                 | False         |           0.690476 |           862 |                      7 | False          | False        |
| Italy       | end-pass J-lens            | True          |           1        |             3 |             1000000000 | True           | True         |
| Italy       | end-pass plain24           | False         |           0.950397 |           859 |             1000000000 | False          | False        |
| Italy       | end-pass plain27           | False         |           0.988095 |            44 |             1000000000 | False          | False        |
| Italy       | end-pass erased1 J-lens    | True          |           0.998016 |            14 |             1000000000 | True           | True         |
| Italy       | end-pass erased0.5 J-lens  | True          |           1        |             3 |             1000000000 | True           | True         |
| Italy       | end-pass erased1 plain24   | False         |           0.938492 |          3286 |             1000000000 | False          | False        |
| Italy       | end-pass erased0.5 plain24 | False         |           0.94246  |          2621 |             1000000000 | False          | False        |
| Italy       | end-pass erased1 plain27   | False         |           0.968254 |          1565 |             1000000000 | False          | False        |
| Italy       | end-pass erased0.5 plain27 | False         |           0.980159 |           197 |             1000000000 | False          | False        |
| Peru        | J-lens                     | False         |           0.807692 |            14 |                     10 | False          | False        |
| Peru        | plain lens                 | False         |           0.668269 |          7280 |                      2 | False          | False        |
| Peru        | end-pass J-lens            | True          |           0.877404 |            13 |             1000000000 | True           | True         |
| Peru        | end-pass plain24           | False         |           0.783654 |          7276 |             1000000000 | False          | False        |
| Peru        | end-pass plain27           | False         |           0.850962 |            96 |             1000000000 | False          | False        |
| Peru        | end-pass erased1 J-lens    | False         |           0.853365 |            40 |             1000000000 | False          | False        |
| Peru        | end-pass erased0.5 J-lens  | True          |           0.872596 |            20 |             1000000000 | True           | True         |
| Peru        | end-pass erased1 plain24   | False         |           0.740385 |         12211 |             1000000000 | False          | False        |
| Peru        | end-pass erased0.5 plain24 | False         |           0.762019 |         11052 |             1000000000 | False          | False        |
| Peru        | end-pass erased1 plain27   | False         |           0.819712 |          1258 |             1000000000 | False          | False        |
| Peru        | end-pass erased0.5 plain27 | False         |           0.84375  |           332 |             1000000000 | False          | False        |
| Chile       | J-lens                     | False         |           0.617778 |            17 |                      5 | False          | False        |
| Chile       | plain lens                 | False         |           0.76     |           433 |                   1002 | False          | False        |
| Chile       | end-pass J-lens            | True          |           0.977778 |            16 |             1000000000 | True           | True         |
| Chile       | end-pass plain24           | False         |           0.977778 |           433 |             1000000000 | False          | False        |
| Chile       | end-pass plain27           | True          |           1        |            30 |             1000000000 | True           | True         |
| Chile       | end-pass erased1 J-lens    | False         |           0.964444 |            45 |             1000000000 | False          | False        |
| Chile       | end-pass erased0.5 J-lens  | False         |           0.968889 |            32 |             1000000000 | False          | False        |
| Chile       | end-pass erased1 plain24   | False         |           0.968889 |           597 |             1000000000 | False          | False        |
| Chile       | end-pass erased0.5 plain24 | False         |           0.973333 |           489 |             1000000000 | False          | False        |
| Chile       | end-pass erased1 plain27   | False         |           1        |            37 |             1000000000 | False          | False        |
| Chile       | end-pass erased0.5 plain27 | False         |           1        |            30 |             1000000000 | False          | False        |
| whale       | J-lens                     | True          |           1        |             6 |                      0 | False          | False        |
| whale       | plain lens                 | False         |           1        |            91 |                      0 | False          | False        |
| whale       | end-pass J-lens            | True          |           1        |             6 |                      0 | False          | False        |
| whale       | end-pass plain24           | False         |           1        |            91 |                      0 | False          | False        |
| whale       | end-pass plain27           | False         |           1        |            33 |                      0 | False          | False        |
| whale       | end-pass erased1 J-lens    | True          |           1        |             6 |                      0 | False          | False        |
| whale       | end-pass erased0.5 J-lens  | True          |           1        |             6 |                      0 | False          | False        |
| whale       | end-pass erased1 plain24   | False         |           1        |           125 |                      0 | False          | False        |
| whale       | end-pass erased0.5 plain24 | False         |           1        |           106 |                      0 | False          | False        |
| whale       | end-pass erased1 plain27   | False         |           1        |            41 |                      0 | False          | False        |
| whale       | end-pass erased0.5 plain27 | False         |           1        |            36 |                      0 | False          | False        |
| bat         | J-lens                     | False         |           0.908571 |          1279 |                      0 | False          | False        |
| bat         | plain lens                 | False         |           0.848571 |           531 |                      0 | False          | False        |
| bat         | end-pass J-lens            | False         |           1        |          1275 |             1000000000 | False          | False        |
| bat         | end-pass plain24           | False         |           0.934286 |           529 |             1000000000 | False          | False        |
| bat         | end-pass plain27           | False         |           1        |           249 |             1000000000 | False          | False        |
| bat         | end-pass erased1 J-lens    | False         |           0.954286 |           450 |             1000000000 | False          | False        |
| bat         | end-pass erased0.5 J-lens  | False         |           0.982857 |           643 |             1000000000 | False          | False        |
| bat         | end-pass erased1 plain24   | False         |           0.922857 |           266 |             1000000000 | False          | False        |
| bat         | end-pass erased0.5 plain24 | False         |           0.928571 |           368 |             1000000000 | False          | False        |
| bat         | end-pass erased1 plain27   | False         |           0.988571 |            92 |             1000000000 | False          | False        |
| bat         | end-pass erased0.5 plain27 | False         |           0.997143 |           145 |             1000000000 | False          | False        |
| snake       | J-lens                     | True          |           0.672358 |           118 |                   6588 | False          | True         |
| snake       | plain lens                 | False         |           0.426016 |          4582 |                 245832 | False          | False        |
| snake       | end-pass J-lens            | True          |           0.672358 |           118 |                   6588 | False          | True         |
| snake       | end-pass plain24           | False         |           0.426016 |          4582 |                 245831 | False          | False        |
| snake       | end-pass plain27           | True          |           0.694309 |            17 |                 242705 | True           | False        |
| snake       | end-pass erased1 J-lens    | True          |           0.672358 |           129 |                  67894 | False          | True         |
| snake       | end-pass erased0.5 J-lens  | True          |           0.669919 |           136 |                  21898 | False          | True         |
| snake       | end-pass erased1 plain24   | False         |           0.403252 |          3743 |                 235559 | False          | False        |
| snake       | end-pass erased0.5 plain24 | False         |           0.419512 |          4217 |                 242632 | False          | False        |
| snake       | end-pass erased1 plain27   | True          |           0.694309 |            17 |                 242816 | True           | False        |
| snake       | end-pass erased0.5 plain27 | True          |           0.694309 |            17 |                 242707 | True           | False        |
| rabbit      | J-lens                     | False         |           0.939459 |            37 |                      0 | False          | False        |
| rabbit      | plain lens                 | False         |           0.625356 |         69039 |                   2009 | False          | False        |
| rabbit      | end-pass J-lens            | False         |           0.982906 |            35 |             1000000000 | False          | False        |
| rabbit      | end-pass plain24           | False         |           0.759259 |         69033 |             1000000000 | False          | False        |
| rabbit      | end-pass plain27           | False         |           0.733618 |         13978 |             1000000000 | False          | False        |
| rabbit      | end-pass erased1 J-lens    | False         |           0.968661 |            73 |             1000000000 | False          | False        |
| rabbit      | end-pass erased0.5 J-lens  | False         |           0.980057 |            51 |             1000000000 | False          | False        |
| rabbit      | end-pass erased1 plain24   | False         |           0.753561 |         87494 |             1000000000 | False          | False        |
| rabbit      | end-pass erased0.5 plain24 | False         |           0.750712 |         77457 |             1000000000 | False          | False        |
| rabbit      | end-pass erased1 plain27   | False         |           0.712963 |         18906 |             1000000000 | False          | False        |
| rabbit      | end-pass erased0.5 plain27 | False         |           0.725071 |         15989 |             1000000000 | False          | False        |
| bear        | J-lens                     | False         |           0.89441  |            55 |                      0 | False          | False        |
| bear        | plain lens                 | False         |           0.84472  |           302 |                     11 | False          | False        |
| bear        | end-pass J-lens            | False         |           1        |            53 |             1000000000 | False          | False        |
| bear        | end-pass plain24           | True          |           1        |           300 |             1000000000 | False          | True         |
| bear        | end-pass plain27           | True          |           1        |            10 |             1000000000 | True           | False        |
| bear        | end-pass erased1 J-lens    | True          |           1        |            30 |             1000000000 | True           | True         |
| bear        | end-pass erased0.5 J-lens  | False         |           1        |            39 |             1000000000 | False          | False        |
| bear        | end-pass erased1 plain24   | True          |           1        |           338 |             1000000000 | False          | True         |
| bear        | end-pass erased0.5 plain24 | True          |           1        |           318 |             1000000000 | False          | True         |
| bear        | end-pass erased1 plain27   | True          |           1        |             7 |             1000000000 | True           | True         |
| bear        | end-pass erased0.5 plain27 | True          |           1        |             6 |             1000000000 | True           | False        |
| butterfly   | J-lens                     | True          |           0.466063 |             5 |                     77 | True           | True         |
| butterfly   | plain lens                 | False         |           0.565611 |          6339 |                   2003 | False          | False        |
| butterfly   | end-pass J-lens            | True          |           0.800905 |             5 |             1000000000 | True           | True         |
| butterfly   | end-pass plain24           | False         |           0.778281 |          6338 |             1000000000 | False          | False        |
| butterfly   | end-pass plain27           | False         |           0.895928 |           121 |             1000000000 | False          | False        |
| butterfly   | end-pass erased1 J-lens    | True          |           0.800905 |             6 |             1000000000 | True           | True         |
| butterfly   | end-pass erased0.5 J-lens  | True          |           0.800905 |             5 |             1000000000 | True           | True         |
| butterfly   | end-pass erased1 plain24   | False         |           0.764706 |          8297 |             1000000000 | False          | False        |
| butterfly   | end-pass erased0.5 plain24 | False         |           0.771493 |          7163 |             1000000000 | False          | False        |
| butterfly   | end-pass erased1 plain27   | False         |           0.891403 |           217 |             1000000000 | False          | False        |
| butterfly   | end-pass erased0.5 plain27 | False         |           0.895928 |           154 |             1000000000 | False          | False        |
| beetle      | J-lens                     | False         |           0.660569 |           437 |                    897 | False          | False        |
| beetle      | plain lens                 | False         |           0.546748 |         18318 |                 227599 | False          | False        |
| beetle      | end-pass J-lens            | False         |           0.660569 |           437 |                    897 | False          | False        |
| beetle      | end-pass plain24           | False         |           0.546748 |         18318 |                 227599 | False          | False        |
| beetle      | end-pass plain27           | False         |           0.545732 |          7611 |                 192894 | False          | False        |
| beetle      | end-pass erased1 J-lens    | False         |           0.713415 |           439 |                   7940 | False          | False        |
| beetle      | end-pass erased0.5 J-lens  | False         |           0.703252 |           446 |                   2472 | False          | False        |
| beetle      | end-pass erased1 plain24   | False         |           0.497967 |         14672 |                 168898 | False          | False        |
| beetle      | end-pass erased0.5 plain24 | False         |           0.521341 |         16239 |                 205172 | False          | False        |
| beetle      | end-pass erased1 plain27   | False         |           0.542683 |          7047 |                 182436 | False          | False        |
| beetle      | end-pass erased0.5 plain27 | False         |           0.544715 |          7316 |                 188794 | False          | False        |
| crab        | J-lens                     | False         |                    |           108 |             1000000000 |                | False        |
| crab        | plain lens                 | False         |                    |          6056 |             1000000000 |                | False        |
| crab        | end-pass J-lens            | False         |                    |           108 |             1000000000 |                | False        |
| crab        | end-pass plain24           | False         |                    |          6056 |             1000000000 |                | False        |
| crab        | end-pass plain27           | False         |                    |          3593 |             1000000000 |                | False        |
| crab        | end-pass erased1 J-lens    | False         |                    |           109 |             1000000000 |                | False        |
| crab        | end-pass erased0.5 J-lens  | False         |                    |           105 |             1000000000 |                | False        |
| crab        | end-pass erased1 plain24   | False         |                    |          4849 |             1000000000 |                | False        |
| crab        | end-pass erased0.5 plain24 | False         |                    |          5423 |             1000000000 |                | False        |
| crab        | end-pass erased1 plain27   | False         |                    |          3989 |             1000000000 |                | False        |
| crab        | end-pass erased0.5 plain27 | False         |                    |          3808 |             1000000000 |                | False        |

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

J-lens: [' Stockholm', ' Sweden', ' Oslo', ' Denmark', ' Berlin', ' Copenhagen', ' Norway', ' Munich', ' Germany', ' Helsinki', ' Finland', ' London', ' Amsterdam', 'Sweden', ' Rotterdam', ' Swedish', ' Paris', ' Switzerland', ' Frankfurt', ' Stuttgart', ' Netherlands', '瑞典', ' Vienna', ' Brussels', ' Scandin', ' Minneapolis', ' Barcelona', ' Edinburgh', ' Zurich', ' Prague', ' Italy', ' Austria']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

plain lens: [' findes', ' Haga', 'datum', '名胜', ' Thụy', '...).', '...**', 'stad', 'located', 'not', 'hatian', ' NOT', '...”', '先到', 'UNK', ' stockholm', '叫什么', 'aname', '.........', '名城', 'stav', 'otope', ' democr', 'ẹo', ' darbo', ' greve', 'više', ' شار', ' medias', '人名', '现', ' ogs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass J-lens: [' Sweden', ' Oslo', ' Denmark', ' Berlin', ' Copenhagen', ' Norway', ' Munich', ' Germany', ' Helsinki', ' Finland', ' London', ' Amsterdam', 'Sweden', ' Rotterdam', ' Paris', ' Swedish', ' Switzerland', ' Frankfurt', ' Netherlands', ' Stuttgart', '瑞典', ' Vienna', ' Brussels', ' Minneapolis', ' Scandin', ' Barcelona', ' Edinburgh', ' Prague', ' Zurich', ' Italy', ' Sverige', ' Austria']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass plain24: [' findes', ' Haga', 'datum', '名胜', ' Thụy', '...).', '...**', 'stad', 'located', 'not', 'hatian', ' NOT', '...”', '先到', 'UNK', '叫什么', 'aname', '.........', '名城', 'otope', ' democr', 'stav', ' darbo', 'ẹo', ' greve', 'više', ' شار', '人名', ' medias', '现', '彩电', ' ogs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass plain27: [' Haga', ' Sweden', '瑞典', 'Sweden', 'ストック', ' Сто', ' Thụy', ' السويد', '.stock', 'almö', ' Swedish', ' Sund', 'สวี', ' Sverige', ' svenska', ' Göteborg', ' Lund', '北欧', ' sweden', ' malmö', 'anyak', ' Rune', ' Шве', ' Scandin', 'Ups', 'köping', ' capitals', 'stav', 'stad', ' sverige', ' swearing', '_stock']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased1 J-lens: [' Germany', ' Denmark', ' Sweden', '.\\', ' Berlin', ' Italy', ' Austria', ' France', ' City', ' Munich', ' Norway', ' London', ' Finland', ' Europe', ' Netherlands', ' Belgium', '____', '...', ' Paris', ' Oslo', '________', ' England', ' Frankfurt', '....', '?', ' Canada', '?\\', '.', 'Germany', ' Switzerland', ' Cities', ' Vienna']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased0.5 J-lens: [' Sweden', ' Germany', ' Denmark', ' Berlin', ' Oslo', ' Norway', ' Munich', ' Finland', ' London', ' Copenhagen', ' Italy', ' Netherlands', ' Paris', ' Austria', ' Amsterdam', ' Frankfurt', ' Switzerland', ' Helsinki', '.\\', ' Rotterdam', ' France', ' Belgium', ' City', ' Brussels', ' Vienna', ' Europe', 'Sweden', ' Barcelona', ' Minneapolis', ' Stuttgart', ' Düsseldorf', ' Hamburg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased1 plain24: [' findes', 'not', ' Haga', ' NOT', '...', 'located', '名胜', 'datum', '...).', '现', '先到', '...**', '...”', '____', '.........', ' called', 'hatian', ' democr', '叫什么', 'stad', 'UNK', 'otope', '人名', ' differs', '..."', 'nam', ' Thụy', 'ẹo', ' nota', '暂', 'aname', '....']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased0.5 plain24: [' findes', ' Haga', 'not', '名胜', 'datum', 'located', '...).', ' NOT', '...**', 'hatian', 'stad', '先到', ' Thụy', '...”', '现', '.........', 'UNK', '叫什么', ' democr', 'otope', ' called', 'aname', '...', '人名', '名城', '____', 'ẹo', 'stav', ' شار', ' darbo', ' medias', '彩电']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased1 plain27: [' Haga', '...', ' Sund', '存在', ' Rune', 'anyak', ' Sweden', '____', ' Сто', ' capitals', '人口', '马克', 'Ups', '现', ' called', '�', '称为', '瑞', '瑞典', 'S', 'Link', 'Den', ' swe', '猪肉', ' swearing', ' Lund', ' inte', ' anders', 'äte', ' huv', 'heden', '__']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Gothenburg is'

Baseline: ' Stockholm.\nHypothesis: The'

end-pass erased0.5 plain27: [' Haga', ' Sweden', '瑞典', ' Сто', ' Sund', 'Sweden', ' Rune', 'anyak', ' Thụy', 'almö', 'ストック', ' Lund', ' svenska', '...', '.stock', '存在', 'Ups', ' السويد', ' capitals', ' Sverige', 'สวี', '北欧', '马克', ' swearing', ' malmö', '人口', '猪肉', ' swe', ' Swedish', 'heden', 'äte', '�']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

J-lens: [' Helsinki', ' Stockholm', ' Berlin', ' Finland', ' Budapest', ' Prague', ' Copenhagen', ' Oslo', ' Munich', ' London', ' Paris', ' Frankfurt', ' Amsterdam', ' Sweden', ' Moscow', ' Brussels', ' Dublin', ' Warsaw', ' Vienna', ' Denmark', ' Toronto', ' Zurich', ' Istanbul', ' Madrid', ' Barcelona', ' Chicago', ' Germany', ' Minneapolis', ' Lisbon', ' Bogotá', ' Jakarta', ' Norway']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

plain lens: ['not', 'boa', 'also', 'しば', ' findes', '名城', '遥遥', ' NOT', 'hatian', 'stad', '____', 'otope', '...).', ' Rais', '名胜', 'nota', '...', 'bur', ' unic', '马力', 'UNK', '...”', 'ؤل', '马拉', 'informatics', 'ints', ' ogs', 'located', 'AGENT', '人名', 'واف', ' politicians']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass J-lens: [' Stockholm', ' Berlin', ' Finland', ' Budapest', ' Prague', ' Copenhagen', ' Oslo', ' Munich', ' London', ' Paris', ' Frankfurt', ' Amsterdam', ' Sweden', ' Brussels', ' Moscow', ' Dublin', ' Warsaw', ' Vienna', ' Denmark', ' Toronto', ' Istanbul', ' Zurich', ' Barcelona', ' Madrid', ' Chicago', ' Germany', ' Lisbon', ' Minneapolis', ' Bogotá', ' Jakarta', ' Norway', ' Leipzig']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass plain24: ['not', 'boa', 'also', 'しば', ' findes', '名城', '遥遥', ' NOT', 'hatian', 'stad', '____', 'otope', '...).', ' Rais', '名胜', 'nota', '...', 'bur', ' unic', '马力', 'UNK', '...”', 'ؤل', '马拉', 'informatics', 'ints', ' ogs', 'located', 'AGENT', '人名', 'واف', ' politicians']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass plain27: [' Finland', ' Finnish', 'Fin', ' Фин', '芬兰', '赫尔', ' fins', ' Finn', ' Esp', 'elsinki', ' Fin', 'FIN', ' FIN', ' Suomen', 'ainen', ' Athletics', '_fin', 'fin', ' fin', '文化中心', ' Rune', ' espoo', ' Pä', ' capitale', '首都', ' Pir', 'หาง', '.fi', ' Finans', ' oulu', '级', ' unic']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased1 J-lens: [' Berlin', ' Paris', ' Germany', ' London', ' City', ' Frankfurt', ' France', ' Sweden', '...', ' Prague', ' Poland', ' Denmark', ' city', ' Finland', ' Munich', ' Chicago', '.\\', ' Toronto', ' Vienna', ' Amsterdam', ' Moscow', ' Dublin', ' Madrid', ' Italy', ' Milan', ' cities', '?', ' Budapest', 'city', ' Barcelona', ' Stockholm', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased0.5 J-lens: [' Berlin', ' Paris', ' London', ' Finland', ' Prague', ' Stockholm', ' Frankfurt', ' Germany', ' Budapest', ' Sweden', ' Munich', ' Denmark', ' City', ' Amsterdam', ' Copenhagen', ' Vienna', ' Moscow', ' Dublin', ' Brussels', ' Toronto', ' Chicago', ' Oslo', ' Madrid', ' Poland', ' Barcelona', ' Warsaw', ' Zurich', ' Milan', ' Norway', ' Bogotá', ' Istanbul', ' city']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased1 plain24: ['not', '...', 'also', 'boa', ' NOT', '____', 'しば', ' findes', 'bur', '遥遥', ' also', '名城', 'otope', '__', '________', '...”', ' Rais', '...).', '现', ' unic', 'located', ' politicians', ' not', 'hatian', 'informatics', 'usually', 'stad', '马拉', '人名', '名胜', 'nota', 'UNK']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased0.5 plain24: ['not', 'boa', 'also', '...', ' NOT', '____', 'しば', ' findes', '遥遥', '名城', 'otope', 'bur', 'hatian', ' Rais', '...).', 'stad', ' unic', '...”', '名胜', 'nota', '________', 'informatics', 'UNK', 'located', '马拉', ' politicians', '人名', 'ؤل', '马力', 'usually', ' also', 'ints']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased1 plain27: ['...', 'Fin', ' Esp', ' also', ' Fin', '级', ' fins', ' fin', ' Finland', ' not', 'ä', ' Pir', '-', ' Finnish', 'fin', '____', 'F', '\xa0', 'not', 'H', ' NOT', '文化中心', '现', ' FIN', 'k', '.', '__', '()', ' Finn', 'FIN', ' supposed', 'to']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Tampere is'

Baseline: ' Helsinki.\nHypothesis: Tamp'

end-pass erased0.5 plain27: ['Fin', '...', ' Finland', ' Finnish', ' Esp', ' fins', ' Fin', ' Фин', ' Finn', ' fin', ' FIN', 'FIN', '级', 'fin', '文化中心', '赫尔', '芬兰', ' Pir', 'ainen', ' Athletics', ' also', ' Rune', '_fin', 'ä', ' Suomen', ' Pä', ' capitale', '首都', ' unic', ' Financial', 'หาง', ' Finance']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

J-lens: [' Copenhagen', ' Oslo', ' Berlin', ' Denmark', ' Helsinki', ' Stockholm', ' Brussels', ' Prague', ' London', ' Vienna', ' Munich', ' Frankfurt', ' Madrid', ' Paris', ' Budapest', ' Seoul', ' Amsterdam', '丹麦', ' Lisbon', ' Nairobi', ' Danish', ' Norway', ' Warsaw', ' Dublin', ' Sweden', ' Toronto', ' Finland', ' Luxembourg', ' Bruxelles', ' Barcelona', ' Hamburg', ' Moscow']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

plain lens: ['više', 'also', ' ogs', 'nici', 'hatian', 'otope', ' medias', '名胜', '担', ' greve', 'stad', 'olon', 'に行ってきました', 'игра', 'urin', ' Haga', '不来', ' correc', '.idea', 'lima', '名城', '...\\', ' likewise', ' unic', ' hereby', '...**', ' findes', ' ALSO', 'pek', 'носит', 'NotFound', ' politicians']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass J-lens: [' Oslo', ' Berlin', ' Denmark', ' Helsinki', ' Stockholm', ' Brussels', ' Prague', ' London', ' Vienna', ' Frankfurt', ' Munich', ' Madrid', ' Budapest', ' Paris', ' Seoul', ' Amsterdam', '丹麦', ' Nairobi', ' Lisbon', ' Danish', ' Norway', ' Warsaw', ' Dublin', ' Sweden', ' Toronto', ' Finland', ' Luxembourg', ' Bruxelles', ' Barcelona', ' Moscow', ' Hamburg', ' Bogotá']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass plain24: ['više', 'also', ' ogs', 'nici', 'hatian', 'otope', ' medias', '名胜', '担', ' greve', 'stad', 'olon', 'に行ってきました', 'игра', 'urin', ' Haga', '不来', ' correc', '.idea', 'lima', '名城', '...\\', ' likewise', ' unic', ' hereby', '...**', ' findes', ' ALSO', 'pek', 'носит', 'NotFound', ' politicians']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass plain27: [' København', ' capitale', '首都', ' Vej', 'kilde', 'bage', 'openhagen', ' Freder', ' Capitals', ' capitals', ' Heller', 'anyak', 'DK', 'Den', 'sek', '首府', ' odense', '谤', 'デン', ' Ribe', '-capital', '丹麦', ' danske', 'ówek', ' capitalized', '资本', '_dc', ' roskilde', ' Charl', 'หลวง', 'ellem', 'benhavn']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased1 J-lens: [' Berlin', ' London', ' Oslo', '...', ' City', '.\\', ' Paris', ' Brussels', ' Madrid', ' Frankfurt', ' Germany', ' Helsinki', ' Denmark', ' Prague', '____', ' Vienna', ' Dublin', ' Finland', ' Budapest', ' Luxembourg', ' Toronto', '________', ' Stockholm', ' Rome', ' Heidelberg', '....', ' Munich', ' Belgium', ' cities', ' Jerusalem', ' Amsterdam', ' city']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased0.5 J-lens: [' Berlin', ' Oslo', ' London', ' Helsinki', ' Brussels', ' Denmark', ' Stockholm', ' Prague', ' Paris', ' Frankfurt', ' Madrid', ' Vienna', ' Munich', ' Budapest', ' City', ' Dublin', ' Toronto', ' Finland', ' Amsterdam', ' Luxembourg', ' Germany', ' Seoul', ' Nairobi', ' Norway', '.\\', ' Sweden', ' Belgium', ' Heidelberg', ' Lisbon', ' Warsaw', ' Bogotá', ' Hamburg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased1 plain24: ['also', '...', 'više', '担', 'otope', 'nici', ' medias', '名胜', 'hatian', 'olon', ' ogs', 'not', 'stad', ' unic', ' likewise', '不来', 'игра', '...\\', ' politicians', ' correc', ' hereby', '.idea', 'urin', 'sek', ' findes', ' Haga', '...**', ' greve', 'pek', 'lands', '名城', 'lima']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased0.5 plain24: ['also', 'više', 'nici', '担', 'otope', ' ogs', 'hatian', ' medias', '名胜', 'olon', 'stad', 'игра', ' unic', '不来', ' greve', ' correc', ' likewise', '...\\', 'urin', '.idea', ' Haga', ' hereby', 'に行ってきました', '...', 'lima', '名城', ' politicians', '...**', ' findes', 'pek', ' ALSO', 'not']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased1 plain27: ['...', ' capitale', '首都', ' Ros', ' Freder', 'bage', 'DK', 'sek', '资本', ' capitals', ' Heller', 'Den', '谤', ' Vej', ' capitalized', 'anyak', 'kilde', '首府', '法定', '_dc', ' Capitals', '存在', '-capital', '鹿', 'Ros', 'หลวง', '不详', 'Sk', 'ellem', ' Gent', '风光', 'DC']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Aarhus is'

Baseline: ' Copenhagen.\nHypothesis: The'

end-pass erased0.5 plain27: [' capitale', '首都', 'bage', ' Freder', ' Vej', ' capitals', 'DK', 'kilde', ' Heller', 'sek', 'Den', 'anyak', ' Capitals', '谤', ' Ros', '资本', '首府', ' capitalized', ' København', '-capital', '_dc', '...', 'หลวง', ' Ribe', 'ellem', ' Charl', '不详', 'デン', ' hoved', ' eget', ' kapital', '法定']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

J-lens: [' Amsterdam', ' Berlin', ' Paris', ' London', ' Brussels', ' Netherlands', ' Frankfurt', ' Düsseldorf', ' Jakarta', ' Madrid', ' Stockholm', ' Belgium', ' Germany', ' Vienna', ' Munich', ' Utrecht', ' Copenhagen', ' Lisbon', ' Hamburg', ' Dublin', ' Budapest', 'Paris', ' Oslo', ' Luxembourg', ' Barcelona', 'London', ' Prague', ' Heidelberg', ' Karlsruhe', ' Zurich', ' Bogotá', ' Istanbul']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

plain lens: ['遥遥', 'located', '鹿', '名胜', 'also', '先到', ' Haga', '...**', '...).', 'stad', '荷兰', ' medias', '...”', '...*', '万国', '...\\', 'mainan', '毗', 'носит', ' unic', 'otope', ' darbo', ' evenement', '.........', ' hereby', ' Luân', ' خاک', ' Edi', ' NOT', '暂定', 'boa', ' simil']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass J-lens: [' Berlin', ' Paris', ' London', ' Brussels', ' Netherlands', ' Frankfurt', ' Düsseldorf', ' Jakarta', ' Madrid', ' Belgium', ' Stockholm', ' Germany', ' Vienna', ' Munich', ' Utrecht', ' Copenhagen', ' Lisbon', ' Hamburg', ' Dublin', ' Budapest', ' Oslo', 'Paris', ' Luxembourg', ' Barcelona', 'London', ' Prague', ' Heidelberg', ' Karlsruhe', ' Zurich', ' Bogotá', ' Stuttgart', ' Istanbul']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass plain24: ['遥遥', 'located', '鹿', '名胜', 'also', '先到', ' Haga', '...**', '...).', 'stad', '荷兰', ' medias', '...”', '...*', '万国', '...\\', 'mainan', '毗', 'носит', ' unic', 'otope', ' darbo', ' evenement', '.........', ' hereby', ' Luân', ' خاک', ' Edi', ' NOT', '暂定', 'boa', ' simil']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass plain27: ['荷兰', '鹿', ' Dutch', ' Haga', 'wij', ' capitals', ' Capitals', 'terdam', ' Holland', '阿姆斯特', ' Hague', ' Netherlands', '马斯', ' medias', ' Brussels', '.nl', ' Wag', '荷', ' Haag', '镐', '荷蘭', '_nl', ' Utrecht', 'дам', 'ブリ', ' آم', ' Washing', ' capitale', ' Bruss', '北京', 'Den', 'ijk']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased1 J-lens: [' Germany', ' Paris', ' Berlin', ' London', ' Brussels', ' City', '.\\', ' Vienna', ' Belgium', ' France', ' Frankfurt', ' Dublin', '____', ' Luxembourg', ' Düsseldorf', ' Madrid', ' Munich', ' Jakarta', ' Italy', ' Denmark', ' city', '...', ' Karlsruhe', ' German', ' Bogotá', ' Heidelberg', ' cities', 'city', ' Cities', ' Europe', ' Stuttgart', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased0.5 J-lens: [' Berlin', ' Paris', ' London', ' Brussels', ' Germany', ' Frankfurt', ' Netherlands', ' Düsseldorf', ' Belgium', ' Vienna', ' Madrid', ' Jakarta', ' Munich', ' Dublin', ' City', ' Luxembourg', ' Copenhagen', ' Stockholm', ' Karlsruhe', ' France', ' Heidelberg', ' Bogotá', ' Denmark', ' Budapest', ' Hamburg', ' Oslo', 'Paris', ' Lisbon', ' Stuttgart', ' Barcelona', '.\\', ' Prague']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased1 plain24: ['遥遥', 'also', '鹿', 'located', '先到', '...).', '名胜', '...**', '...”', ' Haga', '...', 'stad', '现', '毗', ' NOT', ' medias', '...\\', ' unic', 'mainan', '...*', '万国', '.........', 'otope', ' simil', 'носит', ' hereby', 'not', '心惊', ' خاک', '暂定', ' darbo', ' evenement']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased0.5 plain24: ['遥遥', 'also', '鹿', 'located', '先到', '名胜', '...).', '...**', ' Haga', 'stad', '...”', ' medias', '毗', '...\\', '...*', 'mainan', '万国', ' unic', ' NOT', '荷兰', '现', 'otope', 'носит', '.........', '...', ' simil', ' hereby', ' خاک', ' darbo', ' evenement', '心惊', '暂定']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased1 plain27: ['鹿', '荷兰', ' capitals', ' Haga', ' Capitals', 'wij', ' medias', '马斯', 'Den', ' Den', ' Hague', '镐', '____', '话', ' democr', 'ブリ', '荷', '废水', ' Wag', ' ibu', ' Washing', '谤', '布鲁', ' Dutch', 'function', ' niz', ' Wax', '观光', ' sarc', 'terdam', ' Pret', ' Brussels']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Rotterdam is'

Baseline: ' Amsterdam.\nHypothesis: The'

end-pass erased0.5 plain27: ['荷兰', '鹿', ' capitals', ' Haga', ' Capitals', 'wij', ' Dutch', ' medias', '马斯', ' Hague', 'terdam', ' Holland', '镐', ' Brussels', '荷', ' Wag', 'Den', 'ブリ', ' Den', ' Haag', ' democr', ' Washing', '_nl', ' Netherlands', '话', 'дам', '废水', '谤', ' niz', ' ibu', ' Wax', '北京']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

J-lens: [' Paris', ' Zurich', ' Berlin', ' London', ' Switzerland', '巴黎', 'Paris', ' Brussels', ' Vienna', ' Zürich', ' France', ' Luxembourg', ' Stockholm', ' Madrid', ' Oslo', ' Munich', ' Amsterdam', ' Prague', ' Frankfurt', ' Bogotá', ' Montreal', ' París', ' Belgium', ' Bangkok', 'London', ' Dublin', ' Nairobi', ' Barcelona', ' Marseille', ' Londres', ' Rome', ' Moscow']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

plain lens: ['遥遥', 'located', ' none', ' NOT', '心惊', '先到', '____', 'not', '日内', ' zuständig', 'otope', ')?$', '...\\', ' Fiction', '...', '万国', 'bur', 'seat', 'ẹo', ' dumps', 'seit', ' nullptr', ' democr', ' Luân', 'reis', ' Зо', 'više', 'none', '/is', '洛阳', 'also', '赔']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass J-lens: [' Paris', ' Zurich', ' Berlin', ' London', ' Switzerland', '巴黎', 'Paris', ' Brussels', ' Vienna', ' Zürich', ' France', ' Luxembourg', ' Stockholm', ' Madrid', ' Oslo', ' Munich', ' Amsterdam', ' Prague', ' Frankfurt', ' Bogotá', ' Montreal', ' París', ' Belgium', ' Bangkok', 'London', ' Dublin', ' Nairobi', ' Barcelona', ' Marseille', ' Londres', ' Rome', ' Moscow']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass plain24: ['遥遥', 'located', ' none', ' NOT', '心惊', '先到', '____', 'not', '日内', ' zuständig', 'otope', ')?$', '...\\', ' Fiction', '...', '万国', 'bur', 'seat', 'ẹo', ' dumps', 'seit', ' nullptr', ' democr', ' Luân', 'reis', ' Зо', 'više', 'none', '/is', '洛阳', 'also', '赔']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass plain27: ['日内', ' Washington', '北京', ' Washing', ' capitals', '首都', 'กรุง', 'usanne', '瑞士', ' swearing', ' Bras', '镐', '-capital', 'ابين', ' Hauptstadt', ' capitale', ' Жен', ' Capitals', 'Washington', '北京的', ' Swiss', '_gene', '直流', ' กรุง', ' Etter', ' Beijing', 'wash', '存在', 'više', 'ブリ', ' Brussels', ' ژ']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased1 J-lens: [' Paris', '巴黎', ' London', ' Zurich', 'Paris', ' Switzerland', ' Brussels', ' Vienna', ' Berlin', ' France', ' Madrid', ' Zürich', ' Luxembourg', ' Stockholm', ' Oslo', ' Munich', ' Prague', ' Amsterdam', ' París', ' Bogotá', ' Montreal', ' Nairobi', 'London', ' Frankfurt', ' Londres', ' Dublin', ' Belgium', ' Bangkok', '伦敦', ' Marseille', ' Moscow', ' Barcelona']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased0.5 J-lens: [' Paris', '巴黎', ' London', ' Zurich', 'Paris', ' Switzerland', ' Berlin', ' Brussels', ' Vienna', ' France', ' Zürich', ' Madrid', ' Luxembourg', ' Stockholm', ' Oslo', ' Munich', ' Amsterdam', ' Prague', ' París', ' Frankfurt', ' Bogotá', ' Montreal', ' Belgium', 'London', ' Nairobi', ' Bangkok', ' Dublin', ' Londres', ' Barcelona', '伦敦', ' Moscow', ' Marseille']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased1 plain24: ['遥遥', 'located', ' none', '心惊', ' NOT', '____', '先到', 'not', ' zuständig', '日内', ')?$', 'otope', '...\\', ' Fiction', '...', '万国', ' dumps', 'ẹo', 'seat', 'bur', ' nullptr', ' democr', 'seit', ' Luân', 'reis', 'none', 'više', '洛阳', ' Зо', 'also', '/is', ' NULL']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased0.5 plain24: ['遥遥', 'located', ' none', ' NOT', '心惊', '先到', '____', 'not', '日内', ' zuständig', ')?$', 'otope', '...\\', ' Fiction', '...', '万国', 'seat', 'bur', 'ẹo', ' dumps', ' nullptr', 'seit', ' Luân', ' democr', 'reis', ' Зо', 'više', 'none', ' شار', '洛阳', 'also', '/is']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased1 plain27: ['日内', ' Washing', ' capitals', '首都', ' Washington', '北京', 'กรุง', '镐', ' swearing', 'usanne', ' Hauptstadt', ' capitale', 'Washington', ' Жен', ' Bras', 'ابين', ' Capitals', '存在', '-capital', 'wash', ' Etter', '废水', 'više', '瑞士', '直流', '_gene', ' กรุง', 'ブリ', "'}).", '北京的', ' Lagu', 'äte']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Geneva is'

Baseline: ' Bern.\nQuestion: What is the'

end-pass erased0.5 plain27: ['日内', ' Washing', ' capitals', ' Washington', '首都', '北京', 'กรุง', 'usanne', ' swearing', '镐', '瑞士', ' Hauptstadt', ' capitale', ' Bras', 'Washington', 'ابين', '-capital', ' Capitals', ' Жен', ' Etter', 'wash', '存在', '直流', 'više', '_gene', ' กรุง', '废水', '北京的', 'ブリ', ' ژ', "'}).", ' Beijing']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

J-lens: [' Paris', ' London', ' Rome', ' Berlin', ' Italy', ' Madrid', ' Vienna', ' Athens', ' Amsterdam', 'Paris', ' Moscow', '巴黎', ' Frankfurt', ' Brussels', ' Budapest', ' Venice', 'London', ' Lisbon', ' NYC', ' Istanbul', ' Jakarta', ' Naples', ' Prague', ' Barcelona', ' Bologna', ' Dublin', ' Bogotá', ' Milan', ' Vatican', '伦敦', ' Stockholm', ' Jerusalem']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

plain lens: ['遥遥', ' Luân', 'više', '先到', '暂定', '้ม', '...\\', 'aches', 'rome', 'otope', ' correc', '名胜', '现', 'olon', 'oglio', 'reis', '担', ' zuständig', 'usalem', ' dumps', '北京', '}`).', ' NOT', ' ogs', '好评', '...).', '伟人', '美术学院', 'ovas', 'ẩm', '##_', 'acre']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass J-lens: [' Paris', ' London', ' Berlin', ' Italy', ' Madrid', ' Vienna', ' Athens', ' Amsterdam', 'Paris', ' Moscow', '巴黎', ' Frankfurt', ' Brussels', ' Budapest', ' Lisbon', ' Venice', ' NYC', 'London', ' Istanbul', ' Naples', ' Jakarta', ' Prague', ' Barcelona', ' Dublin', ' Bologna', ' Bogotá', '伦敦', ' Milan', ' Vatican', ' Jerusalem', ' Stockholm', ' Cairo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass plain24: ['遥遥', ' Luân', 'više', '先到', '暂定', '้ม', '...\\', 'aches', ' correc', 'otope', '名胜', 'olon', '现', 'oglio', 'reis', '担', ' zuständig', ' dumps', 'usalem', '北京', '}`).', ' NOT', ' ogs', '好评', '...).', '伟人', '美术学院', 'ẩm', 'ovas', '##_', '心惊', 'acre']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass plain27: [' Washington', '北京', ' Washing', ' Berlin', ' London', '罗马', '...', '北京的', 'Washington', ' capitale', 'กรุง', ' capitals', '首都', ' Paris', '东京', ' Beijing', '华盛顿', ' NOT', 'ฯ', ' Vatican', '____', ' washington', ' Hauptstadt', ' Bras', '镐', '京城', '的都', 'Google', ' thủ', '华府', ' Capitals', ' رم']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased1 J-lens: [' Paris', ' London', ' Berlin', ' Frankfurt', ' Amsterdam', '.\\', ' Vienna', ' Madrid', ' NYC', '?\\', ' Bogotá', '巴黎', 'Paris', ' City', ' Italy', ' Budapest', ' Atlanta', ' Barcelona', ' Heidelberg', ' Moscow', ' Istanbul', ' Oslo', ' Bologna', ' Karlsruhe', ' Johannesburg', '...\\', ' Dublin', 'London', '。\\', '伦敦', ' Jakarta', ' Buenos']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased0.5 J-lens: [' Paris', ' London', ' Berlin', ' Madrid', ' Italy', ' Vienna', ' Amsterdam', ' Frankfurt', 'Paris', '巴黎', ' NYC', ' Moscow', ' Budapest', ' Bogotá', ' Istanbul', 'London', ' Barcelona', ' Athens', ' Lisbon', ' Bologna', ' Brussels', ' Jakarta', ' Dublin', ' Atlanta', '伦敦', '.\\', ' Oslo', ' Prague', ' City', ' Stockholm', ' Heidelberg', ' Zurich']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased1 plain24: ['遥遥', '现', '先到', ' Luân', 'više', '...\\', '暂定', 'aches', '担', 'oglio', 'olon', '้ม', '...', '名胜', ' correc', ' zuständig', ' dumps', 'otope', 'reis', ' NOT', '}`).', '好评', '...”', '...).', '伟人', '现任', '................', ' ogs', ' unic', ' none', 'ovas', 'ток']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased0.5 plain24: ['遥遥', ' Luân', '先到', 'više', '现', '...\\', '暂定', 'aches', '้ม', ' correc', 'olon', '担', 'oglio', '名胜', 'otope', ' zuständig', 'reis', ' dumps', '}`).', ' NOT', '好评', '...).', '伟人', 'usalem', '...', ' ogs', '...”', '北京', 'ovas', '现任', '美术学院', '##_']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased1 plain27: ['...', '北京', ' Washington', ' Washing', '____', ' capitals', ' NOT', ' capitale', ' Bras', 'ฯ', '北京的', 'Washington', 'กรุง', '首都', '....', '好评', '马力', ' London', '镐', '华盛顿', '存在', 'DC', ' Berlin', '的都', 'nici', ' Hauptstadt', 'Google', '}`).', 'based', ' thủ', '蚁', '华府']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Florence is'

Baseline: ' Rome.\nHypothesis: The'

end-pass erased0.5 plain27: ['北京', ' Washington', '...', ' Washing', ' capitals', ' capitale', '____', '北京的', ' London', 'Washington', ' NOT', 'กรุง', ' Berlin', '首都', 'ฯ', ' Bras', '华盛顿', '东京', ' Hauptstadt', '镐', ' Paris', '好评', ' Beijing', ' washington', '马力', '的都', 'DC', 'Google', ' thủ', '}`).', '华府', ' Capitals']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

J-lens: [' Bogotá', ' Madrid', ' Buenos', ' Jakarta', ' Vienna', ' Caracas', ' Lisbon', ' Nairobi', ' Brasília', ' Prague', ' Lima', ' Bangkok', ' Ciudad', ' Denver', ' Peru', ' Paris', ' Budapest', ' Berlin', ' Islamabad', 'Madrid', ' Rome', ' Barcelona', ' Santiago', ' Philadelphia', ' London', ' Amsterdam', ' Manila', ' Johannesburg', ' Washington', ' Taipei', ' Bolivia', ' Rio']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

plain lens: ['先到', ' pano', 'lima', 'lis', ' correc', 'umed', 'urin', ' celu', ')?$', 'に行ってきました', 'rome', 'reis', ' egt', '...\\', 'tage', '遥遥', 'elda', ' alred', '吉隆', '省会', '蝇', '马拉', ' Chin', '过神', ' unic', '雄鹰', 'риста', ' ogs', '编辑于', 'alos', 'ถัด', 'リー']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass J-lens: [' Bogotá', ' Madrid', ' Buenos', ' Jakarta', ' Vienna', ' Caracas', ' Lisbon', ' Nairobi', ' Brasília', ' Prague', ' Bangkok', ' Ciudad', ' Denver', ' Peru', ' Paris', ' Budapest', ' Berlin', ' Islamabad', ' Rome', 'Madrid', ' Barcelona', ' Santiago', ' Philadelphia', ' London', ' Amsterdam', ' Manila', ' Johannesburg', ' Washington', ' Taipei', ' Bolivia', ' Rio', ' NYC']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass plain24: ['先到', ' pano', 'lis', ' correc', 'urin', 'umed', ')?$', ' celu', 'に行ってきました', 'rome', 'reis', ' egt', '...\\', 'tage', 'elda', '遥遥', ' alred', '吉隆', '省会', '蝇', '马拉', ' Chin', '过神', ' unic', '雄鹰', 'риста', '编辑于', ' ogs', 'alos', 'リー', 'ถัด', ' finalist']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass plain27: [' capitale', '乌鲁', '-capital', ' capitals', 'acha', ' thủ', 'usco', ' Lime', ' столиц', 'achu', 'acas', 'chu', 'ลิป', ' Capitals', 'หลวง', 'クス', '秘鲁', ' Limo', ' столице', ' Hauptstadt', '资本', ' Tahu', 'urin', 'conde', ' inca', ' pach', ' Lemb', ' Pach', '大圣', ' reinc', '呼び', '首都']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased1 J-lens: [' Bogotá', ' Madrid', ' Buenos', ' Vienna', ' Jakarta', ' Paris', ' Nairobi', ' Prague', ' Denver', ' Berlin', ' Bangkok', ' Ciudad', ' Budapest', ' Barcelona', ' Brasília', ' Washington', ' Rome', ' London', ' Lisbon', ' Caracas', ' Philadelphia', ' Islamabad', ' Johannesburg', ' Amsterdam', '.\\', ' Santiago', 'Madrid', ' Kuala', ' City', ' Taipei', ' Miami', ' NYC']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased0.5 J-lens: [' Bogotá', ' Madrid', ' Buenos', ' Vienna', ' Jakarta', ' Nairobi', ' Brasília', ' Prague', ' Paris', ' Bangkok', ' Lisbon', ' Denver', ' Caracas', ' Ciudad', ' Budapest', ' Berlin', ' Barcelona', ' Rome', ' Islamabad', ' London', ' Peru', ' Washington', ' Philadelphia', 'Madrid', ' Santiago', ' Johannesburg', ' Amsterdam', ' Taipei', ' Dublin', ' NYC', ' Kuala', ' Miami']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased1 plain24: ['先到', ' pano', 'umed', ' correc', ')?$', ' celu', 'lis', '...\\', '蝇', 'urin', '遥遥', 'に行ってきました', 'reis', '吉隆', ' Chin', '省会', ' unic', 'tage', 'elda', 'rome', ' egt', 'ถัด', '马拉', '编辑于', '雄鹰', '过神', 'alos', ' alred', ' ogs', 'リー', ' finalist', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased0.5 plain24: ['先到', ' pano', 'lis', ' correc', 'umed', ')?$', ' celu', 'urin', 'に行ってきました', '...\\', 'reis', 'rome', '遥遥', ' egt', '蝇', '吉隆', 'tage', 'elda', '省会', ' Chin', ' unic', ' alred', '马拉', '过神', '雄鹰', 'ถัด', '编辑于', ' ogs', 'alos', 'リー', ' finalist', 'риста']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased1 plain27: [' capitale', '乌鲁', 'acha', ' capitals', ' thủ', '-capital', ' столиц', 'achu', 'chu', 'usco', 'acas', ' pach', 'หลวง', '资本', 'クス', ' reinc', '大圣', ' Pach', ' Capitals', '号的', 'ลิป', 'Call', '首都', ' })).', '呼び', ' столице', ' Hauptstadt', ' Lime', ' Call', ' epis', 'quí', 'kow']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Cusco is'

Baseline: ' Lima.\nQuestion: What is the'

end-pass erased0.5 plain27: [' capitale', '乌鲁', ' capitals', 'acha', '-capital', ' thủ', ' столиц', 'usco', 'achu', 'chu', 'acas', ' Lime', 'หลวง', 'クス', ' Capitals', 'ลิป', '资本', ' pach', ' Pach', ' reinc', '大圣', ' столице', ' Hauptstadt', 'conde', '首都', '呼び', 'urin', '号的', '秘鲁', ' Lemb', ' Tahu', ' })).']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

J-lens: [' Buenos', ' Madrid', ' Bogotá', ' Paris', ' Lisbon', ' Santiago', ' Vienna', ' Caracas', ' Dublin', ' City', ' Barcelona', ' Prague', ' Oslo', ' London', ' Nairobi', ' Honolulu', ' Ciudad', ' Chile', ' Copenhagen', ' Berlin', ' Seoul', ' Portland', ' Toronto', ' Amsterdam', ' NYC', ' Seattle', ' Washington', ' Auckland', ' Porto', ' Lima', ' Brasília', ' Manila']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

plain lens: ['urin', '金斯', '檀', ' NOT', 'AGENT', 'kow', 'lay', 'しば', ' alred', ' correc', '…]', 'lima', '遥遥', '省会', '心惊', 'not', ' theirs', 'više', ' zod', '"]\').', 'located', ' called', 'otope', '先到', '...).', '...”', 'umed', ' Chin', ' shootout', 'tage', '____', '้ม']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass J-lens: [' Buenos', ' Madrid', ' Bogotá', ' Paris', ' Lisbon', ' Vienna', ' Caracas', ' Dublin', ' City', ' Prague', ' Barcelona', ' London', ' Nairobi', ' Oslo', ' Ciudad', ' Honolulu', ' Chile', ' Copenhagen', ' Berlin', ' Seoul', ' Portland', ' Toronto', ' Amsterdam', ' Washington', ' NYC', ' Seattle', ' Porto', ' Auckland', ' Brasília', ' Lima', ' Manila', ' Denver']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass plain24: ['urin', '金斯', '檀', ' NOT', 'AGENT', 'kow', 'lay', 'しば', ' alred', ' correc', '…]', 'lima', '遥遥', '省会', '心惊', 'not', ' theirs', 'više', ' zod', '"]\').', 'located', ' called', 'otope', '先到', '...).', '...”', 'umed', ' Chin', ' shootout', 'tage', '____', '้ม']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass plain27: [' capitale', ' capitals', '首都', '金斯', 'lima', '地亚', ' NOT', '资本', '-capital', ' العاصمة', ' Anch', '单品', 'laufen', ' столиц', ' capitalist', '檀', 'called', 'lah', 'AGENT', ' Capitals', 'based', '省会', ' Hauptstadt', '大圣', ' Lima', ' thủ', 'Сан', '圣', 'Ch', ' Vina', ' Chil', ' alred']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased1 J-lens: [' Paris', ' Madrid', ' Vienna', ' Bogotá', ' Buenos', ' City', ' London', ' Lisbon', ' Berlin', ' Dublin', ' Oslo', ' Toronto', ' Barcelona', ' Chicago', ' Prague', ' Caracas', ' Honolulu', ' Boston', ' NYC', ' Amsterdam', ' Ciudad', ' Seoul', ' Portland', ' Moscow', ' Seattle', ' Porto', ' Denver', ' Philadelphia', ' Copenhagen', ' Washington', ' Montreal', ' city']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased0.5 J-lens: [' Buenos', ' Paris', ' Madrid', ' Bogotá', ' Vienna', ' Lisbon', ' City', ' London', ' Dublin', ' Caracas', ' Berlin', ' Oslo', ' Prague', ' Barcelona', ' Toronto', ' Honolulu', ' Ciudad', ' Seoul', ' Amsterdam', ' Copenhagen', ' Nairobi', ' Portland', ' NYC', ' Seattle', ' Porto', ' Washington', ' Boston', ' Chicago', ' Denver', ' Philadelphia', ' Auckland', ' Montreal']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased1 plain24: [' NOT', '檀', '金斯', 'urin', 'lay', 'しば', 'AGENT', '...', 'kow', '遥遥', ' called', ' alred', ' correc', 'not', '____', '…]', 'lima', 'otope', 'umed', ' theirs', 'located', '省会', '心惊', ' Chin', '...”', ' zod', '"]\').', '...).', 'also', 'više', ' shootout', '...\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased0.5 plain24: ['urin', '金斯', '檀', ' NOT', 'lay', 'AGENT', 'しば', 'kow', ' alred', ' correc', '遥遥', '…]', 'lima', 'not', ' called', '...', '省会', ' theirs', '心惊', '____', 'otope', 'located', 'umed', ' zod', '...”', 'više', '"]\').', ' Chin', '...).', '先到', ' shootout', '...\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased1 plain27: [' capitale', ' capitals', ' NOT', '资本', '首都', '金斯', '檀', 'lima', ' Anch', 'based', 'Ch', 'called', ' العاصمة', '-capital', ' capitalist', ' thủ', '...', '单品', 'AGENT', 'laufen', ' called', ' Capitals', 'NOT', 'lah', ' столиц', '称为', ' Hauptstadt', '省会', '地亚', 'also', '圣', '户']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The capital of the country containing Valparaiso is'

Baseline: ' Santiago.\nHypothesis: Val'

end-pass erased0.5 plain27: [' capitale', ' capitals', '首都', '金斯', ' NOT', '资本', 'lima', '檀', ' Anch', ' العاصمة', '-capital', '地亚', 'called', ' capitalist', 'based', '单品', ' столиц', 'laufen', ' thủ', 'Ch', 'AGENT', 'lah', ' Capitals', '省会', ' Hauptstadt', '大圣', 'NOT', '称为', '圣', ' Lima', '名城', ' called']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

J-lens: [' lungs', ' underwater', ' aquatic', ' aquarium', ' swim', ' whales', ' whale', ' belly', ' submerged', ' swimming', ' oceans', ' pores', ' muscles', ' submarine', ' seafood', ' marine', '潜水', ' kidneys', ' mouth', '___', ' coral', ' snork', ' swims', ' respiratory', ' stomach', ' seaw', '在水中', ' submarines', '鲸', '__.', ' body', ' fish']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

plain lens: [' lungs', '庞大', ' own', ' entirety', '庞大的', ' underwater', ' submerged', '在水中', ' swim', ' совокуп', 'smouth', ' Reef', 'own', 'ấu', ' aquarium', ' breathed', 'razil', 'OWN', '潜水', '在水里', '水表', ' breathe', 'piring', ' Chambers', ' jeweil', ' Entire', 'uctor', '……………………', ' organs', 'expired', '/her', '협']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass J-lens: [' lungs', ' underwater', ' aquatic', ' aquarium', ' swim', ' whales', ' whale', ' belly', ' submerged', ' swimming', ' oceans', ' pores', ' muscles', ' submarine', ' seafood', ' marine', '潜水', ' kidneys', ' mouth', '___', ' coral', ' snork', ' swims', ' respiratory', ' stomach', ' seaw', '在水中', ' submarines', '鲸', '__.', ' body', ' fish']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass plain24: [' lungs', '庞大', ' own', ' entirety', '庞大的', ' underwater', ' submerged', '在水中', ' swim', ' совокуп', 'smouth', ' Reef', 'own', 'ấu', ' aquarium', ' breathed', 'razil', 'OWN', '潜水', '在水里', '水表', ' breathe', 'piring', ' Chambers', ' jeweil', ' Entire', 'uctor', '……………………', ' organs', 'expired', '/her', '협']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass plain27: [' lungs', ' swim', 'lungs', ' breathe', 'haled', ' respiratory', '�', 'smouth', ' gigantic', ' organs', '庞大', '肺腑', ' bale', ' entirety', 'expanded', '肺', 'ânia', ' eget', '肺部', ' lung', '庞大的', '体表', ' mouth', '宽广', ' органами', ' swims', 'mouth', 'utilus', 'leben', 'EXTERNAL', 'resher', ' specialised']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased1 J-lens: [' lungs', ' underwater', ' aquatic', ' aquarium', ' swim', ' whales', ' whale', ' belly', ' submerged', ' oceans', ' swimming', ' pores', '潜水', ' submarine', ' seafood', ' muscles', ' kidneys', ' marine', ' snork', ' swims', ' mouth', '___', ' coral', ' respiratory', ' submarines', '鲸', ' stomach', ' sails', '在水中', ' squid', '__.', ' seaw']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased0.5 J-lens: [' lungs', ' underwater', ' aquatic', ' aquarium', ' swim', ' whales', ' whale', ' belly', ' submerged', ' swimming', ' oceans', ' pores', ' muscles', '潜水', ' submarine', ' seafood', ' marine', ' kidneys', ' snork', '___', ' mouth', ' coral', ' swims', ' respiratory', ' submarines', ' stomach', '鲸', ' seaw', '在水中', '__.', ' sails', ' abdomen']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased1 plain24: ['庞大', ' lungs', ' own', ' entirety', '庞大的', ' underwater', 'smouth', ' совокуп', ' submerged', '在水中', ' swim', ' Reef', 'razil', 'ấu', 'OWN', ' breathed', ' aquarium', ' jeweil', '潜水', 'own', '水表', '在水里', 'piring', ' breathe', 'ércio', 'uctor', 'expired', ' Entire', '……………………', ' Chambers', '협', '[].']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased0.5 plain24: [' lungs', '庞大', ' own', ' entirety', '庞大的', ' underwater', ' submerged', '在水中', ' совокуп', ' swim', 'smouth', ' Reef', 'ấu', ' aquarium', 'razil', 'own', 'OWN', ' breathed', '潜水', '水表', '在水里', ' jeweil', 'piring', ' breathe', 'uctor', ' Entire', ' Chambers', 'expired', '……………………', 'ércio', '/her', ' organs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased1 plain27: [' lungs', 'lungs', ' swim', 'haled', ' breathe', ' respiratory', 'smouth', ' gigantic', '肺腑', '�', '庞大', 'ânia', ' organs', ' bale', ' entirety', ' Kasat', ' eget', 'expanded', '肺部', '肺', '体表', ' органами', 'resher', '庞大的', 'leben', ' specialised', 'EXTERNAL', '宽广', 'будьте', 'ordi', 'utilus', 'vej']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The breathing organ of the largest animal in the ocean is its'

Baseline: ' gills.\nQuestion: What is'

end-pass erased0.5 plain27: [' lungs', ' swim', 'lungs', 'haled', ' breathe', ' respiratory', 'smouth', ' gigantic', '�', '肺腑', ' organs', '庞大', ' bale', ' entirety', 'expanded', 'ânia', ' eget', '肺', '肺部', ' Kasat', '体表', '庞大的', '宽广', ' органами', 'utilus', 'resher', ' lung', ' mouth', 'leben', ' specialised', 'mouth', ' swims']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

J-lens: [' mammals', ' animals', ' Animals', ' insects', ' birds', ' creatures', 'animals', ' organisms', ' dinosaurs', ' Birds', ' mamm', ' beasts', ' rept', ' rodents', ' Creatures', ' amphib', ' butterflies', 'birds', ' species', ' Species', '哺乳', '动物的', ' fishes', ' verte', ' dinosaur', ' creature', ' humans', ' parasites', '动物', '的动物', ' predators', ' insect']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

plain lens: [' mammals', '哺乳', 'flight', 'spinner', 'ordnung', '人马', '国家一级', '恒温', ' sorts', 'ambul', 'sess', ' noct', 'orders', '统称', ' mamm', ' superclass', ' 분류', ' Ordnung', '吵闹', '-flight', ' Orders', '属', 'stackpath', '固醇', '该类', 'աս', 'thes', '教体', 'uyệt', '折不扣', ' Dici', 'living']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass J-lens: [' animals', ' Animals', ' insects', ' birds', ' creatures', 'animals', ' organisms', ' dinosaurs', ' Birds', ' beasts', ' rept', ' rodents', ' Creatures', ' amphib', ' butterflies', 'birds', ' species', '哺乳', ' Species', '动物的', ' fishes', ' verte', ' dinosaur', ' creature', ' humans', ' parasites', '的动物', '动物', '昆虫', ' carniv', ' insect', ' predators']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass plain24: ['哺乳', 'flight', 'spinner', 'ordnung', '人马', '国家一级', ' sorts', '恒温', 'ambul', 'sess', ' noct', 'orders', '统称', ' superclass', ' 분류', ' Ordnung', '吵闹', ' Orders', 'stackpath', '-flight', '属', '该类', '固醇', 'աս', 'thes', '教体', 'uyệt', '折不扣', ' Dici', 'living', '温带', ' taxonomy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass plain27: [' birds', ' Orders', ' orders', 'order', '哺乳', 'orders', ' animals', 'flight', ' flight', ' Birds', ' bird', 'Bird', ' Flight', '-flight', ' volant', ' order', ' aves', '飞行', 'Flight', 'bird', ' Order', ' rept', ' verte', 'birds', 'ordnung', 'warm', ' Verte', ' feathers', '鸟类', 'Order', ' Bird', ' noct']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased1 J-lens: ['.\\', ' animals', ' \\"', '\\"', ' birds', '\\', ' creatures', ' __', '___', '\\n', ' insects', ' bird', ' biological', ' species', ' rept', ' \\', '____', ' amphib', '.', ' Animals', ' organisms', ' insect', '。\\', ' ___', ':', '__', ' creature', ' Birds', ' dinosaurs', ' dinosaur', '\\u', ' Mac']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased0.5 J-lens: [' animals', ' birds', ' Animals', ' creatures', ' insects', ' organisms', ' dinosaurs', ' rept', ' Birds', ' amphib', '.\\', 'animals', ' species', ' beasts', ' biological', ' bird', ' \\"', '\\"', ' butterflies', ' Creatures', ' insect', ' creature', ' dinosaur', ' aquatic', ' parasites', ' Species', '___', '昆虫', '。\\', ' Biology', ' organism', ' carniv']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased1 plain24: [':', '...', '属', 'flight', 'spinner', 'ordnung', 'thes', ' sorts', '人马', ' noct', 'աս', '恒温', ' 분류', ' superclass', 'sess', '吵闹', '该类', 'orders', 'order', 'living', ' Orders', ' Ordnung', '统称', '凿', ' Flight', 'ряду', ' oblig', '教体', ' specimen', '_', '总部', ' interest']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased0.5 plain24: ['flight', 'spinner', 'ordnung', '属', '人马', ' sorts', '恒温', ' noct', 'thes', 'sess', ' superclass', ' 분류', '国家一级', '哺乳', 'orders', '统称', 'աս', '吵闹', '该类', ' Ordnung', ' Orders', 'living', 'ambul', '教体', '固醇', '-flight', 'ряду', 'order', ' Flight', '温带', 'blatt', ' taxonomy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased1 plain27: [' orders', 'order', ' order', ' flight', ' Orders', ' bird', 'orders', ':', ' Flight', '飞行', ' Order', 'flight', ' birds', 'Flight', ' ', 'Bird', 'Order', 'bird', '-flight', ' Bird', 'ordnung', ' feathers', ',', ' noct', '?', '.', 'warm', ' wing', ' volant', ' Birds', '订单', '...']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The flying animal that sleeps upside down belongs to the class of'

Baseline: ' mammals.\nQuestion: What is the'

end-pass erased0.5 plain27: [' orders', 'order', ' Orders', ' birds', ' flight', 'orders', ' order', ' bird', 'flight', ' Flight', '飞行', ' Order', 'Bird', 'Flight', '-flight', ' Birds', 'bird', ' volant', 'Order', ' Bird', ' animals', 'ordnung', ' aves', ' feathers', 'warm', ' noct', ' rept', '.order', 'wing', '鸟类', ' Verte', '订单']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

J-lens: ['.\\', '?\\', '___', '.\\"', ').\\', '____', '...\\', '。\\', ' Gecko', '__.', '__', ' typically', ' seven', ':\\', ' snakes', ' lizard', ' twelve', '\\"', ' ___', ' mammals', '.**', ' five', ' elephants', '________', ' twenty', '\\u', ' six', ' four', ' rept', ' thirteen', ' eight', ' thirty']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

plain lens: ['više', '很好奇', '.numberOf', ' uff', ' licked', ' Gecko', ' warta', '.trailing', 'gues', '远流', 'numberOf', ':number', ' truff', '通常为', 'omers', '总数', 'instanc', '确定为', ' sertifik', '很好吃', 'shed', 'rapper', 'typically', '�', 'spinner', 'usually', '(number', 'の販', '頂けます', ' massag', '博物', 'lobber']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass J-lens: ['.\\', '?\\', '___', '.\\"', ').\\', '____', '...\\', '。\\', ' Gecko', '__.', '__', ' typically', ' seven', ':\\', ' snakes', ' lizard', ' twelve', '\\"', ' ___', ' mammals', '.**', ' five', ' elephants', '________', ' twenty', '\\u', ' six', ' four', ' rept', ' thirteen', ' eight', ' thirty']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain24: ['više', '很好奇', '.numberOf', ' uff', ' licked', ' Gecko', ' warta', '.trailing', 'gues', '远流', 'numberOf', ':number', ' truff', '通常为', 'omers', '总数', 'instanc', '确定为', ' sertifik', '很好吃', 'shed', 'rapper', 'typically', '�', 'spinner', 'usually', '(number', 'の販', '頂けます', ' massag', '博物', 'lobber']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain27: [' Gecko', '很好奇', 'numberOf', ' snakes', 'ssue', ' tongues', '商机', '多いです', 'usually', '.numberOf', 'plural', '依法须经', ' venom', 'HomePage', 'zero', ' dinas', 'epad', 'snake', 'normally', '爬虫', ' ZERO', '进出口业务', '经相关部门批准', 'LOTS', 'typically', ' laba', ' Чере', '.gradle', '吻', 'の販', '舌头', ' licked']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 J-lens: ['?\\', '.\\', '.\\"', ').\\', '...\\', ' Gecko', '___', '__.', '。\\', '____', '».**', ' snakes', ' lizard', ' seven', 'dogs', ' mammals', ':\\', ' twelve', ' elephants', ' thirteen', '...**', '\\"\\', ' typically', ' .**', '.**', ' claws', '__', 'numberOf', '.*)', '(number', ' thirty', ' ___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 J-lens: ['.\\', '?\\', '.\\"', ').\\', '___', '...\\', ' Gecko', '。\\', '__.', '____', ' seven', ' snakes', ' lizard', '__', ' typically', ':\\', ' twelve', ' mammals', '».**', '.**', ' elephants', ' ___', 'dogs', ' thirteen', '\\"', '\\"\\', ' claws', ' five', ' thirty', ' twenty', '(number', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 plain24: ['很好奇', '.numberOf', 'više', ' Gecko', '通常为', ' licked', ' uff', '.trailing', 'numberOf', '总数', 'typically', 'omers', 'usually', ':number', '(number', 'gues', '�', ' truff', '确定为', '吻', 'shed', '远流', 'spinner', ' warta', '很好吃', 'lobber', 'rapper', '博物', ' tongues', '扬子', ' usus', '_number']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 plain24: ['više', '很好奇', '.numberOf', ' Gecko', ' uff', ' licked', '.trailing', '通常为', 'numberOf', ':number', ' warta', 'omers', 'gues', '总数', '远流', ' truff', 'typically', 'usually', '(number', '�', 'shed', '确定为', 'rapper', 'spinner', '很好吃', 'lobber', '博物', '吻', 'instanc', ' usus', '玩儿', ' sertifik']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 plain27: [' Gecko', '很好奇', 'numberOf', ' snakes', 'ssue', ' tongues', '商机', '多いです', 'usually', '.numberOf', 'plural', '依法须经', ' venom', 'HomePage', 'zero', ' dinas', 'epad', 'snake', 'normally', ' ZERO', '爬虫', '进出口业务', '经相关部门批准', 'LOTS', ' laba', 'typically', ' Чере', '吻', 'の販', '.gradle', '舌头', ' licked']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that slithers and has a forked tongue is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 plain27: [' Gecko', '很好奇', 'numberOf', ' snakes', 'ssue', ' tongues', '商机', '多いです', 'usually', '.numberOf', 'plural', '依法须经', ' venom', 'HomePage', 'zero', ' dinas', 'epad', 'snake', 'normally', '爬虫', ' ZERO', '进出口业务', '经相关部门批准', 'LOTS', 'typically', ' laba', ' Чере', '.gradle', '吻', 'の販', '舌头', ' licked']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

J-lens: [' carrot', ' carrots', ' potatoes', ' potato', ' cabbage', ' lettuce', ' mushroom', ' tuber', '胡萝卜', ' garlic', ' roots', '萝卜', ' Potato', ' banana', '___', ' peanuts', '_____', ' mushrooms', ' tomato', ' bananas', ' pineapple', ' Roots', '____', ' vegetables', '__.', ' onion', 'paragus', ' onions', ' pumpkin', ' apple', ' peanut', 'roots']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

plain lens: ['根', '根的', '_root', '两根', ' roots', ' rooting', 'roots', ' Roots', 'rots', 'parser', ' surprises', '根深', '掘', '地产', ' Mots', '구', ' commonly', 'izona', ' Syrians', ' корне', '/root', '-root', ' diken', 'OTH', 'ikon', '快照', '晗', ' underground', '_lex', ' carrots', 'embed', 'lector']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass J-lens: [' potatoes', ' potato', ' cabbage', ' lettuce', ' mushroom', ' tuber', '胡萝卜', ' garlic', ' roots', ' Potato', '萝卜', ' banana', '___', ' peanuts', '_____', ' mushrooms', ' tomato', ' pineapple', ' bananas', ' Roots', '____', ' vegetables', '__.', ' onion', 'paragus', ' onions', ' pumpkin', ' apple', ' peanut', 'roots', ' cauliflower', ' Garlic']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass plain24: ['根', '根的', '_root', '两根', ' roots', ' rooting', 'roots', ' Roots', 'rots', 'parser', ' surprises', '根深', '掘', '地产', ' Mots', '구', ' commonly', 'izona', ' Syrians', ' корне', '/root', '-root', ' diken', 'OTH', 'ikon', '快照', '晗', ' underground', '医学会', '_lex', 'embed', 'lector']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass plain27: ['根', '_root', '根的', '这根', '-root', ' roots', '/root', '两根', ' Roots', '.root', '_ROOT', '根部', 'roots', ' корне', ' radic', 'rad', '(root', ' rooting', '根深', '[root', ' rad', ' корни', ' 뿌', ' raíz', 'ราก', ' radici', 'icama', 'qrt', '一根', ' tuber', 'celer', '_car']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased1 J-lens: [' potatoes', '____', '_____', '___', ' roots', '________', '.\\', '.', '\\n', '__', ' potato', ' ____', ' ___', ' garlic', ' _____', ' tuber', ' tub', ' Roots', ' __', ' plant', '?', '__.', ' mushrooms', ' peanuts', ' cabbage', ' mushroom', ' lettuce', ' ______', ' ________', ' bananas', '_________', ' vegetables']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased0.5 J-lens: [' potatoes', ' potato', '___', '____', '_____', ' roots', ' cabbage', ' tuber', ' garlic', ' lettuce', ' mushroom', '________', ' peanuts', ' mushrooms', ' Roots', '.\\', '__.', ' Potato', ' ____', ' banana', ' bananas', ' vegetables', ' _____', ' plant', '萝卜', ' ___', ' onions', '__', ' pineapple', '\\n', ' tub', '根']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased1 plain24: ['根', '根的', '_root', '两根', ' roots', ' Roots', 'parser', 'roots', ' rooting', '구', ' surprises', '掘', ' commonly', '地产', 'rots', '根深', 'ikon', ' Mots', ' companions', '____', '常见', 'embed', 'izona', ' underground', ' Syrians', 'lector', 'OTH', ' Underground', ' diken', '晗', '-root', 'common']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased0.5 plain24: ['根', '根的', '两根', '_root', ' roots', 'roots', ' rooting', ' Roots', 'parser', ' surprises', '掘', 'rots', '구', ' commonly', '地产', '根深', ' Mots', 'izona', ' Syrians', 'ikon', ' diken', 'OTH', ' underground', 'embed', ' корне', ' companions', '-root', '/root', '晗', 'lector', '常见', ' Underground']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased1 plain27: ['根', '_root', ' roots', '根的', '这根', '-root', ' Roots', '两根', '_ROOT', '.root', '/root', '根部', 'rad', 'roots', ' rad', ' radic', '(root', ' корне', '根深', ' rooting', '[root', ' корни', ' raíz', ' 뿌', 'sqrt', '一根', ' radici', 'ราก', 'qrt', ' bulb', 'turn', ' bulbs']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The root vegetable associated with the animal that says 'What's up, Doc?' is a"

Baseline: ' carrot.\nQuestion: What is the'

end-pass erased0.5 plain27: ['根', '_root', '这根', '根的', '-root', ' roots', '两根', ' Roots', '/root', '.root', '_ROOT', '根部', 'roots', 'rad', ' корне', ' radic', '(root', ' rad', '根深', ' rooting', '[root', ' корни', ' 뿌', ' raíz', 'ราก', ' radici', '一根', 'qrt', 'sqrt', 'icama', ' tuber', ' rễ']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

J-lens: [' honey', ' Honey', '蜂蜜', ' peanuts', ' candy', ' chocolate', ' sweets', ' Chocolate', ' Milk', ' Peanut', ' peanut', ' Candy', ' chocolates', ' pudding', ' apples', ' yogurt', ' candies', ' cinnamon', ' cheese', ' bananas', ' Pork', ' Teddy', ' milk', ' Roses', ' Cheese', ' biscuits', ' Mickey', ' Rabbit', ' Sugar', ' roses', '棉花糖', ' Ginger']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

plain lens: ['...', '金奖', '湖区', ' Rhodes', 'rovers', '罗德', '无锡', '无锡市', '刨', 'грузка', 'ney', ' honey', '一票', '粉丝', '速度慢', ' bears', '麒', '�', 'منة', 'enade', 'ỏi', 'ọng', '太过', '........', 'arro', 'visibility', '记', '甜的', '甜甜的', ' Literatura', '眯眯', '兑现']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass J-lens: ['蜂蜜', ' peanuts', ' candy', ' chocolate', ' sweets', ' Chocolate', ' Milk', ' Peanut', ' peanut', ' chocolates', ' Candy', ' pudding', ' apples', ' yogurt', ' candies', ' cinnamon', ' cheese', ' bananas', ' Pork', ' Teddy', ' milk', ' Roses', ' Cheese', ' biscuits', ' Rabbit', ' Mickey', ' roses', ' Sugar', '棉花糖', ' Ginger', ' Dairy', ' popcorn']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass plain24: ['...', '金奖', '湖区', ' Rhodes', 'rovers', '罗德', '无锡', '无锡市', '刨', 'грузка', 'ney', '一票', ' bears', '粉丝', '速度慢', '麒', '�', 'منة', 'enade', 'ỏi', '太过', 'ọng', '........', 'arro', 'visibility', '记', '甜的', '甜甜的', '眯眯', '兑现', ' Literatura', '_schema']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass plain27: ['蜂蜜', '蜜', '蜂巢', '湖区', ' bears', ' miel', ' mật', ' bees', '甜的', ' Mật', ' bear', 'poll', '金奖', ' treats', '甜甜的', ' preserves', '蜂窝', '跳跳', ' pek', '査', '蜂', ' пон', '巣', 'bear', '上传者', ' Bear', ' honor', '金斯', 'ריך', '.poll', ' imperialism', '⭐']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased1 J-lens: [' peanuts', ' chocolate', ' Chocolate', ' sweets', ' chocolates', ' Milk', ' apples', ' candy', ' Teddy', ' Peanut', ' pudding', ' bananas', ' biscuits', ' Roses', ' peanut', ' carrots', ' candies', ' roses', ' Pork', ' cupcakes', ' Cheese', ' Candy', ' Mickey', ' yogurt', ' Rabbit', '棉花糖', ' cinnamon', ' Cubs', ' pork', ' cheese', ' Dairy', ' Bear']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased0.5 J-lens: [' peanuts', ' chocolate', ' candy', ' sweets', ' Chocolate', ' Milk', ' chocolates', ' Peanut', ' pudding', ' apples', ' peanut', ' Candy', ' bananas', ' Teddy', ' candies', ' yogurt', ' biscuits', ' Roses', ' Pork', ' cinnamon', ' cheese', ' roses', ' Cheese', ' Mickey', ' carrots', '棉花糖', ' Rabbit', ' cupcakes', ' Dairy', ' milk', ' Bread', ' pork']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased1 plain24: ['...', 'rovers', '金奖', '刨', '罗德', '湖区', '无锡', 'грузка', ' Rhodes', '无锡市', '........', 'ney', '记', '�', ' bears', '粉丝', '..', '速度慢', '太过', 'ọng', '麒', 'ỏi', 'enade', '一票', ' Literatura', '腕', 'visibility', 'ogram', ' invis', 'منة', '兑现', 'arro']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased0.5 plain24: ['...', '金奖', 'rovers', '湖区', '罗德', '刨', ' Rhodes', 'грузка', '无锡', '无锡市', 'ney', '........', '粉丝', ' bears', '�', '速度慢', '麒', '记', 'ọng', '太过', 'ỏi', '一票', 'enade', 'منة', 'visibility', 'arro', ' Literatura', '兑现', ' invis', '展览会', ' trị', '_schema']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased1 plain27: [' bears', '...', '湖区', ' treats', ' preserves', ' pek', 'rovers', ' bear', '⭐', ' Bear', 'poll', '金奖', '査', ' imperialism', '上传者', 'ריך', ' upro', ' пон', 'root', ' genellikle', '官兵', ' Pru', '粘', '小熊', '跳跳', '刨', '交通管制', 'poi', ' mật', '金斯', '甜甜的', 'usually']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The sweet food associated with the animal represented by Winnie-the-Pooh is'

Baseline: ' honey.\nHypothesis: The'

end-pass erased0.5 plain27: [' bears', '湖区', ' treats', '...', ' mật', ' preserves', ' bear', ' miel', '蜜', 'poll', ' pek', '金奖', 'rovers', ' Bear', '蜂巢', '査', '⭐', '甜的', '甜甜的', '上传者', ' imperialism', 'ריך', ' пон', ' Mật', '跳跳', ' upro', ' Pru', '粘', '官兵', '蜂蜜', ' genellikle', '金斯']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

J-lens: [' larvae', ' insects', ' nymph', '___', ' worms', ' butterfly', ' butterflies', ' beetle', ' mosquito', ' bees', ' magg', ' parasite', ' pollen', ' mosquitoes', ' tad', ' worm', ' baby', 'worm', ' fetus', ' embryo', '虫子', ' jelly', '_____', ' candy', ' honey', ' bee', ' puppy', '蛹', '昆虫', ' moth', ' ___', ' parasites']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

plain lens: ['投资基金', ' стадии', ' larvae', 'ersed', 'حلة', ' solchen', 'VERAGE', 'flies', '嗡嗡', '忘返', 'ướ', 'rowsers', '习性', ' tad', '벌', 'sworth', 'ööri', '阶', ' stade', '_emb', 'crawler', '{:', ' sucking', ' insects', 'hab', '...', '飞来', '栩栩', '外国语学校', 'atrix', 'arina', ' stages']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass J-lens: [' larvae', ' insects', ' nymph', '___', ' worms', ' butterfly', ' butterflies', ' beetle', ' mosquito', ' bees', ' magg', ' parasite', ' pollen', ' mosquitoes', ' tad', ' worm', ' baby', 'worm', ' fetus', ' embryo', '虫子', ' jelly', '_____', ' candy', ' honey', ' bee', ' puppy', '蛹', '昆虫', ' moth', ' ___', ' parasites']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass plain24: ['投资基金', ' стадии', ' larvae', 'ersed', 'حلة', ' solchen', 'VERAGE', 'flies', '嗡嗡', '忘返', 'ướ', 'rowsers', '习性', ' tad', '벌', 'sworth', 'ööri', '阶', ' stade', '_emb', 'crawler', '{:', ' sucking', ' insects', 'hab', '...', '飞来', '栩栩', '外国语学校', 'atrix', 'arina', ' stages']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass plain27: [' larvae', '蛹', ' nymph', 'ấu', 'worm', ' лич', ' magg', '蚜', '嗡嗡', 'flutter', '毛毛', 'หนอน', '虫子', '蜕变', ' pup', ' pests', 'opup', ' worm', ' crawler', ' parasite', ' insects', ' praying', '蛀', '虫', ' mosquito', 'sexual', '投资基金', ' parasites', 'sects', ' patriotism', ' beetle', ' buzzing']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased1 J-lens: [' larvae', '___', ' insects', ' nymph', ' worms', ' beetle', ' mosquito', ' butterfly', ' bees', ' butterflies', ' parasite', ' mosquitoes', ' pollen', ' embryo', '_____', ' magg', ' baby', ' ___', ' fetus', ' worm', '__', ' tad', ' jelly', 'worm', ' _____', '____', ' parasites', ' puppy', '虫子', ' candy', ' bee', '________']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased0.5 J-lens: [' larvae', ' insects', '___', ' nymph', ' worms', ' butterfly', ' beetle', ' butterflies', ' mosquito', ' bees', ' parasite', ' mosquitoes', ' pollen', ' magg', ' baby', ' embryo', ' worm', '_____', ' tad', ' fetus', 'worm', ' jelly', ' ___', '虫子', ' candy', ' _____', ' puppy', ' bee', ' parasites', ' honey', '__', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased1 plain24: ['投资基金', ' стадии', ' larvae', 'حلة', 'ersed', ' solchen', '...', '嗡嗡', '忘返', 'VERAGE', 'rowsers', 'flies', 'ướ', '习性', '_', 'ööri', '阶', 'sworth', 'hab', '_emb', ' stade', ' tad', '벌', '外国语学校', '{:', ' sucking', '飞来', ' insects', 'atrix', 'arina', ' называется', 'crawler']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased0.5 plain24: ['投资基金', ' стадии', ' larvae', 'ersed', 'حلة', ' solchen', '嗡嗡', '忘返', 'VERAGE', 'flies', 'ướ', 'rowsers', '习性', '...', 'sworth', 'ööri', '阶', ' tad', '_emb', '벌', ' stade', 'hab', '{:', ' sucking', 'crawler', ' insects', '_', '外国语学校', '飞来', 'arina', '栩栩', 'atrix']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased1 plain27: [' larvae', ' nymph', '蛹', '嗡嗡', ' лич', 'ấu', 'worm', ' pup', ' magg', '蚜', ' parasite', 'flutter', '蜕变', ' pests', '蛀', ' parasites', ' worm', '投资基金', ' mosquito', '虫子', ' называется', ' praying', ' insects', ' beetle', ' absoluta', ' patriotism', 'slug', 'opup', '____', ' buzzing', '虫', 'sexual']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The larval stage of the insect with colorful wings that visits flowers is called a'

Baseline: ' caterpillar.\nHypothesis:'

end-pass erased0.5 plain27: [' larvae', ' nymph', '蛹', 'ấu', 'worm', ' лич', '嗡嗡', ' magg', '蚜', ' pup', ' parasite', 'flutter', '蜕变', ' pests', '虫子', ' worm', '蛀', 'opup', 'หนอน', ' insects', ' mosquito', ' praying', ' crawler', ' parasites', '虫', '投资基金', ' patriotism', ' beetle', ' buzzing', 'sexual', ' называется', 'slug']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

J-lens: ['.\\', '?\\', ' typically', ').\\', '___', ' four', ' fours', ' six', '____', ' seven', ' five', ' animals', ' eight', ' twelve', '。\\', ' mammals', '...\\', ' usually', ' claws', ' Animals', '__.', '.\\"', ' elephants', 'dogs', '四条', ' Gecko', '________', '__', ':\\', 'typically', ' fourteen', ' ___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

plain lens: ['通常为', '.numberOf', 'typically', '很好奇', 'usually', '.trailing', ' typically', '总数', '�', ' licked', 'shed', 'gues', ':number', '远流', 'numberOf', ' pupper', 'Trail', 'wane', '痊', 'instanc', '庄镇', '沟村', ' usually', '一般为', ' warta', 'NumberOf', 'lobber', ' usus', ' سعد', '頂けます', 'goog', 'spinner']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass J-lens: ['.\\', '?\\', ' typically', ').\\', '___', ' four', ' fours', ' six', '____', ' seven', ' five', ' animals', ' eight', ' twelve', '。\\', ' mammals', '...\\', ' usually', ' claws', ' Animals', '__.', '.\\"', ' elephants', 'dogs', '四条', ' Gecko', '________', '__', ':\\', 'typically', ' fourteen', ' ___']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain24: ['通常为', '.numberOf', 'typically', '很好奇', 'usually', '.trailing', ' typically', '总数', '�', ' licked', 'shed', 'gues', ':number', '远流', 'numberOf', ' pupper', 'Trail', 'wane', '痊', 'instanc', '庄镇', '沟村', ' usually', '一般为', ' warta', 'NumberOf', 'lobber', ' usus', ' سعد', '頂けます', 'goog', 'spinner']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass plain27: ['很好奇', 'usually', ' typically', ' fours', 'typically', '四条', '_leg', ' usually', ' الأرج', ' FOUR', '.numberOf', 'numberOf', '通常为', '多いです', ' ZERO', '人类的', '通常情况下', '.zero', '複数', '下肢', 'NumberOf', '商机', ' four', ' _______,', '双腿', '偶', '庄镇', 'cão', '四通', '____', '所大学', ' Typically']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 J-lens: ['?\\', '.\\', ').\\', ' typically', ' fours', '...\\', '___', '。\\', '».**', ' mammals', ' animals', ' twelve', ' seven', '.\\"', 'dogs', ' Animals', '__.', ' claws', ' eight', ' four', ' Gecko', ' five', ' six', '四条', ' elephants', '____', '的动物', 'animals', ' fourteen', ' usually', ' FOUR', ' Dogs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 J-lens: ['.\\', '?\\', ').\\', ' typically', '___', ' fours', ' four', '。\\', '...\\', ' animals', ' seven', ' mammals', ' twelve', ' five', ' six', '____', ' eight', ' claws', ' Animals', '__.', '.\\"', 'dogs', ' Gecko', ' usually', ' elephants', '».**', '四条', ' fourteen', '的动物', 'animals', 'typically', ' FOUR']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 plain24: ['通常为', 'typically', '.numberOf', ' typically', 'usually', '很好奇', '总数', '.trailing', ' usually', '�', 'shed', 'numberOf', ':number', ' licked', 'Trail', 'gues', '一般为', '(number', '远流', 'NumberOf', ' usus', 'wane', 'lobber', '痊', '数', ' Typically', 'spinner', '通常', '庄镇', '习性', 'عادة', 'goog']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 plain24: ['通常为', 'typically', '.numberOf', ' typically', '很好奇', 'usually', '总数', '.trailing', 'shed', '�', ' licked', ':number', ' usually', 'gues', 'numberOf', '远流', 'Trail', '一般为', '痊', 'wane', 'NumberOf', '(number', '庄镇', 'lobber', ' usus', 'instanc', 'goog', 'spinner', ' pupper', 'عادة', '沟村', ' سعد']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased1 plain27: ['很好奇', ' typically', 'usually', 'typically', ' fours', '四条', ' usually', '_leg', ' الأرج', ' FOUR', 'numberOf', '通常为', '.numberOf', '人类的', ' ZERO', '多いです', '通常情况下', '.zero', ' four', '複数', '下肢', '偶', 'NumberOf', '商机', '双腿', ' _______,', '庄镇', '____', 'cão', ' Typically', '四通', '所大学']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of legs on the animal that rolls dung into balls is'

Baseline: ' 4.\nQuestion: How many'

end-pass erased0.5 plain27: ['很好奇', ' typically', 'usually', 'typically', ' fours', '四条', ' usually', '_leg', ' الأرج', ' FOUR', '.numberOf', '通常为', 'numberOf', '多いです', ' ZERO', '人类的', '通常情况下', '.zero', '複数', '下肢', ' four', 'NumberOf', '商机', '偶', '双腿', ' _______,', '庄镇', 'cão', '____', '四通', ' Typically', '所大学']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

J-lens: ['?\\', '.\\', ' seven', ' fourteen', ' forty', ' exactly', ' sixty', '...\\', ' eight', '___', ' four', ' twenty', ' twelve', ' five', ' equals', ' equal', ').\\', ' thirty', ' eighty', ' thirteen', '____', ' six', ' seventeen', ' fifteen', ':\\', ' ALWAYS', '.\\"', ' always', ' counted', ' sixteen', ' fifty', ' nine']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

plain lens: ['otope', ' totaled', '总数', 'olate', ' shells', 'versation', ' warta', ' قوله', '...\\', ' nota', 'LEGAL', 'nota', 'ovre', '招生考试', ' العدد', 'omers', 'olation', ' Fucking', ' massag', 'shed', 'tivo', 'oglio', ' exactly', ':number', '游刃', 'uzu', 'こだ', ' multiplied', '殼', ' الأرج', 'više', 'atria']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass J-lens: ['?\\', '.\\', ' seven', ' fourteen', ' forty', ' exactly', ' sixty', '...\\', ' eight', '___', ' four', ' twenty', ' twelve', ' five', ' equals', ' equal', ').\\', ' thirty', ' eighty', ' thirteen', '____', ' six', ' seventeen', ' fifteen', ':\\', ' ALWAYS', '.\\"', ' always', ' counted', ' sixteen', ' fifty', ' nine']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass plain24: ['otope', ' totaled', '总数', 'olate', ' shells', 'versation', ' warta', ' قوله', '...\\', ' nota', 'LEGAL', 'nota', 'ovre', '招生考试', ' العدد', 'omers', 'olation', ' Fucking', ' massag', 'shed', 'tivo', 'oglio', ' exactly', ':number', '游刃', 'uzu', 'こだ', ' multiplied', '殼', ' الأرج', 'više', 'atria']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass plain27: [' exactly', 'always', 'olate', ' totaled', ' ALWAYS', ' always', 'ssue', 'otope', '所大学', 'versation', 'greater', 'usually', '.EqualTo', ' greater', '.trailing', ' الأرج', ' trăng', 'actly', '多いです', '____', '?,?,?,?,', '庄镇', '...\\', '__:', 'periment', '不少于', 'COMMAND', ' معل', '商机', '_fixture', 'lobber', ' nota']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased1 J-lens: ['?\\', ' fourteen', '...\\', '.\\', ' seven', ').\\', ' sixty', ' forty', ' eighty', ' ALWAYS', ' seventeen', ' thirteen', '.\\"', ' twelve', ' eight', ' thirty', ' twenty', ' fifteen', ' sixteen', ' seventy', ' ninety', ' .**', ' equals', '___', ' fifty', ' exactly', ' five', ' counted', ' equal', ':\\', '。\\', ' four']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased0.5 J-lens: ['?\\', '.\\', ' fourteen', ' seven', ' forty', '...\\', ' sixty', ').\\', ' eighty', ' eight', ' twelve', ' thirteen', ' seventeen', ' ALWAYS', ' thirty', ' exactly', ' twenty', '___', ' equals', '.\\"', ' five', ' four', ' fifteen', ' equal', ' sixteen', ' fifty', ' seventy', ':\\', ' counted', ' six', ' ninety', '____']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased1 plain24: ['otope', ' totaled', '总数', 'olate', ' shells', 'versation', ' nota', ' exactly', ' قوله', '...\\', 'omers', 'olation', ' العدد', '招生考试', 'nota', 'LEGAL', ' multiplied', 'shed', 'ovre', '_number', ' warta', '(number', ' Fucking', 'uzu', ' counted', 'greater', ':number', 'multiply', 'द्ध', 'oglio', 'òng', 'photos']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased0.5 plain24: ['otope', ' totaled', '总数', 'olate', ' shells', 'versation', ' nota', '...\\', ' قوله', 'omers', 'LEGAL', ' العدد', '招生考试', ' exactly', 'olation', 'nota', ' warta', 'ovre', 'shed', ' multiplied', ' Fucking', 'uzu', ' massag', 'oglio', ':number', '_number', '殼', 'こだ', 'tivo', 'द्ध', 'multiply', '游刃']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased1 plain27: [' exactly', 'always', ' totaled', 'olate', ' ALWAYS', 'ssue', ' always', 'otope', 'versation', '所大学', '.EqualTo', 'greater', 'usually', '.trailing', ' الأرج', ' trăng', ' greater', 'actly', '多いです', '?,?,?,?,', '庄镇', '__:', '...\\', 'periment', '____', '不少于', 'COMMAND', ' معل', '商机', '_fixture', '招生考试', '依法须经']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The total number of legs, including the claws, on the animal that walks sideways and has a hard shell is'

Baseline: ' 10.\nQuestion: How'

end-pass erased0.5 plain27: [' exactly', 'always', 'olate', ' totaled', ' ALWAYS', ' always', 'ssue', 'otope', '所大学', 'versation', 'greater', '.EqualTo', 'usually', ' greater', '.trailing', ' الأرج', ' trăng', 'actly', '多いです', '?,?,?,?,', '庄镇', '____', '...\\', '__:', 'periment', '不少于', 'COMMAND', ' معل', '商机', '_fixture', '招生考试', 'lobber']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [J-lens](readout.json)     | 4/16                   |    0.801 | 2/13                     | 4/16             |          1 |
| [plain lens](readout.json) | 0/16                   |    0.735 | 0/13                     | 0/16             |          1 |

### End-of-pass readout (not for earlier edits)

| method                                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:-------------------------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [end-pass J-lens](readout.json)            | 11/16                  |    0.908 | 9/13                     | 11/16            |          1 |
| [end-pass erased0.5 J-lens](readout.json)  | 10/16                  |    0.915 | 8/13                     | 10/16            |          1 |
| [end-pass erased1 J-lens](readout.json)    | 9/16                   |    0.918 | 7/13                     | 9/16             |          1 |
| [end-pass erased1 plain27](readout.json)   | 6/16                   |    0.891 | 5/13                     | 6/16             |          1 |
| [end-pass plain27](readout.json)           | 5/16                   |    0.886 | 4/13                     | 8/16             |          1 |
| [end-pass erased0.5 plain27](readout.json) | 4/16                   |    0.889 | 3/13                     | 6/16             |          1 |
| [end-pass plain24](readout.json)           | 1/16                   |    0.844 | 1/13                     | 1/16             |          1 |
| [end-pass erased1 plain24](readout.json)   | 1/16                   |    0.840 | 1/13                     | 1/16             |          1 |
| [end-pass erased0.5 plain24](readout.json) | 1/16                   |    0.842 | 1/13                     | 1/16             |          1 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_125330_jlens-one-pass/run.md
