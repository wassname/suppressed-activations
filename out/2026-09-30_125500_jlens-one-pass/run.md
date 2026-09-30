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
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 57.83
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Same layer, final position, k32 and prompt mask as before. Selection: First8 prefix-label-eligible words per pair in pinned CSV order; four-shot prompts use seed0 and script04 sampling. No output filtering. de→fr is development, five other de/fr/ru pairs are test; de→zh remains historical reference. English/Chinese hidden labels and their prefix lengths affect scoring only. Frozen after English development; no translation retuning. Concepts recur across language pairs, so prompts are not independent concepts. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Historical cached continuations are regenerated with the same eight-token cap. Scoring definitions are unchanged. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                     | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:---------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| cloud     | J-lens                     | False         |                    |             1 |             1000000000 |                |              |
| cloud     | plain lens                 | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass J-lens            | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain24           | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain27           | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased1 J-lens    | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 J-lens  | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain24   | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain24 | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain27   | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain27 | False         |                    |             0 |             1000000000 |                |              |
| bag       | J-lens                     | True          |           0.980392 |            10 |                   1685 | True           | True         |
| bag       | plain lens                 | True          |           0.911765 |             3 |                    198 | True           | True         |
| bag       | end-pass J-lens            | True          |           0.980392 |            10 |                   1685 | True           | True         |
| bag       | end-pass plain24           | True          |           0.911765 |             3 |                    198 | True           | True         |
| bag       | end-pass plain27           | False         |           0.960784 |             0 |                     16 | False          | False        |
| bag       | end-pass erased1 J-lens    | True          |           0.980392 |            11 |                   2026 | True           | True         |
| bag       | end-pass erased0.5 J-lens  | True          |           0.980392 |            10 |                   1894 | True           | True         |
| bag       | end-pass erased1 plain24   | True          |           0.911765 |             3 |                    177 | True           | True         |
| bag       | end-pass erased0.5 plain24 | True          |           0.911765 |             3 |                    188 | True           | True         |
| bag       | end-pass erased1 plain27   | False         |           0.960784 |             0 |                     15 | False          | False        |
| bag       | end-pass erased0.5 plain27 | False         |           0.960784 |             0 |                     16 | False          | False        |
| mouth     | J-lens                     | False         |           0.970588 |             0 |                     10 | False          | False        |
| mouth     | plain lens                 | True          |           0.980392 |             0 |                     52 | True           | True         |
| mouth     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27           | True          |           0.990196 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           0.970588 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           0.990196 |             0 |             1000000000 | True           | True         |
| soil      | J-lens                     | True          |           0.885714 |             0 |                   6179 | True           | True         |
| soil      | plain lens                 | True          |           0.952381 |             0 |                   5727 | True           | True         |
| soil      | end-pass J-lens            | True          |           0.961905 |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain27           | True          |           1        |             2 |             1000000000 | True           | True         |
| soil      | end-pass erased1 J-lens    | True          |           0.904762 |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 J-lens  | True          |           0.92381  |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased1 plain24   | True          |           0.980952 |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           0.980952 |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased1 plain27   | True          |           1        |             2 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | J-lens                     | False         |           0.875    |             0 |                      4 | False          | False        |
| mountain  | plain lens                 | False         |           0.910714 |             1 |                     15 | False          | False        |
| mountain  | end-pass J-lens            | True          |           0.989286 |             0 |             1000000000 | True           | True         |
| mountain  | end-pass plain24           | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27           | True          |           0.992857 |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           0.989286 |             0 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           0.989286 |             0 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           0.996429 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           0.996429 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           0.992857 |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           0.992857 |             2 |             1000000000 | True           | True         |
| heart     | J-lens                     | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | plain lens                 | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass J-lens            | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | end-pass plain24           | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass plain27           | False         |           0.968254 |             0 |                     10 | False          | False        |
| heart     | end-pass erased1 J-lens    | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | end-pass erased0.5 J-lens  | False         |           0.960317 |             0 |                     12 | False          | False        |
| heart     | end-pass erased1 plain24   | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass erased0.5 plain24 | False         |           0.968254 |             0 |                     13 | False          | False        |
| heart     | end-pass erased1 plain27   | False         |           0.968254 |             0 |                     11 | False          | False        |
| heart     | end-pass erased0.5 plain27 | False         |           0.968254 |             0 |                     11 | False          | False        |
| day       | J-lens                     | True          |           0.992188 |             0 |                     72 | True           | True         |
| day       | plain lens                 | True          |           1        |             0 |                   2941 | True           | True         |
| day       | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens                     | True          |           0.967033 |             1 |                     58 | True           | True         |
| star      | plain lens                 | True          |           0.956044 |             1 |                     32 | True           | True         |
| star      | end-pass J-lens            | True          |           0.967033 |             1 |                     58 | True           | True         |
| star      | end-pass plain24           | True          |           0.956044 |             1 |                     32 | True           | True         |
| star      | end-pass plain27           | True          |           0.967033 |             0 |                     36 | True           | True         |
| star      | end-pass erased1 J-lens    | True          |           0.967033 |             1 |                     59 | True           | True         |
| star      | end-pass erased0.5 J-lens  | True          |           0.967033 |             1 |                     58 | True           | True         |
| star      | end-pass erased1 plain24   | True          |           0.956044 |             1 |                     39 | True           | True         |
| star      | end-pass erased0.5 plain24 | True          |           0.956044 |             1 |                     35 | True           | True         |
| star      | end-pass erased1 plain27   | True          |           0.967033 |             0 |                     36 | True           | True         |
| star      | end-pass erased0.5 plain27 | True          |           0.967033 |             0 |                     36 | True           | True         |
| cloud     | J-lens                     | False         |           0.934641 |             1 |                     17 | False          | False        |
| cloud     | plain lens                 | False         |           0.941176 |             2 |                      6 | False          | False        |
| cloud     | end-pass J-lens            | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass plain24           | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 J-lens    | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 plain24   | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 plain24 | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| bag       | J-lens                     | True          |           1        |             5 |                   3484 | True           | True         |
| bag       | plain lens                 | True          |           0.977778 |            21 |                   1051 | True           | True         |
| bag       | end-pass J-lens            | True          |           1        |             5 |                   3484 | True           | True         |
| bag       | end-pass plain24           | True          |           0.977778 |            21 |                   1050 | True           | True         |
| bag       | end-pass plain27           | False         |           1        |             0 |                     29 | False          | False        |
| bag       | end-pass erased1 J-lens    | True          |           1        |             5 |                   4065 | True           | True         |
| bag       | end-pass erased0.5 J-lens  | True          |           1        |             5 |                   3772 | True           | True         |
| bag       | end-pass erased1 plain24   | True          |           0.977778 |            21 |                   1213 | True           | True         |
| bag       | end-pass erased0.5 plain24 | True          |           0.977778 |            22 |                   1110 | True           | True         |
| bag       | end-pass erased1 plain27   | True          |           1        |             0 |                     34 | True           | True         |
| bag       | end-pass erased0.5 plain27 | True          |           1        |             0 |                     32 | True           | True         |
| mouth     | J-lens                     | True          |           0.992424 |             0 |                    778 | True           | True         |
| mouth     | plain lens                 | True          |           0.977273 |             0 |                    215 | True           | True         |
| mouth     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24           | True          |           0.992424 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           0.992424 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           0.992424 |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens                     | True          |           0.888889 |             0 |                   3187 | True           | True         |
| soil      | plain lens                 | True          |           0.955556 |             5 |                    684 | True           | True         |
| soil      | end-pass J-lens            | True          |           1        |             0 |                   3178 | True           | True         |
| soil      | end-pass plain24           | True          |           1        |             5 |                    684 | True           | True         |
| soil      | end-pass plain27           | True          |           1        |             0 |                     80 | True           | True         |
| soil      | end-pass erased1 J-lens    | True          |           1        |             0 |                   3211 | True           | True         |
| soil      | end-pass erased0.5 J-lens  | True          |           1        |             0 |                   3127 | True           | True         |
| soil      | end-pass erased1 plain24   | True          |           1        |             5 |                    647 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           1        |             5 |                    666 | True           | True         |
| soil      | end-pass erased1 plain27   | True          |           1        |             0 |                     63 | True           | True         |
| soil      | end-pass erased0.5 plain27 | True          |           1        |             0 |                     72 | True           | True         |
| mountain  | J-lens                     | False         |           0.938889 |             0 |                     61 | True           | True         |
| mountain  | plain lens                 | False         |           0.9      |             1 |                      2 | False          | False        |
| mountain  | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | end-pass plain24           | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27           | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| heart     | J-lens                     | False         |           0.894444 |             0 |                      9 | False          | False        |
| heart     | plain lens                 | False         |           0.872222 |             0 |                      5 | False          | False        |
| heart     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | J-lens                     | True          |           0.926471 |             0 |                     91 | True           | True         |
| hand      | plain lens                 | True          |           0.936275 |            18 |                    265 | True           | True         |
| hand      | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain24           | True          |           1        |            18 |             1000000000 | True           | True         |
| hand      | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased1 plain24   | True          |           1        |            30 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 plain24 | True          |           1        |            24 |             1000000000 | True           | True         |
| hand      | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens                     | False         |           0.9      |             1 |                     12 | False          | False        |
| star      | plain lens                 | False         |           0.903846 |             1 |                     21 | False          | False        |
| star      | end-pass J-lens            | False         |           0.9      |             1 |                     12 | False          | False        |
| star      | end-pass plain24           | False         |           0.903846 |             1 |                     21 | False          | False        |
| star      | end-pass plain27           | False         |           0.919231 |             0 |                     16 | False          | False        |
| star      | end-pass erased1 J-lens    | False         |           0.9      |             1 |                     12 | False          | False        |
| star      | end-pass erased0.5 J-lens  | False         |           0.9      |             1 |                     13 | False          | False        |
| star      | end-pass erased1 plain24   | False         |           0.903846 |             1 |                     24 | False          | False        |
| star      | end-pass erased0.5 plain24 | False         |           0.903846 |             1 |                     23 | False          | False        |
| star      | end-pass erased1 plain27   | False         |           0.923077 |             0 |                     16 | False          | False        |
| star      | end-pass erased0.5 plain27 | False         |           0.919231 |             0 |                     16 | False          | False        |
| cloud     | J-lens                     | False         |                    |             1 |             1000000000 |                |              |
| cloud     | plain lens                 | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass J-lens            | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain24           | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass plain27           | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased1 J-lens    | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 J-lens  | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain24   | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain24 | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain27   | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain27 | False         |                    |             0 |             1000000000 |                |              |
| bag       | J-lens                     | True          |           1        |             6 |                   2420 | True           | True         |
| bag       | plain lens                 | True          |           0.841667 |             0 |                    109 | True           | True         |
| bag       | end-pass J-lens            | True          |           1        |             6 |                   2420 | True           | True         |
| bag       | end-pass plain24           | True          |           0.841667 |             0 |                    109 | True           | True         |
| bag       | end-pass plain27           | False         |           0.933333 |             0 |                      4 | False          | False        |
| bag       | end-pass erased1 J-lens    | True          |           1        |             6 |                   2568 | True           | True         |
| bag       | end-pass erased0.5 J-lens  | True          |           1        |             6 |                   2519 | True           | True         |
| bag       | end-pass erased1 plain24   | True          |           0.85     |             0 |                    102 | True           | True         |
| bag       | end-pass erased0.5 plain24 | True          |           0.85     |             0 |                    105 | True           | True         |
| bag       | end-pass erased1 plain27   | False         |           0.933333 |             0 |                      4 | False          | False        |
| bag       | end-pass erased0.5 plain27 | False         |           0.933333 |             0 |                      4 | False          | False        |
| mouth     | J-lens                     | False         |           0.95     |             0 |                     15 | False          | False        |
| mouth     | plain lens                 | True          |           0.966667 |             0 |                   1096 | True           | True         |
| mouth     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens                     | True          |           0.88     |             0 |                   5935 | True           | True         |
| soil      | plain lens                 | True          |           0.986667 |             0 |                   4506 | True           | True         |
| soil      | end-pass J-lens            | True          |           0.986667 |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased1 J-lens    | True          |           0.973333 |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 J-lens  | True          |           0.986667 |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| mountain  | J-lens                     | False         |           0.854762 |             1 |                      5 | False          | False        |
| mountain  | plain lens                 | True          |           0.861905 |             1 |                     48 | True           | True         |
| mountain  | end-pass J-lens            | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain24           | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27           | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           1        |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           1        |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| heart     | J-lens                     | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | plain lens                 | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass J-lens            | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | end-pass plain24           | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass plain27           | False         |           0.936508 |             0 |                     10 | False          | False        |
| heart     | end-pass erased1 J-lens    | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | end-pass erased0.5 J-lens  | False         |           0.920635 |             0 |                     10 | False          | False        |
| heart     | end-pass erased1 plain24   | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass erased0.5 plain24 | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass erased1 plain27   | False         |           0.936508 |             0 |                     11 | False          | False        |
| heart     | end-pass erased0.5 plain27 | False         |           0.936508 |             0 |                     11 | False          | False        |
| hand      | J-lens                     | True          |           0.960145 |             0 |                  32305 | True           | True         |
| hand      | plain lens                 | True          |           0.992754 |             0 |                  34571 | True           | True         |
| hand      | end-pass J-lens            | True          |           0.985507 |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain24           | True          |           0.996377 |             0 |             1000000000 | True           | True         |
| hand      | end-pass plain27           | True          |           1        |             2 |             1000000000 | True           | True         |
| hand      | end-pass erased1 J-lens    | True          |           0.985507 |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 J-lens  | True          |           0.985507 |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased1 plain24   | True          |           0.996377 |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 plain24 | True          |           0.996377 |             0 |             1000000000 | True           | True         |
| hand      | end-pass erased1 plain27   | True          |           1        |             2 |             1000000000 | True           | True         |
| hand      | end-pass erased0.5 plain27 | True          |           1        |             2 |             1000000000 | True           | True         |
| star      | J-lens                     | True          |           0.934066 |             1 |                     63 | True           | True         |
| star      | plain lens                 | False         |           0.912088 |             1 |                     26 | False          | False        |
| star      | end-pass J-lens            | True          |           0.934066 |             1 |                     63 | True           | True         |
| star      | end-pass plain24           | False         |           0.912088 |             1 |                     26 | False          | False        |
| star      | end-pass plain27           | False         |           0.934066 |             0 |                     30 | False          | False        |
| star      | end-pass erased1 J-lens    | True          |           0.934066 |             1 |                     68 | True           | True         |
| star      | end-pass erased0.5 J-lens  | True          |           0.934066 |             1 |                     66 | True           | True         |
| star      | end-pass erased1 plain24   | True          |           0.912088 |             1 |                     32 | True           | True         |
| star      | end-pass erased0.5 plain24 | False         |           0.912088 |             1 |                     28 | False          | False        |
| star      | end-pass erased1 plain27   | True          |           0.934066 |             0 |                     33 | True           | True         |
| star      | end-pass erased0.5 plain27 | True          |           0.934066 |             0 |                     32 | True           | True         |
| book      | J-lens                     | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | plain lens                 | False         |           0.808333 |             1 |                     17 | False          | False        |
| book      | end-pass J-lens            | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | end-pass plain24           | False         |           0.808333 |             1 |                     17 | False          | False        |
| book      | end-pass plain27           | False         |           0.866667 |             2 |                     19 | False          | False        |
| book      | end-pass erased1 J-lens    | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | end-pass erased0.5 J-lens  | True          |           0.875    |             1 |                     32 | True           | True         |
| book      | end-pass erased1 plain24   | False         |           0.808333 |             1 |                     17 | False          | False        |
| book      | end-pass erased0.5 plain24 | False         |           0.808333 |             1 |                     18 | False          | False        |
| book      | end-pass erased1 plain27   | False         |           0.866667 |             2 |                     19 | False          | False        |
| book      | end-pass erased0.5 plain27 | False         |           0.866667 |             2 |                     19 | False          | False        |
| cloud     | J-lens                     | False         |           0.888889 |             1 |                     16 | False          | False        |
| cloud     | plain lens                 | False         |           0.911111 |             2 |                      9 | False          | False        |
| cloud     | end-pass J-lens            | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass plain24           | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass plain27           | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 J-lens    | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 J-lens  | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 plain24   | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 plain24 | True          |           1        |             2 |             1000000000 | True           | True         |
| cloud     | end-pass erased1 plain27   | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | end-pass erased0.5 plain27 | True          |           1        |             1 |             1000000000 | True           | True         |
| bag       | J-lens                     | True          |           1        |            20 |                   5527 | True           | True         |
| bag       | plain lens                 | False         |           0.953704 |           622 |                   1578 | False          | False        |
| bag       | end-pass J-lens            | True          |           1        |            20 |                   5517 | True           | True         |
| bag       | end-pass plain24           | False         |           1        |           621 |                   1577 | False          | False        |
| bag       | end-pass plain27           | True          |           1        |            13 |                     51 | True           | True         |
| bag       | end-pass erased1 J-lens    | True          |           1        |            20 |                   5528 | True           | True         |
| bag       | end-pass erased0.5 J-lens  | True          |           1        |            20 |                   5445 | True           | True         |
| bag       | end-pass erased1 plain24   | False         |           1        |           638 |                   1630 | False          | False        |
| bag       | end-pass erased0.5 plain24 | False         |           1        |           628 |                   1595 | False          | False        |
| bag       | end-pass erased1 plain27   | True          |           1        |            13 |                     49 | True           | True         |
| bag       | end-pass erased0.5 plain27 | True          |           1        |            13 |                     49 | True           | True         |
| mouth     | J-lens                     | True          |           0.988095 |             0 |                    517 | True           | True         |
| mouth     | plain lens                 | True          |           0.976191 |             0 |                    270 | True           | True         |
| mouth     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| soil      | J-lens                     | True          |           0.811765 |             1 |                    978 | True           | True         |
| soil      | plain lens                 | True          |           0.882353 |             5 |                    144 | True           | True         |
| soil      | end-pass J-lens            | True          |           0.952941 |             1 |                    969 | True           | True         |
| soil      | end-pass plain24           | True          |           0.988235 |             5 |                    143 | True           | True         |
| soil      | end-pass plain27           | True          |           1        |             8 |                     92 | True           | True         |
| soil      | end-pass erased1 J-lens    | True          |           0.858824 |             1 |                   1003 | True           | True         |
| soil      | end-pass erased0.5 J-lens  | True          |           0.882353 |             1 |                    948 | True           | True         |
| soil      | end-pass erased1 plain24   | True          |           0.976471 |             2 |                     94 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           0.988235 |             3 |                    116 | True           | True         |
| soil      | end-pass erased1 plain27   | True          |           0.988235 |             6 |                     66 | True           | True         |
| soil      | end-pass erased0.5 plain27 | True          |           1        |             7 |                     80 | True           | True         |
| mountain  | J-lens                     | False         |           0.9      |             1 |                     39 | True           | True         |
| mountain  | plain lens                 | False         |           0.852941 |             2 |                      0 | False          | False        |
| mountain  | end-pass J-lens            | True          |           0.976471 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain24           | True          |           0.982353 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass plain27           | True          |           0.988235 |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           0.964706 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           0.976471 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           0.982353 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           0.982353 |             1 |             1000000000 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           0.982353 |             2 |             1000000000 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           0.982353 |             2 |             1000000000 | True           | True         |
| heart     | J-lens                     | False         |           0.837607 |             0 |                     10 | False          | False        |
| heart     | plain lens                 | False         |           0.82906  |             0 |                      8 | False          | False        |
| heart     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens                     | False         |           0.642012 |             1 |                     16 | False          | False        |
| star      | plain lens                 | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass J-lens            | False         |           0.642012 |             1 |                     16 | False          | False        |
| star      | end-pass plain24           | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass plain27           | False         |           0.64497  |             0 |                     15 | False          | False        |
| star      | end-pass erased1 J-lens    | False         |           0.642012 |             1 |                     17 | False          | False        |
| star      | end-pass erased0.5 J-lens  | False         |           0.642012 |             1 |                     17 | False          | False        |
| star      | end-pass erased1 plain24   | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass erased0.5 plain24 | False         |           0.615385 |             1 |                     20 | False          | False        |
| star      | end-pass erased1 plain27   | False         |           0.64497  |             0 |                     16 | False          | False        |
| star      | end-pass erased0.5 plain27 | False         |           0.64497  |             0 |                     16 | False          | False        |
| book      | J-lens                     | True          |           0.925    |             2 |                    106 | True           | True         |
| book      | plain lens                 | True          |           0.9      |             1 |                    390 | True           | True         |
| book      | end-pass J-lens            | True          |           1        |             2 |             1000000000 | True           | True         |
| book      | end-pass plain24           | True          |           0.99375  |             1 |             1000000000 | True           | True         |
| book      | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| book      | end-pass erased1 J-lens    | True          |           1        |             2 |             1000000000 | True           | True         |
| book      | end-pass erased0.5 J-lens  | True          |           1        |             2 |             1000000000 | True           | True         |
| book      | end-pass erased1 plain24   | True          |           0.9875   |             2 |             1000000000 | True           | True         |
| book      | end-pass erased0.5 plain24 | True          |           0.9875   |             1 |             1000000000 | True           | True         |
| book      | end-pass erased1 plain27   | True          |           1        |             1 |             1000000000 | True           | True         |
| book      | end-pass erased0.5 plain27 | True          |           1        |             1 |             1000000000 | True           | True         |
| cloud     | J-lens                     | True          |           0.864198 |             0 |                    119 | True           | True         |
| cloud     | plain lens                 | True          |           0.851852 |             1 |                     58 | True           | True         |
| cloud     | end-pass J-lens            | True          |           0.864198 |             0 |                    119 | True           | True         |
| cloud     | end-pass plain24           | True          |           0.851852 |             1 |                     58 | True           | True         |
| cloud     | end-pass plain27           | True          |           0.864198 |             1 |                     47 | True           | True         |
| cloud     | end-pass erased1 J-lens    | True          |           0.864198 |             0 |                    128 | True           | True         |
| cloud     | end-pass erased0.5 J-lens  | True          |           0.864198 |             0 |                    123 | True           | True         |
| cloud     | end-pass erased1 plain24   | True          |           0.851852 |             1 |                     60 | True           | True         |
| cloud     | end-pass erased0.5 plain24 | True          |           0.851852 |             1 |                     59 | True           | True         |
| cloud     | end-pass erased1 plain27   | True          |           0.864198 |             1 |                     50 | True           | True         |
| cloud     | end-pass erased0.5 plain27 | True          |           0.864198 |             1 |                     49 | True           | True         |
| bag       | J-lens                     | False         |           0.931818 |            10 |                     21 | False          | False        |
| bag       | plain lens                 | True          |           0.878788 |             1 |                     83 | True           | True         |
| bag       | end-pass J-lens            | False         |           0.931818 |            10 |                     21 | False          | False        |
| bag       | end-pass plain24           | True          |           0.878788 |             1 |                     83 | True           | True         |
| bag       | end-pass plain27           | False         |           0.984848 |             0 |                     18 | False          | False        |
| bag       | end-pass erased1 J-lens    | False         |           0.924242 |            12 |                     19 | False          | False        |
| bag       | end-pass erased0.5 J-lens  | False         |           0.924242 |            11 |                     19 | False          | False        |
| bag       | end-pass erased1 plain24   | True          |           0.909091 |             1 |                     57 | True           | True         |
| bag       | end-pass erased0.5 plain24 | True          |           0.901515 |             1 |                     66 | True           | True         |
| bag       | end-pass erased1 plain27   | False         |           0.969697 |             0 |                     20 | False          | False        |
| bag       | end-pass erased0.5 plain27 | False         |           0.969697 |             0 |                     20 | False          | False        |
| mouth     | J-lens                     | True          |           0.974359 |             0 |                   1077 | True           | True         |
| mouth     | plain lens                 | True          |           0.961538 |             0 |                   1498 | True           | True         |
| mouth     | end-pass J-lens            | True          |           0.974359 |             0 |                   1077 | True           | True         |
| mouth     | end-pass plain24           | True          |           0.961538 |             0 |                   1498 | True           | True         |
| mouth     | end-pass plain27           | True          |           0.935897 |             0 |                     45 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           0.974359 |             0 |                   1356 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           0.974359 |             0 |                   1221 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           0.961538 |             0 |                   1412 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           0.961538 |             0 |                   1458 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           0.935897 |             0 |                     47 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           0.935897 |             0 |                     45 | True           | True         |
| soil      | J-lens                     | False         |           0.8      |             1 |                     21 | False          | False        |
| soil      | plain lens                 | True          |           0.854545 |             0 |                    123 | True           | True         |
| soil      | end-pass J-lens            | False         |           0.8      |             1 |                     21 | False          | False        |
| soil      | end-pass plain24           | True          |           0.854545 |             0 |                    123 | True           | True         |
| soil      | end-pass plain27           | False         |           0.927273 |             0 |                     15 | False          | False        |
| soil      | end-pass erased1 J-lens    | False         |           0.8      |             1 |                     22 | False          | False        |
| soil      | end-pass erased0.5 J-lens  | False         |           0.8      |             1 |                     23 | False          | False        |
| soil      | end-pass erased1 plain24   | True          |           0.854545 |             0 |                    103 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           0.854545 |             0 |                    110 | True           | True         |
| soil      | end-pass erased1 plain27   | False         |           0.927273 |             0 |                     15 | False          | False        |
| soil      | end-pass erased0.5 plain27 | False         |           0.927273 |             0 |                     15 | False          | False        |
| mountain  | J-lens                     | True          |           0.873333 |             2 |                     47 | True           | True         |
| mountain  | plain lens                 | True          |           0.913333 |             2 |                    453 | True           | True         |
| mountain  | end-pass J-lens            | True          |           0.873333 |             2 |                     47 | True           | True         |
| mountain  | end-pass plain24           | True          |           0.913333 |             2 |                    453 | True           | True         |
| mountain  | end-pass plain27           | True          |           0.906667 |             2 |                     71 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           0.873333 |             2 |                     60 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           0.873333 |             2 |                     59 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           0.92     |             2 |                    431 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           0.92     |             2 |                    449 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           0.906667 |             2 |                     87 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           0.906667 |             2 |                     76 | True           | True         |
| heart     | J-lens                     | False         |           0.849206 |             0 |                     17 | False          | False        |
| heart     | plain lens                 | True          |           0.896825 |             0 |                     40 | True           | True         |
| heart     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens                     | True          |           0.611336 |             2 |                    100 | True           | True         |
| star      | plain lens                 | True          |           0.603239 |             1 |                     55 | True           | True         |
| star      | end-pass J-lens            | True          |           0.611336 |             2 |                    100 | True           | True         |
| star      | end-pass plain24           | True          |           0.603239 |             1 |                     55 | True           | True         |
| star      | end-pass plain27           | True          |           0.611336 |             0 |                     54 | True           | True         |
| star      | end-pass erased1 J-lens    | True          |           0.611336 |             2 |                    101 | True           | True         |
| star      | end-pass erased0.5 J-lens  | True          |           0.611336 |             2 |                    100 | True           | True         |
| star      | end-pass erased1 plain24   | True          |           0.603239 |             1 |                     53 | True           | True         |
| star      | end-pass erased0.5 plain24 | True          |           0.603239 |             1 |                     53 | True           | True         |
| star      | end-pass erased1 plain27   | True          |           0.611336 |             0 |                     54 | True           | True         |
| star      | end-pass erased0.5 plain27 | True          |           0.611336 |             0 |                     54 | True           | True         |
| cloud     | J-lens                     | True          |           0.921569 |             1 |                    101 | True           | True         |
| cloud     | plain lens                 | True          |           0.921569 |             2 |                     53 | True           | True         |
| cloud     | end-pass J-lens            | True          |           0.921569 |             1 |                    101 | True           | True         |
| cloud     | end-pass plain24           | True          |           0.921569 |             2 |                     53 | True           | True         |
| cloud     | end-pass plain27           | True          |           0.921569 |             1 |                     48 | True           | True         |
| cloud     | end-pass erased1 J-lens    | True          |           0.921569 |             1 |                    103 | True           | True         |
| cloud     | end-pass erased0.5 J-lens  | True          |           0.921569 |             1 |                    102 | True           | True         |
| cloud     | end-pass erased1 plain24   | True          |           0.921569 |             2 |                     49 | True           | True         |
| cloud     | end-pass erased0.5 plain24 | True          |           0.921569 |             2 |                     49 | True           | True         |
| cloud     | end-pass erased1 plain27   | True          |           0.921569 |             1 |                     48 | True           | True         |
| cloud     | end-pass erased0.5 plain27 | True          |           0.921569 |             1 |                     48 | True           | True         |
| bag       | J-lens                     | False         |           0.95614  |             6 |                     21 | False          | False        |
| bag       | plain lens                 | True          |           0.925439 |             4 |                     48 | True           | True         |
| bag       | end-pass J-lens            | False         |           0.95614  |             6 |                     21 | False          | False        |
| bag       | end-pass plain24           | True          |           0.925439 |             4 |                     48 | True           | True         |
| bag       | end-pass plain27           | False         |           0.991228 |             0 |                     31 | False          | False        |
| bag       | end-pass erased1 J-lens    | False         |           0.95614  |             8 |                     20 | False          | False        |
| bag       | end-pass erased0.5 J-lens  | False         |           0.95614  |             7 |                     20 | False          | False        |
| bag       | end-pass erased1 plain24   | True          |           0.934211 |             3 |                     40 | True           | True         |
| bag       | end-pass erased0.5 plain24 | True          |           0.929825 |             4 |                     43 | True           | True         |
| bag       | end-pass erased1 plain27   | True          |           0.991228 |             0 |                     35 | True           | True         |
| bag       | end-pass erased0.5 plain27 | True          |           0.991228 |             0 |                     34 | True           | True         |
| mouth     | J-lens                     | True          |           0.992064 |             0 |                    256 | True           | True         |
| mouth     | plain lens                 | True          |           0.976191 |             0 |                    441 | True           | True         |
| mouth     | end-pass J-lens            | True          |           0.992064 |             0 |                    256 | True           | True         |
| mouth     | end-pass plain24           | True          |           0.976191 |             0 |                    441 | True           | True         |
| mouth     | end-pass plain27           | True          |           0.960317 |             0 |                     41 | True           | True         |
| mouth     | end-pass erased1 J-lens    | True          |           0.984127 |             0 |                    324 | True           | True         |
| mouth     | end-pass erased0.5 J-lens  | True          |           0.992064 |             0 |                    288 | True           | True         |
| mouth     | end-pass erased1 plain24   | True          |           0.976191 |             0 |                    438 | True           | True         |
| mouth     | end-pass erased0.5 plain24 | True          |           0.976191 |             0 |                    440 | True           | True         |
| mouth     | end-pass erased1 plain27   | True          |           0.960317 |             0 |                     41 | True           | True         |
| mouth     | end-pass erased0.5 plain27 | True          |           0.960317 |             0 |                     41 | True           | True         |
| soil      | J-lens                     | True          |           0.873684 |             0 |                     32 | True           | True         |
| soil      | plain lens                 | True          |           0.894737 |             0 |                    267 | True           | True         |
| soil      | end-pass J-lens            | True          |           0.873684 |             0 |                     32 | True           | True         |
| soil      | end-pass plain24           | True          |           0.894737 |             0 |                    267 | True           | True         |
| soil      | end-pass plain27           | False         |           0.884211 |             8 |                     16 | False          | False        |
| soil      | end-pass erased1 J-lens    | True          |           0.873684 |             0 |                     35 | True           | True         |
| soil      | end-pass erased0.5 J-lens  | True          |           0.873684 |             0 |                     33 | True           | True         |
| soil      | end-pass erased1 plain24   | True          |           0.894737 |             0 |                    218 | True           | True         |
| soil      | end-pass erased0.5 plain24 | True          |           0.894737 |             0 |                    236 | True           | True         |
| soil      | end-pass erased1 plain27   | False         |           0.884211 |             8 |                     16 | False          | False        |
| soil      | end-pass erased0.5 plain27 | False         |           0.884211 |             8 |                     16 | False          | False        |
| mountain  | J-lens                     | True          |           0.947826 |             1 |                     33 | True           | True         |
| mountain  | plain lens                 | True          |           0.956522 |             1 |                    334 | True           | True         |
| mountain  | end-pass J-lens            | True          |           0.947826 |             1 |                     33 | True           | True         |
| mountain  | end-pass plain24           | True          |           0.956522 |             1 |                    334 | True           | True         |
| mountain  | end-pass plain27           | True          |           0.945652 |             2 |                     62 | True           | True         |
| mountain  | end-pass erased1 J-lens    | True          |           0.956522 |             1 |                     38 | True           | True         |
| mountain  | end-pass erased0.5 J-lens  | True          |           0.954348 |             1 |                     36 | True           | True         |
| mountain  | end-pass erased1 plain24   | True          |           0.956522 |             1 |                    263 | True           | True         |
| mountain  | end-pass erased0.5 plain24 | True          |           0.956522 |             1 |                    295 | True           | True         |
| mountain  | end-pass erased1 plain27   | True          |           0.952174 |             2 |                     67 | True           | True         |
| mountain  | end-pass erased0.5 plain27 | True          |           0.947826 |             2 |                     67 | True           | True         |
| heart     | J-lens                     | False         |           0.90404  |             0 |                     18 | False          | False        |
| heart     | plain lens                 | True          |           0.964646 |             0 |                     53 | True           | True         |
| heart     | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| heart     | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | J-lens                     | True          |           1        |             0 |                  14959 | True           | True         |
| day       | plain lens                 | True          |           1        |             0 |                  60463 | True           | True         |
| day       | end-pass J-lens            | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain24           | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass plain27           | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 J-lens    | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 J-lens  | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 plain24   | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 plain24 | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased1 plain27   | True          |           1        |             0 |             1000000000 | True           | True         |
| day       | end-pass erased0.5 plain27 | True          |           1        |             0 |             1000000000 | True           | True         |
| star      | J-lens                     | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | plain lens                 | True          |           0.960114 |             1 |                     63 | True           | True         |
| star      | end-pass J-lens            | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | end-pass plain24           | True          |           0.960114 |             1 |                     63 | True           | True         |
| star      | end-pass plain27           | True          |           0.900285 |             0 |                     54 | True           | True         |
| star      | end-pass erased1 J-lens    | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | end-pass erased0.5 J-lens  | True          |           0.980057 |             1 |                     95 | True           | True         |
| star      | end-pass erased1 plain24   | True          |           0.951567 |             1 |                     56 | True           | True         |
| star      | end-pass erased0.5 plain24 | True          |           0.957265 |             1 |                     62 | True           | True         |
| star      | end-pass erased1 plain27   | True          |           0.900285 |             0 |                     54 | True           | True         |
| star      | end-pass erased0.5 plain27 | True          |           0.900285 |             0 |                     54 | True           | True         |

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

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased1 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云', '云的', '的云', ' cloudy', ' обла', '云彩', '云雾', '.Cloud', '云端', '云服务', '云中', '云海', ' mây', '云计算', '云平台', ' fog', ' 클라우드', ' sky', ' skies', 'クラウド']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased0.5 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云', '云的', '的云', ' cloudy', ' обла', '云彩', '云雾', '.Cloud', '云端', '云服务', '云中', '云海', ' mây', '云计算', '云平台', ' 클라우드', ' fog', ' sky', 'クラウド', ' skies']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased1 plain24: [' clouds', ' cloud', '云', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云层', '云彩', ' обла', '云的', '/cloud', '雲', '云计算', '云朵', '.cloud', '的云', ' cloudy', '云端', 'クラウド', ' 클라우드', '云中', '云服务', '.Cloud', '天空', '云雾', '云平台', '云上', ' mây', '多云', '云飞']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased0.5 plain24: [' clouds', ' cloud', '云', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云层', '云彩', ' обла', '云的', '/cloud', '雲', '云计算', '云朵', '.cloud', '的云', ' cloudy', '云端', 'クラウド', ' 클라우드', '云中', '云服务', '.Cloud', '天空', '云雾', '云平台', '云上', ' mây', '多云', '云飞']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased1 plain27: [' cloud', '云', 'cloud', ' clouds', ' Cloud', 'Cloud', '雲', '-cloud', '云的', '_cloud', '云彩', '的云', '云层', '云朵', '/cloud', ' обла', '.cloud', '云计算', '云端', ' cloudy', '云雾', '云中', '.Cloud', 'クラウド', ' 클라우드', '云上', '云服务', '云飞', '云平台', '云天', ' mây', '雲端']

