---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: None
translation_per_pair: 8
end_pass_readout: true
output_mask_max_n: 1
k: 32
elapsed_seconds: 54.99
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: First8 prefix-label-eligible words per pair in pinned CSV order; four-shot prompts use seed0 and script04 sampling. No output filtering. de→fr is development, five other de/fr/ru pairs are test; de→zh remains historical reference. English/Chinese hidden labels and their prefix lengths affect scoring only. Frozen after English development; no translation retuning. Concepts recur across language pairs, so prompts are not independent concepts. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method           | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:-----------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| cloud     | J-lens           | False         |                    |             1 |             1000000000 |                |              |
| cloud     | plain lens       | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass J-lens  | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain24 | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain27 | False         |                    |             0 |             1000000000 |                |              |
| bag       | J-lens           | True          |           0.980392 |            10 |                   1685 | True           | True         |
| bag       | plain lens       | True          |           0.911765 |             3 |                    198 | True           | True         |
| bag       | end-pass J-lens  | True          |           0.980392 |            10 |                   1685 | True           | True         |
| bag       | end-pass plain24 | True          |           0.911765 |             3 |                    198 | True           | True         |
| bag       | end-pass plain27 | False         |           0.960784 |             0 |                     16 | False          | False        |
| mouth     | J-lens           | False         |           0.970588 |             0 |                     10 | False          | False        |
| mouth     | plain lens       | True          |           0.980392 |             0 |                     52 | True           | True         |
| mouth     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27 | True          |           0.990196 |             0 |             1000000000 | True           | True         |
| soil      | J-lens           | True          |           0.885714 |             0 |                   6179 | True           | True         |
| soil      | plain lens       | True          |           0.952381 |             0 |                   5727 | True           | True         |
| soil      | end-pass J-lens  | True          |           0.961905 |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | J-lens           | False         |           0.875    |             0 |                      4 | False          | False        |
| mountain  | plain lens       | False         |           0.910714 |             1 |                     15 | False          | False        |
| mountain  | end-pass J-lens  | True          |           0.989286 |             0 |             1000000000 | True           | True         |
| mountain  | end-pass plain24 | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27 | True          |           0.992857 |             2 |             1000000000 | True           | True         |
| heart     | J-lens           | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | plain lens       | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass J-lens  | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | end-pass plain24 | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass plain27 | False         |           0.968254 |             0 |                     10 | False          | False        |
| day       | J-lens           | True          |           0.992188 |             0 |                     72 | True           | True         |
| day       | plain lens       | True          |           1        |             0 |                   2941 | True           | True         |
| day       | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens           | True          |           0.967033 |             1 |                     58 | True           | True         |
| star      | plain lens       | True          |           0.956044 |             1 |                     32 | True           | True         |
| star      | end-pass J-lens  | True          |           0.967033 |             1 |                     58 | True           | True         |
| star      | end-pass plain24 | True          |           0.956044 |             1 |                     32 | True           | True         |
| star      | end-pass plain27 | True          |           0.967033 |             0 |                     36 | True           | True         |
| cloud     | J-lens           | False         |           0.934641 |             1 |                     17 | False          | False        |
| cloud     | plain lens       | False         |           0.941176 |             2 |                      6 | False          | False        |
| cloud     | end-pass J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass plain24 | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| bag       | J-lens           | True          |           1        |             5 |                   3484 | True           | True         |
| bag       | plain lens       | True          |           0.977778 |            21 |                   1051 | True           | True         |
| bag       | end-pass J-lens  | True          |           1        |             5 |                   3484 | True           | True         |
| bag       | end-pass plain24 | True          |           0.977778 |            21 |                   1050 | True           | True         |
| bag       | end-pass plain27 | False         |           1        |             0 |                     29 | False          | False        |
| mouth     | J-lens           | True          |           0.992424 |             0 |                    778 | True           | True         |
| mouth     | plain lens       | True          |           0.977273 |             0 |                    215 | True           | True         |
| mouth     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24 | True          |           0.992424 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens           | True          |           0.888889 |             0 |                   3187 | True           | True         |
| soil      | plain lens       | True          |           0.955556 |             5 |                    684 | True           | True         |
| soil      | end-pass J-lens  | True          |           1        |             0 |                   3178 | True           | True         |
| soil      | end-pass plain24 | True          |           1        |             5 |                    684 | True           | True         |
| soil      | end-pass plain27 | True          |           1        |             0 |                     80 | True           | True         |
| mountain  | J-lens           | False         |           0.938889 |             0 |                     61 | True           | True         |
| mountain  | plain lens       | False         |           0.9      |             1 |                      2 | False          | False        |
| mountain  | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | end-pass plain24 | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| heart     | J-lens           | False         |           0.894444 |             0 |                      9 | False          | False        |
| heart     | plain lens       | False         |           0.872222 |             0 |                      5 | False          | False        |
| heart     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | J-lens           | True          |           0.926471 |             0 |                     91 | True           | True         |
| hand      | plain lens       | True          |           0.936275 |            18 |                    265 | True           | True         |
| hand      | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain24 | True          |           1        |            18 |             1000000000 | True           | True         |
| hand      | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens           | False         |           0.9      |             1 |                     12 | False          | False        |
| star      | plain lens       | False         |           0.903846 |             1 |                     21 | False          | False        |
| star      | end-pass J-lens  | False         |           0.9      |             1 |                     12 | False          | False        |
| star      | end-pass plain24 | False         |           0.903846 |             1 |                     21 | False          | False        |
| star      | end-pass plain27 | False         |           0.919231 |             0 |                     16 | False          | False        |
| cloud     | J-lens           | False         |                    |             1 |             1000000000 |                |              |
| cloud     | plain lens       | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass J-lens  | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain24 | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass plain27 | False         |                    |             0 |             1000000000 |                |              |
| bag       | J-lens           | True          |           1        |             6 |                   2420 | True           | True         |
| bag       | plain lens       | True          |           0.841667 |             0 |                    109 | True           | True         |
| bag       | end-pass J-lens  | True          |           1        |             6 |                   2420 | True           | True         |
| bag       | end-pass plain24 | True          |           0.841667 |             0 |                    109 | True           | True         |
| bag       | end-pass plain27 | False         |           0.933333 |             0 |                      4 | False          | False        |
| mouth     | J-lens           | False         |           0.95     |             0 |                     15 | False          | False        |
| mouth     | plain lens       | True          |           0.966667 |             0 |                   1096 | True           | True         |
| mouth     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens           | True          |           0.88     |             0 |                   5935 | True           | True         |
| soil      | plain lens       | True          |           0.986667 |             0 |                   4506 | True           | True         |
| soil      | end-pass J-lens  | True          |           0.986667 |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | J-lens           | False         |           0.854762 |             1 |                      5 | False          | False        |
| mountain  | plain lens       | True          |           0.861905 |             1 |                     48 | True           | True         |
| mountain  | end-pass J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain24 | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| heart     | J-lens           | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | plain lens       | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass J-lens  | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | end-pass plain24 | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass plain27 | False         |           0.936508 |             0 |                     10 | False          | False        |
| hand      | J-lens           | True          |           0.960145 |             0 |                  32305 | True           | True         |
| hand      | plain lens       | True          |           0.992754 |             0 |                  34571 | True           | True         |
| hand      | end-pass J-lens  | True          |           0.985507 |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain24 | True          |           0.996377 |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| star      | J-lens           | True          |           0.934066 |             1 |                     63 | True           | True         |
| star      | plain lens       | False         |           0.912088 |             1 |                     26 | False          | False        |
| star      | end-pass J-lens  | True          |           0.934066 |             1 |                     63 | True           | True         |
| star      | end-pass plain24 | False         |           0.912088 |             1 |                     26 | False          | False        |
| star      | end-pass plain27 | False         |           0.934066 |             0 |                     30 | False          | False        |
| book      | J-lens           | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | plain lens       | False         |           0.808333 |             1 |                     17 | False          | False        |
| book      | end-pass J-lens  | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | end-pass plain24 | False         |           0.808333 |             1 |                     17 | False          | False        |
| book      | end-pass plain27 | False         |           0.866667 |             2 |                     19 | False          | False        |
| cloud     | J-lens           | False         |           0.888889 |             1 |                     16 | False          | False        |
| cloud     | plain lens       | False         |           0.911111 |             2 |                      9 | False          | False        |
| cloud     | end-pass J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass plain24 | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass plain27 | True          |           1        |             1 |             1000000000 | True           | True         |
| bag       | J-lens           | True          |           1        |            20 |                   5527 | True           | True         |
| bag       | plain lens       | False         |           0.953704 |           622 |                   1578 | False          | False        |
| bag       | end-pass J-lens  | True          |           1        |            20 |                   5517 | True           | True         |
| bag       | end-pass plain24 | False         |           1        |           621 |                   1577 | False          | False        |
| bag       | end-pass plain27 | True          |           1        |            13 |                     51 | True           | True         |
| mouth     | J-lens           | True          |           0.988095 |             0 |                    517 | True           | True         |
| mouth     | plain lens       | True          |           0.976191 |             0 |                    270 | True           | True         |
| mouth     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens           | True          |           0.811765 |             1 |                    978 | True           | True         |
| soil      | plain lens       | True          |           0.882353 |             5 |                    144 | True           | True         |
| soil      | end-pass J-lens  | True          |           0.952941 |             1 |                    969 | True           | True         |
| soil      | end-pass plain24 | True          |           0.988235 |             5 |                    143 | True           | True         |
| soil      | end-pass plain27 | True          |           1        |             8 |                     92 | True           | True         |
| mountain  | J-lens           | False         |           0.9      |             1 |                     39 | True           | True         |
| mountain  | plain lens       | False         |           0.852941 |             2 |                      0 | False          | False        |
| mountain  | end-pass J-lens  | True          |           0.976471 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain24 | True          |           0.982353 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27 | True          |           0.988235 |             2 |             1000000000 | True           | True         |
| heart     | J-lens           | False         |           0.837607 |             0 |                     10 | False          | False        |
| heart     | plain lens       | False         |           0.82906  |             0 |                      8 | False          | False        |
| heart     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens           | False         |           0.642012 |             1 |                     16 | False          | False        |
| star      | plain lens       | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass J-lens  | False         |           0.642012 |             1 |                     16 | False          | False        |
| star      | end-pass plain24 | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass plain27 | False         |           0.64497  |             0 |                     15 | False          | False        |
| book      | J-lens           | True          |           0.925    |             2 |                    106 | True           | True         |
| book      | plain lens       | True          |           0.9      |             1 |                    390 | True           | True         |
| book      | end-pass J-lens  | True          |           1        |             2 |             1000000000 | True           | True         |
| book      | end-pass plain24 | True          |           0.99375  |             1 |             1000000000 | True           | True         |
| book      | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| cloud     | J-lens           | True          |           0.864198 |             0 |                    119 | True           | True         |
| cloud     | plain lens       | True          |           0.851852 |             1 |                     58 | True           | True         |
| cloud     | end-pass J-lens  | True          |           0.864198 |             0 |                    119 | True           | True         |
| cloud     | end-pass plain24 | True          |           0.851852 |             1 |                     58 | True           | True         |
| cloud     | end-pass plain27 | True          |           0.864198 |             1 |                     47 | True           | True         |
| bag       | J-lens           | False         |           0.931818 |            10 |                     21 | False          | False        |
| bag       | plain lens       | True          |           0.878788 |             1 |                     83 | True           | True         |
| bag       | end-pass J-lens  | False         |           0.931818 |            10 |                     21 | False          | False        |
| bag       | end-pass plain24 | True          |           0.878788 |             1 |                     83 | True           | True         |
| bag       | end-pass plain27 | False         |           0.984848 |             0 |                     18 | False          | False        |
| mouth     | J-lens           | True          |           0.974359 |             0 |                   1077 | True           | True         |
| mouth     | plain lens       | True          |           0.961538 |             0 |                   1498 | True           | True         |
| mouth     | end-pass J-lens  | True          |           0.974359 |             0 |                   1077 | True           | True         |
| mouth     | end-pass plain24 | True          |           0.961538 |             0 |                   1498 | True           | True         |
| mouth     | end-pass plain27 | True          |           0.935897 |             0 |                     45 | True           | True         |
| soil      | J-lens           | False         |           0.8      |             1 |                     21 | False          | False        |
| soil      | plain lens       | True          |           0.854545 |             0 |                    123 | True           | True         |
| soil      | end-pass J-lens  | False         |           0.8      |             1 |                     21 | False          | False        |
| soil      | end-pass plain24 | True          |           0.854545 |             0 |                    123 | True           | True         |
| soil      | end-pass plain27 | False         |           0.927273 |             0 |                     15 | False          | False        |
| mountain  | J-lens           | True          |           0.873333 |             2 |                     47 | True           | True         |
| mountain  | plain lens       | True          |           0.913333 |             2 |                    453 | True           | True         |
| mountain  | end-pass J-lens  | True          |           0.873333 |             2 |                     47 | True           | True         |
| mountain  | end-pass plain24 | True          |           0.913333 |             2 |                    453 | True           | True         |
| mountain  | end-pass plain27 | True          |           0.906667 |             2 |                     71 | True           | True         |
| heart     | J-lens           | False         |           0.849206 |             0 |                     17 | False          | False        |
| heart     | plain lens       | True          |           0.896825 |             0 |                     40 | True           | True         |
| heart     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens           | True          |           0.611336 |             2 |                    100 | True           | True         |
| star      | plain lens       | True          |           0.603239 |             1 |                     55 | True           | True         |
| star      | end-pass J-lens  | True          |           0.611336 |             2 |                    100 | True           | True         |
| star      | end-pass plain24 | True          |           0.603239 |             1 |                     55 | True           | True         |
| star      | end-pass plain27 | True          |           0.611336 |             0 |                     54 | True           | True         |
| cloud     | J-lens           | True          |           0.921569 |             1 |                    101 | True           | True         |
| cloud     | plain lens       | True          |           0.921569 |             2 |                     53 | True           | True         |
| cloud     | end-pass J-lens  | True          |           0.921569 |             1 |                    101 | True           | True         |
| cloud     | end-pass plain24 | True          |           0.921569 |             2 |                     53 | True           | True         |
| cloud     | end-pass plain27 | True          |           0.921569 |             1 |                     48 | True           | True         |
| bag       | J-lens           | False         |           0.95614  |             6 |                     21 | False          | False        |
| bag       | plain lens       | True          |           0.925439 |             4 |                     48 | True           | True         |
| bag       | end-pass J-lens  | False         |           0.95614  |             6 |                     21 | False          | False        |
| bag       | end-pass plain24 | True          |           0.925439 |             4 |                     48 | True           | True         |
| bag       | end-pass plain27 | False         |           0.991228 |             0 |                     31 | False          | False        |
| mouth     | J-lens           | True          |           0.992064 |             0 |                    256 | True           | True         |
| mouth     | plain lens       | True          |           0.976191 |             0 |                    441 | True           | True         |
| mouth     | end-pass J-lens  | True          |           0.992064 |             0 |                    256 | True           | True         |
| mouth     | end-pass plain24 | True          |           0.976191 |             0 |                    441 | True           | True         |
| mouth     | end-pass plain27 | True          |           0.960317 |             0 |                     41 | True           | True         |
| soil      | J-lens           | True          |           0.873684 |             0 |                     32 | True           | True         |
| soil      | plain lens       | True          |           0.894737 |             0 |                    267 | True           | True         |
| soil      | end-pass J-lens  | True          |           0.873684 |             0 |                     32 | True           | True         |
| soil      | end-pass plain24 | True          |           0.894737 |             0 |                    267 | True           | True         |
| soil      | end-pass plain27 | False         |           0.884211 |             8 |                     16 | False          | False        |
| mountain  | J-lens           | True          |           0.947826 |             1 |                     33 | True           | True         |
| mountain  | plain lens       | True          |           0.956522 |             1 |                    334 | True           | True         |
| mountain  | end-pass J-lens  | True          |           0.947826 |             1 |                     33 | True           | True         |
| mountain  | end-pass plain24 | True          |           0.956522 |             1 |                    334 | True           | True         |
| mountain  | end-pass plain27 | True          |           0.945652 |             2 |                     62 | True           | True         |
| heart     | J-lens           | False         |           0.90404  |             0 |                     18 | False          | False        |
| heart     | plain lens       | True          |           0.964646 |             0 |                     53 | True           | True         |
| heart     | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | J-lens           | True          |           1        |             0 |                  14959 | True           | True         |
| day       | plain lens       | True          |           1        |             0 |                  60463 | True           | True         |
| day       | end-pass J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens           | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | plain lens       | True          |           0.960114 |             1 |                     63 | True           | True         |
| star      | end-pass J-lens  | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | end-pass plain24 | True          |           0.960114 |             1 |                     63 | True           | True         |
| star      | end-pass plain27 | True          |           0.900285 |             0 |                     54 | True           | True         |

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云', '云的', '的云', ' nube', ' cloudy', ' обла', '云彩', '云雾', '.Cloud', '云服务', '云端', '云中', '云海', ' mây', '云计算', '云平台', ' 클라우드', ' fog', 'クラウド', ' sky']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

