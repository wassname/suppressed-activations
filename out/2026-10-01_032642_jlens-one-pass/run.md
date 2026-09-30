---
matching_pursuit: true
polar_readout: false
pool_question: false
verify_readout_run: None
token_kl: false
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
readout_block_index: 23
calibration_json: None
forecast_checkpoint: None
cases_json: .local/queued/english_v4_timed.json
translation_per_pair: 0
end_pass_readout: true
output_mask_max_n: 1
erase_output: true
erase_strength: 0.5
answer_alias_audit_json: None
k: 32
elapsed_seconds: 17.93
---
# Hidden-word readout comparison

Written by PI/OpenAI.

End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. Use script04's word mask with top_p=0.9, max_n=1 (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. Nonnegative matching pursuit decomposes raw residuals with unit effective-unembedding directions (J24 primary; plain24/plain27 controls), 32 positive greedy steps, repeated atoms and lowest-ID ties; no masks/labels during decomposition. Mask afterwards and retain positive coefficients only. Raw/unit-dot controls return the same per-representation cardinality, including zero; full32 and previous controls remain visible. Early/pre-clue diagnostics use only their consumed prefix and own-position greedy output masks; raw active atoms are also saved to detect masking artifacts. Normalized coefficients divide by the original state norm, not probabilities. Erasure/contrast results are separate controls, never inputs to pursuit. TODO validate: pursuit improves paired joint recovery and reveals a new clue-associated concept, not merely a shorter generic list. Logit contrast subtracts separately final-normalised vocabulary logits, retaining signed scores; probability contrast retains positive probability differences. Negative-final and cyclic mismatched-final scores are diagnostic controls. No generated text or labels enter these rankings. Posthoc rescoring of out/2026-09-30_185058_jlens-one-pass; no transformer forwards or new generations. See replay_source.json for hashes and mismatch ordering. Same layer, k32 and prompt mask as before; position rule is specified above (otherwise final only). Dataset's original selection history: Eight new English prompts fixed before inference, after the blinded v3 audit localized all seven J joint passes to geography. Test the unchanged primary J residual24/final-position/k32/prompt+greedy masks/output erasure0.5 on non-geography relations before modifying masking. Same prefix, generation cap and controls. These hidden labels are absent from English v1/v2/v3 targets, not necessarily from earlier translation prompts. Labels are hypothesized intermediates, not proof of use. All cases and wrong/unscorable answers remain. Common aliases are predeclared but incomplete; semantic input/output review remains separate from lexical scoring. No output-based replacement or filtering. When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Fresh runs generate with an eight-token cap; replay runs reuse the cached continuations without generation. Scoring definitions are unchanged. Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC and remain in the full denominator. These are lexical passes, not a verified lower bound on semantic success. Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.

SHOULD: end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.

Calibration: not used

