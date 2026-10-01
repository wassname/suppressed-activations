---
native_metric_erasure: true
boundary_readout: true
expand_input_prefix: true
chat_readout: true
readout_max_new_tokens: 32
gradient_pursuit: false
matching_pursuit: false
polar_readout: false
pool_question: false
verify_readout_run: out/2026-10-01_160913_jlens-one-pass
token_kl: false
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: /workspace/2026/suppressed-activations/data/english_boundary_readout_v1.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 13.10
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Logit contrast subtracts separately final-normalised vocabulary logits, retaining signed scores; probability contrast retains positive probability differences. Negative-final and cyclic mismatched-final scores are diagnostic controls. No generated text or labels enter these rankings. Input-prefix variants additionally exclude strings starting with an entire lowercased prompt word of length>=3. This is a new development mask, not semantic morphology: art also excludes article; the old nam/name exclusion remains. Labels and generated text do not construct the mask. Every addition and originating word is saved in input_prefix_exclusions.json; full original scores are in input_prefix_scores. Original methods are retained unchanged; cyclic mismatch controls are omitted in this specific test. SHOULD: surviving scores and all original rows remain unchanged; inspect replacement entries for semantic leaks. Postmask AUROC can be high merely because negative labels are masked; do not use it as evidence of country recovery. Original methods keep the same layer, k32 and prompt mask; additional variants are described above. Position rule is specified above (otherwise final only). Dataset's original selection history: Post2718 development test: first4 native-v4 cases; first de→fr and fr→de stored translation cases, both cloud. New explicit native translation wrapper. No output/first-hop filter, no v5; nuage scoreability limitation retained. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved continuation (cap32), ignoring punctuation; generation is scoring only. Native-chat mode uses thinking=False and add_generation_prompt=True, stops on tokenizer or model EOS, and excludes special tokens from scoring text only; the verbatim decoded continuation is preserved. Completion-mode defaults remain unchanged. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Replay runs reuse the cached continuations without generation. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC and remain in the full denominator. These are lexical passes, not a verified lower bound on semantic success. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                                                         | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:---------------------------------------------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| December  | J-lens                                                         | False         |          0.385     |             4 |                      6 | False          | False        |
| December  | plain lens                                                     | False         |          0.56      |         23975 |                  18708 | False          | False        |
| December  | end-pass J-lens                                                | True          |          1         |             4 |             1000000000 | True           | True         |
| December  | end-pass logit contrast J-lens                                 | False         |          1         |        185964 |             1000000000 | False          | False        |
| December  | end-pass probability contrast J-lens                           | True          |          0.75      |             4 |             1000000000 | True           | True         |
| December  | end-pass plain24                                               | False         |          1         |         23974 |             1000000000 | False          | False        |
| December  | end-pass logit contrast plain24                                | False         |          1         |        216561 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain24                          | False         |          0.65      |         25474 |             1000000000 | False          | False        |
| December  | end-pass plain27                                               | True          |          1         |             1 |             1000000000 | True           | True         |
| December  | end-pass logit contrast plain27                                | False         |          1         |        155635 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain27                          | True          |          0.9       |             1 |             1000000000 | True           | True         |
| December  | end-pass negative final control                                | False         |          1         |        239760 |             1000000000 | False          | False        |
| December  | end-pass erased1 J-lens                                        | False         |          1         |           101 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 J-lens                                      | True          |          1         |            18 |             1000000000 | True           | True         |
| December  | end-pass erased1 plain24                                       | False         |          1         |         20902 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain24                                     | False         |          1         |         22914 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain27                                       | True          |          1         |            11 |             1000000000 | True           | True         |
| December  | end-pass erased0.5 plain27                                     | True          |          1         |             8 |             1000000000 | True           | True         |
| December  | end-pass input-prefix erased0.5 J-lens                         | True          |          1         |            13 |             1000000000 | True           | True         |
| December  | end-pass input-prefix erased0.5 plain24                        | False         |          1         |         22841 |             1000000000 | False          | False        |
| December  | end-pass input-prefix erased0.5 plain27                        | True          |          1         |             8 |             1000000000 | True           | True         |
| December  | end-pass input-prefix J-lens                                   | True          |          1         |             1 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix J-lens                          | True          |          1         |             0 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix erased0.5 J-lens                | True          |          1         |             2 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix erased0.5 plain24               | False         |          1         |         25775 |             1000000000 | False          | False        |
| December  | end-pass boundary input-prefix erased0.5 plain27               | True          |          1         |             1 |             1000000000 | True           | True         |
| December  | end-pass preclue input-prefix J-lens                           | False         |          1         |         28066 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix erased0.5 J-lens                 | False         |          1         |         28546 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix erased0.5 plain24                | False         |          1         |          9762 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix erased0.5 plain27                | False         |          1         |          3598 |             1000000000 | False          | False        |
| December  | end-pass input-prefix metric-erased0.5 J-lens                  | True          |          1         |            25 |             1000000000 | True           | True         |
| December  | end-pass input-prefix metric-erased0.5 plain24                 | False         |          1         |         23020 |             1000000000 | False          | False        |
| December  | end-pass input-prefix metric-erased0.5 plain27                 | True          |          1         |            10 |             1000000000 | True           | True         |
| December  | end-pass input-prefix metric-erased0.5 random0 J-lens          | True          |          1         |            17 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix metric-erased0.5 J-lens         | True          |          1         |             4 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |          1         |         26494 |             1000000000 | False          | False        |
| December  | end-pass boundary input-prefix metric-erased0.5 plain27        | True          |          1         |             2 |             1000000000 | True           | True         |
| December  | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | True          |          1         |             2 |             1000000000 | True           | True         |
| December  | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |          1         |         27093 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |          1         |          9599 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |          1         |          3405 |             1000000000 | False          | False        |
| December  | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |          1         |         28623 |             1000000000 | False          | False        |
| Thursday  | J-lens                                                         | False         |          0.266667  |             5 |                      3 | False          | False        |
| Thursday  | plain lens                                                     | False         |          0.416667  |          2199 |                   4483 | False          | False        |
| Thursday  | end-pass J-lens                                                | True          |          1         |             4 |                      2 | False          | False        |
| Thursday  | end-pass logit contrast J-lens                                 | False         |          1         |         17558 |                  22244 | False          | False        |
| Thursday  | end-pass probability contrast J-lens                           | True          |          0.7       |             4 |                      3 | False          | False        |
| Thursday  | end-pass plain24                                               | False         |          1         |          2197 |                   4481 | False          | False        |
| Thursday  | end-pass logit contrast plain24                                | False         |          1         |        183592 |                 242485 | False          | False        |
| Thursday  | end-pass probability contrast plain24                          | False         |          0.8       |          2302 |                  22434 | False          | False        |
| Thursday  | end-pass plain27                                               | True          |          1         |             8 |                      2 | False          | False        |
| Thursday  | end-pass logit contrast plain27                                | False         |          1         |         94984 |                 160555 | False          | False        |
| Thursday  | end-pass probability contrast plain27                          | True          |          0.9       |             5 |                      4 | False          | False        |
| Thursday  | end-pass negative final control                                | False         |          1         |        240300 |                 246192 | False          | False        |
| Thursday  | end-pass erased1 J-lens                                        | False         |          1         |            39 |                     18 | False          | False        |
| Thursday  | end-pass erased0.5 J-lens                                      | True          |          1         |            10 |                      3 | False          | False        |
| Thursday  | end-pass erased1 plain24                                       | False         |          1         |          1371 |                   5192 | False          | False        |
| Thursday  | end-pass erased0.5 plain24                                     | False         |          1         |          1699 |                   4861 | False          | False        |
| Thursday  | end-pass erased1 plain27                                       | True          |          1         |            22 |                    127 | True           | True         |
| Thursday  | end-pass erased0.5 plain27                                     | False         |          1         |            35 |                     15 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 J-lens                         | True          |          1         |            10 |                      3 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 plain24                        | False         |          1         |          1689 |                   4840 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 plain27                        | False         |          1         |            34 |                     15 | False          | False        |
| Thursday  | end-pass input-prefix J-lens                                   | True          |          1         |             4 |                      2 | False          | False        |
| Thursday  | end-pass boundary input-prefix J-lens                          | True          |          1         |             6 |                     14 | False          | False        |
| Thursday  | end-pass boundary input-prefix erased0.5 J-lens                | True          |          1         |            24 |                     33 | True           | True         |
| Thursday  | end-pass boundary input-prefix erased0.5 plain24               | False         |          1         |         11886 |                   9463 | False          | False        |
| Thursday  | end-pass boundary input-prefix erased0.5 plain27               | False         |          1         |           358 |                    252 | False          | False        |
| Thursday  | end-pass preclue input-prefix J-lens                           | False         |          1         |          9562 |                   5287 | False          | False        |
| Thursday  | end-pass preclue input-prefix erased0.5 J-lens                 | False         |          1         |          9548 |                   5264 | False          | False        |
| Thursday  | end-pass preclue input-prefix erased0.5 plain24                | False         |          1         |         14480 |                 125215 | False          | False        |
| Thursday  | end-pass preclue input-prefix erased0.5 plain27                | False         |          1         |         27569 |                  39241 | False          | False        |
| Thursday  | end-pass input-prefix metric-erased0.5 J-lens                  | True          |          1         |            10 |                      5 | False          | False        |
| Thursday  | end-pass input-prefix metric-erased0.5 plain24                 | False         |          1         |          1841 |                   4730 | False          | False        |
| Thursday  | end-pass input-prefix metric-erased0.5 plain27                 | False         |          1         |            42 |                     18 | False          | False        |
| Thursday  | end-pass input-prefix metric-erased0.5 random0 J-lens          | True          |          1         |            10 |                      4 | False          | False        |
| Thursday  | end-pass boundary input-prefix metric-erased0.5 J-lens         | False         |          1         |            32 |                     41 | False          | False        |
| Thursday  | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |          1         |         12262 |                   9439 | False          | False        |
| Thursday  | end-pass boundary input-prefix metric-erased0.5 plain27        | False         |          1         |           394 |                    249 | False          | False        |
| Thursday  | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | True          |          1         |            27 |                     33 | True           | True         |
| Thursday  | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |          1         |          9506 |                   5355 | False          | False        |
| Thursday  | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |          1         |         14546 |                 125167 | False          | False        |
| Thursday  | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |          1         |         26590 |                  37987 | False          | False        |
| Thursday  | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |          1         |          9554 |                   5271 | False          | False        |
| autumn    | J-lens                                                         | False         |          0.371658  |            19 |                      0 | False          | False        |
| autumn    | plain lens                                                     | False         |          0.513369  |          1874 |                    402 | False          | False        |
| autumn    | end-pass J-lens                                                | True          |          1         |            14 |             1000000000 | True           | False        |
| autumn    | end-pass logit contrast J-lens                                 | False         |          1         |         46085 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast J-lens                           | True          |          0.617647  |            14 |             1000000000 | True           | False        |
| autumn    | end-pass plain24                                               | False         |          1         |          1872 |             1000000000 | False          | False        |
| autumn    | end-pass logit contrast plain24                                | False         |          1         |        239353 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain24                          | False         |          0.735294  |         67324 |             1000000000 | False          | False        |
| autumn    | end-pass plain27                                               | True          |          1         |            19 |             1000000000 | True           | False        |
| autumn    | end-pass logit contrast plain27                                | False         |          1         |        231836 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain27                          | True          |          0.882353  |            20 |             1000000000 | True           | False        |
| autumn    | end-pass negative final control                                | False         |          1         |        243744 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 J-lens                                        | False         |          1         |           112 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 J-lens                                      | True          |          1         |            24 |             1000000000 | True           | False        |
| autumn    | end-pass erased1 plain24                                       | False         |          1         |          2802 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 plain24                                     | False         |          1         |          3670 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain27                                       | True          |          1         |            61 |             1000000000 | False          | True         |
| autumn    | end-pass erased0.5 plain27                                     | True          |          1         |            25 |             1000000000 | True           | True         |
| autumn    | end-pass input-prefix erased0.5 J-lens                         | True          |          1         |            21 |             1000000000 | True           | False        |
| autumn    | end-pass input-prefix erased0.5 plain24                        | False         |          1         |          3656 |             1000000000 | False          | False        |
| autumn    | end-pass input-prefix erased0.5 plain27                        | True          |          1         |            25 |             1000000000 | True           | True         |
| autumn    | end-pass input-prefix J-lens                                   | True          |          1         |            12 |             1000000000 | True           | False        |
| autumn    | end-pass boundary input-prefix J-lens                          | True          |          1         |            28 |             1000000000 | True           | False        |
| autumn    | end-pass boundary input-prefix erased0.5 J-lens                | False         |          1         |            71 |             1000000000 | False          | False        |
| autumn    | end-pass boundary input-prefix erased0.5 plain24               | False         |          1         |          8194 |             1000000000 | False          | False        |
| autumn    | end-pass boundary input-prefix erased0.5 plain27               | True          |          1         |            16 |             1000000000 | True           | True         |
| autumn    | end-pass preclue input-prefix J-lens                           | False         |          1         |         46009 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix erased0.5 J-lens                 | False         |          1         |         46195 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix erased0.5 plain24                | False         |          1         |          5677 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix erased0.5 plain27                | False         |          1         |          3794 |             1000000000 | False          | False        |
| autumn    | end-pass input-prefix metric-erased0.5 J-lens                  | False         |          1         |            44 |             1000000000 | False          | False        |
| autumn    | end-pass input-prefix metric-erased0.5 plain24                 | False         |          1         |          3929 |             1000000000 | False          | False        |
| autumn    | end-pass input-prefix metric-erased0.5 plain27                 | True          |          1         |            24 |             1000000000 | True           | True         |
| autumn    | end-pass input-prefix metric-erased0.5 random0 J-lens          | True          |          1         |            17 |             1000000000 | True           | False        |
| autumn    | end-pass boundary input-prefix metric-erased0.5 J-lens         | False         |          1         |           179 |             1000000000 | False          | False        |
| autumn    | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |          1         |          9001 |             1000000000 | False          | False        |
| autumn    | end-pass boundary input-prefix metric-erased0.5 plain27        | True          |          1         |            16 |             1000000000 | True           | True         |
| autumn    | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | False         |          1         |            59 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |          1         |         46543 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |          1         |          5732 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |          1         |          3811 |             1000000000 | False          | False        |
| autumn    | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |          1         |         46400 |             1000000000 | False          | False        |
| apple     | J-lens                                                         | False         |          0         |           181 |                      0 | False          | False        |
| apple     | plain lens                                                     | False         |          0.0833333 |           359 |                    320 | False          | False        |
| apple     | end-pass J-lens                                                | False         |          1         |           171 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast J-lens                                 | False         |          1         |        117906 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast J-lens                           | False         |          0.694444  |           325 |             1000000000 | False          | False        |
| apple     | end-pass plain24                                               | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast plain24                                | False         |          1         |        223180 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain24                          | False         |          0.777778  |           372 |             1000000000 | False          | False        |
| apple     | end-pass plain27                                               | False         |          1         |           116 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast plain27                                | False         |          1         |        217940 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain27                          | False         |          0.833333  |           121 |             1000000000 | False          | False        |
| apple     | end-pass negative final control                                | False         |          1         |        225716 |             1000000000 | False          | False        |
| apple     | end-pass erased1 J-lens                                        | False         |          1         |           124 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 J-lens                                      | False         |          1         |           137 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain24                                       | False         |          1         |           374 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain24                                     | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain27                                       | False         |          1         |            88 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain27                                     | False         |          1         |           102 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 J-lens                         | False         |          1         |           131 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 plain24                        | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 plain27                        | False         |          1         |           102 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix J-lens                                   | False         |          1         |           165 |             1000000000 | False          | False        |
| apple     | end-pass boundary input-prefix J-lens                          | True          |          1         |             6 |             1000000000 | True           | True         |
| apple     | end-pass boundary input-prefix erased0.5 J-lens                | True          |          1         |             6 |             1000000000 | True           | True         |
| apple     | end-pass boundary input-prefix erased0.5 plain24               | False         |          1         |          1858 |             1000000000 | False          | False        |
| apple     | end-pass boundary input-prefix erased0.5 plain27               | True          |          1         |             0 |             1000000000 | True           | True         |
| apple     | end-pass preclue input-prefix J-lens                           | False         |          1         |          4584 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix erased0.5 J-lens                 | False         |          1         |          4582 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix erased0.5 plain24                | False         |          1         |          8446 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix erased0.5 plain27                | False         |          1         |          1318 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix metric-erased0.5 J-lens                  | False         |          1         |           132 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix metric-erased0.5 plain24                 | False         |          1         |           353 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix metric-erased0.5 plain27                 | False         |          1         |           100 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix metric-erased0.5 random0 J-lens          | False         |          1         |           113 |             1000000000 | False          | False        |
| apple     | end-pass boundary input-prefix metric-erased0.5 J-lens         | True          |          1         |             6 |             1000000000 | True           | True         |
| apple     | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |          1         |          1858 |             1000000000 | False          | False        |
| apple     | end-pass boundary input-prefix metric-erased0.5 plain27        | True          |          1         |             0 |             1000000000 | True           | True         |
| apple     | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | True          |          1         |             6 |             1000000000 | True           | True         |
| apple     | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |          1         |          4517 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |          1         |          8283 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |          1         |          1317 |             1000000000 | False          | False        |
| apple     | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |          1         |          4701 |             1000000000 | False          | False        |
| cloud     | J-lens                                                         | False         |                    |             1 |             1000000000 |                |              |
| cloud     | plain lens                                                     | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass J-lens                                                | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass logit contrast J-lens                                 | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass probability contrast J-lens                           | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass plain24                                               | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass logit contrast plain24                                | False         |                    |          3882 |             1000000000 |                |              |
| cloud     | end-pass probability contrast plain24                          | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass plain27                                               | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass logit contrast plain27                                | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass probability contrast plain27                          | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass negative final control                                | False         |                    |        151169 |             1000000000 |                |              |
| cloud     | end-pass erased1 J-lens                                        | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 J-lens                                      | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain24                                       | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain24                                     | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased1 plain27                                       | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass erased0.5 plain27                                     | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass input-prefix erased0.5 J-lens                         | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass input-prefix erased0.5 plain24                        | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass input-prefix erased0.5 plain27                        | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass input-prefix J-lens                                   | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix J-lens                          | False         |                    |            15 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix erased0.5 J-lens                | False         |                    |            15 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix erased0.5 plain24               | False         |                    |            19 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix erased0.5 plain27               | False         |                    |             2 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix J-lens                           | False         |                    |         18313 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix erased0.5 J-lens                 | False         |                    |         19829 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix erased0.5 plain24                | False         |                    |         50942 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix erased0.5 plain27                | False         |                    |         13027 |             1000000000 |                |              |
| cloud     | end-pass input-prefix metric-erased0.5 J-lens                  | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass input-prefix metric-erased0.5 plain24                 | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass input-prefix metric-erased0.5 plain27                 | False         |                    |             0 |             1000000000 |                |              |
| cloud     | end-pass input-prefix metric-erased0.5 random0 J-lens          | False         |                    |             1 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix metric-erased0.5 J-lens         | False         |                    |            15 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |                    |            19 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix metric-erased0.5 plain27        | False         |                    |             2 |             1000000000 |                |              |
| cloud     | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | False         |                    |            15 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |                    |         21853 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |                    |         51125 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |                    |         13114 |             1000000000 |                |              |
| cloud     | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |                    |         20772 |             1000000000 |                |              |
| cloud     | J-lens                                                         | True          |          0.62963   |             0 |                    286 | True           | True         |
| cloud     | plain lens                                                     | True          |          0.555556  |             0 |                    233 | True           | True         |
| cloud     | end-pass J-lens                                                | True          |          0.62963   |             0 |                    286 | True           | True         |
| cloud     | end-pass logit contrast J-lens                                 | True          |          1         |             1 |                 246988 | True           | True         |
| cloud     | end-pass probability contrast J-lens                           | True          |          0.833333  |             0 |             1000000000 | True           | True         |
| cloud     | end-pass plain24                                               | True          |          0.555556  |             0 |                    233 | True           | True         |
| cloud     | end-pass logit contrast plain24                                | False         |          0.962963  |          8427 |                 243835 | False          | False        |
| cloud     | end-pass probability contrast plain24                          | True          |          0.814815  |             0 |                  10893 | True           | True         |
| cloud     | end-pass plain27                                               | True          |          0.555556  |             0 |                     49 | True           | True         |
| cloud     | end-pass logit contrast plain27                                | True          |          0.851852  |             0 |                 200238 | True           | True         |
| cloud     | end-pass probability contrast plain27                          | True          |          0.777778  |             0 |             1000000000 | True           | True         |
| cloud     | end-pass negative final control                                | False         |          0.888889  |        199188 |                 248008 | False          | False        |
| cloud     | end-pass erased1 J-lens                                        | True          |          0.62963   |             0 |                    345 | True           | True         |
| cloud     | end-pass erased0.5 J-lens                                      | True          |          0.62963   |             0 |                    323 | True           | True         |
| cloud     | end-pass erased1 plain24                                       | True          |          0.555556  |             0 |                    122 | True           | True         |
| cloud     | end-pass erased0.5 plain24                                     | True          |          0.555556  |             0 |                    157 | True           | True         |
| cloud     | end-pass erased1 plain27                                       | True          |          0.555556  |             0 |                     49 | True           | True         |
| cloud     | end-pass erased0.5 plain27                                     | True          |          0.555556  |             0 |                     49 | True           | True         |
| cloud     | end-pass input-prefix erased0.5 J-lens                         | True          |          0.62963   |             0 |                    322 | True           | True         |
| cloud     | end-pass input-prefix erased0.5 plain24                        | True          |          0.555556  |             0 |                    157 | True           | True         |
| cloud     | end-pass input-prefix erased0.5 plain27                        | True          |          0.555556  |             0 |                     49 | True           | True         |
| cloud     | end-pass input-prefix J-lens                                   | True          |          0.62963   |             0 |                    285 | True           | True         |
| cloud     | end-pass boundary input-prefix J-lens                          | False         |          0.518519  |          3934 |                  21344 | False          | False        |
| cloud     | end-pass boundary input-prefix erased0.5 J-lens                | False         |          0.518519  |          3682 |                  20059 | False          | False        |
| cloud     | end-pass boundary input-prefix erased0.5 plain24               | False         |          0.148148  |          5228 |                   9124 | False          | False        |
| cloud     | end-pass boundary input-prefix erased0.5 plain27               | False         |          0.240741  |          1033 |                   5002 | False          | False        |
| cloud     | end-pass preclue input-prefix J-lens                           | False         |          0.796296  |         18335 |                  70322 | False          | False        |
| cloud     | end-pass preclue input-prefix erased0.5 J-lens                 | False         |          0.796296  |         18522 |                  69938 | False          | False        |
| cloud     | end-pass preclue input-prefix erased0.5 plain24                | False         |          1         |         50002 |                 236976 | False          | False        |
| cloud     | end-pass preclue input-prefix erased0.5 plain27                | False         |          1         |         12936 |                 204781 | False          | False        |
| cloud     | end-pass input-prefix metric-erased0.5 J-lens                  | True          |          0.62963   |             0 |                    315 | True           | True         |
| cloud     | end-pass input-prefix metric-erased0.5 plain24                 | True          |          0.555556  |             0 |                    160 | True           | True         |
| cloud     | end-pass input-prefix metric-erased0.5 plain27                 | True          |          0.555556  |             0 |                     49 | True           | True         |
| cloud     | end-pass input-prefix metric-erased0.5 random0 J-lens          | True          |          0.62963   |             0 |                    323 | True           | True         |
| cloud     | end-pass boundary input-prefix metric-erased0.5 J-lens         | False         |          0.481481  |          3369 |                  17803 | False          | False        |
| cloud     | end-pass boundary input-prefix metric-erased0.5 plain24        | False         |          0.148148  |          5448 |                   8864 | False          | False        |
| cloud     | end-pass boundary input-prefix metric-erased0.5 plain27        | False         |          0.240741  |          1097 |                   5194 | False          | False        |
| cloud     | end-pass boundary input-prefix metric-erased0.5 random0 J-lens | False         |          0.555556  |          3517 |                  21135 | False          | False        |
| cloud     | end-pass preclue input-prefix metric-erased0.5 J-lens          | False         |          0.814815  |         18083 |                  69670 | False          | False        |
| cloud     | end-pass preclue input-prefix metric-erased0.5 plain24         | False         |          1         |         50566 |                 237074 | False          | False        |
| cloud     | end-pass preclue input-prefix metric-erased0.5 plain27         | False         |          1         |         13053 |                 204483 | False          | False        |
| cloud     | end-pass preclue input-prefix metric-erased0.5 random0 J-lens  | False         |          0.777778  |         18054 |                  69589 | False          | False        |

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