Input: 'Deutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "'

Baseline: 'nuage"\nDeutsch: "K'

end-pass erased0.5 plain27: [' cloud', '云', 'cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云彩', '的云', '云层', '云朵', ' обла', '/cloud', '.cloud', '云计算', '云端', ' cloudy', '云雾', '云中', '.Cloud', 'クラウド', ' 클라우드', '云上', '云服务', '云飞', '云平台', '云天', ' mây', '雲端']

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

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased1 J-lens: [' purse', ' pouch', ' pocket', '钱包', ' pockets', ' wallet', '口袋', ' suitcase', ' bags', '-pocket', ' luggage', ' bag', '口袋里', ' tote', 'bags', 'bag', ' wallets', ' bracelet', ' trousers', 'wallet', 'Bags', ' Taschen', ' backpack', '书包', ' baggage', '袋子', ' basket', ' holster', 'กระเป๋า', ' Bags', 'Pocket', ' Wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased0.5 J-lens: [' purse', ' pouch', ' pocket', '钱包', ' pockets', ' wallet', '口袋', ' suitcase', ' bags', '-pocket', ' bag', ' luggage', '口袋里', ' tote', 'bag', 'bags', ' wallets', ' bracelet', ' trousers', 'wallet', ' backpack', 'Bags', ' Taschen', ' baggage', '书包', '袋子', ' basket', ' holster', 'กระเป๋า', ' Bags', 'Pocket', ' Wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased1 plain24: ['加拿大', '提', ' tut', ' bag', ' purse', ' spanish', ' recept', ' tart', ' fond', ' poc', '随身携带', 'zac', '新加坡', '钱包', 'implements', 'Pocket', ' pocket', '口袋', '战术', ' aficion', ' videoc', 'urses', ' magazin', 'achable', '之谜', ' té', ' pockets', 'ré', ' apro', ' Taschen', ' tote', 'naissance']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased0.5 plain24: ['加拿大', '提', ' tut', ' bag', ' purse', ' spanish', ' recept', ' tart', ' poc', ' fond', '随身携带', 'zac', '新加坡', '钱包', 'implements', 'Pocket', ' pocket', '口袋', '战术', ' aficion', ' videoc', 'urses', ' magazin', 'achable', '之谜', ' té', 'ré', ' pockets', ' Taschen', ' apro', 'naissance', 'wallet']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased1 plain27: [' bag', '口袋', ' pocket', ' pockets', ' wallet', '袋', 'bag', 'Pocket', ' bags', 'Wallet', ' purse', '钱包', ' bols', 'Bag', ' wallets', '囊', ' sac', 'wallet', ' Pocket', ' Wallet', ' túi', ' Bag', 'bags', '-pocket', ' pouch', 'กระเป๋า', '_wallet', ' Bags', '袋子', ' BAG', ' poch', '_bag']

Input: 'Deutsch: "Tee" - Français: "thé"\nDeutsch: "Börse" - Français: "bourse"\nDeutsch: "Maschine" - Français: "machine"\nDeutsch: "Straße" - Français: "rue"\nDeutsch: "Tasche" - Français: "'

Baseline: 'sac"\nDeutsch: "K'

end-pass erased0.5 plain27: [' bag', '口袋', ' pocket', ' pockets', ' wallet', '袋', 'bag', 'Pocket', ' bags', 'Wallet', ' purse', '钱包', ' bols', 'Bag', ' wallets', 'wallet', ' sac', '囊', ' Pocket', ' Wallet', ' túi', ' Bag', 'bags', '-pocket', ' pouch', 'กระเป๋า', '_wallet', ' Bags', '袋子', ' BAG', ' poch', '_bag']

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

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased1 J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' lips', ' boca', ' palate', ' jaw', ' saliva', '嘴', ' mulut', ' throat', '口', ' bocca', '嘴唇', ' teeth', ' oral', ' jaws', ' miệng', ' tongues', ' doorway', ' vagina', '口语', 'lips', ' penis', '口中', '舌头', '口的']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased0.5 J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' boca', ' lips', ' palate', ' saliva', ' jaw', '嘴', ' mulut', ' bocca', ' throat', '口', '嘴唇', ' miệng', ' teeth', ' jaws', ' tongues', ' oral', ' doorway', ' vagina', 'lips', '口语', ' mou', '口中', '舌头', ' penis']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased1 plain24: [' mouth', 'mouth', '口腔', '口', ' Mouth', ' mouths', ' oral', '嘴巴', ' mou', '-mouth', '的口', '嘴', '口语', '口的', ' bocca', ' saliva', '口中', '口红', '口干', '口头', '口区', ' pron', ' cunt', 'emouth', '嘴唇', ' lips', '出口', '聘', ' fond', '加拿大', ' orally', ' mond']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased0.5 plain24: [' mouth', 'mouth', '口腔', '口', ' Mouth', ' mouths', ' oral', '嘴巴', ' mou', '-mouth', '的口', '嘴', '口语', ' bocca', '口的', ' saliva', '口中', '口红', '口干', '口区', '口头', 'emouth', ' cunt', ' pron', '嘴唇', '加拿大', ' lips', '聘', '出口', ' mond', ' orally', ' fond']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased1 plain27: [' mouth', '口', 'mouth', '嘴', '口的', ' Mouth', ' mouths', '嘴巴', '口腔', '-mouth', ' oral', '的口', ' boca', '口中', ' bocca', '开口', ' miệng', ' lips', ' Oral', '口中的', 'ปาก', '口の', '口头', ' mulut', '嘴唇', '唇', '口红', '嘴里', '口镇', '张口', 'emouth', '人口']

Input: 'Deutsch: "Haushalt" - Français: "ménage"\nDeutsch: "Macht" - Français: "pouvoir"\nDeutsch: "Pferd" - Français: "cheval"\nDeutsch: "Norden" - Français: "nord"\nDeutsch: "Mund" - Français: "'

Baseline: 'bouche"\nDeutsch: "K'