plain lens: [' clouds', ' cloud', '云', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云层', '云彩', ' обла', '云的', '/cloud', '雲', '云计算', '云朵', '.cloud', '的云', ' cloudy', '云端', 'クラウド', ' 클라우드', '云中', '云服务', '.Cloud', '天空', ' nube', '云雾', '云平台', '云上', ' mây', '多云']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云', '云的', '的云', ' cloudy', ' обла', '云彩', '云雾', '.Cloud', '云端', '云服务', '云中', '云海', ' mây', '云计算', '云平台', ' 클라우드', ' fog', 'クラウド', ' sky', ' skies']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass plain24: [' clouds', ' cloud', '云', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云层', '云彩', ' обла', '云的', '/cloud', '雲', '云计算', '云朵', '.cloud', '的云', ' cloudy', '云端', 'クラウド', ' 클라우드', '云中', '云服务', '.Cloud', '天空', '云雾', '云平台', '云上', ' mây', '多云', '云飞']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass plain27: [' cloud', '云', 'cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '云彩', '_cloud', '的云', '云层', '云朵', ' обла', '/cloud', '.cloud', '云计算', '云端', ' cloudy', '云雾', '云中', '.Cloud', 'クラウド', ' 클라우드', '云上', '云服务', '云飞', '云平台', '云天', ' mây', '雲端']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

J-lens: [' purse', ' pouch', ' pocket', ' pockets', '钱包', ' wallet', ' suitcase', '口袋', ' bags', '-pocket', ' bag', ' luggage', '口袋里', 'bag', ' tote', ' wallets', 'bags', ' bracelet', ' trousers', ' backpack', 'wallet', ' baggage', '书包', ' Taschen', 'Bags', '袋子', ' basket', ' holster', ' Bags', 'กระเป๋า', 'Pocket', ' Wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

plain lens: ['加拿大', '提', ' tut', ' bag', ' purse', ' spanish', ' recept', ' tart', ' poc', '随身携带', ' fond', 'zac', '新加坡', '钱包', 'implements', 'Pocket', ' pocket', '口袋', '战术', ' aficion', ' videoc', 'urses', ' magazin', 'achable', '之谜', ' té', ' pockets', 'ré', ' Taschen', ' apro', 'naissance', 'wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass J-lens: [' purse', ' pouch', ' pocket', ' pockets', '钱包', ' wallet', ' suitcase', '口袋', ' bags', '-pocket', ' bag', ' luggage', '口袋里', 'bag', ' tote', ' wallets', 'bags', ' bracelet', ' trousers', ' backpack', 'wallet', ' baggage', '书包', ' Taschen', 'Bags', '袋子', ' basket', ' holster', ' Bags', 'กระเป๋า', 'Pocket', ' Wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass plain24: ['加拿大', '提', ' tut', ' bag', ' purse', ' spanish', ' recept', ' tart', ' poc', '随身携带', ' fond', 'zac', '新加坡', '钱包', 'implements', 'Pocket', ' pocket', '口袋', '战术', ' aficion', ' videoc', 'urses', ' magazin', 'achable', '之谜', ' té', ' pockets', 'ré', ' Taschen', ' apro', 'naissance', 'wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass plain27: [' bag', '口袋', ' pocket', ' pockets', ' wallet', '袋', 'bag', 'Pocket', ' bags', 'Wallet', ' purse', '钱包', ' bols', 'Bag', ' wallets', 'wallet', ' sac', '囊', ' Pocket', ' Wallet', ' túi', ' Bag', 'bags', '-pocket', ' pouch', 'กระเป๋า', '_wallet', ' Bags', '袋子', ' BAG', ' poch', '_bag']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' tongue', ' lips', ' bouche', ' palate', ' saliva', ' jaw', ' mulut', '嘴', ' bocca', ' throat', '口', ' miệng', '嘴唇', ' jaws', ' tongues', ' teeth', 'lips', ' oral', ' doorway', ' mou', ' vagina', '口语', '口中', '舌头']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

plain lens: [' mouth', 'mouth', '口腔', ' Mouth', '口', ' mouths', ' oral', '嘴巴', ' mou', '-mouth', '的口', ' bocca', '口语', '嘴', '口的', ' saliva', '口中', '口红', '口区', '口干', '口头', 'emouth', ' cunt', ' pron', '加拿大', '嘴唇', '出口', ' mond', '聘', ' orally', ' lips', ' fond']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' tongue', ' lips', ' palate', ' saliva', ' jaw', ' mulut', '嘴', ' bocca', ' throat', '口', '嘴唇', ' miệng', ' tongues', ' jaws', ' teeth', ' oral', 'lips', ' doorway', ' vagina', ' mou', '口语', '口中', '舌头', '口才']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass plain24: [' mouth', 'mouth', '口腔', ' Mouth', '口', ' mouths', ' oral', '嘴巴', ' mou', '-mouth', '的口', ' bocca', '口语', '嘴', '口的', ' saliva', '口中', '口红', '口区', '口干', '口头', 'emouth', ' cunt', ' pron', '加拿大', '嘴唇', '出口', ' mond', '聘', ' orally', ' lips', ' fond']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass plain27: [' mouth', '口', 'mouth', ' Mouth', '口的', ' mouths', '嘴', '嘴巴', '口腔', '-mouth', '的口', ' oral', ' boca', '口中', ' bocca', '开口', ' miệng', '口の', '口中的', ' Oral', ' mulut', 'ปาก', ' lips', '口头', '唇', 'emouth', '口镇', '口红', '嘴唇', '嘴里', '张口', '口干']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

J-lens: [' soil', ' terrain', ' ground', '土壤', 'ground', ' earth', ' tierra', ' tanah', ' soils', ' Terrain', ' Soil', '地面', '土地', ' terra', '大地', ' terre', ' land', ' floor', ' terreno', '的土地', 'Ground', 'terrain', ' suelo', 'earth', '土壤中', ' Ground', 'floor', '-ground', '地基', '泥土', '地板', '的地']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

plain lens: [' soil', ' terrain', ' ground', '地面', '土地', 'ground', ' أرض', ' tanah', '地基', '土壤', '大地', '脚下的', 'Ground', ' land', '底层', ' tierra', '土', ' soils', '地表', '的地', ' đất', '地面的', ' terra', ' terre', ' Ground', 'terrain', ' Soil', 'loor', '_ground', ' earth', ' الأرض', ' terrestrial']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass J-lens: [' soil', ' terrain', ' ground', '土壤', 'ground', ' earth', ' tierra', ' tanah', ' soils', ' Terrain', ' Soil', '地面', '土地', ' terra', '大地', ' terre', ' land', ' floor', ' terreno', '的土地', 'Ground', 'terrain', ' suelo', 'earth', '土壤中', ' Ground', 'floor', '-ground', '地基', '泥土', '地板', '的地']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass plain24: [' soil', ' terrain', ' ground', '地面', '土地', 'ground', ' أرض', ' tanah', '地基', '土壤', '大地', '脚下的', 'Ground', ' land', '底层', ' tierra', '土', ' soils', '地表', '的地', ' đất', '地面的', ' terra', ' terre', ' Ground', 'terrain', ' Soil', 'loor', '_ground', ' earth', ' الأرض', ' terrestrial']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass plain27: [' ground', 'ground', ' soil', '地面', ' Ground', '土壤', 'Ground', '土地', ' tanah', ' terre', ' Soil', ' floor', '_ground', ' suelo', ' earth', ' terrain', '地面的', ' đất', ' soils', ' land', '地板', ' terra', '地', ' grounds', '地面上', '-ground', 'ดิน', '土', ' tierra', '的地', 'floor', '地基']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

J-lens: [' mountains', ' mountain', 'mount', ' Mountains', ' montagne', ' hills', ' montaña', '山峰', 'Mountain', ' montagnes', '山脉', ' Mountain', ' montagna', '山地', ' hill', ' gunung', 'Mount', ' Alps', ' terrain', '山区', ' mount', ' volcano', ' горы', ' massif', '的山', '山体', ' cliffs', '山的', '-mount', ' glacier', '登山', ' núi']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

plain lens: [' mountains', ' mountain', ' гор', ' montaña', ' Mountains', '山峰', ' montagnes', '加拿大', 'mount', '山脉', 'alic', ' montagna', '_MOUNT', '阿拉伯', 'Mount', ' montagne', '依山', 'ugged', ' Mountain', 'Mountain', 'bestos', ' penal', '山之', '卖点', '兢兢业业', ' fond', ' terrain', ' hill', 'peater', 'imestone', '岗', ' mount']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass J-lens: [' mountains', ' mountain', 'mount', ' Mountains', ' hills', '山峰', 'Mountain', '山脉', ' Mountain', '山地', ' hill', ' gunung', 'Mount', ' Alps', ' terrain', '山区', ' mount', ' volcano', ' горы', ' massif', '的山', '山体', ' cliffs', '山的', '-mount', ' glacier', '登山', ' núi', ' جبل', '山顶', ' countryside', '山之']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass plain24: [' mountains', ' mountain', ' гор', ' Mountains', '山峰', '加拿大', 'mount', '山脉', 'alic', '_MOUNT', '阿拉伯', 'Mount', '依山', 'ugged', ' Mountain', 'Mountain', 'bestos', ' penal', '山之', '卖点', '兢兢业业', ' terrain', ' fond', ' hill', 'imestone', 'peater', '岗', ' mount', '靠山', '脊梁', ' inland', ' plateau']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass plain27: [' mountains', ' Mountains', ' mountain', '山峰', 'mount', 'Mount', ' Mountain', 'Mountain', ' гор', '峰', ' hill', ' fond', '山之', ' Peak', '山脉', 'Peak', ' Mount', ' hills', '山的', '加拿大', ' mount', ' peak', ' горы', 'ภูเขา', 'ountains', '的山', ' dãy', 'peak', ' núi', '_MOUNT', ' peaks', 'OUNT']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

J-lens: [' heart', ' hearts', 'heart', ' Heart', '-heart', '心脏', 'Heart', ' corazón', '的心脏', '心臟', ' coração', ' heartbeat', ' cœur', ' cuore', ' Herzen', ' cardiac', ' Hearts', ' сердце', ' сердца', ' قلب', ' coeur', '心跳', ' серд', 'heartbeat', ' cardi', '心肺', ' cardia', ' heartfelt', 'card', ' jantung', ' القلب', '-hearted']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

plain lens: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '心脏', '的心脏', ' corazón', ' серд', '心', ' قلب', '-heart', ' сердца', ' cœur', '心臟', '心的', ' القلب', '的心', ' сердце', ' Herzen', ' cuore', ' Hearts', '心脏病', ' heartbeat', 'heartbeat', '之心', ' cardiac', '心率', '心跳', 'قلب', ' coração', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass J-lens: [' heart', ' hearts', 'heart', ' Heart', '-heart', '心脏', 'Heart', ' corazón', '的心脏', '心臟', ' coração', ' heartbeat', ' cœur', ' cuore', ' Herzen', ' cardiac', ' Hearts', ' сердце', ' сердца', ' قلب', ' coeur', '心跳', ' серд', 'heartbeat', ' cardi', '心肺', ' cardia', ' heartfelt', 'card', ' jantung', ' القلب', '-hearted']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass plain24: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '心脏', '的心脏', ' corazón', ' серд', '心', ' قلب', '-heart', ' сердца', ' cœur', '心臟', '心的', ' القلب', '的心', ' сердце', ' Herzen', ' cuore', ' Hearts', '心脏病', ' heartbeat', 'heartbeat', '之心', ' cardiac', '心率', '心跳', 'قلب', ' coração', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心', '的心', ' corazón', ' cœur', ' قلب', '心的', '的心脏', ' серд', ' сердца', ' coração', ' heartbeat', ' сердце', ' القلب', ' cardiac', 'หัวใจ', ' Hearts', '心跳', '-hearted', 'heartbeat', '心臟', ' cuore', '心和', '心脏病', 'قلب', ' cardi']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

J-lens: [' day', 'day', ' daytime', ' daylight', ' days', 'Day', 'days', ' Day', '_day', ' morning', '/day', '-day', 'Days', '(day', ' journée', '.day', ' día', ' DAY', ' Days', '_days', '白天', '天数', ' afternoon', ' день', '-days', ' weekday', 'DAY', ' días', '的一天', ' Tages', ' дня', ' Tage']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

plain lens: ['day', ' day', '加拿大', ' daylight', ' daytime', ' days', ' sun', 'Day', ' дня', '太阳', ' النهار', '阿拉伯', '天空', ' ημέ', ' té', '-day', '(day', ' vig', '天的', '_days', ' día', '晴朗', '白天', ' DAYS', '一天的', '日', ' parad', 'Days', ' lent', '日历', '姆斯', 'ré']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass J-lens: [' day', 'day', ' daytime', ' daylight', ' days', 'Day', 'days', ' Day', '_day', ' morning', '/day', '-day', 'Days', '(day', ' día', '.day', ' DAY', ' Days', '_days', '白天', '天数', ' afternoon', ' день', ' weekday', '-days', 'DAY', ' días', ' Tages', '的一天', ' дня', '\tday', ' Tage']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass plain24: ['day', ' day', '加拿大', ' daylight', ' daytime', ' days', ' sun', 'Day', ' дня', '太阳', ' النهار', '阿拉伯', '天空', ' ημέ', ' té', '-day', '(day', ' vig', '天的', '_days', ' día', '晴朗', '白天', ' DAYS', '一天的', '日', ' parad', 'Days', ' lent', '日历', '姆斯', 'ré']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass plain27: [' day', 'day', 'Day', '-day', ' Day', ' days', '_day', ' дня', ' día', ' день', '日', ' DAY', '.day', '日的', '\tday', '(day', 'Days', '的一天', '这一天', ' daylight', ' ngày', '一天', ' روز', ' giorno', '_days', ' daytime', '一天的', '-Day', '天的', '/day', 'DAY', ' Days']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

J-lens: [' stars', ' star', ' Stars', 'stars', 'star', 'Stars', '-stars', '-star', ' Star', '/star', '星星', '星', '星辰', '之星', 'Star', ' aster', '星的', ' estrella', ' étoiles', '_star', ' estrellas', ' звезды', '颗星', '星标', ' звезда', ' estrel', ' estrelas', '星光', '恒星', '.star', '-Star', ' STAR']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

plain lens: [' stars', ' star', '星', ' Stars', '星的', 'stars', ' aster', '.star', ' Star', 'Stars', '-stars', '星辰', '_star', 'Star', ' Sternen', ' starred', 'star', '星座', '之星', '-star', ' stellar', '颗星', '恒星', ' звезды', ' estrellas', ' Astroph', '星级', ' celestial', '星标', ' 별', ' звезд', ' estrelas']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass J-lens: [' stars', ' star', ' Stars', 'stars', 'star', 'Stars', '-stars', '-star', ' Star', '/star', '星星', '星', '星辰', '之星', 'Star', ' aster', '星的', ' estrella', ' étoiles', '_star', ' estrellas', ' звезды', '颗星', '星标', ' звезда', ' estrel', ' estrelas', '星光', '恒星', '.star', '-Star', ' STAR']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass plain24: [' stars', ' star', '星', ' Stars', '星的', 'stars', ' aster', '.star', ' Star', 'Stars', '-stars', '星辰', '_star', 'Star', ' Sternen', ' starred', 'star', '星座', '之星', '-star', ' stellar', '颗星', '恒星', ' звезды', ' estrellas', ' Astroph', '星级', ' celestial', '星标', ' 별', ' звезд', ' estrelas']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass plain27: [' star', ' stars', '星', '星的', ' Star', ' Stars', 'star', 'Star', 'stars', '-star', 'Stars', '_star', '星星', '.star', '-stars', ' aster', '-Star', ' STAR', '之星', ' bintang', '恒星', ' starred', '明星', ' звезды', ' stellar', '/star', 'STAR', ' звезд', '颗星', ' estrellas', '星光', '星级']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

J-lens: [' clouds', ' cloud', 'cloud', '-cloud', 'Cloud', ' Cloud', '/cloud', '.cloud', '云层', '_cloud', '雲', ' nube', '云朵', ' cloudy', '云', '的云', '云的', ' обла', '云雾', '.Cloud', '云服务', '云彩', ' fog', '云海', ' sky', '云端', '云计算', ' mây', '云平台', '云中', ' skies', '浮云']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

plain lens: ['云', ' clouds', 'cloud', ' cloud', 'Cloud', ' Cloud', ' обла', '-cloud', '云彩', '_cloud', '云层', '/cloud', '雲', '云的', '.cloud', '的云', '云朵', '云计算', '云端', '云雾', ' cloudy', '.Cloud', '云服务', ' nube', ' 클라우드', ' mây', '云中', '天空', 'クラウド', ' Обла', '天气', '云上']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass J-lens: [' clouds', ' cloud', 'cloud', '-cloud', 'Cloud', ' Cloud', '/cloud', '.cloud', '云层', '_cloud', '雲', ' nube', '云朵', ' cloudy', '云', '的云', '云的', '云雾', '.Cloud', '云服务', '云彩', '云海', ' fog', ' sky', '云计算', '云端', ' mây', '云平台', '云中', ' skies', '浮云', '乌云']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass plain24: ['云', ' clouds', 'cloud', ' cloud', 'Cloud', ' Cloud', '-cloud', '云彩', '_cloud', '云层', '/cloud', '云的', '雲', '.cloud', '的云', '云朵', '云计算', '云端', '云雾', ' cloudy', '.Cloud', '云服务', ' nube', ' 클라우드', ' mây', '云中', '天空', 'クラウド', '天气', '云上', '云山', '雯']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass plain27: ['cloud', '云', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云层', '云彩', '/cloud', '的云', '云雾', '云朵', '.cloud', '.Cloud', '云端', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云飞', '云平台', '云上', 'クラウド', ' nube', '云天', ' đám']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

J-lens: [' bags', ' suitcase', '书包', '钱包', ' pouch', ' bag', ' Bags', ' backpack', 'bags', '袋子', ' luggage', ' wallet', ' sacks', 'bag', ' sack', ' baggage', ' sacs', ' purse', 'Bags', 'wallet', ' 가방', ' pocket', 'Bag', ' wallets', '背包', ' pockets', '口袋', '箱包', ' basket', ' Tasche', '-pocket', '包包']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

plain lens: ['вершенство', '袋子', '加拿大', '书包', ' recept', ' tut', 'implements', '随身携带', '钱包', ' zav', 'editary', ' zak', ' plec', ' Taschen', '-validate', ' moch', '收养', 'ferences', '流行病学', '提', ' sak', 'ISATION', ' bag', ' виз', 'Accepted', 'please', '陪护', 'zac', 'ください', 'wallet', '绽', ' bags']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass J-lens: [' bags', ' suitcase', '书包', '钱包', ' pouch', ' bag', ' Bags', ' backpack', 'bags', '袋子', ' luggage', ' wallet', ' sacks', 'bag', ' sack', ' baggage', ' sacs', ' purse', 'Bags', 'wallet', ' 가방', ' pocket', 'Bag', ' wallets', '背包', ' pockets', '口袋', '箱包', ' basket', ' Tasche', '-pocket', '包包']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass plain24: ['вершенство', '袋子', '加拿大', '书包', ' recept', ' tut', 'implements', '随身携带', '钱包', ' zav', 'editary', ' zak', ' plec', ' Taschen', '-validate', ' moch', '收养', 'ferences', '流行病学', '提', ' sak', 'ISATION', ' bag', ' виз', 'Accepted', 'please', '陪护', 'zac', 'ください', 'wallet', '绽', ' bags']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass plain27: [' bag', ' bags', '袋', 'Bag', ' Bags', 'bags', '袋子', 'bag', ' BAG', ' Bag', 'Bags', '_bag', '囊', ' backpack', ' túi', '书包', '口袋', 'wallet', '背包', '钱包', ' Backpack', 'Wallet', ' moch', '包', '布袋', '包的', ' purse', 'beutel', ' sacks', ' сум', ' wallet', ' pouch']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' throat', ' lips', ' jaw', ' tongue', '嘴', ' saliva', ' teeth', ' cheeks', ' speech', ' bocca', '口语', ' jaws', ' palate', 'lips', '喉咙', ' doorway', '口才', ' mulut', ' tongues', ' vagina', '舌头', '嘴唇', '牙齿', ' kiss']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

plain lens: [' mouth', '嘴', 'mouth', '口腔', '口', '口语', '聘', ' Mouth', 'emouth', '嘴巴', '开口', '一口', ' oral', ' bocca', ' mouths', '口才', '张嘴', '出口', '-mouth', 'unciation', '的口', '、、', 'ullivan', '口水', '口区', 'peech', '_exports', 'please', ' reproduk', 'achable', '嘴边', ' mou']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' throat', ' lips', ' jaw', ' tongue', '嘴', ' saliva', ' teeth', ' cheeks', ' speech', ' bocca', '口语', ' jaws', ' palate', 'lips', '喉咙', ' doorway', '口才', ' mulut', ' tongues', ' vagina', '舌头', '嘴唇', '牙齿', ' kiss']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass plain24: [' mouth', '嘴', 'mouth', '口腔', '口', '口语', '聘', ' Mouth', 'emouth', '嘴巴', '开口', '一口', ' oral', ' bocca', ' mouths', '口才', '张嘴', '出口', '-mouth', 'unciation', '的口', '、、', 'ullivan', '口水', '口区', 'peech', '_exports', 'please', ' reproduk', 'achable', '嘴边', ' mou']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '口的', ' mouths', '嘴巴', '口腔', '-mouth', '的口', ' bocca', ' boca', '开口', ' oral', '口中', '唇', '嘴边', ' lips', '口の', '嘴唇', '口中的', '张嘴', ' Oral', 'emouth', ' miệng', '张口', '嘴里', ' рта', ' mulut', '口に', 'ปาก']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

