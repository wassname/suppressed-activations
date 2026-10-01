---
expand_input_prefix: true
chat_readout: true
readout_max_new_tokens: 32
gradient_pursuit: false
matching_pursuit: false
polar_readout: false
pool_question: false
verify_readout_run: None
token_kl: false
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: .local/queued/native_v4.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 10.78
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Logit contrast subtracts separately final-normalised vocabulary logits, retaining signed scores; probability contrast retains positive probability differences. Negative-final and cyclic mismatched-final scores are diagnostic controls. No generated text or labels enter these rankings. Posthoc rescoring of /workspace/2026/suppressed-activations/out/2026-10-01_102219_jlens-one-pass; no transformer forwards or new generations. See replay_source.json for hashes and mismatch ordering. Input-prefix variants additionally exclude strings starting with an entire lowercased prompt word of length>=3. This is a new development mask, not semantic morphology: art also excludes article; the old nam/name exclusion remains. Labels and generated text do not construct the mask. Every addition and originating word is saved in input_prefix_exclusions.json; full original scores are in input_prefix_scores. Original methods are retained unchanged; cyclic mismatch controls are omitted in this specific test. SHOULD: surviving scores and all original rows remain unchanged; inspect replacement entries for semantic leaks. Postmask AUROC can be high merely because negative labels are masked; do not use it as evidence of country recovery. Original methods keep the same layer, k32 and prompt mask; additional variants are described above. Position rule is specified above (otherwise final only). Dataset's original selection history: PI/OpenAI: all eight known v4 development concepts, original order and label/alias fields unchanged. One uniform native-chat completion instruction, old Japan/Tokyo demonstration omitted. New prompt frames, not unseen concepts or a pure chat-effect test. Frozen2686 head and controls; no output-based replacement; retain all failures. Reserved v5 not consumed. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved continuation (cap32), ignoring punctuation; generation is scoring only. Native-chat mode uses thinking=False and add_generation_prompt=True, stops on tokenizer or model EOS, and excludes special tokens from scoring text only; the verbatim decoded continuation is preserved. Completion-mode defaults remain unchanged. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Replay runs reuse the cached continuations without generation. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC and remain in the full denominator. These are lexical passes, not a verified lower bound on semantic success. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                                  | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:----------------------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| December  | J-lens                                  | False         |          0.385     |             4 |                      6 | False          | False        |
| December  | plain lens                              | False         |          0.56      |         23975 |                  18708 | False          | False        |
| December  | end-pass J-lens                         | True          |          1         |             4 |             1000000000 | True           | True         |
| December  | end-pass logit contrast J-lens          | False         |          1         |        185964 |             1000000000 | False          | False        |
| December  | end-pass probability contrast J-lens    | True          |          0.75      |             4 |             1000000000 | True           | True         |
| December  | end-pass plain24                        | False         |          1         |         23974 |             1000000000 | False          | False        |
| December  | end-pass logit contrast plain24         | False         |          1         |        216561 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain24   | False         |          0.65      |         25474 |             1000000000 | False          | False        |
| December  | end-pass plain27                        | True          |          1         |             1 |             1000000000 | True           | True         |
| December  | end-pass logit contrast plain27         | False         |          1         |        155635 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain27   | True          |          0.9       |             1 |             1000000000 | True           | True         |
| December  | end-pass negative final control         | False         |          1         |        239760 |             1000000000 | False          | False        |
| December  | end-pass erased1 J-lens                 | False         |          1         |           101 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 J-lens               | True          |          1         |            18 |             1000000000 | True           | True         |
| December  | end-pass erased1 plain24                | False         |          1         |         20902 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain24              | False         |          1         |         22914 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain27                | True          |          1         |            11 |             1000000000 | True           | True         |
| December  | end-pass erased0.5 plain27              | True          |          1         |             8 |             1000000000 | True           | True         |
| December  | end-pass input-prefix erased0.5 J-lens  | True          |          1         |            13 |             1000000000 | True           | True         |
| December  | end-pass input-prefix erased0.5 plain24 | False         |          1         |         22841 |             1000000000 | False          | False        |
| December  | end-pass input-prefix erased0.5 plain27 | True          |          1         |             8 |             1000000000 | True           | True         |
| December  | end-pass input-prefix J-lens            | True          |          1         |             1 |             1000000000 | True           | True         |
| Thursday  | J-lens                                  | False         |          0.266667  |             5 |                      3 | False          | False        |
| Thursday  | plain lens                              | False         |          0.416667  |          2199 |                   4483 | False          | False        |
| Thursday  | end-pass J-lens                         | True          |          1         |             4 |                      2 | False          | False        |
| Thursday  | end-pass logit contrast J-lens          | False         |          1         |         17558 |                  22244 | False          | False        |
| Thursday  | end-pass probability contrast J-lens    | True          |          0.7       |             4 |                      3 | False          | False        |
| Thursday  | end-pass plain24                        | False         |          1         |          2197 |                   4481 | False          | False        |
| Thursday  | end-pass logit contrast plain24         | False         |          1         |        183592 |                 242485 | False          | False        |
| Thursday  | end-pass probability contrast plain24   | False         |          0.8       |          2302 |                  22434 | False          | False        |
| Thursday  | end-pass plain27                        | True          |          1         |             8 |                      2 | False          | False        |
| Thursday  | end-pass logit contrast plain27         | False         |          1         |         94984 |                 160555 | False          | False        |
| Thursday  | end-pass probability contrast plain27   | True          |          0.9       |             5 |                      4 | False          | False        |
| Thursday  | end-pass negative final control         | False         |          1         |        240300 |                 246192 | False          | False        |
| Thursday  | end-pass erased1 J-lens                 | False         |          1         |            39 |                     18 | False          | False        |
| Thursday  | end-pass erased0.5 J-lens               | True          |          1         |            10 |                      3 | False          | False        |
| Thursday  | end-pass erased1 plain24                | False         |          1         |          1371 |                   5192 | False          | False        |
| Thursday  | end-pass erased0.5 plain24              | False         |          1         |          1699 |                   4861 | False          | False        |
| Thursday  | end-pass erased1 plain27                | True          |          1         |            22 |                    127 | True           | True         |
| Thursday  | end-pass erased0.5 plain27              | False         |          1         |            35 |                     15 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 J-lens  | True          |          1         |            10 |                      3 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 plain24 | False         |          1         |          1689 |                   4840 | False          | False        |
| Thursday  | end-pass input-prefix erased0.5 plain27 | False         |          1         |            34 |                     15 | False          | False        |
| Thursday  | end-pass input-prefix J-lens            | True          |          1         |             4 |                      2 | False          | False        |
| autumn    | J-lens                                  | False         |          0.371658  |            19 |                      0 | False          | False        |
| autumn    | plain lens                              | False         |          0.513369  |          1874 |                    402 | False          | False        |
| autumn    | end-pass J-lens                         | True          |          1         |            14 |             1000000000 | True           | False        |
| autumn    | end-pass logit contrast J-lens          | False         |          1         |         46085 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast J-lens    | True          |          0.617647  |            14 |             1000000000 | True           | False        |
| autumn    | end-pass plain24                        | False         |          1         |          1872 |             1000000000 | False          | False        |
| autumn    | end-pass logit contrast plain24         | False         |          1         |        239353 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain24   | False         |          0.735294  |         67324 |             1000000000 | False          | False        |
| autumn    | end-pass plain27                        | True          |          1         |            19 |             1000000000 | True           | False        |
| autumn    | end-pass logit contrast plain27         | False         |          1         |        231836 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain27   | True          |          0.882353  |            20 |             1000000000 | True           | False        |
| autumn    | end-pass negative final control         | False         |          1         |        243744 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 J-lens                 | False         |          1         |           112 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 J-lens               | True          |          1         |            24 |             1000000000 | True           | False        |
| autumn    | end-pass erased1 plain24                | False         |          1         |          2802 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 plain24              | False         |          1         |          3670 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain27                | True          |          1         |            61 |             1000000000 | False          | True         |
| autumn    | end-pass erased0.5 plain27              | True          |          1         |            25 |             1000000000 | True           | True         |
| autumn    | end-pass input-prefix erased0.5 J-lens  | True          |          1         |            21 |             1000000000 | True           | False        |
| autumn    | end-pass input-prefix erased0.5 plain24 | False         |          1         |          3656 |             1000000000 | False          | False        |
| autumn    | end-pass input-prefix erased0.5 plain27 | True          |          1         |            25 |             1000000000 | True           | True         |
| autumn    | end-pass input-prefix J-lens            | True          |          1         |            12 |             1000000000 | True           | False        |
| apple     | J-lens                                  | False         |          0         |           181 |                      0 | False          | False        |
| apple     | plain lens                              | False         |          0.0833333 |           359 |                    320 | False          | False        |
| apple     | end-pass J-lens                         | False         |          1         |           171 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast J-lens          | False         |          1         |        117906 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast J-lens    | False         |          0.694444  |           325 |             1000000000 | False          | False        |
| apple     | end-pass plain24                        | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast plain24         | False         |          1         |        223180 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain24   | False         |          0.777778  |           372 |             1000000000 | False          | False        |
| apple     | end-pass plain27                        | False         |          1         |           116 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast plain27         | False         |          1         |        217940 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain27   | False         |          0.833333  |           121 |             1000000000 | False          | False        |
| apple     | end-pass negative final control         | False         |          1         |        225716 |             1000000000 | False          | False        |
| apple     | end-pass erased1 J-lens                 | False         |          1         |           124 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 J-lens               | False         |          1         |           137 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain24                | False         |          1         |           374 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain24              | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain27                | False         |          1         |            88 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain27              | False         |          1         |           102 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 J-lens  | False         |          1         |           131 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 plain24 | False         |          1         |           356 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix erased0.5 plain27 | False         |          1         |           102 |             1000000000 | False          | False        |
| apple     | end-pass input-prefix J-lens            | False         |          1         |           165 |             1000000000 | False          | False        |
| violin    | J-lens                                  | False         |          0.958929  |            18 |                    917 | True           | True         |
| violin    | plain lens                              | False         |          0.970536  |          9264 |                   7561 | False          | False        |
| violin    | end-pass J-lens                         | False         |          0.958929  |            18 |                    911 | True           | True         |
| violin    | end-pass logit contrast J-lens          | False         |          0.833036  |        163428 |                 216018 | False          | False        |
| violin    | end-pass probability contrast J-lens    | False         |          0.744196  |            18 |                   5238 | True           | True         |
| violin    | end-pass plain24                        | False         |          0.970536  |          9256 |                   7554 | False          | False        |
| violin    | end-pass logit contrast plain24         | False         |          0.814286  |        242109 |                 236231 | False          | False        |
| violin    | end-pass probability contrast plain24   | False         |          0.497321  |        132477 |                  38254 | False          | False        |
| violin    | end-pass plain27                        | False         |          0.985714  |            32 |                     12 | False          | False        |
| violin    | end-pass logit contrast plain27         | False         |          0.867857  |        181200 |                 171002 | False          | False        |
| violin    | end-pass probability contrast plain27   | True          |          0.749554  |            31 |                     10 | False          | False        |
| violin    | end-pass negative final control         | False         |          0.799107  |        245367 |                 237474 | False          | False        |
| violin    | end-pass erased1 J-lens                 | True          |          0.967857  |            23 |                    830 | True           | True         |
| violin    | end-pass erased0.5 J-lens               | True          |          0.9625    |            21 |                    789 | True           | True         |
| violin    | end-pass erased1 plain24                | False         |          0.971429  |         10663 |                   8609 | False          | False        |
| violin    | end-pass erased0.5 plain24              | False         |          0.971429  |          9948 |                   8118 | False          | False        |
| violin    | end-pass erased1 plain27                | False         |          0.985714  |            37 |                     13 | False          | False        |
| violin    | end-pass erased0.5 plain27              | False         |          0.985714  |            32 |                     12 | False          | False        |
| violin    | end-pass input-prefix erased0.5 J-lens  | True          |          0.9625    |            20 |                    780 | True           | True         |
| violin    | end-pass input-prefix erased0.5 plain24 | False         |          0.971429  |          9936 |                   8110 | False          | False        |
| violin    | end-pass input-prefix erased0.5 plain27 | True          |          0.985714  |            29 |                     10 | False          | False        |
| violin    | end-pass input-prefix J-lens            | False         |          0.958929  |            17 |                    903 | True           | True         |
| Hamlet    | J-lens                                  | False         |          0.673333  |           202 |                      0 | False          | False        |
| Hamlet    | plain lens                              | False         |          0.606667  |          6834 |                    100 | False          | False        |
| Hamlet    | end-pass J-lens                         | False         |          0.86      |           200 |                      0 | False          | False        |
| Hamlet    | end-pass logit contrast J-lens          | False         |          0.613333  |        211489 |                  11537 | False          | False        |
| Hamlet    | end-pass probability contrast J-lens    | False         |          0.453333  |           243 |                      0 | False          | False        |
| Hamlet    | end-pass plain24                        | False         |          0.713333  |          6834 |                    100 | False          | False        |
| Hamlet    | end-pass logit contrast plain24         | False         |          0.546667  |        238152 |                 189827 | False          | False        |
| Hamlet    | end-pass probability contrast plain24   | False         |          0.493333  |          7695 |                    686 | False          | False        |
| Hamlet    | end-pass plain27                        | False         |          0.726667  |           485 |                      3 | False          | False        |
| Hamlet    | end-pass logit contrast plain27         | False         |          0.54      |        219517 |                  80841 | False          | False        |
| Hamlet    | end-pass probability contrast plain27   | False         |          0.433333  |           500 |                      3 | False          | False        |
| Hamlet    | end-pass negative final control         | False         |          0.526667  |        247175 |                 207550 | False          | False        |
| Hamlet    | end-pass erased1 J-lens                 | False         |          0.856667  |           184 |                      0 | False          | False        |
| Hamlet    | end-pass erased0.5 J-lens               | False         |          0.866667  |           196 |                      0 | False          | False        |
| Hamlet    | end-pass erased1 plain24                | False         |          0.713333  |          6955 |                    103 | False          | False        |
| Hamlet    | end-pass erased0.5 plain24              | False         |          0.713333  |          6745 |                    104 | False          | False        |
| Hamlet    | end-pass erased1 plain27                | False         |          0.72      |           477 |                      3 | False          | False        |
| Hamlet    | end-pass erased0.5 plain27              | False         |          0.723333  |           482 |                      3 | False          | False        |
| Hamlet    | end-pass input-prefix erased0.5 J-lens  | False         |          0.866667  |           194 |                      0 | False          | False        |
| Hamlet    | end-pass input-prefix erased0.5 plain24 | False         |          0.713333  |          6728 |                    104 | False          | False        |
| Hamlet    | end-pass input-prefix erased0.5 plain27 | False         |          0.723333  |           475 |                      3 | False          | False        |
| Hamlet    | end-pass input-prefix J-lens            | False         |          0.86      |           198 |                      0 | False          | False        |
| hydrogen  | J-lens                                  | False         |          0.0444444 |           232 |                     22 | False          | False        |
| hydrogen  | plain lens                              | False         |          0         |         62558 |                  10267 | False          | False        |
| hydrogen  | end-pass J-lens                         | False         |          1         |           226 |             1000000000 | False          | False        |
| hydrogen  | end-pass logit contrast J-lens          | False         |          1         |         97652 |             1000000000 | False          | False        |
| hydrogen  | end-pass probability contrast J-lens    | False         |          0.944444  |           248 |             1000000000 | False          | False        |
| hydrogen  | end-pass plain24                        | False         |          1         |         62544 |             1000000000 | False          | False        |
| hydrogen  | end-pass logit contrast plain24         | False         |          1         |        240782 |             1000000000 | False          | False        |
| hydrogen  | end-pass probability contrast plain24   | False         |          0.666667  |        222459 |             1000000000 | False          | False        |
| hydrogen  | end-pass plain27                        | False         |          1         |          7811 |             1000000000 | False          | False        |
| hydrogen  | end-pass logit contrast plain27         | False         |          1         |        231281 |             1000000000 | False          | False        |
| hydrogen  | end-pass probability contrast plain27   | False         |          0.5       |    1000000000 |             1000000000 | False          | False        |
| hydrogen  | end-pass negative final control         | False         |          1         |        216665 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased1 J-lens                 | False         |          1         |           248 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased0.5 J-lens               | False         |          1         |           228 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased1 plain24                | False         |          1         |         62401 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased0.5 plain24              | False         |          1         |         62276 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased1 plain27                | False         |          1         |          6849 |             1000000000 | False          | False        |
| hydrogen  | end-pass erased0.5 plain27              | False         |          1         |          6809 |             1000000000 | False          | False        |
| hydrogen  | end-pass input-prefix erased0.5 J-lens  | False         |          1         |           224 |             1000000000 | False          | False        |
| hydrogen  | end-pass input-prefix erased0.5 plain24 | False         |          1         |         62163 |             1000000000 | False          | False        |
| hydrogen  | end-pass input-prefix erased0.5 plain27 | False         |          1         |          6792 |             1000000000 | False          | False        |
| hydrogen  | end-pass input-prefix J-lens            | False         |          1         |           224 |             1000000000 | False          | False        |
| triangle  | J-lens                                  | True          |          1         |            23 |                   9725 | True           | True         |
| triangle  | plain lens                              | False         |          1         |          4908 |                 209250 | False          | False        |
| triangle  | end-pass J-lens                         | True          |          1         |            23 |                   9724 | True           | True         |
| triangle  | end-pass logit contrast J-lens          | False         |          1         |        225706 |                 248037 | False          | False        |
| triangle  | end-pass probability contrast J-lens    | True          |          0.833333  |            24 |             1000000000 | True           | True         |
| triangle  | end-pass plain24                        | False         |          1         |          4908 |                 209249 | False          | False        |
| triangle  | end-pass logit contrast plain24         | False         |          1         |        246465 |                 248037 | False          | False        |
| triangle  | end-pass probability contrast plain24   | False         |          0.733333  |          9639 |             1000000000 | False          | False        |
| triangle  | end-pass plain27                        | True          |          1         |            61 |                 194219 | False          | True         |
| triangle  | end-pass logit contrast plain27         | False         |          1         |        243289 |                 248037 | False          | False        |
| triangle  | end-pass probability contrast plain27   | True          |          0.833333  |            94 |             1000000000 | False          | True         |
| triangle  | end-pass negative final control         | False         |          1         |        247194 |                 248037 | False          | False        |
| triangle  | end-pass erased1 J-lens                 | False         |          1         |            35 |                  11331 | False          | False        |
| triangle  | end-pass erased0.5 J-lens               | True          |          1         |            25 |                  10108 | True           | True         |
| triangle  | end-pass erased1 plain24                | False         |          1         |         10456 |                 212391 | False          | False        |
| triangle  | end-pass erased0.5 plain24              | False         |          1         |          7349 |                 210750 | False          | False        |
| triangle  | end-pass erased1 plain27                | True          |          1         |            73 |                 198688 | False          | True         |
| triangle  | end-pass erased0.5 plain27              | True          |          1         |            65 |                 195752 | False          | True         |
| triangle  | end-pass input-prefix erased0.5 J-lens  | True          |          1         |            22 |                  10037 | True           | True         |
| triangle  | end-pass input-prefix erased0.5 plain24 | False         |          1         |          7326 |                 210411 | False          | False        |
| triangle  | end-pass input-prefix erased0.5 plain27 | True          |          1         |            64 |                 195433 | False          | True         |
| triangle  | end-pass input-prefix J-lens            | True          |          1         |            20 |                   9653 | True           | True         |

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

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

