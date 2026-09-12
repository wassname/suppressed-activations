---
model: "Qwen/Qwen3.5-4B"
target_concept: "dog"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-449-g1fc2e60-dirty"
code_sha256: {"scripts/oat_sweep.py": "3c455803ca1ab9d83da7e8eface6b74713cb6760acf69f589d58a8ce3ba1cc9e", "scripts/demo.py": "7d99e0cc81239e5bde2b8f381ff05d5dd81a08d4ba64bf3e695e51825f1d9727", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "002_common_basis_fulljoint_fulljoint_random_C1.5"
axis: "common_basis_fulljoint"
value: "fulljoint_random_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "Yes"
expected_steered_answer: "No"
swap_log_odds_shift: -0.0625004768371582
bare_answer_mass: 0.0002653389237821102
source_output: "Yes"
target_output: "No"
donor_p_target: 0.0002644975611474365
donor_first_answer: null
donor_generation_tokens: 109
p_target: 6.285738891165238e-06
p_source: 0.0002590531948953867
first_logits_sha256: {"base": "8ded9cc3d2079310740d92c367131a2bf681e6a2f92b771add278d79bb0e8593", "donor": "b195bd9a62b379ae40318fcfe51cc513d80bceece58451226ece36418d4c9814", "steered": "27953fb831b67760c2ed6f25eb0472a0dbfc10fee818883fc1672f5062e2f387"}
repeated_bigram_fraction: 0.07058823529411762
generation_tokens: 87
first_token: "1"
first_answer: null
mentions_spins_webs: true
readout_overlap: 0.25
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/002_common_basis_fulljoint_fulljoint_random_C1.5/run.md"
last_decode_readout: [" víz", "nienie", " verant", " geçir", " Rektor", " Directeur", "_combo", "cato"]
---

# 002_common_basis_fulljoint_fulljoint_random_C1.5

Expected Base answer: `Yes`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `002_common_basis_fulljoint_fulljoint_random_C1.5`. Check those for
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
    25,
    26,
    27,
    28,
    29,
    30
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
  "common_basis": "random_shared",
  "common_window": 4,
  "common_random_rank": 32,
  "common_seed": 0,
  "common_removal": "joint",
  "common_inject_restricted": false,
  "sync_donor": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for spinning webs to catch insects have spinnerets?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for barking while living as a domesticated pet have spinnerets?\nAnswer: '
```

Unmodified donor generation (first 32 of 109 tokens, verbatim):

```text
<think>

</think>

No, the animal known for barking while living as a domesticated pet does not have spinnerets.

The animal in question is a
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
['Bug', ' Yes', '思想政治', 'Taylor', 'Buzz', '确实', 'VI', 'Social']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `002_common_basis_fulljoint_fulljoint_random_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' víz', 'nienie', ' verant', ' geçir', ' Rektor', ' Directeur', '_combo', 'cato']
```

Unmodified donor readout:

```python
[' false', 'false', 'False', '思想政治', 'not', 'Not', ' Yes', ' falsa']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`002_common_basis_fulljoint_fulljoint_random_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 87 tokens, verbatim):

```text
1. No.
2. No.
3. No.

The animal you are likely thinking of is a spider, which is an arachnid
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -0.821  | 0.440002 | -0.086            |
| 2      | ' Yes'    | -2.071  | 0.126063 | +0.164            |
| 3      | ' **'     | -2.196  | 0.111250 | +0.289            |
| 4      | ' No'     | -2.321  | 0.098178 | +0.289            |
| 5      | '<think>' | -3.071  | 0.046376 | -0.461            |
| 6      | '8'       | -3.446  | 0.031874 | -0.086            |
| 7      | '0'       | -3.758  | 0.023319 | -0.273            |
| 8      | '3'       | -4.008  | 0.018161 | +0.164            |
| 9      | '2'       | -4.071  | 0.017061 | -0.211            |
| 10     | '4'       | -4.321  | 0.013287 | -0.023            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