J-lens: [' Months', ' months', ' February', 'months', ' December', ' Calendar', ' Facts', ' Year', ' January', 'Months', ' **', '次年', '事实', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' April', ' holidays', '/month', ' Seasons']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

plain lens: ['事实', '_fact', ' صدا', 'orías', 'вис', ' Fakta', '…the', ' fakta', ' facts', '名副其实的', ' Câ', ' Pôle', 'óź', '事实和', '版权声明', 'の販', '事實', 'ヵ', ' prekybos', ' beleg', ':...', '?...', ' факта', ' Situé', 'ément', ' Facts', '…**', ' факт', '探し', ' **:**', ' sacerdo', 'eceğ']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass J-lens: [' Months', ' months', ' February', 'months', ' December', ' Calendar', ' Facts', ' Year', 'Months', ' **', '事实', '次年', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', '-month', ' Tomorrow', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' April', '/month', ' holidays', ' Seasons', '...**']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass logit contrast J-lens: [' Months', ' Seasons', ' Skyl', ' Weeks', ' Autumn', ' Stars', ' Holidays', ' Rings', ' Calendar', ' Padding', ' Sundays', ' Moon', ' Tues', ' Sink', ' Week', ' Seconds', ' Past', ' Esc', ' Thurs', ' Season', ' Sunset', ' Tro', ' Hills', ' months', ' Extras', ' Bend', ' Pets', ' Weekend', ' Hours', ' calendars', ' Camp', ' Spring']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass probability contrast J-lens: [' Months', ' months', ' February', 'months', ' December', ' Calendar', ' Facts', ' Year', 'Months', ' **', '次年', '事实', ' November', ' Next', ' July', ' calendar', ' Winter', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' holidays', '/month', ' April', ' Seasons', '...**']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass plain24: ['事实', '_fact', ' صدا', 'orías', 'вис', ' Fakta', '…the', ' fakta', ' facts', '名副其实的', ' Câ', ' Pôle', 'óź', '事实和', '版权声明', 'の販', '事實', 'ヵ', ' prekybos', ' beleg', ':...', '?...', ' факта', ' Situé', 'ément', ' Facts', '…**', ' факт', '探し', ' **:**', ' sacerdo', 'eceğ']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass logit contrast plain24: [' vids', ' الفض', 'orías', ' amator', ' Росси', ' कांग', 'снабжение', ' prostituer', ' koncer', '金は', 'испуска', 'erias', ' спів', ' Пле', 'örde', ' Collec', ' 웹사이트가', 'veux', 'питы', ' petró', 'prüft', ' صدا', ' frags', 'клеи', ' zove', 'ợi', 'venes', 'áles', 'tiges', ' ГИБ', 'giờ', '-ves']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass probability contrast plain24: ['事实', '_fact', ' صدا', 'orías', 'вис', ' Fakta', ' fakta', '…the', ' facts', ' Câ', '名副其实的', ' Pôle', 'óź', '事实和', 'の販', '版权声明', '事實', ' prekybos', 'ヵ', ' beleg', ' факта', '?...', ':...', ' Situé', 'ément', '…**', ' Facts', '探し', ' **:**', ' факт', 'eceğ', ' sacerdo']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass plain27: ['_Dec', 'December', ' December', '事实', '-Jan', '版权声明', '展望', '寒冷的', '腊', ' Empresarial', 'ajukan', '冬', '元旦', '闰', ' Ро', ' Fakta', '越し', '腊月', '新年快乐', ' Januari', '-Nov', 'Leap', ' صدا', ' February', ' Leap', 'February', '新年的', 'Dec', ' facts', ' факта', '-Apr', '…the']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass logit contrast plain27: [' الفض', ' frags', ' petró', ' amator', ' vids', ' *))', 'ESSAGES', ' nutris', '��', ' prostituer', ' trots', 'cios', 'ợi', 'ssia', '金は', 'испуска', 'питы', 'hål', 'prüft', ' صدا', 'снабжение', ' porsi', ')./', 'śnia', ' ГИБ', 'tridges', ' Attra', ' beri', ' :*', 'chtet', 'czą', ' cuz']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass probability contrast plain27: ['_Dec', ' December', '事实', '-Jan', '版权声明', '展望', '寒冷的', '腊', ' Empresarial', 'ajukan', '冬', '闰', '元旦', ' Ро', '越し', '新年快乐', ' Fakta', '腊月', '-Nov', ' Januari', 'Leap', ' صدا', ' February', ' Leap', '新年的', ' facts', ' факта', '-Apr', '…the', 'の販', '明け', '事實']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass negative final control: [' msgs', '/bg', '娃', ' BG', ' BB', '勇者', ',msg', 'tiges', ' RR', ' chk', ' HD', 'anggar', ' KK', ' cid', 'altungs', ' creds', '不胜', ' excep', ' Horiz', 'estes', ' cx', ' msg', ' htt', '郎', ' cursus', ' vids', ' HS', ' HT', '混混', '.hd', '_msgs', ' fig']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased1 J-lens: [' **', '...', ' ...', ' Next', ' Facts', ' Months', '**', '事实', ' months', ' Calendar', ' Year', '…', ' next', ' Future', ' Tomorrow', ' calendar', ' Leap', 'months', ' …', 'Next', '次年', '……', ' facts', ' Week', '(next', ' Spring', 'next', ' Past', ' Summer', ' Actually', ' Winter', ' weeks']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased0.5 J-lens: [' **', ' Months', ' months', ' Facts', ' Calendar', ' Year', ' Next', '事实', 'months', '...', ' ...', ' calendar', 'Months', '次年', ' Tomorrow', ' Leap', '**', ' February', ' Future', ' December', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', ' Summer', '…', '(next', ' weeks', ' facts']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased1 plain24: ['事实', '_fact', ' صدا', 'вис', ' facts', 'orías', ' fakta', ' Fakta', '名副其实的', ' Câ', '事實', 'óź', '版权声明', '…the', '事实和', ' Pôle', 'ヵ', ' beleg', ' Facts', ' факт', ' факта', ':...', ' prekybos', '?...', 'の販', ' Situé', 'ément', '探し', '事实上', '...(', ' sacerdo', '…**']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased0.5 plain24: ['事实', '_fact', ' صدا', 'вис', 'orías', ' Fakta', ' facts', ' fakta', ' Câ', '名副其实的', '…the', 'óź', ' Pôle', '事實', '版权声明', '事实和', 'ヵ', ' beleg', ' prekybos', ' факта', 'の販', ':...', ' Facts', ' факт', '?...', ' Situé', 'ément', '探し', '…**', '...(', ' sacerdo', '事实上']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased1 plain27: ['_Dec', '事实', ' ...', '…', '...', '展望', '版权声明', ' …', 'apt', ' facts', ' **', ' Dec', '冬', '闰', '寒冷的', 'Dec', '……', ' Ро', '乞', '<think>', ' Leap', ' Facts', '赔', '腊', '陪', 'Leap', ' called', '的事实', '越し', '猎', '_dec', ' yours']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass erased0.5 plain27: ['_Dec', '事实', '版权声明', '展望', '寒冷的', '冬', '腊', '闰', ' Ро', ' ...', ' December', ' facts', '…', ' Empresarial', '越し', 'Leap', ' Leap', 'Dec', 'ajukan', '新年快乐', ' Dec', '乞', ' Facts', ' صدا', 'apt', ' Fakta', ' факта', 'December', '事實', '_dec', ' Yours', '...']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' **', ' Calendar', ' Year', ' Next', '事实', ' ...', '...', '次年', ' calendar', ' Tomorrow', ' Leap', '**', ' February', ' December', ' Future', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', '…', ' weeks', '(next', 'Calendar', ' Summer', '-month', ' Seasons', ' Holidays', ' Season', ' year']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['事实', '_fact', ' صدا', 'вис', 'orías', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', ' beleg', 'ヵ', 'の販', ' prekybos', ' факта', ':...', ' факт', '?...', 'ément', ' Situé', '探し', '…**', '...(', ' sacerdo', '事实上', 'eceğ', '小编为大家整理的']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['_Dec', '事实', '版权声明', '展望', '寒冷的', '冬', '腊', '闰', ' Ро', ' ...', ' December', '…', 'Leap', ' Empresarial', '越し', 'ajukan', ' Leap', 'Dec', '新年快乐', '乞', ' Dec', ' صدا', 'apt', ' Fakta', ' факта', 'December', '事實', '_dec', ' Yours', '...', '元旦', '赔']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix J-lens: [' February', ' December', ' Calendar', ' Year', ' **', '事实', '次年', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' holidays', ' April', '/month', ' Seasons', '...**', ' weeks', 'December', '_year', ' Future', ' Season']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix J-lens: [' December', '月份', ' February', 'December', '次年', 'February', ' November', '-month', ' October', ' April', '_month', '当月', ' Calendar', ' Year', 'October', '/month', 'April', 'November', 'Calendar', '十二月', 'calendar', ' September', ' March', '___', '月份的', ' July', '.Month', '一个月', 'Year', '.month', '月底', 'September']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: ['月份', '次年', ' December', '___', '____', '__', '-month', ' Calendar', ' Year', '当月', ' February', '_month', 'Calendar', '**', 'calendar', '日历', ' Tomorrow', '一个月', ' November', ' ___', ' next', ' calendar', '闰', ' ____', ' October', 'next', '月底', ' April', '_*', '明年', '翌', ' Next']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['unie', '圆梦', '籌', 'の販', '筹', ' sluts', '雰', ' eskort', '[image', ' قائ', '같', '問わず', 'ovem', '服务部', '路网', 'ISATION', 'ément', 'wali', 'ujuan', '订制', ' gee', ' cherchez', '日历', '拉开序幕', 'разу', ' Folg', 'ヵ', 'ฉาย', 'رفة', '_variation', 'lepší', '力士']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: ['_Dec', ' Boxing', ' December', ' Ро', ' Dec', 'ecoin', ' Feliz', '雰', 'December', ' قائ', 'ypy', ' Advent', 'elő', 'Ро', '要么是', '阳春', '籌', '新的一年', ' gee', 'unie', 'Dec', '闰', '尽享', ' fö', ' payday', '\tJ', ' ژ', '(_)', '跨年', 'ヵ', '风景名胜', ' посл']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', ':\\"', ').\\', '?\\', ',\\', '\\"\\', ' **“', '\\")', '*\\', ')\\', ',__', ',”', ' \\"{', ':+', '\\",\\"', '+)\\', '."),', ' franz', '+z', '+",', '>\\', ')”', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', 'os', '中和', 'AYS', 'corr', '発表した', 'udy', ' Entrega', 'ud', 'itu', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', '有关人员', 'eme']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', 'ute', '2', 'in', 'l', 'oe', 'ug', 'zt', '4', '1', 'ere', 'os', 'ill', 'se', 'im', 'id', '处', 'ort', 'ud', '3', 'je', 'zz', 'ur', '义', 'usr', '5', 'endants', 'ills', '8', ' +', 'ounds', 'ore']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' **', ' Calendar', ' Next', ' Year', '事实', ' Tomorrow', ' Leap', '次年', '...**', ' Future', '…**', ' Holidays', ' Seasons', ' Week', ' calendar', 'calendar', '(next', ' Winter', ' February', ' Fakt', ' Vacation', ' Spring', 'Calendar', ' Past', ' **.**', ' Weeks', ' December', ' Season', ' Nothing', ' holidays', ':...', ' Summer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: ['事实', '_fact', ' صدا', 'orías', 'вис', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', 'ヵ', ' prekybos', ' beleg', ' факта', 'の販', ':...', '?...', ' факт', ' Situé', 'ément', '探し', '…**', '...(', 'eceğ', ' sacerdo', ' **:**', '事实上']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: ['_Dec', '事实', '版权声明', '展望', '寒冷的', '闰', ' Ро', '腊', '冬', ' Empresarial', ' December', 'Leap', 'ajukan', '越し', ' Leap', ' ...', ' Fakta', '新年快乐', ' صدا', 'Dec', '…', '乞', ' факта', ' Dec', '事實', 'apt', 'December', '_dec', ' Yours', '-Nov', '的事实', '赔']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' **', ' Calendar', ' Next', '事实', ' Year', '次年', ' calendar', '**', ' Tomorrow', '...', ' ...', ' February', ' next', ' Future', 'calendar', ' Leap', ' Spring', ' December', ' Winter', ' Week', ' weeks', 'next', '(next', 'Next', 'Calendar', '…', ' Summer', ' summer', ' holidays', ' Season', ' Seasons', ' year']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: ['月份', '次年', ' Calendar', '___', ' December', '-month', '当月', '**!', ' Tomorrow', '...**', ' Year', '_month', '[__', '____', ' ___', '__:', 'Calendar', '_*', 'calendar', '日历', ' February', '翌', ' следующего', ' ____', ' *[', '__', '/month', ' NEXT', '闰', '月份的', '_MONTH', '一个月']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['unie', '圆梦', '籌', '雰', ' eskort', ' sluts', 'の販', '筹', '[image', ' قائ', '같', '問わず', 'ovem', '服务部', '路网', 'ISATION', 'ément', 'wali', '订制', ' Folg', ' gee', ' cherchez', '日历', '拉开序幕', 'ujuan', 'ฉาย', 'ヵ', 'разу', 'lepší', 'رفة', '_variation', '力士']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: ['_Dec', ' Boxing', ' December', ' Ро', ' Dec', 'ecoin', ' Feliz', '雰', 'December', ' قائ', 'ypy', ' Advent', 'Ро', 'elő', '阳春', '要么是', '籌', 'unie', ' gee', '新的一年', '闰', '尽享', ' payday', 'Dec', 'ヵ', ' fö', ' ژ', '\tJ', '跨年', 'ộp', '(_)', '风景名胜']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: ['月份', '次年', ' December', ' Calendar', '___', '____', '__', ' February', '-month', '**', 'calendar', '_month', '当月', ' Year', ' next', '月底', 'Calendar', 'next', '一个月', '日历', ' calendar', ' Tomorrow', ' November', '闰', ' October', ' ____', ' ___', ' April', ' **', '翌', ' следующего', ' birthdays']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', '?\\', ').\\', ' **„', ':\\"', ',\\', '\\"\\', '\\")', ' **“', '*\\', ')\\', ',”', ',__', ':+', '\\",\\"', ' \\"{', '+)\\', '."),', '+z', '.#', ' franz', '>\\', '+",', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', 'os', '中和', '钦', 'AYS', 'corr', '発表した', 'udy', 'ud', ' Entrega', 'uz', 'zz', 'itu', '发', 'rait', 'äs', 'uto', '有关人员', 'eme', '说法']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', 'ute', '2', 'in', 'l', 'oe', 'ug', 'zt', '4', '1', 'ere', 'os', 'ill', 'se', 'im', 'id', '处', 'ort', '3', 'ud', 'je', 'zz', 'ur', '5', 'usr', '义', 'endants', 'ills', ' +', '8', 'ore', 'ounds']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'January<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ':\\"', '?\\', ').\\', ',\\', '\\"\\', '\\")', ' **“', '*\\', ')\\', ',__', ' \\"{', ',”', ':+', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+",', '+z', ')”', '.#']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

J-lens: [' Tuesday', ' Saturday', ' Monday', ' Wednesday', ' Friday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Tues', ' Night', ' Today', ' Days', ' weekend', ' Mondays', ' Thanksgiving', ' Facts', ' Christmas', '明天的', ' Sundays', ' **', 'Tuesday', ' weekends', 'Monday', ' Evening', ' Morning', ' weekdays', ' Halloween']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