end-pass erased0.5 plain27: [' mouth', '口', 'mouth', '嘴', ' Mouth', '口的', ' mouths', '嘴巴', '口腔', '-mouth', ' oral', '的口', ' boca', '口中', ' bocca', '开口', ' miệng', ' lips', ' Oral', '口の', '口中的', 'ปาก', ' mulut', '口头', '嘴唇', '唇', '口红', '嘴里', 'emouth', '口镇', '张嘴', '张口']

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

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased1 J-lens: [' soil', ' terrain', ' ground', '土壤', 'ground', ' earth', ' tierra', ' tanah', ' terra', ' Terrain', '土地', '地面', ' soils', ' land', '大地', ' terreno', ' floor', ' Soil', ' terre', '的土地', 'Ground', 'terrain', ' suelo', ' Ground', 'earth', 'floor', '-ground', '地板', '的地', '地基', '土壤中', ' dirt']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased0.5 J-lens: [' soil', ' terrain', ' ground', '土壤', 'ground', ' earth', ' tierra', ' tanah', ' Terrain', ' terra', ' soils', '地面', '土地', ' Soil', ' land', '大地', ' terreno', ' terre', '的土地', ' floor', 'Ground', 'terrain', ' suelo', ' Ground', 'earth', 'floor', '土壤中', '-ground', '地基', '地板', '泥土', '的地']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased1 plain24: [' soil', ' terrain', ' ground', '地面', '土地', 'ground', ' أرض', '地基', ' tanah', '土壤', '大地', ' land', '脚下的', '底层', 'Ground', ' tierra', '土', ' terra', '地表', '的地', ' đất', ' soils', ' terre', ' Ground', '地面的', 'terrain', ' الأرض', ' earth', 'loor', ' terrestrial', ' floor', '_ground']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased0.5 plain24: [' soil', ' terrain', ' ground', '地面', '土地', 'ground', ' أرض', '地基', ' tanah', '土壤', '大地', '脚下的', 'Ground', ' land', '底层', ' tierra', '土', '地表', ' soils', ' đất', ' terra', '的地', ' terre', ' Ground', '地面的', 'terrain', 'loor', ' Soil', ' الأرض', ' earth', ' terrestrial', '_ground']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased1 plain27: [' ground', 'ground', ' soil', '地面', ' Ground', 'Ground', '土壤', '土地', ' tanah', ' terre', ' floor', ' Soil', ' earth', ' terrain', '_ground', ' suelo', '地面的', ' đất', ' land', ' soils', '地', ' terra', '地板', '地面上', ' grounds', '-ground', 'ดิน', '的地', ' tierra', 'floor', '土', '接地']

Input: 'Deutsch: "sieben" - Français: "sept"\nDeutsch: "Brücke" - Français: "pont"\nDeutsch: "Bahnhof" - Français: "gare"\nDeutsch: "Provinz" - Français: "province"\nDeutsch: "Boden" - Français: "'

Baseline: 'sol"\nDeutsch: "Berg'

end-pass erased0.5 plain27: [' ground', 'ground', ' soil', '地面', ' Ground', 'Ground', '土壤', '土地', ' tanah', ' terre', ' Soil', ' floor', '_ground', ' suelo', ' earth', ' terrain', '地面的', ' đất', ' land', ' soils', '地', ' terra', '地板', ' grounds', '地面上', '-ground', 'ดิน', '的地', ' tierra', '土', 'floor', '地基']

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

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased1 J-lens: [' mountains', ' mountain', ' Mountains', ' hills', '山峰', '山脉', 'Mountain', ' Mountain', 'mount', ' hill', ' terrain', '山地', ' volcano', ' gunung', ' Alps', '山区', ' cliffs', ' massif', ' горы', ' glacier', 'Mount', '山体', '的山', ' valley', ' mount', ' wilderness', ' countryside', ' canyon', '登山', 'landscape', ' landscape', ' summit']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased0.5 J-lens: [' mountains', ' mountain', ' Mountains', ' hills', 'mount', '山峰', 'Mountain', '山脉', ' Mountain', ' hill', '山地', ' gunung', ' terrain', ' volcano', ' Alps', '山区', 'Mount', ' горы', ' massif', ' cliffs', '山体', '的山', ' mount', ' glacier', '山的', '登山', ' núi', ' countryside', ' wilderness', '山顶', ' canyon', ' valley']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased1 plain24: [' mountains', ' mountain', ' гор', ' Mountains', '山峰', '加拿大', '山脉', 'alic', 'mount', '阿拉伯', '_MOUNT', 'ugged', ' penal', '依山', 'bestos', 'Mount', ' fond', ' Mountain', '卖点', ' terrain', ' hill', 'peater', 'imestone', '兢兢业业', '岗', 'Mountain', ' geological', ' inland', '脊梁', '山之', ' plateau', '境内的']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased0.5 plain24: [' mountains', ' mountain', ' гор', ' Mountains', '山峰', '加拿大', '山脉', 'mount', 'alic', '_MOUNT', '阿拉伯', 'Mount', 'ugged', '依山', ' Mountain', ' penal', 'bestos', ' fond', '卖点', 'Mountain', ' terrain', ' hill', '兢兢业业', 'peater', '山之', 'imestone', '岗', ' inland', ' geological', '脊梁', '靠山', ' plateau']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', '山峰', '峰', ' hill', ' Mountain', ' fond', ' гор', ' Peak', 'Mountain', 'Peak', 'Mount', ' peak', '山脉', ' hills', 'mount', '山之', '加拿大', ' peaks', 'peak', 'ountains', ' plateau', ' dés', ' volcano', '山的', ' terrain', ' Mount', ' dãy', ' altitude', ' pe', ' pir']

Input: 'Deutsch: "Gesetz" - Français: "loi"\nDeutsch: "Tür" - Français: "porte"\nDeutsch: "Osten" - Français: "est"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Berg" - Français: "'

Baseline: 'montagne"\nDeutsch: "Fl'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', '山峰', ' Mountain', '峰', 'Mountain', ' гор', ' hill', 'mount', 'Mount', ' fond', ' Peak', 'Peak', '山脉', '山之', ' peak', ' hills', '加拿大', ' Mount', '山的', 'ountains', 'peak', ' peaks', ' горы', 'ภูเขา', ' mount', ' plateau', ' dãy', '的山', ' volcano', ' dés']

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

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased1 J-lens: [' heart', ' hearts', 'heart', '-heart', ' Heart', '心脏', 'Heart', ' corazón', '心臟', '的心脏', ' coração', ' heartbeat', ' cœur', ' Herzen', ' cuore', ' cardiac', ' Hearts', ' сердце', ' сердца', ' قلب', ' coeur', ' серд', '心跳', 'heartbeat', '心肺', ' cardi', ' cardia', ' heartfelt', ' القلب', ' jantung', '-hearted', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased0.5 J-lens: [' heart', ' hearts', 'heart', '-heart', ' Heart', '心脏', 'Heart', ' corazón', '心臟', '的心脏', ' coração', ' heartbeat', ' cœur', ' cuore', ' Herzen', ' cardiac', ' Hearts', ' сердце', ' сердца', ' قلب', ' coeur', '心跳', ' серд', 'heartbeat', ' cardi', '心肺', ' cardia', ' heartfelt', ' القلب', ' jantung', ' καρ', '-hearted']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased1 plain24: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '心脏', '的心脏', ' corazón', ' серд', '心', '-heart', ' قلب', ' сердца', ' cœur', '心臟', '心的', ' القلب', '的心', ' сердце', ' Herzen', ' cuore', ' Hearts', '心脏病', ' heartbeat', 'heartbeat', '之心', ' cardiac', '心率', '心跳', 'قلب', ' coração', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased0.5 plain24: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '心脏', '的心脏', ' corazón', ' серд', '心', '-heart', ' قلب', ' сердца', ' cœur', '心臟', '心的', ' القلب', '的心', ' сердце', ' Herzen', ' cuore', ' Hearts', '心脏病', ' heartbeat', 'heartbeat', ' cardiac', '之心', '心率', '心跳', 'قلب', ' coração', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased1 plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心', ' قلب', ' corazón', '的心', ' cœur', '心的', '的心脏', ' сердца', ' серд', ' coração', ' القلب', ' сердце', ' heartbeat', ' cardiac', ' Hearts', 'หัวใจ', '心跳', '-hearted', 'heartbeat', '心臟', ' cuore', '心和', '心脏病', 'قلب', ' καρ']

Input: 'Deutsch: "Plattform" - Français: "plate-forme"\nDeutsch: "Abschnitt" - Français: "section"\nDeutsch: "Blume" - Français: "fleur"\nDeutsch: "Art" - Français: "genre"\nDeutsch: "Herz" - Français: "'

Baseline: 'cœur"\nDeutsch: "K'

end-pass erased0.5 plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心', ' corazón', '的心', ' قلب', ' cœur', '心的', '的心脏', ' сердца', ' серд', ' coração', ' heartbeat', ' сердце', ' القلب', ' cardiac', 'หัวใจ', ' Hearts', '心跳', '-hearted', 'heartbeat', '心臟', ' cuore', '心和', '心脏病', 'قلب', ' cardi']

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

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased1 J-lens: [' day', ' daytime', 'day', ' daylight', ' days', 'Day', 'days', ' Day', ' morning', '_day', '/day', '-day', 'Days', '白天', ' Days', '(day', ' afternoon', ' день', '.day', ' weekday', ' día', '_days', ' DAY', '天数', ' Tages', ' evening', ' días', ' sunrise', '-days', ' Tage', ' дня', ' mornings']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased0.5 J-lens: [' day', 'day', ' daytime', ' daylight', ' days', 'Day', 'days', ' Day', ' morning', '_day', '/day', '-day', 'Days', '(day', ' Days', '白天', '.day', ' día', ' DAY', ' afternoon', ' день', '_days', ' weekday', '天数', ' días', ' Tages', '-days', ' evening', ' Tage', '的一天', ' дня', 'DAY']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased1 plain24: ['day', ' day', '加拿大', ' daylight', ' daytime', ' sun', ' days', '太阳', 'Day', '天空', ' дня', ' النهار', ' té', '阿拉伯', ' vig', ' ημέ', '-day', '天的', '晴朗', '白天', '日', ' parad', ' lent', '(day', '_days', '�', '日历', ' día', ' DAYS', ' sunny', ' solar', 'Days']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased0.5 plain24: ['day', ' day', '加拿大', ' daylight', ' daytime', ' sun', ' days', '太阳', 'Day', ' дня', '天空', ' النهار', '阿拉伯', ' té', ' ημέ', ' vig', '-day', '(day', '天的', '晴朗', '_days', '白天', '日', ' parad', ' lent', ' día', ' DAYS', '日历', '一天的', '姆斯', 'Days', 'ré']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased1 plain27: [' day', 'day', 'Day', ' Day', '-day', ' days', '_day', '日', ' дня', ' день', ' día', ' DAY', '日的', '.day', '一天', ' daylight', '(day', ' ngày', 'Days', '这一天', '\tday', ' روز', '的一天', ' daytime', '天的', '_days', ' giorno', '/day', '一天的', ' Days', ' dag', '-Day']

Input: 'Deutsch: "eins" - Français: "un"\nDeutsch: "Wald" - Français: "forêt"\nDeutsch: "Niederlage" - Français: "défaite"\nDeutsch: "Mond" - Français: "lune"\nDeutsch: "Tag" - Français: "'

Baseline: 'jour"\nDeutsch: "Kaff'

end-pass erased0.5 plain27: [' day', 'day', 'Day', '-day', ' Day', ' days', '_day', ' дня', '日', ' день', ' día', ' DAY', '.day', '日的', '(day', '\tday', '一天', 'Days', ' ngày', ' daylight', '的一天', '这一天', ' روز', ' giorno', '_days', ' daytime', '天的', '/day', '一天的', '-Day', ' Days', ' dag']

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

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased1 J-lens: [' stars', ' star', ' Stars', 'stars', 'Stars', 'star', '-stars', '-star', '/star', ' Star', '星星', '星辰', '之星', '星', ' estrella', 'Star', '星的', ' aster', ' estrellas', ' étoiles', '_star', ' звезды', '颗星', '星标', ' estrelas', ' звезда', ' estrel', '星光', '.star', '-Star', '恒星', ' stella']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased0.5 J-lens: [' stars', ' star', ' Stars', 'stars', 'Stars', 'star', '-stars', '-star', '/star', ' Star', '星星', '星辰', '星', '之星', 'Star', ' estrella', '星的', ' aster', '_star', ' étoiles', ' estrellas', ' звезды', '颗星', '星标', ' estrelas', ' звезда', ' estrel', '星光', '恒星', '.star', '-Star', ' STAR']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased1 plain24: [' stars', ' star', '星', ' Stars', '星的', 'stars', ' aster', '.star', ' Star', 'Stars', '-stars', '星辰', '_star', ' Sternen', 'Star', '之星', '-star', '星座', ' starred', 'star', '颗星', ' stellar', '恒星', ' звезды', ' Astroph', ' estrellas', '星标', '星级', ' estrelas', ' 별', ' звезд', ' celestial']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased0.5 plain24: [' stars', ' star', '星', ' Stars', '星的', 'stars', ' aster', '.star', ' Star', 'Stars', '-stars', '星辰', '_star', 'Star', ' Sternen', '之星', 'star', ' starred', '星座', '-star', '颗星', ' stellar', '恒星', ' звезды', ' estrellas', ' Astroph', '星级', ' celestial', '星标', ' 별', ' звезд', ' estrelas']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased1 plain27: [' star', ' stars', '星', '星的', ' Star', ' Stars', 'Star', 'star', 'stars', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' aster', '之星', ' STAR', ' bintang', '恒星', ' звезды', '/star', ' starred', '明星', ' stellar', ' звезд', 'STAR', '颗星', ' estrellas', ' звезда', '星辰']

Input: 'Deutsch: "Tugend" - Français: "vertu"\nDeutsch: "vier" - Français: "quatre"\nDeutsch: "tausend" - Français: "mille"\nDeutsch: "Krawatte" - Français: "cravate"\nDeutsch: "Stern" - Français: "'

Baseline: 'étoile"\nDeutsch: "K'

end-pass erased0.5 plain27: [' star', ' stars', '星', '星的', ' Star', ' Stars', 'Star', 'star', 'stars', '-star', 'Stars', '_star', '星星', '.star', '-stars', ' aster', '-Star', '之星', ' STAR', ' bintang', '恒星', ' starred', ' звезды', '/star', '明星', ' stellar', 'STAR', ' звезд', '颗星', ' estrellas', '星光', '星辰']

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

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased1 J-lens: [' clouds', ' cloud', 'cloud', '-cloud', 'Cloud', ' Cloud', '/cloud', '.cloud', '云层', '_cloud', '雲', ' nube', '云朵', ' cloudy', '云', '的云', '云的', '云雾', '.Cloud', '云服务', '云彩', ' fog', '云海', ' sky', '云计算', '云端', ' mây', '云平台', ' skies', '云中', '浮云', '乌云']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased0.5 J-lens: [' clouds', ' cloud', 'cloud', '-cloud', 'Cloud', ' Cloud', '/cloud', '.cloud', '云层', '_cloud', '雲', ' nube', '云朵', ' cloudy', '云', '的云', '云的', '云雾', '.Cloud', '云服务', '云彩', ' fog', '云海', ' sky', '云计算', '云端', ' mây', '云平台', ' skies', '云中', '浮云', '乌云']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased1 plain24: [' clouds', '云', 'cloud', ' cloud', 'Cloud', ' Cloud', '-cloud', '云彩', '_cloud', '云层', '/cloud', '云的', '雲', '.cloud', '的云', '云朵', '云计算', '云端', '云雾', ' cloudy', '.Cloud', '云服务', ' nube', ' 클라우드', ' mây', '云中', '天空', 'クラウド', '天气', '云上', '云山', '雯']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased0.5 plain24: [' clouds', '云', 'cloud', ' cloud', 'Cloud', ' Cloud', '-cloud', '云彩', '_cloud', '云层', '/cloud', '云的', '雲', '.cloud', '的云', '云朵', '云计算', '云端', '云雾', ' cloudy', '.Cloud', '云服务', ' nube', ' 클라우드', ' mây', '云中', '天空', 'クラウド', '天气', '云上', '云山', '雯']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased1 plain27: ['cloud', '云', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云层', '云彩', '/cloud', '的云', '云雾', '云朵', '.cloud', '.Cloud', '云端', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云飞', '云平台', '云上', 'クラウド', ' nube', '云天', '乌云']

Input: 'Français: "partie" - Русский: "часть"\nFrançais: "tour" - Русский: "башня"\nFrançais: "paire" - Русский: "пара"\nFrançais: "main" - Русский: "рука"\nFrançais: "nuage" - Русский: "'

Baseline: 'облако"\nFrançais:'

end-pass erased0.5 plain27: ['cloud', '云', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云层', '云彩', '/cloud', '的云', '云雾', '云朵', '.cloud', '.Cloud', '云端', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云飞', '云上', '云平台', 'クラウド', ' nube', '云天', ' đám']

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

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased1 J-lens: [' bags', ' suitcase', '书包', '钱包', ' pouch', ' bag', ' Bags', ' backpack', 'bags', '袋子', ' wallet', ' luggage', ' sacks', 'bag', ' sack', ' baggage', ' sacs', 'Bags', ' purse', 'wallet', ' 가방', ' pocket', 'Bag', ' wallets', '背包', ' pockets', '口袋', '箱包', ' basket', '-pocket', ' Tasche', '包包']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased0.5 J-lens: [' bags', ' suitcase', '钱包', '书包', ' pouch', ' bag', ' Bags', ' backpack', 'bags', '袋子', ' wallet', ' luggage', ' sacks', 'bag', ' sack', ' baggage', ' sacs', 'Bags', ' purse', 'wallet', ' 가방', ' pocket', 'Bag', ' wallets', '背包', ' pockets', '箱包', '口袋', ' basket', ' Tasche', '-pocket', '包包']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased1 plain24: ['вершенство', '加拿大', '袋子', '书包', ' recept', 'implements', ' tut', '随身携带', '钱包', ' zav', 'editary', ' plec', ' zak', '-validate', ' Taschen', ' moch', '收养', 'ferences', '流行病学', 'ISATION', '提', ' sak', ' bag', 'Accepted', ' виз', 'zac', 'please', 'wallet', '陪护', 'ください', '绽', ' bags']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased0.5 plain24: ['вершенство', '加拿大', '袋子', '书包', ' recept', ' tut', 'implements', '随身携带', '钱包', ' zav', 'editary', ' zak', ' plec', '-validate', ' Taschen', ' moch', '收养', 'ferences', '流行病学', '提', 'ISATION', ' sak', ' bag', 'Accepted', ' виз', 'zac', 'please', 'wallet', '陪护', 'ください', '绽', ' bags']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased1 plain27: [' bag', ' bags', '袋', ' Bags', 'Bag', 'bags', '袋子', ' BAG', 'bag', ' Bag', 'Bags', '_bag', '囊', ' backpack', ' túi', '口袋', 'wallet', '书包', '背包', '钱包', ' Backpack', 'Wallet', ' moch', '包', '布袋', '包的', ' purse', 'beutel', ' pouch', ' sacks', ' wallet', ' zak']

Input: 'Français: "or" - Русский: "золото"\nFrançais: "école" - Русский: "школа"\nFrançais: "couleur" - Русский: "цвет"\nFrançais: "danse" - Русский: "танец"\nFrançais: "sac" - Русский: "'

Baseline: 'сумка"\nFrançais:'

end-pass erased0.5 plain27: [' bag', ' bags', '袋', 'Bag', ' Bags', 'bags', '袋子', 'bag', ' BAG', ' Bag', 'Bags', '_bag', '囊', ' backpack', ' túi', '口袋', 'wallet', '书包', '背包', '钱包', ' Backpack', 'Wallet', ' moch', '包', '布袋', '包的', ' purse', 'beutel', ' pouch', ' sacks', ' wallet', ' zak']

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

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased1 J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' throat', ' jaw', ' lips', ' tongue', '嘴', ' saliva', ' teeth', ' speech', ' cheeks', '口语', ' jaws', ' bocca', ' palate', '喉咙', ' doorway', 'lips', ' tongues', '口才', '嘴唇', ' kiss', ' vagina', ' mulut', '牙齿', ' bite']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased0.5 J-lens: [' mouth', 'mouth', ' Mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' boca', ' throat', ' lips', ' jaw', ' tongue', '嘴', ' saliva', ' teeth', ' speech', ' cheeks', '口语', ' bocca', ' jaws', ' palate', 'lips', '喉咙', ' doorway', '口才', ' tongues', ' mulut', ' vagina', '嘴唇', '牙齿', ' kiss', ' bite']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased1 plain24: [' mouth', '嘴', '口腔', 'mouth', '口', '口语', '聘', '开口', ' Mouth', '嘴巴', 'emouth', '一口', ' oral', ' mouths', '出口', ' bocca', '口才', '张嘴', 'unciation', '-mouth', 'please', '、、', '的口', 'ullivan', 'peech', '口水', ' speech', '_exports', ' mou', '口区', '嘴边', '发音']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased0.5 plain24: [' mouth', '嘴', '口腔', 'mouth', '口', '口语', '聘', ' Mouth', 'emouth', '嘴巴', '开口', '一口', ' oral', ' bocca', ' mouths', '口才', '张嘴', '出口', 'unciation', '-mouth', '、、', '的口', 'please', 'ullivan', '口水', 'peech', '_exports', '口区', ' mou', ' speech', '嘴边', ' Oral']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased1 plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '口的', ' mouths', '嘴巴', '口腔', '-mouth', '的口', '开口', ' bocca', ' boca', ' oral', '口中', '唇', ' lips', '嘴唇', '嘴边', '张嘴', ' Oral', '口中的', '口の', ' miệng', 'emouth', '张口', '嘴里', ' рта', ' mulut', 'ปาก', '对口']

Input: 'Français: "son" - Русский: "звук"\nFrançais: "trois" - Русский: "три"\nFrançais: "milieu" - Русский: "середина"\nFrançais: "dix" - Русский: "десять"\nFrançais: "bouche" - Русский: "'

Baseline: 'рот"\nFrançais: "c'

end-pass erased0.5 plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '口的', ' mouths', '嘴巴', '口腔', '-mouth', '的口', ' bocca', ' boca', '开口', ' oral', '口中', '唇', ' lips', '嘴边', '嘴唇', '张嘴', ' Oral', '口の', '口中的', 'emouth', ' miệng', '张口', '嘴里', ' рта', ' mulut', '口に', 'ปาก']

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

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased1 J-lens: [' soil', '土壤', ' solvent', ' Soil', ' solution', ' dirt', ' solar', ' ground', ' soils', ' surface', 'solution', ' floor', ' pavement', ' sols', '_sol', '.sol', ' solver', ' terrain', ' solids', ' suelo', ' stone', ' Сол', 'ground', ' solitude', '_SOL', ' earth', ' sunlight', '溶剂', ' sun', ' sidewalk', ' solve', ' soul']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased0.5 J-lens: [' soil', '土壤', ' Soil', ' solvent', ' solution', ' ground', ' dirt', ' soils', ' solar', 'solution', ' floor', ' sols', 'ground', ' surface', ' pavement', '_sol', '.sol', ' suelo', ' terrain', ' solver', ' earth', ' solids', ' Сол', '_SOL', ' stone', '溶剂', ' sunlight', ' solitude', ' flooring', 'floor', ' floors', ' sun']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased1 plain24: [' сол', '_sol', 'сол', '太阳', ' solvent', ' soil', ' sols', ' Сол', '溶解', '_solution', '溶', ' soli', '.sol', ' solu', ' soluble', 'solver', ' solved', '土壤', '固体', ' solving', '(sol', '_SOL', ' solution', ' solves', '坚', '溶液', ' solve', '解决', '团结', '.solve', 'olvency', ' solar']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased0.5 plain24: [' сол', '_sol', 'сол', '太阳', ' sols', ' soil', ' solvent', ' Сол', '_solution', '溶解', ' soli', '溶', ' solu', '.sol', ' soluble', 'solver', ' solved', '土壤', '_SOL', '固体', '(sol', ' solving', ' solution', ' solves', '坚', '溶液', ' solve', '.solve', 'olvency', '解决', '团结', ' Soil']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased1 plain27: [' soil', '土壤', ' ground', '地面', 'ground', ' suelo', ' Soil', ' floor', '地板', ' sols', 'Ground', ' Ground', ' soils', '地面的', ' Boden', ' сол', '土', 'floor', '土地', ' tanah', '_ground', '解决', '泥土', 'Floor', ' đất', ' solutions', '地', ' solving', ' почвы', '地基', ' solution', '_solution']

