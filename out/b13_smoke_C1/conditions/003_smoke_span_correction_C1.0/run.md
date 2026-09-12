---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-342-gf00bb07"
code_sha256: {"scripts/oat_sweep.py": "01901b17a9ade112d49e60c260c8cfa723ffc6b692196cff319c1a7079baf13c", "scripts/demo.py": "9cdb417c1e1fd0963cb285c0fc9ac4f06af50d72de5680ce795697006c049b21", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "003_smoke_span_correction_C1.0"
axis: "smoke_span_correction"
value: "C1.0"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "8"
expected_steered_answer: "4"
swap_log_odds_shift: -1.0703125
bare_answer_mass: 2.7478699848870747e-06
source_output: "8"
target_output: "4"
donor_p_target: 1.0132788474948029e-07
donor_first_answer: null
donor_generation_tokens: 4
p_target: 7.465752105417778e-08
p_source: 2.6732125206763158e-06
first_logits_sha256: {"base": "e1d44deb20b41b63a96b775fe5b49c3b6ee54a31cad57ba375aff1a3b2ed29b7", "donor": "ad1ddaa92cf19379fd87c9f5ab80de32d842e77be4ad525bc67d15f87a379907", "steered": "e3b895b81f9cf389a75805ac6db183a63bc919b48b2bb4238ab7e3a11eea9ae9"}
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "атель"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
log: "conditions/003_smoke_span_correction_C1.0/run.md"
last_decode_readout: [" anc", "şim", " sağlık", " tpl", " strains", "剧烈", "胖子", " biz"]
---

# 003_smoke_span_correction_C1.0

Expected Base answer: `8`. Expected donor-directed answer:
`4`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `003_smoke_span_correction_C1.0`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    0,
    2,
    4
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    2
  ],
  "intervention_positions": 3,
  "strength": 1.0,
  "match_component_norm": true,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 4,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "none",
  "source_dominant_only": false,
  "template_contrast": true,
  "contrastive_suppression": false,
  "template_state_span": "attenuation",
  "discarded_fraction": 0.0,
  "normalize_selector_residuals": false,
  "bee_correction": 0.0,
  "bee_correction_seed": -1,
  "bee_correction_only": false,
  "project_bee_correction": false,
  "transport_readout": false,
  "template_clamp": false,
  "future_coordinate": false,
  "future_clamp": false,
  "future_lexical_union": false,
  "span_correction": true,
  "random_in_span": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that barks and is called man's best friend have?\\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
 textViewAux.market.entries
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' студент', ' arous', 'parsers', '燠', '想念', 'łam', 'Prop', '"));']
```

Base generation (first 4 of 4 tokens, verbatim):

```text
атель招募형 vets
```

Base next-token distribution:

| rank   | token        | log p   | p        | change in log p   |
|:-------|:-------------|:--------|:---------|:------------------|
| 1      | 'атель'      | -2.967  | 0.051457 | +0.000            |
| 2      | ' pie'       | -4.905  | 0.007413 | +0.000            |
| 3      | 'Thousands'  | -4.905  | 0.007413 | +0.000            |
| 4      | 'Destroyed'  | -4.967  | 0.006964 | +0.000            |
| 5      | '________'   | -5.030  | 0.006542 | +0.000            |
| 6      | ' sab'       | -5.342  | 0.004786 | +0.000            |
| 7      | ' список'    | -5.405  | 0.004496 | +0.000            |
| 8      | 'acr'        | -5.467  | 0.004224 | +0.000            |
| 9      | ' neces'     | -5.467  | 0.004224 | +0.000            |
| 10     | ' Molecular' | -5.592  | 0.003728 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['难怪', ')r', "']),", '(init', '一分', ' Bir', '_PROPERTIES', '波']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `003_smoke_span_correction_C1.0`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' anc', 'şim', ' sağlık', ' tpl', ' strains', '剧烈', '胖子', ' biz']
```

Unmodified donor readout:

```python
['悄', ' Sw', '.Matrix', '巨型', '融入', '了一场', 'izing', 'arden']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`003_smoke_span_correction_C1.0`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
атель招募형!",
```

| rank   | token       | log p   | p        | change in log p   |
|:-------|:------------|:--------|:---------|:------------------|
| 1      | 'атель'     | -3.512  | 0.029840 | -0.545            |
| 2      | ' pie'      | -4.699  | 0.009101 | +0.205            |
| 3      | 'aille'     | -4.949  | 0.007088 | +0.893            |
| 4      | 'Thousands' | -5.012  | 0.006658 | -0.107            |
| 5      | '所得税'       | -5.137  | 0.005876 | +1.830            |
| 6      | ' idea'     | -5.137  | 0.005876 | +1.580            |
| 7      | '規'         | -5.387  | 0.004576 | +0.518            |
| 8      | ' prime'    | -5.449  | 0.004299 | +0.518            |
| 9      | ' neces'    | -5.699  | 0.003348 | -0.232            |
| 10     | ' sab'      | -5.699  | 0.003348 | -0.357            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