plain lens: ['事实', '_fact', ' fakta', ' факт', ' facts', 'ceptive', '的事实', '事实和', '明天的', ' Facts', ' Empresarial', ' compro', 'eve', '当地的', ' факта', 'facts', '…**', ' Fakta', ' beleg', 'IVAL', ' Fakten', ' chôm', ' factura', ' sacerdo', ' Pôle', ' fatos', '事实上', ' 사실', '本题考查', '赔', 'eceğ', ' صدا']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass J-lens: [' Saturday', ' Monday', ' Friday', ' Wednesday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' Days', ' Mondays', ' weekend', ' Thanksgiving', ' Facts', ' Christmas', ' Sundays', '明天的', ' **', ' weekends', 'Monday', ' Evening', ' Morning', ' Halloween', ' weekdays', ' Saturdays', '事实', ' Fridays']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass logit contrast J-lens: [' Nights', ' Skyl', ' Days', ' Months', ' Yesterday', ' Emails', ' Night', ' NIGHT', ' Tonight', ' Smooth', ' Pets', ' nights', ' Whites', ' Slack', ' Calendar', ' Holidays', ' Barra', ' mornings', ' **—', ' Weeks', ' Breakfast', ' Día', ' Eggs', ' Cura', ' Entries', ' Camel', ' Month', ' Messages', ' Stars', ' Bairro', ' Espero', ' Tomorrow']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass probability contrast J-lens: [' Monday', ' Saturday', ' Wednesday', ' Friday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' Days', ' Mondays', ' weekend', ' Thanksgiving', ' Facts', ' Christmas', '明天的', ' Sundays', ' **', ' weekends', ' Evening', ' Morning', ' Halloween', ' weekdays', ' Saturdays', ' Fridays', '事实', ' nights']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass plain24: ['事实', '_fact', ' fakta', ' факт', ' facts', 'ceptive', '的事实', '事实和', '明天的', ' Facts', ' Empresarial', ' compro', 'eve', '当地的', ' факта', 'facts', '…**', ' Fakta', ' beleg', 'IVAL', ' Fakten', ' chôm', ' factura', ' sacerdo', ' Pôle', ' fatos', '事实上', ' 사실', '本题考查', '赔', 'eceğ', ' صدا']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass logit contrast plain24: [' projec', ' amator', 'amenta', 'erias', ' assemb', ' Arro', 'áles', '_router', 'colas', 'ehrte', ' videoc', 'SETTING', 'питы', ' vids', ' Escolar', ' 웹사이트가', 'клеи', 'испуска', 'orías', 'проце', ' correc', ' urls', ' prospec', ' sluts', ' esimerk', ' nasta', ' netizen', ' concurr', 'ehrt', ' especi', '图片素材', 'stants']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass probability contrast plain24: ['事实', '_fact', ' fakta', ' facts', ' факт', 'ceptive', '的事实', '明天的', '事实和', ' Facts', ' Empresarial', ' compro', '当地的', 'eve', ' факта', 'facts', '…**', ' beleg', ' Fakta', 'IVAL', ' chôm', ' factura', ' Fakten', ' sacerdo', ' Pôle', ' fatos', ' 사실', '事实上', 'eceğ', '赔', '本题考查', ' صدا']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass plain27: ['Monday', ' Wednesday', '周一', ' Saturday', 'Friday', ' Monday', ' Friday', 'Saturday', ' Thursday', ' Sunday', '周六', ' среду', '赔', ' среда', 'Wednesday', 'Sunday', ' weekends', '圩', 'rides', '事实', '星期六', '星期二', '요일', ' friday', '安息', 'Thursday', '礼拜', ' monday', '.tom', ' pazar', '星期日', '后天']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass logit contrast plain27: [' videoc', ' amator', ' Administra', 'ỐI', ' fabr', '图片素材', ' Crian', '_registers', ' videok', 'ENCES', 'َاء', ' assemb', ' muta', ' siguran', 'ỒNG', '网卡', ' Putih', ' ARGS', ' cargos', ' lancar', 'питы', ' ervar', '圈圈', ' efficac', 'ulangan', ' Responsabile', 'acza', 'писы', 'をストック', ' cioc', ' Gradu', ' webb']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass probability contrast plain27: [' Wednesday', '周一', ' Monday', ' Saturday', ' Friday', ' Thursday', ' Sunday', '周六', '赔', ' среду', ' среда', '圩', ' weekends', 'rides', '事实', '星期六', '星期二', '요일', '礼拜', '安息', ' friday', ' monday', ' pazar', '.tom', '后天', '星期日', '星期一', ' weekdays', ' therap', '普通的', ' Fakta', ' fronti']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass negative final control: ['站站', ' msgs', ' simila', ' Attra', ' profiles', ' §§', ' amator', ' files', ' graphics', ' decals', ' styles', ' codec', ' disadv', ' originals', ' Istitu', 'azos', ' 웹사이트가', ' messages', ' coeffs', ' JAVA', ' animations', ' fonts', ' visuals', ' filmer', ' Евгений', ' images', ' ejem', ' estilos', ' finali', ' inves', '花草', ' timings']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased1 J-lens: [' **', ' Tomorrow', ' Night', ' Midnight', ' Today', ' Christmas', '**', ' Facts', '事实', ' Days', ' Yesterday', ' Thanksgiving', ' Halloween', ' tomorrow', ' Tonight', ' Saturday', ' Weekend', ' It', ' Friday', ' Sunday', ' Moon', ' daylight', ' Monday', ' nights', ' Leap', ' Morning', ' Answer', ' night', ' weekend', '明天的', ' Nights', ' Next']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased0.5 J-lens: [' Tomorrow', ' **', ' Saturday', ' Friday', ' Monday', ' Midnight', ' Yesterday', ' Night', ' Sunday', ' Wednesday', ' Thursday', ' tomorrow', ' Today', ' Tonight', ' Facts', ' Christmas', ' Days', ' Weekend', ' Thanksgiving', '事实', ' Halloween', ' weekend', '明天的', ' Morning', ' Evening', ' nights', ' weekends', ' Nights', ' Holidays', ' NIGHT', ' daylight', ' Leap']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased1 plain24: ['事实', '_fact', ' fakta', ' facts', ' факт', 'ceptive', '的事实', ' Facts', '事实和', '明天的', '当地的', ' compro', 'eve', ' Empresarial', ' факта', '本题考查', 'facts', '事实上', ' 사실', ' beleg', '赔', 'IVAL', ' factual', ' Fakten', ' fatos', ' factura', ' факты', '…**', ' fato', 'yar', '版权声明', '医疗队']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased0.5 plain24: ['事实', '_fact', ' fakta', ' facts', ' факт', 'ceptive', '的事实', ' Facts', '事实和', '明天的', ' compro', '当地的', 'eve', ' Empresarial', ' факта', 'facts', '本题考查', ' beleg', 'IVAL', '事实上', ' 사실', '赔', '…**', ' factura', ' Fakten', ' fatos', ' Fakta', ' факты', ' factual', ' chôm', 'eceğ', ' sacerdo']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased1 plain27: ['赔', '...', ' **', '事实', 'fr', 'rides', '圩', '…', '中华人民共和国', '普通的', ' среда', '.tom', ' среду', '普通', 'FR', '安息', '周一', ' wed', ' sund', '금', ' ...', '后天', ' thu', '礼拜', '**', '요일', ' weekends', '法定', '陪', '_parser', ' pazar', ' جم']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass erased0.5 plain27: ['赔', '周一', 'Monday', '事实', '圩', ' Saturday', 'rides', ' среду', ' среда', ' Wednesday', ' Monday', '.tom', ' weekends', '普通的', '安息', ' Friday', '요일', '周六', '后天', '礼拜', 'Friday', 'fr', ' Sunday', ' wed', ' pazar', '中华人民共和国', ' sund', '금', '星期六', ' **', ' therap', ' جم']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' Tomorrow', ' **', ' Saturday', ' Friday', ' Monday', ' Midnight', ' Yesterday', ' Night', ' Sunday', ' Wednesday', ' Thursday', ' tomorrow', ' Today', ' Tonight', ' Christmas', ' Weekend', ' Thanksgiving', '事实', ' Halloween', ' weekend', '明天的', ' Evening', ' Morning', ' nights', ' weekends', ' Nights', ' Holidays', ' NIGHT', ' Leap', ' night', ' Sundays', ' Easter']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' compro', '当地的', 'eve', ' Empresarial', ' факта', ' beleg', '本题考查', 'IVAL', '事实上', '赔', '…**', ' 사실', ' Fakten', ' fatos', ' Fakta', 'eceğ', ' صدا', ' факты', ' chôm', ' sacerdo', ' Pôle', '医疗队', ' fato', '版权声明']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['赔', '周一', 'Monday', '事实', ' Saturday', '圩', 'rides', ' среду', ' среда', ' Wednesday', ' Monday', '.tom', '安息', '普通的', ' weekends', ' Friday', '요일', '周六', '礼拜', '后天', 'Friday', 'fr', ' wed', ' Sunday', ' pazar', '中华人民共和国', ' sund', '금', '星期六', ' **', ' جم', '普通']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix J-lens: [' Saturday', ' Monday', ' Friday', ' Wednesday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' weekend', ' Mondays', ' Thanksgiving', ' Christmas', ' Sundays', '明天的', ' **', ' weekends', 'Monday', ' Evening', ' Morning', ' Halloween', ' Saturdays', '事实', ' Fridays', ' nights', ' Holidays', ' Nights']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix J-lens: ['次日', ' tomorrow', ' next', ' Saturday', 'next', '第二天', ' Thursday', '紧接着', 'Next', ' Next', ' weekend', ' Monday', ' NEXT', '.next', '明天的', '_next', ' Friday', '-next', '翌', '(next', '下一个', ' Tomorrow', '接下来', ' weekends', '接下来的', 'Saturday', 'Monday', ' Wednesday', '明天', ' Sunday', ' getNext', '-day']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: ['次日', ' next', ' tomorrow', ' Next', 'Next', '紧接着', 'next', '.next', ' NEXT', '_next', '第二天', '下一个', '接下来', '-next', '(next', '翌', ' weekend', '明天的', '接下来的', ' Saturday', ' Tomorrow', '接着', ' weekends', '明天', '-day', ' Thursday', ' getNext', ' 다음', '\tnext', '.Next', ' следующий', ' Monday']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['紧接着', '下一个', 'ถัด', '.next', 'sequent', '-next', 'next', '(next', ' посл', '接下来', ' next', 'Next', '接踵', ' succeeding', '.Next', '翌', '之后的', ' kolej', '随后的', '下个', '_next', '日历', ' следующего', '紧随', '接下来的', '管所', '明天的', '\tnext', ' следующий', 'дне', ' наступ', ' getNext']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: ['-day', 'วัน', '.day', '(day', ' día', '_day', ' дня', '的那天', '/day', '-Day', 'eday', 'יום', '这一天', '�', ' день', '翌', '当天的', ' วัน', ' followed', ' follows', '明天的', '紧跟', '.tom', '跟进', 'ในวัน', '后天', '营业', '日的', '日是', 'День', '요일', 'днев']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '+",']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', 'corr', '中和', 'os', 'AYS', 'udy', '発表した', 'itu', 'ud', ' Entrega', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', 'eme', '中心医院']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', 'ute', '2', 'in', 'oe', 'l', 'zt', 'ug', '4', 'ere', 'ill', '1', 'os', 'se', 'im', 'id', '处', 'ort', 'ud', 'zz', '义', 'endants', 'ur', 'je', 'usr', 'ills', '3', '5', 'ounds', 'rie', ' +', '8']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' Tomorrow', ' Midnight', ' Yesterday', ' **', ' Saturday', ' Friday', ' Night', ' Tonight', ' Monday', ' Wednesday', ' Weekend', ' Thursday', ' Sunday', ' Today', '事实', ' Thanksgiving', ' tomorrow', ' Christmas', ' Holidays', '明天的', ' Halloween', ' Leap', ' NIGHT', ' Nights', ' Evening', ' Fakt', ' Morning', ' Calendar', ' Mondays', ' weekend', ' Truth', ' Easter']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: ['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' Empresarial', '当地的', ' compro', 'eve', ' факта', ' beleg', '本题考查', '…**', 'IVAL', '事实上', '赔', ' 사실', ' Fakta', ' fatos', ' Fakten', ' chôm', 'eceğ', ' صدا', ' Pôle', ' sacerdo', ' факты', '医疗队', ' fato', 'yar']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: ['赔', '周一', 'Monday', '事实', 'rides', '圩', ' Saturday', ' среду', ' среда', '.tom', ' Wednesday', ' Monday', ' weekends', '普通的', '安息', '요일', '礼拜', '周六', 'Friday', ' Friday', '后天', ' sund', ' pazar', ' wed', '中华人民共和国', 'fr', '금', ' Sunday', '星期六', ' fronti', ' جم', ' Satur']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' Tomorrow', ' **', ' Saturday', ' Monday', ' Friday', ' Midnight', ' Sunday', ' Wednesday', ' Yesterday', ' tomorrow', ' Thursday', ' Tonight', ' Night', ' Today', ' Christmas', ' Thanksgiving', ' Weekend', '明天的', '事实', ' Halloween', ' weekend', ' nights', ' Nights', ' Morning', ' Evening', ' weekends', ' Holidays', '**', ' Leap', ' Sundays', ' Calendar', ' night']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: ['次日', ' next', '紧接着', ' tomorrow', ' Next', ' NEXT', 'next', 'Next', '.next', '_next', '下一个', '接下来', '-next', '(next', '翌', '接下来的', '第二天', '明天的', ' Tomorrow', ' getNext', ' следующий', ' weekend', 'ถัด', '接着', ' Saturday', ' следующего', ' 다음', '\tnext', '随后的', '.Next', '下一页', ' lendemain']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['紧接着', 'ถัด', '下一个', '.next', 'sequent', '-next', '(next', 'next', ' посл', '接踵', '接下来', ' succeeding', ' next', 'Next', '.Next', '翌', '随后的', ' kolej', '下个', '之后的', '日历', '_next', '管所', '紧随', ' следующего', '接下来的', '明天的', '\tnext', ' следующий', 'дне', ' التالي', ' наступ']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: ['-day', 'วัน', '.day', '(day', ' día', '_day', ' дня', '的那天', '-Day', '/day', 'eday', 'יום', '�', '这一天', ' день', '翌', '当天的', ' วัน', ' followed', '明天的', ' follows', '紧跟', '.tom', '跟进', 'ในวัน', '营业', '后天', '日是', 'День', '日的', '요일', 'днев']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: ['次日', ' next', ' tomorrow', 'next', ' Next', '紧接着', 'Next', '.next', '第二天', '_next', ' NEXT', '下一个', '-next', '接下来', '明天的', '(next', '翌', ' weekend', ' Saturday', '接下来的', '接着', ' Tomorrow', '明天', ' следующего', ' Monday', '\tnext', ' weekends', ' Thursday', ' следующий', '-day', ' 다음', ' getNext']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',__', ',”', ':+', '\\",\\"', '+)\\', ' \\"{', '."),', ' franz', '+z', '>\\', '.#', ')”', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['udu', 'oe', 'zn', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', '中和', 'os', 'AYS', 'corr', 'udy', '発表した', 'itu', 'ud', ' Entrega', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', 'eme', '有关人员']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', 'ute', '2', 'in', 'oe', 'l', 'zt', 'ug', '4', 'ere', '1', 'os', 'ill', 'se', 'im', 'id', 'ort', '处', 'ud', 'zz', 'usr', '义', '3', 'ur', 'je', 'ills', 'endants', '5', 'rie', 'ounds', '8', ' +']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Tuesday<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', '+z', ' franz', ')”', '.#', '+",']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

J-lens: [' winter', 'winter', ' Winter', 'Winter', ' winters', ' summer', '冬季', '冬天', ' colder', 'summer', ' Seasons', ' seasons', ' **', ' frost', ' drought', '寒冬', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', ' spring', '春天', 'spring', ' seasonal', ' Tropical', ' primavera']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

plain lens: [' fakta', ' факта', '_fact', '事实', ' Facts', ' Pôle', ' наступ', ' Empresarial', ' fatos', '当地的', 'orías', 'rollers', 'つも', ' recherch', ' Croce', '越し', ' fatt', ' صدا', 'ẩm', '名副其实的', 'дем', 'óź', ' zove', ' pitan', 'レード', '월까지', ' факты', '乞', '寒冷的', 'ontaine', ' sanks', '版权声明']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass J-lens: [' summer', '冬季', '冬天', ' colder', 'summer', ' Seasons', ' seasons', ' **', ' frost', '寒冬', ' drought', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', ' spring', '春天', 'spring', ' Tropical', ' seasonal', ' primavera', ' vinter', ' Autumn', ' Frost', 'Spring', ' Facts']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass logit contrast J-lens: [' Seasons', ' Months', ' seasons', ' Holidays', '__:', ' **—', ' holidays', ' Mondays', '-season', ' Tropical', ' Trails', ' Tô', ' Tro', ' Moon', ' Whites', 'ฤดูกาล', ')__', '__[', ':__', '勿扰', ' Threads', '/Peak', ' Desert', ' Rocks', ' Peaks', ' Blacks', '季节', '季的', ' months', '=__', ' Lunar', ' Month']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass probability contrast J-lens: [' summer', '冬季', '冬天', ' colder', ' Seasons', ' seasons', ' **', ' frost', ' drought', '寒冬', '淡季', ' warmer', ' Summer', ' Spring', ' autumn', '冬天的', '-season', '冬', '夏季', '春季', '春天', ' Tropical', ' seasonal', ' spring', ' primavera', ' vinter', ' Frost', ' Autumn', '_season', ' Facts', ' зим', ' rainy']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass plain24: [' fakta', ' факта', '_fact', '事实', ' Facts', ' Pôle', ' наступ', ' Empresarial', ' fatos', '当地的', 'orías', 'rollers', 'つも', ' recherch', ' Croce', '越し', ' fatt', ' صدا', 'ẩm', '名副其实的', 'дем', 'óź', ' zove', ' pitan', 'レード', '월까지', ' факты', '乞', '寒冷的', 'ontaine', ' sanks', '版权声明']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass logit contrast plain24: ['veux', 'áles', ' Pipes', '-orders', ' Icons', ' Arro', "(['/", 'ehrt', '��', 'orías', '_router', 'の販', ' Croce', ' Trails', ' Bagno', 'iktigt', '-pocket', '-gay', ' cargos', ' Riders', ' trasparen', 'ùi', 'ehrte', '_pd', 'orios', 'izei', 'мога', ' Tô', 'andelt', ' chatten', ' Threads', ' Packs']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass probability contrast plain24: [' fakta', ' факта', '_fact', ' Facts', '事实', ' Pôle', ' Empresarial', ' наступ', 'orías', '当地的', ' fatos', ' recherch', 'つも', 'rollers', ' Croce', '越し', ' fatt', ' صدا', 'ẩm', 'дем', '名副其实的', ' zove', 'óź', ' pitan', 'レード', '월까지', '乞', ' факты', ' sanks', 'ontaine', '寒冷的', 'の販']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass plain27: ['spring', ' spring', ' Spring', 'Spring', 'summer', ' springs', '冬', ' summer', 'pring', '.spring', '夏', ' verano', ' colder', '春', '夏天', ' primavera', '春天', 'ฤดู', 'zim', ' autumn', ' vinter', ' summers', ' наступ', '\tSpring', ' Empresarial', '冬天', '暑', '夏天的', ' verão', ' лето', '冬天的', ' warmer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass logit contrast plain27: ['veux', '-orders', ' Pipes', 'onents', 'áles', ' esco', '��', 'izzano', ' Validators', ' Gerindra', ' Juta', '配乐', '_tools', '图片来源', '_pan', 'čko', 'PERTIES', 'struments', ' Bagno', ' Vrouw', 'の販', 'ESSAGES', 'atteri', '-pocket', '企业地址', ' Orders', ' الفض', ' Painter', 'urers', '_registers', '我的企业', ' Objects']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass probability contrast plain27: [' spring', ' Spring', ' springs', '冬', ' summer', 'pring', '.spring', '夏', 'Spring', ' verano', ' colder', '春', ' primavera', '夏天', 'ฤดู', '春天', 'zim', ' vinter', ' summers', ' наступ', ' autumn', '\tSpring', ' Empresarial', '冬天', '夏天的', '暑', ' verão', ' лето', '冬天的', '_season', '寒冷', ' warmer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass negative final control: [' msgs', ' packages', 'ienes', ' figures', '内外', ' threads', '-deals', 'idUser', ' logs', ' tokens', '_pkg', ' Threads', ' Packages', '潘', ' libs', ' Tokens', ' §§', ' pkg', ' Pad', 'orios', ' HD', 'ريد', '-stats', '_MB', ' PAD', ' package', ' paths', ' messages', '(PATH', ' polies', 'iglio', 'züg']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased1 J-lens: [' **', '**', '...', '…', ' ...', ':', '�', '<|endoftext|>', ' drought', ' …', ' It', 'It', '__', ' warmer', ' Facts', '事实', '……', ' frost', ' colder', '____', ' Tropical', ' seasons', ' tropical', '_', ';', ' warm', ' Seasons', ' This', '\\_', ' Spring', ' Frost', ' summer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased0.5 J-lens: [' **', '**', ' colder', ' drought', ' summer', ' frost', ' seasons', ' Seasons', ' warmer', '...', ' Spring', ' Facts', '…', ' Tropical', '淡季', '事实', ' Frost', ' tropical', ' spring', '冬季', ' Summer', ' rainy', '冬天', '春天', '寒冬', ' autumn', ' warm', ' seasonal', '夏季', ' Warm', ' ...', '-season']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased1 plain24: [' fakta', ' факта', '事实', '_fact', ' Facts', '...', '…', '当地的', ' наступ', ' ...', '乞', ' facts', ' fatt', ' fatos', 'дем', ' Croce', ' факты', '……', ' Pôle', ' temper', ' recherch', ' pitan', '本题考查', ' صدا', '件事', '版权声明', '名副其实的', 'lated', ' 사실을', 'orías', ' Empresarial', '暖']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased0.5 plain24: [' fakta', ' факта', '_fact', '事实', ' Facts', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', '乞', ' recherch', ' Empresarial', 'дем', 'orías', ' صدا', ' факты', ' pitan', ' facts', '名副其实的', 'ẩm', '越し', 'rollers', 'つも', 'óź', '版权声明', 'レード', '월까지', '件事', ' 사실을', ' temper']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased1 plain27: [' spring', ' Spring', 'spring', ' springs', 'Spring', '...', ' ...', '…', '夏', ' наступ', '春', 'pring', ' summer', '暑', '.spring', ' bore', ' …', ' **', ' colder', ' called', '春天', ' warmer', ' temper', 'zim', '版权声明', '夏天', '冬', '\xa0', '……', ' Empresarial', ' verano', 'fall']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass erased0.5 plain27: ['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '冬', '.spring', '春', ' наступ', ' colder', '春天', '暑', '夏天', ' verano', 'zim', ' primavera', 'ฤดู', ' warmer', ' Empresarial', ' ...', ' summers', ' autumn', '寒冷', ' bore', ' лето', '版权声明', '夏天的', 'fall']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' **', '**', ' colder', ' drought', ' summer', ' frost', ' warmer', '...', ' Spring', '…', ' Tropical', '淡季', '事实', ' Frost', ' tropical', ' spring', ' rainy', ' Summer', '冬季', '冬天', '春天', ' autumn', '寒冬', ' warm', '夏季', ' Warm', ' ...', '-season', '春季', 'Spring', 'summer', '�']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix erased0.5 plain24: [' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', '乞', ' recherch', ' Empresarial', 'orías', 'дем', ' факты', ' صدا', ' pitan', 'ẩm', '名副其实的', '越し', 'rollers', 'つも', 'óź', 'レード', '版权声明', '월까지', '件事', ' temper', ' 사실을', 'ontaine', 'lated']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '冬', '.spring', '春', ' наступ', ' colder', '春天', '暑', '夏天', ' verano', 'zim', ' primavera', 'ฤดู', ' warmer', ' Empresarial', ' ...', ' summers', ' autumn', '寒冷', ' bore', ' лето', '版权声明', '夏天的', 'fall']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix J-lens: [' summer', '冬季', '冬天', ' colder', 'summer', ' **', ' frost', '寒冬', ' drought', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', '春天', ' spring', 'spring', ' Tropical', ' primavera', ' vinter', ' Autumn', 'Spring', ' Frost', '_season', ' зим', ' printemps', ' rainy']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix J-lens: ['Spring', '春季', '___', 'spring', ' printemps', '雨季', 'summer', ' Spring', ' spring', ' summer', '冬季', '冬', '淡季', '夏季', '__:', ' primavera', '旺季', '春天', ' rainy', '__', '-season', ' summers', '季节', '寒冬', '春暖花开', '_season', '__)', '__.', ' autumn', '次年', '早春', 'Summer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: ['___', '__', 'Spring', '____', '春季', ' Spring', '雨季', '**', ' **', ' rainy', ' printemps', ' spring', ' ___', 'spring', '__:', ' __', '__.', '春天', ' summer', '__)', '淡季', '干旱', '夏季', '旺季', '季节', '春暖花开', ' primavera', ' ____', '_____', '次年', '_________', ' drought']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['問わず', '_-', ' springs', '要么是', 'spring', '管理类', 'imbul', 'onto', 'Regions', 'icu', ' preceded', ' mide', 'unno', '最专业的', 'разу', 'tings', 'Spring', '到来', 'дем', 'umont', 'urus', 'unity', '什么都没', 'REW', ' قائ', ' ką', 'schnitt', '้ง', 'azan', 'QUOTE', 'intérêt', 'IMG']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: [' Spring', ' spring', 'spring', 'Spring', 'pring', ' springs', '春', '.spring', 'fall', '春意', '夏', ' Springs', ' summer', ' fall', ' Fall', '\tSpring', ' autumn', '春的', '.Spring', ' primavera', ' FALL', '弹簧', '(Spring', ' Summer', '봄', '春天', '.springframework', 'Fall', '春天的', ' printemps', ' вес', 'summer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['udu', 'oe', 'zn', '义', 'zt', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', 'ute', '钦', '中和', 'ud', ' ficará', '投资有限公司', 'corr', '发', 'zz', 'uz', 'udy', 'AYS', '2', '5', 'itu', '発表した', '说法', ' Entrega', 'äs', 'uto', 'rait']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', 'ute', '2', 'oe', 'l', 'zt', 'ug', 'ere', '4', 'ill', '1', 'os', 'se', 'im', 'id', 'ort', '处', 'ud', 'endants', 'zz', 'ur', 'usr', '义', 'je', 'ills', '3', '5', 'rie', 'ounds', ' +', '8', 'od']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' **', ' colder', ' drought', ' Tropical', '…**', ' frost', '**', ' warmer', '事实', '淡季', ' tropical', '...**', ' summer', ' Frost', ' fakta', ' **.**', ' Spring', ' Warm', '__:', ' rainy', '-season', '干旱', ' kalt', ':...', ' primavera', ' **-', ' **.', ' Summer', ' Desert', '寒冬', '_season', ' Answer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: [' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', ' Empresarial', ' recherch', 'дем', 'orías', '乞', ' صدا', ' факты', 'ẩm', '名副其实的', ' pitan', '越し', 'óź', 'rollers', 'つも', '월까지', '版权声明', 'レード', 'ontaine', ' 사실을', ' zove', ' cocks', '件事']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: ['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '.spring', '冬', ' наступ', '春', ' colder', '春天', '暑', 'zim', ' verano', '夏天', ' primavera', ' Empresarial', 'ฤดู', ' warmer', ' summers', ' лето', ' autumn', '.Sum', '寒冷', '版权声明', ' fakta', ' bore', '\tSpring']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' **', '**', ' colder', ' summer', ' drought', ' frost', ' warmer', ' Spring', ' Tropical', ' tropical', '...', ' spring', '…', '事实', ' Frost', '淡季', '冬季', 'Spring', ' autumn', ' warm', ' Warm', '春季', ' Summer', ' rainy', '春天', '冬天', '寒冬', '夏季', 'summer', ' snow', '�', '寒冷']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: ['___', '__:', '__', '雨季', 'Spring', '__)', ' printemps', ' *__', '__.', '’**', '[__', ' ___', '春季', ' rainy', '____', ' Spring', ':__', '干旱', 'spring', ' **.', ' **.**', '春暖花开', '_),', '淡季', "'**", ')__', '**!', '旺季', '_________', ' primavera', '_*', ' ____']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['問わず', '_-', '要么是', ' springs', '管理类', 'imbul', 'spring', 'onto', 'Regions', 'icu', ' preceded', ' mide', '最专业的', 'unno', 'разу', 'tings', '到来', 'дем', 'Spring', 'umont', 'REW', 'urus', '什么都没', 'unity', ' قائ', 'schnitt', ' ką', 'intérêt', '้ง', 'azan', '航空航天大学', 'QUOTE']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: [' Spring', ' spring', 'spring', 'Spring', 'pring', ' springs', '春', '.spring', 'fall', '春意', ' Springs', '夏', ' summer', ' Fall', ' fall', '\tSpring', '春的', ' autumn', '.Spring', ' primavera', ' FALL', '(Spring', '弹簧', ' Summer', '봄', '春天', '春天的', 'Fall', '.springframework', ' printemps', ' Вес', ' вес']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: ['___', '__', 'Spring', '春季', ' Spring', '**', '____', ' spring', ' **', ' printemps', '雨季', 'spring', ' rainy', ' ___', '__:', '干旱', '__.', ' __', ' summer', '__)', '春暖花开', '春天', '夏季', ' primavera', '淡季', '季节', '旺季', '次年', '_____', '旱', '’**', '**.']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['udu', 'oe', 'zn', '义', 'zt', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', 'ute', '中和', '钦', ' ficará', '投资有限公司', 'ud', 'corr', 'AYS', '发', 'uz', 'zz', 'udy', 'itu', '5', '2', '発表した', ' Entrega', 'rait', '说法', 'äs', 'uto']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', 'ute', '2', 'l', 'oe', 'zt', 'ug', 'ere', '4', '1', 'ill', 'os', 'se', 'im', 'id', '处', 'ort', 'ud', 'ur', 'endants', 'zz', '义', 'usr', 'je', 'ills', '3', '5', ' +', '8', 'rie', 'ounds', 'od']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'winter<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', '+z', ' franz', '+",', '"\\', '.#']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

J-lens: [' red', ' purple', '红色', ' green', ' pink', ' blue', ' black', ':red', ' redd', 'green', 'black', 'blue', ' yellow', 'purple', 'pink', '红色的', ' Purple', ' brown', ' violet', '黑色的', ' orange', ' crimson', '黑色', '_red', '蓝色', '-red', 'red', ' dark', '绿色', '(red', ' rouge', ' Red']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

plain lens: [':red', ' reda', '…**', '红了', ' warta', ' สี', ' pales', 'меется', 'acin', 'мали', 'imson', 'acre', '_red', 'isers', 'geries', 'bán', '眯眯', ' крас', 'lep', ' утвер', ' Rowling', '同期的', ' uby', ' berüh', 'rosa', '红色', ' setBackgroundColor', '加拿大的', ':green', ' 스위트', '红颜', '及配件']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass J-lens: [' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', 'green', 'black', 'blue', ' yellow', 'pink', 'purple', '红色的', ' Purple', ' brown', '黑色的', ' orange', ' violet', ' crimson', '黑色', '_red', '蓝色', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass logit contrast J-lens: [' Colors', ' COLORS', ' colors', '颜色', ' **—', ' Yellow', '_colors', ' Purple', ' kolor', ' **■', ' colours', '蓝色的', '颜色的', ' YELLOW', '的颜色', ' Colour', ' colorful', ' purple', '黄色的', ' Brown', ' Cà', '_COLOR', ' Basta', ' *–', '/colors', ' colored', ' darker', ' **:**', '黄色', ' Eggs', ' Blacks', '.colors']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass probability contrast J-lens: [' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', ' yellow', 'blue', 'green', '红色的', 'purple', 'pink', ' Purple', ' brown', ' orange', ' violet', '黑色的', ' crimson', '黑色', '蓝色', '_red', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black', ':green']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass plain24: [':red', '…**', '红了', ' pales', ' สี', 'меется', ' warta', 'acin', 'мали', 'imson', 'acre', 'geries', '_red', 'isers', 'bán', '眯眯', ' крас', ' Rowling', 'lep', ' утвер', '同期的', ' berüh', ' uby', '红色', ' setBackgroundColor', 'rosa', '加拿大的', ':green', ' 스위트', ' сбы', '及配件', '红颜']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass logit contrast plain24: [' Sán', ' warta', ' webb', ' sacerdo', ' 웹사이트가', '套件', 'intervista', ' Blasio', 'veux', ' Parcheggio', ' Annunci', ' Ejem', ' Ilmais', '-lnd', 'acza', 'Besøg', 'église', 'eceğ', '成功后即可', ' BHY', '投资事件', 'ouvrez', ' Contras', ' Kasich', 'eceğini', 'estens', '迪士', ' contac', 'éclairage', 'ESSO', 'iciels', ' egt']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass probability contrast plain24: [':red', '…**', '红了', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'imson', 'acre', 'geries', 'isers', 'bán', '_red', '眯眯', ' Rowling', ' утвер', 'lep', ' крас', '同期的', ' uby', ' berüh', ' setBackgroundColor', 'rosa', '加拿大的', '红色', ' 스위트', ':green', ' Eventi', '及配件', ' сбы']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass plain27: [':red', '红色', ' крас', 'imson', '…**', '_red', ' pales', 'мали', '通红', 'สีแดง', '紅色', 'acre', '红的', '.red', ' berüh', '红色的', '红了', ' الأحمر', '加拿大的', '本题考查', '\xa0\xa0\xa0', '-red', ' kı', '(red', '”…', ' czerw', 'acin', '红线', ' warta', 'struments', '五颜六色的', ':green']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass logit contrast plain27: [' webb', '埔寨', ' warta', ' Parcheggio', ' Juta', '=length', ' Ilmais', '乐乎', '套件', ' sacerdo', ' Habitaciones', 'aéroport', ' duga', 'iciels', 'onents', 'izzano', ' просмо', 'veux', '罪魁', '駅徒歩', ' Annunci', ' Fonse', ' изыска', ' Безу', '手术室', ' Attra', '锦涛', 'estens', ' kebe', 'ouvrez', 'yerek', 'ESSO']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass probability contrast plain27: [':red', '红色', ' крас', 'imson', '…**', '_red', ' pales', '通红', 'мали', 'สีแดง', '紅色', ' berüh', 'acre', '红的', '.red', '红色的', ' الأحمر', '红了', '加拿大的', '本题考查', '\xa0\xa0\xa0', ' kı', '(red', '-red', '”…', 'acin', ' czerw', ' warta', '红线', 'struments', '五颜六色的', ':green']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass negative final control: ['intervista', ' Ez', 'щность', 'erstellen', ' Wo', ' conforta', 'olja', ' جوز', '_MB', ' Descar', 'ulangan', ' Показа', 'ekre', ' sela', 'éclairage', 'iesto', 'ดน', ' هی', 'ilhar', ' mh', ' tx', ' Parlam', 'úz', "।'", ' Компа', 'ЕК', ' рассматри', ' MG', ' *–', ' Pey', 'olib', ' library']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased1 J-lens: [' purple', ' green', ' pink', ' black', '黑色的', ' blue', ' Purple', ' violet', ' dark', ' brown', '黑色', ' yellow', 'pink', 'purple', '蓝色', '…**', ':black', 'black', ' orange', '的颜色', '绿色', 'green', ':green', '绿色的', ' **', '颜色', ' Colors', ' Pink', ' darker', 'blue', '白色的', ' gray']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased0.5 J-lens: [' purple', ' green', ' pink', ' black', ' blue', '黑色的', ' Purple', ' violet', ' yellow', '红色', 'pink', 'purple', ' brown', 'black', 'green', '黑色', ' orange', ':red', ' dark', 'blue', '蓝色', '绿色', ':black', ' crimson', '的颜色', ':green', '绿色的', 'brown', ' Pink', '…**', '红色的', ' gray']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased1 plain24: ['…**', ' warta', 'меется', ' pales', ':red', ' สี', 'acin', 'acre', 'мали', 'bán', 'isers', '眯眯', 'geries', ' Rowling', ' uby', 'imson', '同期的', '加拿大的', ' setBackgroundColor', 'lep', ' утвер', ' 스위트', 'ogna', ' berüh', 'の販', ' Liebl', ' Eventi', 'iciels', ' сбы', 'ائع', '죄', ' zove']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased0.5 plain24: [':red', '…**', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '同期的', '红了', ' утвер', 'lep', ' uby', '加拿大的', ' setBackgroundColor', ' berüh', ' 스위트', 'rosa', ' Eventi', 'iciels', '及配件', ' сбы', 'の販', 'ائع', '죄']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased1 plain27: ['…**', 'imson', ':red', ' pales', 'acre', '加拿大的', 'мали', '”…', ' berüh', ' warta', ' крас', '五颜六色的', '本题考查', 'struments', 'acin', '\xa0\xa0\xa0', 'eiß', '{}".', ' Eintritt', '죄', '如荼', '../../../../', '红色', '各种各样', 'dling', 'ceptive', ' kı', ':green', ' сбы', '通红', '])**', '=length']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass erased0.5 plain27: [':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', '通红', '\xa0\xa0\xa0', ' warta', 'acin', '五颜六色的', 'struments', 'สีแดง', ' kı', '_red', 'eiß', ' الأحمر', '如荼', ' Eintritt', '../../../../', ':green', '죄', '{}".', ' сбы', '各种各样', ' утвер']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' purple', ' green', ' pink', ' black', ' blue', '黑色的', ' Purple', ' violet', ' yellow', '红色', 'pink', 'purple', ' brown', 'black', 'green', '黑色', ' orange', ':red', ' dark', 'blue', '蓝色', '绿色', ':black', ' crimson', '的颜色', ':green', '绿色的', 'brown', ' Pink', '…**', '红色的', ' gray']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix erased0.5 plain24: [':red', '…**', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '同期的', '红了', ' утвер', 'lep', ' uby', '加拿大的', ' setBackgroundColor', ' berüh', ' 스위트', 'rosa', ' Eventi', 'iciels', '及配件', ' сбы', 'の販', 'ائع', '죄']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix erased0.5 plain27: [':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', '通红', '\xa0\xa0\xa0', ' warta', 'acin', '五颜六色的', 'struments', 'สีแดง', ' kı', '_red', 'eiß', ' الأحمر', '如荼', ' Eintritt', '../../../../', ':green', '죄', '{}".', ' сбы', '各种各样', ' утвер']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix J-lens: [' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', 'green', 'black', 'blue', ' yellow', 'pink', 'purple', '红色的', ' Purple', ' brown', '黑色的', ' orange', ' violet', ' crimson', '黑色', '_red', '蓝色', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix J-lens: [' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', 'apple', ' mushrooms', '苹果', '樱桃', ' candies', ' sweets', ' candy', '苹果的', '毒药', ' cakes', ' carrots', '剧毒', ' poisoning', ' grapes', ' Apfel', ' fairy', ' cherry', '-*-', '/apple', 'Apple', 'cakes', '草莓', ' chocolates', '毒']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: [' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', 'apple', ' candies', '苹果', ' sweets', '樱桃', ' candy', '毒药', '苹果的', ' cakes', ' poisoning', '剧毒', ' carrots', ' grapes', ' Apfel', ' fairy', '-*-', ' cherry', 'cakes', '/apple', 'Apple', ' **【', ' chocolates', ' bananas']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['меется', '一整', '中毒', '￣', '整座', 'uentes', '连心', '�', '颗星', '时许', '迈着', '现实中', '头等', '剧毒', ' вред', 'lips', 'eware', '_topology', 'integration', '块的', 'IDI', '这颗', ' اشت', ' poisoning', '倾心', '机械设计', '现实的', '一口', '常温', 'okin', 'Fatal', ' berries']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: [' apple', '苹果', ' apples', 'apple', '中毒', ' poisoning', 'Apple', '苹果的', '毒', ' Apple', ' poisonous', '.apple', ' APPLE', ' ябло', '_app', 'แอป', '-po', 'พิษ', 'APPLE', '-app', ' po', '剧毒', '苹果公司', '蘋果', ' 사과', ' созре', '_APP', 'app', 'Org', ' app', '有毒', '(app']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', '+)\\', '\\",\\"', ' \\"{', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'uth', 'ute', 'os', '中和', '钦', '投资有限公司', ' ficará', 'ud', 'corr', 'AYS', 'udy', 'uz', '発表した', 'itu', 'zz', '发', ' Entrega', 'rait', 'uto', 'äs', '说法', 'eme', '2']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', 'ute', '2', 'l', '4', '1', 'oe', 'ug', 'zt', 'ere', 'os', 'ill', 'se', 'im', 'id', '3', '5', '处', 'ort', 'ud', '8', 'ur', ' +', 'zz', 'je', '义', 'usr', 'ills', ' at', 'endants', ' (', '0']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' purple', ' green', ' black', ' pink', ' blue', '黑色的', ' Purple', ' violet', ' yellow', 'black', '黑色', ' brown', 'purple', '红色', ' dark', 'pink', 'green', ' orange', '蓝色', ':red', ':black', '…**', 'blue', '绿色', ':green', '绿色的', ' Pink', ' **', '的颜色', ' crimson', ' GREEN', ' Green']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: [':red', '…**', 'меется', ' pales', ' warta', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '红了', 'lep', '同期的', ' uby', ' утвер', '加拿大的', ' berüh', ' setBackgroundColor', 'rosa', ' Eventi', ' 스위트', '及配件', ' сбы', ' Liebl', 'ائع', '죄', 'iciels']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: [':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', ' warta', '\xa0\xa0\xa0', '通红', 'acin', 'struments', '五颜六色的', ' kı', 'สีแดง', '如荼', 'eiß', '_red', '../../../../', ' الأحمر', ':green', ' Eintritt', '죄', '{}".', ' утвер', ' сбы', 'dling']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' purple', ' green', ' pink', ' blue', ' black', 'pink', ' yellow', ' violet', '红色', ' Purple', ':red', ' orange', 'green', 'purple', '黑色的', ' brown', 'blue', ' dark', 'black', '蓝色', '黑色', ' crimson', '绿色', '的颜色', ' rouge', ' Pink', 'brown', ' gray', ':black', '…**', '绿色的', 'orange']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: [' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', '苹果', ' candies', ' sweets', 'apple', '樱桃', '苹果的', '毒药', '剧毒', ' candy', ' cakes', ' poisoning', ' carrots', ' Apfel', ' grapes', ' fairy', '-*-', '/apple', 'cakes', ' cherry', ' chocolates', '毒', ' **【', '-**']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['меется', '一整', '中毒', '￣', '整座', 'uentes', '连心', '�', '颗星', '时许', '迈着', '现实中', '头等', '剧毒', ' вред', 'lips', 'eware', '_topology', 'integration', '块的', 'IDI', '这颗', ' اشت', ' poisoning', '机械设计', '倾心', '现实的', '一口', '常温', 'okin', 'Fatal', ' berries']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: [' apple', '苹果', ' apples', 'apple', '中毒', ' poisoning', 'Apple', '苹果的', '毒', ' Apple', ' poisonous', '.apple', ' APPLE', ' ябло', '_app', 'แอป', '-po', 'พิษ', 'APPLE', '-app', ' po', '剧毒', '苹果公司', '蘋果', ' 사과', ' созре', '_APP', 'app', 'Org', ' app', '有毒', '(app']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: [' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', '苹果', ' candies', 'apple', ' sweets', '樱桃', ' candy', '苹果的', ' carrots', '剧毒', ' poisoning', '毒药', ' cakes', ' grapes', ' Apfel', ' fairy', 'cakes', '-*-', '毒', 'Apple', ' cherry', '/apple', '草莓', ' bananas']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', ' franz', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['udu', 'oe', 'zn', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'uth', 'ute', 'os', '中和', '钦', '投资有限公司', ' ficará', 'ud', 'corr', 'AYS', 'udy', 'uz', '発表した', 'itu', 'zz', '发', ' Entrega', 'rait', 'uto', 'äs', '说法', 'eme', '2']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', 'ute', '2', 'l', '4', '1', 'oe', 'ug', 'zt', 'ere', 'os', 'ill', 'se', 'im', 'id', '3', '5', '处', 'ort', 'ud', '8', 'ur', ' +', 'zz', 'je', '义', 'usr', 'ills', ' at', 'endants', ' (', '0']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'red<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: [',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', '+)\\', '\\",\\"', ' \\"{', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', ' nube', '云彩', '的云', '云服务', '云端', '乌云', '云海', '浮云', ' fog', 'クラウド', ' 클라우드', ' skies', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

plain lens: ['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '/cloud', '云层', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', ' mây', '云雾', '云计算', 'クラウド', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '云平台']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', 'クラウド', '浮云', ' 클라우드', ' skies', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass logit contrast J-lens: [' clouds', ' cloud', ' Cloud', ' fog', ' mây', ' pond', ' râ', ' solar', ' jelly', ' podr', ' cloudy', ' înd', ' skies', '云层', ' sky', ' pé', ' waterfall', ' hyd', '/cloud', '喜马拉雅', ' sod', '.SO', '雲', ' river', ' rivers', '火箭', ' peta', '-cloud', ' rady', ' Sod', ' spider', ' Bagno']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass probability contrast J-lens: [' clouds', 'cloud', ' cloud', 'Cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', ' mây', '云雾', ' cloudy', ' обла', '.Cloud', '的云', '云彩', ' fog', '云端', ' skies', '浮云', '乌云', '白云', '雾', ' sky', '云平台', ' rain', ' 클라우드']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass plain24: ['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '/cloud', '云层', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', ' mây', '云雾', '云计算', 'クラウド', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '云平台']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass logit contrast plain24: [' sod', '.SO', ' peta', '可乐', ' Arro', ' rada', '博格', 'วิทย', ' rota', ' pio', ' titular', 'OPY', ' pena', ' tenda', ' onda', 'ugd', ' rasa', ' genü', ' Sod', ' pond', ' radi', ' Marina', ' sca', ' kust', ' râ', ' toko', ' stacks', ' pods', 'افي', ' 박', '응', ' prezi']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass probability contrast plain24: ['cloud', '_cloud', ' clouds', '-cloud', 'Cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '.Cloud', '/cloud', ' обла', '雲', '云彩', '云朵', '云服务', ' mây', '云雾', '云计算', 'クラウド', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '天空', '的云', '白云', '云平台']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', '的云', '.cloud', ' cloudy', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' 클라우드', ' mây', '云中', '云平台', '云服务器']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass logit contrast plain27: [' cloud', ' Cloud', '云', ' clouds', '云的', '雲', '的云', ' sod', ' marg', ' genü', '白云', ' cloudy', '连云', ' Алла', ' pond', ' lax', '-cloud', '可乐', ' tenda', ' fog', ' Mary', ' jug', ' rent', ' Mine', '云层', ' pio', ' pods', ' Marina', ' rada', ' har', 'ий', ' barr']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass probability contrast plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', '的云', ' cloudy', '.Cloud', ' обла', '云端', '云朵', '/cloud', '云天', '云计算', 'クラウド', '白云', '云上', ' mây', ' 클라우드', '云中', '云平台', '云飞', '连云', '雾', '浮云']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass negative final control: [' Aga', ' poda', ' Kak', ' TAR', ' Hid', ' Poly', ' sod', '裕', ' Sh', ' Locker', ' hooks', ' Bee', ' Rod', '小马', ' Pick', ' asim', ' Socket', 'uga', ' Addison', 'AMA', '狩', ' Alexander', ' vara', '马拉', ' skall', ' Root', '乔丹', '卡拉', ' Fora', '老妈', ' hyd', ' lax']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased1 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云雾', '云', '云朵', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', ' skies', '浮云', 'クラウド', ' 클라우드', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased0.5 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云', '云朵', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', ' skies', '浮云', 'クラウド', ' 클라우드', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased1 plain24: ['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '/cloud', '云层', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', ' mây', '云雾', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '天空', '云端', '的云', '白云', '人民医院']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased0.5 plain24: ['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '/cloud', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', '云雾', ' mây', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '人民医院']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased1 plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', '/cloud', ' обла', '云端', '云朵', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', '云中', ' mây', ' 클라우드', '云平台', '云服务器']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass erased0.5 plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' 클라우드', ' mây', '云中', '云平台', '云服务器']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云', '云朵', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', ' skies', '浮云', 'クラウド', ' 클라우드', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '/cloud', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', '云雾', ' mây', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '人民医院']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' 클라우드', ' mây', '云中', '云平台', '云服务器']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', 'クラウド', '浮云', ' 클라우드', ' skies', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix J-lens: ['德语', ' meaning', ' **„', '单词', 'German', '这个词', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', ' meanings', ' Translate', 'Translate', 'meaning', '翻译成', '意思', ' слово', 'cloud', ' Cloud', '云', ' palavra', ':\\"', ' palabra', '含义', '的意思是']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: ['德语', ' meaning', ' **„', '单词', 'German', '这个词', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', ' meanings', ' Translate', 'Translate', '翻译成', 'meaning', '意思', ' слово', '云', ' Cloud', ' palavra', 'cloud', ':\\"', ' palabra', '的意思是', '含义']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['_cloud', ' translates', '意为', '云', ' meaning', '云服务', '云的', ' перево', ' translated', '#w', '对应的', ' แปล', 'แปล', ' vols', '意思是', 'translated', 'Translate', ' traduc', '的意思是', '-word', 'cloud', 'translate', ' translate', '意思', ' traduz', '翻译', 'meaning', '"w', ' meanings', ' ترجمة', '匹', 'apus']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: ['云', '_cloud', 'cloud', '-word', '云的', ' cloud', '词', '_word', 'Cloud', '雲', ' clouds', ' Cloud', ' meaning', '单词', '云彩', '.word', ' palavra', '-cloud', '云服务', ' cloudy', '云上', '这个词', ' palabra', ' слово', 'meaning', '(word', '字', '的词', '云平台', '字的', '云计算', '/cloud']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', '?\\', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', ' \\"{', '\\",\\"', '+)\\', ' franz', '."),', '>\\', '+z', '"\\', '.#', '+",']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ':\\"', ').\\', ' **„', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '"\\', '>\\', '.#', '."),', '+z', ')”']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', ' ficará', '投资有限公司', 'corr', '中和', '钦', 'ute', 'AYS', 'itu', 'ud', 'uz', 'zz', '発表した', 'udy', 'rait', ' Entrega', '发', 'uto', 'äs', 'eme', '说法', '有关人员']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', 'ute', '2', 'in', 'l', '4', 'oe', 'ug', '1', 'zt', 'ere', 'os', 'se', 'ill', 'im', 'id', '3', 'ort', '5', 'ud', '处', 'ur', 'je', 'zz', '8', '义', ' +', 'usr', 'ills', 'endants', ' at', '0']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', 'クラウド', '浮云', ' skies', ' 클라우드', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: ['cloud', '_cloud', 'Cloud', '-cloud', ' clouds', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '/cloud', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', '云雾', ' mây', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '人民医院']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: ['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' mây', ' 클라우드', '云中', '云平台', '云服务器']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '的云', '云彩', '云服务', '云端', '乌云', '云海', ' fog', ' 클라우드', 'クラウド', ' skies', '浮云', '云中', '云计算']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: ['德语', ' meaning', ' **„', '单词', '这个词', 'German', '翻译', ' Meaning', ' translates', '_cloud', ' German', ' translated', ' translate', '意为', '-word', 'Cloud', '_word', ' Translate', '翻译成', ' meanings', '意思', ' слово', 'Translate', 'meaning', '云', ' Cloud', ':\\"', ' palavra', 'cloud', ' palabra', '的意思是', '含义']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['_cloud', ' translates', '意为', '云', ' meaning', '云服务', '云的', ' перево', ' translated', '#w', '对应的', ' แปล', 'แปล', ' vols', '意思是', 'translated', 'Translate', ' traduc', '的意思是', '-word', 'cloud', 'translate', ' translate', '意思', ' traduz', '翻译', 'meaning', '"w', ' meanings', ' ترجمة', '匹', 'apus']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: ['云', '_cloud', 'cloud', '-word', '云的', ' cloud', '词', '_word', 'Cloud', '雲', ' clouds', ' Cloud', ' meaning', '单词', '云彩', '.word', ' palavra', '-cloud', '云服务', ' cloudy', '云上', ' слово', '这个词', ' palabra', 'meaning', '(word', '字', '的词', '云平台', '字的', '云计算', '/cloud']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: ['德语', ' meaning', ' **„', '单词', '这个词', 'German', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', 'Translate', '翻译成', ' Translate', 'meaning', ' слово', ' meanings', '意思', ' palavra', ' Cloud', 'cloud', ':\\"', '云', ' palabra', '的意思是', '含义']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: ['+\\', ',\\"', '):\\', '.\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ' **„', ').\\', ':\\"', ' **“', ',\\', '\\"\\', '\\")', ')\\', '*\\', ',”', ',__', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '."),', '+z', ')”', '+",', '>\\', '"\\']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', ' ficará', '投资有限公司', 'ute', '中和', 'corr', 'AYS', 'itu', '钦', 'ud', 'uz', 'zz', '発表した', 'udy', 'rait', ' Entrega', '发', 'uto', 'äs', 'eme', '说法', '有关人员']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', 'ute', '2', 'in', 'l', '4', 'oe', 'ug', '1', 'zt', 'ere', 'os', 'se', 'ill', 'im', 'id', '3', 'ort', '5', 'ud', '处', 'ur', 'je', 'zz', '8', '义', ' +', 'usr', 'ills', 'endants', ' at', '0']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'nuage<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: ['+\\', ',\\"', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', ')\\', '*\\', ',”', ',__', ':+', '\\",\\"', '+)\\', ' franz', ' \\"{', '+z', '"\\', '.#', '."),', '>\\', 'uz']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

J-lens: [' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '云层', '_cloud', '.cloud', '雲', '/cloud', '云雾', '云', '云的', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', ' Weather', ' Fog', 'クラウド', '“']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

plain lens: ['cloud', 'Cloud', '_cloud', ' Cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '/cloud', '云的', '云', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '云服务', 'opies', '�', '云彩', '云雾', '加拿大的', 'ungkapkan', '云山', '多云', '習', '云天', '云朵', 'abut', ' mây', 'veux']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass J-lens: [' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '云层', '_cloud', '.cloud', '雲', '/cloud', '云雾', '云', '云的', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', ' Weather', ' Fog', 'クラウド', '“']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass logit contrast J-lens: [' Mountains', ' Cloud', ' Magical', ' Root', ' Airways', ' Another', ' Shadows', ' Buildings', ' Moon', ' Roof', ' Roots', ' Con', ' Engine', ' Natural', ' Vert', ' Cap', ' Mother', ' Dreams', ' Isles', ' Creatures', ' Gods', ' Mountain', '*”', ' Animals', ' Air', ' clouds', ' Tower', ' City', ' Void', ' Nature', ' Imag', ' Noise']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass probability contrast J-lens: [' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', ' Weather', ' Fog', 'クラウド', ' Rain']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass plain24: ['cloud', 'Cloud', '_cloud', ' Cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '/cloud', '云的', '云', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '云服务', 'opies', '�', '云彩', '云雾', '加拿大的', 'ungkapkan', '云山', '多云', '習', '云天', '云朵', 'abut', ' mây', 'veux']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass logit contrast plain24: ['ительства', 'ervations', ' rute', ' byd', 'ysi', '-animate', ' saj', 'ugd', 'adě', '馒', 'ито', ' Mother', ' Muit', ' gry', '-ves', ' Albums', '在售', 'lables', 'sgi', 'peater', '勇', 'OCUMENT', 'encontre', 'ingas', '같', ' Fora', ' Осно', ' Progress', 'pread', ' Characters', ' bov', ' sod']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass probability contrast plain24: ['cloud', ' Cloud', '_cloud', 'Cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '/cloud', '云的', '云', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '云服务', 'opies', '�', '云彩', '加拿大的', 'ungkapkan', '云雾', '云山', '多云', '習', '云朵', '云天', 'abut', 'ĂNG', 'veux']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', '云服务', ' обла', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '云服务器', '白云', ' nube', 'クラウド', ' 클라우드', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass logit contrast plain27: [' Cloud', ' cloud', '云', ' clouds', '云的', '的云', '_cloud', ' Mother', '白云区', 'ervations', 'cloud', ' Mapping', ' Marg', ' saj', ' Over', '云服务', '雲', '云上', '白云', '青云', ' Minor', 'ито', ' mây', ' gry', ' Équip', ' BU', '-cloud', ' Motor', '养', '云飞', ' Capital', ' Py']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass probability contrast plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', '云服务', ' обла', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '云服务器', '白云', ' nube', 'クラウド', ' 클라우드', '云上']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass negative final control: [' Marg', ' Pi', ' Cutting', ' Capital', ' Prime', 'ortable', ' Orders', ' PI', ' Vector', ' Energy', ' Root', ' Do', 'yiz', ' VD', ' cap', ' gi', ' mata', ' Another', ' Ri', 'ipasi', ' From', ' Mother', ' Out', ' Con', ' Inside', ' salg', ' sup', ' pi', ' Three', ' sin', ' pud', ' Does']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased1 J-lens: [' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云朵', '云', ' mây', ' nube', '.Cloud', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云海', '云端', ' Meteor', '云服务', 'クラウド', ' Fog', ' Nimbus', ' Weather']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased0.5 J-lens: [' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', '云服务', ' Meteor', ' Weather', 'クラウド', ' Nimbus', ' Fog']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased1 plain24: ['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '云', ' clouds', '.Cloud', '雲', '/cloud', ' обла', '云的', '云层', '凝结', '.cloud', ' trots', '�', '云服务', '云彩', 'opies', '云雾', '多云', '云朵', '云山', '習', '凝', '云天', 'ungkapkan', '夢', ' mây', '天空']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased0.5 plain24: ['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '云', '/cloud', '云的', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '�', '云服务', 'opies', '云彩', '云雾', '多云', '云山', 'ungkapkan', '習', '云朵', '云天', '凝', 'abut', '加拿大的', ' mây']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased1 plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', '云服务', ' обла', '/cloud', ' cloudy', '云天', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '云服务器', '白云', ' nube', 'クラウド', ' 클라우드', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass erased0.5 plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', ' обла', '云服务', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '白云', '云服务器', ' nube', 'クラウド', ' 클라우드', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', '云服务', ' Meteor', ' Weather', 'クラウド', ' Nimbus', ' Fog']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '云', '/cloud', '云的', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '�', '云服务', 'opies', '云彩', '云雾', '多云', '云山', 'ungkapkan', '習', '云朵', '云天', '凝', 'abut', '加拿大的', ' mây']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix erased0.5 plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', ' обла', '云服务', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '白云', '云服务器', ' nube', 'クラウド', ' 클라우드', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix J-lens: [' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '云层', '_cloud', '.cloud', '雲', '/cloud', '云雾', '云', '云的', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', ' Weather', ' Fog', 'クラウド', '“']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix J-lens: ['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '日语', '英语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', '法國', ' Italian', '翻译', '翻译成', 'Spanish', '韩语', ' spanish', ' 프랑스', ' Portuguese', ' немец', '瑞士']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix erased0.5 J-lens: ['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '英语', '日语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', '翻译', '法國', ' Italian', 'Spanish', '翻译成', '韩语', ' Portuguese', ' 프랑스', ' spanish', '日本語', ' немец']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix erased0.5 plain24: ['法语', '英语', 'French', ' translates', '德语', ' French', '对应的', ' translated', '翻译成', '-word', '翻译', '罗曼', 'iền', ' meanings', '意为', '汉语', 'Translate', ' untranslated', 'แปล', ' translators', ' Romance', '慕尼', ' перево', 'Rech', '日语', 'nameof', 'English', ' translate', '当て', '_nb', ' meaning', 'rench']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix erased0.5 plain27: ['-word', '法语', '英语', 'French', ' French', '单词', '.word', '_word', ' palavra', '词', ' meaning', ' слово', '字的', '中文', ' noun', '德语', '[word', ' француз', ' كلمة', '这个词', ' fransk', 'meaning', ' English', ' palabra', '翻译成', '一词', 'means', '字', '(word', ' فرن', 'English', '韩语']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', '?\\', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', ' \\"{', '\\",\\"', '+)\\', ' franz', '."),', '>\\', '+z', '"\\', '.#', '+",']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix erased0.5 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', '?\\', ' **„', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '>\\', '"\\', '+z', '."),', '.#', ')”']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix erased0.5 plain24: ['oe', 'zn', 'udu', '义', 'zt', 'ug', 'aaaa', 'utt', 'os', 'itz', '2', 'uth', 'ute', 'ud', '5', '中和', '钦', 'uz', 'zz', '发', ' ficará', '投资有限公司', 'corr', 'udy', 'itu', 'AYS', '8', '4', 'uto', 'eme', '说法', 'rait']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix erased0.5 plain27: ['ia', '2', 'ute', 'in', 'l', '1', '4', 'ug', 'oe', 'zt', 'ere', '3', 'os', 'se', 'im', 'id', '5', 'ill', '8', 'ort', 'ur', ' +', 'ud', '处', 'je', 'zz', '0', ' (', '义', '9', '^', ' at']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix metric-erased0.5 J-lens: [' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', ' nube', '.Cloud', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云海', '云端', ' Meteor', '云服务', 'クラウド', ' Himmel', ' Weather', ' Fog']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix metric-erased0.5 plain24: ['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '云', '/cloud', '云的', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '云服务', '�', 'opies', '云彩', '云雾', '多云', '云山', '云朵', '習', 'ungkapkan', '云天', '凝', '加拿大的', 'abut', ' mây']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix metric-erased0.5 plain27: [' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', '云服务', ' обла', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '云服务器', '白云', ' nube', 'クラウド', ' 클라우드', '云中']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass input-prefix metric-erased0.5 random0 J-lens: [' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云朵', '云', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', 'クラウド', ' Nimbus', ' Weather', ' Fog']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 J-lens: ['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', ' English', '汉语', '英语', '日语', ' француз', 'English', ' Spanish', '西班牙语', '俄语', ' english', ' francés', ' francese', 'Spanish', ' francês', '翻译成', '翻译', '法國', ' Italian', '韩语', ' spanish', ' 프랑스', ' Portuguese', '日本語', ' немец']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain24: ['法语', '英语', 'French', ' translates', '德语', ' French', '对应的', ' translated', '翻译成', '-word', '翻译', '罗曼', 'iền', '意为', '汉语', ' meanings', ' untranslated', 'Translate', '慕尼', 'แปล', ' translators', 'Rech', ' перево', ' Romance', 'nameof', ' translate', 'English', '日语', '当て', '_nb', 'rench', ' meaning']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 plain27: ['-word', '法语', '英语', 'French', ' French', '单词', '.word', '_word', ' palavra', '词', ' meaning', ' слово', '字的', '中文', ' noun', '德语', '[word', ' француз', ' كلمة', '这个词', ' fransk', 'meaning', ' palabra', '翻译成', '一词', ' English', 'means', '字', '(word', '韩语', ' فرن', 'English']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass boundary input-prefix metric-erased0.5 random0 J-lens: ['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '日语', '英语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', ' Italian', '翻译', '法國', '翻译成', 'Spanish', ' Portuguese', ' 프랑스', '韩语', '日本語', ' spanish', ' немец']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ':\\"', ').\\', ' **„', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',”', ':+', ',__', '\\",\\"', ' \\"{', '+)\\', ' franz', '"\\', '."),', '.#', '>\\', '+z', '+",']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain24: ['oe', 'udu', 'zn', '义', 'zt', 'ug', 'aaaa', 'utt', 'itz', 'os', 'uth', '2', 'ud', 'ute', '中和', '5', '钦', ' ficará', 'zz', 'uz', '发', 'corr', '投资有限公司', 'udy', 'AYS', 'itu', '8', 'uto', '说法', '発表した', 'eme', 'rait']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 plain27: ['ia', '2', 'ute', 'in', 'l', '1', '4', 'ug', 'oe', 'zt', 'ere', 'os', '3', 'se', 'im', 'id', 'ill', '5', '8', 'ur', 'ud', '处', 'ort', ' +', 'je', 'zz', '0', '义', ' (', ' at', '9', '^']

Input: '<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'Wolke<|im_end|>'

end-pass preclue input-prefix metric-erased0.5 random0 J-lens: [',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', '?\\', ' **„', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',”', ':+', ',__', ' \\"{', '\\",\\"', '+)\\', '+z', '>\\', '"\\', ' franz', '."),', '.#', '+",']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Actual-output lexical-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [J-lens](readout.json)     | 1/6                    |    0.319 | 1/5                      | 1/6                            |          1 |
| [plain lens](readout.json) | 1/6                    |    0.409 | 1/5                      | 1/6                            |          1 |

### End-of-pass readout (not for earlier edits)

| method                                                                         | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:-------------------------------------------------------------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [end-pass erased1 plain27](readout.json)                                       | 4/6                    |    0.850 | 3/5                      | 4/6                            |          1 |
| [end-pass J-lens](readout.json)                                                | 3/6                    |    0.834 | 2/5                      | 4/6                            |          1 |
| [end-pass probability contrast J-lens](readout.json)                           | 3/6                    |    0.657 | 2/5                      | 4/6                            |          1 |
| [end-pass plain27](readout.json)                                               | 3/6                    |    0.832 | 2/5                      | 4/6                            |          1 |
| [end-pass probability contrast plain27](readout.json)                          | 3/6                    |    0.789 | 2/5                      | 4/6                            |          1 |
| [end-pass erased0.5 J-lens](readout.json)                                      | 3/6                    |    0.848 | 2/5                      | 4/6                            |          1 |
| [end-pass erased0.5 plain27](readout.json)                                     | 3/6                    |    0.840 | 3/5                      | 3/6                            |          1 |
| [end-pass input-prefix erased0.5 J-lens](readout.json)                         | 3/6                    |    0.848 | 2/5                      | 4/6                            |          1 |
| [end-pass input-prefix erased0.5 plain27](readout.json)                        | 3/6                    |    0.840 | 3/5                      | 3/6                            |          1 |
| [end-pass input-prefix J-lens](readout.json)                                   | 3/6                    |    0.834 | 2/5                      | 4/6                            |          1 |
| [end-pass boundary input-prefix J-lens](readout.json)                          | 3/6                    |    0.831 | 2/5                      | 4/6                            |          1 |
| [end-pass boundary input-prefix erased0.5 J-lens](readout.json)                | 3/6                    |    0.831 | 2/5                      | 3/6                            |          1 |
| [end-pass boundary input-prefix erased0.5 plain27](readout.json)               | 3/6                    |    0.838 | 3/5                      | 3/6                            |          1 |
| [end-pass input-prefix metric-erased0.5 J-lens](readout.json)                  | 3/6                    |    0.850 | 2/5                      | 3/6                            |          1 |
| [end-pass input-prefix metric-erased0.5 plain27](readout.json)                 | 3/6                    |    0.841 | 3/5                      | 3/6                            |          1 |
| [end-pass input-prefix metric-erased0.5 random0 J-lens](readout.json)          | 3/6                    |    0.849 | 2/5                      | 4/6                            |          1 |
| [end-pass boundary input-prefix metric-erased0.5 plain27](readout.json)        | 3/6                    |    0.839 | 3/5                      | 3/6                            |          1 |
| [end-pass boundary input-prefix metric-erased0.5 random0 J-lens](readout.json) | 3/6                    |    0.839 | 2/5                      | 3/6                            |          1 |
| [end-pass boundary input-prefix metric-erased0.5 J-lens](readout.json)         | 2/6                    |    0.825 | 2/5                      | 2/6                            |          1 |
| [end-pass logit contrast J-lens](readout.json)                                 | 1/6                    |    0.909 | 1/5                      | 1/6                            |          1 |
| [end-pass plain24](readout.json)                                               | 1/6                    |    0.826 | 1/5                      | 1/6                            |          1 |
| [end-pass probability contrast plain24](readout.json)                          | 1/6                    |    0.694 | 1/5                      | 1/6                            |          1 |
| [end-pass logit contrast plain27](readout.json)                                | 1/6                    |    0.898 | 1/5                      | 1/6                            |          1 |
| [end-pass erased1 J-lens](readout.json)                                        | 1/6                    |    0.855 | 1/5                      | 1/6                            |          1 |
| [end-pass erased1 plain24](readout.json)                                       | 1/6                    |    0.840 | 1/5                      | 1/6                            |          1 |
| [end-pass erased0.5 plain24](readout.json)                                     | 1/6                    |    0.832 | 1/5                      | 1/6                            |          1 |
| [end-pass input-prefix erased0.5 plain24](readout.json)                        | 1/6                    |    0.832 | 1/5                      | 1/6                            |          1 |
| [end-pass input-prefix metric-erased0.5 plain24](readout.json)                 | 1/6                    |    0.833 | 1/5                      | 1/6                            |          1 |
| [end-pass logit contrast plain24](readout.json)                                | 0/6                    |    0.926 | 0/5                      | 0/6                            |          1 |
| [end-pass negative final control](readout.json)                                | 0/6                    |    0.943 | 0/5                      | 0/6                            |          1 |
| [end-pass boundary input-prefix erased0.5 plain24](readout.json)               | 0/6                    |    0.775 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix J-lens](readout.json)                           | 0/6                    |    0.910 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix erased0.5 J-lens](readout.json)                 | 0/6                    |    0.910 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix erased0.5 plain24](readout.json)                | 0/6                    |    0.955 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix erased0.5 plain27](readout.json)                | 0/6                    |    0.955 | 0/5                      | 0/6                            |          1 |
| [end-pass boundary input-prefix metric-erased0.5 plain24](readout.json)        | 0/6                    |    0.775 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix metric-erased0.5 J-lens](readout.json)          | 0/6                    |    0.916 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix metric-erased0.5 plain24](readout.json)         | 0/6                    |    0.956 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix metric-erased0.5 plain27](readout.json)         | 0/6                    |    0.955 | 0/5                      | 0/6                            |          1 |
| [end-pass preclue input-prefix metric-erased0.5 random0 J-lens](readout.json)  | 0/6                    |    0.907 | 0/5                      | 0/6                            |          1 |