J-lens: [' soil', '土壤', ' Soil', ' ground', ' solvent', 'ground', ' dirt', ' solution', ' soils', ' sols', ' solar', 'solution', ' earth', ' suelo', ' floor', ' pavement', '.sol', '_sol', ' terrain', ' surface', '_SOL', ' solver', ' Сол', ' solids', ' sunlight', '溶剂', 'floor', ' flooring', ' floors', ' stone', ' solitude', 'surface']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

plain lens: [' сол', '_sol', 'сол', '太阳', ' sols', ' soil', ' Сол', ' solvent', '_solution', '溶解', ' soli', ' solu', '溶', '.sol', 'solver', ' soluble', '土壤', ' solved', '_SOL', '(sol', '固体', ' solving', ' solves', '坚', ' solution', '溶液', '.solve', ' solve', 'olvency', ' Soil', '_solve', '解决']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass J-lens: [' soil', '土壤', ' Soil', ' ground', ' solvent', 'ground', ' dirt', ' solution', ' soils', ' sols', ' solar', 'solution', ' earth', ' suelo', ' floor', ' pavement', '.sol', '_sol', ' terrain', ' surface', '_SOL', ' solver', ' Сол', ' solids', ' sunlight', '溶剂', 'floor', ' flooring', ' floors', ' stone', ' solitude', 'surface']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass plain24: [' сол', '_sol', 'сол', '太阳', ' sols', ' soil', ' Сол', ' solvent', '_solution', '溶解', ' soli', ' solu', '溶', '.sol', 'solver', ' soluble', '土壤', ' solved', '_SOL', '(sol', '固体', ' solving', ' solves', '坚', ' solution', '溶液', '.solve', ' solve', 'olvency', ' Soil', '_solve', '解决']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass plain27: [' ground', ' soil', 'ground', '土壤', '地面', ' suelo', 'Ground', ' Soil', ' Ground', ' floor', '地板', ' sols', '地面的', ' soils', '_ground', ' tanah', ' Boden', '土地', 'floor', '土', ' сол', ' đất', 'Floor', '泥土', 'GROUND', 'ดิน', ' أرض', '地表', '地基', 'grounds', ' почвы', '地板上']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

J-lens: [' mountain', ' mountains', 'mount', ' Mountains', 'Mountain', '山脉', ' Mountain', ' montaña', ' montagnes', ' hills', '山峰', ' montagna', 'Mount', '山地', ' volcano', ' hill', '的山', ' gunung', ' горы', '-mount', ' mount', '山体', '山区', '登山', ' Alps', ' canyon', ' جبل', '山的', '山顶', ' cliffs', '大山', ' wilderness']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

plain lens: [' mountains', ' mountain', ' гор', 'mount', ' Mountains', ' montagnes', ' montaña', '山峰', '山脉', '加拿大', 'ountains', '岗', 'haupt', '不可思议', '贡', '登', '_MOUNT', '耸', 'alic', ' montagna', 'Mountain', 'Mount', '本山', 'Monad', ' горы', '外国语', '等奖', 'verity', ' Mountain', '业余', '重装', '登山']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass J-lens: [' mountain', ' mountains', 'mount', ' Mountains', 'Mountain', '山脉', ' Mountain', ' montaña', ' montagnes', ' hills', '山峰', ' montagna', 'Mount', '山地', ' volcano', ' hill', '的山', ' gunung', '-mount', '山体', ' mount', '山区', '登山', ' Alps', ' canyon', '山的', ' جبل', '山顶', ' cliffs', '大山', ' monte', ' wilderness']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass plain24: [' mountains', ' mountain', 'mount', ' Mountains', ' montagnes', ' montaña', '山峰', '山脉', '加拿大', 'ountains', '岗', 'haupt', '不可思议', '贡', '登', '_MOUNT', 'alic', '耸', ' montagna', 'Mountain', 'Mount', '本山', 'Monad', '等奖', '外国语', '重装', ' Mountain', 'verity', '业余', '登山', 'informatics', 'sembled']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass plain27: [' mountains', ' Mountains', ' mountain', 'ountains', '山脉', 'mount', '山峰', 'Mountain', ' núi', 'Mount', ' montagnes', ' hill', ' montaña', ' хол', 'OUNT', ' Mountain', ' montagna', '山的', ' mount', ' hills', '_MOUNT', '山体', ' Alps', '山之', '山大', '峰', 'ภูเขา', 'ensus', 'เนิน', 'úi', ' slopes', ' Mount']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

J-lens: [' heart', 'heart', ' hearts', '心脏', '-heart', '的心脏', ' corazón', ' Heart', 'Heart', ' сердце', ' coração', ' cuore', ' heartbeat', '心臟', ' сердца', ' قلب', ' серд', ' Hearts', ' Herzen', '心肺', '心跳', ' coeur', 'heartbeat', ' cardiac', '心肌', 'قلب', ' القلب', ' conscience', ' heartfelt', 'core', '心房', '的心']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