Input: 'Français: "beauté" - Русский: "красота"\nFrançais: "rouge" - Русский: "красный"\nFrançais: "juge" - Русский: "судья"\nFrançais: "onde" - Русский: "волна"\nFrançais: "sol" - Русский: "'

Baseline: 'земля"\nFrançais: "'

end-pass erased0.5 plain27: [' soil', '土壤', ' ground', 'ground', '地面', ' suelo', ' Soil', ' floor', 'Ground', ' Ground', '地板', ' sols', ' soils', '地面的', ' Boden', '土地', ' tanah', 'floor', '_ground', '土', ' сол', ' đất', 'Floor', '泥土', '地基', 'ดิน', '解决', '地', '地表', ' почвы', ' أرض', '地板上']

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

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased1 J-lens: [' mountain', ' mountains', ' Mountains', 'mount', '山脉', ' Mountain', 'Mountain', ' montaña', ' hills', ' montagnes', '山峰', ' montagna', ' volcano', 'Mount', '山地', ' hill', '的山', ' gunung', '山区', ' mount', '山体', '-mount', '登山', ' canyon', ' Alps', ' cliffs', '山顶', ' wilderness', ' countryside', '山的', ' جبل', ' terrain']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased0.5 J-lens: [' mountain', ' mountains', ' Mountains', 'mount', '山脉', ' Mountain', 'Mountain', ' montaña', ' montagnes', ' hills', '山峰', ' montagna', 'Mount', ' volcano', '山地', ' hill', '的山', ' gunung', '山区', '山体', ' mount', '-mount', '登山', ' canyon', ' Alps', ' cliffs', '山顶', ' جبل', '山的', ' wilderness', '大山', ' countryside']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased1 plain24: [' mountains', ' mountain', 'mount', ' Mountains', ' montagnes', '山峰', ' montaña', '山脉', '加拿大', 'ountains', '岗', '登', '贡', 'haupt', '不可思议', 'alic', '耸', '_MOUNT', 'Mountain', 'Mount', ' montagna', '本山', 'Monad', '业余', '外国语', 'informatics', ' Mountain', 'verity', '译', '等奖', '重装', '登山']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased0.5 plain24: [' mountains', ' mountain', 'mount', ' Mountains', ' montagnes', ' montaña', '山峰', '山脉', '加拿大', 'ountains', '岗', '登', 'haupt', '贡', '不可思议', '_MOUNT', 'alic', '耸', 'Mountain', ' montagna', 'Mount', '本山', 'Monad', '外国语', '业余', '等奖', ' Mountain', 'verity', '重装', '登山', 'informatics', '译']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', 'ountains', '山脉', 'mount', '山峰', 'Mountain', ' hill', ' núi', 'Mount', ' montagnes', ' montaña', ' Mountain', 'OUNT', ' хол', ' hills', ' mount', '山的', '峰', ' Alps', 'ensus', '山体', ' montagna', ' slopes', '_MOUNT', 'เนิน', '山大', '山之', 'ภูเขา', ' Mount', '的山']

Input: 'Français: "cheval" - Русский: "лошадь"\nFrançais: "onde" - Русский: "волна"\nFrançais: "enfant" - Русский: "ребенок"\nFrançais: "grille" - Русский: "сетка"\nFrançais: "montagne" - Русский: "'

Baseline: 'горы"\nFrançais: "'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', 'ountains', '山脉', 'mount', '山峰', 'Mountain', ' hill', 'Mount', ' núi', ' montagnes', ' montaña', ' хол', 'OUNT', ' Mountain', '山的', ' hills', ' mount', ' montagna', '山体', ' Alps', '_MOUNT', '峰', 'ensus', '山之', 'เนิน', '山大', ' slopes', 'ภูเขา', '的山', ' Mount']

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

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased1 J-lens: [' heart', 'heart', ' hearts', '心脏', '-heart', '的心脏', ' corazón', ' Heart', 'Heart', ' coração', ' cuore', ' heartbeat', ' قلب', '心臟', ' Hearts', '心肺', '心跳', ' Herzen', ' cardiac', ' coeur', 'heartbeat', '心肌', ' conscience', 'core', 'قلب', ' القلب', ' heartfelt', '心房', '的心', '-hearted', ' ❤', '❤']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased0.5 J-lens: [' heart', 'heart', ' hearts', '心脏', '-heart', '的心脏', ' Heart', ' corazón', 'Heart', ' coração', ' cuore', ' heartbeat', '心臟', ' قلب', ' Hearts', ' Herzen', '心肺', '心跳', ' coeur', ' cardiac', 'heartbeat', '心肌', ' conscience', 'قلب', ' القلب', 'core', ' heartfelt', '心房', '的心', '-hearted', ' καρ', '❤']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased1 plain24: ['heart', ' heart', '心脏', '心的', '的心脏', ' قلب', 'قلب', ' Heart', ' hearts', 'Heart', ' corazón', ' القلب', '心', ' centrum', '核心', '的心', '心和', '-heart', '一颗', '_cores', ' Hearts', '的核心', '全心全意', ' coeur', '心了', '心臟', '为核心', ' heartbeat', 'heartbeat', ' cuore', '这颗', '心头']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased0.5 plain24: ['heart', ' heart', '心脏', '心的', '的心脏', ' قلب', 'قلب', ' Heart', ' hearts', 'Heart', ' corazón', ' القلب', '心', '的心', ' centrum', '核心', '-heart', '心和', '_cores', '一颗', ' Hearts', '全心全意', '心了', '心臟', ' coeur', '的核心', 'heartbeat', ' heartbeat', ' cuore', '为核心', '这颗', '心头']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased1 plain27: [' heart', 'heart', ' Heart', ' hearts', '心脏', 'Heart', '-heart', '心的', ' قلب', '心', '的心', '的心脏', ' corazón', ' coração', '心和', ' القلب', ' Hearts', 'หัวใจ', ' heartbeat', '-hearted', 'قلب', ' cardiac', '心脏病', '之心', '心臟', ' cuore', '心跳', 'heartbeat', ' jantung', '我的心', '心了', ' καρ']

Input: 'Français: "histoire" - Русский: "история"\nFrançais: "été" - Русский: "лето"\nFrançais: "pied" - Русский: "нога"\nFrançais: "exemple" - Русский: "пример"\nFrançais: "cœur" - Русский: "'

Baseline: 'сердце"\nFrançais:'

end-pass erased0.5 plain27: [' heart', 'heart', ' Heart', ' hearts', '心脏', 'Heart', '-heart', '心的', ' قلب', '心', '的心', '的心脏', ' corazón', ' coração', '心和', ' القلب', ' Hearts', 'หัวใจ', ' heartbeat', '-hearted', 'قلب', '心臟', ' cardiac', ' cuore', '心脏病', 'heartbeat', '之心', '心跳', '心了', ' jantung', '我的心', ' coeur']

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

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased1 J-lens: [' hand', ' hands', 'hand', ' handshake', ' Hand', '-main', 'Hand', 'hands', '>Main', ' fingers', ' mano', ' mains', ' tangan', '/main', '/Main', '_Main', ' HAND', ' Hands', '_main', ' palm', '我的手', '(main', '_hand', ' gloves', ' wrist', '手部', '.main', '-hand', ' glove', '手心', '\\"",', '_MAIN']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased0.5 J-lens: [' hand', 'hand', ' hands', ' handshake', ' Hand', 'Hand', '>Main', 'hands', ' mano', '-main', ' fingers', ' tangan', ' mains', '/Main', ' HAND', '_Main', '/main', ' Hands', '我的手', ' palm', '_hand', '_main', '(main', '手部', ' wrist', '手心', ' gloves', '-hand', '\\"",', ' glove', ' mão', ' manos']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased1 plain24: ['.main', '_MAIN', '_Main', '的主', '.MAIN', '主', '为主', '-main', '加拿大', '阿拉伯', '一把手', 'PRIMARY', 'aupt', ' الرئيسية', '主控', 'гла', '挥', '主治', '_main', '主要的', '之主', ' principale', '姆斯', '(main', '/main', '主力', '主场', '主要', 'の主', ' utama', ' HAND', '聘']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased0.5 plain24: ['.main', '_MAIN', '_Main', '.MAIN', '的主', '主', '为主', '加拿大', '阿拉伯', '-main', '一把手', 'PRIMARY', ' الرئيسية', 'aupt', '主控', 'гла', '挥', '主治', '之主', '_main', '主要的', ' principale', '主场', '(main', ' HAND', '姆斯', '主力', '/main', 'の主', '主要', ' utama', ' hand']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased1 plain27: [' hand', ' hands', '手掌', '手的', ' palm', ' Hand', '掌', 'hands', '手', '一只手', 'Hand', '的手', 'hand', ' HAND', '手心', '手部', 'Hands', ' Hands', '手指', '右手', ' pal', '掌心', ' fingers', '_HAND', '之手', '_hand', 'の手', '-hand', '握', 'handler', '.hand', ' Palma']

Input: 'Français: "défaite" - Русский: "поражение"\nFrançais: "soleil" - Русский: "солнце"\nFrançais: "océan" - Русский: "океан"\nFrançais: "quatre" - Русский: "четыре"\nFrançais: "main" - Русский: "'

Baseline: 'рука"\nFrançais: "'

end-pass erased0.5 plain27: [' hand', ' hands', '手掌', '手的', ' palm', ' Hand', '掌', 'hands', '手', '一只手', 'Hand', '的手', 'hand', ' HAND', '手心', '手部', 'Hands', ' Hands', '手指', '掌心', '之手', '右手', '_HAND', '_hand', ' fingers', ' pal', 'の手', 'handler', '握', '-hand', '.hand', ' mano']

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

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased1 J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', '-star', 'Stars', '/star', '星星', ' Star', ' estrella', ' звезда', ' aster', '星', '恒星', ' звезды', ' estrellas', '星光', 'Star', ' celestial', '.star', '星辰', '之星', ' estrel', ' étoiles', '_star', ' stella', ' constellation', '星的', ' estrelas', '-Star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased0.5 J-lens: [' stars', ' star', 'stars', 'star', ' Stars', '-stars', '-star', 'Stars', '/star', '星星', ' Star', ' estrella', ' aster', ' звезда', '星', '恒星', ' звезды', ' estrellas', 'Star', '星光', ' celestial', '星辰', '.star', '之星', ' estrel', ' étoiles', '_star', ' stella', '星的', ' constellation', ' estrelas', '-Star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased1 plain24: [' stars', ' star', '星', 'stars', ' Stars', '-stars', ' celestial', ' نجوم', ' astronomers', '.star', ' Astronomy', ' Star', '星的', 'Stars', '恒星', ' estrellas', 'star', '星光', ' astrology', ' aster', ' stellar', '之星', ' Stellar', '星座', ' звезд', '天文', 'stellar', ' Astroph', ' astronomy', '星星', ' starred', '_star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased0.5 plain24: [' stars', ' star', '星', 'stars', ' Stars', '-stars', ' نجوم', ' celestial', ' astronomers', '.star', ' Astronomy', ' Star', '星的', 'Stars', '恒星', ' estrellas', 'star', '星光', ' astrology', ' aster', '之星', '星座', ' stellar', ' звезд', ' Stellar', '天文', 'stellar', ' Astroph', ' astronomy', '星星', ' Bintang', '_star']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased1 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'Star', 'stars', 'star', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' звезд', '/star', ' STAR', ' звезды', '恒星', 'STAR', '明星', ' звезда', ' bintang', '之星', ' aster', ' stellar', ' starred', ' estrellas', '星级', '星光']

Input: 'Français: "grille" - Русский: "сетка"\nFrançais: "est" - Русский: "восток"\nFrançais: "village" - Русский: "деревня"\nFrançais: "vitesse" - Русский: "скорость"\nFrançais: "étoile" - Русский: "'

Baseline: 'звезда"\nFrançais:'