## Held-scale native-metric erasure

Same half greedy-output-coordinate reduction, using G J Jᵀ G w (plain: G²w), without renormalization after correction. This minimizes native residual change only under held RMS scale. Output-space change is at least as large as ordinary projection. Primary J has a seed0 Gaussian control matched in requested output-space norm and coordinate, not realized BF16/native/score-space norms. All states, directions, raw scores and cast errors are in native_metric_readouts/. Original rows/states/generations reproduce metric_reproduction.json. — PI/OpenAI

## Fixed structural readout positions

Pre-assistant boundary and preclue user-header control use the same end-pass masks and final-greedy output direction. They are not information available to an earlier causal editor. Final-position scores reproduce within each capture; indices/prefixes and raw scores are in boundary_readouts/. — PI/OpenAI

### Case 0: December

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
January<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' **', ' Calendar', ' Year', ' Next', '事实', ' ...', '...', '次年', ' calendar', ' Tomorrow', ' Leap', '**', ' February', ' December', ' Future', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', '…', ' weeks', '(next', 'Calendar', ' Summer', '-month', ' Seasons', ' Holidays', ' Season', ' year']

end-pass input-prefix erased0.5 plain24:

['事实', '_fact', ' صدا', 'вис', 'orías', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', ' beleg', 'ヵ', 'の販', ' prekybos', ' факта', ':...', ' факт', '?...', 'ément', ' Situé', '探し', '…**', '...(', ' sacerdo', '事实上', 'eceğ', '小编为大家整理的']

end-pass input-prefix erased0.5 plain27:

['_Dec', '事实', '版权声明', '展望', '寒冷的', '冬', '腊', '闰', ' Ро', ' ...', ' December', '…', 'Leap', ' Empresarial', '越し', 'ajukan', ' Leap', 'Dec', '新年快乐', '乞', ' Dec', ' صدا', 'apt', ' Fakta', ' факта', 'December', '事實', '_dec', ' Yours', '...', '元旦', '赔']

end-pass input-prefix J-lens:

[' February', ' December', ' Calendar', ' Year', ' **', '事实', '次年', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' holidays', ' April', '/month', ' Seasons', '...**', ' weeks', 'December', '_year', ' Future', ' Season']

end-pass boundary input-prefix J-lens:

[' December', '月份', ' February', 'December', '次年', 'February', ' November', '-month', ' October', ' April', '_month', '当月', ' Calendar', ' Year', 'October', '/month', 'April', 'November', 'Calendar', '十二月', 'calendar', ' September', ' March', '___', '月份的', ' July', '.Month', '一个月', 'Year', '.month', '月底', 'September']

end-pass boundary input-prefix erased0.5 J-lens:

['月份', '次年', ' December', '___', '____', '__', '-month', ' Calendar', ' Year', '当月', ' February', '_month', 'Calendar', '**', 'calendar', '日历', ' Tomorrow', '一个月', ' November', ' ___', ' next', ' calendar', '闰', ' ____', ' October', 'next', '月底', ' April', '_*', '明年', '翌', ' Next']

end-pass boundary input-prefix erased0.5 plain24:

['unie', '圆梦', '籌', 'の販', '筹', ' sluts', '雰', ' eskort', '[image', ' قائ', '같', '問わず', 'ovem', '服务部', '路网', 'ISATION', 'ément', 'wali', 'ujuan', '订制', ' gee', ' cherchez', '日历', '拉开序幕', 'разу', ' Folg', 'ヵ', 'ฉาย', 'رفة', '_variation', 'lepší', '力士']

end-pass boundary input-prefix erased0.5 plain27:

['_Dec', ' Boxing', ' December', ' Ро', ' Dec', 'ecoin', ' Feliz', '雰', 'December', ' قائ', 'ypy', ' Advent', 'elő', 'Ро', '要么是', '阳春', '籌', '新的一年', ' gee', 'unie', 'Dec', '闰', '尽享', ' fö', ' payday', '\tJ', ' ژ', '(_)', '跨年', 'ヵ', '风景名胜', ' посл']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', ':\\"', ').\\', '?\\', ',\\', '\\"\\', ' **“', '\\")', '*\\', ')\\', ',__', ',”', ' \\"{', ':+', '\\",\\"', '+)\\', '."),', ' franz', '+z', '+",', '>\\', ')”', '"\\']

end-pass preclue input-prefix erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', 'os', '中和', 'AYS', 'corr', '発表した', 'udy', ' Entrega', 'ud', 'itu', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', '有关人员', 'eme']

end-pass preclue input-prefix erased0.5 plain27:

['ia', 'ute', '2', 'in', 'l', 'oe', 'ug', 'zt', '4', '1', 'ere', 'os', 'ill', 'se', 'im', 'id', '处', 'ort', 'ud', '3', 'je', 'zz', 'ur', '义', 'usr', '5', 'endants', 'ills', '8', ' +', 'ounds', 'ore']

end-pass input-prefix metric-erased0.5 J-lens:

[' **', ' Calendar', ' Next', ' Year', '事实', ' Tomorrow', ' Leap', '次年', '...**', ' Future', '…**', ' Holidays', ' Seasons', ' Week', ' calendar', 'calendar', '(next', ' Winter', ' February', ' Fakt', ' Vacation', ' Spring', 'Calendar', ' Past', ' **.**', ' Weeks', ' December', ' Season', ' Nothing', ' holidays', ':...', ' Summer']

end-pass input-prefix metric-erased0.5 plain24:

['事实', '_fact', ' صدا', 'orías', 'вис', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', 'ヵ', ' prekybos', ' beleg', ' факта', 'の販', ':...', '?...', ' факт', ' Situé', 'ément', '探し', '…**', '...(', 'eceğ', ' sacerdo', ' **:**', '事实上']

end-pass input-prefix metric-erased0.5 plain27:

['_Dec', '事实', '版权声明', '展望', '寒冷的', '闰', ' Ро', '腊', '冬', ' Empresarial', ' December', 'Leap', 'ajukan', '越し', ' Leap', ' ...', ' Fakta', '新年快乐', ' صدا', 'Dec', '…', '乞', ' факта', ' Dec', '事實', 'apt', 'December', '_dec', ' Yours', '-Nov', '的事实', '赔']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' **', ' Calendar', ' Next', '事实', ' Year', '次年', ' calendar', '**', ' Tomorrow', '...', ' ...', ' February', ' next', ' Future', 'calendar', ' Leap', ' Spring', ' December', ' Winter', ' Week', ' weeks', 'next', '(next', 'Next', 'Calendar', '…', ' Summer', ' summer', ' holidays', ' Season', ' Seasons', ' year']

end-pass boundary input-prefix metric-erased0.5 J-lens:

['月份', '次年', ' Calendar', '___', ' December', '-month', '当月', '**!', ' Tomorrow', '...**', ' Year', '_month', '[__', '____', ' ___', '__:', 'Calendar', '_*', 'calendar', '日历', ' February', '翌', ' следующего', ' ____', ' *[', '__', '/month', ' NEXT', '闰', '月份的', '_MONTH', '一个月']

end-pass boundary input-prefix metric-erased0.5 plain24:

['unie', '圆梦', '籌', '雰', ' eskort', ' sluts', 'の販', '筹', '[image', ' قائ', '같', '問わず', 'ovem', '服务部', '路网', 'ISATION', 'ément', 'wali', '订制', ' Folg', ' gee', ' cherchez', '日历', '拉开序幕', 'ujuan', 'ฉาย', 'ヵ', 'разу', 'lepší', 'رفة', '_variation', '力士']

end-pass boundary input-prefix metric-erased0.5 plain27:

['_Dec', ' Boxing', ' December', ' Ро', ' Dec', 'ecoin', ' Feliz', '雰', 'December', ' قائ', 'ypy', ' Advent', 'Ро', 'elő', '阳春', '要么是', '籌', 'unie', ' gee', '新的一年', '闰', '尽享', ' payday', 'Dec', 'ヵ', ' fö', ' ژ', '\tJ', '跨年', 'ộp', '(_)', '风景名胜']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

['月份', '次年', ' December', ' Calendar', '___', '____', '__', ' February', '-month', '**', 'calendar', '_month', '当月', ' Year', ' next', '月底', 'Calendar', 'next', '一个月', '日历', ' calendar', ' Tomorrow', ' November', '闰', ' October', ' ____', ' ___', ' April', ' **', '翌', ' следующего', ' birthdays']

end-pass preclue input-prefix metric-erased0.5 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', '?\\', ').\\', ' **„', ':\\"', ',\\', '\\"\\', '\\")', ' **“', '*\\', ')\\', ',”', ',__', ':+', '\\",\\"', ' \\"{', '+)\\', '."),', '+z', '.#', ' franz', '>\\', '+",', '"\\']

end-pass preclue input-prefix metric-erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', 'os', '中和', '钦', 'AYS', 'corr', '発表した', 'udy', 'ud', ' Entrega', 'uz', 'zz', 'itu', '发', 'rait', 'äs', 'uto', '有关人员', 'eme', '说法']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', 'ute', '2', 'in', 'l', 'oe', 'ug', 'zt', '4', '1', 'ere', 'os', 'ill', 'se', 'im', 'id', '处', 'ort', '3', 'ud', 'je', 'zz', 'ur', '5', 'usr', '义', 'endants', 'ills', ' +', '8', 'ore', 'ounds']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ':\\"', '?\\', ').\\', ',\\', '\\"\\', '\\")', ' **“', '*\\', ')\\', ',__', ' \\"{', ',”', ':+', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+",', '+z', ')”', '.#']