plain lens: ['heart', ' heart', '心脏', '心的', '的心脏', ' серд', ' قلب', 'قلب', ' Heart', ' hearts', 'Heart', ' corazón', ' сердце', ' القلب', '心', ' сердца', '的心', ' centrum', '-heart', '核心', '心和', ' Hearts', '_cores', '一颗', '全心全意', '心臟', '心了', ' coeur', ' cuore', 'heartbeat', '的核心', ' heartbeat']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass J-lens: [' heart', 'heart', ' hearts', '心脏', '-heart', '的心脏', ' corazón', ' Heart', 'Heart', ' coração', ' cuore', ' heartbeat', '心臟', ' قلب', ' Hearts', ' Herzen', '心肺', '心跳', ' coeur', 'heartbeat', ' cardiac', '心肌', 'قلب', ' القلب', ' conscience', 'core', ' heartfelt', '心房', '的心', '-hearted', ' καρ', ' jantung']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass plain24: ['heart', ' heart', '心脏', '心的', '的心脏', ' قلب', 'قلب', ' hearts', ' Heart', 'Heart', ' corazón', ' القلب', '心', '的心', ' centrum', '-heart', '核心', '心和', ' Hearts', '_cores', '一颗', '全心全意', '心了', '心臟', ' coeur', ' cuore', 'heartbeat', '的核心', ' heartbeat', '为核心', '这颗', '心头']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass plain27: [' heart', 'heart', ' Heart', ' hearts', '心脏', 'Heart', '-heart', '心的', ' قلب', '心', '的心', '的心脏', ' corazón', ' coração', '心和', ' القلب', ' Hearts', 'หัวใจ', 'قلب', ' heartbeat', '-hearted', '心臟', ' cardiac', ' cuore', '心脏病', 'heartbeat', '之心', '心跳', '心了', ' jantung', ' coeur', '我的心']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

J-lens: [' hand', 'hand', ' hands', ' handshake', 'Hand', ' Hand', ' mano', ' tangan', '>Main', 'hands', '-main', ' fingers', ' mains', ' HAND', '_Main', '我的手', '/Main', '/main', '_hand', ' Hands', ' palm', '_main', '手部', '(main', '手心', '-hand', '\\"",', ' wrist', ' mão', ' gloves', ' manos', ' glove']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

plain lens: ['.main', '_MAIN', '_Main', '.MAIN', '的主', '主', '阿拉伯', '加拿大', '为主', '-main', '一把手', 'PRIMARY', ' الرئيسية', '主控', 'aupt', 'гла', '挥', '之主', '主治', ' HAND', '_main', ' principale', '主场', '主要的', 'の主', '(main', '姆斯', '/main', '的手', ' hand', ' utama', '主力']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass J-lens: [' hand', 'hand', ' hands', ' handshake', 'Hand', ' Hand', ' mano', ' tangan', '>Main', 'hands', '-main', ' fingers', ' mains', ' HAND', '_Main', '我的手', '/Main', '/main', '_hand', ' Hands', ' palm', '_main', '手部', '(main', '手心', '-hand', '\\"",', ' wrist', ' mão', ' gloves', ' manos', ' glove']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass plain24: ['.main', '_MAIN', '_Main', '.MAIN', '的主', '主', '阿拉伯', '加拿大', '为主', '-main', '一把手', 'PRIMARY', ' الرئيسية', '主控', 'aupt', 'гла', '挥', '之主', '主治', ' HAND', '_main', ' principale', '主场', '主要的', 'の主', '(main', '姆斯', '/main', '的手', ' hand', ' utama', '主力']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass plain27: [' hand', '手掌', ' hands', '手的', ' Hand', ' palm', '掌', 'hands', '手', '的手', 'Hand', '一只手', 'hand', ' HAND', '手心', '手部', 'Hands', ' Hands', '手指', '之手', '_hand', '_HAND', '掌心', '右手', ' fingers', ' pal', 'handler', 'の手', '.hand', '-hand', '握', ' mano']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', '-star', 'Stars', '/star', '星星', ' Star', ' estrella', ' звезда', ' aster', '星', ' звезды', '恒星', ' estrellas', 'Star', '星光', '之星', ' estrel', '.star', ' celestial', ' étoiles', '星辰', '_star', ' stella', '星的', ' constellation', ' estrelas', '-Star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

plain lens: [' stars', ' star', '星', 'stars', ' Stars', '-stars', ' نجوم', ' celestial', ' astronomers', '.star', ' Astronomy', ' Star', '星的', 'Stars', '恒星', ' estrellas', 'star', ' astrology', '星光', ' aster', ' stellar', ' звезд', '之星', '星座', ' Stellar', 'stellar', '天文', ' Astroph', '星星', ' astronomy', ' Bintang', '_star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', '-star', 'Stars', '/star', '星星', ' Star', ' estrella', ' звезда', ' aster', '星', ' звезды', '恒星', ' estrellas', 'Star', '星光', '之星', ' estrel', '.star', ' celestial', ' étoiles', '星辰', '_star', ' stella', '星的', ' constellation', ' estrelas', '-Star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass plain24: [' stars', ' star', '星', 'stars', ' Stars', '-stars', ' نجوم', ' celestial', ' astronomers', '.star', ' Astronomy', ' Star', '星的', 'Stars', '恒星', ' estrellas', 'star', ' astrology', '星光', ' aster', ' stellar', ' звезд', '之星', '星座', ' Stellar', 'stellar', '天文', ' Astroph', '星星', ' astronomy', ' Bintang', '_star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'stars', 'star', 'Star', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' звезд', '/star', ' STAR', ' звезды', 'STAR', ' bintang', '恒星', ' звезда', '之星', '明星', ' aster', ' starred', ' estrellas', ' stellar', '星光', '星级']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', ' nube', '云朵', '云', '云的', '的云', '云端', '云服务', ' cloudy', '云计算', '云彩', '.Cloud', '云雾', '云平台', '云海', '云中', ' 클라우드', ' sky', '云上', ' mây', 'クラウド', '雲端']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

plain lens: [' cloud', ' clouds', '云', 'cloud', ' Cloud', 'Cloud', '云计算', '云层', '-cloud', '_cloud', '云彩', '/cloud', '云端', '.cloud', '云朵', '雲', '云的', '的云', ' cloudy', '云服务', ' 클라우드', '云雾', 'クラウド', '云平台', ' nube', '天空', '.Cloud', '云上', '云中', ' mây', '云山', 'LOUD']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云的', '云', '的云', '云端', '云服务', ' cloudy', '云计算', '云彩', '.Cloud', '云雾', '云平台', '云海', '云中', ' 클라우드', ' sky', '云上', ' mây', '雲端', 'クラウド', ' skies']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass plain24: [' cloud', ' clouds', '云', 'cloud', ' Cloud', 'Cloud', '云计算', '云层', '-cloud', '_cloud', '云彩', '/cloud', '云端', '.cloud', '云朵', '雲', '云的', '的云', ' cloudy', '云服务', ' 클라우드', '云雾', 'クラウド', '云平台', '天空', '.Cloud', '云中', '云上', ' mây', '云山', 'LOUD', ' sky']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass plain27: [' cloud', 'cloud', '云', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云层', '云彩', '的云', '云朵', '/cloud', '云计算', '.cloud', '云端', '云雾', ' cloudy', '云中', '.Cloud', 'クラウド', ' 클라우드', '云平台', '云上', '云服务', '云天', '雲端', '云飞', ' mây', ' cl']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

J-lens: [' suitcase', ' luggage', ' bags', '书包', ' purse', ' backpack', ' bag', 'Bags', 'bags', 'bag', ' baggage', '钱包', ' pouch', ' Bags', '口袋', '包包', '袋子', ' tote', '箱包', 'Bag', 'uggage', ' wallet', '行李箱', ' bracelet', ' 가방', 'กระเป๋า', ' Tasche', '背包', '-pocket', ' souvenir', ' shoes', ' necklace']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

plain lens: [' bag', '加拿大', ' fond', ' tut', 'uggage', ' tart', ' recept', ' carrying', ' carried', ' ví', 'urses', '�', ' videoc', ' tote', '負擔', '手提', 'ré', ' agre', ' gab', ' lent', '书包', ' spanish', 'zuh', ' bags', ' lé', ' excurs', ' moch', ' bat', ' trag', 'udence', 'abancı', 'inne']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass J-lens: [' suitcase', ' luggage', ' bags', '书包', ' purse', ' backpack', ' bag', 'Bags', 'bags', 'bag', ' baggage', '钱包', ' pouch', ' Bags', '口袋', '包包', '袋子', ' tote', '箱包', 'Bag', 'uggage', ' wallet', '行李箱', ' bracelet', ' 가방', 'กระเป๋า', ' Tasche', '背包', '-pocket', ' souvenir', ' shoes', ' necklace']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass plain24: [' bag', '加拿大', ' fond', ' tut', 'uggage', ' tart', ' recept', ' carrying', ' carried', ' ví', 'urses', '�', ' videoc', ' tote', '負擔', '手提', 'ré', ' agre', ' gab', ' lent', '书包', ' spanish', 'zuh', ' bags', ' lé', ' excurs', ' moch', ' bat', ' trag', 'udence', 'abancı', 'inne']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass plain27: [' bag', ' bags', 'bag', 'Bag', ' sac', ' Bag', 'bags', '袋', ' Bags', ' BAG', '_bag', ' moch', ' backpack', '囊', ' Sac', '袋子', ' purse', 'Bags', ' tote', ' bols', ' sacs', ' luggage', 'กระเป๋า', ' baggage', ' saco', ' túi', 'uggage', ' 가방', ' wallet', ' tas', '书包', 'Wallet']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '-mouth', '口腔', ' throat', ' palate', ' lips', '嘴巴', ' boca', ' cheeks', ' jaw', ' рта', '喉咙', ' bouche', ' tongue', 'lips', ' nose', ' saliva', ' mulut', ' jaws', ' lungs', ' bocca', ' teeth', ' pores', 'roat', ' genitals', '嘴', ' vagina', ' penis', ' nostr']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

plain lens: [' mouth', 'mouth', '口腔', '聘', '膛', ' Mouth', ' рта', '口语', 'roat', ' مخاط', '口', '-mouth', ' ratus', ' oral', 'phinx', '嘴巴', ' lips', ' saliva', ' aficion', ' anatom', ' riz', ' biro', ' bocca', '卖点', '读卡', ' rot', 'utilus', 'lips', '的口', '天安门', ' cunt', ' mouths']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '口腔', '-mouth', ' throat', ' palate', ' lips', '嘴巴', ' boca', ' cheeks', ' jaw', ' рта', '喉咙', ' tongue', 'lips', ' saliva', ' nose', ' mulut', ' jaws', ' lungs', ' bocca', ' teeth', ' pores', ' genitals', '嘴', 'roat', ' vagina', ' penis', ' nostr', ' noses']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass plain24: [' mouth', 'mouth', '口腔', '聘', '膛', ' Mouth', ' рта', '口语', 'roat', ' مخاط', '口', '-mouth', ' ratus', ' oral', 'phinx', '嘴巴', ' lips', ' saliva', ' aficion', ' anatom', ' riz', ' biro', ' bocca', '卖点', '读卡', ' rot', 'utilus', 'lips', '的口', '天安门', ' cunt', ' mouths']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass plain27: [' mouth', '口', 'mouth', '嘴', ' Mouth', '口的', '嘴巴', ' mouths', '口腔', '-mouth', '的口', ' oral', ' bocca', ' boca', '口中', ' lips', '开口', '唇', ' miệng', '口の', '口中的', 'ปาก', ' mulut', ' Oral', ' рта', '张嘴', '嘴唇', '张口', '口红', 'emouth', '口镇', '口头']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

J-lens: [' soil', '土壤', ' soils', ' terrain', ' Soil', '土壤中', ' почвы', '泥土', ' tanah', ' почву', ' earth', ' Terrain', ' tierra', 'terrain', ' terreno', '土地', '沃土', ' terre', 'ground', '土层', ' terra', ' ground', '的土地', ' suolo', '土', ' dirt', 'earth', 'Earth', ' suelo', '土的', 'ดิน', '大地']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

plain lens: [' soil', '土壤', ' Soil', ' soils', ' почву', ' почвы', ' terrain', '土', '沃土', ' tanah', '土壤中', '脚下的', '土地', ' land', '泥土', ' Dirt', ' ground', 'ดิน', ' 토', '土层', ' dirt', ' đất', '土的', '底层', '地基', ' terre', ' أرض', 'ground', ' fertile', '地层', '接地气', '操场']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass J-lens: [' soil', '土壤', ' soils', ' terrain', ' Soil', '土壤中', ' почвы', '泥土', ' tanah', ' почву', ' earth', ' Terrain', ' tierra', 'terrain', ' terreno', '土地', '沃土', ' terre', 'ground', '土层', ' terra', ' ground', '的土地', ' suolo', '土', ' dirt', 'earth', 'Earth', ' suelo', '土的', 'ดิน', '大地']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass plain24: [' soil', '土壤', ' Soil', ' soils', ' почву', ' почвы', ' terrain', '土', '沃土', ' tanah', '土壤中', '脚下的', '土地', ' land', '泥土', ' Dirt', ' ground', 'ดิน', ' 토', '土层', ' dirt', ' đất', '土的', '底层', '地基', ' terre', ' أرض', 'ground', ' fertile', '地层', '接地气', '操场']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass plain27: [' soil', '土壤', ' Soil', ' soils', '土', '土壤中', '泥土', ' tanah', ' почвы', '土的', 'ดิน', ' почву', ' earth', ' ground', ' suelo', ' đất', '土地', ' terre', 'ground', ' Boden', '土层', ' terrain', ' 토', ' Ground', '地面', '壤', ' dirt', ' suolo', 'Ground', ' land', '土地上', 'earth']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

J-lens: [' mountains', ' mountain', ' hills', 'mount', ' Mountains', ' montagne', '山峰', ' montaña', ' hill', 'Mountain', ' montagnes', '山脉', ' volcano', ' Mountain', ' gunung', 'Mount', ' горы', ' cliffs', ' terrain', ' canyon', ' montagna', ' Alps', ' glacier', '山地', '山体', ' mount', '的山', '山区', ' monte', '山的', '-mount', ' volcan']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