end-pass erased0.5 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'Star', 'stars', 'star', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' звезд', '/star', ' STAR', ' звезды', 'STAR', '恒星', ' bintang', '明星', ' звезда', '之星', ' aster', ' stellar', ' starred', ' estrellas', '星级', '星光']

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

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased1 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云', '云的', '的云', '云端', ' cloudy', '云服务', '云计算', '云彩', '.Cloud', '云雾', '云平台', '云海', '云中', ' 클라우드', ' sky', ' mây', 'クラウド', '云上', '雲端', ' skies']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased0.5 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', '-cloud', ' Cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云朵', '云的', '云', '的云', '云端', '云服务', ' cloudy', '云计算', '云彩', '.Cloud', '云雾', '云平台', '云海', '云中', ' 클라우드', ' sky', ' mây', '云上', 'クラウド', '雲端', ' skies']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased1 plain24: [' cloud', '云', ' clouds', 'cloud', ' Cloud', 'Cloud', '云计算', '云层', '-cloud', '_cloud', '云彩', '/cloud', '云端', '云朵', '.cloud', '雲', '云的', '的云', ' cloudy', '云服务', ' 클라우드', '云雾', 'クラウド', '云平台', '天空', '.Cloud', '云中', '云上', ' mây', '云山', 'LOUD', ' sky']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased0.5 plain24: [' cloud', ' clouds', '云', 'cloud', ' Cloud', 'Cloud', '云计算', '云层', '-cloud', '_cloud', '云彩', '/cloud', '云朵', '云端', '.cloud', '雲', '云的', '的云', ' cloudy', '云服务', ' 클라우드', '云雾', 'クラウド', '云平台', '天空', '.Cloud', '云中', '云上', ' mây', '云山', 'LOUD', ' sky']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased1 plain27: [' cloud', '云', 'cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '雲', '云的', '_cloud', '云彩', '云层', '的云', '云朵', '/cloud', '云端', '云计算', '.cloud', '云雾', ' cloudy', '云中', '.Cloud', 'クラウド', ' 클라우드', '云平台', '云上', '云服务', '云天', '云飞', '雲端', ' cl', ' mây']

Input: 'Русский: "часть" - Français: "partie"\nРусский: "башня" - Français: "tour"\nРусский: "пара" - Français: "paire"\nРусский: "рука" - Français: "main"\nРусский: "облако" - Français: "'

Baseline: 'nuage"\nРусский: "'

end-pass erased0.5 plain27: [' cloud', '云', 'cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '雲', '云的', '_cloud', '云层', '云彩', '的云', '云朵', '/cloud', '云计算', '云端', '.cloud', '云雾', ' cloudy', '云中', '.Cloud', 'クラウド', ' 클라우드', '云平台', '云上', '云服务', '云天', '雲端', '云飞', ' mây', ' cl']

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

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased1 J-lens: [' suitcase', ' luggage', ' bags', '书包', ' backpack', ' purse', ' bag', 'Bags', 'bags', 'bag', ' baggage', '钱包', ' pouch', ' Bags', '口袋', '包包', '袋子', ' tote', '箱包', 'uggage', ' wallet', 'Bag', '行李箱', 'กระเป๋า', ' 가방', ' bracelet', ' Tasche', '背包', '-pocket', ' necklace', ' souvenir', ' shoes']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased0.5 J-lens: [' suitcase', ' luggage', ' bags', '书包', ' purse', ' backpack', ' bag', 'Bags', 'bags', 'bag', ' baggage', '钱包', ' pouch', ' Bags', '口袋', '包包', '袋子', ' tote', '箱包', 'uggage', 'Bag', ' wallet', '行李箱', ' bracelet', 'กระเป๋า', ' 가방', ' Tasche', '背包', ' necklace', '-pocket', ' souvenir', ' shoes']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased1 plain24: [' bag', '加拿大', ' fond', ' tut', 'uggage', ' tart', ' recept', ' carrying', ' carried', ' ví', 'urses', '�', ' videoc', ' tote', '手提', 'ré', '負擔', ' agre', ' lent', ' gab', '书包', ' spanish', ' bags', ' lé', 'zuh', ' bat', ' excurs', ' trag', ' moch', 'udence', 'inne', ' purse']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased0.5 plain24: [' bag', '加拿大', ' fond', ' tut', 'uggage', ' tart', ' recept', ' carried', ' carrying', ' ví', 'urses', '�', ' videoc', ' tote', '手提', '負擔', 'ré', ' agre', '书包', ' lent', ' gab', ' spanish', ' lé', ' bags', 'zuh', ' excurs', ' bat', ' moch', ' trag', 'udence', 'inne', ' purse']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased1 plain27: [' bag', ' bags', 'bag', 'Bag', ' sac', ' Bag', 'bags', '袋', ' Bags', ' BAG', '_bag', ' moch', ' backpack', '囊', ' Sac', '袋子', ' purse', ' tote', 'Bags', ' bols', ' sacs', ' luggage', 'กระเป๋า', ' baggage', ' saco', ' túi', 'uggage', ' wallet', ' 가방', ' tas', '书包', 'Wallet']

Input: 'Русский: "золото" - Français: "or"\nРусский: "школа" - Français: "école"\nРусский: "цвет" - Français: "couleur"\nРусский: "танец" - Français: "danse"\nРусский: "сумка" - Français: "'

Baseline: 'sac"\nРусский: "'

end-pass erased0.5 plain27: [' bag', ' bags', 'bag', 'Bag', ' sac', ' Bag', 'bags', '袋', ' Bags', ' BAG', '_bag', ' moch', ' backpack', '囊', ' Sac', '袋子', ' purse', ' tote', 'Bags', ' bols', ' sacs', ' luggage', 'กระเป๋า', ' baggage', ' saco', ' túi', 'uggage', ' 가방', ' wallet', ' tas', '书包', 'Wallet']

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

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased1 J-lens: [' mouth', 'mouth', ' mouths', ' Mouth', ' throat', '口腔', '-mouth', ' palate', ' lips', '嘴巴', ' cheeks', ' jaw', ' tongue', ' рта', '喉咙', ' boca', ' nose', ' lungs', ' saliva', ' jaws', ' teeth', 'lips', '嘴', ' pores', ' mulut', ' genitals', ' bocca', 'roat', ' vagina', ' penis', ' nostr', ' doorway']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased0.5 J-lens: [' mouth', 'mouth', ' mouths', ' Mouth', ' throat', '口腔', '-mouth', ' palate', ' lips', '嘴巴', ' cheeks', ' jaw', ' boca', ' рта', '喉咙', ' tongue', ' nose', 'lips', ' saliva', ' jaws', ' lungs', ' teeth', ' mulut', ' pores', ' bocca', '嘴', ' genitals', 'roat', ' vagina', ' penis', ' nostr', ' noses']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased1 plain24: [' mouth', '口腔', 'mouth', '聘', '膛', ' Mouth', ' рта', '口语', '口', 'roat', ' مخاط', ' oral', '-mouth', '嘴巴', ' ratus', 'phinx', ' lips', ' anatom', ' saliva', ' aficion', ' riz', ' bocca', ' rot', ' biro', '卖点', '读卡', 'utilus', '天安门', ' sailor', '的口', 'lips', ' recept']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased0.5 plain24: [' mouth', '口腔', 'mouth', '聘', '膛', ' Mouth', ' рта', '口语', 'roat', ' مخاط', '口', ' oral', '-mouth', ' ratus', '嘴巴', 'phinx', ' lips', ' saliva', ' aficion', ' anatom', ' riz', ' biro', ' bocca', '卖点', ' rot', '读卡', 'utilus', 'lips', '天安门', '的口', ' sailor', ' mouths']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased1 plain27: [' mouth', '口', 'mouth', '嘴', '口的', '嘴巴', ' Mouth', ' mouths', '口腔', '-mouth', ' oral', '的口', ' bocca', '口中', ' boca', ' lips', '开口', '唇', ' miệng', '口中的', 'ปาก', ' Oral', '口の', ' рта', ' mulut', '张嘴', '嘴唇', '口红', '张口', 'emouth', '口头', '口镇']

Input: 'Русский: "звук" - Français: "son"\nРусский: "три" - Français: "trois"\nРусский: "середина" - Français: "milieu"\nРусский: "десять" - Français: "dix"\nРусский: "рот" - Français: "'

Baseline: 'bouche"\nРусский: "'

end-pass erased0.5 plain27: [' mouth', '口', 'mouth', '嘴', ' Mouth', '口的', '嘴巴', ' mouths', '口腔', '-mouth', ' oral', '的口', ' bocca', ' boca', '口中', ' lips', '开口', '唇', ' miệng', '口中的', '口の', 'ปาก', ' Oral', ' mulut', ' рта', '张嘴', '嘴唇', '张口', '口红', 'emouth', '口镇', '口头']

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

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased1 J-lens: [' soil', '土壤', ' terrain', ' soils', ' Soil', '土壤中', '泥土', ' почвы', ' tanah', ' почву', ' earth', ' tierra', ' Terrain', 'terrain', '土地', ' terreno', ' terra', ' terre', '沃土', 'ground', ' ground', ' dirt', '的土地', '土层', '土', 'Earth', 'earth', ' suolo', ' suelo', '土的', '大地', ' terrains']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased0.5 J-lens: [' soil', '土壤', ' terrain', ' soils', ' Soil', '土壤中', '泥土', ' почвы', ' tanah', ' почву', ' earth', ' tierra', ' Terrain', 'terrain', ' terreno', '土地', ' terre', '沃土', ' terra', 'ground', ' ground', '土层', '的土地', ' dirt', '土', ' suolo', 'Earth', 'earth', ' suelo', '土的', 'ดิน', '大地']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased1 plain24: [' soil', '土壤', ' Soil', ' soils', ' terrain', ' почву', ' почвы', '土', ' tanah', '沃土', '土地', ' land', '土壤中', '脚下的', ' ground', '泥土', ' Dirt', ' 토', 'ดิน', ' dirt', ' đất', '底层', '土层', '地基', ' terre', '土的', ' أرض', 'ground', '地层', ' fertile', '接地气', '操场']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased0.5 plain24: [' soil', '土壤', ' Soil', ' soils', ' почвы', ' почву', ' terrain', '土', ' tanah', '沃土', '土壤中', '土地', '脚下的', ' land', ' ground', '泥土', ' Dirt', 'ดิน', ' 토', ' dirt', '土层', ' đất', '底层', '地基', '土的', ' terre', ' أرض', 'ground', ' fertile', '地层', '接地气', '操场']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased1 plain27: [' soil', '土壤', ' Soil', ' soils', '土', '土壤中', '泥土', ' tanah', ' почвы', '土的', 'ดิน', ' ground', ' earth', ' почву', ' suelo', '土地', ' đất', ' terre', 'ground', ' Boden', ' terrain', '土层', ' land', ' dirt', ' 토', '地面', ' Ground', '壤', 'Ground', ' Earth', '土地上', ' terra']

Input: 'Русский: "красота" - Français: "beauté"\nРусский: "красный" - Français: "rouge"\nРусский: "судья" - Français: "juge"\nРусский: "волна" - Français: "onde"\nРусский: "почва" - Français: "'

Baseline: 'sol"\nРусский: "с'

end-pass erased0.5 plain27: [' soil', '土壤', ' Soil', ' soils', '土', '土壤中', '泥土', ' tanah', ' почвы', '土的', 'ดิน', ' ground', ' earth', ' почву', ' suelo', ' đất', '土地', ' terre', 'ground', ' Boden', '土层', ' terrain', ' 토', ' Ground', '地面', ' dirt', ' land', '壤', 'Ground', ' suolo', '土地上', ' Earth']

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

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased1 J-lens: [' mountains', ' mountain', ' hills', ' Mountains', '山峰', ' hill', ' volcano', '山脉', 'mount', 'Mountain', ' cliffs', ' terrain', ' Mountain', ' gunung', ' canyon', ' горы', ' glacier', ' Alps', 'Mount', ' volcan', '山体', '山地', '山区', ' gorge', ' valley', ' massif', '的山', ' mound', 'landscape', '山顶', ' glaciers', ' countryside']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased0.5 J-lens: [' mountains', ' mountain', ' hills', ' Mountains', 'mount', '山峰', ' hill', '山脉', ' volcano', 'Mountain', ' Mountain', ' gunung', ' cliffs', ' terrain', ' горы', ' canyon', 'Mount', ' glacier', ' Alps', '山地', '山体', '山区', ' volcan', '的山', ' massif', '山顶', '山的', ' gorge', ' mount', ' valley', ' mound', ' countryside']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased1 plain24: [' mountains', ' mountain', '加拿大', '山峰', '发卡', ' Mountains', ' fond', 'mount', ' observ', '贺', ' emin', ' vain', 'peater', ' gir', ' hill', ' terrain', ' plateau', ' precip', ' volcan', '岗', ' peninsula', ' aficion', 'alic', '卖点', '山脉', ' volcano', '兢兢业业', ' mam', '峰', 'imestone', ' pel', ' horn']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased0.5 plain24: [' mountains', ' mountain', '加拿大', '山峰', '发卡', 'mount', ' Mountains', ' fond', '贺', ' emin', ' observ', 'peater', ' hill', ' vain', ' gir', ' plateau', ' terrain', ' volcan', ' precip', '岗', ' aficion', '卖点', ' peninsula', 'alic', '兢兢业业', '山脉', ' volcano', ' mam', 'Mount', '峰', 'imestone', ' pel']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', ' hill', '峰', '山峰', ' hills', ' fond', ' peak', ' Peak', 'Peak', ' volcano', 'mount', ' Mountain', ' peaks', ' slopes', ' slope', '高峰', ' plateau', ' incl', ' volcan', 'เนิน', 'Mountain', 'Mount', 'peak', ' hil', '加拿大', ' dés', ' emin', '山顶', '山之', '_peak']

Input: 'Русский: "лошадь" - Français: "cheval"\nРусский: "волна" - Français: "onde"\nРусский: "ребенок" - Français: "enfant"\nРусский: "сетка" - Français: "grille"\nРусский: "гора" - Français: "'

Baseline: 'montagne"\nРусский: "'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', ' hill', '峰', '山峰', ' hills', 'mount', ' fond', ' Peak', 'Peak', ' peak', 'Mount', ' volcano', ' Mountain', 'Mountain', '高峰', 'เนิน', ' plateau', ' slopes', ' volcan', ' hil', '山之', ' peaks', ' slope', '加拿大', '山顶', 'peak', ' incl', ' dés', ' emin', '山脉']

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

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased1 J-lens: [' heart', 'heart', ' hearts', '心脏', '-heart', ' corazón', '的心脏', '心臟', 'Heart', ' Heart', ' cœur', ' coração', ' cuore', ' heartbeat', ' сердца', ' قلب', ' cardiac', ' Herzen', ' coeur', '心肺', '心跳', ' Hearts', 'heartbeat', ' cardia', ' القلب', ' jantung', '心脏病', 'card', ' cardi', '-hearted', ' καρ', '心肌']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased0.5 J-lens: [' heart', ' hearts', 'heart', '心脏', ' corazón', '-heart', '的心脏', '心臟', 'Heart', ' Heart', ' cœur', ' coração', ' cuore', ' heartbeat', ' сердца', ' cardiac', ' قلب', ' Herzen', ' coeur', '心肺', '心跳', ' Hearts', 'heartbeat', ' cardia', 'card', ' القلب', '心脏病', ' jantung', ' cardi', '-hearted', ' καρ', '心肌']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased1 plain24: [' heart', 'heart', '心脏', '的心脏', ' Heart', 'Heart', ' hearts', ' corazón', '心', '心臟', ' قلب', ' cœur', ' сердца', 'قلب', '心的', '-heart', ' القلب', ' cardiac', '心脏病', ' cuore', '心了', '的心', '心肺', 'heartbeat', ' coração', '之心', '全心全意', ' centre', ' cardia', ' coeur', ' καρ', ' heartbeat']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased0.5 plain24: [' heart', 'heart', '心脏', '的心脏', ' Heart', 'Heart', ' hearts', ' corazón', '心', '心臟', ' قلب', ' cœur', ' сердца', 'قلب', '心的', ' القلب', '-heart', ' cardiac', '心脏病', ' cuore', '心了', '的心', '心肺', 'heartbeat', ' coração', '之心', ' centre', '全心全意', ' coeur', ' cardia', ' καρ', ' heartbeat']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased1 plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心的', ' corazón', '心', '的心脏', ' cœur', ' قلب', '的心', ' coração', ' сердца', ' cardiac', ' القلب', '心臟', 'หัวใจ', '-hearted', ' heartbeat', ' Hearts', 'قلب', '心跳', 'heartbeat', '心和', ' cuore', '心脏病', ' Herz', ' cardia', '之心']

Input: 'Русский: "история" - Français: "histoire"\nРусский: "лето" - Français: "été"\nРусский: "нога" - Français: "pied"\nРусский: "пример" - Français: "exemple"\nРусский: "сердце" - Français: "'

Baseline: 'cœur"\nРусский: "'

end-pass erased0.5 plain27: [' heart', 'heart', ' Heart', 'Heart', ' hearts', '-heart', '心脏', '心的', '心', ' corazón', '的心脏', ' cœur', '的心', ' قلب', ' coração', ' сердца', ' cardiac', ' القلب', '心臟', 'หัวใจ', '-hearted', ' heartbeat', ' Hearts', 'قلب', '心跳', '心和', 'heartbeat', ' cuore', '心脏病', ' Herz', ' cardia', '之心']

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

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased1 J-lens: ['hand', ' hand', '手臂', 'Hand', ' hands', ' handshake', ' forearm', ' tangan', 'hands', ' руки', ' HAND', '_hand', ' wrist', '手的', ' Hand', ' mano', ' arm', ' arms', '之手', '手掌', '手腕', 'Hands', ' fingers', ' Hands', '的手臂', '手', '手部', ' wrists', '臂', 'arms', '(hand', ' руке']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased0.5 J-lens: ['hand', ' hand', 'Hand', '手臂', ' hands', ' handshake', ' forearm', ' tangan', 'hands', ' руки', ' HAND', '_hand', ' wrist', '手的', ' mano', ' Hand', ' arms', ' arm', '之手', '手掌', '手腕', ' fingers', ' Hands', 'Hands', '的手臂', '手部', ' wrists', '手', '臂', 'arms', '(hand', ' руке']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased1 plain24: [' hand', '阿拉伯', ' arm', 'Hand', ' HAND', 'hand', ' manus', '加拿大', 'naissance', '用手', ' Hand', '鲁', '挥', '_hand', '手', '人脉', '手臂', ' handy', ' hands', ' rud', '手数', '-hand', '的手臂', '聘', ' videoc', 'ủy', ' rach', 'lier', '一只手', 'manuel', '手的', 'ré']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased0.5 plain24: [' hand', '阿拉伯', ' arm', 'Hand', ' HAND', 'hand', ' manus', '加拿大', 'naissance', '用手', '鲁', ' Hand', '_hand', '挥', '手', '人脉', ' handy', '手臂', ' hands', ' rud', '手数', '-hand', '的手臂', '聘', ' videoc', 'ủy', ' rach', '一只手', 'manuel', 'lier', '手的', 'ré']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased1 plain27: [' arm', '手臂', ' hand', '臂', '的手臂', ' hands', '手', 'hand', 'arm', ' Arm', '手的', '_arm', 'Arm', ' Hand', 'Hand', '_hand', 'hands', ' forearm', '一只手', '之手', ' arms', '-hand', '只手', '右手', '胳膊', '-arm', ' руки', ' HAND', ' руку', ' bras', ' palm', '手掌']

Input: 'Русский: "поражение" - Français: "défaite"\nРусский: "солнце" - Français: "soleil"\nРусский: "океан" - Français: "océan"\nРусский: "четыре" - Français: "quatre"\nРусский: "рука" - Français: "'

Baseline: 'main"\nРусский: "но'

end-pass erased0.5 plain27: [' arm', '手臂', ' hand', '臂', '的手臂', ' hands', '手', 'hand', 'arm', ' Arm', '手的', '_arm', 'Arm', ' Hand', 'Hand', '_hand', 'hands', ' forearm', '一只手', ' arms', '只手', '之手', '-hand', '右手', '胳膊', '-arm', ' руки', ' HAND', ' руку', ' bras', ' palm', '手掌']

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

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased1 J-lens: [' stars', ' star', 'stars', ' Stars', '-stars', 'star', 'Stars', '星星', '-star', '/star', '星辰', ' звезды', '之星', '星光', '恒星', ' estrella', '星的', '_star', '星', ' Star', ' estrellas', 'Star', ' étoiles', '星座', ' estrel', ' estrelas', ' aster', ' celestial', ' stella', '颗星', ' bintang', '.star']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased0.5 J-lens: [' stars', ' star', 'stars', ' Stars', 'star', '-stars', 'Stars', '星星', '-star', '/star', '之星', '星辰', ' звезды', '星光', '星', ' Star', '_star', '星的', '恒星', ' estrella', ' estrellas', 'Star', ' étoiles', '星座', ' estrel', ' celestial', ' aster', ' estrelas', ' stella', '颗星', ' bintang', '.star']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased1 plain24: [' stars', ' star', '星', 'stars', ' Stars', '星的', ' aster', '_star', ' Star', 'star', '星座', '-stars', '.star', '之星', 'Star', '恒星', 'Stars', ' starred', '-star', ' celestial', '星星', ' astronomers', '星光', ' astronom', ' yıld', '颗星', ' astrology', ' astro', ' звезды', ' Astroph', '星级', ' stellar']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased0.5 plain24: [' stars', ' star', '星', 'stars', ' Stars', '星的', ' aster', '_star', ' Star', 'star', '星座', '-stars', '.star', 'Star', '恒星', '之星', 'Stars', ' starred', ' celestial', '-star', '星星', ' astronomers', '星光', ' astronom', ' yıld', ' astro', '颗星', ' astrology', ' Astroph', ' звезды', ' éto', ' stellar']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased1 plain27: [' star', ' stars', '星', ' Star', '星的', ' Stars', 'star', 'stars', 'Star', '-star', '星星', '_star', 'Stars', '.star', '-stars', ' aster', '恒星', '之星', '-Star', ' STAR', '明星', ' bintang', '星光', ' stellar', ' starred', '颗星', 'STAR', '/star', ' звезды', '星级', ' estrel', ' estrellas']

Input: 'Русский: "сетка" - Français: "grille"\nРусский: "восток" - Français: "est"\nРусский: "деревня" - Français: "village"\nРусский: "скорость" - Français: "vitesse"\nРусский: "звезда" - Français: "'

Baseline: 'étoile"\nРусский: "'

end-pass erased0.5 plain27: [' star', ' stars', '星', ' Star', '星的', ' Stars', 'star', 'stars', 'Star', '-star', '_star', '星星', 'Stars', '.star', '-stars', ' aster', '恒星', '-Star', ' STAR', '之星', '明星', ' bintang', ' starred', '星光', ' stellar', 'STAR', '颗星', '/star', ' звезды', '星级', ' estrel', ' estrellas']

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

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased1 J-lens: [' books', ' book', ' Books', 'book', '书籍', 'books', ' BOOK', ' Book', '-book', '-books', 'Books', ' buku', '书的', '/book', 'Book', '一本书', '书', '书本', '/books', ' booklet', ' bookstore', 'BOOK', '的书', '_book', '图书', '書', ' книги', '.book', ' libro', '之书', '(book', '这本书']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased0.5 J-lens: [' books', ' book', 'book', ' Books', '书籍', 'books', ' BOOK', ' Book', '-book', '-books', 'Books', ' buku', 'Book', '/book', '书的', '一本书', '书', '书本', '/books', ' booklet', ' bookstore', 'BOOK', '的书', '_book', '图书', ' книги', '書', '.book', ' libro', '(book', '之书', '这本书']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased1 plain24: ['书籍', ' BOOK', ' books', '一本书', '书', ' book', '书的', '书记', '图书', '加拿大', '这本书', '-books', '一本', '册', '书本', '的书', '阿拉伯', ' книга', '之书', ' книги', '.book', ' Books', ' الكتاب', ' książ', '书名', '/books', ' buku', '书房', 'book', ' книг', '俱乐部', '书包']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased0.5 plain24: ['书籍', ' BOOK', ' books', '一本书', '书', ' book', '书的', '书记', '图书', '加拿大', '这本书', '-books', '一本', '册', '书本', '的书', ' книги', '阿拉伯', '之书', ' книга', '.book', ' Books', ' الكتاب', ' książ', '书名', '/books', ' buku', '书房', 'book', ' книг', '俱乐部', '书包']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased1 plain27: ['书籍', ' books', ' book', '书', '书的', ' BOOK', 'book', '一本书', '图书', 'books', '书本', ' Books', '这本书', ' Book', '-books', ' книги', 'Book', '_book', '-book', ' книга', '的书', '/books', 'Books', '/book', '.book', '书中', 'BOOK', '书中的', '一本', '之书', ' buku', '_BOOK']

Input: 'Deutsch: "zehn" - Русский: "десять"\nDeutsch: "Rede" - Русский: "речь"\nDeutsch: "Teil" - Русский: "часть"\nDeutsch: "Herz" - Русский: "сердце"\nDeutsch: "Buch" - Русский: "'

Baseline: 'книга"\nDeutsch: "'

end-pass erased0.5 plain27: ['书籍', ' books', ' book', '书', '书的', ' BOOK', 'book', '一本书', '图书', 'books', '书本', '这本书', ' Books', ' Book', '-books', ' книги', 'Book', '_book', '-book', ' книга', '的书', '/books', 'Books', '.book', '/book', '书中', 'BOOK', '书中的', '一本', '之书', ' buku', '_BOOK']

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

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased1 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云的', ' cloudy', '云', '云朵', '的云', ' nube', '云雾', '云服务', '云彩', '.Cloud', '云计算', ' fog', '云端', ' sky', '云中', '云海', '云平台', 'クラウド', ' mây', ' 클라우드', ' skies']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased0.5 J-lens: [' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '/cloud', '_cloud', '.cloud', '云层', '雲', '云的', ' cloudy', '云', '云朵', '的云', ' nube', '云雾', '云服务', '.Cloud', '云彩', '云计算', ' fog', '云端', '云中', ' sky', '云海', '云平台', 'クラウド', ' mây', ' 클라우드', ' skies']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased1 plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云彩', '云的', '/cloud', '雲', '云层', '云朵', '.cloud', '的云', '云计算', '云端', ' cloudy', '云中', '云服务', ' 클라우드', '.Cloud', 'クラウド', '云雾', '天空', ' mây', '云上', ' nube', '云平台', '云浮', '白云']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased0.5 plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', '-cloud', '_cloud', '云彩', '云的', '/cloud', '雲', '云层', '云朵', '.cloud', '的云', '云计算', '云端', ' cloudy', '云中', '云服务', ' 클라우드', '.Cloud', 'クラウド', '云雾', '天空', ' mây', ' nube', '云上', '云平台', '云浮', '白云']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased1 plain27: ['云', 'cloud', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云彩', '云层', '/cloud', '的云', '.cloud', '云朵', '云雾', '云端', '.Cloud', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云天', '云平台', 'クラウド', '云上', '云飞', ' nube', ' đám']

Input: 'Deutsch: "Netz" - Русский: "сетка"\nDeutsch: "Farbe" - Русский: "цвет"\nDeutsch: "Börse" - Русский: "биржа"\nDeutsch: "Streifen" - Русский: "полоса"\nDeutsch: "Wolke" - Русский: "'

Baseline: 'облако"\nDeutsch: "'

end-pass erased0.5 plain27: ['云', 'cloud', ' cloud', ' clouds', ' Cloud', 'Cloud', '-cloud', '云的', '雲', '_cloud', '云彩', '云层', '/cloud', '的云', '.cloud', '云朵', '云雾', '云端', '.Cloud', '云计算', ' cloudy', '云中', '云服务', ' 클라우드', ' mây', '云天', '云平台', 'クラウド', '云上', '云飞', ' nube', ' đám']

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

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased1 J-lens: [' pockets', ' pouch', ' pocket', '钱包', '-pocket', ' wallet', '口袋', ' purse', ' suitcase', ' bags', 'Pocket', ' Pocket', '口袋里', ' wallets', ' holster', ' Wallet', 'wallet', ' luggage', ' Bags', ' Taschen', ' bag', 'bags', ' backpack', '袋子', '书包', 'Wallet', ' tote', 'กระเป๋า', ' bracelet', ' trousers', 'Bags', 'bag']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased0.5 J-lens: [' pockets', ' pouch', ' pocket', '钱包', '-pocket', ' wallet', '口袋', ' purse', ' suitcase', ' bags', 'Pocket', ' Pocket', '口袋里', ' wallets', ' holster', ' Wallet', 'wallet', ' luggage', ' Bags', ' Taschen', ' bag', 'bags', ' backpack', '袋子', '书包', 'Wallet', ' tote', ' trousers', 'Bags', 'กระเป๋า', ' bracelet', 'bag']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased1 plain24: ['随身携带', 'Pocket', ' pockets', '加拿大', '钱包', 'implements', ' Taschen', ' recept', '猜你喜欢', ' LIABILITY', ' pocket', '口袋', 'wallet', ' plec', '袋子', ' pouc', ' tut', '-pocket', '战术', '提', '绽', 'zuh', '揣', '流行病学', 'udit', 'Wallet', 'favorites', ' purse', '收容', ' poc', ' Pocket', '周转']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased0.5 plain24: ['随身携带', 'Pocket', ' pockets', '加拿大', '钱包', 'implements', ' Taschen', ' recept', '猜你喜欢', ' LIABILITY', ' pocket', '口袋', 'wallet', ' plec', '袋子', ' pouc', ' tut', '-pocket', '战术', '提', '绽', 'zuh', '揣', '流行病学', 'udit', 'Wallet', 'favorites', ' purse', ' poc', ' Pocket', '收容', '周转']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased1 plain27: [' pocket', '口袋', ' pockets', 'Pocket', ' wallet', '钱包', ' wallets', '-pocket', ' Pocket', 'Wallet', 'wallet', ' Wallet', '囊', ' bag', ' pouch', '袋', '_wallet', ' túi', '袋子', ' purse', '.wallet', ' bags', ' Taschen', ' bols', 'Bag', 'bags', 'Bags', ' Bags', 'bag', 'กระเป๋า', ' BAG', ' poch']