### Case 1: Thursday

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
Tuesday<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' Tomorrow', ' **', ' Saturday', ' Friday', ' Monday', ' Midnight', ' Yesterday', ' Night', ' Sunday', ' Wednesday', ' Thursday', ' tomorrow', ' Today', ' Tonight', ' Christmas', ' Weekend', ' Thanksgiving', '事实', ' Halloween', ' weekend', '明天的', ' Evening', ' Morning', ' nights', ' weekends', ' Nights', ' Holidays', ' NIGHT', ' Leap', ' night', ' Sundays', ' Easter']

end-pass input-prefix erased0.5 plain24:

['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' compro', '当地的', 'eve', ' Empresarial', ' факта', ' beleg', '本题考查', 'IVAL', '事实上', '赔', '…**', ' 사실', ' Fakten', ' fatos', ' Fakta', 'eceğ', ' صدا', ' факты', ' chôm', ' sacerdo', ' Pôle', '医疗队', ' fato', '版权声明']

end-pass input-prefix erased0.5 plain27:

['赔', '周一', 'Monday', '事实', ' Saturday', '圩', 'rides', ' среду', ' среда', ' Wednesday', ' Monday', '.tom', '安息', '普通的', ' weekends', ' Friday', '요일', '周六', '礼拜', '后天', 'Friday', 'fr', ' wed', ' Sunday', ' pazar', '中华人民共和国', ' sund', '금', '星期六', ' **', ' جم', '普通']

end-pass input-prefix J-lens:

[' Saturday', ' Monday', ' Friday', ' Wednesday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' weekend', ' Mondays', ' Thanksgiving', ' Christmas', ' Sundays', '明天的', ' **', ' weekends', 'Monday', ' Evening', ' Morning', ' Halloween', ' Saturdays', '事实', ' Fridays', ' nights', ' Holidays', ' Nights']

end-pass boundary input-prefix J-lens:

['次日', ' tomorrow', ' next', ' Saturday', 'next', '第二天', ' Thursday', '紧接着', 'Next', ' Next', ' weekend', ' Monday', ' NEXT', '.next', '明天的', '_next', ' Friday', '-next', '翌', '(next', '下一个', ' Tomorrow', '接下来', ' weekends', '接下来的', 'Saturday', 'Monday', ' Wednesday', '明天', ' Sunday', ' getNext', '-day']

end-pass boundary input-prefix erased0.5 J-lens:

['次日', ' next', ' tomorrow', ' Next', 'Next', '紧接着', 'next', '.next', ' NEXT', '_next', '第二天', '下一个', '接下来', '-next', '(next', '翌', ' weekend', '明天的', '接下来的', ' Saturday', ' Tomorrow', '接着', ' weekends', '明天', '-day', ' Thursday', ' getNext', ' 다음', '\tnext', '.Next', ' следующий', ' Monday']

end-pass boundary input-prefix erased0.5 plain24:

['紧接着', '下一个', 'ถัด', '.next', 'sequent', '-next', 'next', '(next', ' посл', '接下来', ' next', 'Next', '接踵', ' succeeding', '.Next', '翌', '之后的', ' kolej', '随后的', '下个', '_next', '日历', ' следующего', '紧随', '接下来的', '管所', '明天的', '\tnext', ' следующий', 'дне', ' наступ', ' getNext']

end-pass boundary input-prefix erased0.5 plain27:

['-day', 'วัน', '.day', '(day', ' día', '_day', ' дня', '的那天', '/day', '-Day', 'eday', 'יום', '这一天', '�', ' день', '翌', '当天的', ' วัน', ' followed', ' follows', '明天的', '紧跟', '.tom', '跟进', 'ในวัน', '后天', '营业', '日的', '日是', 'День', '요일', 'днев']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '+",']

end-pass preclue input-prefix erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', 'corr', '中和', 'os', 'AYS', 'udy', '発表した', 'itu', 'ud', ' Entrega', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', 'eme', '中心医院']