J-lens: [' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Facts', ' Unknown', '**', ' Sound', ' Actually', ' known', ' Silent', ' vocals', ' Nothing', ' auditory', ' Based', ' unknown', ' violin', ' piano', ' Founded', ' Guitar', ' Heard', 'actually', ' Audio', 'unknown', '声乐', ' drums', ' Wood', '…**', ' flute', ' acoustic']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

plain lens: ['xhr', ' صدا', ' beleg', '的事实', ' percussion', '...(', ' theirs', ' warta', 'ốn', ' факта', ' pipa', ' fapt', '小编为大家整理的', ' Isles', ' ですが', 'плы', 'acre', '事实', 'ungi', '沉寂', '树人', 'ässe', ' gry', 'đu', 'โปรด', 'ագ', '(eventName', 'đenje', '(&:', '..........', 'actually', '단은']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass J-lens: [' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Facts', ' Unknown', '**', ' Sound', ' Actually', ' known', ' Silent', ' vocals', ' Nothing', ' auditory', ' Based', ' unknown', ' violin', ' piano', ' Founded', ' Guitar', ' Heard', 'actually', ' Audio', 'unknown', '声乐', ' drums', ' Wood', '…**', ' flute', ' acoustic']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass logit contrast J-lens: [' **—', ' Arte', ' Masks', ' Machines', 'ťa', ' Whites', ' Centrale', ' Equipment', ' Cargo', ' Telescope', ' Ung', ' Canal', ' Representatives', ' Resistance', ' Câ', ' **■', ' Machinery', ' Islands', ' Parab', ' Mixer', ' Rotate', ' Vehicles', ' Appliances', ':NO', ' Verte', ' Agua', ' Tele', ' Grinder', ' жаре', ' Broadcasting', ' Mask', ' Unik']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass probability contrast J-lens: [' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Facts', ' Unknown', ' Sound', ' Actually', ' Silent', ' known', ' vocals', ' Nothing', ' unknown', ' auditory', ' Based', ' piano', ' violin', ' Founded', ' Heard', ' Guitar', ' Audio', 'actually', '声乐', ' drums', 'unknown', '…**', ' acoustic', ' flute', ' Wood', ' none']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass plain24: ['xhr', ' صدا', ' beleg', '...(', '的事实', ' percussion', ' warta', 'ốn', ' факта', ' pipa', ' fapt', ' Isles', '小编为大家整理的', 'плы', ' ですが', 'acre', 'ungi', '事实', 'ässe', '沉寂', '树人', ' gry', 'đu', 'โปรด', 'ագ', '(eventName', 'actually', '(&:', '..........', '단은', 'đenje', ' famously']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass logit contrast plain24: ['intégration', ' Sán', '马拉', ' Краси', ' Автомоби', 'ψη', 'empf', ' スポンサー', 'ạy', ' Putih', 'ọa', 'áles', ' cargos', 'ủy', ' Разу', ' trasparen', '_cpus', ' ГИБ', '일자', ' Росси', ' egt', ' ということで', 'ehrte', ' Alegre', ' Степа', ' โรคสะเก็ดเงิน', ' Tô', 'ườ', 'ťa', ' discu', '九寨', '[]={']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass probability contrast plain24: ['xhr', ' صدا', ' beleg', '...(', '的事实', ' warta', 'ốn', ' факта', ' pipa', ' fapt', ' percussion', ' Isles', '小编为大家整理的', 'плы', ' ですが', 'acre', 'ungi', '事实', 'ässe', '树人', '沉寂', ' gry', 'đu', 'โปรด', 'ագ', '(eventName', 'đenje', '(&:', '단은', '..........', 'ぶり', '祉']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass plain27: ['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' instrumental', ' Wind', ' instruments', ' brass', 'Wind', ' strings', ' Strings', ' drums', ' pipa', 'Strings', '打击', '风能', ' Instruments', '鼓', '声器', '风的', 'strings', '键盘', ' Perc', '风管', '.wind', '_string', '风和', ' sax', ' Brass']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass logit contrast plain27: [' Краси', ' Разу', ' Автомоби', ' Nichtra', '��', ' Евге', 'āja', ' Хабар', ' Tô', ' Степа', ' Росси', ' Regionale', ' Еги', ' Blasio', '迪亚', ' ということで', ' ГИБ', ' Juta', '投资事件', 'の販', ' Especi', ' Апре', '_deploy', ' Politica', '如荼', 'intégration', '託', ' Alegre', ' Разви', ' Изу', ' Gerindra', '锦涛']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass probability contrast plain27: ['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' instrumental', ' Wind', ' instruments', ' strings', ' brass', 'Wind', ' Strings', ' drums', ' pipa', '风能', '打击', ' Instruments', '鼓', '声器', '风的', '键盘', '.wind', '风管', ' Perc', '风和', '_string', ' sax', ' Brass', 'STRING', ' viol']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass negative final control: ['altungs', '逃', 'ajs', ' Автомоби', 'iliz', '耘', 'iesto', '渣', '敖', 'intégration', ' cargos', '云峰', 'าลัย', 'isté', ' Tô', ' Ranh', ' Olah', 'ítása', 'usza', ' giveaways', 'ítás', 'iciais', '_dl', '($_', '摩尔', 'Nya', ' mAh', ' Jal', ' Addr', ' έγι', '累計', 'orelease']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased1 J-lens: [' nonexistent', ' percussion', ' Vocal', ' vocal', ' **—', '…**', ' **:**', ' Known', ' Unknown', ' Facts', ' **.**', ' **', ' Heard', ' vocals', ' Sound', ' Silent', ' **.', ' Founded', ' auditory', '声乐', ' Guitar', ' Nothing', '__;', ' violin', ' Choir', "'**", ' Listener', ' Audio', ' drums', ' Actually', ' unknown', ' piano']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased0.5 J-lens: [' percussion', ' nonexistent', ' Vocal', ' vocal', ' **', ' Known', ' Facts', ' Unknown', ' Sound', ' **—', '…**', ' vocals', ' Silent', ' Actually', ' Heard', ' auditory', ' Nothing', ' **:**', ' unknown', ' Founded', ' known', ' Guitar', ' violin', ' piano', '声乐', ' **.**', ' Based', ' Audio', ' **.', 'actually', ' drums', ' Choir']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased1 plain24: ['xhr', ' صدا', ' beleg', ' warta', '...(', '的事实', 'ốn', ' pipa', ' ですが', '小编为大家整理的', ' percussion', 'плы', ' факта', 'đu', ' fapt', 'ässe', ' Isles', 'acre', ' ;-)', '树人', '__;', ' gry', ' スポンサー', '沉寂', 'โปรด', 'ungi', 'đenje', ' spok', '祉', 'ぶり', 'ագ', '(eventName']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased0.5 plain24: ['xhr', ' صدا', ' beleg', '...(', ' warta', '的事实', ' percussion', 'ốn', ' pipa', '小编为大家整理的', ' факта', ' ですが', 'плы', ' Isles', ' fapt', 'acre', 'ässe', 'đu', '树人', 'ungi', '沉寂', ' gry', 'โปรด', '事实', 'ագ', 'đenje', '__;', ' ;-)', '祉', '(eventName', '단은', '(&:']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased1 plain27: ['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' instrumental', ' instruments', ' Wind', ' brass', ' pipa', 'Wind', ' Strings', ' strings', '风能', ' drums', '打击', 'Strings', ' Instruments', '声器', '风的', '.wind', '鼓', '键盘', 'strings', '风管', ' Perc', '风和', '打擊', '_string', ' sax']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass erased0.5 plain27: ['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' instrumental', ' Wind', ' instruments', ' brass', 'Wind', ' strings', ' Strings', ' pipa', ' drums', '风能', 'Strings', '打击', ' Instruments', '声器', '鼓', '风的', 'strings', '键盘', ' Perc', '.wind', '风管', '风和', '_string', ' sax', ' Brass']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass input-prefix erased0.5 J-lens: [' percussion', ' nonexistent', ' Vocal', ' vocal', ' **', ' Known', ' Unknown', ' Sound', ' **—', '…**', ' vocals', ' Silent', ' Actually', ' Heard', ' auditory', ' Nothing', ' **:**', ' Founded', ' unknown', ' known', ' Guitar', ' violin', '声乐', ' piano', ' Based', ' **.**', 'actually', ' Audio', ' **.', ' drums', ' Choir', ' flute']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass input-prefix erased0.5 plain24: ['xhr', ' صدا', ' beleg', '...(', ' warta', '的事实', ' percussion', 'ốn', ' pipa', '小编为大家整理的', ' факта', ' ですが', 'плы', ' Isles', ' fapt', 'acre', 'ässe', 'đu', '树人', 'ungi', '沉寂', ' gry', 'โปรด', '事实', 'ագ', 'đenje', '__;', ' ;-)', '祉', '(eventName', '단은', '(&:']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass input-prefix erased0.5 plain27: ['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' Wind', ' brass', 'Wind', ' Strings', ' strings', ' pipa', ' drums', '风能', '打击', 'Strings', '声器', '鼓', '风的', 'strings', '键盘', '.wind', ' Perc', '风管', '风和', '_string', ' Brass', ' sax', ' Winds', ' viol', 'STRING']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.\n\n**Reasoning:**\n1.  **Identify the instrument:**'

end-pass input-prefix J-lens: [' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Unknown', '**', ' Sound', ' Actually', ' Silent', ' known', ' vocals', ' Nothing', ' Based', ' auditory', ' unknown', ' piano', ' violin', ' Founded', ' Guitar', 'actually', ' Heard', ' Audio', '声乐', ' drums', 'unknown', ' Wood', '…**', ' acoustic', ' flute', ' none']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

J-lens: [' Shakespeare', ' Robert', ' William', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Edmund', ' Aristotle', ' Tolkien', ' Richard', ' Charles', ' Edward', ' George', ' Samuel', 'Robert', ' Sir', ' Julius', ' Stephen', ' Rowling', ' Dickens', '莎士比亚', ' James', ' Hugo', ' Thomas', ' Benjamin', ' Daniel', 'Henry', 'William', ' Theodore', 'John']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

plain lens: ['akespeare', '佚', ' onstage', '...(', ' tragedia', 'ťa', ' famously', ' **:**', ' spok', 'чиной', ' greve', ' Ata', 'icide', 'র্ত', ' mily', ' _______,', '-fiction', ' Laufe', '自来', '马拉', '?...', 'trar', 'vias', ' Hinblick', 'ehrte', ' berüh', 'меется', ' spiritu', ' työn', ' sanks', ' fisse', 'ću']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass J-lens: [' Shakespeare', ' Robert', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Edmund', ' Aristotle', ' Tolkien', ' Richard', ' Charles', ' Edward', ' Samuel', ' George', 'Robert', ' Sir', ' Julius', ' Stephen', ' Rowling', ' Dickens', '莎士比亚', ' James', ' Hugo', ' Thomas', 'Henry', ' Daniel', ' Benjamin', ' Theodore', 'John', ' Harry', ' Gabriel']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass logit contrast J-lens: [' Robbins', ' Roths', ' Moses', ' Roberts', ' Rowling', ' Robert', ' Bob', ' Lucas', ' Dumbledore', ' Lynch', ' Roosevelt', ' Betty', ' Alic', ' Timothy', ' Rosie', ' Melania', 'itelj', ' Romans', ' Hillary', ' Muss', ' Jefferson', ' Rob', ' Tiffany', ' Riv', ' Rogers', ' Neville', ' Lucy', ' Pins', ' Pug', ' Luke', ' Rum', ' Robertson']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass probability contrast J-lens: [' Shakespeare', ' Robert', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Aristotle', ' Edmund', ' Tolkien', ' Richard', ' Charles', ' Edward', ' George', ' Samuel', ' Sir', 'Robert', ' Julius', ' Stephen', ' Rowling', ' Dickens', '莎士比亚', ' Hugo', ' James', ' Thomas', ' Benjamin', ' Daniel', ' Theodore', ' Harry', 'Henry', ' Gabriel', ' Arthur']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass plain24: ['akespeare', '佚', ' onstage', '...(', ' tragedia', 'ťa', ' famously', ' **:**', ' spok', 'чиной', ' greve', ' Ata', 'icide', 'র্ত', ' mily', ' _______,', '-fiction', ' Laufe', '自来', '马拉', '?...', 'trar', 'vias', ' Hinblick', 'ehrte', ' berüh', 'меется', ' spiritu', ' työn', ' sanks', ' fisse', 'ću']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass logit contrast plain24: [' greve', ' svel', ' نجوم', ' رياض', ' رابط', ' Ata', ' スポンサー', ' spez', 'проце', ' subven', 'พาน', 'клеи', ' โรคสะเก็ดเงิน', 'ộp', 'снабжение', '咙', ' Pony', 'Ổ', 'ujuan', 'čaju', ' Vaksin', 'ポリエステ', 'ajes', ' lanzó', 'стій', ' Груп', 'будьте', 'jalanan', ' Pelabuhan', ' prospet', ' Attra', ' rivolg']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass probability contrast plain24: ['akespeare', '佚', ' onstage', '...(', 'ťa', ' tragedia', ' spok', ' **:**', ' famously', 'чиной', ' greve', ' Ata', 'icide', ' mily', 'র্ত', ' _______,', '自来', ' Laufe', '-fiction', '马拉', 'trar', '?...', 'vias', ' Hinblick', 'ehrte', 'меется', ' berüh', ' työn', ' spiritu', ' sanks', ' fisse', ' vaid']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass plain27: ['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' Shakespe', ' مسرح', '-play', ' Plays', 'icide', ' playwright', ' المسرح', ' tragedia', 'ốn', ' Mancha', '-fiction', '该剧', '话剧', ' teatr', 'коле', ' théâtre', 'ốc', 'oling', 'åde', ' sien', ' îns', ' teb', ' traged', 'erval', 'Sir', 'πτωση']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass logit contrast plain27: [' pouc', ' Satgas', '/Branch', ' Пита', 'čaju', ' Jurusan', 'atasan', ' greve', ' seques', 'ATUR', ' sese', ' laks', 'كيم', ' szen', ' egt', ' sét', 'tés', ' スポンサー', ' setHidden', 'angguan', 'itelji', ' concurr', 'jekte', ' Attra', 'ẳn', 'OffsetTable', ' Panitia', 'IPPING', ' chatte', 'ležitost', ' exitos', ' Juta']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass probability contrast plain27: ['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' Shakespe', ' مسرح', '-play', ' Plays', 'icide', ' playwright', ' المسرح', ' tragedia', 'ốn', ' Mancha', '-fiction', '该剧', '话剧', ' teatr', 'ốc', 'коле', ' théâtre', 'åde', 'oling', 'πτωση', ' îns', ' teb', ' sien', 'erval', ' traged', 'émie']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass negative final control: [' lesbische', '铃声', ' Palav', 'atasan', 'ffy', '咙', ' Posta', '连云', ' Panels', ' Attra', 'ibox', '_Panel', 'ТС', 'Ỏ', 'itere', '冲冲', ' movil', '.HttpStatus', ' Personali', ' Rays', ' Logs', '眼了', ' fetisch', '面板', 'quetas', 'úz', ' Pej', 'ଛ', 'ATAB', '云上', ' YYS', '专车']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased1 J-lens: [' Shakespeare', ' **', ' Robert', ' Aristotle', ' Tolkien', ' Sir', 'akespeare', ' Elizabeth', ' John', ' Edmund', ' Christopher', ' Henry', ' Richard', ' Hugo', ' Dickens', ' Julius', ' George', ' English', ' himself', ' Rowling', ' Luke', ' Bob', ' Samuel', ' Charles', ' Daniel', ' Jane', ' Harry', ' Mozart', ' Romeo', ' Hans', ' Peter', '**']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased0.5 J-lens: [' Shakespeare', ' Robert', 'akespeare', ' Aristotle', ' Henry', ' Tolkien', ' Elizabeth', ' John', ' Edmund', ' Christopher', ' **', ' Sir', ' Richard', ' George', ' Julius', ' Samuel', ' Charles', ' Dickens', ' Hugo', ' Edward', ' Rowling', ' Daniel', ' Stephen', ' himself', '莎士比亚', ' Luke', ' Harry', ' Thomas', ' James', ' English', ' Benjamin', ' Jane']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased1 plain24: ['akespeare', '佚', ' onstage', '...(', 'ťa', ' famously', ' tragedia', 'чиной', 'icide', ' **:**', ' Ata', ' spok', 'র্ত', ' greve', '自来', ' Laufe', '马拉', '-fiction', ' _______,', ' mily', '?...', ' Hinblick', 'trar', ' berüh', 'vias', ' îns', 'ehrte', 'टक', ' työn', ' vaid', ' spiritu', 'меется']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased0.5 plain24: ['akespeare', '佚', ' onstage', '...(', 'ťa', ' tragedia', ' famously', 'чиной', ' **:**', ' spok', ' Ata', 'icide', 'র্ত', ' greve', '自来', ' Laufe', ' mily', '-fiction', ' _______,', '马拉', '?...', ' Hinblick', 'trar', ' berüh', 'vias', 'ehrte', ' spiritu', 'меется', 'टक', ' työn', ' vaid', ' fisse']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased1 plain27: ['akespeare', ' شك', ' onstage', ' Shakespeare', '这部剧', '莎士比亚', '-play', ' مسرح', 'icide', ' Shakespe', ' playwright', ' المسرح', ' Plays', 'ốn', '该剧', 'ốc', ' tragedia', '-fiction', ' Mancha', 'коле', '话剧', ' îns', 'émie', 'oling', ' sien', ' théâtre', ' Guild', ' Cie', '屠', 'åde', '戏剧', 'erval']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass erased0.5 plain27: ['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' مسرح', ' Shakespe', '-play', 'icide', ' playwright', ' Plays', ' المسرح', ' tragedia', 'ốn', ' Mancha', '该剧', '-fiction', '话剧', 'ốc', 'коле', ' îns', 'oling', ' sien', ' teatr', 'åde', ' théâtre', 'émie', 'erval', 'πτωση', ' teb', 'Sir']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' Shakespeare', ' Robert', 'akespeare', ' Aristotle', ' Henry', ' Tolkien', ' Elizabeth', ' John', ' Edmund', ' Christopher', ' **', ' Sir', ' Richard', ' George', ' Julius', ' Samuel', ' Charles', ' Dickens', ' Hugo', ' Edward', ' Rowling', ' Daniel', ' Stephen', ' himself', '莎士比亚', ' Luke', ' Harry', ' Thomas', ' James', ' English', ' Benjamin', ' Jane']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['akespeare', '佚', ' onstage', '...(', 'ťa', ' tragedia', ' famously', 'чиной', ' **:**', ' spok', ' Ata', 'icide', 'র্ত', ' greve', '自来', ' Laufe', ' mily', '-fiction', ' _______,', '马拉', '?...', ' Hinblick', 'trar', ' berüh', 'vias', 'ehrte', ' spiritu', 'меется', 'टक', ' työn', ' vaid', ' fisse']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' مسرح', ' Shakespe', '-play', 'icide', ' المسرح', ' tragedia', 'ốn', ' Mancha', '-fiction', '该剧', '话剧', 'ốc', 'коле', ' îns', ' teatr', ' sien', 'oling', 'åde', 'émie', ' théâtre', 'πτωση', 'erval', ' teb', 'Sir', 'engang', ' traged']

Input: "<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

Baseline: 'William Shakespeare<|im_end|>'

end-pass input-prefix J-lens: [' Shakespeare', ' Robert', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Edmund', ' Aristotle', ' Tolkien', ' Richard', ' Charles', ' Edward', ' Samuel', ' George', 'Robert', ' Sir', ' Julius', ' Stephen', ' Dickens', ' Rowling', '莎士比亚', ' James', ' Hugo', ' Thomas', ' Benjamin', ' Daniel', 'Henry', ' Harry', 'John', ' Gabriel', ' **']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

J-lens: ['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' gases', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ':...', ' Facts', '固态', '液体', ' Answer', ' Gas', ' **—', 'gas', '-fluid', ' Liqu', '：**', ' frozen', 'Gas', ' gas']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

plain lens: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', 'utow', '常温', 'ائع', 'geries', ' berüh', '英文名称', '加拿大的', '我来说', ' lique', ' الاعتبار', 'anime', ' kwest', 'vestig', 'irie', ' утвер', 'liquid', '件事', 'iration', ' liquids', ' gases', '.freeze', ' Awake', ' physicists', ' газо', '-fluid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass J-lens: ['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ':...', ' Facts', '固态', '液体', ' **—', ' Answer', '-fluid', '：**', ' Liqu', ' frozen', ' Frozen', ' soluble', ' **:**', '液体的', '**:']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass logit contrast J-lens: [':__', ')__', ' Whites', ' Mines', ' Stateless', ' **—', '.www', ' |–', ' undermin', 'udahkan', 'дельник', ' Món', ' verzek', ' **>>', 'πεζ', 'imals', ' Machines', ' fluids', 'ocities', '__:', 'ieties', '마자', ' POLÍT', ' Emails', ' Pregun', ' Konkur', '#__', '白光', 'elok', ' Downs', ' PÚBL', 'кологи']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass probability contrast J-lens: ['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' vapor', 'fluid', ' Vapor', ' fluids', 'Liquid', ' fluid', ' Fluid', ':...', ' Facts', '固态', '液体', ' **—', ' Answer', '-fluid', '：**', ' Liqu', ' frozen', ' **:**', ' soluble', ' Frozen', '液体的', '**:']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass plain24: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', 'utow', '常温', 'ائع', 'geries', ' berüh', '英文名称', '加拿大的', '我来说', ' lique', ' الاعتبار', 'anime', 'vestig', ' kwest', 'irie', ' утвер', 'liquid', '件事', 'iration', ' liquids', '.freeze', ' Awake', ' physicists', ' газо', ' pione', '-fluid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass logit contrast plain24: ['马拉', ' совмести', 'ehrt', ' prostytut', ' 웹사이트가', '위원장', ' Jardim', ' Geile', '加拿大的', 'iciels', ' jente', ' المعم', 'éclairage', 'betaling', '稼ぎ', 'intégration', 'ministra', 'ieties', 'église', 'ตั๋ว', 'افية', 'euillez', 'izers', 'izare', 'снабжение', ' Konkur', ' Sán', ' Playstation', 'orías', 'acza', '迪士', ' pione']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass probability contrast plain24: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', 'utow', '常温', 'geries', 'ائع', ' berüh', '英文名称', '加拿大的', '我来说', ' lique', ' الاعتبار', 'anime', 'irie', ' kwest', 'vestig', ' утвер', '件事', 'iration', ' liquids', '.freeze', ' Awake', ' physicists', ' газо', ' pione', 'разу', '-fluid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass plain27: ['气体', '气体的', '_gas', ' газ', '气', '的气体', ' газо', ' газа', '固态', ' گاز', ' الغاز', ' gaz', ' liquid', ' غاز', ' gás', '液态', 'gaz', ' газов', 'liquid', '氣體', '的气', 'غاز', 'ก๊าซ', ' liquids', 'ガス', ' Газ', '气的', '气和', '固体', '气了', ' Liquid', 'solid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass logit contrast plain27: ['위원장', ' Jardim', '加拿大的', ' Gerindra', ' Росси', 'дельник', 'onomies', '่อง', 'azes', ' Maranh', '埔寨', ' prostytut', 'onesa', 'izers', 'mény', 'toffe', 'iciels', '인증', 'をストック', ' Ristorante', '신문', 'izzano', 'ehrt', ' шос', '_transactions', ' 웹사이트가', 'боле', 'ススメ', ' Konkur', ' Moraes', 'integrazione', '_interfaces']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass probability contrast plain27: ['气体', '气体的', '_gas', ' газ', '气', '的气体', ' газо', ' газа', '固态', ' گاز', ' gaz', ' الغاز', ' غاز', ' gás', '液态', ' газов', 'gaz', '氣體', '的气', 'غاز', 'ก๊าซ', ' liquids', 'ガス', ' Газ', '气的', '气和', '固体', '气了', '天然气', ' lỏng', '가스', ' gaze']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass negative final control: [' urls', ' التم', '垂', ' باك', ' Edels', '_tm', '(DIR', 'скле', 'клады', '驹', ' Ün', 'tiges', 'onesa', '机芯', 'ímos', 'ieties', 'éries', 'ältä', '#__', '_MA', ' URLs', ' Whites', '马拉', 'ätter', 'теры', 'iesto', '/bg', ' tranny', ' знамени', ' VNĐ', 'ЕК', '拉拉']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased1 J-lens: [' **', '**', ' liquid', 'liquid', ' liquids', ' Liquid', '液态', ' lique', '…**', '...**', '...', ' vapor', '�', ' Facts', ' fluid', ' fluids', ' Answer', 'fluid', ' Vapor', '**:', '…', 'Liquid', ' frozen', '____', '固态', 'Answer', ' ...', '________', ' Fluid', '：**', ' According', ' soluble']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased0.5 J-lens: [' **', '**', 'liquid', ' liquid', ' Liquid', ' liquids', '液态', '…**', ' lique', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Facts', ' Answer', ' Fluid', '固态', ':...', '**:', ' frozen', '�', '：**', '...', '液体', ' soluble', 'Answer', ' According', '____', '________']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased1 plain24: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', '常温', 'โปร่ง', '我来说', 'utow', '英文名称', 'ائع', ' berüh', ' утвер', ' lique', '件事', 'anime', 'geries', 'vestig', ' الاعتبار', 'irie', ' kwest', 'iration', '-free', '.freeze', '加拿大的', '本题考查', ' liquids', 'free', ' Awake', ' physicists', '猜想']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased0.5 plain24: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', '常温', 'utow', '我来说', '英文名称', 'ائع', ' berüh', 'geries', ' lique', ' الاعتبار', 'anime', ' утвер', '加拿大的', 'vestig', '件事', 'irie', ' kwest', 'iration', 'liquid', '.freeze', ' liquids', ' Awake', ' physicists', '本题考查', 'free', '-free']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased1 plain27: ['固态', ' liquid', '液态', '气', ' liquids', ' solid', '固体', '...', 'liquid', ' твер', ' lỏng', ' газо', '气体', ' ...', '气体的', ' fluids', ' gaz', 'solid', ' газ', '液体', ' solids', ' Liquid', ' rắn', ' fluid', '液体的', '(g', ' газа', '液化', 'fluid', ' gaze', ' lique', '的气']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass erased0.5 plain27: ['固态', '气体', '气体的', '气', ' liquid', '液态', ' газо', ' газ', ' газа', '的气体', 'liquid', ' gaz', '_gas', ' liquids', ' گاز', ' غاز', '固体', ' الغاز', ' solid', '的气', ' твер', ' lỏng', ' fluids', 'solid', ' Liquid', ' gás', ' газов', '液体', ' rắn', 'غاز', ' gaze', 'fluid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' **', '**', 'liquid', ' liquid', ' Liquid', ' liquids', '液态', '…**', ' lique', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ' Answer', '固态', ':...', '**:', '�', ' frozen', '...', '液体', ' soluble', '：**', 'Answer', ' brittle', ' According', '____', '________']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', '常温', 'utow', '我来说', '英文名称', 'ائع', ' berüh', 'geries', ' lique', ' الاعتبار', 'anime', ' утвер', '加拿大的', 'vestig', '件事', 'irie', ' kwest', 'iration', 'liquid', '.freeze', ' liquids', ' Awake', ' physicists', '本题考查', 'free', '-free']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['固态', '气体', '气体的', '气', ' liquid', '液态', ' газо', ' газ', ' газа', '的气体', 'liquid', ' gaz', '_gas', ' liquids', ' گاز', ' غاز', '固体', ' الغاز', ' solid', '的气', ' твер', ' lỏng', ' fluids', 'solid', ' Liquid', ' gás', ' газов', '液体', ' rắn', 'غاز', ' gaze', 'fluid']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'gas<|im_end|>'

end-pass input-prefix J-lens: ['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ':...', '固态', '液体', ' Answer', ' **—', '-fluid', ' Liqu', '：**', ' frozen', ' Frozen', ' soluble', ' **:**', '液体的', ' líqu', '**:']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

J-lens: [' Facts', ' **', '**', ' Answer', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'facts', 'greater', ' facts', ' Based', ' Always', 'answered', ' Infinite', '：**', ' Depends', ' Greater', ' Fakt', ' Triangle', ';**', ' fakta', 'equal', ' answer', ' **+', '>**', ' Definitely', 'answer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

plain lens: ['.gradle', '的答案', '…**', 'ছিল', '本题考查', ' zahl', '当地的', '_fact', ' ...(', '事实', '参考答案', '<think>', 'euillez', '我来说', ' факты', 'église', '阿拉伯', ' indefinitely', '答案是', ' kebe', '陪', '的事实', '_depend', '...\\', '通过使用', ' beleg', '...(', ' Öffentlichkeit', ' Vergangenheit', ' Fakten', ' warta', '穌']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass J-lens: [' Facts', ' **', '**', ' Answer', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'facts', 'greater', ' facts', ' Based', ' Always', 'answered', ' Infinite', '：**', ' Depends', ' Greater', ' Fakt', ' Triangle', ';**', ' fakta', 'equal', ' answer', ' **+', '>**', ' Definitely', 'answer']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass logit contrast J-lens: [' **—', '自达', ' Assertions', ' .**', ' Skyl', ' Answers', ' **■', ' Singular', ' Downs', ' **>>', ' **:**', ' Nodes', ' Drops', 'ecam', ' Validates', 'udou', ' Defaults', ' Pregun', 'mener', ' Whites', ' Adds', ':Add', ' Seconds', ' Scr', ' **:', ' Autore', ' Pets', ' Masks', ' Vô', ' Gà', ' Inserts', ' –**']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass probability contrast J-lens: [' Facts', ' **', ' Answer', '**', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'facts', ' facts', ' Always', ' Based', 'greater', 'answered', '：**', ' Infinite', ' Depends', ' Greater', ' Fakt', ';**', ' Triangle', ' fakta', ' **+', ' answer', 'equal', '>**', ' Definitely', ' Fakta']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass plain24: ['.gradle', '的答案', '…**', 'ছিল', '本题考查', ' zahl', '当地的', '_fact', ' ...(', '事实', '参考答案', '<think>', 'euillez', '我来说', ' факты', 'église', '阿拉伯', ' indefinitely', '答案是', ' kebe', '陪', '的事实', '_depend', '...\\', '通过使用', ' beleg', '...(', ' Öffentlichkeit', ' Vergangenheit', ' Fakten', ' warta', '穌']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass logit contrast plain24: [' warta', ' Warsza', 'präg', ' Spra', 'èrement', ' Habitaciones', '.SO', ' amator', ' Peker', 'っちり', 'ประช', ' Raqqa', '-orders', ' pornos', 'gerà', 'acza', '乐乎', 'izare', 'براء', 'міна', 'idora', ' Tillerson', '刘畅', ' Хабар', ' Bade', ' Росси', ' 웹사이트가', ' competen', ' ที่ดีที่สุดใน', ' prostituer', ' filmer', 'いと']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass probability contrast plain24: ['.gradle', '的答案', 'ছিল', '…**', '本题考查', ' zahl', '当地的', '_fact', ' ...(', '事实', '参考答案', 'euillez', '我来说', 'église', ' факты', '阿拉伯', ' indefinitely', '答案是', ' kebe', '陪', ' beleg', '通过使用', '_depend', '...\\', '的事实', ' Öffentlichkeit', ' Vergangenheit', '...(', ' Fakten', ' warta', '穌', ' Wisata']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass plain27: [' triangles', 'greater', '<think>', ' greater', '…**', '本题考查', '_depend', '阿拉伯', ' thirds', '的答案', 'odd', '当地的', ' **:**', '_triangle', '.isFile', ' concurs', ' mitra', 'ilateral', '.gradle', 'åde', ' pales', 'always', ' trots', ' odd', '参考答案', '...**', '三角形', ' indefinitely', '三角形的', '_rectangle', '事实', 'euillez']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass logit contrast plain27: [' warta', ' amator', '!”.', ' vids', 'acza', ' concurr', '��', '乐乎', 'ربول', ' Habitaciones', 'präg', ' abbast', ' Publicidad', ' concurs', 'èrement', 'πτωση', ' pornos', 'ήμε', 'をストック', ' prostituer', ' Росси', ' Spra', ' denun', ' filmer', ' handphone', ' Insg', ' Tillerson', ' Direttore', 'idora', ' alasti', ' Warsza', ' Selatan']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass probability contrast plain27: [' triangles', ' greater', 'greater', '…**', '本题考查', '_depend', '阿拉伯', '<think>', ' thirds', '的答案', '当地的', ' **:**', '_triangle', '.isFile', ' concurs', ' mitra', 'ilateral', '.gradle', 'åde', ' pales', ' trots', 'odd', '参考答案', 'always', ' odd', '...**', ' indefinitely', '_rectangle', '三角形', '事实', 'euillez', '三角形的']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass negative final control: ['usche', '-deals', ' рассматри', '淑', 'alista', 'чья', '_dl', 'amana', '有啥', '-Ta', '在白', 'imana', 'azos', '渝', '��', ' Warsza', '云峰', ' nederlandse', '/Dk', ',DB', '.codes', '_SD', 'λάχ', '-prof', 'хта', '(IL', '宣读了', ' рассмат', '-messages', 'راض', ',msg', '新都']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased1 J-lens: [' **', '**', ' Facts', ' Answer', ' Answers', 'Answer', '答案', '的答案', '答案是', '事实', ' Based', ' facts', '：**', ' Always', ' answer', '...**', ' Infinite', ' Actually', 'facts', 'answered', ' Greater', '<|im_end|>', ' fakta', ' Fakt', ' Depends', ' factual', '的事实', ' According', '正确答案', 'Based', ' **+', ' Yes']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased0.5 J-lens: [' **', '**', ' Facts', ' Answer', ' Answers', '的答案', 'Answer', '答案是', '答案', '事实', ' Based', ' facts', '...**', ' Always', '：**', 'facts', ' Infinite', ' answer', 'answered', ' Greater', ' Depends', '…**', ' Fakt', ' fakta', 'greater', ' Triangle', '的事实', ' Actually', ' **+', ' factual', ';**', ' According']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased1 plain24: ['.gradle', '的答案', '本题考查', '事实', '_fact', '<think>', '参考答案', 'ছিল', ' zahl', '当地的', ' ...(', '…**', '陪', ' indefinitely', '的事实', '答案是', ' факты', '我来说', 'euillez', ' beleg', '偏方', '...\\', '_depend', ' Fakten', '...(', ' Vergangenheit', 'église', '在这种情况下', '.gener', '通过使用', ' Öffentlichkeit', ' …']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased0.5 plain24: ['.gradle', '的答案', '本题考查', 'ছিল', '事实', '_fact', '…**', ' zahl', '当地的', '<think>', '参考答案', ' ...(', '我来说', ' indefinitely', '陪', 'euillez', '答案是', ' факты', '的事实', ' beleg', 'église', '...\\', '_depend', '...(', ' Fakten', '通过使用', ' Vergangenheit', '偏方', '.gener', ' Öffentlichkeit', ' kebe', '阿拉伯']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased1 plain27: ['<think>', '本题考查', ' greater', ' triangles', '_depend', 'greater', '…**', '的答案', ' odd', '阿拉伯', '当地的', 'odd', '.gradle', 'ilateral', '事实', '参考答案', '.isFile', ' indefinitely', '三角形', '_triangle', ' mitra', ' concurs', '_rectangle', '...,', ' trots', 'åde', '三角形的', '...**', ' **:**', ' pales', '奇', '陪']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass erased0.5 plain27: ['<think>', ' triangles', ' greater', '本题考查', 'greater', '_depend', '…**', '阿拉伯', '的答案', 'odd', '当地的', 'ilateral', '.isFile', '.gradle', ' odd', '_triangle', '参考答案', ' thirds', '事实', ' mitra', ' **:**', ' concurs', ' indefinitely', 'åde', '三角形', ' trots', ' pales', '_rectangle', 'always', '...**', '三角形的', '...,']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass input-prefix erased0.5 J-lens: [' **', '**', ' Answer', ' Answers', '的答案', '答案是', 'Answer', '事实', '答案', ' Based', '...**', ' Always', '：**', ' Infinite', ' answer', 'answered', '…**', ' Greater', ' Depends', ' Fakt', ' fakta', 'greater', ' Triangle', ' Actually', ' **+', '的事实', ';**', ' According', ' Definitely', 'equal', '>**', '正确答案']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass input-prefix erased0.5 plain24: ['.gradle', '的答案', '本题考查', 'ছিল', '事实', '_fact', '…**', ' zahl', '当地的', '<think>', '参考答案', ' ...(', '我来说', ' indefinitely', '陪', 'euillez', '答案是', ' факты', '的事实', ' beleg', 'église', '...\\', '_depend', '...(', ' Fakten', '通过使用', ' Vergangenheit', '偏方', '.gener', ' Öffentlichkeit', ' kebe', '阿拉伯']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass input-prefix erased0.5 plain27: ['<think>', ' triangles', ' greater', '本题考查', 'greater', '_depend', '…**', '阿拉伯', '的答案', 'odd', '当地的', 'ilateral', '.isFile', '.gradle', ' odd', '_triangle', '参考答案', ' thirds', '事实', ' mitra', ' **:**', ' concurs', ' indefinitely', 'åde', '三角形', ' trots', ' pales', '_rectangle', 'always', '...**', '三角形的', '...,']

Input: '<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'

Baseline: 'three<|im_end|>'

end-pass input-prefix J-lens: [' **', ' Answer', '**', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'greater', ' Based', ' Always', 'answered', '：**', ' Infinite', ' Greater', ' Depends', ' Fakt', ' Triangle', ';**', ' fakta', 'equal', ' answer', ' **+', '>**', 'answer', ' Definitely', '的事实', ' Fakta', 'equals']


## Fixed-set readout results

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Actual-output lexical-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [J-lens](readout.json)     | 1/8                    |    0.451 | 1/6                      | 1/8                            |          0 |
| [plain lens](readout.json) | 0/8                    |    0.506 | 0/6                      | 0/8                            |          0 |

### End-of-pass readout (not for earlier edits)

| method                                                  | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:--------------------------------------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [end-pass probability contrast plain27](readout.json)   | 4/8                    |    0.698 | 2/6                      | 5/8                            |          0 |
| [end-pass erased0.5 J-lens](readout.json)               | 4/8                    |    0.907 | 2/6                      | 5/8                            |          0 |
| [end-pass erased1 plain27](readout.json)                | 4/8                    |    0.901 | 3/6                      | 4/8                            |          0 |
| [end-pass input-prefix erased0.5 J-lens](readout.json)  | 4/8                    |    0.907 | 2/6                      | 5/8                            |          0 |
| [end-pass input-prefix erased0.5 plain27](readout.json) | 4/8                    |    0.895 | 3/6                      | 4/8                            |          0 |
| [end-pass J-lens](readout.json)                         | 3/8                    |    0.895 | 2/6                      | 4/8                            |          0 |
| [end-pass probability contrast J-lens](readout.json)    | 3/8                    |    0.657 | 2/6                      | 4/8                            |          0 |
| [end-pass plain27](readout.json)                        | 3/8                    |    0.890 | 2/6                      | 4/8                            |          0 |
| [end-pass erased0.5 plain27](readout.json)              | 3/8                    |    0.895 | 3/6                      | 3/8                            |          0 |
| [end-pass input-prefix J-lens](readout.json)            | 3/8                    |    0.895 | 2/6                      | 4/8                            |          0 |
| [end-pass erased1 J-lens](readout.json)                 | 1/8                    |    0.925 | 0/6                      | 1/8                            |          0 |
| [end-pass logit contrast J-lens](readout.json)          | 0/8                    |    0.866 | 0/6                      | 0/8                            |          0 |
| [end-pass plain24](readout.json)                        | 0/8                    |    0.883 | 0/6                      | 0/8                            |          0 |
| [end-pass logit contrast plain24](readout.json)         | 0/8                    |    0.863 | 0/6                      | 0/8                            |          0 |
| [end-pass probability contrast plain24](readout.json)   | 0/8                    |    0.628 | 0/6                      | 0/8                            |          0 |
| [end-pass logit contrast plain27](readout.json)         | 0/8                    |    0.856 | 0/6                      | 0/8                            |          0 |
| [end-pass negative final control](readout.json)         | 0/8                    |    0.886 | 0/6                      | 0/8                            |          0 |
| [end-pass erased1 plain24](readout.json)                | 0/8                    |    0.892 | 0/6                      | 0/8                            |          0 |
| [end-pass erased0.5 plain24](readout.json)              | 0/8                    |    0.887 | 0/6                      | 0/8                            |          0 |
| [end-pass input-prefix erased0.5 plain24](readout.json) | 0/8                    |    0.887 | 0/6                      | 0/8                            |          0 |

run.md: /workspace/2026/suppressed-activations/out/2026-10-01_102255_jlens-one-pass/run.md