Input: 'Deutsch: "Person" - Русский: "человек"\nDeutsch: "Tür" - Русский: "дверь"\nDeutsch: "Provinz" - Русский: "провинция"\nDeutsch: "sechs" - Русский: "шесть"\nDeutsch: "Tasche" - Русский: "'

Baseline: 'кошелек"\nDeutsch:'

end-pass erased0.5 plain27: [' pocket', '口袋', ' pockets', 'Pocket', '钱包', ' wallet', '-pocket', ' wallets', ' Pocket', 'Wallet', 'wallet', ' Wallet', '囊', ' bag', '袋', ' pouch', '_wallet', ' túi', '袋子', ' purse', '.wallet', ' bags', 'bags', ' bols', ' Taschen', 'Bag', 'Bags', ' Bags', 'bag', 'กระเป๋า', ' BAG', ' poch']

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

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased1 J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' jaw', ' lips', ' boca', '嘴', ' saliva', ' throat', '嘴唇', ' mulut', '口', ' palate', ' teeth', ' doorway', 'lips', ' bouche', ' jaws', ' bocca', '喉咙', '口语', ' kiss', '出口', ' miệng', ' tongues', '舌头', ' pores']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased0.5 J-lens: [' mouth', ' Mouth', 'mouth', ' mouths', '-mouth', '口腔', '嘴巴', ' tongue', ' jaw', ' lips', ' boca', '嘴', ' saliva', ' throat', ' mulut', '嘴唇', '口', 'lips', ' bouche', ' palate', ' teeth', ' bocca', ' doorway', '喉咙', ' jaws', ' miệng', '口语', ' kiss', '出口', ' tongues', '舌头', '进出口']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased1 plain24: [' mouth', '口', 'mouth', '口腔', ' Mouth', '嘴', ' mouths', '口的', '嘴巴', '出口', ' oral', '进出口', '聘', '_exports', '的口', '-mouth', ' mou', '一口', '口语', '口红', '口头', '开口', '口区', 'emouth', '嘴唇', ' bocca', '口中', ' м', '出入口', '张嘴', '口径', '口才']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased0.5 plain24: [' mouth', 'mouth', '口', '口腔', ' Mouth', '嘴', ' mouths', '口的', '嘴巴', '出口', '进出口', ' oral', '聘', '_exports', '的口', '-mouth', ' mou', '一口', '口语', '口红', '口区', 'emouth', '口头', ' bocca', '开口', '嘴唇', '出入口', '口中', '口径', '张嘴', '口才', '口腔溃疡']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased1 plain27: [' mouth', '口', '嘴', 'mouth', '口的', ' mouths', ' Mouth', '嘴巴', '的口', '-mouth', '口腔', '口中', ' boca', '开口', ' oral', ' bocca', '口の', '口中的', '嘴里', ' miệng', ' bouche', '嘴边', ' lips', '张口', '唇', '嘴唇', '张嘴', ' Oral', ' mulut', '口红', '口に', ' рта']

Input: 'Deutsch: "löschen" - Русский: "удалить"\nDeutsch: "Version" - Русский: "версия"\nDeutsch: "Freund" - Русский: "друг"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Mund" - Русский: "'

Baseline: 'рот"\nDeutsch: "Kopf'

end-pass erased0.5 plain27: [' mouth', '口', '嘴', 'mouth', '口的', ' mouths', ' Mouth', '嘴巴', '的口', '-mouth', '口腔', '口中', ' boca', '开口', ' bocca', ' oral', '口の', '口中的', '嘴里', ' bouche', ' miệng', '嘴边', '张口', ' lips', '唇', ' mulut', '口に', '嘴唇', '张嘴', ' Oral', ' рта', '口红']

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

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased1 J-lens: [' floor', ' soil', ' ground', ' terrain', ' floors', 'floor', ' flooring', '土壤', '地板', ' earth', ' dirt', ' Floor', 'ground', ' Soil', ' surface', ' body', ' pavement', '地面', ' soils', ' Ground', ' bottom', 'Floor', '地基', ' suelo', ' basement', ' Earth', ' foundation', ' substrate', ' Terrain', ' 바닥', '-floor', 'body']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased0.5 J-lens: [' floor', ' soil', ' ground', ' floors', 'floor', ' terrain', ' earth', ' flooring', 'ground', '地板', '土壤', ' Floor', ' dirt', ' Soil', ' Ground', '地面', ' surface', 'Floor', ' body', ' pavement', '地基', ' soils', ' suelo', 'Ground', ' Earth', ' Terrain', ' tierra', ' terra', '-floor', ' 바닥', ' bottom', '-ground']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased1 plain24: ['地面', '底层', ' soil', ' ground', ' floor', '地面的', '地基', 'floor', 'Floor', '在地上', 'ground', '地板', '土', '土壤', 'Ground', 'loor', ' Dirt', '地', '基层', ' أرض', ' terrain', '底价', ' Flooring', ' Ground', '卑', '加拿大', ' Floor', '大地', '地表', 'urface', '平面图', ' Soil']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased0.5 plain24: ['地面', '底层', ' ground', ' soil', '地面的', 'ground', ' floor', '地基', '在地上', 'Floor', 'floor', '地板', 'Ground', ' أرض', '土壤', '土', 'loor', ' Dirt', ' Ground', '地', ' Flooring', '基层', ' terrain', '底价', '大地', '加拿大', '卑', '_ground', ' Floor', '地表', '_floor', 'urface']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased1 plain27: [' ground', '地面', ' floor', 'ground', ' Ground', '地板', ' soil', 'Ground', '土壤', 'floor', '地面的', ' suelo', ' Floor', 'Floor', '地', '_ground', ' floors', ' Soil', '地基', ' đất', '在地上', '地板上', '土地', ' tanah', ' أرض', '地面上', ' grounds', ' earth', ' grounded', '的地', '地表', '-ground']

Input: 'Deutsch: "Fuß" - Русский: "нога"\nDeutsch: "Fluss" - Русский: "река"\nDeutsch: "Osten" - Русский: "восток"\nDeutsch: "Gitter" - Русский: "сетка"\nDeutsch: "Boden" - Русский: "'

Baseline: 'земля"\nDeutsch: "B'

end-pass erased0.5 plain27: [' ground', '地面', 'ground', ' floor', ' Ground', 'Ground', '地板', ' soil', '地面的', 'floor', '土壤', ' suelo', ' Floor', 'Floor', '_ground', ' floors', '地', ' Soil', '地基', ' đất', ' tanah', '在地上', '土地', '地板上', ' أرض', '-ground', ' earth', '地面上', ' الأرض', '的地', ' grounds', ' grounded']

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

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased1 J-lens: [' mountains', ' mountain', ' Mountains', 'mount', '山脉', ' hills', 'Mountain', '山峰', ' Mountain', ' montaña', ' montagne', ' montagnes', ' hill', ' gunung', '山地', ' volcano', '山体', '的山', ' montagna', 'Mount', ' cliffs', ' Alps', '山的', '登山', '山区', '山顶', ' terrain', ' glacier', ' جبل', '山', ' canyon', ' mount']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased0.5 J-lens: [' mountains', ' mountain', ' Mountains', 'mount', '山脉', '山峰', 'Mountain', ' hills', ' Mountain', ' montaña', ' montagne', ' montagnes', ' hill', ' gunung', ' montagna', '山地', '山体', ' volcano', '的山', 'Mount', ' cliffs', ' Alps', '山的', '登山', '山区', ' جبل', '山顶', ' glacier', ' terrain', ' mount', '大山', ' canyon']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased1 plain24: [' mountains', ' mountain', ' Mountains', '山峰', ' montaña', 'mount', ' montagnes', '山脉', 'alic', 'ountains', '加拿大', 'informatics', 'bestos', 'imestone', '岗', '音标', '阿拉伯', 'verity', ' Geological', '本山', 'ugged', '矿', '译', 'ographical', 'haupt', ' ув', '登山', ' geological', '俱乐部', '聘', '_MOUNT', 'Mountain']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased0.5 plain24: [' mountains', ' mountain', ' Mountains', '山峰', ' montaña', 'mount', ' montagnes', '山脉', 'alic', 'ountains', '加拿大', 'informatics', 'bestos', 'imestone', '阿拉伯', '岗', '音标', 'verity', '本山', 'ugged', ' Geological', '矿', 'haupt', 'ographical', '俱乐部', '登山', ' ув', '译', '_MOUNT', ' montagna', 'Mountain', '聘']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', '山脉', '山峰', 'ountains', 'Mountain', ' hill', 'mount', 'Mount', ' núi', '山之', '峰', ' montagnes', 'OUNT', ' montaña', '山的', ' hills', ' Mountain', ' Peak', 'Peak', ' mount', ' slopes', ' хол', 'เนิน', '山体', ' склон', '山', '_MOUNT', ' Alps', ' montagne', 'ensus']

Input: 'Deutsch: "Haus" - Русский: "дом"\nDeutsch: "Macht" - Русский: "власть"\nDeutsch: "Linie" - Русский: "линия"\nDeutsch: "Schule" - Русский: "школа"\nDeutsch: "Berg" - Русский: "'

Baseline: 'горы"\nDeutsch: "W'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', '山脉', '山峰', 'ountains', 'Mountain', 'mount', ' hill', 'Mount', ' núi', '山之', '峰', ' montagnes', ' montaña', '山的', 'OUNT', ' Mountain', ' hills', ' mount', 'Peak', ' хол', ' Peak', '_MOUNT', '山体', ' montagne', 'เนิน', ' slopes', ' Alps', ' склон', '山', ' montagna']

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

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased1 J-lens: [' heart', ' hearts', 'heart', '心脏', '-heart', ' Heart', 'Heart', '的心脏', ' corazón', ' heartbeat', ' Hearts', ' coração', ' Herzen', ' cuore', '心臟', ' قلب', '心跳', ' cœur', 'heartbeat', ' cardiac', '心肺', ' heartfelt', ' القلب', '心肌', '-hearted', '的心', ' ❤', ' cardi', ' myocard', '心房', 'قلب', '❤']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased0.5 J-lens: [' heart', ' hearts', 'heart', '-heart', '心脏', ' Heart', 'Heart', '的心脏', ' corazón', ' heartbeat', ' Hearts', ' coração', ' Herzen', ' cuore', '心臟', ' قلب', '心跳', ' cœur', 'heartbeat', ' cardiac', '心肺', ' heartfelt', ' القلب', '心肌', '-hearted', '的心', ' coeur', 'قلب', '心房', ' ❤', '❤', '♡']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased1 plain24: [' heart', 'heart', '心脏', ' Heart', 'Heart', '的心脏', ' hearts', ' قلب', ' corazón', 'قلب', '-heart', ' القلب', '心的', ' Hearts', ' cœur', ' heartbeat', '心', '的心', ' cuore', '一颗', 'heartbeat', '心臟', '这颗', ' καρ', ' centrum', '心脏病', ' Herzen', ' cardiac', 'หัวใจ', ' coração', '心和', '-hearted']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased0.5 plain24: [' heart', 'heart', '心脏', ' Heart', 'Heart', '的心脏', ' hearts', ' قلب', ' corazón', 'قلب', '-heart', ' القلب', '心的', ' Hearts', ' cœur', ' heartbeat', '心', '的心', ' cuore', 'heartbeat', '心臟', '一颗', '这颗', ' καρ', ' centrum', ' Herzen', '心脏病', ' cardiac', 'หัวใจ', ' coração', '心和', '-hearted']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased1 plain27: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '心脏', '-heart', '心的', ' قلب', '心', '的心', ' corazón', '的心脏', ' coração', ' Hearts', ' cœur', ' القلب', '心和', ' heartbeat', 'หัวใจ', '-hearted', 'قلب', ' cardiac', 'heartbeat', '心跳', '心脏病', ' cuore', '心臟', '之心', ' Herzen', ' καρ', ' jantung']

Input: 'Deutsch: "Geschwindigkeit" - Русский: "скорость"\nDeutsch: "Sommer" - Русский: "лето"\nDeutsch: "Schönheit" - Русский: "красота"\nDeutsch: "Gesetz" - Русский: "закон"\nDeutsch: "Herz" - Русский: "'

Baseline: 'сердце"\nDeutsch: "'

end-pass erased0.5 plain27: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '心脏', '-heart', '心的', ' قلب', '的心', '心', ' corazón', '的心脏', ' coração', ' Hearts', ' cœur', ' القلب', '心和', 'หัวใจ', ' heartbeat', '-hearted', 'قلب', 'heartbeat', ' cardiac', '心臟', ' cuore', '心脏病', '心跳', '之心', ' Herzen', ' καρ', ' jantung']

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

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased1 J-lens: [' stars', ' star', ' Stars', 'stars', 'star', '-stars', 'Stars', '-star', '/star', ' Star', '星星', '星', '星辰', ' aster', '之星', ' estrella', ' звезды', 'Star', ' звезда', ' estrellas', '_star', '恒星', '星的', '-Star', ' celestial', '.star', '星座', ' STAR', ' estrel', ' étoiles', ' stella', '颗星']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased0.5 J-lens: [' stars', ' star', ' Stars', 'stars', 'star', '-stars', 'Stars', '-star', '/star', ' Star', '星星', '星', ' aster', '星辰', '之星', ' звезды', ' estrella', 'Star', ' звезда', ' estrellas', '-Star', '恒星', '星的', '_star', ' celestial', '.star', '星座', ' STAR', ' estrel', ' étoiles', ' stella', '颗星']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased1 plain24: [' stars', ' star', '星', ' Stars', 'stars', '-stars', '星的', '星座', ' celestial', 'Stars', ' Star', ' Sternen', ' aster', '.star', '星辰', ' Astronomy', '恒星', '之星', ' astronomers', ' estrellas', ' звезд', ' نجوم', '星星', ' Bintang', ' звезды', ' bintang', ' звезда', ' Stellar', '星级', 'Star', ' stellar', 'star']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased0.5 plain24: [' stars', ' star', '星', ' Stars', 'stars', '-stars', '星的', '星座', ' celestial', 'Stars', ' Star', ' Sternen', ' aster', '.star', '星辰', ' Astronomy', ' astronomers', '恒星', '之星', ' estrellas', ' звезд', ' Bintang', ' نجوم', '星星', ' звезды', ' bintang', ' звезда', 'Star', ' Stellar', '星级', ' stellar', 'star']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased1 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'Star', 'stars', 'star', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' звезд', ' STAR', '/star', ' звезды', '之星', ' звезда', ' aster', '恒星', ' bintang', 'STAR', '明星', ' starred', ' estrellas', '星级', ' stellar', '星辰']

Input: 'Deutsch: "Stamm" - Русский: "племя"\nDeutsch: "drei" - Русский: "три"\nDeutsch: "Maschine" - Русский: "машина"\nDeutsch: "Gesicht" - Русский: "лицо"\nDeutsch: "Stern" - Русский: "'

Baseline: 'звезда"\nDeutsch: "'

end-pass erased0.5 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'Star', 'stars', 'star', '-star', 'Stars', '_star', '星星', '.star', '-stars', '-Star', ' звезд', ' STAR', '/star', ' звезды', '之星', ' звезда', ' aster', ' bintang', 'STAR', '恒星', ' estrellas', ' starred', '明星', '星级', ' stellar', ' estrel']

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

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased1 J-lens: [' Books', ' books', ' book', '书籍', ' Book', 'books', 'book', 'Books', ' BOOK', '一本书', '-books', ' buku', '书本', ' книги', '书的', '书', ' libro', 'Book', '-book', '/books', ' booklet', '图书', '/book', ' Bücher', ' Libro', ' bookstore', ' kitap', ' libri', ' Library', 'BOOK', ' کتاب', ' Bible']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased0.5 J-lens: [' Books', ' books', ' book', '书籍', ' Book', 'books', 'book', 'Books', ' BOOK', '一本书', '-books', ' buku', '书的', '书本', ' книги', '书', '-book', 'Book', ' libro', '/books', '/book', ' Bücher', ' booklet', 'BOOK', '图书', ' Libro', ' kitap', ' bookstore', '_book', ' libri', ' Buku', ' کتاب']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased1 plain24: [' books', '书籍', ' book', '加拿大', '一本书', ' BOOK', '册', '书记', '课外', '-books', 'unread', ' книги', '书', '阿拉伯', ' книге', '一本', ' książ', '图书', '书的', '这本书', '公司债券', ' Books', ' audi', ' lent', '书本', '心爱的', ' الكتاب', '/books', ' knih', '书房', '�', ' quyển']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased0.5 plain24: [' books', '书籍', ' book', '加拿大', '一本书', ' BOOK', '-books', '书记', '册', ' книги', '阿拉伯', '书', 'unread', ' книге', ' książ', '课外', '书的', '一本', '图书', '这本书', ' Books', '书本', '公司债券', '/books', ' الكتاب', ' audi', ' knih', '书房', ' lent', '心爱的', ' quyển', ' kitap']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased1 plain27: [' books', ' book', ' Book', '书', '书籍', '这本书', ' Books', ' BOOK', '一本书', 'Book', 'book', '书的', 'books', ' книги', '书本', '-books', '图书', '_book', ' книге', 'Books', '一本', '書', '书中', '/books', 'BOOK', '的书', ' 책', '-book', '书中的', ' buku', '/book', '.book']

Input: 'Русский: "десять" - Deutsch: "zehn"\nРусский: "речь" - Deutsch: "Rede"\nРусский: "часть" - Deutsch: "Teil"\nРусский: "сердце" - Deutsch: "Herz"\nРусский: "книга" - Deutsch: "'

Baseline: 'Buch"\nРусский: "м'

end-pass erased0.5 plain27: [' books', ' book', ' Book', '书', '书籍', ' Books', '这本书', ' BOOK', 'Book', 'book', '一本书', '书的', 'books', ' книги', '书本', '-books', '_book', 'Books', ' книге', '图书', '书中', '/books', '書', 'BOOK', '的书', '一本', '-book', '书中的', ' 책', '.book', '/book', ' buku']

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

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased1 J-lens: [' Cloud', ' clouds', 'cloud', ' cloud', 'Cloud', '-cloud', '_cloud', '/cloud', '.cloud', '云层', '雲', '云的', '云朵', '云服务', ' nube', '云', '.Cloud', '云端', '云计算', '的云', '云平台', '云彩', ' 클라우드', '云雾', 'クラウド', '云海', ' cloudy', '云中', '雲端', ' mây', '乌云', ' iCloud']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased0.5 J-lens: [' Cloud', ' clouds', 'cloud', 'Cloud', ' cloud', '-cloud', '_cloud', '/cloud', '.cloud', '云层', '雲', '云的', '云朵', '云服务', ' nube', '云', '.Cloud', '云端', '云计算', '的云', '云平台', '云彩', ' 클라우드', '云雾', '云海', 'クラウド', ' cloudy', '云中', '雲端', ' mây', '乌云', ' iCloud']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased1 plain24: ['云', ' cloud', ' Cloud', ' clouds', 'Cloud', 'cloud', '云计算', '云服务', '/cloud', '云层', '_cloud', '云彩', '云端', '.cloud', '-cloud', '云朵', '云的', '雲', '云雾', ' cloudy', '云平台', '的云', ' 클라우드', 'クラウド', '.Cloud', '天空', ' mây', '云中', '云上', '多云', ' nube', '工业协会']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased0.5 plain24: ['云', ' cloud', ' Cloud', ' clouds', 'Cloud', 'cloud', '云计算', '云服务', '/cloud', '云层', '_cloud', '云彩', '云端', '.cloud', '-cloud', '云朵', '云的', '雲', '云雾', ' cloudy', '云平台', '的云', ' 클라우드', 'クラウド', '.Cloud', '天空', ' mây', '云中', '云上', '多云', ' nube', '工业协会']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased1 plain27: ['云', ' cloud', ' Cloud', ' clouds', 'cloud', 'Cloud', '雲', '云的', '-cloud', '_cloud', '云计算', '云彩', '/cloud', '云端', '云层', '云朵', '.cloud', '云服务', '云雾', '的云', ' cloudy', '云平台', '.Cloud', '云中', 'クラウド', ' 클라우드', ' nube', ' mây', '云上', '云天', '云服务器', '云飞']

Input: 'Русский: "сетка" - Deutsch: "Netz"\nРусский: "цвет" - Deutsch: "Farbe"\nРусский: "биржа" - Deutsch: "Börse"\nРусский: "полоса" - Deutsch: "Streifen"\nРусский: "облако" - Deutsch: "'

Baseline: 'Wolke"\nРусский:'