end-pass preclue input-prefix erased0.5 plain27:

['ia', 'ute', '2', 'in', 'oe', 'l', 'zt', 'ug', '4', 'ere', 'ill', '1', 'os', 'se', 'im', 'id', '处', 'ort', 'ud', 'zz', '义', 'endants', 'ur', 'je', 'usr', 'ills', '3', '5', 'ounds', 'rie', ' +', '8']

end-pass input-prefix metric-erased0.5 J-lens:

[' Tomorrow', ' Midnight', ' Yesterday', ' **', ' Saturday', ' Friday', ' Night', ' Tonight', ' Monday', ' Wednesday', ' Weekend', ' Thursday', ' Sunday', ' Today', '事实', ' Thanksgiving', ' tomorrow', ' Christmas', ' Holidays', '明天的', ' Halloween', ' Leap', ' NIGHT', ' Nights', ' Evening', ' Fakt', ' Morning', ' Calendar', ' Mondays', ' weekend', ' Truth', ' Easter']

end-pass input-prefix metric-erased0.5 plain24:

['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' Empresarial', '当地的', ' compro', 'eve', ' факта', ' beleg', '本题考查', '…**', 'IVAL', '事实上', '赔', ' 사실', ' Fakta', ' fatos', ' Fakten', ' chôm', 'eceğ', ' صدا', ' Pôle', ' sacerdo', ' факты', '医疗队', ' fato', 'yar']

end-pass input-prefix metric-erased0.5 plain27:

['赔', '周一', 'Monday', '事实', 'rides', '圩', ' Saturday', ' среду', ' среда', '.tom', ' Wednesday', ' Monday', ' weekends', '普通的', '安息', '요일', '礼拜', '周六', 'Friday', ' Friday', '后天', ' sund', ' pazar', ' wed', '中华人民共和国', 'fr', '금', ' Sunday', '星期六', ' fronti', ' جم', ' Satur']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' Tomorrow', ' **', ' Saturday', ' Monday', ' Friday', ' Midnight', ' Sunday', ' Wednesday', ' Yesterday', ' tomorrow', ' Thursday', ' Tonight', ' Night', ' Today', ' Christmas', ' Thanksgiving', ' Weekend', '明天的', '事实', ' Halloween', ' weekend', ' nights', ' Nights', ' Morning', ' Evening', ' weekends', ' Holidays', '**', ' Leap', ' Sundays', ' Calendar', ' night']