plain lens: [' mountains', ' mountain', '加拿大', '山峰', 'mount', ' montaña', ' Mountains', '发卡', ' fond', '贺', ' emin', ' observ', 'peater', ' hill', ' vain', ' montagnes', ' plateau', ' gir', ' terrain', ' volcan', '岗', '兢兢业业', ' aficion', '山脉', 'alic', ' precip', ' peninsula', '卖点', 'Mount', ' volcano', '_MOUNT', ' mount']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass J-lens: [' mountains', ' mountain', ' hills', 'mount', ' Mountains', '山峰', ' hill', 'Mountain', '山脉', ' volcano', ' Mountain', ' gunung', 'Mount', ' горы', ' cliffs', ' terrain', ' canyon', ' Alps', '山地', ' glacier', '的山', '山体', ' mount', '山区', '山的', '-mount', ' volcan', '山顶', ' جبل', ' massif', ' núi', ' mound']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass plain24: [' mountains', ' mountain', '加拿大', '山峰', 'mount', ' Mountains', '发卡', ' fond', '贺', ' emin', ' observ', ' hill', 'peater', ' vain', ' plateau', ' terrain', ' volcan', ' gir', '岗', '兢兢业业', ' aficion', '山脉', 'alic', ' precip', '卖点', ' peninsula', 'Mount', ' volcano', '_MOUNT', ' mount', ' mam', 'imestone']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass plain27: [' mountains', ' Mountains', ' mountain', ' hill', '峰', '山峰', 'mount', ' hills', 'Mount', ' fond', 'Peak', ' Peak', 'Mountain', ' Mountain', ' peak', ' volcano', '山之', 'เนิน', ' hil', '高峰', '山顶', ' plateau', ' volcan', ' mount', '加拿大', ' slopes', '的山', ' peaks', '山的', ' slope', '山脉', 'peak']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

J-lens: [' heart', ' hearts', 'heart', '心脏', ' corazón', '-heart', '的心脏', '心臟', 'Heart', ' Heart', ' cœur', ' coração', ' cuore', ' heartbeat', ' cardiac', ' сердца', ' قلب', ' Herzen', ' coeur', '心肺', '心跳', ' Hearts', 'card', ' cardia', 'heartbeat', ' القلب', ' cardi', '心脏病', ' jantung', '心', '-hearted', ' Herz']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

plain lens: [' heart', 'heart', '心脏', '的心脏', ' Heart', 'Heart', ' hearts', ' corazón', '心', '心臟', ' قلب', ' cœur', ' сердца', '心的', 'قلب', ' القلب', '-heart', ' cardiac', '心脏病', ' cuore', '心了', '的心', '心肺', 'heartbeat', ' coração', '之心', ' centre', ' coeur', ' cardia', ' καρ', ' Hearts', ' heartbeat']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass J-lens: [' heart', ' hearts', 'heart', '心脏', ' corazón', '-heart', '的心脏', '心臟', 'Heart', ' Heart', ' cœur', ' coração', ' cuore', ' heartbeat', ' cardiac', ' сердца', ' قلب', ' Herzen', ' coeur', '心肺', '心跳', ' Hearts', 'card', ' cardia', 'heartbeat', ' القلب', ' cardi', '心脏病', ' jantung', '心', '-hearted', ' Herz']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass plain24: [' heart', 'heart', '心脏', '的心脏', ' Heart', 'Heart', ' hearts', ' corazón', '心', '心臟', ' قلب', ' cœur', ' сердца', '心的', 'قلب', ' القلب', '-heart', ' cardiac', '心脏病', ' cuore', '心了', '的心', '心肺', 'heartbeat', ' coração', '之心', ' centre', ' coeur', ' cardia', ' καρ', ' Hearts', ' heartbeat']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心的', '心', ' corazón', '的心脏', ' cœur', '的心', ' قلب', ' coração', ' cardiac', ' сердца', ' القلب', 'หัวใจ', '心臟', ' heartbeat', '-hearted', ' Hearts', 'قلب', '心跳', '心和', 'heartbeat', ' cuore', '心脏病', ' Herz', ' cardia', '之心']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

J-lens: ['hand', ' hand', 'Hand', '手臂', ' hands', ' handshake', ' forearm', ' tangan', 'hands', ' руки', ' HAND', '_hand', ' wrist', '手的', ' mano', ' Hand', ' arm', ' arms', '之手', '手掌', '手腕', '手', 'Hands', ' fingers', '手部', ' wrists', ' Hands', '的手臂', '(hand', 'arms', '臂', '我的手']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

plain lens: [' hand', '阿拉伯', ' arm', 'Hand', ' HAND', 'hand', ' manus', '加拿大', 'naissance', '用手', ' Hand', '鲁', '_hand', '手', '挥', '人脉', ' handy', '手臂', ' hands', ' rud', '手数', '-hand', '的手臂', ' videoc', '聘', 'ủy', 'manuel', 'lier', '手的', '一只手', ' rach', 'ré']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass J-lens: ['hand', ' hand', 'Hand', '手臂', ' hands', ' handshake', ' forearm', ' tangan', 'hands', ' руки', ' HAND', '_hand', ' wrist', '手的', ' mano', ' Hand', ' arm', ' arms', '之手', '手掌', '手腕', '手', 'Hands', ' fingers', '手部', ' wrists', ' Hands', '的手臂', '(hand', 'arms', '臂', '我的手']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass plain24: [' hand', '阿拉伯', ' arm', 'Hand', ' HAND', 'hand', ' manus', '加拿大', 'naissance', '用手', ' Hand', '鲁', '_hand', '手', '挥', '人脉', ' handy', '手臂', ' hands', ' rud', '手数', '-hand', '的手臂', ' videoc', '聘', 'ủy', 'manuel', 'lier', '手的', '一只手', ' rach', 'ré']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass plain27: [' arm', '手臂', ' hand', '臂', '的手臂', ' hands', '手', 'hand', 'arm', ' Arm', '手的', '_arm', 'Arm', ' Hand', 'Hand', '_hand', 'hands', ' forearm', '一只手', '只手', ' arms', '之手', '胳膊', '-hand', '右手', '-arm', ' руки', ' HAND', ' руку', ' bras', ' palm', '手掌']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', 'Stars', '星星', '-star', '/star', '星辰', ' звезды', '之星', '星', ' Star', '星光', '_star', '星的', '恒星', 'Star', ' estrella', ' estrellas', ' étoiles', ' aster', '星座', ' celestial', ' estrel', ' estrelas', ' stella', '颗星', ' bintang', '.star']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

plain lens: [' stars', ' star', '星', 'stars', ' Stars', ' aster', '星的', '_star', ' Star', 'star', '星座', '.star', 'Star', '-stars', '恒星', '之星', ' starred', 'Stars', ' celestial', '-star', '星星', ' astronomers', '星光', ' astronom', ' astro', ' yıld', ' astrology', ' éto', '颗星', ' звезды', ' Astroph', '星级']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', 'Stars', '星星', '-star', '/star', '星辰', ' звезды', '之星', '星', ' Star', '星光', '_star', '星的', '恒星', 'Star', ' estrella', ' estrellas', ' étoiles', ' aster', '星座', ' celestial', ' estrel', ' estrelas', ' stella', '颗星', ' bintang', '.star']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass plain24: [' stars', ' star', '星', 'stars', ' Stars', ' aster', '星的', '_star', ' Star', 'star', '星座', '.star', 'Star', '-stars', '恒星', '之星', ' starred', 'Stars', ' celestial', '-star', '星星', ' astronomers', '星光', ' astronom', ' astro', ' yıld', ' astrology', ' éto', '颗星', ' звезды', ' Astroph', '星级']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass plain27: [' star', ' stars', '星', ' Star', '星的', ' Stars', 'star', 'Star', 'stars', '-star', '_star', '星星', 'Stars', '.star', ' aster', '-stars', '恒星', ' STAR', '-Star', '明星', '之星', ' starred', ' bintang', 'STAR', '星光', ' stellar', '颗星', ' звезды', '/star', '星级', ' éto', ' estrellas']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

J-lens: [' books', ' book', ' Books', 'book', '书籍', 'books', ' BOOK', ' Book', '-book', '-books', 'Books', ' buku', '书的', '一本书', 'Book', '/book', '书', '书本', '/books', ' booklet', 'BOOK', ' bookstore', '的书', '_book', ' книги', '書', '图书', '.book', ' libro', '(book', '之书', '这本书']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

plain lens: ['书籍', ' BOOK', ' books', '一本书', '书', ' book', '书的', '书记', '图书', '加拿大', '这本书', '-books', '一本', '书本', '册', '的书', ' книги', ' книга', '阿拉伯', '.book', '之书', ' Books', ' الكتاب', ' książ', '书名', '/books', ' buku', '书房', 'book', ' книг', '俱乐部', '书包']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass J-lens: [' books', ' book', ' Books', 'book', '书籍', 'books', ' BOOK', ' Book', '-book', '-books', 'Books', ' buku', '书的', '一本书', 'Book', '/book', '书', '书本', '/books', ' booklet', 'BOOK', ' bookstore', '的书', '_book', ' книги', '書', '图书', '.book', ' libro', '(book', '之书', '这本书']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass plain24: ['书籍', ' BOOK', ' books', '一本书', '书', ' book', '书的', '书记', '图书', '加拿大', '这本书', '-books', '一本', '书本', '册', '的书', ' книги', ' книга', '阿拉伯', '.book', '之书', ' Books', ' الكتاب', ' książ', '书名', '/books', ' buku', '书房', 'book', ' книг', '俱乐部', '书包']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass plain27: ['书籍', ' books', ' book', '书', '书的', ' BOOK', 'book', '一本书', '图书', 'books', '书本', ' Books', '这本书', ' Book', '-books', ' книги', 'Book', '_book', '-book', ' книга', '的书', '/books', 'Books', '.book', '/book', '书中', 'BOOK', '书中的', '一本', ' buku', '_BOOK', '之书']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云的', ' cloudy', '云', '云朵', '的云', ' обла', ' nube', '云雾', '云服务', '.Cloud', '云彩', '云计算', ' fog', '云端', '云中', '云海', ' sky', '云平台', 'クラウド', ' 클라우드', ' mây']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

plain lens: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云彩', ' обла', '云的', '/cloud', '雲', '云层', '云朵', '.cloud', '的云', '云计算', '云端', ' cloudy', '云中', '云服务', ' 클라우드', '.Cloud', 'クラウド', '云雾', '天空', ' mây', ' nube', '云上', '云平台', ' Обла']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云的', ' cloudy', '云', '云朵', '的云', ' nube', '云雾', '云服务', '.Cloud', '云彩', '云计算', ' fog', '云端', '云中', '云海', ' sky', '云平台', 'クラウド', ' mây', ' 클라우드', ' skies']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云彩', '云的', '/cloud', '雲', '云层', '云朵', '.cloud', '的云', '云计算', '云端', ' cloudy', '云中', '云服务', ' 클라우드', '.Cloud', 'クラウド', '云雾', '天空', ' mây', '云上', ' nube', '云平台', '云浮', '白云']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass plain27: ['云', 'cloud', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云彩', '云层', '的云', '/cloud', '.cloud', '云朵', '云雾', '云端', '.Cloud', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云天', '云平台', 'クラウド', '云上', '云飞', ' đám', ' nube']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

J-lens: [' pockets', ' pouch', ' pocket', '钱包', '-pocket', ' wallet', '口袋', ' purse', ' suitcase', ' bags', 'Pocket', ' Pocket', '口袋里', ' wallets', ' holster', ' Wallet', 'wallet', ' luggage', ' Bags', ' Taschen', ' bag', 'bags', ' backpack', '袋子', '书包', 'Wallet', ' tote', ' trousers', 'Bags', 'กระเป๋า', ' bracelet', 'bag']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

plain lens: ['随身携带', 'Pocket', ' pockets', '加拿大', '钱包', 'implements', ' Taschen', ' recept', '猜你喜欢', ' LIABILITY', ' pocket', '口袋', 'wallet', ' plec', '袋子', ' pouc', ' tut', '-pocket', '提', '战术', '绽', 'zuh', '揣', '流行病学', 'udit', 'Wallet', ' purse', ' poc', 'favorites', ' Pocket', '收容', '周转']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass J-lens: [' pockets', ' pouch', ' pocket', '钱包', '-pocket', ' wallet', '口袋', ' purse', ' suitcase', ' bags', 'Pocket', ' Pocket', '口袋里', ' wallets', ' holster', ' Wallet', 'wallet', ' luggage', ' Bags', ' Taschen', ' bag', 'bags', ' backpack', '袋子', '书包', 'Wallet', ' tote', ' trousers', 'Bags', 'กระเป๋า', ' bracelet', 'bag']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass plain24: ['随身携带', 'Pocket', ' pockets', '加拿大', '钱包', 'implements', ' Taschen', ' recept', '猜你喜欢', ' LIABILITY', ' pocket', '口袋', 'wallet', ' plec', '袋子', ' pouc', ' tut', '-pocket', '提', '战术', '绽', 'zuh', '揣', '流行病学', 'udit', 'Wallet', ' purse', ' poc', 'favorites', ' Pocket', '收容', '周转']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass plain27: [' pocket', '口袋', ' pockets', 'Pocket', '钱包', ' wallet', '-pocket', ' wallets', ' Pocket', 'Wallet', 'wallet', ' Wallet', '囊', ' bag', '袋', ' pouch', '_wallet', ' túi', '袋子', ' purse', '.wallet', ' bags', 'bags', ' bols', ' Taschen', 'Bag', 'Bags', ' Bags', 'bag', 'กระเป๋า', ' BAG', ' poch']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' jaw', ' lips', ' boca', '嘴', ' saliva', ' throat', ' mulut', '嘴唇', 'lips', ' bouche', ' bocca', ' palate', '口', '喉咙', ' teeth', ' doorway', ' jaws', ' miệng', '口语', ' kiss', ' tongues', '出口', '舌头', '进出口']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

plain lens: [' mouth', 'mouth', '口', ' Mouth', '口腔', ' mouths', '嘴', '口的', '嘴巴', '出口', '进出口', ' oral', '-mouth', '_exports', '聘', '的口', ' mou', 'emouth', '一口', '口红', '口区', '口语', ' bocca', '口头', '开口', '出入口', '嘴唇', 'lips', '口径', '口中', '口才', '张嘴']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' jaw', ' lips', ' boca', '嘴', ' saliva', ' throat', ' mulut', '嘴唇', 'lips', ' bouche', ' bocca', ' palate', '口', '喉咙', ' teeth', ' doorway', ' jaws', ' miệng', '口语', ' kiss', ' tongues', '出口', '舌头', '进出口']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass plain24: [' mouth', 'mouth', '口', ' Mouth', '口腔', ' mouths', '嘴', '口的', '嘴巴', '出口', '进出口', ' oral', '-mouth', '_exports', '聘', '的口', ' mou', 'emouth', '一口', '口红', '口区', '口语', ' bocca', '口头', '开口', '出入口', '嘴唇', 'lips', '口径', '口中', '口才', '张嘴']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass plain27: [' mouth', '口', '嘴', 'mouth', '口的', ' Mouth', ' mouths', '嘴巴', '-mouth', '的口', '口腔', '口中', ' boca', '开口', ' bocca', ' oral', '口の', '口中的', ' bouche', '嘴里', ' miệng', '嘴边', '张口', ' lips', '口に', ' mulut', ' рта', '嘴唇', '唇', ' Oral', '张嘴', '口红']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