end-pass erased0.5 plain27: ['云', ' cloud', ' Cloud', ' clouds', 'cloud', 'Cloud', '雲', '云的', '-cloud', '_cloud', '云计算', '云彩', '/cloud', '云层', '云端', '云朵', '.cloud', '云服务', '云雾', '的云', ' cloudy', '云平台', '.Cloud', '云中', ' 클라우드', 'クラウド', ' nube', ' mây', '云上', '云天', '云服务器', '云飞']

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

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased1 J-lens: [' suitcase', ' luggage', ' Bags', ' bags', '书包', ' backpack', 'Bags', 'bags', ' pouch', ' Backpack', '钱包', ' baggage', ' bag', 'bag', '袋子', '行李箱', '背包', 'uggage', '箱包', ' Tasche', ' tote', '行李', 'Bag', ' Wallet', 'กระเป๋า', ' Bag', ' purse', '-pocket', ' 가방', '包包', '口袋', '挎']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased0.5 J-lens: [' suitcase', ' luggage', ' Bags', ' bags', '书包', ' backpack', 'Bags', 'bags', ' pouch', ' Backpack', '钱包', ' baggage', ' bag', 'bag', '袋子', '行李箱', '背包', 'uggage', '箱包', ' Tasche', ' tote', '行李', 'Bag', ' Bag', ' purse', ' Wallet', '-pocket', ' 가방', 'กระเป๋า', '口袋', '挎', '包包']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased1 plain24: ['加拿大', ' bag', 'Summer', ' sum', ' bags', ' recept', '手提', ' tote', ' suma', '..........', ' kul', '收纳', 'uggage', ',sum', ' kau', ' kont', 'inne', ' gab', ' tut', '书包', 'eves', ' sung', '种类繁多', '随身携带', ' prakt', ' Summer', ' bef', 'informatics', ' carried', ' carrying', 'いだ', ' fundament']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased0.5 plain24: ['加拿大', ' bag', 'Summer', ' sum', ' bags', ' recept', ' tote', '手提', ' suma', '..........', ' kul', ',sum', 'uggage', '收纳', ' kau', 'inne', ' kont', 'eves', '书包', '种类繁多', ' gab', ' tut', '随身携带', ' sung', 'informatics', ' prakt', ' Summer', ' bef', 'いだ', ' fundament', '負擔', ' carried']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased1 plain27: [' bag', ' bags', ' Bag', 'Bag', ' Bags', '袋', ' BAG', 'bags', 'bag', '袋子', ' backpack', 'Bags', ' moch', '_bag', ' purse', ' tote', ' bols', 'กระเป๋า', ' sack', ' túi', ' tas', ' Backpack', '背包', '手提', ' luggage', 'Wallet', '背', ' baggage', '书包', '钱包', '口袋', '囊']

Input: 'Русский: "человек" - Deutsch: "Person"\nРусский: "дверь" - Deutsch: "Tür"\nРусский: "провинция" - Deutsch: "Provinz"\nРусский: "шесть" - Deutsch: "sechs"\nРусский: "сумка" - Deutsch: "'

Baseline: 'Tasche"\nРусский:'

end-pass erased0.5 plain27: [' bag', ' bags', ' Bag', 'Bag', ' Bags', '袋', ' BAG', 'bags', 'bag', '袋子', ' backpack', 'Bags', ' moch', '_bag', ' purse', ' tote', ' bols', ' sack', 'กระเป๋า', ' túi', ' tas', '背包', ' Backpack', '手提', '背', ' luggage', ' baggage', 'Wallet', '书包', '钱包', '囊', '口袋']

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

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased1 J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', ' Teeth', '口腔', '-mouth', ' рта', ' throat', '嘴巴', '喉咙', ' Tooth', ' teeth', ' palate', ' cheeks', ' mulut', ' Nose', ' boca', ' nose', ' Ruhr', 'roat', ' jaw', ' tongue', ' pores', ' genitals', ' lips', 'lips', '鼻子', '鼻孔', '牙齿', '舌头', ' tooth']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased0.5 J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', ' Teeth', '口腔', '-mouth', ' throat', ' рта', '嘴巴', '喉咙', ' Tooth', ' teeth', ' palate', ' cheeks', ' nose', ' jaw', ' tongue', ' boca', ' Nose', ' mulut', ' Ruhr', ' pores', 'roat', ' genitals', ' lips', '鼻子', ' tooth', '牙齿', '鼻孔', '咽喉', '舌头']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased1 plain24: [' mouth', ' rot', 'mouth', ' Mouth', ' roh', '膛', '口腔', '聘', ' рта', ' porti', '-mouth', ' rö', '口', '的口', ' råd', ' مخاط', '嘴巴', '一口', '_exports', '口才', ' fundament', 'fang', ' rut', '嘴', '口红', 'phinx', ' hör', '旋转', ' būt', '[…', '轮流', '口中的']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased0.5 plain24: [' mouth', ' rot', 'mouth', ' roh', ' Mouth', '膛', '口腔', ' рта', ' porti', '聘', '-mouth', ' rö', '的口', ' råd', '口', ' مخاط', '嘴巴', '一口', '_exports', '口才', ' fundament', 'fang', ' rut', '[…', '口红', '嘴', 'phinx', ' būt', ' hör', '口中的', '旋转', '轮流']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased1 plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '嘴巴', ' mouths', '-mouth', '口的', '口腔', '的口', ' oral', ' рта', '口中的', '口中', ' bocca', ' boca', '开口', ' Oral', '张嘴', '口の', ' miệng', ' mulut', '张口', ' bouche', '口に', '口红', ' orale', '口水', '嘴里', '嘴边', 'emouth']

Input: 'Русский: "удалить" - Deutsch: "löschen"\nРусский: "версия" - Deutsch: "Version"\nРусский: "друг" - Deutsch: "Freund"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "рот" - Deutsch: "'

Baseline: 'Mund"\nРусский: "'

end-pass erased0.5 plain27: [' mouth', '口', '嘴', 'mouth', ' Mouth', '嘴巴', ' mouths', '口的', '-mouth', '口腔', ' oral', '的口', ' рта', '口中', '口中的', ' bocca', ' boca', '开口', ' Oral', '张嘴', '口の', ' miệng', ' mulut', '张口', ' bouche', '口に', '口红', ' orale', '嘴里', '口水', '嘴边', '一口']

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

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased1 J-lens: ['土壤', ' soil', ' Soil', ' soils', '土壤中', ' Terrain', ' почвы', '泥土', ' почву', ' terrain', ' Dirt', '土层', 'terrain', '沃土', ' tanah', 'Earth', 'ground', ' خاک', ' terreno', 'Terrain', '土的', ' suolo', 'Ground', '土地', ' Boden', ' suelo', ' tierra', '的土地', '岩土', ' Erde', '土方', ' dirt']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased0.5 J-lens: ['土壤', ' soil', ' Soil', ' soils', '土壤中', ' Terrain', ' почвы', '泥土', ' почву', ' terrain', ' Dirt', '土层', 'terrain', ' tanah', '沃土', 'Earth', 'ground', ' خاک', ' terreno', ' suolo', 'Terrain', '土的', '土地', 'Ground', ' Boden', ' tierra', ' suelo', ' dirt', '的土地', '岩土', ' Erde', '土方']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased1 plain24: [' soil', '土壤', ' Soil', ' soils', ' почвы', ' почву', '土', '脚下的', ' tanah', '泥土', ' terrain', '土地', ' Dirt', '地表', '土壤中', ' đất', ' ground', '土层', '表层', 'ดิน', ' land', ' Terrain', '土的', ' 토', '沃土', '基质', ' zem', '地基', '地面', ' lands', ' suelo', '_so']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased0.5 plain24: [' soil', '土壤', ' Soil', ' soils', ' почвы', ' почву', '土', '脚下的', ' tanah', '泥土', ' terrain', ' Dirt', '土地', '土壤中', '地表', ' đất', '土层', '表层', 'ดิน', ' ground', ' land', '土的', ' Terrain', ' 토', '沃土', '基质', ' zem', '地基', '_so', ' suelo', '土石', '地面']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased1 plain27: [' soil', '土壤', ' Soil', ' soils', '土', ' tanah', '土壤中', ' почвы', '泥土', ' ground', ' suelo', ' đất', '土的', ' почву', 'ดิน', ' Boden', ' earth', ' Ground', '土层', 'ground', ' terre', ' suelos', 'Ground', '土地', '地面', ' خاک', ' suolo', ' Earth', ' 토', ' грунта', ' Đất', ' грунт']

Input: 'Русский: "нога" - Deutsch: "Fuß"\nРусский: "река" - Deutsch: "Fluss"\nРусский: "восток" - Deutsch: "Osten"\nРусский: "сетка" - Deutsch: "Gitter"\nРусский: "почва" - Deutsch: "'

Baseline: 'Boden"\nРусский: "'

end-pass erased0.5 plain27: [' soil', '土壤', ' Soil', ' soils', '土', ' tanah', '土壤中', ' почвы', '泥土', ' ground', ' suelo', ' đất', '土的', 'ดิน', ' почву', ' Boden', ' earth', ' Ground', '土层', 'ground', ' terre', '土地', 'Ground', ' suelos', '地面', ' خاک', ' suolo', ' Earth', ' 토', ' грунта', ' Đất', ' грунт']

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

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased1 J-lens: [' Mountains', ' mountains', ' mountain', ' Mountain', 'mount', 'Mountain', '山峰', ' montaña', ' hills', ' montagne', ' Alps', ' montagnes', '山脉', ' gunung', ' горы', 'Mount', '山的', ' Mount', '山体', ' montagna', ' hill', '的山', ' Peaks', '山地', 'ภูเขา', '-mount', ' volcano', ' جبل', '名山', ' Gunung', ' Hills', ' núi']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased0.5 J-lens: [' Mountains', ' mountains', ' mountain', ' Mountain', 'mount', 'Mountain', '山峰', ' hills', ' montaña', ' montagne', '山脉', ' Alps', ' montagnes', ' gunung', 'Mount', ' горы', '山的', ' Mount', ' hill', '山体', ' montagna', '的山', '山地', ' Peaks', 'ภูเขา', '-mount', ' volcano', ' جبل', ' Gunung', ' núi', ' Hills', '名山']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased1 plain24: [' mountains', '加拿大', ' mountain', ' montaña', '山峰', ' Mountains', 'Mount', ' справед', ' hör', '吼', 'aurus', '峰', 'mener', '阿拉伯', '_MOUNT', ' horn', '升起', 'mount', ' Geological', 'ountains', 'peater', ' naud', ' hill', '姆斯', '发卡', ' hil', '上山', 'imestone', ' Mounted', '卖点', ' mitochond', '一点儿']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased0.5 plain24: [' mountains', '加拿大', ' mountain', ' montaña', '山峰', ' Mountains', 'Mount', ' справед', ' hör', 'mener', '阿拉伯', 'aurus', '吼', '峰', '_MOUNT', '升起', 'mount', ' horn', 'ountains', ' Geological', 'peater', ' naud', '姆斯', ' hill', '发卡', ' hil', ' Mounted', 'imestone', '上山', ' truk', '一点儿', '卖点']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', '峰', 'Mountain', 'Mount', '山峰', ' Peak', ' Mountain', ' núi', ' montaña', ' Mount', 'Peak', ' горы', 'mount', ' mount', ' hill', '加拿大', ' mitochond', ' Alps', '山大', 'ountains', ' montagne', '山之', ' peak', ' peaks', '山脉', 'OUNT', ' hil', '山的', 'ภูเขา', '山上']

Input: 'Русский: "дом" - Deutsch: "Haus"\nРусский: "власть" - Deutsch: "Macht"\nРусский: "линия" - Deutsch: "Linie"\nРусский: "школа" - Deutsch: "Schule"\nРусский: "гора" - Deutsch: "'

Baseline: 'Berg"\nРусский: "'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', '峰', 'Mountain', 'Mount', '山峰', ' Mountain', ' Peak', ' núi', ' montaña', ' Mount', 'Peak', ' горы', 'mount', ' hill', ' mount', ' mitochond', ' Alps', '加拿大', '山大', 'ountains', ' peak', ' peaks', ' montagne', '山脉', '山之', 'OUNT', '山的', ' hil', 'ภูเขา', '山上']

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

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased1 J-lens: [' Heart', '心脏', 'heart', 'Heart', ' heart', ' hearts', '的心脏', ' Hearts', ' corazón', '-heart', ' сердца', ' coração', '心臟', ' cuore', ' قلب', '心跳', ' cœur', 'heartbeat', ' heartbeat', '心肺', ' القلب', '心脏病', 'หัวใจ', 'card', '的心', '心', ' coeur', '心率', '-hearted', ' serca', 'قلب', ' jantung']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased0.5 J-lens: [' Heart', '心脏', 'heart', 'Heart', ' hearts', '的心脏', ' heart', ' Hearts', ' corazón', '-heart', ' сердца', ' coração', '心臟', ' cuore', ' قلب', '心跳', ' cœur', 'heartbeat', ' heartbeat', '心肺', ' القلب', '心脏病', 'หัวใจ', ' coeur', '的心', 'card', '心率', '心', ' jantung', ' serca', 'قلب', '-hearted']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased1 plain24: [' heart', '的心脏', ' Heart', 'heart', '心脏', ' сердца', 'Heart', ' corazón', ' hearts', 'قلب', ' القلب', ' قلب', '心', '-heart', '的心', ' centrum', '心的', '心率', '一颗', ' cœur', 'heartbeat', '心跳', ' Hearts', ' καρ', ' сердечно', '全心全意', '这颗', '心臟', '-hearted', '心脏病', ' coração', 'หัวใจ']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased0.5 plain24: [' heart', ' Heart', '的心脏', 'heart', '心脏', ' сердца', 'Heart', ' corazón', ' hearts', 'قلب', ' القلب', ' قلب', '心', '-heart', '的心', ' centrum', '心的', '心率', '一颗', ' cœur', 'heartbeat', ' Hearts', '心跳', ' καρ', '全心全意', '这颗', ' сердечно', '心臟', '-hearted', '心脏病', ' coração', 'หัวใจ']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased1 plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', ' قلب', '的心', ' сердца', ' corazón', '心的', '的心脏', ' cœur', '-hearted', ' Hearts', 'قلب', 'หัวใจ', ' القلب', ' coração', '心跳', ' hart', ' cardiac', ' heartbeat', '心和', '心脏病', ' cuore', '之心', ' καρ', '心臟', 'heartbeat']

Input: 'Русский: "скорость" - Deutsch: "Geschwindigkeit"\nРусский: "лето" - Deutsch: "Sommer"\nРусский: "красота" - Deutsch: "Schönheit"\nРусский: "закон" - Deutsch: "Gesetz"\nРусский: "сердце" - Deutsch: "'

Baseline: 'Herz"\nРусский: "'

end-pass erased0.5 plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', ' قلب', '的心', ' сердца', ' corazón', '心的', '的心脏', ' cœur', '-hearted', ' Hearts', 'قلب', 'หัวใจ', ' القلب', ' coração', '心跳', ' hart', ' cardiac', ' heartbeat', '心和', '心脏病', ' cuore', '之心', ' καρ', '心臟', 'heartbeat']

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

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased1 J-lens: [' Stars', ' stars', ' star', 'stars', 'Stars', 'star', '-stars', ' Star', '星星', '-star', '星辰', ' звезды', '/star', '_star', 'Star', '-Star', '星', ' estrella', '星光', '星的', '之星', ' estrellas', '明星', '.star', '恒星', '星空', ' stella', ' bintang', ' estrelas', '颗星', ' stelle', ' Stard']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased0.5 J-lens: [' Stars', ' stars', ' star', 'stars', 'star', 'Stars', '-stars', ' Star', '星星', '-star', '星辰', ' звезды', '/star', '_star', 'Star', '-Star', '星', ' estrella', '星光', '星的', '之星', ' estrellas', '恒星', '明星', '.star', '星空', ' stella', ' bintang', ' estrelas', '颗星', ' stelle', ' Stard']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased1 plain24: [' stars', ' star', '星', ' Stars', '星的', ' Star', '-stars', 'stars', '_star', 'star', '星辰', '.star', '星座', 'Stars', 'Star', '星星', ' звезды', '-star', '星光', ' starred', ' stellar', ' bintang', ' celestial', '恒星', ' نجوم', ' Astroph', ' aster', '明星', '颗星', '/star', '星级', ' estrellas']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased0.5 plain24: [' stars', ' star', '星', ' Stars', '星的', '-stars', ' Star', 'stars', '_star', 'star', '星辰', '.star', '星座', 'Stars', 'Star', '星星', ' звезды', '-star', '星光', ' starred', ' bintang', ' نجوم', ' stellar', ' celestial', '恒星', ' Astroph', ' aster', '颗星', '/star', '明星', ' estrellas', '星级']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased1 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '_star', 'stars', '-star', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезды', '明星', ' STAR', ' bintang', '星光', '恒星', ' stellar', '之星', ' starred', '星级', ' aster', 'STAR', ' estrellas', '星辰', '_STAR']

Input: 'Русский: "племя" - Deutsch: "Stamm"\nРусский: "три" - Deutsch: "drei"\nРусский: "машина" - Deutsch: "Maschine"\nРусский: "лицо" - Deutsch: "Gesicht"\nРусский: "звезда" - Deutsch: "'

Baseline: 'Stern"\nРусский: "'

end-pass erased0.5 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '_star', 'stars', '-star', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезды', '明星', ' STAR', ' bintang', '星光', '恒星', ' stellar', '之星', ' starred', '星级', ' aster', 'STAR', ' estrellas', '星辰', '_STAR']

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

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased1 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '/cloud', '云层', '_cloud', '.cloud', '雲', ' nube', '云的', '云', '云朵', ' обла', '的云', '.Cloud', ' cloudy', '云彩', '云雾', '云服务', '云端', ' mây', '云海', '乌云', '云计算', '云平台', '云中', ' 클라우드', 'クラウド', ' Обла']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased0.5 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '云层', '/cloud', '_cloud', '.cloud', '雲', ' nube', '云的', '云', '云朵', ' обла', '的云', ' cloudy', '.Cloud', '云彩', '云雾', '云服务', '云端', ' mây', '云海', '乌云', '云计算', '云平台', '云中', ' 클라우드', 'クラウド', ' Обла']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased1 plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', ' обла', '云彩', '/cloud', '_cloud', '云层', '-cloud', '云计算', '云的', '雲', '.cloud', '的云', '云朵', '云服务', ' cloudy', '云端', '.Cloud', ' mây', ' 클라우드', 'クラウド', ' nube', '云雾', '天气', '云中', '天空', '云山', '云平台']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased0.5 plain24: ['云', ' clouds', ' cloud', 'cloud', 'Cloud', ' Cloud', ' обла', '云彩', '/cloud', '_cloud', '-cloud', '云层', '云计算', '云的', '雲', '.cloud', '的云', '云朵', '云服务', ' cloudy', '云端', '.Cloud', ' mây', ' 클라우드', 'クラウド', ' nube', '云雾', '天气', '云中', '天空', '云山', '云平台']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased1 plain27: ['云', ' cloud', ' Cloud', ' clouds', 'cloud', 'Cloud', '雲', '云的', '-cloud', '_cloud', '云彩', ' обла', '/cloud', '云层', '的云', '云朵', '云计算', '.cloud', '云端', ' cloudy', '云雾', '.Cloud', '云服务', '云平台', ' mây', '云中', ' nube', ' 클라우드', '云飞', '云天', 'クラウド', '云上']

Input: 'Français: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "'

Baseline: 'Wolke"\nFrançais:'

end-pass erased0.5 plain27: ['云', ' cloud', ' Cloud', ' clouds', 'cloud', 'Cloud', '雲', '云的', '-cloud', '_cloud', '云彩', ' обла', '/cloud', '云层', '云朵', '的云', '云计算', '.cloud', ' cloudy', '云端', '云雾', '.Cloud', '云服务', '云平台', ' mây', '云中', ' nube', ' 클라우드', '云飞', '云天', 'クラウド', '云上']

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

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased1 J-lens: [' Bags', ' bags', '书包', '钱包', ' suitcase', '袋子', ' pouch', 'bags', ' bag', 'Bags', ' sack', ' sacks', ' Wallet', 'bag', ' wallet', ' luggage', '-pocket', ' pocket', '口袋', ' Bag', ' Taschen', ' Tasche', 'wallet', ' sacs', ' backpack', ' 가방', 'Bag', ' Basket', ' baggage', 'packet', ' Backpack', ' basket']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased0.5 J-lens: [' Bags', ' bags', '书包', '钱包', ' suitcase', '袋子', ' pouch', ' bag', 'bags', 'Bags', ' sack', ' sacks', 'bag', ' Wallet', ' wallet', ' luggage', '-pocket', ' pocket', ' Bag', '口袋', ' Taschen', ' Tasche', ' backpack', 'wallet', ' sacs', 'Bag', ' baggage', ' Basket', ' 가방', ' Backpack', ' basket', 'packet']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased1 plain24: ['加拿大', '袋子', ' recept', ' bag', '阿拉伯', '书包', ' bags', 'ISATION', ' sach', 'вершенство', '钱包', ' Saga', 'unread', 'OnChange', ' tut', 'Bags', ' Sachs', ' Bags', '随身携带', 'editary', ' plec', '一脸', ' рекв', ' prakt', '种类繁多', ' Adventure', 'verity', ' sak', 'reatest', ' виз', '-fashioned', '卖点']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased0.5 plain24: ['加拿大', '袋子', '阿拉伯', ' recept', ' bag', '书包', ' bags', 'ISATION', 'вершенство', ' sach', 'unread', ' Saga', '钱包', 'OnChange', 'Bags', ' Bags', ' tut', ' Sachs', '随身携带', ' plec', 'editary', ' рекв', '种类繁多', '一脸', ' prakt', 'verity', ' Adventure', 'reatest', ' sak', ' виз', ' bols', '卖点']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased1 plain27: [' bag', ' bags', '袋', '袋子', ' Bag', ' Bags', 'Bag', ' BAG', 'bags', 'bag', '口袋', ' túi', ' sack', 'Bags', '_bag', '钱包', 'Wallet', '布袋', ' purse', '购物', 'beutel', ' sacks', ' bols', ' wallet', '书包', ' pouch', ' moch', ' pocket', '囊', ' pockets', ' Wallet', 'กระเป๋า']

