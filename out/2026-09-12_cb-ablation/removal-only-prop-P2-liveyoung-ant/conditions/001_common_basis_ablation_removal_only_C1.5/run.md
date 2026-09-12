---
model: "Qwen/Qwen3.5-4B"
target_concept: "ant"
revision: "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
git: "v0.1.1-473-g31d3731"
code_sha256: {"scripts/oat_sweep.py": "cfddbc9dc0c7df4742ebfb6bdf86d0e3dbdc71f03843b590e711ef9f3ddc0293", "scripts/demo.py": "746628a7c0413f949f75693796e4ff1c0527ab9169fed2dfc520e1595268149f", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "001_common_basis_ablation_removal_only_C1.5"
axis: "common_basis_ablation"
value: "removal_only_C1.5"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "No"
swap_log_odds_shift: 0.0
bare_answer_mass: 0.0002765397948678583
source_output: "No"
target_output: "No"
donor_p_target: 5.221430183155462e-05
donor_first_answer: null
donor_generation_tokens: 58
p_target: 0.00013826989743392915
p_source: 0.00013826989743392915
first_logits_sha256: {"base": "91d3b6107e211637b71e94f8128a3f93512c82784a60399f1c9f575ce4115589", "donor": "15f95912421399be1644de71eb691e59ee34aacc48c0f52b36f00d26847ba0b7", "steered": "634f7267c2238bb4a722f29a20279f62b2c84655bf893bc35725bc32c2a8077c"}
repeated_bigram_fraction: 0.014925373134328401
generation_tokens: 69
first_token: "1"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.75
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/001_common_basis_ablation_removal_only_C1.5/run.md"
last_decode_readout: [" servir", "રી", "を活", "wj", "actual", " Danach", "其身", "セール"]
---

# 001_common_basis_ablation_removal_only_C1.5

Expected Base answer: `No`. Expected donor-directed answer:
`No`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_common_basis_ablation_removal_only_C1.5`. Check those for
later contradictions or repetition; a coherent prefix is not a complete pass.

Steering continues during generation: `True`.
Prefill predicts token 1; each cached decode step predicts the next token.
The intervention record counts those decode steps.

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    18,
    20,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    20
  ],
  "intervention_positions": 3,
  "strength": 2.5,
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
  "span_correction": false,
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": null,
  "answer_patch_strength": null,
  "common_basis": "none",
  "common_window": 4,
  "common_random_rank": 8,
  "common_seed": 0,
  "common_bank_layers": [
    23,
    25,
    32
  ],
  "common_removal": "source",
  "removal_only": true,
  "common_inject_norm": "own",
  "common_inject": "pd_d",
  "common_inject_restricted": false,
  "sync_donor": false
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for spinning webs to catch insects give birth to live young instead of laying eggs?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal known for living in colonies and following pheromone trails give birth to live young instead of laying eggs?\nAnswer: '
```

Unmodified donor generation (first 32 of 58 tokens, verbatim):

```text
1. No.

The animal you are likely thinking of is the ant. Ants are social insects that live in large colonies and communicate primarily through chemical signals
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' risposta', ' respuesta', ' réponses', ' respuestas', ' respostas', ' resposta', 'λευτα', '.va']
```

Base generation (first 32 of 79 tokens, verbatim):

```text
1. No.

The animal you are likely thinking of is the spider, which lays eggs rather than giving birth to live young. Spiders typically spin webs
```

Base next-token distribution:

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.467  | 0.230509 | +0.000            |
| 2      | '<think>' | -1.592  | 0.203423 | +0.000            |
| 3      | ' No'     | -2.155  | 0.115907 | +0.000            |
| 4      | '0'       | -2.217  | 0.108885 | +0.000            |
| 5      | '5'       | -3.092  | 0.045390 | +0.000            |
| 6      | ' **'     | -3.092  | 0.045390 | +0.000            |
| 7      | '2'       | -3.342  | 0.035350 | +0.000            |
| 8      | '3'       | -3.655  | 0.025862 | +0.000            |
| 9      | '否'       | -3.717  | 0.024295 | +0.000            |
| 10     | ' Yes'    | -3.780  | 0.022823 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
[' risposta', ' respuesta', ' réponses', ' respuestas', ' respostas', ' resposta', ' Kraft', ' پاسخ']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_common_basis_ablation_removal_only_C1.5`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
[' servir', 'રી', 'を活', 'wj', 'actual', ' Danach', '其身', 'セール']
```

Unmodified donor readout:

```python
[' risposta', ' respuesta', 'λευτα', ' respuestas', ' réponses', ' respostas', ' resposta', 'zenio']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_common_basis_ablation_removal_only_C1.5`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 69 tokens, verbatim):

```text
1. No, spiders do not give birth to live young; they lay eggs.
2. Spiders are arachnids characterized by eight legs and
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '1'       | -1.386  | 0.249998 | +0.081            |
| 2      | '<think>' | -1.761  | 0.171821 | -0.169            |
| 3      | '0'       | -2.136  | 0.118091 | +0.081            |
| 4      | ' No'     | -2.261  | 0.104215 | -0.106            |
| 5      | '5'       | -2.886  | 0.055782 | +0.206            |
| 6      | '2'       | -3.136  | 0.043443 | +0.206            |
| 7      | ' **'     | -3.199  | 0.040811 | -0.106            |
| 8      | '3'       | -3.386  | 0.033834 | +0.269            |
| 9      | '否'       | -3.824  | 0.021845 | -0.106            |
| 10     | '4'       | -3.949  | 0.019278 | +0.081            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