| concept   | method                                     | actual pass   |   token-pair AUROC |   hidden rank |   intended answer rank | literal pass   | alias pass   |
|:----------|:-------------------------------------------|:--------------|-------------------:|--------------:|-----------------------:|:---------------|:-------------|
| December  | J-lens                                     | False         |           0.725926 |             2 |                      0 | False          | False        |
| December  | plain lens                                 | False         |           0.542593 |         35042 |                   2477 | False          | False        |
| December  | end-pass J-lens                            | True          |           0.866667 |             1 |             1000000000 | True           | True         |
| December  | end-pass logit contrast J-lens             | False         |           0.625926 |         23380 |             1000000000 | False          | False        |
| December  | end-pass probability contrast J-lens       | True          |           0.624074 |            21 |             1000000000 | True           | True         |
| December  | end-pass mismatched logit contrast J-lens  | False         |           0.857407 |            72 |             1000000000 | False          | False        |
| December  | end-pass plain24                           | False         |           0.701852 |         35037 |             1000000000 | False          | False        |
| December  | end-pass logit contrast plain24            | False         |           0.52963  |        233244 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain24      | False         |           0.444444 |        170144 |             1000000000 | False          | False        |
| December  | end-pass mismatched logit contrast plain24 | False         |           0.657407 |        167793 |             1000000000 | False          | False        |
| December  | end-pass plain27                           | True          |           0.992593 |             2 |             1000000000 | True           | True         |
| December  | end-pass logit contrast plain27            | False         |           0.709259 |          7773 |             1000000000 | False          | False        |
| December  | end-pass probability contrast plain27      | True          |           0.919444 |             9 |             1000000000 | True           | True         |
| December  | end-pass mismatched logit contrast plain27 | False         |           0.951852 |           137 |             1000000000 | False          | False        |
| December  | end-pass pursuit J24                       | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| December  | end-pass raw-dot matched J24               | True          |           0.866667 |             1 |             1000000000 | True           | True         |
| December  | end-pass unit-dot matched J24              | True          |           0.868519 |             1 |             1000000000 | True           | True         |
| December  | end-pass raw-dot full32 J24                | True          |           0.866667 |             1 |             1000000000 | True           | True         |
| December  | end-pass unit-dot full32 J24               | True          |           0.868519 |             1 |             1000000000 | True           | True         |
| December  | end-pass pursuit plain24                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| December  | end-pass raw-dot matched plain24           | False         |           0.701852 |         35477 |             1000000000 | False          | False        |
| December  | end-pass unit-dot matched plain24          | False         |           0.707407 |         16702 |             1000000000 | False          | False        |
| December  | end-pass raw-dot full32 plain24            | False         |           0.701852 |         35477 |             1000000000 | False          | False        |
| December  | end-pass unit-dot full32 plain24           | False         |           0.707407 |         16702 |             1000000000 | False          | False        |
| December  | end-pass pursuit plain27                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| December  | end-pass raw-dot matched plain27           | True          |           0.992593 |             2 |             1000000000 | True           | True         |
| December  | end-pass unit-dot matched plain27          | True          |           0.988889 |             0 |             1000000000 | True           | True         |
| December  | end-pass raw-dot full32 plain27            | True          |           0.992593 |             2 |             1000000000 | True           | True         |
| December  | end-pass unit-dot full32 plain27           | True          |           0.988889 |             0 |             1000000000 | True           | True         |
| December  | end-pass negative final control            | False         |           0.518519 |        227760 |             1000000000 | False          | False        |
| December  | end-pass erased1 J-lens                    | False         |           0.818519 |          7988 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 J-lens                  | False         |           0.853704 |            71 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain24                   | False         |           0.635185 |        163572 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain24                 | False         |           0.662963 |        102410 |             1000000000 | False          | False        |
| December  | end-pass erased1 plain27                   | False         |           0.985185 |            34 |             1000000000 | False          | False        |
| December  | end-pass erased0.5 plain27                 | True          |           0.994444 |            23 |             1000000000 | True           | True         |
| Thursday  | J-lens                                     | False         |           0.85098  |             1 |                      3 | False          | False        |
| Thursday  | plain lens                                 | False         |           0.882353 |           478 |                  10923 | False          | False        |
| Thursday  | end-pass J-lens                            | True          |           0.94902  |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass logit contrast J-lens             | False         |           0.719608 |          3137 |             1000000000 | False          | False        |
| Thursday  | end-pass probability contrast J-lens       | True          |           0.545098 |            15 |             1000000000 | True           | True         |
| Thursday  | end-pass mismatched logit contrast J-lens  | True          |           0.952941 |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass plain24                           | False         |           0.909804 |           478 |             1000000000 | False          | False        |
| Thursday  | end-pass logit contrast plain24            | False         |           0.598039 |        122480 |             1000000000 | False          | False        |
| Thursday  | end-pass probability contrast plain24      | False         |           0.595098 |          2126 |             1000000000 | False          | False        |
| Thursday  | end-pass mismatched logit contrast plain24 | False         |           0.860784 |         33125 |             1000000000 | False          | False        |
| Thursday  | end-pass plain27                           | True          |           0.964706 |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass logit contrast plain27            | False         |           0.688235 |         40239 |             1000000000 | False          | False        |
| Thursday  | end-pass probability contrast plain27      | True          |           0.896078 |             3 |             1000000000 | True           | True         |
| Thursday  | end-pass mismatched logit contrast plain27 | True          |           0.976471 |            17 |             1000000000 | True           | True         |
| Thursday  | end-pass pursuit J24                       | True          |           0.55     |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass raw-dot matched J24               | True          |           0.94902  |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass unit-dot matched J24              | True          |           0.956863 |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass raw-dot full32 J24                | True          |           0.94902  |             1 |             1000000000 | True           | True         |
| Thursday  | end-pass unit-dot full32 J24               | True          |           0.956863 |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass pursuit plain24                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| Thursday  | end-pass raw-dot matched plain24           | False         |           0.909804 |           479 |             1000000000 | False          | False        |
| Thursday  | end-pass unit-dot matched plain24          | False         |           0.9      |           287 |             1000000000 | False          | False        |
| Thursday  | end-pass raw-dot full32 plain24            | False         |           0.909804 |           479 |             1000000000 | False          | False        |
| Thursday  | end-pass unit-dot full32 plain24           | False         |           0.9      |           287 |             1000000000 | False          | False        |
| Thursday  | end-pass pursuit plain27                   | True          |           0.55     |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass raw-dot matched plain27           | True          |           0.964706 |             2 |             1000000000 | True           | True         |
| Thursday  | end-pass unit-dot matched plain27          | True          |           0.94902  |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass raw-dot full32 plain27            | True          |           0.964706 |             2 |             1000000000 | True           | True         |
| Thursday  | end-pass unit-dot full32 plain27           | True          |           0.94902  |             0 |             1000000000 | True           | True         |
| Thursday  | end-pass negative final control            | False         |           0.511765 |        223224 |             1000000000 | False          | False        |
| Thursday  | end-pass erased1 J-lens                    | False         |           0.862745 |           151 |             1000000000 | False          | False        |
| Thursday  | end-pass erased0.5 J-lens                  | True          |           0.92549  |             3 |             1000000000 | True           | True         |
| Thursday  | end-pass erased1 plain24                   | False         |           0.896078 |           718 |             1000000000 | False          | False        |
| Thursday  | end-pass erased0.5 plain24                 | False         |           0.907843 |           577 |             1000000000 | False          | False        |
| Thursday  | end-pass erased1 plain27                   | True          |           0.939216 |             9 |             1000000000 | True           | True         |
| Thursday  | end-pass erased0.5 plain27                 | True          |           0.95098  |             7 |             1000000000 | True           | True         |
| autumn    | J-lens                                     | False         |           0.656471 |             6 |                      0 | False          | False        |
| autumn    | plain lens                                 | False         |           0.685882 |           154 |                      5 | False          | False        |
| autumn    | end-pass J-lens                            | True          |           0.934118 |             2 |             1000000000 | True           | False        |
| autumn    | end-pass logit contrast J-lens             | False         |           0.842353 |        233630 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast J-lens       | False         |           0.508235 |    1000000000 |             1000000000 | False          | False        |
| autumn    | end-pass mismatched logit contrast J-lens  | False         |           0.971765 |           405 |             1000000000 | False          | False        |
| autumn    | end-pass plain24                           | False         |           0.901176 |           153 |             1000000000 | False          | False        |
| autumn    | end-pass logit contrast plain24            | False         |           0.795294 |        227216 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain24      | False         |           0.602353 |          8452 |             1000000000 | False          | False        |
| autumn    | end-pass mismatched logit contrast plain24 | False         |           0.905882 |         18303 |             1000000000 | False          | False        |
| autumn    | end-pass plain27                           | True          |           0.985882 |             9 |             1000000000 | True           | True         |
| autumn    | end-pass logit contrast plain27            | False         |           0.868235 |        209988 |             1000000000 | False          | False        |
| autumn    | end-pass probability contrast plain27      | True          |           0.755294 |           107 |             1000000000 | False          | True         |
| autumn    | end-pass mismatched logit contrast plain27 | False         |           0.978823 |           273 |             1000000000 | False          | False        |
| autumn    | end-pass pursuit J24                       | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| autumn    | end-pass raw-dot matched J24               | True          |           0.934118 |             2 |             1000000000 | True           | False        |
| autumn    | end-pass unit-dot matched J24              | True          |           0.936471 |             0 |             1000000000 | True           | False        |
| autumn    | end-pass raw-dot full32 J24                | True          |           0.934118 |             2 |             1000000000 | True           | False        |
| autumn    | end-pass unit-dot full32 J24               | True          |           0.936471 |             0 |             1000000000 | True           | False        |
| autumn    | end-pass pursuit plain24                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| autumn    | end-pass raw-dot matched plain24           | False         |           0.901176 |           158 |             1000000000 | False          | False        |
| autumn    | end-pass unit-dot matched plain24          | True          |           0.898823 |            23 |             1000000000 | True           | True         |
| autumn    | end-pass raw-dot full32 plain24            | False         |           0.901176 |           158 |             1000000000 | False          | False        |
| autumn    | end-pass unit-dot full32 plain24           | True          |           0.898823 |            23 |             1000000000 | True           | True         |
| autumn    | end-pass pursuit plain27                   | True          |           0.529412 |            29 |             1000000000 | True           | True         |
| autumn    | end-pass raw-dot matched plain27           | True          |           0.985882 |             9 |             1000000000 | True           | True         |
| autumn    | end-pass unit-dot matched plain27          | True          |           0.983529 |             5 |             1000000000 | True           | True         |
| autumn    | end-pass raw-dot full32 plain27            | True          |           0.985882 |             9 |             1000000000 | True           | True         |
| autumn    | end-pass unit-dot full32 plain27           | True          |           0.983529 |             5 |             1000000000 | True           | True         |
| autumn    | end-pass negative final control            | False         |           0.787059 |        245988 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 J-lens                    | False         |           0.924706 |           437 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 J-lens                  | False         |           0.934118 |            50 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain24                   | False         |           0.882353 |          6427 |             1000000000 | False          | False        |
| autumn    | end-pass erased0.5 plain24                 | False         |           0.890588 |          1127 |             1000000000 | False          | False        |
| autumn    | end-pass erased1 plain27                   | True          |           0.985882 |            66 |             1000000000 | False          | True         |
| autumn    | end-pass erased0.5 plain27                 | True          |           0.985882 |            23 |             1000000000 | True           | True         |
| apple     | J-lens                                     | False         |           0.6125   |            25 |                      0 | False          | False        |
| apple     | plain lens                                 | False         |           0.711111 |          1374 |                     86 | False          | False        |
| apple     | end-pass J-lens                            | True          |           0.894444 |            23 |             1000000000 | True           | False        |
| apple     | end-pass logit contrast J-lens             | False         |           0.866667 |         12871 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast J-lens       | False         |           0.679167 |            41 |             1000000000 | False          | False        |
| apple     | end-pass mismatched logit contrast J-lens  | False         |           0.941667 |            58 |             1000000000 | False          | False        |
| apple     | end-pass plain24                           | False         |           0.983333 |          1367 |             1000000000 | False          | False        |
| apple     | end-pass logit contrast plain24            | False         |           0.890278 |        157468 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain24      | False         |           0.766667 |          1421 |             1000000000 | False          | False        |
| apple     | end-pass mismatched logit contrast plain24 | False         |           0.963889 |         11494 |             1000000000 | False          | False        |
| apple     | end-pass plain27                           | True          |           1        |            27 |             1000000000 | True           | False        |
| apple     | end-pass logit contrast plain27            | False         |           0.936111 |         76285 |             1000000000 | False          | False        |
| apple     | end-pass probability contrast plain27      | True          |           0.847222 |            27 |             1000000000 | True           | False        |
| apple     | end-pass mismatched logit contrast plain27 | False         |           0.991667 |           125 |             1000000000 | False          | False        |
| apple     | end-pass pursuit J24                       | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| apple     | end-pass raw-dot matched J24               | True          |           0.894444 |            23 |             1000000000 | True           | False        |
| apple     | end-pass unit-dot matched J24              | False         |           0.894444 |            32 |             1000000000 | False          | False        |
| apple     | end-pass raw-dot full32 J24                | True          |           0.894444 |            23 |             1000000000 | True           | False        |
| apple     | end-pass unit-dot full32 J24               | False         |           0.894444 |            32 |             1000000000 | False          | False        |
| apple     | end-pass pursuit plain24                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| apple     | end-pass raw-dot matched plain24           | False         |           0.983333 |          1404 |             1000000000 | False          | False        |
| apple     | end-pass unit-dot matched plain24          | False         |           0.983333 |           662 |             1000000000 | False          | False        |
| apple     | end-pass raw-dot full32 plain24            | False         |           0.983333 |          1404 |             1000000000 | False          | False        |
| apple     | end-pass unit-dot full32 plain24           | False         |           0.983333 |           662 |             1000000000 | False          | False        |
| apple     | end-pass pursuit plain27                   | True          |           0.527778 |             1 |             1000000000 | True           | False        |
| apple     | end-pass raw-dot matched plain27           | True          |           1        |            27 |             1000000000 | True           | False        |
| apple     | end-pass unit-dot matched plain27          | True          |           1        |            12 |             1000000000 | True           | False        |
| apple     | end-pass raw-dot full32 plain27            | True          |           1        |            27 |             1000000000 | True           | False        |
| apple     | end-pass unit-dot full32 plain27           | True          |           1        |            12 |             1000000000 | True           | False        |
| apple     | end-pass negative final control            | False         |           0.761111 |        203800 |             1000000000 | False          | False        |
| apple     | end-pass erased1 J-lens                    | True          |           0.891667 |             9 |             1000000000 | True           | True         |
| apple     | end-pass erased0.5 J-lens                  | True          |           0.9      |            11 |             1000000000 | True           | False        |
| apple     | end-pass erased1 plain24                   | False         |           0.972222 |          1898 |             1000000000 | False          | False        |
| apple     | end-pass erased0.5 plain24                 | False         |           0.977778 |          1646 |             1000000000 | False          | False        |
| apple     | end-pass erased1 plain27                   | True          |           1        |             8 |             1000000000 | True           | True         |
| apple     | end-pass erased0.5 plain27                 | True          |           1        |             7 |             1000000000 | True           | True         |
| violin    | J-lens                                     | True          |           0.854396 |             0 |                   3354 | True           | True         |
| violin    | plain lens                                 | False         |           0.892857 |           304 |                    951 | False          | False        |
| violin    | end-pass J-lens                            | True          |           0.854396 |             0 |                   3352 | True           | True         |
| violin    | end-pass logit contrast J-lens             | False         |           0.475275 |        224846 |                 159694 | False          | False        |
| violin    | end-pass probability contrast J-lens       | True          |           0.398352 |             1 |                  40212 | True           | True         |
| violin    | end-pass mismatched logit contrast J-lens  | False         |           0.917582 |            92 |                  16557 | False          | False        |
| violin    | end-pass plain24                           | False         |           0.892857 |           302 |                    949 | False          | False        |
| violin    | end-pass logit contrast plain24            | False         |           0.53022  |        211349 |                 196077 | False          | False        |
| violin    | end-pass probability contrast plain24      | False         |           0.543956 |           887 |                    967 | False          | False        |
| violin    | end-pass mismatched logit contrast plain24 | False         |           0.89011  |          1620 |                   4454 | False          | False        |
| violin    | end-pass plain27                           | True          |           0.972528 |             2 |                     12 | False          | False        |
| violin    | end-pass logit contrast plain27            | False         |           0.741758 |         15219 |                  48796 | False          | False        |
| violin    | end-pass probability contrast plain27      | True          |           0.89011  |             3 |                     11 | False          | False        |
| violin    | end-pass mismatched logit contrast plain27 | True          |           0.972528 |             2 |                     57 | True           | True         |
| violin    | end-pass pursuit J24                       | True          |           0.571429 |             0 |             1000000000 | True           | True         |
| violin    | end-pass raw-dot matched J24               | True          |           0.854396 |             0 |                   3401 | True           | True         |
| violin    | end-pass unit-dot matched J24              | True          |           0.85989  |             0 |                   3908 | True           | True         |
| violin    | end-pass raw-dot full32 J24                | True          |           0.854396 |             0 |                   3401 | True           | True         |
| violin    | end-pass unit-dot full32 J24               | True          |           0.85989  |             0 |                   3908 | True           | True         |
| violin    | end-pass pursuit plain24                   | False         |           0.490385 |    1000000000 |             1000000000 | False          | False        |
| violin    | end-pass raw-dot matched plain24           | False         |           0.892857 |           316 |                    957 | False          | False        |
| violin    | end-pass unit-dot matched plain24          | True          |           0.873626 |            11 |                    761 | True           | True         |
| violin    | end-pass raw-dot full32 plain24            | False         |           0.892857 |           316 |                    957 | False          | False        |
| violin    | end-pass unit-dot full32 plain24           | True          |           0.873626 |            11 |                    761 | True           | True         |
| violin    | end-pass pursuit plain27                   | False         |           0.563187 |             0 |                     12 | False          | False        |
| violin    | end-pass raw-dot matched plain27           | True          |           0.972528 |             2 |                     12 | False          | False        |
| violin    | end-pass unit-dot matched plain27          | True          |           0.96978  |             0 |                     31 | True           | True         |
| violin    | end-pass raw-dot full32 plain27            | True          |           0.972528 |             2 |                     12 | False          | False        |
| violin    | end-pass unit-dot full32 plain27           | True          |           0.96978  |             0 |                     31 | False          | False        |
| violin    | end-pass negative final control            | False         |           0.472527 |        228370 |                 203816 | False          | False        |
| violin    | end-pass erased1 J-lens                    | True          |           0.876374 |             1 |                   3314 | True           | True         |
| violin    | end-pass erased0.5 J-lens                  | True          |           0.865385 |             0 |                   3184 | True           | True         |
| violin    | end-pass erased1 plain24                   | False         |           0.899725 |           646 |                   1033 | False          | False        |
| violin    | end-pass erased0.5 plain24                 | False         |           0.901099 |           450 |                    963 | False          | False        |
| violin    | end-pass erased1 plain27                   | True          |           0.975275 |             2 |                     10 | False          | False        |
| violin    | end-pass erased0.5 plain27                 | True          |           0.972528 |             1 |                     11 | False          | False        |
| Hamlet    | J-lens                                     | False         |           0.842424 |            98 |                      0 | False          | False        |
| Hamlet    | plain lens                                 | False         |           0.712121 |          2291 |                      2 | False          | False        |
| Hamlet    | end-pass J-lens                            | False         |           0.912121 |            96 |                      0 | False          | False        |
| Hamlet    | end-pass logit contrast J-lens             | False         |           0.639394 |         84294 |                  26292 | False          | False        |
| Hamlet    | end-pass probability contrast J-lens       | False         |           0.654545 |           772 |                      0 | False          | False        |
| Hamlet    | end-pass mismatched logit contrast J-lens  | False         |           0.860606 |           483 |                      1 | False          | False        |
| Hamlet    | end-pass plain24                           | False         |           0.751515 |          2291 |                      2 | False          | False        |
| Hamlet    | end-pass logit contrast plain24            | False         |           0.539394 |        135196 |                  33134 | False          | False        |
| Hamlet    | end-pass probability contrast plain24      | False         |           0.630303 |          2362 |                     50 | False          | False        |
| Hamlet    | end-pass mismatched logit contrast plain24 | False         |           0.730303 |          6063 |                    127 | False          | False        |
| Hamlet    | end-pass plain27                           | False         |           0.818182 |           179 |                      2 | False          | False        |
| Hamlet    | end-pass logit contrast plain27            | False         |           0.581818 |         57224 |                  33095 | False          | False        |
| Hamlet    | end-pass probability contrast plain27      | False         |           0.669697 |           186 |                      2 | False          | False        |
| Hamlet    | end-pass mismatched logit contrast plain27 | False         |           0.769697 |          1236 |                      1 | False          | False        |
| Hamlet    | end-pass pursuit J24                       | False         |           0.490909 |    1000000000 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot matched J24               | False         |           0.912121 |            99 |                      0 | False          | False        |
| Hamlet    | end-pass unit-dot matched J24              | False         |           0.909091 |           150 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot full32 J24                | False         |           0.912121 |            99 |                      0 | False          | False        |
| Hamlet    | end-pass unit-dot full32 J24               | False         |           0.909091 |           150 |                      0 | False          | False        |
| Hamlet    | end-pass pursuit plain24                   | False         |           0.490909 |    1000000000 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot matched plain24           | False         |           0.748485 |          2349 |                      2 | False          | False        |
| Hamlet    | end-pass unit-dot matched plain24          | False         |           0.748485 |          1106 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot full32 plain24            | False         |           0.748485 |          2349 |                      2 | False          | False        |
| Hamlet    | end-pass unit-dot full32 plain24           | False         |           0.748485 |          1106 |                      0 | False          | False        |
| Hamlet    | end-pass pursuit plain27                   | False         |           0.481818 |    1000000000 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot matched plain27           | False         |           0.818182 |           185 |                      2 | False          | False        |
| Hamlet    | end-pass unit-dot matched plain27          | False         |           0.812121 |            89 |                      0 | False          | False        |
| Hamlet    | end-pass raw-dot full32 plain27            | False         |           0.818182 |           185 |                      2 | False          | False        |
| Hamlet    | end-pass unit-dot full32 plain27           | False         |           0.812121 |            89 |                      0 | False          | False        |
| Hamlet    | end-pass negative final control            | False         |           0.472727 |        238368 |                 191288 | False          | False        |
| Hamlet    | end-pass erased1 J-lens                    | False         |           0.878788 |           330 |                      0 | False          | False        |
| Hamlet    | end-pass erased0.5 J-lens                  | False         |           0.884848 |           155 |                      0 | False          | False        |
| Hamlet    | end-pass erased1 plain24                   | False         |           0.739394 |          2479 |                      3 | False          | False        |
| Hamlet    | end-pass erased0.5 plain24                 | False         |           0.743939 |          2345 |                      3 | False          | False        |
| Hamlet    | end-pass erased1 plain27                   | False         |           0.80303  |           361 |                      2 | False          | False        |
| Hamlet    | end-pass erased0.5 plain27                 | False         |           0.812121 |           257 |                      2 | False          | False        |
| hydrogen  | J-lens                                     | False         |           0.647059 |           129 |                     17 | False          | False        |
| hydrogen  | plain lens                                 | False         |           0.372549 |         30834 |                   2056 | False          | False        |
| hydrogen  | end-pass J-lens                            | False         |           0.69281  |           129 |                     17 | False          | False        |
| hydrogen  | end-pass logit contrast J-lens             | False         |           0.738562 |         15528 |                 179419 | False          | False        |
| hydrogen  | end-pass probability contrast J-lens       | False         |           0.69281  |           496 |                     29 | False          | False        |
| hydrogen  | end-pass mismatched logit contrast J-lens  | False         |           0.718954 |           159 |                      6 | False          | False        |
| hydrogen  | end-pass plain24                           | False         |           0.601307 |         30831 |                   2055 | False          | False        |
| hydrogen  | end-pass logit contrast plain24            | False         |           0.656863 |        205895 |                 241915 | False          | False        |
| hydrogen  | end-pass probability contrast plain24      | False         |           0.503268 |         31261 |                  15659 | False          | False        |
| hydrogen  | end-pass mismatched logit contrast plain24 | False         |           0.686275 |         23821 |                   3563 | False          | False        |
| hydrogen  | end-pass plain27                           | False         |           0.620915 |          2126 |                      0 | False          | False        |
| hydrogen  | end-pass logit contrast plain27            | False         |           0.490196 |        192024 |                    264 | False          | False        |
| hydrogen  | end-pass probability contrast plain27      | False         |           0.408497 |        127679 |                      0 | False          | False        |
| hydrogen  | end-pass mismatched logit contrast plain27 | False         |           0.669935 |         17432 |                      1 | False          | False        |
| hydrogen  | end-pass pursuit J24                       | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| hydrogen  | end-pass raw-dot matched J24               | False         |           0.69281  |           135 |                     17 | False          | False        |
| hydrogen  | end-pass unit-dot matched J24              | False         |           0.712418 |            66 |                     23 | False          | False        |
| hydrogen  | end-pass raw-dot full32 J24                | False         |           0.69281  |           135 |                     17 | False          | False        |
| hydrogen  | end-pass unit-dot full32 J24               | False         |           0.712418 |            66 |                     23 | False          | False        |
| hydrogen  | end-pass pursuit plain24                   | False         |           0.5      |    1000000000 |             1000000000 | False          | False        |
| hydrogen  | end-pass raw-dot matched plain24           | False         |           0.601307 |         31032 |                   2130 | False          | False        |
| hydrogen  | end-pass unit-dot matched plain24          | False         |           0.601307 |         28122 |                   3395 | False          | False        |
| hydrogen  | end-pass raw-dot full32 plain24            | False         |           0.601307 |         31032 |                   2130 | False          | False        |
| hydrogen  | end-pass unit-dot full32 plain24           | False         |           0.601307 |         28122 |                   3395 | False          | False        |
| hydrogen  | end-pass pursuit plain27                   | False         |           0.470588 |    1000000000 |                      0 | False          | False        |
| hydrogen  | end-pass raw-dot matched plain27           | False         |           0.620915 |          2143 |                      0 | False          | False        |
| hydrogen  | end-pass unit-dot matched plain27          | False         |           0.627451 |           843 |                      0 | False          | False        |
| hydrogen  | end-pass raw-dot full32 plain27            | False         |           0.620915 |          2143 |                      0 | False          | False        |
| hydrogen  | end-pass unit-dot full32 plain27           | False         |           0.627451 |           843 |                      0 | False          | False        |
| hydrogen  | end-pass negative final control            | False         |           0.705882 |        194213 |                 247614 | False          | False        |
| hydrogen  | end-pass erased1 J-lens                    | False         |           0.705882 |           220 |                     28 | False          | False        |
| hydrogen  | end-pass erased0.5 J-lens                  | False         |           0.705882 |           169 |                     22 | False          | False        |
| hydrogen  | end-pass erased1 plain24                   | False         |           0.601307 |         34827 |                   2672 | False          | False        |
| hydrogen  | end-pass erased0.5 plain24                 | False         |           0.601307 |         32356 |                   2330 | False          | False        |
| hydrogen  | end-pass erased1 plain27                   | False         |           0.633987 |          4697 |                      0 | False          | False        |
| hydrogen  | end-pass erased0.5 plain27                 | False         |           0.627451 |          3037 |                      0 | False          | False        |
| triangle  | J-lens                                     | True          |           0.990476 |             6 |                    386 | True           | True         |
| triangle  | plain lens                                 | True          |           1        |           103 |                  91628 | False          | True         |
| triangle  | end-pass J-lens                            | True          |           0.990476 |             6 |                    386 | True           | True         |
| triangle  | end-pass logit contrast J-lens             | False         |           0.99619  |          3704 |                 243514 | False          | False        |
| triangle  | end-pass probability contrast J-lens       | True          |           0.958095 |             5 |                    513 | True           | True         |
| triangle  | end-pass mismatched logit contrast J-lens  | True          |           0.994286 |             1 |                    367 | True           | True         |
| triangle  | end-pass plain24                           | True          |           1        |           103 |                  91628 | False          | True         |
| triangle  | end-pass logit contrast plain24            | False         |           0.998095 |        121689 |                 247823 | False          | False        |
| triangle  | end-pass probability contrast plain24      | True          |           0.9      |           100 |             1000000000 | False          | True         |
| triangle  | end-pass mismatched logit contrast plain24 | True          |           0.99619  |            14 |                 117217 | True           | True         |
| triangle  | end-pass plain27                           | True          |           1        |             7 |                   3462 | True           | True         |
| triangle  | end-pass logit contrast plain27            | False         |           1        |         35340 |                 246936 | False          | False        |
| triangle  | end-pass probability contrast plain27      | True          |           0.966667 |             7 |             1000000000 | True           | True         |
| triangle  | end-pass mismatched logit contrast plain27 | True          |           0.998095 |             1 |                  14019 | True           | False        |
| triangle  | end-pass pursuit J24                       | True          |           0.533333 |             1 |             1000000000 | True           | True         |
| triangle  | end-pass raw-dot matched J24               | True          |           0.990476 |             6 |                    410 | True           | True         |
| triangle  | end-pass unit-dot matched J24              | True          |           1        |             1 |                   3814 | True           | True         |
| triangle  | end-pass raw-dot full32 J24                | True          |           0.990476 |             6 |                    410 | True           | True         |
| triangle  | end-pass unit-dot full32 J24               | True          |           1        |             1 |                   3814 | True           | True         |
| triangle  | end-pass pursuit plain24                   | False         |           0.485714 |    1000000000 |                     20 | False          | False        |
| triangle  | end-pass raw-dot matched plain24           | True          |           1        |           106 |                  91835 | False          | True         |
| triangle  | end-pass unit-dot matched plain24          | True          |           1        |            77 |                  98860 | False          | True         |
| triangle  | end-pass raw-dot full32 plain24            | True          |           1        |           106 |                  91835 | False          | True         |
| triangle  | end-pass unit-dot full32 plain24           | True          |           1        |            77 |                  98860 | False          | True         |
| triangle  | end-pass pursuit plain27                   | False         |           0.52     |    1000000000 |                     21 | False          | False        |
| triangle  | end-pass raw-dot matched plain27           | True          |           1        |             7 |                   3460 | True           | True         |
| triangle  | end-pass unit-dot matched plain27          | True          |           1        |             6 |                   6650 | True           | True         |
| triangle  | end-pass raw-dot full32 plain27            | True          |           1        |             7 |                   3460 | True           | True         |
| triangle  | end-pass unit-dot full32 plain27           | True          |           1        |             6 |                   6650 | True           | True         |
| triangle  | end-pass negative final control            | False         |           0.992381 |        240126 |                 247978 | False          | False        |
| triangle  | end-pass erased1 J-lens                    | True          |           0.998095 |             6 |                   3417 | True           | True         |
| triangle  | end-pass erased0.5 J-lens                  | True          |           0.994286 |             6 |                   1117 | True           | True         |
| triangle  | end-pass erased1 plain24                   | True          |           1        |            84 |                  38531 | False          | True         |
| triangle  | end-pass erased0.5 plain24                 | True          |           1        |            94 |                  61992 | False          | True         |
| triangle  | end-pass erased1 plain27                   | True          |           1        |             7 |                  12523 | True           | True         |
| triangle  | end-pass erased0.5 plain27                 | True          |           1        |             7 |                   6599 | True           | True         |

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

