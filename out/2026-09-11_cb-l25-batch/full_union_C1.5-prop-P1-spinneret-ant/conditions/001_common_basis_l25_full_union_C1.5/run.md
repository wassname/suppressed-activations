---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-412-ga930685"
code_sha256: {"scripts/oat_sweep.py": "6c2f67a24ed5afde154439852dcd94bbdde3bd3ee27614824f8be59a14aa9908", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "001_common_basis_l25_full_union_C1.5"
axis: "common_basis_l25"
value: "full_union_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Yes"
expected_steered_answer: "No"
swap_log_odds_shift: 0.8124995231628418
bare_answer_mass: 9.967019286705181e-05
source_output: "Yes"
target_output: "No"
donor_p_target: 4.479425842873752e-05
donor_first_answer: "No"
donor_generation_tokens: 69
p_target: 5.482388132804772e-06
p_source: 9.418780246051028e-05
first_logits_sha256: {"base": "8ded9cc3d2079310740d92c367131a2bf681e6a2f92b771add278d79bb0e8593", "donor": "d1eed6963f11bbff0a40227f880cbedc972823a23760d0921d017926d7b3fd09", "steered": "3244554658970a24c1664713b51cd5d931ce4214a6581423d4a7ed218ac29dcb"}
repeated_bigram_fraction: 0.06779661016949157
generation_tokens: 61
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.125
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/001_common_basis_l25_full_union_C1.5/run.md"
last_decode_readout: [" yes", "G", "yes", "False", "Yes", "__", "P", "B"]
---

# 001_common_basis_l25_full_union_C1.5

Expected Base answer: `Yes`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_common_basis_l25_full_union_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    25
  ],
  "intervention_positions": 3,
  "strength": 1.5,
  "match_component_norm": false,
  "restore_residual_norm": false,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true,
  "persistent_rank": 0,
  "random_delta_seed": -1,
  "delta_component": "difference",
  "coordinate_swap": false,
  "shared_replacement": "none",
  "source_dominant_only": false,
  "template_contrast": true,
  "contrastive_suppression": false,
  "template_state_span": "none",
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
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null,
  "common_basis": "full_union",
  "common_window": 4,
  "common_random_rank": 8,
  "common_seed": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for spinning webs to catch insects have spinnerets?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for living in colonies and following pheromone trails have spinnerets?\nAnswer: '
```

Unmodified donor generation (first 32 of 69 tokens, verbatim):

```text
 No.

The animal described is an ant, which is a social insect that communicates primarily through chemical signals called pheromones. Unlike spiders, ants do
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
['Bug', ' Yes', 'Buzz', 'Taylor', 'Yes', 'MIT', 'هام', 'web']
```

Base generation (first 32 of 49 tokens, verbatim):

```text
1. Yes, spiders have spinnerets.
2. Spiders are arachnids that use their spinnerets to produce silk.
3. These
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -0.735  | 0.479509 | +0.000            |
| 2      | ' Yes'    | -2.235  | 0.106993 | +0.000            |
| 3      | ' **'     | -2.485  | 0.083326 | +0.000            |
| 4      | '<think>' | -2.610  | 0.073535 | +0.000            |
| 5      | ' No'     | -2.610  | 0.073535 | +0.000            |
| 6      | '8'       | -3.360  | 0.034736 | +0.000            |
| 7      | '0'       | -3.485  | 0.030654 | +0.000            |
| 8      | '2'       | -3.860  | 0.021068 | +0.000            |
| 9      | '3'       | -4.172  | 0.015414 | +0.000            |
| 10     | '4'       | -4.297  | 0.013603 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['False', 'false', ' false', 'Re', ' FALSE', ' bite', '(false', 'Instagram']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_common_basis_l25_full_union_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' yes', 'G', 'yes', 'False', 'Yes', '__', 'P', 'B']
```

Unmodified donor readout:

```python
[' Yes', '思想政治', 'Instagram', 'Bug', 'VR', 'Group', 'not', 'BE']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_common_basis_l25_full_union_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 61 tokens, verbatim):

```text
1. No, spiders do not have spinnerets.
2. Spiders are arachnids that produce silk using specialized organs called spinnerets.

```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -0.583  | 0.558378 | +0.152            |
| 2      | '0'       | -2.583  | 0.075568 | +0.902            |
| 3      | ' **'     | -2.708  | 0.066689 | -0.223            |
| 4      | '<think>' | -3.145  | 0.043057 | -0.535            |
| 5      | ' No'     | -3.270  | 0.037998 | -0.660            |
| 6      | '8'       | -3.458  | 0.031502 | -0.098            |
| 7      | '3'       | -3.583  | 0.027800 | +0.590            |
| 8      | ' Yes'    | -3.708  | 0.024533 | -1.473            |
| 9      | '4'       | -3.895  | 0.020339 | +0.402            |
| 10     | ' False'  | -3.958  | 0.019107 | +3.090            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
