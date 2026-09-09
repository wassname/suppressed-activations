---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "dog"
revision: "main"
git: "v0.1.1-332-ga49e4cf-dirty"
code_sha256: {"scripts/oat_sweep.py": "82a109fc1db2b02e84896a486f65dda448dce293140ee1852b8c47ac10128cbb", "scripts/demo.py": "3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "000_smoke_detector_D0_2_4_matchedFalse"
axis: "smoke_detector"
value: "D0_2_4_matchedFalse"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Spider"
expected_steered_answer: "Dog"
swap_log_odds_shift: 2.80126953125
bare_answer_mass: 2.161749762308318e-06
source_output: "Spider"
target_output: "Dog"
donor_p_target: 1.4115861404206953e-06
donor_first_answer: null
donor_generation_tokens: 4
p_target: 1.3153766076356987e-06
p_source: 8.463731546726194e-07
first_logits_sha256: {"base": "fa3285391491651c1057d4cd10e3841dfcbdb16ff592ca47e44ef185c1262dd6", "donor": "01f41e4585b5938a3e38d230b5b401bec8b8e6596e264b380e1a9f26c2ec3b58", "steered": "79ef9dfcb075c3db72b450cd57c042d1c48b3a87953a4a0a3cfcdeb8b4879fa8"}
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "acula"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
log: "conditions/000_smoke_detector_D0_2_4_matchedFalse/run.md"
last_decode_readout: ["=\"//", " doors", " realpath", "�", "tyard", ".mock", "(init", "_APP"]
---

# 000_smoke_detector_D0_2_4_matchedFalse

Expected Base answer: `Spider`. Expected donor-directed answer:
`Dog`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `000_smoke_detector_D0_2_4_matchedFalse`. Check those for
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
  "strength": 2.0,
  "match_component_norm": false,
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
  "template_state_span": "peak",
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
  "future_lexical_union": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that spins webs called?\nAnswer: '
```

Donor input (`repr`):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: What is the animal that barks and is called man's best friend called?\nAnswer: "
```

Unmodified donor generation (first 4 of 4 tokens, verbatim):

```text
_CHARellery BAL"In
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['.Matrix', ' студент', 'apps', '$id', 'พรร', '查找', ' DEN', '悄']
```

Base generation (first 4 of 4 tokens, verbatim):

```text
acked �Annotationsaced
```

Base next-token distribution:

| rank   | token          | log p   | p        | change in log p   |
|:-------|:---------------|:--------|:---------|:------------------|
| 1      | 'acked'        | -5.355  | 0.004724 | +0.000            |
| 2      | '滹'            | -5.418  | 0.004438 | +0.000            |
| 3      | ' stimulating' | -5.730  | 0.003247 | +0.000            |
| 4      | '战士来说'         | -5.730  | 0.003247 | +0.000            |
| 5      | 'ではなく'         | -5.918  | 0.002692 | +0.000            |
| 6      | ' textView'    | -5.918  | 0.002692 | +0.000            |
| 7      | ' samt'        | -5.980  | 0.002529 | +0.000            |
| 8      | 'dirname'      | -6.043  | 0.002376 | +0.000            |
| 9      | ' קיש'         | -6.043  | 0.002376 | +0.000            |
| 10     | 'Fit'          | -6.043  | 0.002376 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['ues', ' Madagascar', 'apps', 'ży', 'พรร', ')r', '둥', 'exas']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `000_smoke_detector_D0_2_4_matchedFalse`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['="//', ' doors', ' realpath', '�', 'tyard', '.mock', '(init', '_APP']
```

Unmodified donor readout:

```python
['ᴴ', ' Braz', '悄', 'uctor', '了一场', 'arms', '.Matrix', ' Phantom']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`000_smoke_detector_D0_2_4_matchedFalse`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 4 of 4 tokens, verbatim):

```text
acula拄犟ᵛ
```

| rank   | token         | log p   | p        | change in log p   |
|:-------|:--------------|:--------|:---------|:------------------|
| 1      | 'acula'       | -5.998  | 0.002484 | +4.216            |
| 2      | ' طويلة'      | -6.092  | 0.002262 | +2.982            |
| 3      | '_MATCH'      | -6.154  | 0.002125 | +0.888            |
| 4      | ' ordinarily' | -6.217  | 0.001996 | +2.638            |
| 5      | ' backpage'   | -6.498  | 0.001507 | +7.154            |
| 6      | 'umor'        | -6.592  | 0.001372 | +2.420            |
| 7      | ' idea'       | -6.592  | 0.001372 | +1.607            |
| 8      | ',’’'         | -6.717  | 0.001211 | +1.701            |
| 9      | '龅'           | -6.717  | 0.001211 | +1.888            |
| 10     | 'change'      | -6.810  | 0.001102 | +3.435            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