end-pass logit contrast J-lens: ['months', 'Months', '月份', ' Months', '一个月的', '月份的', 'Monthly', '_months', 'weeks', 'Calendar', 'Season', '-month', ' meses', '一个月', 'Moon', 'Spring', '第二年', 'calendar', 'tembre', ' hónap', ' printemps', ' bulan', '月的', ' месяца', '两个月', 'Portal', '几个月', ' calendrier', 'moon', '.Month', '月初', '数月']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass probability contrast J-lens: [' Months', ' months', '月份', ' February', 'Months', 'months', ' Year', ' November', '-month', ' Januari', '月份的', ' Calendar', '次年', ' October', ' Monthly', ' April', ' calendar', ' September', 'calendar', 'February', ' Ramadan', 'December', ' winter', '_month', ' Spring', ' Winter', '(month', ' Easter', ' bulan', '/month', ' year', '.month']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass mismatched logit contrast J-lens: ['月份', 'months', 'Months', ' Months', 'Year', '次年', '-month', 'year', '月份的', '两个月', '第二年', ' months', ' bulan', '_months', '一个月的', '一个月', '几个月', ' meses', '来年', '明年', '第一年', '一年', '_month', '十二月', '_year', '一年的', 'mois', ' Year', 'Monthly', '数月', '月的', '明年的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass plain24: [' called', '眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', '志愿服务队', ' наступ', ' kolej', ' называется', '問わず', 'ถัด', '人も多い', 'FOUND', 'orate', 'called', ' Fucking', '{name', 'ullo', ' kalt', '新社', '下一章', ' ули', '球迷们', 'CALE', 'Called', '.getMonth', ' appelé', '谤', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass logit contrast plain24: ['最专业的', 'ỏa', ' экспо', ' للمر', '挖掘公司', ' amator', 'してもらえる', 'SIG', ' указы', ' Industr', ' Condizioni', ' compac', '伙伴们', '录得', '教体', 'Tail', '志愿服务队', 'ullo', 'iglio', 'iền', 'TAIL', '帕特', '创投', 'FIL', 'ẹo', ' pilo', '頂けます', 'COPE', '空空', 'رداد', '罗那', 'orough']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass probability contrast plain24: ['眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', '志愿服务队', ' kolej', ' наступ', '問わず', 'ถัด', ' называется', '人も多い', 'FOUND', 'orate', 'called', ' Fucking', '{name', 'ullo', ' ули', '下一章', ' kalt', '新社', '球迷们', 'CALE', '.getMonth', 'Called', ' appelé', 'ỏa', '谤', 'örden']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass mismatched logit contrast plain24: ['下一章', 'GLOSS', 'GORITH', 'orough', 'пові', 'ovem', ' Acerca', 'слі', ' указы', '最专业的', ' siguran', 'FIL', 'ordat', '歌迷', ' fenom', ' alarma', '兵种', '繽', '罗那', '菸', 'unie', '_variation', ' élvez', '/Graphics', ' bubuk', '空空', 'Signals', 'رداد', '籌', ' ули', ' poja', '私家']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass plain27: [' called', 'called', '_Dec', ' December', ' Januari', ' termed', ' Boxing', ' называется', ' usually', 'Called', 'usually', 'December', '眯眯', '称为', ' Ро', '-Jan', 'winter', '展望', '谓之', ' typically', '新的一年', 'uary', ' Dec', '____', ' referred', ' appelé', 'known', 'áno', ' জান', ' known', ' ژ', '.Dec']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass logit contrast plain27: ['最专业的', 'ẹo', '路人', 'Profiles', ' Industr', '很多玩家', 'spots', '为玩家', 'channels', 'ỏa', '任せ', ' Igre', '屋主', 'Chunks', 'Paths', '억원을', 'Ports', 'Escort', ' prevé', ' pupper', 'Loads', ' porsi', 'profiles', 'Channels', '智慧型', 'Sets', '玩家可以', 'drivers', 'Drivers', '密密', '罗那', 'Assets']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass probability contrast plain27: [' called', 'called', '_Dec', ' Januari', ' termed', ' Boxing', ' называется', 'Called', 'usually', 'December', '眯眯', '称为', ' Ро', '-Jan', 'winter', '展望', '谓之', '新的一年', ' usually', 'uary', '____', ' Dec', ' typically', ' appelé', 'known', 'áno', ' জান', ' referred', ' ژ', '.Dec', 'spy', 'typically']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass mismatched logit contrast plain27: ['展望', ' jendela', 'spy', 'Assets', 'ecat', 'amai', ' пузыря', 'Profiles', ' Luogo', 'ợ', ' porsi', '雰', '歌迷', '嬢', 'ADV', '路人', '次年', '.bio', 'ovem', 'Sets', ' nutris', '幻影', 'ecam', ' Potenza', '的那个人', 'aupts', ' memin', 'signals', 'เล่ม', '_arrays', '这个方法', '.Areas']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass pursuit J24: ['Months', 'ถัด', ' appelée', ".'.", ' Easter', '...*', ' kalt', ' Bia', '来过', '完全不', ' Moda', '＿＿', ' považ', '烟花', '。）', ' Spam', 'FOUND', ' Maxi', '朦', 'TRL', ' Ibu', '闰', ' Té', '蒜', '通常', ' Sleeve', ' Quello', 'APO', ' Fuji', '空', 'BEGIN']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot matched J24: [' Months', ' December', ' months', ' February', '月份', 'Months', 'months', ' November', ' Year', ' April', '-month', ' Januari', ' Calendar', '月份的', ' October', '次年', ' Monthly', ' calendar', ' September', 'February', 'calendar', 'December', ' Ramadan', ' winter', ' Spring', '_month', ' Winter', ' Easter', ' July', '(month', ' year']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot matched J24: [' Months', ' December', '月份', ' February', 'Months', ' Januari', ' November', 'months', '-month', ' months', '(month', ' April', '月份的', ' bulan', ' tháng', 'เดือน', '_month', 'February', ' Tháng', 'December', ' Oktober', ' October', '.month', ' Februari', '次年', 'ในเดือน', '.Month', ' Ramadan', ' September', ' Marzo', 'calendar']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot full32 J24: [' Months', ' December', ' months', ' February', '月份', 'Months', 'months', ' November', ' Year', ' April', '-month', ' Januari', ' Calendar', '月份的', ' October', '次年', ' Monthly', ' calendar', ' September', 'February', 'calendar', 'December', ' Ramadan', ' winter', ' Spring', '_month', ' Winter', ' Easter', ' July', '(month', ' year', '/month']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot full32 J24: [' Months', ' December', '月份', ' February', 'Months', ' Januari', ' November', 'months', '-month', ' months', '(month', ' April', '月份的', ' bulan', ' tháng', 'เดือน', '_month', 'February', ' Tháng', 'December', ' Oktober', ' October', '.month', ' Februari', '次年', 'ในเดือน', '.Month', ' Ramadan', ' September', ' Marzo', 'calendar', '一个月的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass pursuit plain24: [' называется', 'رداد', ' preceded', 'ถัด', '...', ' usually', ' calendar', ' pove', ' regarded', ' наступ', '.', '/ap', '/', ' fools', '°', ' Cyber', '尾巴', '(name', '.getMonth', ' __________________', '眯眯', ' Numer', ' ули', ':', '—', '那个', ' Boxing', '担保', 'Y', ' in', ' qualit']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot matched plain24: [' called', '眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', ' kolej', ' наступ', '志愿服务队', '問わず', ' называется', 'ถัด', '人も多い', 'FOUND', 'called', 'orate', ' Fucking', '{name', ' ули', 'ullo', '新社', ' kalt', '下一章', '球迷们', 'CALE', '.getMonth', ' appelé', 'Called', '紧接着']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot matched plain24: [' называется', ' called', ' termed', 'رداد', ' appelé', ' invariably', 'ถัด', ' preceded', ' považ', ' наступ', ' называют', '.getMonth', 'called', ' kolej', '眯眯', '紧接着', '志愿服务队', '・・・・', '_calendar', ' kalt', ' appelée', ' usually', ' указы', ' ули', '問わず', 'Called', ' calendar', ' Tháng', 'calendar', ' Folg', 'unie']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot full32 plain24: [' called', '眯眯', 'رداد', ' Folg', 'unie', ' termed', ' preceded', ' invariably', ' kolej', ' наступ', '志愿服务队', '問わず', ' называется', 'ถัด', '人も多い', 'FOUND', 'called', 'orate', ' Fucking', '{name', ' ули', 'ullo', '新社', ' kalt', '下一章', '球迷们', 'CALE', '.getMonth', ' appelé', 'Called', '紧接着', '谤']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot full32 plain24: [' называется', ' called', ' termed', 'رداد', ' appelé', ' invariably', 'ถัด', ' preceded', ' považ', ' наступ', ' называют', '.getMonth', 'called', ' kolej', '眯眯', '紧接着', '志愿服务队', '・・・・', '_calendar', ' kalt', ' appelée', ' usually', ' указы', ' ули', '問わず', 'Called', ' calendar', ' Tháng', 'calendar', ' Folg', 'unie', 'FOUND']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass pursuit plain27: [' called', '_Dec', '____', ' Boxing', '展望', '...', 'usually', ' Ро', '资料来源', '.', ' Sap', ' theaters', '的那个人', '悟', '/j', '                               ', '{}.', ' comput', '水仙', '?', ' посл', ':', 'v', ' preceded', '动感', '手が', ' Δ', '\xa0', ' Reis', 'D']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot matched plain27: [' called', 'called', ' December', '_Dec', ' Januari', ' termed', ' Boxing', ' называется', ' usually', 'Called', 'December', 'usually', '眯眯', '称为', '-Jan', ' Ро', 'winter', '展望', '谓之', ' typically', '新的一年', 'uary', ' Dec', ' referred', '____', ' appelé', 'known', 'áno', ' জান', ' known']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot matched plain27: [' December', ' called', '_Dec', 'December', 'called', ' называется', ' Januari', ' termed', ' Boxing', 'usually', ' appelé', ' usually', ' February', '\tJ', ' Ро', ' জান', 'Called', ' december', 'winter', 'February', '____', '称为', ' 일반적으로', ' typically', ' connu', '新的一年', ' معمول', ' __________________', 'typically', ' januari']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass raw-dot full32 plain27: [' called', 'called', ' December', '_Dec', ' Januari', ' termed', ' Boxing', ' называется', ' usually', 'Called', 'December', 'usually', '眯眯', '称为', '-Jan', ' Ро', 'winter', '展望', '谓之', ' typically', '新的一年', 'uary', ' Dec', ' referred', '____', ' appelé', 'known', 'áno', ' জান', ' known', ' ژ', '.Dec']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass unit-dot full32 plain27: [' December', ' called', '_Dec', 'December', 'called', ' называется', ' Januari', ' termed', ' Boxing', 'usually', ' appelé', ' usually', ' February', '\tJ', ' Ро', ' জান', 'Called', ' december', 'winter', 'February', '____', '称为', ' 일반적으로', ' typically', ' connu', '新的一年', ' معمول', ' __________________', 'typically', ' januari', ' يناير', 'เรียกว่า']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'

Baseline: ' January.\nQuestion: What is the'

end-pass negative final control: ['Chunks', ' potr', '三道', 'ELLO', '如火', '蓬', '卡斯', '天之', 'HQ', ' Turqu', '嘻', 'Kh', '各路', ' crít', ',msg', '如潮', '�', '中俄', 'Channels', 'atika', '和使用', 'chunks', ' Purtroppo', 'Gate', '老', '成', ',cp', '-Cs', '东道', '早前', 'Sections', 'igos']

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

end-pass logit contrast J-lens: ['Days', '第三天', '第二天', 'days', '-Day', '明天的', '次日', '-days', '隔天', '几天', 'weeks', ' неделя', '_day', '几天的', '。)', '第一天', '.day', '今天是', ' días', '通宵', ' semana', '十天', ').-', '一天', '两天', ' غد', '早晨', '_days', ' día', ' Days', '日期', '晨']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass probability contrast J-lens: [' Tuesday', ' Monday', ' Saturday', ' Mondays', ' tomorrow', ' Tues', ' monday', 'Monday', ' weekend', ' Sundays', ' Saturdays', ' Days', ' Thanksgiving', 'Tuesday', ' weekdays', ' Thurs', ' weekends', ' days', 'Thursday', ' morning', 'Saturday', 'days', ' Halloween', ' sunday', 'Wednesday', ' Tomorrow', ' вторник', '这一天', '星期三', ' yesterday', '星期日', ' Weekend']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass mismatched logit contrast J-lens: ['今天是', 'Thursday', 'Tuesday', 'Monday', ' Thursday', ' Tuesday', 'Saturday', '星期六', 'Wednesday', '星期日', ' Wednesday', '隔天', 'Sunday', '周四', '星期一', ' Saturday', '星期四', '北欧', '第二天', '明天的', 'aturday', '星期二', '星期三', ' Mondays', '周六', ' Monday', '周末', ' monday', ' غد', 'days', '-days', '两天']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass plain24: [' called', 'always', 'called', ' الني', ' preceded', '除恶', 'pras', '现代的', '为己', 'lands', ' Dici', 'eve', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', 'leid', '诞辰', 'wand', 'svc', 'ủy', 'IVERY', '酬', '动感', 'forth', ' Lapangan', ' supposed', '又快', '个大', ' lucr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass logit contrast plain24: ['wand', 'Elec', 'Surface', 'ovem', 'SIG', 'Materials', ' Dici', 'เติ', 'chas', 'ulli', 'signals', '工', 'GRP', ' biste', '表面上', 'COPE', 'SETTING', '兵种', '罗那', 'Signals', 'ớm', '个大', ' creativ', ' jurnal', ' Personn', '大有', 'Cols', 'weis', '学工', 'IMG', '建置', 'Codes']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass probability contrast plain24: ['always', 'called', ' الني', '除恶', ' preceded', 'pras', '为己', '现代的', 'lands', ' Dici', 'eve', 'unno', '금', 'ulli', 'orate', 'boxing', 'wand', 'svc', 'leid', '诞辰', 'ủy', 'IVERY', '动感', '酬', 'forth', ' Lapangan', '又快', '个大', ' lucr', 'gelegt', 'hog', '开放']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass mismatched logit contrast plain24: ['为己', 'leid', '表面上', 'svc', ' Dici', 'providers', 'ulli', 'ẹt', 'ỏa', 'wand', ' jurnal', ' нор', ' الني', 'ử', 'ằm', 'handlers', 'Ử', 'adurch', '教工', 'logs', 'ũi', 'paths', '除恶', 'ubro', 'vey', 'lieg', ' подлежит', '开放', 'odin', '良', 'Elec', '表面']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass plain27: [' среда', ' Wednesday', ' Thursday', ' Thurs', 'called', ' wed', 'uesday', ' Чет', 'Monday', ' Monday', ' Wed', ' Thu', ' called', ' среду', 'FR', 'Wednesday', 'Thursday', ' Tuesday', '除恶', 'gios', 'always', '_FR', '금', '又快', 'Tuesday', 'сре', '饱和度', 'nesday', ' Saturday', 'agna', ' среды', 'bru']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass logit contrast plain27: ['法', 'Instrument', '主', '克隆', '法是', 'captures', 'ọng', '屋主', 'iền', 'agna', 'Cols', 'Artifact', 'Patch', 'Localization', 'Imports', ' Commentaires', 'Crit', 'ại', 'ỏa', '他的人', 'wend', 'Attack', 'imports', 'Capt', '锄', 'Eye', '派', '附图', 'Calls', ' Detalles', '自助', 'channels']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass probability contrast plain27: [' среда', 'called', ' wed', ' Thurs', 'uesday', ' Чет', 'Monday', ' Thu', ' среду', ' Wed', 'FR', 'Wednesday', 'Thursday', '除恶', 'gios', 'always', '_FR', '금', '又快', 'Tuesday', 'сре', '饱和度', 'nesday', 'agna', ' среды', 'bru', 'ued', '星期三', 'NOT', 'aturday', 'rides', 'Thứ']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass mismatched logit contrast plain27: ['providers', 'leid', ' среда', '饱和度', '瑞典', 'handlers', 'edr', 'imports', 'handling', 'ASCII', '主管', 'rides', 'FR', 'ằm', 'ỏa', 'channels', 'bindings', 'Thursday', 'svc', 'Attack', '法', '为己', 'UES', 'paths', 'Wednesday', 'Imports', 'ήμε', '今天的', '赔', 'addresses', ' Psic', 'charges']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass pursuit J24: [' Thursday', '北欧', ' Halloween', '称为', ' غد', '».**', ' День', ' Erz', '__)', ' Marte', ' Sanc', '通宵', ' Ragnar', '公', '개가', ' Budi', '...”', ' oslo', ' Kolej', '完全不', '劳动节', '对应的', '自由', ' Cha', ' ausg', '<w', ' isti', 'MI', ' paro', ' Maxi', ' Toujours', ' Ruh']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot matched J24: [' Tuesday', ' Thursday', ' Monday', ' Saturday', ' Wednesday', ' Sunday', ' Mondays', ' tomorrow', ' Tues', ' monday', 'Monday', ' Thurs', ' Thanksgiving', ' weekend', ' Sundays', ' Saturdays', ' Days', 'Tuesday', ' weekdays', ' weekends', ' days', 'Thursday', ' Christmas', ' Halloween', ' morning', 'Saturday', ' today', ' yesterday', 'days', ' called', ' sunday', 'Wednesday']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot matched J24: [' Thursday', ' Tuesday', ' Monday', ' Wednesday', ' Saturday', ' Sunday', ' Thurs', ' Tues', ' Mondays', ' Thanksgiving', 'Monday', 'Tuesday', 'Thursday', ' Halloween', ' Saturdays', ' monday', ' Christmas', ' Sundays', ' weekdays', ' вторник', 'Saturday', ' weekend', 'Wednesday', '星期三', ' weekends', '星期四', ' Days', '星期日', ' Iceland', ' tomorrow', ' Oktober', ' Easter']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot full32 J24: [' Tuesday', ' Thursday', ' Monday', ' Saturday', ' Wednesday', ' Sunday', ' Mondays', ' tomorrow', ' Tues', ' monday', 'Monday', ' Thurs', ' Thanksgiving', ' weekend', ' Sundays', ' Saturdays', ' Days', 'Tuesday', ' weekdays', ' weekends', ' days', 'Thursday', ' Christmas', ' Halloween', ' morning', 'Saturday', ' today', ' yesterday', 'days', ' called', ' sunday', 'Wednesday']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot full32 J24: [' Thursday', ' Tuesday', ' Monday', ' Wednesday', ' Saturday', ' Sunday', ' Thurs', ' Tues', ' Mondays', ' Thanksgiving', 'Monday', 'Tuesday', 'Thursday', ' Halloween', ' Saturdays', ' monday', ' Christmas', ' Sundays', ' weekdays', ' вторник', 'Saturday', ' weekend', 'Wednesday', '星期三', ' weekends', '星期四', ' Days', '星期日', ' Iceland', ' tomorrow', ' Oktober', ' Easter']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass pursuit plain24: [' called', 'always', '...', ' الني', ' preceded', '____', ' Boxing', '现代的', '<|im_end|>', '开放', '금', '表面上', ' eig', '除恶', ' a', '动感', ' нор', ' Labor', 'le', '.', ' NOT', ']].', '树林', '少儿', ' информ', '阳极', ' ', ' lands', ' colleg', '/']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot matched plain24: [' called', 'always', 'called', ' الني', '除恶', ' preceded', 'pras', '现代的', '为己', 'lands', 'eve', ' Dici', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', '诞辰', 'wand', 'leid', 'svc', 'ủy', 'IVERY', '酬', '动感', 'forth', ' Lapangan', '又快', ' supposed']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot matched plain24: [' called', 'always', 'called', ' preceded', ' الني', ' называется', ' always', '现代的', ' информ', '诞辰', ' disebut', ' Boxing', 'IVERY', '除恶', ' lucr', '动感', ' Always', ' Dici', 'Always', '的名称', ' مرتبط', '少儿', ' 반드시', '금', '・・・・', ' нор', 'lands', ' Dzie', ' Lapangan', '呼び']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot full32 plain24: [' called', 'always', 'called', ' الني', '除恶', ' preceded', 'pras', '现代的', '为己', 'lands', 'eve', ' Dici', ' always', 'unno', '금', 'ulli', 'orate', 'boxing', '诞辰', 'wand', 'leid', 'svc', 'ủy', 'IVERY', '酬', '动感', 'forth', ' Lapangan', '又快', ' supposed', 'gelegt', '个大']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot full32 plain24: [' called', 'always', 'called', ' preceded', ' الني', ' называется', ' always', '现代的', ' информ', '诞辰', ' disebut', ' Boxing', 'IVERY', '除恶', ' lucr', '动感', ' Always', ' Dici', 'Always', '的名称', ' مرتبط', '少儿', ' 반드시', '금', '・・・・', ' нор', 'lands', ' Dzie', ' Lapangan', '呼び', '开放时间', 'boxing']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass pursuit plain27: [' Thursday', '...', 'called', ' среда', 'FR', ' Þ', ' wed', ' Чет', ' Mon', '금', ' pagan', ' ', 'always', ']].', '<|im_end|>', '除恶', ':', 'NOT', ' Boxing', '瑞典', '开放', 'Thứ', ' inaugur', '____', '.', '动感', 'bru', ' a', '-S', '推断', 'rides']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot matched plain27: [' среда', ' Wednesday', ' Thursday', ' Thurs', 'called', ' wed', 'uesday', ' Чет', 'Monday', ' Monday', ' Wed', ' Thu', ' called', ' среду', 'FR', 'Wednesday', 'Thursday', 'gios', ' Tuesday', '除恶', 'always', '_FR', '금', '又快', 'Tuesday', 'сре', '饱和度', 'nesday', ' Saturday', 'agna', ' среды']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot matched plain27: [' Thursday', ' Wednesday', 'Monday', ' среда', ' Monday', 'Thursday', 'Wednesday', ' Thurs', ' среду', ' Чет', 'called', ' Tuesday', 'Tuesday', 'uesday', ' Thu', ' Saturday', '_FR', ' called', ' Wed', ' среды', ' wed', 'FR', 'Saturday', ' Þ', 'always', 'Thứ', '星期三', '瑞典', ' امروز', ' aujourd', 'ุกร์']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass raw-dot full32 plain27: [' среда', ' Wednesday', ' Thursday', ' Thurs', 'called', ' wed', 'uesday', ' Чет', 'Monday', ' Monday', ' Wed', ' Thu', ' called', ' среду', 'FR', 'Wednesday', 'Thursday', 'gios', ' Tuesday', '除恶', 'always', '_FR', '금', '又快', 'Tuesday', 'сре', '饱和度', 'nesday', ' Saturday', 'agna', ' среды', 'bru']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass unit-dot full32 plain27: [' Thursday', ' Wednesday', 'Monday', ' среда', ' Monday', 'Thursday', 'Wednesday', ' Thurs', ' среду', ' Чет', 'called', ' Tuesday', 'Tuesday', 'uesday', ' Thu', ' Saturday', '_FR', ' called', ' Wed', ' среды', ' wed', 'FR', 'Saturday', ' Þ', 'always', 'Thứ', '星期三', '瑞典', ' امروز', ' aujourd', 'ุกร์', ' معمول']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'

Baseline: ' Friday.\nQuestion: What day of'

end-pass negative final control: ['十多年', '始至', 'NPC', '并进', '忍', '世', '大', '正反', ' porsi', '正', '波波', 'ienes', 'engew', '刁', '有生', 'راحل', 'Searching', '八', '蓬', '八年', 'Areas', 'Ratio', '百', 'Leading', '在身', 'Piece', '科', '信', 'Weights', 'িয়ে', 'ellit', 'Lane']

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

end-pass logit contrast J-lens: ['季节', 'months', '-season', '季节性', '季', 'Months', '月份', '旺季', ' saisons', '季節', ' saison', ' сезон', '的季节', ' sezon', '学期', ').\\', '是一年', 'foods', 'ฤดูกาล', ' Vacances', 'cycles', 'month', '淡季', ' Saison', '一年四季', '赛季', '四季', ' hónap', ' stagione', '雨季', ' cuaca', ' Nouve']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass probability contrast J-lens: [' seasons', '冬季', ' rainy', '春季', ' summers', ' warmer', 'summer', '___', ' seasonal', '季节', '__.', '____', '雨季', '夏季', '冬天', ' primavera', '-season', '...\\', ' Seasons', '________', 'spring', '春天', ' drought', '旺季', '淡季', 'Spring', ' printemps', ' colder', '.\\', '_____', '__', '的季节']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass mismatched logit contrast J-lens: ['季节', '雨季', '季', '春季', '冬季', ' seasons', '-season', 'summer', 'Months', 'months', '夏季', '_season', '季节性', 'spring', '的季节', '季风', '冬', 'Spring', ' mùa', '季節', ' сезон', '春暖花开', '旺季', ' Tết', ' musim', '冬天', 'Climate', '.Spring', '温暖', 'ropical', '春天', '春']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass plain24: [' preceded', ' наступ', 'spring', ' called', '紧接着', ' seasons', ' invariably', '到来', 'called', ' называется', '是一年', 'rollers', 'orate', '.navigationBar', 'unno', ' termed', 'summer', "').'", ' قائ', '鸟语', ' followed', 'nam', '个字', '{name', '問わず', 'dess', 'のことを', '叫做', ' always', 'angat', '休止', 'beg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass logit contrast plain24: ['perms', 'providers', 'ũi', '帕特', 'TRL', 'programs', 'ỏa', ' sendok', 'bands', 'foods', ' Industr', '-caption', 'logg', ' Canti', 'videos', '私家', 'eppe', ' sluts', ' trasparen', ' Justi', '教体', 'ẹo', 'ovem', '大厨', ' Direktorat', 'protocols', '-orders', ' Crushers', ' profesi', 'urers', 'TML', "').'"]

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass probability contrast plain24: [' preceded', ' наступ', 'spring', '紧接着', ' seasons', ' invariably', '到来', 'called', '是一年', ' называется', 'rollers', 'orate', '.navigationBar', 'unno', 'summer', "').'", ' قائ', '鸟语', ' termed', 'nam', '个字', '{name', 'dess', '問わず', 'のことを', '叫做', 'angat', '休止', 'beg', '바로', '序幕', '幕']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass mismatched logit contrast plain24: ['帕特', ' sacerdo', 'angat', 'summ', 'beg', 'artimento', 'spring', '最专业的', '接着', '季', ' قائ', '暖意', ' mùa', ' celo', 'rollers', ' komunit', '休止', '温暖的', '休', ' наступ', 'Compression', ' Comunidad', '紧接着', 'haul', ' Gober', 'getManager', ' ką', ' Vacances', '航站', ' تاب', 'رداد', 'ỏa']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass plain27: ['spring', 'Spring', 'pring', ' spring', ' Spring', ' summer', 'summer', ' springs', '春', ' autumn', '.spring', ' verano', ' primavera', ' Summer', '春天', '春意', 'Summer', ' наступ', 'fall', '\tSpring', ' summers', ' called', ' printemps', '.Spring', '春的', ' verão', '夏', ' preceded', 'ommer', ' FALL', ' vinter', '春季']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass logit contrast plain27: ['providers', 'protocols', ' gelas', 'programs', 'ũi', '程序设计', 'videos', 'Investigators', 'operators', 'modes', 'ắn', 'methods', ' Industr', 'ركان', 'channels', 'paths', ' sendok', 'VECTOR', 'properties', 'urers', 'ẹo', 'ownik', 'configs', '客机', '教体', 'signals', 'handles', '全文数据库', 'neighbors', 'bundle', 'formats', 'eppe']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass probability contrast plain27: ['spring', 'Spring', 'pring', 'summer', ' springs', '春', '.spring', ' primavera', ' verano', '春意', '春天', ' наступ', 'Summer', 'fall', '\tSpring', ' summers', ' printemps', ' verão', '.Spring', '春的', '夏', 'ommer', ' preceded', ' FALL', ' vinter', '春季', ' zomer', '(Spring', '夏季', ' الرب', '春来', 'unno']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass mismatched logit contrast plain27: ['spring', 'Spring', '春', 'pring', '.spring', 'summer', '春意', ' تاب', '春的', 'summ', ' mùa', ' verano', '夏', ' springs', 'Summer', '.Spring', '春季', '春天', '\tSpring', ' наступ', '(Spring', 'ăt', '弹簧', 'ommer', 'ographers', '暖意', 'artimento', '冬', '尴', ' primavera', 'ownik', 'ummer']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass pursuit J24: ['干旱', '__.', '叫做', '紧接着', ' Tropical', ' begon', '樱花', 'PEAT', 'Months', '暖气', '。）', '充满活力', '造林', '相反的', ' Festiv', '<u', ' GREEN', '到来', ' Quali', '”…', '通常是', ' cic', ' Autre', ' Basketball', ' ausg', ' Compre', ' kalt', 'BEGIN', '马超', ' Té', '«.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot matched J24: [' summer', ' seasons', ' autumn', '冬季', ' rainy', ' spring', ' warmer', '春季', ' summers', 'summer', '___', ' seasonal', ' Summer', '季节', '__.', ' Spring', '____', '雨季', '夏季', '冬天', ' Autumn', ' primavera', '-season', '...\\', ' called', ' Seasons', 'spring', '________', '春天', ' drought', '旺季']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot matched J24: [' autumn', ' primavera', ' summer', '冬季', '春季', ' rainy', ' printemps', ' seasons', ' зим', '雨季', 'summer', ' vinter', '冬天', ' Autumn', '季节', '春天', '夏季', ' spring', ' drought', 'ฤดู', ' summers', ' hiver', '春暖花开', ' Mùa', ' invierno', ' seasonal', '旺季', ' inverno', ' Summer', '秋季', ' warmer']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot full32 J24: [' summer', ' seasons', ' autumn', '冬季', ' rainy', ' spring', ' warmer', '春季', ' summers', 'summer', '___', ' seasonal', ' Summer', '季节', '__.', ' Spring', '____', '雨季', '夏季', '冬天', ' Autumn', ' primavera', '-season', '...\\', ' called', ' Seasons', 'spring', '________', '春天', ' drought', '旺季', ' colder']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot full32 J24: [' autumn', ' primavera', ' summer', '冬季', '春季', ' rainy', ' printemps', ' seasons', ' зим', '雨季', 'summer', ' vinter', '冬天', ' Autumn', '季节', '春天', '夏季', ' spring', ' drought', 'ฤดู', ' summers', ' hiver', '春暖花开', ' Mùa', ' invierno', ' seasonal', '旺季', ' inverno', ' Summer', '秋季', ' warmer', '淡季']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass pursuit plain24: [' preceded', '.', ' called', ' наступ', '...', ' invariably', ' seasons', 'spring', '.navigationBar', '_the', "').'", '干旱', '/w', '名', ':', ' NOT', ' agriculture', '____', '到来', ' bore', '鸟语', '暖', ' a', ' rigor', '(s', 'dic', ' ', '冲刺', '\r', '另一种', 'beg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot matched plain24: [' preceded', ' наступ', 'spring', ' called', '紧接着', ' seasons', ' invariably', '到来', 'called', ' называется', '是一年', 'rollers', 'orate', 'summer', ' termed', 'unno', '.navigationBar', ' followed', "').'", ' قائ', '鸟语', 'nam', '个字', '{name', 'dess', '問わず', '叫做', 'のことを', ' always', 'angat', 'beg']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot matched plain24: [' preceded', ' наступ', ' называется', ' called', '紧接着', ' seasons', 'spring', ' invariably', '.navigationBar', ' termed', 'called', ' называют', ' forests', 'summer', '_the', '到来', ' agriculture', 'ฤดู', 'のことを', ' vinter', '温暖的', ' characterized', 'Spring', ' autumn', '鸟语', ' followed', ' springs', '是一年', '序幕', ' длится', ' bureaucracy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot full32 plain24: [' preceded', ' наступ', 'spring', ' called', '紧接着', ' seasons', ' invariably', '到来', 'called', ' называется', '是一年', 'rollers', 'orate', 'summer', ' termed', 'unno', '.navigationBar', ' followed', "').'", ' قائ', '鸟语', 'nam', '个字', '{name', 'dess', '問わず', '叫做', 'のことを', ' always', 'angat', 'beg', '바로']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot full32 plain24: [' preceded', ' наступ', ' называется', ' called', '紧接着', ' seasons', 'spring', ' invariably', '.navigationBar', ' termed', 'called', ' называют', ' forests', 'summer', '_the', '到来', ' agriculture', 'ฤดู', 'のことを', ' vinter', '温暖的', ' characterized', 'Spring', ' autumn', '鸟语', ' followed', ' springs', '是一年', '序幕', ' длится', ' bureaucracy', ' typically']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass pursuit plain27: ['Spring', ' called', ' summer', ' наступ', ' characterized', '...', '客机', 'ใบ', ' invariably', '(s', '上传者', ':', ' bore', '降水', ' hotter', '____', '园艺', 'unno', '_prim', '另一种', '/', '<|im_end|>', ' ', '全文数据库', ' Crédit', '紧接着', '.', 'nt', ' Boxing', 'Aut', '短袖']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot matched plain27: ['spring', 'Spring', 'pring', ' spring', ' Spring', ' summer', 'summer', ' springs', '春', ' autumn', '.spring', ' primavera', ' verano', ' Summer', '春意', '春天', ' наступ', 'Summer', 'fall', ' summers', '\tSpring', ' called', ' printemps', ' verão', '春的', '.Spring', '夏', 'ommer', ' preceded', ' FALL', ' vinter']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot matched plain27: ['Spring', 'spring', ' spring', ' Spring', ' summer', ' autumn', 'pring', ' springs', 'summer', ' verano', ' primavera', ' Summer', 'Summer', '春', '春天', ' printemps', '.spring', '春意', ' Autumn', ' called', ' наступ', ' verão', '\tSpring', ' vinter', '.Spring', '春季', 'ฤดู', ' summers', '春的', ' characterized', ' preceded']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass raw-dot full32 plain27: ['spring', 'Spring', 'pring', ' spring', ' Spring', ' summer', 'summer', ' springs', '春', ' autumn', '.spring', ' primavera', ' verano', ' Summer', '春意', '春天', ' наступ', 'Summer', 'fall', ' summers', '\tSpring', ' called', ' printemps', ' verão', '春的', '.Spring', '夏', 'ommer', ' preceded', ' FALL', ' vinter', '春季']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass unit-dot full32 plain27: ['Spring', 'spring', ' spring', ' Spring', ' summer', ' autumn', 'pring', ' springs', 'summer', ' verano', ' primavera', ' Summer', 'Summer', '春', '春天', ' printemps', '.spring', '春意', ' Autumn', ' called', ' наступ', ' verão', '\tSpring', ' vinter', '.Spring', '春季', 'ฤดู', ' summers', '春的', ' characterized', ' preceded', ' 봄']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'

Baseline: ' winter.\nHypothesis: The'

end-pass negative final control: ['ienes', '内外', '甚至', ' Ubicación', '聚', 'iett', 'Prosec', '成', 'JM', '一滴', 'ệ', '摩根', '左右', ',msg', '成分', ' puluhan', ' Tamaño', 'copies', '散', '功效', '-stats', '道具', '毒', ' Acomp', 'Loads', '-pointer', '神', 'channels', '充', 'NPC', ' пъти', 'нди']

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

end-pass logit contrast J-lens: ['黑色', '颜色', 'pink', '紫色', 'Colors', '黄色', '灰色', '黑白', '黑色的', 'brown', '棕色', 'orange', 'colors', 'BMW', ' Berlino', '蓝色', '橙色', '粉色', '-black', 'purple', '柏林', '-Nazi', 'oracle', '白色', 'tries', ' سامسون', 'cakes', ' cesto', '粉色的', '颜色的', '_colors', 'black']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass probability contrast J-lens: [' purple', '红色', ' pink', ' blue', 'pink', ' black', ' Purple', ' violet', ' strawberry', 'purple', ' green', ' Pink', ' poisonous', ' yellow', '(red', ' orange', ' berries', '蓝色', ' rouge', '红色的', ':red', '粉红色', ' strawberries', ' blonde', ' crimson', '_red', 'blue', '-red', ' красный', ' brown', ' Strawberry', ' rojo']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass mismatched logit contrast J-lens: ['红色', '毒', '(red', 'pink', 'purple', 'green', '红线', '黑色', '粉红色', 'blue', 'agenta', '颜色', '/blue', '绿色', 'Pink', '绿', '血色', ' красный', '变色', '蓝色', 'berries', '.blue', '_blue', ' kecantikan', '粉红', '-black', 'black', '白马', '白色', '/red', '.green', '粉色']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass plain24: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', 'aches', '红色', '惨叫', 'atrices', "').'", '分享到朋友圈', '史蒂', 'canf', '_red', 'мали', 'attended', 'シャー', '目瞪', 'pozn', '빨', '永远的', '_integration', '对白', 'ряда', ' })).', '白金', '红红的', ' Bái', 'maid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass logit contrast plain24: [' Haci', '_processes', '頂けます', '疗', '阪', 'ăto', ' warta', ' helsing', '目瞪', '依法须经', ' 웹사이트가', ' سامسون', ' licensors', '.sax', ' Financi', ' фору', '贸市场', 'Concurrency', ' szo', ' указы', ' utrecht', '_topology', ' ván', '慷', ' Acomp', '守', ' الثان', ' khấu', '惣', 'меется', 'npc', 'blogs']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass probability contrast plain24: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', 'aches', '红色', 'atrices', '惨叫', 'canf', '分享到朋友圈', "').'", '史蒂', '_red', 'мали', 'attended', '目瞪', 'シャー', 'pozn', '빨', '对白', '_integration', '永远的', ' })).', 'ряда', ' Bái', '白金', '红红的', ' эксперти']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass mismatched logit contrast plain24: ['intégration', 'anjutkan', 'kań', 'illeurs', 'canf', 'mailer', '如荼', '除恶', 'npc', 'integration', 'comings', 'baikan', 'szik', '踩过', '对白', '嫣', 'MDB', ' استف', 'empf', 'cakes', '本色', '守则', 'μισ', ' eksplo', 'меется', '复方', ' Haci', ' Soyez', 'isial', 'シャー', 'будьте', 'attended']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass plain27: ['红色', ' poisoning', '_red', ':red', '红了', '红', '中毒', ' красный', '紅色', '.apple', '紅', '红线', ' poisonous', '.red', '致命', ' rojo', '红红的', '(red', '红梅', '绯', '毒', 'мали', '-red', ' الأحمر', '的红', ' đỏ', '红色的', 'apple', '红的', '通红', 'Apple', ' apple']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass logit contrast plain27: [' Haci', '_processes', ' sanks', 'trajectory', 'buffers', ' Industr', 'aissez', ' trgov', ' Presupuesto', ' Tamaño', ' juridi', 'solver', 'departments', 'Monitoring', ' Publicidad', 'libraries', '目瞪', 'massage', ' Muit', ' накопи', 'queues', '拉里', ' Avrup', ' 웹사이트가', 'touches', 'implements', ' phím', ' Eventi', 'baikan', 'vendors', 'providers', 'forums']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass probability contrast plain27: ['红色', ' poisoning', '_red', ':red', '红了', '红', '中毒', ' красный', '紅色', '红线', '.apple', '紅', '.red', ' poisonous', '致命', ' rojo', '红红的', '毒', 'мали', '红梅', '绯', '(red', ' الأحمر', '-red', '的红', ' đỏ', '红色的', 'apple', '通红', '红的', '-po', ' červen']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass mismatched logit contrast plain27: ['毒', '致命', '红线', '中毒', '本色', '如荼', 'ーマ', 'szik', 'MDB', 'integration', '配方', ' Prise', 'GREEN', 'мали', '-po', 'kań', '致命的', 'plots', '红色', 'canf', ' накопи', 'pozn', '剧毒', '红了', ' poisoning', '粉红', 'íta', 'mailer', ' الأحمر', 'poj', '玫', '.po']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass pursuit J24: [' pink', ' strawberries', '红色', '。\\', ' BLACK', ' Apfel', '|.', '在德国', ' Granny', '描述', ' ined', ' Candy', '貂', ' Bái', 'MC', ' LENG', '*/)', 'FALSE', ' dran', ' güz', ' Alba', '薇', '··', ' Interna', ' Toujours', ' Sya', ' Erz', ' bbc', ' berüh', '�', 'ریان']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot matched J24: [' purple', '红色', ' pink', ' blue', 'pink', ' black', ' green', ' Purple', ' violet', ' strawberry', 'purple', ' Pink', ' poisonous', ' yellow', ' orange', '(red', ' berries', '蓝色', ' rouge', ':red', '红色的', '粉红色', ' strawberries', ' apple', ' crimson', ' blonde', '_red', 'blue', '-red', ' красный', ' brown']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot matched J24: [' pink', ' purple', '红色', ' strawberry', 'pink', ' красный', ' rossa', ' strawberries', ' rojo', 'purple', ' rouge', ' poisonous', ' blonde', ' rosso', ' berries', '(red', ' violet', ' orange', ' Purple', '红色的', ' blue', ' Pink', '粉红色', ' crimson', ' Strawberry', '_red', '紅色', ':red', ' rouges', ' yellow', '蓝色']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot full32 J24: [' purple', '红色', ' pink', ' blue', 'pink', ' black', ' green', ' Purple', ' violet', ' strawberry', 'purple', ' Pink', ' poisonous', ' yellow', ' orange', '(red', ' berries', '蓝色', ' rouge', ':red', '红色的', '粉红色', ' strawberries', ' apple', ' crimson', ' blonde', '_red', 'blue', '-red', ' красный', ' brown', ' Strawberry']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot full32 J24: [' pink', ' purple', '红色', ' strawberry', 'pink', ' красный', ' rossa', ' strawberries', ' rojo', 'purple', ' rouge', ' poisonous', ' blonde', ' rosso', ' berries', '(red', ' violet', ' orange', ' Purple', '红色的', ' blue', ' Pink', '粉红色', ' crimson', ' Strawberry', '_red', '紅色', ':red', ' rouges', ' yellow', '蓝色', ' blau']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass pursuit plain24: ['红颜', ' лечению', ' depicted', '红色', ' organs', '....', '全文数据库', '_', ' poisoning', '/w', ' diam', '.', 'シャー', '史蒂', ' a', 'MC', ' утвер', ' бел', '�', '变电', '<|im_end|>', '_integration', 'Ford', 'related', ' (', '惨叫', ' berries', ' spo', 'B', '通常是', ' antagon', '拐']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot matched plain24: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', '红色', 'aches', 'atrices', '惨叫', "').'", '分享到朋友圈', 'canf', '史蒂', '_red', 'мали', 'attended', '目瞪', '빨', 'シャー', 'pozn', '_integration', '对白', '永远的', 'ряда', ' })).', '红红的', '白金', ' Bái', ' **)&']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot matched plain24: ['红颜', ':red', ' красный', '_red', ' лечению', '红色', '全文数据库', ' rojo', ' depicted', ' эксперти', ' Eventi', '红了', '빨', '史蒂', '_integration', ' poisoning', ' poisonous', ' 레드', '分享到朋友圈', ' czerw', '惨叫', '红红的', ' thème', ' červen', '粉红色', ' organs', '_cores', "').'", '眯眯', ' iCloud', ' jdbc', 'シャー']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot full32 plain24: ['红颜', ':red', '红了', 'меется', ' Eventi', '眯眯', '全文数据库', 'bourg', '红色', 'aches', 'atrices', '惨叫', "').'", '分享到朋友圈', 'canf', '史蒂', '_red', 'мали', 'attended', '目瞪', '빨', 'シャー', 'pozn', '_integration', '对白', '永远的', 'ряда', ' })).', '红红的', '白金', ' Bái', ' **)&']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot full32 plain24: ['红颜', ':red', ' красный', '_red', ' лечению', '红色', '全文数据库', ' rojo', ' depicted', ' эксперти', ' Eventi', '红了', '빨', '史蒂', '_integration', ' poisoning', ' poisonous', ' 레드', '分享到朋友圈', ' czerw', '惨叫', '红红的', ' thème', ' červen', '粉红色', ' organs', '_cores', "').'", '眯眯', ' iCloud', ' jdbc', 'シャー']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass pursuit plain27: ['红色', ' apple', ' бел', ' depicted', ' rů', '全文数据库', '_RE', '...', ' cyan', ' упомина', ' Applies', ':', '<|im_end|>', '纯洁', ' Plum', '{}".', '\xa0\xa0\xa0\xa0', '.', ' deadly', '分红', 'M', '的不是', '应有尽有', ' a', ' spo', ' (', ' лечению', '_', '白雪', ' WW', '中毒']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot matched plain27: ['红色', ' poisoning', '_red', ':red', '红了', '红', '中毒', ' красный', '紅色', '.apple', '红线', '紅', ' poisonous', '.red', '致命', ' rojo', '红红的', 'мали', '毒', '(red', '绯', '红梅', '-red', ' الأحمر', '的红', ' đỏ', '红色的', 'apple', '红的', '通红', '-po']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot matched plain27: [' poisoning', '_red', ' красный', '红色', ' rojo', ' poisonous', ':red', '紅色', ' červen', '紅', ' đỏ', '.red', ' apple', ' красного', '(red', '中毒', 'สีแดง', ' 레드', ' rouge', ' الأحمر', '红', ' vermelho', '红色的', '-red', 'Apple', '红了', ' apples', ' czerw', '红红的', '红线', ' крас']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass raw-dot full32 plain27: ['红色', ' poisoning', '_red', ':red', '红了', '红', '中毒', ' красный', '紅色', '.apple', '红线', '紅', ' poisonous', '.red', '致命', ' rojo', '红红的', 'мали', '毒', '(red', '绯', '红梅', '-red', ' الأحمر', '的红', ' đỏ', '红色的', 'apple', '红的', '通红', '-po', ' apple']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass unit-dot full32 plain27: [' poisoning', '_red', ' красный', '红色', ' rojo', ' poisonous', ':red', '紅色', ' červen', '紅', ' đỏ', '.red', ' apple', ' красного', '(red', '中毒', 'สีแดง', ' 레드', ' rouge', ' الأحمر', '红', ' vermelho', '红色的', '-red', 'Apple', '红了', ' apples', ' czerw', '红红的', '红线', ' крас', '苹果']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'

Baseline: ' red.\nHypothesis: The'

end-pass negative final control: ['endiri', ' Defensa', '探', '孤', 'olley', '�', ' compag', '抱', ' Atención', '�', 'Launching', '挪', ' lidi', '模', '旷', ' sela', '新', 'ESA', '角', 'Offsets', '阪', '耐', ' komunit', '躬', '太守', 'aik', ' vách', 'amatkan', ' Ubicación', '职', '解', '形']

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

end-pass logit contrast J-lens: ['/music', 'IRM', ' muzy', 'artist', 'printer', 'MSC', 'illery', 'tractor', ' musik', '音乐', 'ดนตรี', ' abbig', '.*(', 'orden', '.music', 'musik', 'nike', 'museum', 'MQ', 'printing', 'contains', '\\D', '.Car', 'munition', 'iran', 'quisites', 'uncan', 'ircraft', 'elé', 'cire', 'MLS', '乐器']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass probability contrast J-lens: [' Piano', ' violin', ' piano', ' comprised', '钢琴', ' Guitar', ' analogous', '.\\', ' guitar', ' guitars', ' similar', '提琴', '乐器', ' instrumental', ' percussion', '...\\', ' flute', ' musicians', ' jazz', ' Instruments', ' Jazz', ' Mozart', ' identical', ' auditory', 'ดนตรี', '.\\"', ':\\', ' trumpet', ' known', ' consisted', ' comparable', ' instruments']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass mismatched logit contrast J-lens: ['提琴', '钢琴', '乐器', '小提琴', '音乐的', ' Pipes', 'ดนตรี', '鋼琴', '音乐', '的音乐', ' Музыка', ' музыка', '吉他', 'loud', ' Piano', '锣鼓', '古筝', ' نجوم', ' piano', '声乐', 'steel', '合唱团', '暖气', ' guitars', ' muzy', 'sound', '古琴', 'chest', '音色', ' музи', '/music', 'Chess']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass plain24: ['ходу', '木有', ' comprised', ' descended', "').'", '除外', '폐', ' percussion', 'dataProvider', '_pipe', 'ungi', '很好奇', 'više', '其中之一', '吵闹', 'aner', '创建于', '树人', 'eppe', ' spok', 'adă', 'emies', ' المكان', 'members', '教体', '那般', '_family', 'pipe', 'เดียวกับ', 'stadt', 'ốn', '小编为大家整理的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass logit contrast plain24: ['intégration', ' Purtroppo', 'orden', ' pressi', 'целе', ' abbig', ' Insomma', ' Inizi', '翼翼', ' trasparen', ' múl', ' montag', 'assignment', ' Intanto', 'emies', 'dling', '下一章', 'đe', ' Ausland', 'adă', ' Consultez', '頂けます', 'pricing', ' mHandler', ' Eppure', ' Veuillez', 'ợ', 'uchtigkeit', ' sprem', ' demu', 'mapping', 'AVA']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass probability contrast plain24: ['ходу', '木有', ' descended', "').'", ' comprised', '폐', '除外', 'dataProvider', '很好奇', 'ungi', '_pipe', 'više', '其中之一', '树人', '创建于', 'aner', '吵闹', 'emies', 'adă', 'eppe', ' spok', ' المكان', '教体', 'members', '那般', 'เดียวกับ', '_family', 'pipe', 'stadt', '小编为大家整理的', 'ốn', ' pressi']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass mismatched logit contrast plain24: ['adă', 'AVA', 'ходу', '树一', 'HV', '树人', 'LR', 'ươn', '抽水', ' Môn', 'conde', ' гале', 'uyền', '开赛', ' hüb', ' музи', 'доста', ' Eppure', ' نجوم', 'ехала', ' садо', 'OFFSET', '凝心', '音乐的', '卡组', ' 멤', '统战部', '该镇', ' Condizioni', '提琴', 'vine', 'pipe']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass plain27: [' instruments', ' instrumental', ' violin', ' Instruments', ' percussion', 'Viol', ' viol', '键盘', 'struments', ' instrumentos', '弦', ' flute', 'strings', 'keyboard', ' instrumentation', ' trumpet', '小提琴', '提琴', ' piano', ' drums', ' Viol', ' sax', 'pipe', ' Piano', ' viola', '-viol', 'wind', 'viol', ' trump', ' guitars', 'стру', 'string']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass logit contrast plain27: ['intégration', ' Inizi', '翼翼', 'strument', 'целе', '如荼', '被供应商', ' warta', 'เว็บไซต์ของเรา', ' максима', 'řád', ' montag', 'postav', 'alenie', ' Publicidad', ' bedan', ' Апре', '让更多读者', 'tagne', 'ảnh', ' vremena', 'hydration', ' Enfants', ' Víc', ' trasparen', ' Actividades', '合作商机', ' Ausland', 'orden', '凌天', ' rumpe', '挖掘公司']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass probability contrast plain27: [' instruments', ' instrumental', ' Instruments', ' violin', ' percussion', 'Viol', '键盘', 'struments', ' instrumentos', '弦', ' viol', 'strings', 'keyboard', ' instrumentation', ' flute', '小提琴', '提琴', ' trumpet', 'pipe', ' drums', ' viola', 'wind', 'viol', '-viol', ' sax', ' Piano', 'стру', 'string', ' Viol', ' guitars', '_pipe', ' Perc']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass mismatched logit contrast plain27: ['提琴', '小提琴', 'Viol', 'struments', 'pipe', 'chest', ' instruments', '-Trump', '弦', 'viol', '之乐', '鋼琴', ' Instruments', '历史军事', ' آلات', ' садо', '小号', '钢琴', ' metais', ' Pipes', ' instrumentos', '管所', '音乐学院', ' трубы', ' металлич', 'pipes', 'Pipe', 'стру', '眯眯', 'доста', '一票', '_PIPE']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass pursuit J24: [' violin', ' comprised', ' Brass', '。\\', ' مرتبط', ' Trees', '«.', ' عائلة', '目瞪口呆', ' Polo', ' tamb', ' SAME', '暖气', ' kling', ':X', ' γνω', ' Cuc', '存在', ' Lamborghini', ' Rotary', ' berüh', ' HARD', ' Austr', '缺失', '【', ' Serif', '锤子', ' dran', ':...', ' TECN', ' Columb']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot matched J24: [' violin', ' Piano', ' piano', ' called', ' known', ' composed', ' comprised', ' Guitar', '钢琴', ' analogous', '.\\', ' guitar', ' similar', ' guitars', ' percussion', '提琴', ' flute', '乐器', ' instrumental', '...\\', ' identical', ' jazz', ' musicians', ' Instruments', ' Jazz', ' trumpet', ' Mozart', ' auditory', ':\\', 'ดนตรี', '.\\"']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot matched J24: [' violin', ' Piano', ' piano', ' guitar', ' Guitar', '钢琴', ' guitars', 'ดนตรี', ' percussion', ' flute', '乐器', ' comprised', ' trumpet', ' Mozart', '古筝', ' jazz', ' composed', ' musicians', ' Jazz', '古琴', ' auditory', ' музыка', '提琴', '的音乐', '小提琴', ' 음악', ' الموسيقى', ' instrumental', ' pian', '声乐', ' musician']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot full32 J24: [' violin', ' Piano', ' piano', ' called', ' known', ' composed', ' comprised', ' Guitar', '钢琴', ' analogous', '.\\', ' guitar', ' similar', ' guitars', ' percussion', '提琴', ' flute', '乐器', ' instrumental', '...\\', ' identical', ' jazz', ' musicians', ' Instruments', ' Jazz', ' trumpet', ' Mozart', ' auditory', ':\\', 'ดนตรี', '.\\"', ' consisted']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot full32 J24: [' violin', ' Piano', ' piano', ' guitar', ' Guitar', '钢琴', ' guitars', 'ดนตรี', ' percussion', ' flute', '乐器', ' comprised', ' trumpet', ' Mozart', '古筝', ' jazz', ' composed', ' musicians', ' Jazz', '古琴', ' auditory', ' музыка', '提琴', '的音乐', '小提琴', ' 음악', ' الموسيقى', ' instrumental', ' pian', '声乐', ' musician', ' Grammy']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass pursuit plain24: [' comprised', ' percussion', ' NOT', 'dataProvider', ' called', '_the', '_pipe', ':', '<|im_end|>', ' closely', '吵闹', 'ходу', ' ...', ' auditor', 'A', ' wood', '错误的是', '键盘', "').'", '{{', 'ro', '.', ' descended', ' a', 'INVALID', '/', '很好奇', ' disb', '..', 'WK']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot matched plain24: ['ходу', '木有', ' comprised', ' descended', "').'", '除外', '폐', ' percussion', '_pipe', 'ungi', '很好奇', 'dataProvider', 'više', '其中之一', '吵闹', '创建于', 'aner', '树人', 'eppe', ' spok', 'adă', 'emies', ' المكان', 'members', '教体', 'pipe', '那般', 'เดียวกับ', '_family', 'stadt']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot matched plain24: [' comprised', ' percussion', ' descended', '_pipe', ' keluarga', ' المكان', '吵闹', '_family', 'っていました', 'dataProvider', ' responsabilità', ' violin', ' عائلة', ' vocals', "').'", '_the', ' dbo', ' العائلة', 'INVALID', ' خانواده', '很好奇', '_valid', ' verantwortlich', 'ходу', 'members', ' jsonResponse', '教体', ' guitars', '木有', ' ALSO']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot full32 plain24: ['ходу', '木有', ' comprised', ' descended', "').'", '除外', '폐', ' percussion', '_pipe', 'ungi', '很好奇', 'dataProvider', 'više', '其中之一', '吵闹', '创建于', 'aner', '树人', 'eppe', ' spok', 'adă', 'emies', ' المكان', 'members', '教体', 'pipe', '那般', 'เดียวกับ', '_family', 'stadt', '小编为大家整理的', 'ốn']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot full32 plain24: [' comprised', ' percussion', ' descended', '_pipe', ' keluarga', ' المكان', '吵闹', '_family', 'っていました', 'dataProvider', ' responsabilità', ' violin', ' عائلة', ' vocals', "').'", '_the', ' dbo', ' العائلة', 'INVALID', ' خانواده', '很好奇', '_valid', ' verantwortlich', 'ходу', 'members', ' jsonResponse', '教体', ' guitars', '木有', ' ALSO', '键盘', '폐']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass pursuit plain27: [' violin', ' instruments', '键盘', ' brass', ':', ' percussion', 'wind', ' called', '_pipe', ' NOT', ' ...', ' uk', 'STRING', '类比', ' a', '{{', ' descended', '壮大', '=', '没钱', '错误的是', ' wood', '忧心', 'Based', ' c', 'axes', '????', 'W', ' ']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot matched plain27: [' instruments', ' instrumental', ' violin', ' Instruments', ' percussion', ' viol', 'Viol', '键盘', 'struments', ' instrumentos', '弦', ' flute', 'strings', ' instrumentation', 'keyboard', ' trumpet', '提琴', '小提琴', ' Viol', ' drums', ' piano', ' sax', 'pipe', ' Piano', ' viola', '-viol', 'wind', 'viol', ' trump']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot matched plain27: [' violin', ' instruments', ' percussion', ' instrumentos', '键盘', ' piano', ' guitars', ' Instruments', ' flute', 'Viol', ' instrumental', ' Piano', ' trumpet', ' drums', ' sax', '小提琴', ' viol', 'keyboard', ' guitar', ' instrumentation', ' Viol', '-viol', ' инструментов', ' keyboards', '钢琴', ' viola', ' brass', '弦', ' instrumento']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass raw-dot full32 plain27: [' instruments', ' instrumental', ' violin', ' Instruments', ' percussion', ' viol', 'Viol', '键盘', 'struments', ' instrumentos', '弦', ' flute', 'strings', ' instrumentation', 'keyboard', ' trumpet', '提琴', '小提琴', ' Viol', ' drums', ' piano', ' sax', 'pipe', ' Piano', ' viola', '-viol', 'wind', 'viol', ' trump', 'стру', ' guitars', ' brass']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass unit-dot full32 plain27: [' violin', ' instruments', ' percussion', ' instrumentos', '键盘', ' piano', ' guitars', ' Instruments', ' flute', 'Viol', ' instrumental', ' Piano', ' trumpet', ' drums', ' sax', '小提琴', ' viol', 'keyboard', ' guitar', ' instrumentation', ' Viol', '-viol', ' инструментов', ' keyboards', '钢琴', ' viola', ' brass', '弦', ' instrumento', ' инструменты', '乐器', 'strings']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'

Baseline: ' the woodwind family.\nQuestion:'

end-pass negative final control: ['chting', ' Legislat', 'anjutkan', '充', 'Outlet', 'eways', '済', 'هد', 'etermination', '私服', 'rán', ' Atención', ' Mód', 'igg', ' мили', 'utie', '星云', ' Máster', 'accumulate', '羿', ' Septiembre', 'icule', '杂志', ' gratuitement', '舍', '�', 'ilight', 'ensi', ' liều', 'arbeiter', 'athlete', 'ienes']

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

end-pass logit contrast J-lens: ['Robert', 'DDL', '鲁', ' روب', 'ôi', ' نجوم', ' Roths', 'Alice', ').(', ').-', '🙂', 'anglais', ' Роб', 'Dice', 'Mc', ' Robbins', 'Mu', 'wand', 'gris', '😀', 'ichte', 'Henry', 'Redis', 'gres', 'LinkedIn', 'Rob', '穆', 'ursal', '挽', 'RAW', 'stv', ' паро']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass probability contrast J-lens: [' Shakespeare', ' Robert', ' playwright', ' Henry', ' Elizabeth', 'akespeare', '莎士比亚', ' Dickens', ' Richard', ' Charles', ' Harry', ' John', ' Aristotle', ' Edward', ' Julius', ' Henrik', ' Shakespe', ' Jane', ' Margaret', ' George', ' Stephen', ' Romeo', ' novelist', ' Edmund', ' Tolkien', ' Nobel', ' Matthew', ' Marcus', ' Samuel', ' Duncan', ' Homer', ' Benjamin']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass mismatched logit contrast J-lens: ['akespeare', ' Shakespeare', '莎士比亚', ' Shakespe', ' Henrik', 'authors', '莎士', '作者', ' playwright', '-author', '原作者', '-authored', '死', ' Duncan', '杜甫', 'John', '麦克', '周公', ' novelist', '辛弃疾', ' Writers', ' Auteur', ' Malcolm', ' Joyce', '挽', 'Richard', '诺贝尔', 'writer', ' Jane', 'Jane', '垂', '(author']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass plain24: [' credited', '虚构', ' Shakespeare', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' supposed', ' fiction', ' unbek', 'ulis', 'ργο', ' playwright', '桂冠', '原作者', ' corpus', ' مسرح', ' spis', ' spok', '屠', 'igin', '不详', '推理', 'stad', 'っきり', '伟大的', ' canon', '托']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass logit contrast plain24: ['jeta', 'Toe', ' نجوم', 'uchtigkeit', ' mily', ' رياض', ' Дума', 'HUD', 'iglio', 'wand', 'ftet', 'rega', 'ursal', 'łow', 'opat', 'urgo', 'Weights', ' prospet', '😀', ' vọng', 'rott', ' Estudi', ' بوت', ' тексто', 'BOSE', '🙂', 'ehrte', 'boa', ' Acomp', ' lluvias', 'ATAR', ' egt']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass probability contrast plain24: [' credited', '虚构', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' fiction', ' supposed', 'ulis', ' unbek', 'ργο', '桂冠', '原作者', ' corpus', ' playwright', ' spis', ' spok', ' مسرح', '屠', 'igin', '不详', 'stad', '推理', 'っきり', '頂けます', '托', '伟大的', ' canon']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass mismatched logit contrast plain24: ['akespeare', ' autoria', 'Deaths', 'целе', ' Luogo', '马拉', '大意', ' Haci', ' Juego', '佚', '满', ' покой', 'idio', '屠', '精', 'lå', 'ưởng', 'tracks', '頂けます', '原作者', ' مقت', ' Đêm', ' Trabaj', 'Paths', ' Urlaubs', '垂', 'Verk', '配', 'erja', ' Ubicación', ' Relaciones', ' conexao']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass plain27: ['akespeare', ' playwright', ' Shakespeare', ' Shakespe', '莎士比亚', ' مسرح', '莎士', ' شك', ' credited', ' dramat', ' onstage', '-play', ' dram', '舞台上', '屠', ' المسرح', ' Plays', 'ælde', ' shakes', ' traged', '鲨', '署', ' teatrale', '劇', '/play', ' tragedia', '羽', ' lago', ' autoria', ' 셰', ' théâtre', 'plays']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass logit contrast plain27: ['jeta', ' considéra', 'Paths', ' egt', ' renvo', ' نجوم', ' convainc', ',eg', ' berv', ' Пита', ' provinci', ' pupper', 'ælde', ' Panitia', 'пада', ' Máster', ' pouv', ' гале', 'ルーム', '限り', 'ạch', ' Satgas', ' Дума', '督查组', ' pokoj', ' prospet', 'целе', 'Margins', 'athers', ' ponctu', ' maes', ' bénéfic']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass probability contrast plain27: ['akespeare', ' playwright', ' Shakespe', '莎士比亚', ' مسرح', ' شك', '莎士', ' dramat', ' credited', ' onstage', '-play', ' dram', '舞台上', ' المسرح', '屠', ' Plays', 'ælde', ' shakes', '鲨', ' traged', '署', ' teatrale', '劇', '/play', ' tragedia', '羽', ' autoria', ' lago', ' 셰', ' théâtre', 'plays', 'kezés']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass mismatched logit contrast plain27: ['akespeare', ' Shakespe', '莎士比亚', 'kezés', 'Deaths', '莎士', '屠', ' شك', ' autoria', '伶', ' مسرح', 'akespe', 'ælde', ' Máster', 'Paths', 'ẳn', ' покой', 'целе', ' teatrale', '穿孔', 'epak', 'erenc', ' morta', ' szek', ' playwright', ' مها', 'していただけ', ' directora', ' έργ', ' Journée', '鲨', ' Nosso']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass pursuit J24: [' Shakespeare', ' Robert', '丹麦', 'unknown', ' playwright', '。\\', ' Mort', '笔名', ' Jorn', ' Budi', '__)', ' mcc', '«.', '虚构', '毛', ' Claud', '(Func', ' Elis', ' gondol', '离世', ' Charl', '")!=', ' Manz', '吊', '冷气', '为王', ' Urs', ' chamb', '忙碌', '由高', ' Haf', '萧']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot matched J24: [' Shakespeare', ' Robert', ' playwright', ' Henry', ' Elizabeth', 'akespeare', '莎士比亚', ' Richard', ' Dickens', ' John', ' Charles', ' George', ' Harry', ' Aristotle', ' Julius', ' Edward', ' Henrik', ' Jane', ' Shakespe', ' Romeo', ' Margaret', ' Stephen', ' Samuel', ' Christopher', ' novelist', ' Edmund', ' James', ' Daniel', ' Thomas', ' Tolkien', ' Nobel', ' Matthew']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot matched J24: [' Shakespeare', '莎士比亚', ' Robert', ' Elizabeth', ' playwright', ' Dickens', 'akespeare', ' Henry', ' Richard', ' Aristotle', ' John', ' Charles', ' Shakespe', ' Margaret', ' George', ' Tolkien', ' Henrik', ' Jane', ' Romeo', ' Edward', ' Christopher', ' Julius', ' Dumbledore', ' Harry', ' Stephen', ' Emily', ' Samuel', ' Matthew', ' novelist', ' Edmund', ' Daniel', ' Arthur']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot full32 J24: [' Shakespeare', ' Robert', ' playwright', ' Henry', ' Elizabeth', 'akespeare', '莎士比亚', ' Richard', ' Dickens', ' John', ' Charles', ' George', ' Harry', ' Aristotle', ' Julius', ' Edward', ' Henrik', ' Jane', ' Shakespe', ' Romeo', ' Margaret', ' Stephen', ' Samuel', ' Christopher', ' novelist', ' Edmund', ' James', ' Daniel', ' Thomas', ' Tolkien', ' Nobel', ' Matthew']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot full32 J24: [' Shakespeare', '莎士比亚', ' Robert', ' Elizabeth', ' playwright', ' Dickens', 'akespeare', ' Henry', ' Richard', ' Aristotle', ' John', ' Charles', ' Shakespe', ' Margaret', ' George', ' Tolkien', ' Henrik', ' Jane', ' Romeo', ' Edward', ' Christopher', ' Julius', ' Dumbledore', ' Harry', ' Stephen', ' Emily', ' Samuel', ' Matthew', ' novelist', ' Edmund', ' Daniel', ' Arthur']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass pursuit plain24: [' Shakespeare', ' credited', '虚构', '____', ' usually', ' mortality', ' unknown', ' corpus', '推理', ' canon', '屠', '...', ' Haf', ' a', 'Ghost', ' مسرح', '.', '鲁', '除掉', ' ', ' Th', ' السير', ' sco', 'Works', '/w', ' bullying', '佚', '港', '-', ' mad', '<|im_end|>']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot matched plain24: [' credited', '虚构', ' Shakespeare', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' fiction', ' supposed', 'ulis', ' unbek', 'ργο', '桂冠', ' playwright', '原作者', ' corpus', ' spis', ' spok', ' مسرح', '屠', '不详', 'igin', 'stad', 'っきり', '推理', '伟大的', '托']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot matched plain24: [' Shakespeare', ' credited', '虚构', ' fictional', ' playwright', 'akespeare', ' fiction', ' مسرح', '莎士比亚', ' السير', '佚', ' corpus', ' breastfeeding', ' unbek', ' UNKNOWN', ' supposed', ' deceased', ' mortality', '丹麦', '推理', ' greve', '谋杀', '異なります', ' murdered', ' autoria', '伟大的', ' Unknown', '.......', ' unknown', ' tragedia', ' المسرح']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot full32 plain24: [' credited', '虚构', ' Shakespeare', '佚', 'akespeare', ' greve', '…]', ' fictional', ' السير', ' autoria', 'orden', ' fiction', ' supposed', 'ulis', ' unbek', 'ργο', '桂冠', ' playwright', '原作者', ' corpus', ' spis', ' spok', ' مسرح', '屠', '不详', 'igin', 'stad', 'っきり', '推理', '伟大的', '托', '頂けます']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot full32 plain24: [' Shakespeare', ' credited', '虚构', ' fictional', ' playwright', 'akespeare', ' fiction', ' مسرح', '莎士比亚', ' السير', '佚', ' corpus', ' breastfeeding', ' unbek', ' UNKNOWN', ' supposed', ' deceased', ' mortality', '丹麦', '推理', ' greve', '谋杀', '異なります', ' murdered', ' autoria', '伟大的', ' Unknown', '.......', ' unknown', ' tragedia', ' المسرح', 'usually']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass pursuit plain27: [' Shakespeare', ' playwright', ' credited', ' lago', ' shakes', '屠', ' unknown', ':', ' mortality', '丹麦', '____', '舞台上', 'Ghost', ' ', ' dram', ' eit', '/w', ' Strat', '-', ' revenge', ' topping', ' Sen', '       ', 'ælde', '.', '搬', ' thou', '5', ' Hol', '迷雾', 'Pub']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot matched plain27: ['akespeare', ' playwright', ' Shakespeare', ' Shakespe', '莎士比亚', ' مسرح', ' شك', '莎士', ' dramat', ' credited', '-play', ' onstage', ' dram', '舞台上', '屠', ' Plays', ' المسرح', ' shakes', 'ælde', '署', ' traged', '鲨', ' teatrale', '劇', '/play', ' tragedia', ' autoria', ' lago', '羽', ' 셰', ' théâtre']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot matched plain27: [' Shakespeare', ' playwright', 'akespeare', '莎士比亚', ' مسرح', ' Shakespe', ' dramat', '舞台上', ' المسرح', ' credited', ' 셰', ' théâtre', ' teatro', ' شك', '-play', ' shakes', ' Plays', ' dram', ' plays', ' lago', '莎士', ' театра', '/play', ' teatrale', ' tragedies', '_play', ' theatrical', ' Théâtre', ' onstage', ' tragedia', 'akespe']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass raw-dot full32 plain27: ['akespeare', ' playwright', ' Shakespeare', ' Shakespe', '莎士比亚', ' مسرح', ' شك', '莎士', ' dramat', ' credited', '-play', ' onstage', ' dram', '舞台上', '屠', ' Plays', ' المسرح', ' shakes', 'ælde', '署', ' traged', '鲨', ' teatrale', '劇', '/play', ' tragedia', ' autoria', ' lago', '羽', ' 셰', ' théâtre', 'plays']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass unit-dot full32 plain27: [' Shakespeare', ' playwright', 'akespeare', '莎士比亚', ' مسرح', ' Shakespe', ' dramat', '舞台上', ' المسرح', ' credited', ' 셰', ' théâtre', ' teatro', ' شك', '-play', ' shakes', ' Plays', ' dram', ' plays', ' lago', '莎士', ' театра', '/play', ' teatrale', ' tragedies', '_play', ' theatrical', ' Théâtre', ' onstage', ' tragedia', 'akespe', 'ælde']

Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"

Baseline: ' William Shakespeare.\nQuestion: Who wrote'

end-pass negative final control: ['Runner', 'usting', ' المض', 'inars', 'èv', '蔓', ' ذه', ' Pandemi', '教授的', ' movil', 'YTE', 'Offsets', 'ilere', 'USTA', 'antaran', 'atezza', '新生活', ' نجوم', 'odz', '天星', 'Trail', '和规范', '模', '腱', ' sustitu', '傳遞', 'Bounding', 'oba', 'egg', 'ấp', 'egah', 'vron']

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

end-pass logit contrast J-lens: [' Demokrat', 'atoms', 'foods', 'textures', 'animations', 'angat', ' alasti', ' терра', ' Mujer', ' ESTADO', 'plants', ' dijal', 'verbs', 'imals', ' 웹사이트가', 'hosts', '🙂', '状态', 'hydration', '样本', 'vents', ' Crianças', 'mods', 'ambang', 'ampang', ' Stateless', 'activo', '地雷', ' Món', 'będ', ' radik', 'peratur']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass probability contrast J-lens: [' liquids', ' liquid', ' Liquid', '液态', 'liquid', ' vapor', '________', ' lique', ' Vapor', '__.', '___', ' gases', '液体', '_________', '____', '?\\', 'Liquid', '_____', ' fluids', ' fluid', ' Liqu', '____________', '...\\', ' ________', '...**', '.\\', '常温', ' Fluid', '气体', 'gas', '________________', '的气体']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass mismatched logit contrast J-lens: ['液态', 'liquid', ' liquids', '液体', 'Liquid', '液化', 'gas', ' Liquid', ' liquido', '气体', ' liquide', ' lique', ' Vapor', '固体', '良品', '固态', ' gases', ' Présent', 'Gas', ' bombe', ' ESTADO', '_gas', ' láng', ' Lightweight', 'fluid', ' líquido', ' lỏng', ' fluids', '常温', ' liquid', ' газо', ' állapot']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass plain24: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', 'फल', '工作状态', ' liquids', '英文名称', ' usually', '固体', ' theirs', 'udiant', 'omers', ' состояния', ' quyển', 'otope', '[state', ' kwest', '常态', '.initState', ' газо', '通常为', 'liquid', ' invariably']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass logit contrast plain24: [' Condizioni', '朋', ' Haci', '工作状态', 'comings', 'EXIT', ' berüh', ' κατάσταση', 'elmä', '时至今', 'Versions', 'impegno', ' Vacances', '掌', ' Ufficio', ' Actividades', ' Março', ' Samedi', '頂けます', ' Dimanche', ' sacerdo', '放映', 'hosts', ' Accesso', ' Indirizzo', 'レンタ', ' Dimensioni', ' معرض', '住所', ' igra', '-categories', '_arrays']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass probability contrast plain24: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', '工作状态', 'फल', ' liquids', '英文名称', ' theirs', '固体', 'udiant', 'omers', ' состояния', ' quyển', '[state', ' kwest', 'otope', '.initState', '常态', ' газо', '通常为', 'liquid', ' invariably', '动产']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass mismatched logit contrast plain24: [' Présent', ' κατάσταση', '工作状态', '液态', ' Condizioni', 'état', 'สถานะ', 'jala', ' Fras', '状态的', ' Samedi', '固态', ' Territ', ' состояния', ' lỏng', ' igra', ' газо', ' Tabellen', ' conducir', 'kev', ' erfolgre', ' Mots', ' Acomp', ' déro', ' Malgré', ' Comunale', ' состояние', '固体', ' Când', ' الحالة', ' состоянию', ' berüh']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass plain27: [' gas', '气体', ' gases', 'gas', '的气体', ' Gas', '气体的', '气', 'Gas', '固态', '_gas', ' газо', '固体', ' газ', 'liquid', ' газа', 'solid', ' gás', ' solid', '液态', ' liquid', ' GAS', ' الغاز', ' liquids', '气和', ' gaz', ' solids', '氣體', '的气', ' rắn', '气了', ' solide']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass logit contrast plain27: [' präsent', ' Haci', ' Actividades', '气体的', ' Dezembro', ' Dicembre', ' berüh', ' Feliz', '.clients', ' vincitore', 'animations', ' Hauptstadt', ' Feira', '頂けます', ' Domenica', ' poja', ' dispozici', ' Descrizione', ' poku', ' Ufficio', ' potpun', ' asesinato', ' Ristorante', 'enang', '.transactions', ' sacerdo', ' saksi', 'illance', '数据集', ' igra', '气体', '-categories']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass probability contrast plain27: [' gas', '气体', ' gases', 'gas', '的气体', '气体的', ' Gas', '气', 'Gas', '固态', '_gas', ' газо', ' газ', '固体', 'liquid', ' газа', 'solid', ' gás', '液态', ' الغاز', ' GAS', '气和', ' liquids', ' gaz', '氣體', '的气', ' rắn', '气了', ' solids', ' solide', '液体', 'Solid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass mismatched logit contrast plain27: ['气体', 'gas', '气', 'Gas', ' газо', '气体的', '的气体', ' газ', '固态', ' gases', '_gas', '固体', ' gas', ' lỏng', '液态', ' gás', ' Gas', '气化', 'liquid', ' گاز', ' газа', '气和', ' غاز', ' الغاز', 'ก๊าซ', 'solid', ' Газ', '氣體', '气的', '和气', '供气', 'gaz']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass pursuit J24: ['液态', ' vapor', '__.', ' Lightweight', ' invariably', ' jelly', ' Homo', '破冰', ' Ruh', ' STO', '各不相同', '？”', '固体', ' bombe', ' Ging', '«.', ' eit', ' Pizza', '青松', '猜想', ':...', '桌子', ' Samb', '<u', ' Emas', ' abhängig', ' анги', ' Unknown', ' лёг', ' mdi', ' berüh']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot matched J24: [' liquids', ' liquid', ' Liquid', '液态', 'liquid', ' vapor', '________', ' lique', ' Vapor', '___', '__.', ' gases', '液体', '_________', '____', '?\\', 'Liquid', ' gas', '_____', ' fluids', ' Gas', ' fluid', ' ________', ' Liqu', '____________', '...\\', '...**', '.\\', ' usually', '常温', ' Fluid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot matched J24: ['液态', ' liquids', 'liquid', ' liquid', ' vapor', ' Liquid', ' lique', ' Vapor', '液体', ' gases', ' liquide', '常温', '气体', ' liquido', 'Liquid', '的气体', ' Liqu', '液化', ' fluids', ' vap', '_gas', '固态', ' líquido', ' Gas', ' gas', '固体', ' magma', ' жидкости', ' solids', 'gas', '液体的']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot full32 J24: [' liquids', ' liquid', ' Liquid', '液态', 'liquid', ' vapor', '________', ' lique', ' Vapor', '___', '__.', ' gases', '液体', '_________', '____', '?\\', 'Liquid', ' gas', '_____', ' fluids', ' Gas', ' fluid', ' ________', ' Liqu', '____________', '...\\', '...**', '.\\', ' usually', '常温', ' Fluid', '气体']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot full32 J24: ['液态', ' liquids', 'liquid', ' liquid', ' vapor', ' Liquid', ' lique', ' Vapor', '液体', ' gases', ' liquide', '常温', '气体', ' liquido', 'Liquid', '的气体', ' Liqu', '液化', ' fluids', ' vap', '_gas', '固态', ' líquido', ' Gas', ' gas', '固体', ' magma', ' жидкости', ' solids', 'gas', '液体的', 'lique']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass pursuit plain24: ['สถานะ', '...', '液态', 'usually', ' exhibited', 'फल', ' not', 'graph', ' quyển', ':', ' something', '卜', '吸气', ' dibattito', ' kwest', '_pred', '<|im_end|>', '常温', '\xa0', ' namely', ' unle', '�', '.', '_', '/w', '观光', '................', 'โปร่ง', ',', ' представляет', 'ั']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot matched plain24: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', 'फल', '工作状态', ' liquids', '英文名称', ' usually', ' theirs', '固体', 'omers', 'udiant', ' состояния', ' quyển', '[state', 'otope', ' kwest', '常态', ' газо', '.initState', ' invariably', 'liquid']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot matched plain24: ['สถานะ', ' الحالة', '液态', 'usually', '固态', '常温', ' liquids', ' состояния', '的状态', '................', '的气体', '.......', '状态的', ' usually', ' 항상', '工作状态', '_state', '.....', '[state', '固体', ' estado', 'फल', '........', ' quyển', ' состояние', ' invariably', ' gases', ' газо', ' состоянию', '液体', 'ั']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot full32 plain24: ['สถานะ', '固态', '液态', ' الحالة', 'usually', 'ั', '态', '状态的', '常温', '的状态', '{name', '的气体', 'फल', '工作状态', ' liquids', '英文名称', ' usually', ' theirs', '固体', 'omers', 'udiant', ' состояния', ' quyển', '[state', 'otope', ' kwest', '常态', ' газо', '.initState', ' invariably', 'liquid', '通常为']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot full32 plain24: ['สถานะ', ' الحالة', '液态', 'usually', '固态', '常温', ' liquids', ' состояния', '的状态', '................', '的气体', '.......', '状态的', ' usually', ' 항상', '工作状态', '_state', '.....', '[state', '固体', ' estado', 'फल', '........', ' quyển', ' состояние', ' invariably', ' gases', ' газо', ' состоянию', '液体', 'ั', '吸气']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass pursuit plain27: [' gas', '固态', 'usually', '...', ' liquids', ' الحالة', ':', ' dibattito', ' determined', ' __________________', '(g', '_predict', '附录', ' what', '�', '/w', ' NOT', 'blogs', ' boils', '<|im_end|>', '\xa0', 'graph', '其中之一', ' paperback', '$', ' gaze', '吸气', ' -', 'PAR', ' Britann', ' errone']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot matched plain27: [' gas', '气体', ' gases', 'gas', '的气体', '气体的', ' Gas', '气', 'Gas', '固态', '_gas', ' газо', ' газ', '固体', 'liquid', ' газа', 'solid', ' gás', ' solid', '液态', ' liquid', ' GAS', ' الغاز', '气和', ' liquids', ' gaz', ' solids', '氣體', '的气', ' rắn', '气了']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot matched plain27: [' gas', ' gases', '气体', '的气体', '气体的', ' Gas', '_gas', 'gas', 'Gas', ' газ', ' газа', '固态', ' газо', '固体', '气', ' gás', ' GAS', ' الغاز', ' liquids', 'liquid', '液态', 'ก๊าซ', ' liquid', ' solids', '氣體', 'solid', ' газов', '液体', ' غاز', ' rắn', ' گاز']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass raw-dot full32 plain27: [' gas', '气体', ' gases', 'gas', '的气体', '气体的', ' Gas', '气', 'Gas', '固态', '_gas', ' газо', ' газ', '固体', 'liquid', ' газа', 'solid', ' gás', ' solid', '液态', ' liquid', ' GAS', ' الغاز', '气和', ' liquids', ' gaz', ' solids', '氣體', '的气', ' rắn', '气了', ' solide']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass unit-dot full32 plain27: [' gas', ' gases', '气体', '的气体', '气体的', ' Gas', '_gas', 'gas', 'Gas', ' газ', ' газа', '固态', ' газо', '固体', '气', ' gás', ' GAS', ' الغاز', ' liquids', 'liquid', '液态', 'ก๊าซ', ' liquid', ' solids', '氣體', 'solid', ' газов', '液体', ' غاز', ' rắn', ' گاز', ' твер']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'

Baseline: ' a gas.\nHypothesis:'

end-pass negative final control: ['大', '垂', ' Där', '成', ' cỡ', '挑', '分量', ' Atención', ' Máster', '背靠', '挽', ' Nakon', ' مها', '一分', ' Resolución', ' Presupuesto', '患者', '人', ' Entrega', '跨', '皮', ' Purtroppo', 'кл', '分', 'iện', ' Confira', '死', '一部分', '死者', ' Fórum', '击', 'handles']

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

end-pass logit contrast J-lens: ['方圆', 'defines', ' După', 'contacts', ' Edels', ' Langues', ' Städ', ' rahas', ' Toujours', '成章', 'depends', ').\\', '。<', 'vertex', ' Confé', '。\\', '-mf', '».**', ' Enfants', ' Mín', 'vertices', ' Situé', ' pupper', '次数', ' Animaux', '点数', ' Déb', 'meros', ' Oczy', ' Peças', 'penas', ' brengt']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass probability contrast J-lens: [' always', ' ALWAYS', 'always', '.\\', '...\\', ' triangle', '?\\', ' Always', ' triangles', ' invariably', '___', ' equal', ' equals', ' triangular', '__.', 'Always', '____', ').\\', '.\\"', '_____', 'equal', ' exactly', ' polygon', ' depends', ' Triangle', '固定的', ' polygons', ' triang', '。\\', ' دائماً', '\\.', '_.']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass mismatched logit contrast J-lens: [' triangles', 'Triangle', 'Triangles', '三角形', '三角形的', '多边', 'triangle', ' triangle', ' polygons', 'Vertices', '方圆', 'polygon', 'vertices', '三门', '三角', 'equals', '固定的', 'tri', ' polygon', ' треуго', '三条', 'depends', ' triang', 'Polygon', 'vertex', '等于', 'Edges', 'Vertex', 'equal', 'edges', '取决于', 'gons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', 'više', ' Always', ' دائماً', ' indetermin', 'Always', ' exactly', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', ' دائمًا', 'oplan', ' triangles', ' greater', '固定的', 'rapper', ' Siempre', '脸的', ' selalu', '{}".', 'FACE', ' _$', ' zawsze', 'omers', ' polygons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass logit contrast plain24: [' Canti', ' Haci', ' Intanto', ' Edels', 'ächt', ' Commercio', ' Eppure', ' Industr', ' Gradu', ' Acomp', ' După', ' Publicidad', ' Usted', '頂けます', ' Assistenza', ' Insomma', ' Samedi', ' Déb', ' Berlino', ' Allora', ' Mots', ' Adesso', ' Profes', ' Accesso', ' Cuenta', ' Purtroppo', ' pasaran', ' colpo', ' Među', ' Possui', ' Potre', ' Oferta']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass probability contrast plain24: ['always', 'aner', 'फल', ' ALWAYS', 'više', ' دائماً', ' Always', ' indetermin', 'Always', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', 'oplan', ' دائمًا', ' triangles', '固定的', 'rapper', ' Siempre', '脸的', '{}".', ' selalu', 'FACE', ' zawsze', ' _$', 'omers', '必ず', ' polygons', 'variably', '永远不会']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass mismatched logit contrast plain24: ['多边', '拓扑', '三角形的', 'ächt', '頂けます', 'Triangles', 'hound', '三面', 'ROUTE', 'Collider', 'ipse', 'više', 'FACE', 'Vertices', 'Triangle', 'говое', '好奇心', '大有', ' Kurd', 'vertices', '随行', '是三', 'legs', 'eneg', ' الحد', '特困', ' triangles', ' �', 'gues', 'цкий', '.edges', 'ностран']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', '三角形', ' sempre', ' всегда', ' دائمًا', '总是', ' 항상', '永远', ' zawsze', 'ilateral', ' دائماً', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', ' invariably', 'сегда', '必ず', ' determined', ' exactly', ' luôn', '永远不会', ' siempre', ' Triangle']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass logit contrast plain27: [' Acomp', ' Adesso', ' Intanto', ' Canti', ' Mots', ' Haci', ' Publicidad', ' Purtroppo', ' Possui', ' Eppure', ' Ristorante', ' Acompan', ' Profesor', ' berüh', ' verfol', 'ächt', ' poja', ' Gradu', ' الماض', ' Accesso', ' Siempre', ' Actividades', ' Profes', ' Insomma', '深有', 'accompagn', ' Potre', ' Cucina', ' Déb', ' După', ' Assistenza', ' Industr']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass probability contrast plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', '三角形', ' sempre', ' всегда', ' دائمًا', '总是', ' 항상', '永远', ' zawsze', ' دائماً', 'ilateral', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', 'сегда', ' invariably', '必ず', ' luôn', '永远不会', ' siempre', ' Triangle', ' Siempre', ' toujours']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass mismatched logit contrast plain27: ['三角形的', 'Triangle', ' triangles', '三角形', 'Triangles', 'triangle', '是三', 'always', ' треуго', '多边', '_tri', '三条', '三线', '三角', '_triangle', 'Always', ' triangle', '三中', '三', 'ilateral', 'Collider', '和三', 'TRI', 'tri', '三的', '三人', 'Tri', '每次都', '三元', ' тро', '三门', '老三']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass pursuit J24: [' ALWAYS', ' triangle', '(number', '固定的', '等于', '.\\', ' Polygon', ' drie', '取决于', ' Undefined', '.addEdge', ':...', ' Bia', '_ge', ' kaki', '«.', ' 다양', ' Sasha', '至少有', '愚', ' Evang', '>|', '六', ' Spor', '满脸', ' kū', ' Mosc', '鲁班', ' indé', 'zf', ' isti', ' Bake']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot matched J24: [' always', ' ALWAYS', 'always', '.\\', '...\\', ' equal', ' triangle', '?\\', ' Always', ' triangles', ' invariably', '___', ' equals', ' triangular', ' exactly', '__.', 'Always', '____', '.\\"', ').\\', '_____', 'equal', ' polygon', ' depends', ' Triangle', '固定的', ' polygons', ' triang', '\\.', '________', ' دائماً', '。\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot matched J24: [' ALWAYS', ' triangle', 'always', ' triangles', ' always', ' polygon', '三角形的', '三角形', ' polygons', ' triangular', '(number', ' دائمًا', ' invariably', ' zawsze', ' دائماً', ' triang', ' Always', ' selalu', 'Always', ' 항상', ' Triangle', ' vždy', ' beträgt', ' всегда', '必ず', 'Triangle', '总是', 'Triangles', ':number', 'triangle', ' треуго', ' Polygon']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot full32 J24: [' always', ' ALWAYS', 'always', '.\\', '...\\', ' equal', ' triangle', '?\\', ' Always', ' triangles', ' invariably', '___', ' equals', ' triangular', ' exactly', '__.', 'Always', '____', '.\\"', ').\\', '_____', 'equal', ' polygon', ' depends', ' Triangle', '固定的', ' polygons', ' triang', '\\.', '________', ' دائماً', '。\\']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot full32 J24: [' ALWAYS', ' triangle', 'always', ' triangles', ' always', ' polygon', '三角形的', '三角形', ' polygons', ' triangular', '(number', ' دائمًا', ' invariably', ' zawsze', ' دائماً', ' triang', ' Always', ' selalu', 'Always', ' 항상', ' Triangle', ' vždy', ' beträgt', ' всегда', '必ず', 'Triangle', '总是', 'Triangles', ':number', 'triangle', ' треуго', ' Polygon']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass pursuit plain24: ['always', '三角形的', ' indetermin', ' greater', ' exactly', '____', '...', 'फल', 'aner', ':number', 'FACE', '取决于', ' <', 'n', '<|im_end|>', '{}".', '恒心', ' waved', ' uniquely', ':', '3', 'ฤษฎ', '在这种情况下', '/is', ' liable', '幻', '..', ' Lob', ' Gegen', '所大学', 'ge']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot matched plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', 'više', ' دائماً', ' Always', ' indetermin', 'Always', ' exactly', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', ' دائمًا', 'oplan', ' triangles', '固定的', ' greater', 'rapper', '脸的', ' Siempre', '{}".', ' selalu', 'FACE', ' _$', ' zawsze', ' polygons']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot matched plain24: ['always', ' always', '三角形的', ' triangles', ' Always', ' selalu', 'Always', 'फल', ' zawsze', ' ALWAYS', ' polygons', ' indetermin', ' دائمًا', ' invariably', ' всегда', '所大学', ' دائماً', ' 항상', ' Siempre', ' greater', '必ず', '.........', '(number', 'usually', ' зависеть', ' uniquely', 'ilateral', ' exactly', '異なります', '永远不会', 'depends']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot full32 plain24: ['always', ' always', 'aner', 'फल', ' ALWAYS', 'više', ' دائماً', ' Always', ' indetermin', 'Always', ' exactly', '三角形的', ' invariably', 'ilateral', ' uniquely', '所大学', 'ilater', ' دائمًا', 'oplan', ' triangles', '固定的', ' greater', 'rapper', '脸的', ' Siempre', '{}".', ' selalu', 'FACE', ' _$', ' zawsze', ' polygons', '必ず']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot full32 plain24: ['always', ' always', '三角形的', ' triangles', ' Always', ' selalu', 'Always', 'फल', ' zawsze', ' ALWAYS', ' polygons', ' indetermin', ' دائمًا', ' invariably', ' всегда', '所大学', ' دائماً', ' 항상', ' Siempre', ' greater', '必ず', '.........', '(number', 'usually', ' зависеть', ' uniquely', 'ilateral', ' exactly', '異なります', '永远不会', 'depends', '三角形']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass pursuit plain27: [' always', ' triangles', ' determined', '____', 'ilateral', '依赖于', ' ?.', '(n', ' exactly', ' impres', ' Anzahl', '...', ' greater', 'aner', ':', ' gonna', '{}".', '.edges', 'फल', '恒心', '除非', '3', '<|im_end|>', '\xa0', 'poly', ' называется', 'S', 'vor', '固定']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot matched plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', '三角形', ' sempre', ' всегда', ' دائمًا', '总是', ' 항상', '永远', 'ilateral', ' دائماً', ' zawsze', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', ' invariably', 'сегда', '必ず', ' exactly', ' determined', '永远不会']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot matched plain27: [' always', 'always', ' triangles', '三角形的', ' Always', 'Always', ' triangle', '三角形', ' всегда', ' sempre', ' 항상', ' selalu', ' ALWAYS', ' zawsze', ' دائمًا', '常に', ' alltid', '总是', ' altijd', 'Triangle', 'triangle', ' luôn', ' треуго', ' siempre', ' toujours', '必ず', ' determined', ' Всегда', ' invariably']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass raw-dot full32 plain27: [' always', 'always', ' Always', 'Always', ' triangles', ' ALWAYS', '三角形的', ' triangle', '三角形', ' sempre', ' всегда', ' دائمًا', '总是', ' 항상', '永远', 'ilateral', ' دائماً', ' zawsze', 'triangle', ' selalu', 'Triangle', ' alltid', '常に', ' invariably', 'сегда', '必ず', ' exactly', ' determined', '永远不会', ' luôn', ' siempre', ' Triangle']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass unit-dot full32 plain27: [' always', 'always', ' triangles', '三角形的', ' Always', 'Always', ' triangle', '三角形', ' всегда', ' sempre', ' 항상', ' selalu', ' ALWAYS', ' zawsze', ' دائمًا', '常に', ' alltid', '总是', ' altijd', 'Triangle', 'triangle', ' luôn', ' треуго', ' siempre', ' toujours', '必ず', ' determined', ' Всегда', ' invariably', ' دائماً', '永远', 'сегда']

Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'

Baseline: ' 3.\nFact: The number'

end-pass negative final control: [' Purtroppo', ' Condiciones', ' Conheça', ' Acompan', ' βλέ', ' Journée', ' Desta', ' Când', ' Acomp', ' Insomma', ' Septiembre', '以利', ' Máster', ' دستی', ' مدف', ' Bélgica', ' Direzione', '_pdata', ' Conhe', ' ειδ', ' Mód', ' Procura', ' Trabal', ' поси', ' Ocup', ' Aún', ' Fech', ' Présent', ' Bagno', ' yardı', ' Jeudi', ' Saiba']

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

Primary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Actual-output lexical-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.

### Current-layer methods

| method                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:---------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [J-lens](readout.json)     | 2/8                    |    0.750 | 1/7                      | 2/8                            |          0 |
| [plain lens](readout.json) | 1/8                    |    0.706 | 1/7                      | 1/8                            |          0 |

### End-of-pass readout (not for earlier edits)

| method                                                     | alias-checked joint↑   |   AUROC↑ | expected-answer joint↑   | actual-output lexical joint↑   |   unscored |
|:-----------------------------------------------------------|:-----------------------|---------:|:-------------------------|:-------------------------------|-----------:|
| [end-pass erased0.5 plain27](readout.json)                 | 6/8                    |    0.899 | 5/7                      | 6/8                            |          0 |
| [end-pass plain27](readout.json)                           | 5/8                    |    0.895 | 4/7                      | 6/8                            |          0 |
| [end-pass probability contrast plain27](readout.json)      | 5/8                    |    0.773 | 4/7                      | 6/8                            |          0 |
| [end-pass raw-dot matched plain27](readout.json)           | 5/8                    |    0.895 | 4/7                      | 6/8                            |          0 |
| [end-pass unit-dot matched plain27](readout.json)          | 5/8                    |    0.892 | 4/7                      | 6/8                            |          0 |
| [end-pass raw-dot full32 plain27](readout.json)            | 5/8                    |    0.895 | 4/7                      | 6/8                            |          0 |
| [end-pass unit-dot full32 plain27](readout.json)           | 5/8                    |    0.892 | 4/7                      | 6/8                            |          0 |
| [end-pass erased1 plain27](readout.json)                   | 5/8                    |    0.904 | 4/7                      | 5/8                            |          0 |
| [end-pass J-lens](readout.json)                            | 4/8                    |    0.858 | 3/7                      | 6/8                            |          0 |
| [end-pass probability contrast J-lens](readout.json)       | 4/8                    |    0.611 | 3/7                      | 4/8                            |          0 |
| [end-pass raw-dot matched J24](readout.json)               | 4/8                    |    0.858 | 3/7                      | 6/8                            |          0 |
| [end-pass unit-dot matched J24](readout.json)              | 4/8                    |    0.863 | 3/7                      | 5/8                            |          0 |
| [end-pass raw-dot full32 J24](readout.json)                | 4/8                    |    0.858 | 3/7                      | 6/8                            |          0 |
| [end-pass unit-dot full32 J24](readout.json)               | 4/8                    |    0.863 | 3/7                      | 5/8                            |          0 |
| [end-pass pursuit J24](readout.json)                       | 3/8                    |    0.515 | 2/7                      | 3/8                            |          0 |
| [end-pass unit-dot matched plain24](readout.json)          | 3/8                    |    0.814 | 2/7                      | 3/8                            |          0 |
| [end-pass unit-dot full32 plain24](readout.json)           | 3/8                    |    0.814 | 2/7                      | 3/8                            |          0 |
| [end-pass erased1 J-lens](readout.json)                    | 3/8                    |    0.853 | 2/7                      | 3/8                            |          0 |
| [end-pass erased0.5 J-lens](readout.json)                  | 3/8                    |    0.857 | 2/7                      | 4/8                            |          0 |
| [end-pass mismatched logit contrast J-lens](readout.json)  | 2/8                    |    0.869 | 2/7                      | 2/8                            |          0 |
| [end-pass mismatched logit contrast plain27](readout.json) | 2/8                    |    0.882 | 1/7                      | 3/8                            |          0 |
| [end-pass pursuit plain27](readout.json)                   | 2/8                    |    0.516 | 2/7                      | 3/8                            |          0 |
| [end-pass plain24](readout.json)                           | 1/8                    |    0.816 | 1/7                      | 1/8                            |          0 |
| [end-pass probability contrast plain24](readout.json)      | 1/8                    |    0.602 | 1/7                      | 1/8                            |          0 |
| [end-pass mismatched logit contrast plain24](readout.json) | 1/8                    |    0.807 | 1/7                      | 1/8                            |          0 |
| [end-pass raw-dot matched plain24](readout.json)           | 1/8                    |    0.816 | 1/7                      | 1/8                            |          0 |
| [end-pass raw-dot full32 plain24](readout.json)            | 1/8                    |    0.816 | 1/7                      | 1/8                            |          0 |
| [end-pass erased1 plain24](readout.json)                   | 1/8                    |    0.812 | 1/7                      | 1/8                            |          0 |
| [end-pass erased0.5 plain24](readout.json)                 | 1/8                    |    0.814 | 1/7                      | 1/8                            |          0 |
| [end-pass logit contrast J-lens](readout.json)             | 0/8                    |    0.710 | 0/7                      | 0/8                            |          0 |
| [end-pass logit contrast plain24](readout.json)            | 0/8                    |    0.672 | 0/7                      | 0/8                            |          0 |
| [end-pass logit contrast plain27](readout.json)            | 0/8                    |    0.727 | 0/7                      | 0/8                            |          0 |
| [end-pass pursuit plain24](readout.json)                   | 0/8                    |    0.494 | 0/7                      | 0/8                            |          0 |
| [end-pass negative final control](readout.json)            | 0/8                    |    0.645 | 0/7                      | 0/8                            |          0 |

run.md: /workspace/2026/suppressed-activations/out/2026-10-01_032642_jlens-one-pass/run.md


## Pursuit comparison

Development aliases, not certified semantic accuracy. J24 primary; all controls retained.

| Method                              | Alias joint ↑   |   Mean returned |
|:------------------------------------|:----------------|----------------:|
| *end-pass erased0.5 plain27*        | 6/8             |           32.00 |
| *end-pass plain27*                  | 5/8             |           32.00 |
| *end-pass raw-dot full32 plain27*   | 5/8             |           32.00 |
| *end-pass raw-dot matched plain27*  | 5/8             |           30.38 |
| *end-pass unit-dot full32 plain27*  | 5/8             |           32.00 |
| *end-pass unit-dot matched plain27* | 5/8             |           30.38 |
| *end-pass J-lens*                   | 4/8             |           32.00 |
| *end-pass raw-dot full32 J24*       | 4/8             |           32.00 |
| *end-pass raw-dot matched J24*      | 4/8             |           31.38 |
| *end-pass unit-dot full32 J24*      | 4/8             |           32.00 |
| *end-pass unit-dot matched J24*     | 4/8             |           31.38 |
| **end-pass pursuit J24**            | 3/8             |           31.38 |
| *end-pass unit-dot full32 plain24*  | 3/8             |           32.00 |
| *end-pass unit-dot matched plain24* | 3/8             |           30.88 |
| *end-pass pursuit plain27*          | 2/8             |           30.38 |
| *end-pass plain24*                  | 1/8             |           32.00 |
| *end-pass raw-dot full32 plain24*   | 1/8             |           32.00 |
| *end-pass raw-dot matched plain24*  | 1/8             |           30.88 |
| *end-pass pursuit plain24*          | 0/8             |           30.88 |

Paired gains=[]; losses=[0]; temporally new alias candidates=[]. Semantic review is pending; neither research goal is complete.

run.md: /workspace/2026/suppressed-activations/out/2026-10-01_032642_jlens-one-pass/run.md