end-pass boundary input-prefix metric-erased0.5 J-lens:

['次日', ' next', '紧接着', ' tomorrow', ' Next', ' NEXT', 'next', 'Next', '.next', '_next', '下一个', '接下来', '-next', '(next', '翌', '接下来的', '第二天', '明天的', ' Tomorrow', ' getNext', ' следующий', ' weekend', 'ถัด', '接着', ' Saturday', ' следующего', ' 다음', '\tnext', '随后的', '.Next', '下一页', ' lendemain']

end-pass boundary input-prefix metric-erased0.5 plain24:

['紧接着', 'ถัด', '下一个', '.next', 'sequent', '-next', '(next', 'next', ' посл', '接踵', '接下来', ' succeeding', ' next', 'Next', '.Next', '翌', '随后的', ' kolej', '下个', '之后的', '日历', '_next', '管所', '紧随', ' следующего', '接下来的', '明天的', '\tnext', ' следующий', 'дне', ' التالي', ' наступ']

end-pass boundary input-prefix metric-erased0.5 plain27:

['-day', 'วัน', '.day', '(day', ' día', '_day', ' дня', '的那天', '-Day', '/day', 'eday', 'יום', '�', '这一天', ' день', '翌', '当天的', ' วัน', ' followed', '明天的', ' follows', '紧跟', '.tom', '跟进', 'ในวัน', '营业', '后天', '日是', 'День', '日的', '요일', 'днев']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

['次日', ' next', ' tomorrow', 'next', ' Next', '紧接着', 'Next', '.next', '第二天', '_next', ' NEXT', '下一个', '-next', '接下来', '明天的', '(next', '翌', ' weekend', ' Saturday', '接下来的', '接着', ' Tomorrow', '明天', ' следующего', ' Monday', '\tnext', ' weekends', ' Thursday', ' следующий', '-day', ' 다음', ' getNext']

end-pass preclue input-prefix metric-erased0.5 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',__', ',”', ':+', '\\",\\"', '+)\\', ' \\"{', '."),', ' franz', '+z', '>\\', '.#', ')”', '"\\']

end-pass preclue input-prefix metric-erased0.5 plain24:

['udu', 'oe', 'zn', 'zt', '义', 'aaaa', 'utt', 'ug', 'itz', 'uth', '投资有限公司', ' ficará', 'ute', '钦', '中和', 'os', 'AYS', 'corr', 'udy', '発表した', 'itu', 'ud', ' Entrega', 'uz', 'zz', '发', 'rait', 'äs', 'uto', '说法', 'eme', '有关人员']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', 'ute', '2', 'in', 'oe', 'l', 'zt', 'ug', '4', 'ere', '1', 'os', 'ill', 'se', 'im', 'id', 'ort', '处', 'ud', 'zz', 'usr', '义', '3', 'ur', 'je', 'ills', 'endants', '5', 'rie', 'ounds', '8', ' +']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', '.\\"', '!\\', ':\\', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', '+z', ' franz', ')”', '.#', '+",']

### Case 2: autumn

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
winter<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' **', '**', ' colder', ' drought', ' summer', ' frost', ' warmer', '...', ' Spring', '…', ' Tropical', '淡季', '事实', ' Frost', ' tropical', ' spring', ' rainy', ' Summer', '冬季', '冬天', '春天', ' autumn', '寒冬', ' warm', '夏季', ' Warm', ' ...', '-season', '春季', 'Spring', 'summer', '�']

end-pass input-prefix erased0.5 plain24:

[' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', '乞', ' recherch', ' Empresarial', 'orías', 'дем', ' факты', ' صدا', ' pitan', 'ẩm', '名副其实的', '越し', 'rollers', 'つも', 'óź', 'レード', '版权声明', '월까지', '件事', ' temper', ' 사실을', 'ontaine', 'lated']

end-pass input-prefix erased0.5 plain27:

['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '冬', '.spring', '春', ' наступ', ' colder', '春天', '暑', '夏天', ' verano', 'zim', ' primavera', 'ฤดู', ' warmer', ' Empresarial', ' ...', ' summers', ' autumn', '寒冷', ' bore', ' лето', '版权声明', '夏天的', 'fall']

end-pass input-prefix J-lens:

[' summer', '冬季', '冬天', ' colder', 'summer', ' **', ' frost', '寒冬', ' drought', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', '春天', ' spring', 'spring', ' Tropical', ' primavera', ' vinter', ' Autumn', 'Spring', ' Frost', '_season', ' зим', ' printemps', ' rainy']

end-pass boundary input-prefix J-lens:

['Spring', '春季', '___', 'spring', ' printemps', '雨季', 'summer', ' Spring', ' spring', ' summer', '冬季', '冬', '淡季', '夏季', '__:', ' primavera', '旺季', '春天', ' rainy', '__', '-season', ' summers', '季节', '寒冬', '春暖花开', '_season', '__)', '__.', ' autumn', '次年', '早春', 'Summer']

end-pass boundary input-prefix erased0.5 J-lens:

['___', '__', 'Spring', '____', '春季', ' Spring', '雨季', '**', ' **', ' rainy', ' printemps', ' spring', ' ___', 'spring', '__:', ' __', '__.', '春天', ' summer', '__)', '淡季', '干旱', '夏季', '旺季', '季节', '春暖花开', ' primavera', ' ____', '_____', '次年', '_________', ' drought']

end-pass boundary input-prefix erased0.5 plain24:

['問わず', '_-', ' springs', '要么是', 'spring', '管理类', 'imbul', 'onto', 'Regions', 'icu', ' preceded', ' mide', 'unno', '最专业的', 'разу', 'tings', 'Spring', '到来', 'дем', 'umont', 'urus', 'unity', '什么都没', 'REW', ' قائ', ' ką', 'schnitt', '้ง', 'azan', 'QUOTE', 'intérêt', 'IMG']

end-pass boundary input-prefix erased0.5 plain27:

[' Spring', ' spring', 'spring', 'Spring', 'pring', ' springs', '春', '.spring', 'fall', '春意', '夏', ' Springs', ' summer', ' fall', ' Fall', '\tSpring', ' autumn', '春的', '.Spring', ' primavera', ' FALL', '弹簧', '(Spring', ' Summer', '봄', '春天', '.springframework', 'Fall', '春天的', ' printemps', ' вес', 'summer']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 plain24:

['udu', 'oe', 'zn', '义', 'zt', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', 'ute', '钦', '中和', 'ud', ' ficará', '投资有限公司', 'corr', '发', 'zz', 'uz', 'udy', 'AYS', '2', '5', 'itu', '発表した', '说法', ' Entrega', 'äs', 'uto', 'rait']

end-pass preclue input-prefix erased0.5 plain27:

['ia', 'ute', '2', 'oe', 'l', 'zt', 'ug', 'ere', '4', 'ill', '1', 'os', 'se', 'im', 'id', 'ort', '处', 'ud', 'endants', 'zz', 'ur', 'usr', '义', 'je', 'ills', '3', '5', 'rie', 'ounds', ' +', '8', 'od']

end-pass input-prefix metric-erased0.5 J-lens:

[' **', ' colder', ' drought', ' Tropical', '…**', ' frost', '**', ' warmer', '事实', '淡季', ' tropical', '...**', ' summer', ' Frost', ' fakta', ' **.**', ' Spring', ' Warm', '__:', ' rainy', '-season', '干旱', ' kalt', ':...', ' primavera', ' **-', ' **.', ' Summer', ' Desert', '寒冬', '_season', ' Answer']

end-pass input-prefix metric-erased0.5 plain24:

[' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', ' Empresarial', ' recherch', 'дем', 'orías', '乞', ' صدا', ' факты', 'ẩm', '名副其实的', ' pitan', '越し', 'óź', 'rollers', 'つも', '월까지', '版权声明', 'レード', 'ontaine', ' 사실을', ' zove', ' cocks', '件事']

end-pass input-prefix metric-erased0.5 plain27:

['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '.spring', '冬', ' наступ', '春', ' colder', '春天', '暑', 'zim', ' verano', '夏天', ' primavera', ' Empresarial', 'ฤดู', ' warmer', ' summers', ' лето', ' autumn', '.Sum', '寒冷', '版权声明', ' fakta', ' bore', '\tSpring']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' **', '**', ' colder', ' summer', ' drought', ' frost', ' warmer', ' Spring', ' Tropical', ' tropical', '...', ' spring', '…', '事实', ' Frost', '淡季', '冬季', 'Spring', ' autumn', ' warm', ' Warm', '春季', ' Summer', ' rainy', '春天', '冬天', '寒冬', '夏季', 'summer', ' snow', '�', '寒冷']

end-pass boundary input-prefix metric-erased0.5 J-lens:

['___', '__:', '__', '雨季', 'Spring', '__)', ' printemps', ' *__', '__.', '’**', '[__', ' ___', '春季', ' rainy', '____', ' Spring', ':__', '干旱', 'spring', ' **.', ' **.**', '春暖花开', '_),', '淡季', "'**", ')__', '**!', '旺季', '_________', ' primavera', '_*', ' ____']

end-pass boundary input-prefix metric-erased0.5 plain24:

['問わず', '_-', '要么是', ' springs', '管理类', 'imbul', 'spring', 'onto', 'Regions', 'icu', ' preceded', ' mide', '最专业的', 'unno', 'разу', 'tings', '到来', 'дем', 'Spring', 'umont', 'REW', 'urus', '什么都没', 'unity', ' قائ', 'schnitt', ' ką', 'intérêt', '้ง', 'azan', '航空航天大学', 'QUOTE']

end-pass boundary input-prefix metric-erased0.5 plain27:

[' Spring', ' spring', 'spring', 'Spring', 'pring', ' springs', '春', '.spring', 'fall', '春意', ' Springs', '夏', ' summer', ' Fall', ' fall', '\tSpring', '春的', ' autumn', '.Spring', ' primavera', ' FALL', '(Spring', '弹簧', ' Summer', '봄', '春天', '春天的', 'Fall', '.springframework', ' printemps', ' Вес', ' вес']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

['___', '__', 'Spring', '春季', ' Spring', '**', '____', ' spring', ' **', ' printemps', '雨季', 'spring', ' rainy', ' ___', '__:', '干旱', '__.', ' __', ' summer', '__)', '春暖花开', '春天', '夏季', ' primavera', '淡季', '季节', '旺季', '次年', '_____', '旱', '’**', '**.']

end-pass preclue input-prefix metric-erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix metric-erased0.5 plain24:

['udu', 'oe', 'zn', '义', 'zt', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', 'ute', '中和', '钦', ' ficará', '投资有限公司', 'ud', 'corr', 'AYS', '发', 'uz', 'zz', 'udy', 'itu', '5', '2', '発表した', ' Entrega', 'rait', '说法', 'äs', 'uto']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', 'ute', '2', 'l', 'oe', 'zt', 'ug', 'ere', '4', '1', 'ill', 'os', 'se', 'im', 'id', '处', 'ort', 'ud', 'ur', 'endants', 'zz', '义', 'usr', 'je', 'ills', '3', '5', ' +', '8', 'rie', 'ounds', 'od']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', '+z', ' franz', '+",', '"\\', '.#']

### Case 3: apple

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
red<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' purple', ' green', ' pink', ' black', ' blue', '黑色的', ' Purple', ' violet', ' yellow', '红色', 'pink', 'purple', ' brown', 'black', 'green', '黑色', ' orange', ':red', ' dark', 'blue', '蓝色', '绿色', ':black', ' crimson', '的颜色', ':green', '绿色的', 'brown', ' Pink', '…**', '红色的', ' gray']

end-pass input-prefix erased0.5 plain24:

[':red', '…**', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '同期的', '红了', ' утвер', 'lep', ' uby', '加拿大的', ' setBackgroundColor', ' berüh', ' 스위트', 'rosa', ' Eventi', 'iciels', '及配件', ' сбы', 'の販', 'ائع', '죄']

end-pass input-prefix erased0.5 plain27:

[':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', '通红', '\xa0\xa0\xa0', ' warta', 'acin', '五颜六色的', 'struments', 'สีแดง', ' kı', '_red', 'eiß', ' الأحمر', '如荼', ' Eintritt', '../../../../', ':green', '죄', '{}".', ' сбы', '各种各样', ' утвер']

end-pass input-prefix J-lens:

[' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', 'green', 'black', 'blue', ' yellow', 'pink', 'purple', '红色的', ' Purple', ' brown', '黑色的', ' orange', ' violet', ' crimson', '黑色', '_red', '蓝色', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black']

end-pass boundary input-prefix J-lens:

[' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', 'apple', ' mushrooms', '苹果', '樱桃', ' candies', ' sweets', ' candy', '苹果的', '毒药', ' cakes', ' carrots', '剧毒', ' poisoning', ' grapes', ' Apfel', ' fairy', ' cherry', '-*-', '/apple', 'Apple', 'cakes', '草莓', ' chocolates', '毒']

end-pass boundary input-prefix erased0.5 J-lens:

[' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', 'apple', ' candies', '苹果', ' sweets', '樱桃', ' candy', '毒药', '苹果的', ' cakes', ' poisoning', '剧毒', ' carrots', ' grapes', ' Apfel', ' fairy', '-*-', ' cherry', 'cakes', '/apple', 'Apple', ' **【', ' chocolates', ' bananas']

end-pass boundary input-prefix erased0.5 plain24:

['меется', '一整', '中毒', '￣', '整座', 'uentes', '连心', '�', '颗星', '时许', '迈着', '现实中', '头等', '剧毒', ' вред', 'lips', 'eware', '_topology', 'integration', '块的', 'IDI', '这颗', ' اشت', ' poisoning', '倾心', '机械设计', '现实的', '一口', '常温', 'okin', 'Fatal', ' berries']

end-pass boundary input-prefix erased0.5 plain27:

[' apple', '苹果', ' apples', 'apple', '中毒', ' poisoning', 'Apple', '苹果的', '毒', ' Apple', ' poisonous', '.apple', ' APPLE', ' ябло', '_app', 'แอป', '-po', 'พิษ', 'APPLE', '-app', ' po', '剧毒', '苹果公司', '蘋果', ' 사과', ' созре', '_APP', 'app', 'Org', ' app', '有毒', '(app']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', '+)\\', '\\",\\"', ' \\"{', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'uth', 'ute', 'os', '中和', '钦', '投资有限公司', ' ficará', 'ud', 'corr', 'AYS', 'udy', 'uz', '発表した', 'itu', 'zz', '发', ' Entrega', 'rait', 'uto', 'äs', '说法', 'eme', '2']

end-pass preclue input-prefix erased0.5 plain27:

['ia', 'ute', '2', 'l', '4', '1', 'oe', 'ug', 'zt', 'ere', 'os', 'ill', 'se', 'im', 'id', '3', '5', '处', 'ort', 'ud', '8', 'ur', ' +', 'zz', 'je', '义', 'usr', 'ills', ' at', 'endants', ' (', '0']

end-pass input-prefix metric-erased0.5 J-lens:

[' purple', ' green', ' black', ' pink', ' blue', '黑色的', ' Purple', ' violet', ' yellow', 'black', '黑色', ' brown', 'purple', '红色', ' dark', 'pink', 'green', ' orange', '蓝色', ':red', ':black', '…**', 'blue', '绿色', ':green', '绿色的', ' Pink', ' **', '的颜色', ' crimson', ' GREEN', ' Green']

end-pass input-prefix metric-erased0.5 plain24:

[':red', '…**', 'меется', ' pales', ' warta', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '红了', 'lep', '同期的', ' uby', ' утвер', '加拿大的', ' berüh', ' setBackgroundColor', 'rosa', ' Eventi', ' 스위트', '及配件', ' сбы', ' Liebl', 'ائع', '죄', 'iciels']

end-pass input-prefix metric-erased0.5 plain27:

[':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', ' warta', '\xa0\xa0\xa0', '通红', 'acin', 'struments', '五颜六色的', ' kı', 'สีแดง', '如荼', 'eiß', '_red', '../../../../', ' الأحمر', ':green', ' Eintritt', '죄', '{}".', ' утвер', ' сбы', 'dling']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' purple', ' green', ' pink', ' blue', ' black', 'pink', ' yellow', ' violet', '红色', ' Purple', ':red', ' orange', 'green', 'purple', '黑色的', ' brown', 'blue', ' dark', 'black', '蓝色', '黑色', ' crimson', '绿色', '的颜色', ' rouge', ' Pink', 'brown', ' gray', ':black', '…**', '绿色的', 'orange']

end-pass boundary input-prefix metric-erased0.5 J-lens:

[' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', '苹果', ' candies', ' sweets', 'apple', '樱桃', '苹果的', '毒药', '剧毒', ' candy', ' cakes', ' poisoning', ' carrots', ' Apfel', ' grapes', ' fairy', '-*-', '/apple', 'cakes', ' cherry', ' chocolates', '毒', ' **【', '-**']

end-pass boundary input-prefix metric-erased0.5 plain24:

['меется', '一整', '中毒', '￣', '整座', 'uentes', '连心', '�', '颗星', '时许', '迈着', '现实中', '头等', '剧毒', ' вред', 'lips', 'eware', '_topology', 'integration', '块的', 'IDI', '这颗', ' اشت', ' poisoning', '机械设计', '倾心', '现实的', '一口', '常温', 'okin', 'Fatal', ' berries']

end-pass boundary input-prefix metric-erased0.5 plain27:

[' apple', '苹果', ' apples', 'apple', '中毒', ' poisoning', 'Apple', '苹果的', '毒', ' Apple', ' poisonous', '.apple', ' APPLE', ' ябло', '_app', 'แอป', '-po', 'พิษ', 'APPLE', '-app', ' po', '剧毒', '苹果公司', '蘋果', ' 사과', ' созре', '_APP', 'app', 'Org', ' app', '有毒', '(app']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

[' berries', ' strawberries', 'berries', ' poisonous', ' apples', ' berry', ' apple', ' strawberry', ' mushrooms', '苹果', ' candies', 'apple', ' sweets', '樱桃', ' candy', '苹果的', ' carrots', '剧毒', ' poisoning', '毒药', ' cakes', ' grapes', ' Apfel', ' fairy', 'cakes', '-*-', '毒', 'Apple', ' cherry', '/apple', '草莓', ' bananas']

end-pass preclue input-prefix metric-erased0.5 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', ' \\"{', '\\",\\"', '+)\\', '."),', '>\\', ' franz', '+z', ')”', '.#', '"\\']