J-lens: [' ground', ' soil', ' floor', 'ground', ' earth', 'floor', ' floors', ' flooring', ' terrain', '地板', ' Floor', '土壤', ' Ground', ' Soil', ' dirt', '地面', 'Ground', 'Floor', '-ground', ' tierra', '地基', 'earth', ' terra', ' suelo', ' tanah', ' Terrain', ' pavement', ' soils', ' Earth', '在地上', ' surface', '-floor']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

plain lens: ['地面', ' ground', 'ground', '地面的', '底层', ' soil', 'Ground', '地基', '在地上', 'Floor', ' floor', 'floor', ' أرض', '地板', ' Ground', 'loor', ' Dirt', '土壤', ' Flooring', '_ground', '土', '大地', '底价', '地', '地表', ' terrain', '加拿大', ' Floor', ' zem', '阿拉伯', '基层', 'GROUND']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass J-lens: [' ground', ' soil', ' floor', 'ground', ' earth', 'floor', ' floors', ' flooring', ' terrain', '地板', ' Floor', '土壤', ' Ground', ' Soil', ' dirt', '地面', 'Ground', 'Floor', '-ground', ' tierra', '地基', 'earth', ' terra', ' suelo', ' tanah', ' Terrain', ' pavement', ' soils', ' Earth', '在地上', ' surface', '-floor']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass plain24: ['地面', ' ground', 'ground', '地面的', '底层', ' soil', 'Ground', '地基', '在地上', 'Floor', ' floor', 'floor', ' أرض', '地板', ' Ground', 'loor', ' Dirt', '土壤', ' Flooring', '_ground', '土', '大地', '底价', '地', '地表', ' terrain', '加拿大', ' Floor', ' zem', '阿拉伯', '基层', 'GROUND']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass plain27: [' ground', 'ground', '地面', ' Ground', 'Ground', ' floor', '地板', '地面的', ' soil', 'floor', '土壤', ' suelo', '_ground', ' Floor', 'Floor', ' floors', ' tanah', ' đất', '-ground', '在地上', '地基', '土地', '地', ' Soil', ' أرض', 'GROUND', '地板上', ' earth', ' الأرض', 'grounds', '地面上', ' grounded']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

J-lens: [' mountains', ' mountain', ' Mountains', 'mount', '山脉', 'Mountain', ' hills', '山峰', ' montaña', ' Mountain', ' montagne', ' montagnes', ' hill', ' горы', ' gunung', ' montagna', '山地', '山体', '的山', 'Mount', ' volcano', ' Alps', ' cliffs', '山的', '登山', '山区', ' جبل', '山顶', ' glacier', '-mount', '大山', ' mount']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

plain lens: [' гор', ' mountains', ' mountain', ' Mountains', '山峰', ' montaña', 'mount', ' montagnes', '山脉', 'ountains', 'alic', '加拿大', '阿拉伯', 'informatics', 'bestos', 'imestone', '岗', '音标', '本山', 'verity', 'ugged', '矿', ' Geological', '俱乐部', 'haupt', '_MOUNT', ' montagna', '登山', 'ographical', ' ув', ' горы', 'Mountain']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass J-lens: [' mountains', ' mountain', ' Mountains', 'mount', '山脉', 'Mountain', ' hills', '山峰', ' montaña', ' Mountain', ' montagne', ' montagnes', ' hill', ' montagna', ' gunung', '山体', '山地', '的山', 'Mount', ' volcano', ' Alps', ' cliffs', '山的', '登山', '山区', ' جبل', '山顶', ' glacier', '-mount', ' mount', '大山', ' terrain']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass plain24: [' mountains', ' mountain', ' Mountains', '山峰', ' montaña', 'mount', ' montagnes', '山脉', 'ountains', '加拿大', 'alic', 'informatics', '阿拉伯', 'bestos', 'imestone', '岗', '音标', 'verity', '本山', 'ugged', '矿', ' Geological', 'haupt', '俱乐部', ' montagna', '登山', '_MOUNT', 'ographical', ' ув', 'Mountain', '山顶', '译']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass plain27: [' mountains', ' Mountains', ' mountain', '山峰', '山脉', 'ountains', 'Mountain', 'mount', ' hill', 'Mount', ' núi', '山之', ' montaña', ' montagnes', '山的', '峰', 'OUNT', ' Mountain', ' hills', ' montagne', '_MOUNT', ' хол', '山体', ' mount', 'Peak', ' montagna', 'เนิน', ' Peak', 'ภูเขา', ' Alps', '山大', ' Mount']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

J-lens: [' heart', ' hearts', 'heart', '-heart', '心脏', ' Heart', 'Heart', '的心脏', ' corazón', ' heartbeat', ' сердце', ' Hearts', ' coração', ' сердца', ' Herzen', '心臟', ' cuore', ' قلب', '心跳', ' серд', ' cœur', 'heartbeat', ' cardiac', '心肺', ' heartfelt', ' القلب', '心肌', '-hearted', ' coeur', ' serca', '的心', 'قلب']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

plain lens: [' heart', 'heart', '心脏', ' Heart', 'Heart', '的心脏', ' hearts', ' قلب', ' серд', ' corazón', 'قلب', '-heart', ' сердце', ' القلب', '心的', ' сердца', ' Hearts', ' cœur', ' heartbeat', '心', '的心', ' cuore', '心臟', 'heartbeat', ' καρ', ' Herzen', '这颗', '一颗', ' centrum', '心脏病', 'หัวใจ', ' coração']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass J-lens: [' heart', ' hearts', 'heart', '-heart', '心脏', ' Heart', 'Heart', '的心脏', ' corazón', ' heartbeat', ' Hearts', ' coração', ' Herzen', '心臟', ' cuore', ' قلب', '心跳', 'heartbeat', ' cœur', ' cardiac', '心肺', ' heartfelt', ' القلب', '-hearted', ' coeur', '心肌', '的心', ' serca', 'قلب', '心房', '❤', ' ❤']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass plain24: [' heart', 'heart', '心脏', ' Heart', 'Heart', '的心脏', ' hearts', ' قلب', ' corazón', 'قلب', '-heart', ' القلب', '心的', ' Hearts', ' cœur', ' heartbeat', '心', '的心', ' cuore', '心臟', 'heartbeat', ' καρ', '这颗', ' Herzen', '一颗', ' centrum', '心脏病', 'หัวใจ', ' coração', ' cardiac', '心和', ' coeur']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass plain27: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '-heart', '心脏', ' قلب', '心的', ' corazón', '的心', '的心脏', '心', ' Hearts', ' coração', ' cœur', ' القلب', '心和', 'หัวใจ', ' heartbeat', 'قلب', '-hearted', 'heartbeat', '心臟', ' cuore', ' cardiac', '心脏病', '心跳', ' Herzen', '之心', ' jantung', ' καρ']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

J-lens: [' stars', ' star', ' Stars', 'stars', 'star', '-stars', 'Stars', '-star', '/star', ' Star', '星星', '星', ' aster', '星辰', '之星', ' estrella', ' звезда', 'Star', ' звезды', ' estrellas', '_star', '恒星', '星的', '-Star', ' celestial', '.star', '星座', ' STAR', ' estrel', ' étoiles', ' stella', ' estrelas']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

plain lens: [' stars', ' star', '星', ' Stars', 'stars', '-stars', '星的', '星座', ' celestial', 'Stars', ' aster', ' Star', ' Sternen', '.star', '星辰', '恒星', ' Astronomy', '之星', ' astronomers', ' estrellas', ' звезд', ' نجوم', '星星', ' Bintang', ' звезды', ' bintang', ' звезда', 'Star', '星级', ' Stellar', ' stellar', 'star']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass J-lens: [' stars', ' star', ' Stars', 'stars', 'star', '-stars', 'Stars', '-star', '/star', ' Star', '星星', '星', ' aster', '星辰', '之星', ' estrella', ' звезда', 'Star', ' звезды', ' estrellas', '_star', '恒星', '星的', '-Star', ' celestial', '.star', '星座', ' STAR', ' estrel', ' étoiles', ' stella', ' estrelas']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass plain24: [' stars', ' star', '星', ' Stars', 'stars', '-stars', '星的', '星座', ' celestial', 'Stars', ' aster', ' Star', ' Sternen', '.star', '星辰', '恒星', ' Astronomy', '之星', ' astronomers', ' estrellas', ' звезд', ' نجوم', '星星', ' Bintang', ' звезды', ' bintang', ' звезда', 'Star', '星级', ' Stellar', ' stellar', 'star']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'stars', 'Star', 'star', '-star', 'Stars', '_star', '星星', '.star', '-stars', ' звезд', '-Star', ' STAR', '/star', ' звезды', '之星', ' звезда', ' bintang', ' aster', '恒星', 'STAR', ' starred', ' estrellas', '明星', '星级', ' estrel', ' stellar']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

J-lens: [' Books', ' books', ' book', '书籍', ' Book', 'book', 'books', 'Books', ' BOOK', '-books', ' buku', '一本书', '书的', '-book', 'Book', ' книги', '书本', '书', '/book', '/books', ' Bücher', 'BOOK', ' libro', '_book', ' Libro', ' kitap', ' Buku', ' booklet', '图书', ' bookstore', ' کتاب', ' libri']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

plain lens: [' books', ' book', '书籍', '一本书', ' BOOK', '加拿大', '-books', ' книги', '书记', '书', '阿拉伯', ' książ', ' книге', '册', '书的', 'unread', '课外', '图书', '一本', '这本书', ' Books', '书本', '/books', ' الكتاب', ' knih', '书房', '公司债券', ' kitap', '.book', ' audi', ' knj', ' buku']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass J-lens: [' Books', ' books', ' book', '书籍', ' Book', 'book', 'books', 'Books', ' BOOK', '-books', ' buku', '一本书', '书的', '-book', 'Book', ' книги', '书本', '书', '/book', '/books', ' Bücher', 'BOOK', ' libro', '_book', ' Libro', ' kitap', ' Buku', ' booklet', '图书', ' bookstore', ' کتاب', ' libri']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass plain24: [' books', ' book', '书籍', '一本书', ' BOOK', '加拿大', '-books', ' книги', '书记', '书', '阿拉伯', ' książ', ' книге', '册', '书的', 'unread', '课外', '图书', '一本', '这本书', ' Books', '书本', '/books', ' الكتاب', ' knih', '书房', '公司债券', ' kitap', '.book', ' audi', ' knj', ' buku']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass plain27: [' book', ' books', ' Book', '书', '书籍', ' BOOK', '这本书', ' Books', 'Book', 'book', '书的', '一本书', 'books', ' книги', '-books', '_book', '书本', 'Books', ' книге', '图书', 'BOOK', '书中', '書', '/books', '的书', '书中的', '-book', '.book', '/book', ' buku', '一本', '(book']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

J-lens: [' Cloud', ' clouds', 'cloud', 'Cloud', ' cloud', '-cloud', '_cloud', '/cloud', '.cloud', '云层', '雲', '云的', '云朵', '云', '云服务', ' nube', '云端', '.Cloud', '云计算', '的云', '云平台', '云彩', ' 클라우드', '云雾', '云海', 'クラウド', ' cloudy', '云中', '雲端', ' mây', '乌云', ' iCloud']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

plain lens: ['云', ' cloud', ' Cloud', ' clouds', 'Cloud', 'cloud', '云计算', '云服务', '/cloud', '云层', '_cloud', '云彩', '云端', '.cloud', '云朵', '-cloud', '云的', '雲', '云雾', ' cloudy', '云平台', '的云', ' 클라우드', 'クラウド', '.Cloud', '天空', ' mây', '云中', '云上', '多云', ' nube', '工业协会']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass J-lens: [' Cloud', ' clouds', 'cloud', 'Cloud', ' cloud', '-cloud', '_cloud', '/cloud', '.cloud', '云层', '雲', '云的', '云朵', '云', '云服务', ' nube', '云端', '.Cloud', '云计算', '的云', '云平台', '云彩', ' 클라우드', '云雾', '云海', 'クラウド', ' cloudy', '云中', '雲端', ' mây', '乌云', ' iCloud']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass plain24: ['云', ' cloud', ' Cloud', ' clouds', 'Cloud', 'cloud', '云计算', '云服务', '/cloud', '云层', '_cloud', '云彩', '云端', '.cloud', '云朵', '-cloud', '云的', '雲', '云雾', ' cloudy', '云平台', '的云', ' 클라우드', 'クラウド', '.Cloud', '天空', ' mây', '云中', '云上', '多云', ' nube', '工业协会']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass plain27: ['云', ' cloud', ' Cloud', ' clouds', 'cloud', 'Cloud', '雲', '云的', '-cloud', '_cloud', '云计算', '云彩', '/cloud', '云层', '云端', '云朵', '.cloud', '云服务', '云雾', '的云', ' cloudy', '云平台', '.Cloud', '云中', ' 클라우드', 'クラウド', ' nube', ' mây', '云上', '云天', '云服务器', '云飞']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

J-lens: [' suitcase', ' luggage', ' Bags', ' bags', '书包', ' backpack', 'Bags', 'bags', ' pouch', ' Backpack', ' bag', '钱包', ' baggage', 'bag', '袋子', '行李箱', '背包', 'uggage', '行李', '箱包', ' tote', ' Tasche', 'Bag', ' Bag', ' purse', ' Wallet', '挎', '口袋', 'กระเป๋า', ' 가방', '包包', '-pocket']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

plain lens: ['加拿大', ' bag', 'Summer', ' sum', ' bags', ' suma', ' recept', '手提', ' tote', '..........', ',sum', 'uggage', ' kul', ' kau', '收纳', 'eves', 'inne', ' kont', '书包', '种类繁多', ' gab', '随身携带', ' tut', ' sung', 'いだ', 'informatics', ' prakt', ' Summer', ' bef', '負擔', ' fundament', ' Bags']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass J-lens: [' suitcase', ' luggage', ' Bags', ' bags', '书包', ' backpack', 'Bags', 'bags', ' pouch', ' Backpack', ' bag', '钱包', ' baggage', 'bag', '袋子', '行李箱', '背包', 'uggage', '行李', '箱包', ' tote', ' Tasche', 'Bag', ' Bag', ' purse', ' Wallet', '挎', '口袋', 'กระเป๋า', ' 가방', '包包', '-pocket']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass plain24: ['加拿大', ' bag', 'Summer', ' sum', ' bags', ' suma', ' recept', '手提', ' tote', '..........', ',sum', 'uggage', ' kul', ' kau', '收纳', 'eves', 'inne', ' kont', '书包', '种类繁多', ' gab', '随身携带', ' tut', ' sung', 'いだ', 'informatics', ' prakt', ' Summer', ' bef', '負擔', ' fundament', ' Bags']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass plain27: [' bag', ' bags', ' Bag', 'Bag', '袋', ' Bags', ' BAG', 'bags', 'bag', ' backpack', '袋子', 'Bags', ' moch', ' purse', '_bag', ' tote', ' sack', ' bols', ' túi', 'กระเป๋า', ' tas', '背包', '背', ' Backpack', '手提', ' luggage', ' baggage', 'Wallet', '书包', '钱包', '口袋', '囊']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', ' Teeth', '口腔', ' throat', '-mouth', ' рта', '嘴巴', '喉咙', ' Tooth', ' teeth', ' palate', ' cheeks', ' nose', ' jaw', ' tongue', ' boca', ' Nose', ' Ruhr', ' pores', ' lips', ' mulut', 'roat', ' tooth', ' genitals', '鼻子', '牙齿', '咽喉', '舌头', ' jaws']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