Input: 'Français: "thé" - Deutsch: "Tee"\nFrançais: "bourse" - Deutsch: "Börse"\nFrançais: "machine" - Deutsch: "Maschine"\nFrançais: "rue" - Deutsch: "Straße"\nFrançais: "sac" - Deutsch: "'

Baseline: 'Tasche"\nFrançais:'

end-pass erased0.5 plain27: [' bag', ' bags', '袋', '袋子', ' Bag', ' Bags', 'Bag', ' BAG', 'bags', 'bag', '口袋', ' túi', ' sack', 'Bags', '_bag', '钱包', 'Wallet', '布袋', ' purse', '购物', 'beutel', ' sacks', ' bols', ' wallet', '书包', ' pouch', ' moch', ' pocket', '囊', ' pockets', ' Wallet', ' sacs']

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

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased1 J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', '-mouth', '嘴巴', '口腔', ' boca', ' Teeth', '嘴', ' tongue', ' bocca', ' jaw', ' throat', ' mulut', ' lips', '舌头', ' jaws', ' teeth', ' cheeks', '喉咙', 'lips', '口语', ' saliva', ' palate', '牙齿', ' Speech', ' tongues', ' miệng', '口才', ' рта', '嘴唇']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased0.5 J-lens: [' Mouth', ' mouth', 'mouth', ' mouths', '-mouth', '嘴巴', '口腔', ' boca', ' Teeth', '嘴', ' tongue', ' bocca', ' jaw', ' throat', ' lips', ' mulut', ' jaws', ' teeth', '舌头', ' cheeks', '喉咙', '牙齿', '口语', ' saliva', ' palate', 'lips', ' Speech', ' tongues', '嘴唇', ' miệng', '口才', ' speech']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased1 plain24: [' mouth', '嘴', 'mouth', ' Mouth', '嘴巴', '口', '口腔', ' mouths', '-mouth', '开口', ' bocca', '口语', '一口', '的口', ' oral', '口才', ' spok', 'emouth', 'fang', '嘴边', '张嘴', '口头', '进出口', '姆斯', '出口', ' Oral', 'unciation', ' mulut', ' рта', '口区', ' Grimm', '口的']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased0.5 plain24: [' mouth', '嘴', 'mouth', ' Mouth', '嘴巴', '口', '口腔', ' mouths', '-mouth', '开口', ' bocca', '口语', '一口', '的口', ' oral', '口才', ' spok', 'emouth', 'fang', '嘴边', '张嘴', '口头', '进出口', '姆斯', '出口', ' Oral', 'unciation', ' mulut', ' рта', '口区', ' Grimm', '口的']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased1 plain27: [' mouth', '口', '嘴', ' Mouth', '嘴巴', 'mouth', ' mouths', '口的', '-mouth', '口腔', ' oral', '的口', ' boca', ' bocca', '口中', '开口', ' Oral', '张嘴', '嘴边', ' mulut', '口中的', ' miệng', '口の', ' рта', '张口', '嘴里', '口に', 'emouth', '口头', ' orale', '唇', '口水']

Input: 'Français: "ménage" - Deutsch: "Haushalt"\nFrançais: "pouvoir" - Deutsch: "Macht"\nFrançais: "cheval" - Deutsch: "Pferd"\nFrançais: "nord" - Deutsch: "Norden"\nFrançais: "bouche" - Deutsch: "'

Baseline: 'Mund"\nFrançais: "'

end-pass erased0.5 plain27: [' mouth', '口', '嘴', ' Mouth', '嘴巴', 'mouth', ' mouths', '口的', '-mouth', '口腔', ' oral', '的口', ' boca', ' bocca', '开口', '口中', ' Oral', '张嘴', '嘴边', ' mulut', ' miệng', '口中的', '口の', ' рта', '张口', '嘴里', '口に', '口头', 'emouth', '唇', ' orale', '嘴唇']

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

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased1 J-lens: [' soil', 'ground', 'floor', ' ground', '土壤', ' Soil', ' floor', ' pavement', ' suelo', '地板', ' Floor', ' Terrain', ' floors', ' flooring', ' Ground', 'surface', '地面', 'Ground', 'Floor', ' terrain', ' suolo', ' soils', ' surface', ' dirt', ' Floors', '土壤中', '-ground', ' Flooring', '地基', ' sidewalk', 'phalt', ' earth']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased0.5 J-lens: [' soil', 'ground', ' ground', 'floor', '土壤', ' Soil', ' floor', ' pavement', ' suelo', '地板', ' Floor', ' floors', ' Terrain', ' flooring', ' Ground', '地面', 'surface', 'Ground', ' terrain', 'Floor', ' suolo', ' soils', ' surface', ' dirt', '土壤中', ' Floors', '-ground', '地基', ' Flooring', ' sidewalk', ' earth', '地面的']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased1 plain24: [' soil', '脚下的', '_sol', '地面', ' ground', '土壤', ' сол', ' suelo', '脚下', '土地', ' fundament', ' sols', '地板', '混凝', ' floor', '太阳', '地基', '地砖', ' tanah', ' Flooring', ' pavement', 'floor', 'crete', '土', 'Floor', ' أرض', 'Ground', ' solving', ' Soil', '_solution', '地表', 'loor']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased0.5 plain24: [' soil', '脚下的', '_sol', '地面', ' ground', '土壤', ' сол', ' suelo', '脚下', ' fundament', ' sols', '土地', '地板', '混凝', '地基', '太阳', ' floor', ' Flooring', '地砖', ' tanah', 'floor', 'crete', ' pavement', 'Floor', ' أرض', 'Ground', '_solution', ' solving', '土', ' Soil', '地表', 'solver']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased1 plain27: [' ground', '地面', ' floor', ' Ground', 'ground', '地板', 'Ground', ' suelo', ' soil', ' Floor', 'floor', '地面的', 'Floor', '_ground', ' tanah', '土壤', ' Boden', ' floors', '土地', '-ground', ' terre', '地表', ' đất', '地面上', '地砖', ' Soil', ' Flooring', ' flooring', '在地上', ' grounds', '地板上', ' earth']

Input: 'Français: "sept" - Deutsch: "sieben"\nFrançais: "pont" - Deutsch: "Brücke"\nFrançais: "gare" - Deutsch: "Bahnhof"\nFrançais: "province" - Deutsch: "Provinz"\nFrançais: "sol" - Deutsch: "'

Baseline: 'Boden"\nFrançais: "'

end-pass erased0.5 plain27: [' ground', '地面', ' floor', ' Ground', 'ground', '地板', 'Ground', ' suelo', ' soil', ' Floor', 'floor', '地面的', 'Floor', ' tanah', '_ground', '土壤', ' Boden', ' floors', '土地', '-ground', ' terre', '地表', ' đất', '地面上', '地砖', ' Soil', ' Flooring', ' flooring', '在地上', ' grounds', '地板上', ' earth']

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

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased1 J-lens: [' mountains', ' mountain', ' Mountains', ' Mountain', 'mount', 'Mountain', ' montaña', ' montagnes', ' hills', '山脉', ' Alps', '山峰', 'Mount', ' montagna', ' Mount', ' mount', ' gunung', '-mount', ' hill', '山地', ' горы', ' volcano', '山区', '的山', '山的', ' Peaks', ' countryside', ' núi', '山体', 'ountain', ' جبل', ' Highlands']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased0.5 J-lens: [' mountains', ' mountain', ' Mountains', ' Mountain', 'mount', 'Mountain', ' montaña', ' montagnes', ' hills', '山脉', ' Alps', '山峰', 'Mount', ' montagna', ' Mount', ' mount', ' gunung', '-mount', ' hill', '山地', ' volcano', ' горы', '山区', '的山', '山的', ' Peaks', ' countryside', ' núi', '山体', 'ountain', ' Highlands', ' جبل']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased1 plain24: [' mountains', ' mountain', ' Mountains', 'mount', ' montaña', ' гор', '山峰', 'Mount', '加拿大', ' mount', ' montagnes', '山脉', 'Mountain', '_MOUNT', ' Mountain', 'ountains', '阿拉伯', '峰', ' 산', ' montagna', ' Alps', 'alic', '耸', '的山', '姆斯', '卖点', ' peaks', ' inland', '岩', 'OUNT', '�', ' gunung']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased0.5 plain24: [' mountains', ' mountain', ' Mountains', 'mount', ' montaña', 'Mount', '山峰', ' гор', '加拿大', ' mount', ' montagnes', '山脉', '_MOUNT', 'Mountain', ' Mountain', 'ountains', '阿拉伯', '峰', ' 산', ' montagna', ' Alps', 'alic', '耸', '姆斯', '的山', '卖点', 'OUNT', ' inland', ' peaks', '岩', '-mount', '�']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased1 plain27: [' mountains', ' Mountains', ' mountain', 'Mountain', ' Mountain', 'Mount', 'mount', ' núi', '峰', '山峰', ' montaña', ' гор', ' Peak', ' mount', ' горы', '山脉', ' Alps', ' Mount', 'ountains', 'Peak', ' Alp', '山的', ' montagnes', ' hill', '山大', ' peaks', '山人', 'OUNT', ' peak', 'ภูเขา', '山之', ' mitochond']

Input: 'Français: "loi" - Deutsch: "Gesetz"\nFrançais: "porte" - Deutsch: "Tür"\nFrançais: "est" - Deutsch: "Osten"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "montagne" - Deutsch: "'

Baseline: 'Berg"\nFrançais: "'

end-pass erased0.5 plain27: [' mountains', ' Mountains', ' mountain', 'Mountain', ' Mountain', 'Mount', 'mount', ' núi', '峰', '山峰', ' гор', ' montaña', ' Peak', ' mount', ' горы', '山脉', ' Alps', ' Mount', 'ountains', 'Peak', ' Alp', '山的', ' hill', ' montagnes', '山大', ' peaks', '山人', ' peak', 'OUNT', 'ภูเขา', '山之', ' mitochond']

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

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased1 J-lens: [' heart', ' Heart', 'heart', ' hearts', ' Hearts', '-heart', 'Heart', '心脏', '的心脏', ' corazón', ' coração', ' сердце', ' cuore', ' сердца', ' قلب', '心臟', ' heartbeat', ' серд', '心跳', 'heartbeat', ' coeur', '心肺', ' cardiac', ' heartfelt', ' القلب', '-hearted', '的心', ' Core', '❤', 'หัวใจ', ' jantung', '心肌']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased0.5 J-lens: [' Heart', ' heart', 'heart', ' hearts', ' Hearts', 'Heart', '-heart', '心脏', '的心脏', ' corazón', ' coração', ' сердце', ' cuore', ' сердца', ' قلب', '心臟', ' heartbeat', ' серд', '心跳', 'heartbeat', ' coeur', '心肺', ' heartfelt', ' cardiac', ' القلب', '❤', '-hearted', '的心', 'หัวใจ', ' Core', ' jantung', '心肌']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased1 plain24: [' heart', 'heart', ' Heart', ' hearts', 'Heart', '的心脏', '心脏', ' серд', ' сердце', '心', '心的', ' сердца', '的心', ' corazón', ' قلب', ' القلب', '-heart', ' Hearts', 'قلب', '心了', ' καρ', '心和', '心跳', '心头', '心脏病', '心率', 'heartbeat', '之心', '这颗', '心臟', ' coeur', 'หัวใจ']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased0.5 plain24: [' heart', 'heart', ' Heart', ' hearts', 'Heart', ' серд', '心脏', '的心脏', ' сердце', '心', '心的', '的心', ' corazón', ' сердца', ' قلب', '-heart', ' القلب', ' Hearts', 'قلب', '心了', '心和', ' καρ', '心跳', '心头', '心脏病', 'heartbeat', '心率', '之心', '这颗', 'หัวใจ', '心臟', ' coeur']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased1 plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', '的心', ' сердце', ' قلب', '心的', ' сердца', ' серд', ' corazón', '的心脏', ' Hearts', 'หัวใจ', ' القلب', '-hearted', ' coração', '心和', '心跳', ' hart', ' cardiac', ' καρ', 'قلب', '之心', ' cuore', ' heartbeat', '心了', '心脏病']

Input: 'Français: "plate-forme" - Deutsch: "Plattform"\nFrançais: "section" - Deutsch: "Abschnitt"\nFrançais: "fleur" - Deutsch: "Blume"\nFrançais: "genre" - Deutsch: "Art"\nFrançais: "cœur" - Deutsch: "'

Baseline: 'Herz"\nFrançais: "'

end-pass erased0.5 plain27: [' heart', ' Heart', 'heart', ' hearts', 'Heart', '-heart', '心脏', '心', '的心', ' сердце', ' قلب', '心的', ' сердца', ' серд', ' corazón', '的心脏', ' Hearts', 'หัวใจ', ' القلب', '-hearted', '心和', ' coração', '心跳', ' cardiac', ' καρ', 'قلب', ' hart', '之心', ' cuore', ' heartbeat', '心了', '心脏病']

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

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased1 J-lens: ['day', ' day', ' daytime', ' daylight', ' days', 'days', ' morning', 'Day', ' Day', '/day', '_day', ' mornings', '白天', 'Days', ' afternoon', ' Days', '-day', ' sunrise', ' journée', ' evening', '(day', ' DAY', ' nights', ' день', '-days', ' night', ' дня', ' днем', '.day', ' Morning', ' evenings', '_days']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased0.5 J-lens: ['day', ' day', ' daytime', ' daylight', 'Day', 'days', ' days', ' morning', ' Day', '/day', '_day', ' mornings', '白天', 'Days', ' afternoon', ' Days', '-day', ' sunrise', ' journée', ' evening', ' DAY', '(day', ' nights', ' день', '-days', ' днем', ' дня', ' night', '.day', 'DAY', ' Morning', '_days']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased1 plain24: ['day', ' day', ' daylight', '太阳', '加拿大', '姆斯', ' daytime', '天的', '阿拉伯', ' ημέ', '日光', ' дня', ' sun', '中午', '白天', '-day', ' scho', 'Day', ' days', '日生', '晴天', ' день', '一天的', ' Présent', ' النهار', '日', '日出', '日的', '青天', '_day', '阳光', '天空']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased0.5 plain24: ['day', ' day', ' daylight', '太阳', '加拿大', '姆斯', ' daytime', '天的', '阿拉伯', ' ημέ', '日光', ' дня', ' sun', '中午', '白天', '-day', ' scho', 'Day', ' days', '日生', '晴天', ' день', '一天的', ' Présent', ' النهار', '日', '日出', '日的', '青天', '_day', '阳光', '天空']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased1 plain27: [' day', 'day', '-day', ' Day', 'Day', '_day', ' DAY', ' days', '日', ' день', ' дня', ' dag', ' daylight', ' día', '日的', '.day', '-Day', '(day', '一天', ' daytime', '\tday', ' روز', ' ngày', 'Days', '天的', '一天的', '/day', 'DAY', '白天', '日子', ' giorno', '日照']

Input: 'Français: "un" - Deutsch: "eins"\nFrançais: "forêt" - Deutsch: "Wald"\nFrançais: "défaite" - Deutsch: "Niederlage"\nFrançais: "lune" - Deutsch: "Mond"\nFrançais: "jour" - Deutsch: "'

Baseline: 'Tag"\nFrançais: "m'

end-pass erased0.5 plain27: [' day', 'day', '-day', ' Day', 'Day', '_day', ' DAY', ' days', '日', ' день', ' дня', ' día', ' dag', ' daylight', '-Day', '日的', '.day', '(day', '一天', '\tday', ' daytime', ' روز', 'Days', '一天的', '天的', ' ngày', '/day', 'DAY', '白天', '日子', ' giorno', 'День']

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

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased1 J-lens: [' stars', ' star', ' Stars', 'star', 'stars', 'Stars', '-stars', '-star', ' Star', '星星', ' estrella', ' звезда', '/star', 'Star', '星辰', '星', ' звезды', '_star', '-Star', ' estrellas', '之星', '星光', ' aster', '星的', '.star', ' étoiles', ' estrel', ' stelle', ' estrelas', ' stella', '星标', '颗星']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased0.5 J-lens: [' stars', ' star', ' Stars', 'star', 'stars', 'Stars', '-stars', '-star', ' Star', '星星', ' estrella', ' звезда', '/star', 'Star', '星辰', '星', ' звезды', '_star', '-Star', ' estrellas', '之星', '星光', ' aster', '星的', '.star', ' étoiles', ' estrel', ' stelle', ' estrelas', ' stella', '星标', '颗星']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased1 plain24: [' stars', ' star', '星', ' Stars', 'stars', ' Star', '-stars', '星的', 'star', '.star', '_star', '星辰', 'Stars', 'Star', ' aster', '星星', '-star', ' stellar', '星光', ' звезд', ' estrellas', ' звезда', ' نجوم', ' звезды', '之星', ' starred', '颗星', ' bintang', ' stell', '星级', ' estrelas', ' 별']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased0.5 plain24: [' stars', ' star', '星', ' Stars', 'stars', '-stars', ' Star', '星的', '.star', 'star', '_star', '星辰', 'Stars', ' aster', '星星', 'Star', '-star', ' stellar', ' звезд', ' نجوم', '星光', ' estrellas', ' звезда', ' звезды', '之星', ' starred', '颗星', ' bintang', '星级', ' stell', '/star', ' estrelas']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased1 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '-star', '_star', 'stars', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезд', ' звезды', ' STAR', ' звезда', ' bintang', '明星', ' stellar', ' estrellas', '之星', '星光', 'STAR', '星级', ' aster', ' starred', '恒星']

Input: 'Français: "vertu" - Deutsch: "Tugend"\nFrançais: "quatre" - Deutsch: "vier"\nFrançais: "mille" - Deutsch: "tausend"\nFrançais: "cravate" - Deutsch: "Krawatte"\nFrançais: "étoile" - Deutsch: "'

Baseline: 'Stern"\nFrançais: "'

end-pass erased0.5 plain27: [' star', ' stars', '星', ' Star', ' Stars', '星的', 'star', 'Star', '-star', 'stars', '_star', '星星', 'Stars', '.star', '-stars', '-Star', '/star', ' звезд', ' звезды', ' STAR', ' звезда', ' bintang', '明星', ' stellar', ' estrellas', '星光', '之星', 'STAR', '星级', ' aster', ' starred', '恒星']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [plain lens](readout.json) | 32/48                  |    0.912 | 30/43                    | 32/48            |          2 |
| [J-lens](readout.json)     | 27/48                  |    0.912 | 24/43                    | 27/48            |          2 |

### End-of-pass readout (not for earlier edits)

| method                                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | literal joint↑   |   unscored |
|:-------------------------------------------|:-----------------------|---------:|:-------------------------|:-----------------|-----------:|
| [end-pass erased1 plain24](readout.json)   | 40/48                  |    0.945 | 36/43                    | 40/48            |          2 |
| [end-pass J-lens](readout.json)            | 39/48                  |    0.951 | 34/43                    | 39/48            |          2 |
| [end-pass plain24](readout.json)           | 39/48                  |    0.945 | 35/43                    | 39/48            |          2 |
| [end-pass erased1 J-lens](readout.json)    | 39/48                  |    0.947 | 34/43                    | 39/48            |          2 |
| [end-pass erased0.5 J-lens](readout.json)  | 39/48                  |    0.949 | 34/43                    | 39/48            |          2 |
| [end-pass erased0.5 plain24](readout.json) | 39/48                  |    0.946 | 35/43                    | 39/48            |          2 |
| [end-pass erased1 plain27](readout.json)   | 36/48                  |    0.954 | 31/43                    | 36/48            |          2 |
| [end-pass erased0.5 plain27](readout.json) | 36/48                  |    0.955 | 31/43                    | 36/48            |          2 |
| [end-pass plain27](readout.json)           | 33/48                  |    0.955 | 28/43                    | 33/48            |          2 |

### Translation development/test splits

| split   | method                     | joint↑   |   AUROC↑ |   unscored |
|:--------|:---------------------------|:---------|---------:|-----------:|
| dev     | J-lens                     | 4/8      |    0.947 |          1 |
| dev     | plain lens                 | 5/8      |    0.954 |          1 |
| dev     | end-pass J-lens            | 6/8      |    0.980 |          1 |
| dev     | end-pass plain24           | 6/8      |    0.977 |          1 |
| dev     | end-pass plain27           | 5/8      |    0.983 |          1 |
| dev     | end-pass erased1 J-lens    | 6/8      |    0.972 |          1 |
| dev     | end-pass erased0.5 J-lens  | 6/8      |    0.974 |          1 |
| dev     | end-pass erased1 plain24   | 6/8      |    0.973 |          1 |
| dev     | end-pass erased0.5 plain24 | 6/8      |    0.973 |          1 |
| dev     | end-pass erased1 plain27   | 5/8      |    0.980 |          1 |
| dev     | end-pass erased0.5 plain27 | 5/8      |    0.983 |          1 |
| test    | J-lens                     | 23/40    |    0.906 |          1 |
| test    | plain lens                 | 27/40    |    0.904 |          1 |
| test    | end-pass J-lens            | 33/40    |    0.946 |          1 |
| test    | end-pass plain24           | 33/40    |    0.940 |          1 |
| test    | end-pass plain27           | 28/40    |    0.950 |          1 |
| test    | end-pass erased1 J-lens    | 33/40    |    0.943 |          1 |
| test    | end-pass erased0.5 J-lens  | 33/40    |    0.944 |          1 |
| test    | end-pass erased1 plain24   | 34/40    |    0.940 |          1 |
| test    | end-pass erased0.5 plain24 | 33/40    |    0.941 |          1 |
| test    | end-pass erased1 plain27   | 31/40    |    0.950 |          1 |
| test    | end-pass erased0.5 plain27 | 31/40    |    0.950 |          1 |

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_125500_jlens-one-pass/run.md