end-pass preclue input-prefix metric-erased0.5 plain24:

['udu', 'oe', 'zn', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'uth', 'ute', 'os', '中和', '钦', '投资有限公司', ' ficará', 'ud', 'corr', 'AYS', 'udy', 'uz', '発表した', 'itu', 'zz', '发', ' Entrega', 'rait', 'uto', 'äs', '说法', 'eme', '2']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', 'ute', '2', 'l', '4', '1', 'oe', 'ug', 'zt', 'ere', 'os', 'ill', 'se', 'im', 'id', '3', '5', '处', 'ort', 'ud', '8', 'ur', ' +', 'zz', 'je', '义', 'usr', 'ills', ' at', 'endants', ' (', '0']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

[',\\"', '+\\', '):\\', '.\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', '*\\', ')\\', ',”', ',__', ':+', '+)\\', '\\",\\"', ' \\"{', '."),', ' franz', '>\\', '+z', ')”', '.#', '"\\']

### Case 4: cloud

Input repr:
```text
'<|im_start|>user\nComplete the last translation with only the missing word:\nDeutsch: "Kopf" - Français: "tête"\nDeutsch: "Rede" - Français: "discours"\nDeutsch: "Auge" - Français: "œil"\nDeutsch: "Hand" - Français: "main"\nDeutsch: "Wolke" - Français: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
nuage<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云', '云朵', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', ' skies', '浮云', 'クラウド', ' 클라우드', '云中', '云计算']

end-pass input-prefix erased0.5 plain24:

['cloud', '_cloud', 'Cloud', ' clouds', '-cloud', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '/cloud', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', '云雾', ' mây', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '人民医院']

end-pass input-prefix erased0.5 plain27:

['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' 클라우드', ' mây', '云中', '云平台', '云服务器']

end-pass input-prefix J-lens:

[' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', 'クラウド', '浮云', ' 클라우드', ' skies', '云中', '云计算']

end-pass boundary input-prefix J-lens:

['德语', ' meaning', ' **„', '单词', 'German', '这个词', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', ' meanings', ' Translate', 'Translate', 'meaning', '翻译成', '意思', ' слово', 'cloud', ' Cloud', '云', ' palavra', ':\\"', ' palabra', '含义', '的意思是']

end-pass boundary input-prefix erased0.5 J-lens:

['德语', ' meaning', ' **„', '单词', 'German', '这个词', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', ' meanings', ' Translate', 'Translate', '翻译成', 'meaning', '意思', ' слово', '云', ' Cloud', ' palavra', 'cloud', ':\\"', ' palabra', '的意思是', '含义']

end-pass boundary input-prefix erased0.5 plain24:

['_cloud', ' translates', '意为', '云', ' meaning', '云服务', '云的', ' перево', ' translated', '#w', '对应的', ' แปล', 'แปล', ' vols', '意思是', 'translated', 'Translate', ' traduc', '的意思是', '-word', 'cloud', 'translate', ' translate', '意思', ' traduz', '翻译', 'meaning', '"w', ' meanings', ' ترجمة', '匹', 'apus']

end-pass boundary input-prefix erased0.5 plain27:

['云', '_cloud', 'cloud', '-word', '云的', ' cloud', '词', '_word', 'Cloud', '雲', ' clouds', ' Cloud', ' meaning', '单词', '云彩', '.word', ' palavra', '-cloud', '云服务', ' cloudy', '云上', '这个词', ' palabra', ' слово', 'meaning', '(word', '字', '的词', '云平台', '字的', '云计算', '/cloud']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', '?\\', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', ' \\"{', '\\",\\"', '+)\\', ' franz', '."),', '>\\', '+z', '"\\', '.#', '+",']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ':\\"', ').\\', ' **„', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '"\\', '>\\', '.#', '."),', '+z', ')”']

end-pass preclue input-prefix erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', ' ficará', '投资有限公司', 'corr', '中和', '钦', 'ute', 'AYS', 'itu', 'ud', 'uz', 'zz', '発表した', 'udy', 'rait', ' Entrega', '发', 'uto', 'äs', 'eme', '说法', '有关人员']

end-pass preclue input-prefix erased0.5 plain27:

['ia', 'ute', '2', 'in', 'l', '4', 'oe', 'ug', '1', 'zt', 'ere', 'os', 'se', 'ill', 'im', 'id', '3', 'ort', '5', 'ud', '处', 'ur', 'je', 'zz', '8', '义', ' +', 'usr', 'ills', 'endants', ' at', '0']

end-pass input-prefix metric-erased0.5 J-lens:

[' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '云彩', '的云', '云服务', '云端', '乌云', '云海', ' fog', 'クラウド', '浮云', ' skies', ' 클라우드', '云中', '云计算']

end-pass input-prefix metric-erased0.5 plain24:

['cloud', '_cloud', 'Cloud', '-cloud', ' clouds', ' Cloud', ' cloud', '云的', '.cloud', '云', '云层', '/cloud', '.Cloud', ' обла', '雲', '云彩', '云朵', '云服务', '云雾', ' mây', 'クラウド', '云计算', ' cloudy', ' trots', '多云', '凝结', 'ceptive', '云端', '的云', '天空', '白云', '人民医院']

end-pass input-prefix metric-erased0.5 plain27:

['cloud', ' cloud', ' Cloud', '云', ' clouds', '-cloud', '云的', 'Cloud', '_cloud', '雲', '云层', '云彩', ' cloudy', '的云', '.cloud', '.Cloud', ' обла', '/cloud', '云朵', '云端', '云雾', 'クラウド', '云天', '云服务', '云计算', '云上', '白云', ' mây', ' 클라우드', '云中', '云平台', '云服务器']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' clouds', 'cloud', 'Cloud', ' cloud', ' Cloud', '-cloud', '.cloud', '/cloud', '_cloud', '云层', '雲', '云的', '云朵', '云', '云雾', ' mây', ' cloudy', ' обла', '.Cloud', '的云', '云彩', '云服务', '云端', '乌云', '云海', ' fog', ' 클라우드', 'クラウド', ' skies', '浮云', '云中', '云计算']

end-pass boundary input-prefix metric-erased0.5 J-lens:

['德语', ' meaning', ' **„', '单词', '这个词', 'German', '翻译', ' Meaning', ' translates', '_cloud', ' German', ' translated', ' translate', '意为', '-word', 'Cloud', '_word', ' Translate', '翻译成', ' meanings', '意思', ' слово', 'Translate', 'meaning', '云', ' Cloud', ':\\"', ' palavra', 'cloud', ' palabra', '的意思是', '含义']

end-pass boundary input-prefix metric-erased0.5 plain24:

['_cloud', ' translates', '意为', '云', ' meaning', '云服务', '云的', ' перево', ' translated', '#w', '对应的', ' แปล', 'แปล', ' vols', '意思是', 'translated', 'Translate', ' traduc', '的意思是', '-word', 'cloud', 'translate', ' translate', '意思', ' traduz', '翻译', 'meaning', '"w', ' meanings', ' ترجمة', '匹', 'apus']

end-pass boundary input-prefix metric-erased0.5 plain27:

['云', '_cloud', 'cloud', '-word', '云的', ' cloud', '词', '_word', 'Cloud', '雲', ' clouds', ' Cloud', ' meaning', '单词', '云彩', '.word', ' palavra', '-cloud', '云服务', ' cloudy', '云上', ' слово', '这个词', ' palabra', 'meaning', '(word', '字', '的词', '云平台', '字的', '云计算', '/cloud']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

['德语', ' meaning', ' **„', '单词', '这个词', 'German', '翻译', ' Meaning', ' translates', ' translated', ' German', ' translate', '_cloud', '意为', '-word', 'Cloud', '_word', 'Translate', '翻译成', ' Translate', 'meaning', ' слово', ' meanings', '意思', ' palavra', ' Cloud', 'cloud', ':\\"', '云', ' palabra', '的意思是', '含义']

end-pass preclue input-prefix metric-erased0.5 J-lens:

['+\\', ',\\"', '):\\', '.\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ' **„', ').\\', ':\\"', ' **“', ',\\', '\\"\\', '\\")', ')\\', '*\\', ',”', ',__', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '."),', '+z', ')”', '+",', '>\\', '"\\']

end-pass preclue input-prefix metric-erased0.5 plain24:

['udu', 'zn', 'oe', 'zt', '义', 'aaaa', 'ug', 'utt', 'itz', 'os', 'uth', ' ficará', '投资有限公司', 'ute', '中和', 'corr', 'AYS', 'itu', '钦', 'ud', 'uz', 'zz', '発表した', 'udy', 'rait', ' Entrega', '发', 'uto', 'äs', 'eme', '说法', '有关人员']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', 'ute', '2', 'in', 'l', '4', 'oe', 'ug', '1', 'zt', 'ere', 'os', 'se', 'ill', 'im', 'id', '3', 'ort', '5', 'ud', '处', 'ur', 'je', 'zz', '8', '义', ' +', 'usr', 'ills', 'endants', ' at', '0']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

['+\\', ',\\"', '.\\', '):\\', '.“', '。\\', ':\\', '!\\', '.\\"', ' **„', ').\\', '?\\', ':\\"', ',\\', ' **“', '\\"\\', '\\")', ')\\', '*\\', ',”', ',__', ':+', '\\",\\"', '+)\\', ' franz', ' \\"{', '+z', '"\\', '.#', '."),', '>\\', 'uz']

### Case 5: cloud

Input repr:
```text
'<|im_start|>user\nComplete the last translation with only the missing word:\nFrançais: "tête" - Deutsch: "Kopf"\nFrançais: "discours" - Deutsch: "Rede"\nFrançais: "œil" - Deutsch: "Auge"\nFrançais: "main" - Deutsch: "Hand"\nFrançais: "nuage" - Deutsch: "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Complete generation:
```text
Wolke<|im_end|>
```

end-pass input-prefix erased0.5 J-lens:

[' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', '云服务', ' Meteor', ' Weather', 'クラウド', ' Nimbus', ' Fog']

end-pass input-prefix erased0.5 plain24:

['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '云', '/cloud', '云的', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '�', '云服务', 'opies', '云彩', '云雾', '多云', '云山', 'ungkapkan', '習', '云朵', '云天', '凝', 'abut', '加拿大的', ' mây']

end-pass input-prefix erased0.5 plain27:

[' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', ' обла', '云服务', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '白云', '云服务器', ' nube', 'クラウド', ' 클라우드', '云中']

end-pass input-prefix J-lens:

[' Cloud', 'Cloud', 'cloud', ' clouds', '-cloud', ' cloud', '云层', '_cloud', '.cloud', '雲', '/cloud', '云雾', '云', '云的', '云朵', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', ' Weather', ' Fog', 'クラウド', '“']

end-pass boundary input-prefix J-lens:

['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '日语', '英语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', '法國', ' Italian', '翻译', '翻译成', 'Spanish', '韩语', ' spanish', ' 프랑스', ' Portuguese', ' немец', '瑞士']

end-pass boundary input-prefix erased0.5 J-lens:

['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '英语', '日语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', '翻译', '法國', ' Italian', 'Spanish', '翻译成', '韩语', ' Portuguese', ' 프랑스', ' spanish', '日本語', ' немец']

end-pass boundary input-prefix erased0.5 plain24:

['法语', '英语', 'French', ' translates', '德语', ' French', '对应的', ' translated', '翻译成', '-word', '翻译', '罗曼', 'iền', ' meanings', '意为', '汉语', 'Translate', ' untranslated', 'แปล', ' translators', ' Romance', '慕尼', ' перево', 'Rech', '日语', 'nameof', 'English', ' translate', '当て', '_nb', ' meaning', 'rench']

end-pass boundary input-prefix erased0.5 plain27:

['-word', '法语', '英语', 'French', ' French', '单词', '.word', '_word', ' palavra', '词', ' meaning', ' слово', '字的', '中文', ' noun', '德语', '[word', ' француз', ' كلمة', '这个词', ' fransk', 'meaning', ' English', ' palabra', '翻译成', '一词', 'means', '字', '(word', ' فرن', 'English', '韩语']

end-pass preclue input-prefix J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', ' **„', '?\\', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', ' \\"{', '\\",\\"', '+)\\', ' franz', '."),', '>\\', '+z', '"\\', '.#', '+",']

end-pass preclue input-prefix erased0.5 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', '?\\', ' **„', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',__', ',”', ':+', '\\",\\"', ' \\"{', '+)\\', ' franz', '>\\', '"\\', '+z', '."),', '.#', ')”']

end-pass preclue input-prefix erased0.5 plain24:

['oe', 'zn', 'udu', '义', 'zt', 'ug', 'aaaa', 'utt', 'os', 'itz', '2', 'uth', 'ute', 'ud', '5', '中和', '钦', 'uz', 'zz', '发', ' ficará', '投资有限公司', 'corr', 'udy', 'itu', 'AYS', '8', '4', 'uto', 'eme', '说法', 'rait']

end-pass preclue input-prefix erased0.5 plain27:

['ia', '2', 'ute', 'in', 'l', '1', '4', 'ug', 'oe', 'zt', 'ere', '3', 'os', 'se', 'im', 'id', '5', 'ill', '8', 'ort', 'ur', ' +', 'ud', '处', 'je', 'zz', '0', ' (', '义', '9', '^', ' at']

end-pass input-prefix metric-erased0.5 J-lens:

[' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云', '云朵', ' mây', ' nube', '.Cloud', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云海', '云端', ' Meteor', '云服务', 'クラウド', ' Himmel', ' Weather', ' Fog']

end-pass input-prefix metric-erased0.5 plain24:

['cloud', 'Cloud', ' Cloud', '_cloud', '-cloud', ' cloud', '.Cloud', ' clouds', '云', '/cloud', '云的', '雲', ' обла', '凝结', '云层', ' trots', '.cloud', '云服务', '�', 'opies', '云彩', '云雾', '多云', '云山', '云朵', '習', 'ungkapkan', '云天', '凝', '加拿大的', 'abut', ' mây']

end-pass input-prefix metric-erased0.5 plain27:

[' Cloud', ' cloud', '云', 'cloud', ' clouds', 'Cloud', '-cloud', '云的', '_cloud', '雲', '.Cloud', '云服务', ' обла', '/cloud', '云天', ' cloudy', '云层', '.cloud', '的云', '云端', '云彩', '云雾', '云朵', '云平台', '云计算', ' mây', '云服务器', '白云', ' nube', 'クラウド', ' 클라우드', '云中']

end-pass input-prefix metric-erased0.5 random0 J-lens:

[' Cloud', 'Cloud', ' clouds', 'cloud', '-cloud', ' cloud', '_cloud', '云层', '.cloud', '雲', '/cloud', '云雾', '云的', '云朵', '云', ' mây', '.Cloud', ' nube', ' обла', '乌云', '云彩', ' cloudy', '的云', ' Neb', '云端', '云海', ' Meteor', '云服务', 'クラウド', ' Nimbus', ' Weather', ' Fog']

end-pass boundary input-prefix metric-erased0.5 J-lens:

['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', ' English', '汉语', '英语', '日语', ' француз', 'English', ' Spanish', '西班牙语', '俄语', ' english', ' francés', ' francese', 'Spanish', ' francês', '翻译成', '翻译', '法國', ' Italian', '韩语', ' spanish', ' 프랑스', ' Portuguese', '日本語', ' немец']

end-pass boundary input-prefix metric-erased0.5 plain24:

['法语', '英语', 'French', ' translates', '德语', ' French', '对应的', ' translated', '翻译成', '-word', '翻译', '罗曼', 'iền', '意为', '汉语', ' meanings', ' untranslated', 'Translate', '慕尼', 'แปล', ' translators', 'Rech', ' перево', ' Romance', 'nameof', ' translate', 'English', '日语', '当て', '_nb', 'rench', ' meaning']

end-pass boundary input-prefix metric-erased0.5 plain27:

['-word', '法语', '英语', 'French', ' French', '单词', '.word', '_word', ' palavra', '词', ' meaning', ' слово', '字的', '中文', ' noun', '德语', '[word', ' француз', ' كلمة', '这个词', ' fransk', 'meaning', ' palabra', '翻译成', '一词', ' English', 'means', '字', '(word', '韩语', ' فرن', 'English']

end-pass boundary input-prefix metric-erased0.5 random0 J-lens:

['法语', ' French', 'French', '德语', ' french', ' German', 'German', '法国', '汉语', ' English', '日语', '英语', ' француз', ' Spanish', 'English', '西班牙语', '俄语', ' francés', ' english', ' francese', ' francês', ' Italian', '翻译', '法國', '翻译成', 'Spanish', ' Portuguese', ' 프랑스', '韩语', '日本語', ' spanish', ' немец']

end-pass preclue input-prefix metric-erased0.5 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', ':\\', '.\\"', '?\\', ':\\"', ').\\', ' **„', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',”', ':+', ',__', '\\",\\"', ' \\"{', '+)\\', ' franz', '"\\', '."),', '.#', '>\\', '+z', '+",']

end-pass preclue input-prefix metric-erased0.5 plain24:

['oe', 'udu', 'zn', '义', 'zt', 'ug', 'aaaa', 'utt', 'itz', 'os', 'uth', '2', 'ud', 'ute', '中和', '5', '钦', ' ficará', 'zz', 'uz', '发', 'corr', '投资有限公司', 'udy', 'AYS', 'itu', '8', 'uto', '说法', '発表した', 'eme', 'rait']

end-pass preclue input-prefix metric-erased0.5 plain27:

['ia', '2', 'ute', 'in', 'l', '1', '4', 'ug', 'oe', 'zt', 'ere', 'os', '3', 'se', 'im', 'id', 'ill', '5', '8', 'ur', 'ud', '处', 'ort', ' +', 'je', 'zz', '0', '义', ' (', ' at', '9', '^']

end-pass preclue input-prefix metric-erased0.5 random0 J-lens:

[',\\"', '+\\', '.\\', '):\\', '.“', '。\\', '!\\', '.\\"', ':\\', '?\\', ' **„', ').\\', ':\\"', ',\\', '\\"\\', ' **“', '\\")', ')\\', '*\\', ',”', ':+', ',__', ' \\"{', '\\",\\"', '+)\\', '+z', '>\\', '"\\', ' franz', '."),', '.#', '+",']
run.md: /workspace/2026/suppressed-activations/out/2026-10-01_170329_jlens-one-pass/run.md