plain lens: [' mouth', ' rot', 'mouth', ' roh', ' Mouth', '膛', '口腔', ' рта', ' porti', '聘', '-mouth', ' rö', '的口', ' råd', ' مخاط', '口', '_exports', '一口', '口才', '嘴巴', '[…', ' fundament', 'fang', ' rut', '口红', ' hör', '嘴', 'phinx', ' būt', '口中的', '轮流', 'roat']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', ' Teeth', '口腔', ' throat', '-mouth', ' рта', '嘴巴', '喉咙', ' Tooth', ' teeth', ' palate', ' cheeks', ' nose', ' jaw', ' tongue', ' boca', ' Nose', ' Ruhr', ' pores', ' lips', ' mulut', 'roat', ' tooth', ' genitals', '鼻子', '牙齿', '咽喉', '舌头', ' jaws']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass plain24: [' mouth', ' rot', 'mouth', ' roh', ' Mouth', '膛', '口腔', ' рта', ' porti', '聘', '-mouth', ' rö', '的口', ' råd', ' مخاط', '口', '_exports', '一口', '口才', '嘴巴', '[…', ' fundament', 'fang', ' rut', '口红', ' hör', '嘴', 'phinx', ' būt', '口中的', '轮流', 'roat']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '嘴巴', ' mouths', '口的', '-mouth', '口腔', ' oral', '的口', '口中', ' рта', '口中的', ' bocca', '开口', ' boca', ' Oral', '张嘴', ' miệng', '口の', ' mulut', '张口', ' bouche', '口红', '口に', '嘴里', ' orale', '口水', '嘴边', '一口']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

J-lens: ['土壤', ' soil', ' Soil', ' soils', '土壤中', ' Terrain', ' почвы', '泥土', ' почву', ' terrain', ' Dirt', '土层', ' tanah', 'terrain', '沃土', 'Earth', 'ground', ' خاک', '土地', ' suolo', ' terreno', ' Boden', 'Ground', 'Terrain', ' suelo', '土的', ' dirt', ' tierra', '土方', '的土地', ' Ground', '地面']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

plain lens: [' soil', '土壤', ' Soil', ' soils', ' почвы', ' почву', '土', '脚下的', ' tanah', '泥土', ' Dirt', ' terrain', '土地', '土壤中', '地表', '土层', ' đất', '表层', 'ดิน', '土的', ' ground', ' Terrain', ' land', '沃土', ' 토', '基质', ' zem', '地基', 'umus', '土石', '_so', ' suelo']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass J-lens: ['土壤', ' soil', ' Soil', ' soils', '土壤中', ' Terrain', ' почвы', '泥土', ' почву', ' terrain', ' Dirt', '土层', ' tanah', 'terrain', '沃土', 'Earth', 'ground', ' خاک', '土地', ' suolo', ' terreno', ' Boden', 'Ground', 'Terrain', ' suelo', '土的', ' dirt', ' tierra', '土方', '的土地', ' Ground', '地面']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass plain24: [' soil', '土壤', ' Soil', ' soils', ' почвы', ' почву', '土', '脚下的', ' tanah', '泥土', ' Dirt', ' terrain', '土地', '土壤中', '地表', '土层', ' đất', '表层', 'ดิน', '土的', ' ground', ' Terrain', ' land', '沃土', ' 토', '基质', ' zem', '地基', 'umus', '土石', '_so', ' suelo']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass plain27: [' soil', '土壤', ' Soil', ' soils', '土', ' tanah', '土壤中', ' почвы', '泥土', ' ground', ' suelo', ' đất', '土的', 'ดิน', ' почву', ' Boden', ' earth', ' Ground', '土层', '土地', 'ground', ' terre', 'Ground', ' suelos', '地面', ' خاک', ' suolo', ' Earth', ' 토', ' грунта', ' Đất', ' грунт']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

J-lens: [' Mountains', ' mountains', ' mountain', ' Mountain', 'mount', 'Mountain', '山峰', ' hills', ' montaña', ' montagne', '山脉', ' Alps', ' montagnes', 'Mount', ' gunung', ' горы', '山的', ' Mount', ' hill', '山体', '的山', ' montagna', '山地', ' Peaks', 'ภูเขา', '-mount', ' volcano', ' Hills', ' جبل', ' núi', ' Gunung', '名山']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

plain lens: [' mountains', '加拿大', ' mountain', ' montaña', '山峰', ' Mountains', 'Mount', ' справед', 'mener', '阿拉伯', ' hör', 'aurus', '吼', '峰', '_MOUNT', '升起', 'ountains', ' Geological', 'peater', ' horn', 'mount', ' naud', '姆斯', '发卡', ' hill', ' truk', 'imestone', ' Mounted', ' hil', '上山', '一点儿', 'yms']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass J-lens: [' Mountains', ' mountains', ' mountain', ' Mountain', 'mount', 'Mountain', '山峰', ' hills', ' montaña', ' montagne', '山脉', ' Alps', ' montagnes', 'Mount', ' gunung', ' горы', '山的', ' Mount', ' hill', '山体', '的山', ' montagna', '山地', ' Peaks', 'ภูเขา', '-mount', ' volcano', ' Hills', ' جبل', ' núi', ' Gunung', '名山']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass plain24: [' mountains', '加拿大', ' mountain', ' montaña', '山峰', ' Mountains', 'Mount', ' справед', 'mener', '阿拉伯', ' hör', 'aurus', '吼', '峰', '_MOUNT', '升起', 'ountains', ' Geological', 'peater', ' horn', 'mount', ' naud', '姆斯', '发卡', ' hill', ' truk', 'imestone', ' Mounted', ' hil', '上山', '一点儿', 'yms']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass plain27: [' mountains', ' Mountains', ' mountain', '峰', 'Mount', 'Mountain', '山峰', ' Mountain', ' Peak', ' núi', ' Mount', ' montaña', 'Peak', ' горы', 'mount', ' hill', ' mount', ' mitochond', ' Alps', '加拿大', '山大', ' peak', ' peaks', 'ountains', '山脉', '山之', ' montagne', 'OUNT', '山的', ' hil', '山上', ' Alp']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

J-lens: [' Heart', '心脏', 'heart', 'Heart', ' heart', ' hearts', '的心脏', ' Hearts', '-heart', ' corazón', ' сердца', ' coração', '心臟', ' cuore', ' قلب', ' cœur', '心跳', ' Herz', 'heartbeat', ' Herzen', ' heartbeat', '心肺', ' القلب', '心脏病', 'หัวใจ', ' coeur', ' jantung', 'card', '心率', '的心', ' serca', '心']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

plain lens: [' heart', ' Heart', '的心脏', 'heart', '心脏', ' сердца', 'Heart', ' corazón', ' hearts', 'قلب', ' القلب', '-heart', ' قلب', '心', '的心', ' centrum', '心的', '心率', '一颗', ' cœur', ' Hearts', 'heartbeat', '心跳', ' καρ', '全心全意', '这颗', ' сердечно', '心臟', '-hearted', '心脏病', 'หัวใจ', ' coração']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass J-lens: [' Heart', '心脏', 'heart', 'Heart', ' heart', ' hearts', '的心脏', ' Hearts', '-heart', ' corazón', ' сердца', ' coração', '心臟', ' cuore', ' قلب', ' cœur', '心跳', 'heartbeat', ' heartbeat', '心肺', ' القلب', '心脏病', 'หัวใจ', ' coeur', ' jantung', '心率', '的心', 'card', ' serca', '心', 'قلب', '-hearted']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass plain24: [' heart', ' Heart', '的心脏', 'heart', '心脏', ' сердца', 'Heart', ' corazón', ' hearts', 'قلب', ' القلب', '-heart', ' قلب', '心', '的心', ' centrum', '心的', '心率', '一颗', ' cœur', ' Hearts', 'heartbeat', '心跳', ' καρ', '全心全意', '这颗', ' сердечно', '心臟', '-hearted', '心脏病', 'หัวใจ', ' coração']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', ' قلب', '的心', ' сердца', ' corazón', '心的', '的心脏', ' cœur', 'หัวใจ', ' Hearts', '-hearted', 'قلب', ' coração', ' القلب', '心跳', ' hart', ' heartbeat', ' cardiac', '心和', '心脏病', ' cuore', '之心', ' καρ', '心臟', 'heartbeat']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

J-lens: [' Stars', ' stars', ' star', 'stars', 'star', 'Stars', '-stars', ' Star', '星星', '-star', '星辰', ' звезды', '/star', '_star', 'Star', '星', '-Star', ' estrella', '星光', '星的', '之星', ' estrellas', '明星', '.star', '星空', '恒星', ' stella', ' bintang', ' estrelas', '颗星', ' stelle', ' Stard']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

plain lens: [' stars', ' star', '星', ' Stars', '-stars', '星的', 'stars', '_star', ' Star', 'star', '.star', '星辰', '星座', 'Stars', '星星', ' звезды', 'Star', '-star', '星光', ' starred', ' نجوم', ' bintang', ' stellar', ' celestial', '恒星', ' Astroph', '颗星', ' aster', '/star', '星级', '明星', ' estrellas']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass J-lens: [' Stars', ' stars', ' star', 'stars', 'star', 'Stars', '-stars', ' Star', '星星', '-star', '星辰', ' звезды', '/star', '_star', 'Star', '星', '-Star', ' estrella', '星光', '星的', '之星', ' estrellas', '明星', '.star', '星空', '恒星', ' stella', ' bintang', ' estrelas', '颗星', ' stelle', ' Stard']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass plain24: [' stars', ' star', '星', ' Stars', '-stars', '星的', 'stars', '_star', ' Star', 'star', '.star', '星辰', '星座', 'Stars', '星星', ' звезды', 'Star', '-star', '星光', ' starred', ' نجوم', ' bintang', ' stellar', ' celestial', '恒星', ' Astroph', '颗星', ' aster', '/star', '星级', '明星', ' estrellas']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '_star', 'stars', '-star', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезды', '明星', ' STAR', ' bintang', '星光', '恒星', ' stellar', '之星', ' starred', '星级', ' aster', 'STAR', ' estrellas', '星辰', '_STAR']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '云层', '/cloud', '.cloud', '_cloud', '雲', '云', '云的', ' nube', '云朵', ' обла', '的云', ' cloudy', '.Cloud', '云彩', '云雾', '云服务', '云端', ' mây', '云海', '乌云', '云计算', '云平台', '云中', ' 클라우드', 'クラウド', ' Обла']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

plain lens: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', ' обла', '云彩', '/cloud', '_cloud', '-cloud', '云计算', '云的', '云层', '雲', '.cloud', '的云', '云朵', '云服务', ' cloudy', '云端', '.Cloud', ' mây', ' 클라우드', 'クラウド', ' nube', '云雾', '云中', '天气', '天空', '云山', '云平台']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '云层', '/cloud', '.cloud', '_cloud', '雲', '云', '云的', ' nube', '云朵', ' обла', '的云', ' cloudy', '.Cloud', '云彩', '云雾', '云服务', '云端', ' mây', '云海', '乌云', '云计算', '云平台', '云中', ' 클라우드', 'クラウド', ' Обла']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', ' обла', '云彩', '/cloud', '_cloud', '-cloud', '云计算', '云的', '云层', '雲', '.cloud', '的云', '云朵', '云服务', ' cloudy', '云端', '.Cloud', ' mây', ' 클라우드', 'クラウド', ' nube', '云雾', '云中', '天气', '天空', '云山', '云平台']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass plain27: ['云', ' cloud', ' clouds', ' Cloud', 'cloud', 'Cloud', '雲', '云的', '-cloud', '云彩', '_cloud', ' обла', '/cloud', '云层', '云朵', '云计算', '的云', '.cloud', ' cloudy', '云端', '云雾', '.Cloud', '云服务', '云平台', ' mây', '云中', ' nube', ' 클라우드', '云飞', '云天', 'クラウド', '云上']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

J-lens: [' Bags', ' bags', '钱包', '书包', ' suitcase', '袋子', ' pouch', ' bag', 'bags', ' sack', 'Bags', ' sacks', 'bag', ' wallet', ' Wallet', ' luggage', ' pocket', ' Bag', '口袋', '-pocket', ' backpack', ' Tasche', ' Taschen', 'wallet', ' sacs', 'Bag', ' baggage', ' Basket', ' basket', ' 가방', ' Backpack', 'packet']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

plain lens: ['加拿大', '袋子', '阿拉伯', ' recept', ' bag', '书包', 'ISATION', ' bags', 'вершенство', ' sach', 'unread', 'OnChange', '钱包', ' Saga', 'Bags', ' Bags', ' Sachs', ' tut', ' plec', '随身携带', ' рекв', 'editary', '种类繁多', ' prakt', '一脸', 'verity', ' Adventure', 'reatest', '卖点', 'implements', ' sak', ' bols']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass J-lens: [' Bags', ' bags', '钱包', '书包', ' suitcase', '袋子', ' pouch', ' bag', 'bags', ' sack', 'Bags', ' sacks', 'bag', ' wallet', ' Wallet', ' luggage', ' pocket', ' Bag', '口袋', '-pocket', ' backpack', ' Tasche', ' Taschen', 'wallet', ' sacs', 'Bag', ' baggage', ' Basket', ' basket', ' 가방', ' Backpack', 'packet']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass plain24: ['加拿大', '袋子', '阿拉伯', ' recept', ' bag', '书包', 'ISATION', ' bags', 'вершенство', ' sach', 'unread', 'OnChange', '钱包', ' Saga', 'Bags', ' Bags', ' Sachs', ' tut', ' plec', '随身携带', ' рекв', 'editary', '种类繁多', ' prakt', '一脸', 'verity', ' Adventure', 'reatest', '卖点', 'implements', ' sak', ' bols']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass plain27: [' bag', ' bags', '袋', '袋子', ' Bag', ' Bags', 'Bag', ' BAG', 'bags', 'bag', '口袋', ' túi', ' sack', 'Bags', '_bag', '钱包', 'Wallet', '布袋', ' purse', '购物', ' sacks', 'beutel', ' wallet', ' bols', '书包', ' pouch', ' pocket', ' pockets', ' moch', '囊', ' Wallet', ' tas']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', '-mouth', '嘴巴', '口腔', ' boca', '嘴', ' Teeth', ' tongue', ' jaw', ' bocca', ' throat', ' lips', ' mulut', ' jaws', ' teeth', '舌头', ' cheeks', '喉咙', '牙齿', '口语', ' palate', ' saliva', '嘴唇', ' Speech', 'lips', ' tongues', ' speech', '口才', ' bite']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

plain lens: [' mouth', '嘴', 'mouth', ' Mouth', '嘴巴', '口', '口腔', ' mouths', '-mouth', '开口', ' bocca', '口语', '一口', '的口', ' oral', '口才', ' spok', 'emouth', 'fang', '嘴边', '张嘴', '口头', '进出口', '姆斯', '出口', ' Oral', 'unciation', ' mulut', ' рта', '口区', ' Grimm', '口的']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', '-mouth', '嘴巴', '口腔', ' boca', '嘴', ' Teeth', ' tongue', ' jaw', ' bocca', ' throat', ' lips', ' mulut', ' jaws', ' teeth', '舌头', ' cheeks', '喉咙', '牙齿', '口语', ' palate', ' saliva', '嘴唇', ' Speech', 'lips', ' tongues', ' speech', '口才', ' bite']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass plain24: [' mouth', '嘴', 'mouth', ' Mouth', '嘴巴', '口', '口腔', ' mouths', '-mouth', '开口', ' bocca', '口语', '一口', '的口', ' oral', '口才', ' spok', 'emouth', 'fang', '嘴边', '张嘴', '口头', '进出口', '姆斯', '出口', ' Oral', 'unciation', ' mulut', ' рта', '口区', ' Grimm', '口的']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass plain27: [' mouth', '口', '嘴', ' Mouth', '嘴巴', 'mouth', ' mouths', '口的', '-mouth', '口腔', ' oral', '的口', ' boca', ' bocca', '开口', '口中', ' Oral', '张嘴', '嘴边', ' mulut', ' miệng', '口中的', '口の', ' рта', '张口', '嘴里', '口に', '口头', '唇', 'emouth', '嘴唇', ' orale']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

J-lens: [' soil', 'ground', ' ground', 'floor', '土壤', ' Soil', ' floor', ' pavement', ' suelo', '地板', ' Floor', ' Terrain', ' floors', ' flooring', ' Ground', '地面', 'surface', 'Ground', ' terrain', 'Floor', ' suolo', ' soils', ' surface', ' dirt', '土壤中', '-ground', '地基', ' Floors', ' sidewalk', ' earth', ' Flooring', '地面的']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

plain lens: [' soil', '脚下的', '_sol', '地面', ' ground', '土壤', ' сол', ' suelo', ' fundament', '脚下', ' sols', '土地', '混凝', '地板', ' Flooring', '地基', '太阳', ' floor', ' tanah', '地砖', 'crete', 'floor', 'Floor', ' pavement', ' أرض', '_solution', 'bestos', 'Ground', 'solver', ' Soil', '地表', 'loor']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass J-lens: [' soil', 'ground', ' ground', 'floor', '土壤', ' Soil', ' floor', ' pavement', ' suelo', '地板', ' Floor', ' Terrain', ' floors', ' flooring', ' Ground', '地面', 'surface', 'Ground', ' terrain', 'Floor', ' suolo', ' soils', ' surface', ' dirt', '土壤中', '-ground', '地基', ' Floors', ' sidewalk', ' earth', ' Flooring', '地面的']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass plain24: [' soil', '脚下的', '_sol', '地面', ' ground', '土壤', ' сол', ' suelo', ' fundament', '脚下', ' sols', '土地', '混凝', '地板', ' Flooring', '地基', '太阳', ' floor', ' tanah', '地砖', 'crete', 'floor', 'Floor', ' pavement', ' أرض', '_solution', 'bestos', 'Ground', 'solver', ' Soil', '地表', 'loor']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass plain27: [' ground', '地面', ' floor', ' Ground', 'ground', '地板', 'Ground', ' suelo', ' soil', ' Floor', 'floor', '地面的', 'Floor', ' tanah', '_ground', '土壤', ' Boden', ' floors', '土地', '-ground', ' terre', '地表', ' đất', '地面上', '地砖', ' Soil', ' flooring', ' Flooring', ' grounds', '在地上', '地板上', ' earth']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

J-lens: [' mountains', ' mountain', ' Mountains', ' Mountain', 'mount', 'Mountain', ' montaña', ' hills', '山脉', ' montagnes', ' Alps', '山峰', 'Mount', ' Mount', ' montagna', ' mount', ' gunung', '-mount', ' hill', '山地', ' volcano', ' горы', '山区', '的山', '山的', ' Peaks', ' countryside', ' núi', '山体', 'ountain', ' Highlands', ' Hills']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

plain lens: [' mountains', ' mountain', ' Mountains', 'mount', ' montaña', '山峰', 'Mount', '加拿大', ' гор', ' montagnes', ' mount', '山脉', '_MOUNT', 'Mountain', 'ountains', '阿拉伯', ' Mountain', '峰', ' 산', ' montagna', ' Alps', 'alic', '姆斯', '耸', '的山', '卖点', ' inland', 'OUNT', ' peaks', '-mount', ' gunung', ' Mounted']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass J-lens: [' mountains', ' mountain', ' Mountains', ' Mountain', 'mount', 'Mountain', ' montaña', ' hills', '山脉', ' montagnes', ' Alps', '山峰', 'Mount', ' Mount', ' montagna', ' mount', ' gunung', '-mount', ' hill', '山地', ' volcano', ' горы', '山区', '的山', '山的', ' Peaks', ' countryside', ' núi', '山体', 'ountain', ' Highlands', ' Hills']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass plain24: [' mountains', ' mountain', ' Mountains', 'mount', ' montaña', '山峰', 'Mount', '加拿大', ' гор', ' montagnes', ' mount', '山脉', '_MOUNT', 'Mountain', 'ountains', '阿拉伯', ' Mountain', '峰', ' 산', ' montagna', ' Alps', 'alic', '姆斯', '耸', '的山', '卖点', ' inland', 'OUNT', ' peaks', '-mount', ' gunung', ' Mounted']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass plain27: [' mountains', ' Mountains', ' mountain', 'Mountain', ' Mountain', 'Mount', 'mount', '峰', ' núi', '山峰', ' гор', ' montaña', ' mount', ' Peak', ' горы', '山脉', ' Alps', ' Mount', 'ountains', ' Alp', 'Peak', '山的', ' hill', '山大', ' montagnes', ' peaks', '山人', ' peak', ' mitochond', 'OUNT', 'ภูเขา', '山之']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

J-lens: [' Heart', ' heart', 'heart', ' hearts', 'Heart', ' Hearts', '-heart', '心脏', '的心脏', ' corazón', ' coração', ' сердце', ' cuore', ' сердца', '心臟', ' قلب', ' heartbeat', ' серд', ' Herz', ' Herzen', '心跳', 'heartbeat', ' coeur', '心肺', ' heartfelt', ' cardiac', ' القلب', '❤', '的心', 'หัวใจ', ' jantung', '-hearted']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

plain lens: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '的心脏', '心脏', ' серд', ' сердце', '心', '心的', ' сердца', '的心', ' corazón', ' قلب', '-heart', ' القلب', ' Hearts', 'قلب', '心了', '心和', ' καρ', '心跳', '心头', '心脏病', '心率', 'heartbeat', '之心', '这颗', '心臟', ' coeur', 'หัวใจ']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass J-lens: [' Heart', ' heart', 'heart', ' hearts', 'Heart', ' Hearts', '-heart', '心脏', '的心脏', ' corazón', ' coração', ' сердце', ' cuore', ' сердца', '心臟', ' قلب', ' heartbeat', ' серд', '心跳', 'heartbeat', ' coeur', '心肺', ' heartfelt', ' cardiac', ' القلب', '❤', '的心', 'หัวใจ', ' jantung', '-hearted', ' Core', '心肌']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass plain24: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '的心脏', '心脏', ' серд', ' сердце', '心', '心的', ' сердца', '的心', ' corazón', ' قلب', '-heart', ' القلب', ' Hearts', 'قلب', '心了', '心和', ' καρ', '心跳', '心头', '心脏病', '心率', 'heartbeat', '之心', '这颗', '心臟', ' coeur', 'หัวใจ']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', '的心', ' сердце', ' قلب', '心的', ' сердца', ' серд', ' corazón', '的心脏', ' Hearts', 'หัวใจ', ' القلب', '心和', '-hearted', ' coração', '心跳', ' καρ', 'قلب', ' hart', ' cardiac', ' cuore', '之心', ' heartbeat', '心了', '心脏病']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

J-lens: ['day', ' day', ' daytime', ' daylight', 'Day', 'days', ' days', ' morning', ' Day', '_day', '/day', ' mornings', '白天', 'Days', ' Days', ' afternoon', '-day', ' sunrise', ' journée', ' DAY', ' evening', '(day', ' день', ' nights', '-days', '.day', ' днем', ' дня', ' night', 'DAY', '的一天', ' día']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

plain lens: ['day', ' day', ' daylight', '太阳', '加拿大', '姆斯', ' daytime', '天的', '阿拉伯', ' ημέ', '日光', ' дня', ' sun', '中午', '白天', '-day', ' scho', 'Day', ' days', '日生', '晴天', ' день', '一天的', ' Présent', ' النهار', '日', '日出', '日的', '青天', '_day', '阳光', '天空']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass J-lens: ['day', ' day', ' daytime', ' daylight', 'Day', 'days', ' days', ' morning', ' Day', '_day', '/day', ' mornings', '白天', 'Days', ' Days', ' afternoon', '-day', ' sunrise', ' journée', ' DAY', ' evening', '(day', ' день', ' nights', '-days', '.day', ' днем', ' дня', ' night', 'DAY', '的一天', ' día']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass plain24: ['day', ' day', ' daylight', '太阳', '加拿大', '姆斯', ' daytime', '天的', '阿拉伯', ' ημέ', '日光', ' дня', ' sun', '中午', '白天', '-day', ' scho', 'Day', ' days', '日生', '晴天', ' день', '一天的', ' Présent', ' النهار', '日', '日出', '日的', '青天', '_day', '阳光', '天空']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass plain27: [' day', 'day', '-day', ' Day', 'Day', '_day', ' DAY', '日', ' days', ' день', ' día', ' дня', ' dag', ' daylight', '-Day', '.day', '日的', '(day', '一天', '\tday', ' daytime', '一天的', ' روز', 'Days', '天的', ' ngày', 'DAY', '/day', '白天', '日子', 'День', ' giorno']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

J-lens: [' stars', ' star', ' Stars', 'star', 'stars', 'Stars', '-stars', '-star', ' Star', '星星', ' звезда', ' estrella', '/star', 'Star', '星辰', '星', ' звезды', '_star', '-Star', ' estrellas', '之星', '星光', ' aster', '星的', '.star', ' étoiles', ' estrel', ' stelle', ' estrelas', ' stella', '星标', '颗星']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

plain lens: [' stars', ' star', '星', ' Stars', '-stars', 'stars', ' Star', '星的', '.star', 'star', '_star', 'Stars', '星辰', ' aster', '星星', '-star', ' نجوم', 'Star', ' звезд', ' stellar', '星光', ' звезда', ' estrellas', ' звезды', '之星', ' starred', '颗星', ' bintang', '/star', '星级', ' stell', ' estrelas']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass J-lens: [' stars', ' star', ' Stars', 'star', 'stars', 'Stars', '-stars', '-star', ' Star', '星星', ' звезда', ' estrella', '/star', 'Star', '星辰', '星', ' звезды', '_star', '-Star', ' estrellas', '之星', '星光', ' aster', '星的', '.star', ' étoiles', ' estrel', ' stelle', ' estrelas', ' stella', '星标', '颗星']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass plain24: [' stars', ' star', '星', ' Stars', '-stars', 'stars', ' Star', '星的', '.star', 'star', '_star', 'Stars', '星辰', ' aster', '星星', '-star', ' نجوم', 'Star', ' звезд', ' stellar', '星光', ' звезда', ' estrellas', ' звезды', '之星', ' starred', '颗星', ' bintang', '/star', '星级', ' stell', ' estrelas']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '-star', 'stars', '_star', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезд', ' звезды', ' STAR', ' звезда', ' bintang', '明星', ' stellar', ' estrellas', '之星', '星光', 'STAR', '星级', ' aster', ' starred', ' estrella']


## Fixed-set readout results

Joint pass means a hidden alias is found and all lexical words in the eight-token continuation are excluded. Unscored rows remain in the full denominator but cannot earn a pass. Correct-answer columns condition on an expected answer alias appearing. Neither proves internal reasoning.

### Current-layer methods

| method                     | joint↑   |   AUROC↑ | correct-answer joint↑   |   unscored |
|:---------------------------|:---------|---------:|:------------------------|-----------:|
| [plain lens](readout.json) | 32/48    |    0.912 | 30/43                   |          2 |
| [J-lens](readout.json)     | 27/48    |    0.912 | 24/43                   |          2 |

### End-of-pass readout (not for earlier edits)

| method                           | joint↑   |   AUROC↑ | correct-answer joint↑   |   unscored |
|:---------------------------------|:---------|---------:|:------------------------|-----------:|
| [end-pass J-lens](readout.json)  | 39/48    |    0.951 | 34/43                   |          2 |
| [end-pass plain24](readout.json) | 39/48    |    0.945 | 35/43                   |          2 |
| [end-pass plain27](readout.json) | 33/48    |    0.955 | 28/43                   |          2 |

### Translation development/test splits

| split   | method           | joint↑   |   AUROC↑ |   unscored |
|:--------|:-----------------|:---------|---------:|-----------:|
| dev     | J-lens           | 4/8      |    0.947 |          1 |
| dev     | plain lens       | 5/8      |    0.954 |          1 |
| dev     | end-pass J-lens  | 6/8      |    0.980 |          1 |
| dev     | end-pass plain24 | 6/8      |    0.977 |          1 |
| dev     | end-pass plain27 | 5/8      |    0.983 |          1 |
| test    | J-lens           | 23/40    |    0.906 |          1 |
| test    | plain lens       | 27/40    |    0.904 |          1 |
| test    | end-pass J-lens  | 33/40    |    0.946 |          1 |
| test    | end-pass plain24 | 33/40    |    0.940 |          1 |
| test    | end-pass plain27 | 28/40    |    0.950 |          1 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_104102_jlens-one-pass/run.md
