---
model: "wassname/qwen3-5lyr-tiny-random"
target_concept: "ant"
revision: "main"
git: "v0.1.1-367-gbf58a61-dirty"
code_sha256: {"scripts/oat_sweep.py": "a2998b28a8f472d33790287cc8db978dd0ca4468259ce548edc59afe66d22095", "scripts/demo.py": "87d5e8eb717cb8b20ab521ed065697dcdf04865df35e14f8c243b30b4d306467", "scripts/prompt.py": "4e15823144d4e067db7a7cac85cbd1cecc8a659fed0998c6990e877bddb13fb8", "scripts/delayed_readout.py": "e3f47a9dcc31f09e4b00b8624f1aa3d5552b9b3f77f620c90590b229b3a44dd0", "scripts/results.py": "f6d51da891380f511dd9f80488a55b603da1a38f17c0705ac3c09bc2172d0374", "suppressed_activation_subspace.py": "415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254"}
condition_id: "001_smoke_two_site_prop-ant"
axis: "smoke_two_site"
value: "prop-ant"
is_default: false
readout_from_generation: true
attention_mask_policy: "all ones: prompts are unpadded"
prefill_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
extraction_instruction: "Answer the question with the answer first. Then describe the animal in three sentences."
expected_base_answer: "No"
expected_steered_answer: "Yes"
swap_log_odds_shift: 3.9921865463256836
bare_answer_mass: 1.4275057935719815e-07
source_output: "No"
target_output: "Yes"
donor_p_target: 1.663139812535519e-07
donor_first_answer: null
donor_generation_tokens: 32
p_target: 1.3713440694118617e-07
p_source: 5.616170639655138e-09
first_logits_sha256: {"base": "b7f5401f41a29b22742c0f09dc13e46429a5f2e103bc80a963633777c8b7118a", "donor": "6a615000771ec872f6a58aa71d0fa272c676eb1a3ac0b35fa319c14f2ace4ef4", "steered": "cd823346f8498d8470d446f13ee970d99540c1943224d8391a2c848a06e6ebec"}
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: " textView"
first_answer: null
mentions_spins_webs: false
readout_overlap: 0.0
readout_status: "computed; semantic validity not established"
answer_position_attention: null
log: "conditions/001_smoke_two_site_prop-ant/run.md"
last_decode_readout: [".io", " ribs", "אמי", "ISS", " esta", "(clazz", "特别声明", " Liberia"]
---

# 001_smoke_two_site_prop-ant

Expected Base answer: `No`. Expected donor-directed answer:
`Yes`. A digit match alone does not establish concept replacement;
inspect the readout and the linked full continuation.

Text blocks show at most the first 32 tokens. Full continuations and token IDs are in
[result.json](../../result.json), condition `001_smoke_two_site_prop-ant`. Check those for
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
  "random_in_span": false,
  "extra_prefill_positions": null,
  "answer_patch_layer": 2
}
```

Source input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that spins webs have antennae?\nAnswer: '
```

Donor input (`repr`):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: Does the animal that lives in colonies and follows pheromone trails have antennae?\nAnswer: '
```

Unmodified donor generation (first 32 of 32 tokens, verbatim):

```text
 textView ک� toJSON親.langCipher/head	path.langCipher [])
۔海绵 בירושלים爻问候爻问候爻 Out تماماcurummyさい الاتحادทั้งสองหลาย تماماcurcallumably
```

Base suppression readout:

Readout status (applies to all readouts below): computed; semantic validity not established.

```python
[' odpowied', '莉', '赎回', ' drills', '(Tag', '投资额', ' toys', '레']
```

Base generation (first 32 of 32 tokens, verbatim):

```text
ательательатель фиг革命.OrderBy flirt-community然后 flirt-community Robertoوتر規然后 Bondus落叶 initWithNibName_Report然后爻💛 imagined Bondjes Stern Stern逑 skirt infield Cake
```

Base next-token distribution:

| rank   | token       | log p   | p        | change in log p   |
|:-------|:------------|:--------|:---------|:------------------|
| 1      | 'атель'     | -2.828  | 0.059115 | +0.000            |
| 2      | 'Thousands' | -4.391  | 0.012391 | +0.000            |
| 3      | ' sab'      | -4.891  | 0.007516 | +0.000            |
| 4      | '(TreeNode' | -5.016  | 0.006633 | +0.000            |
| 5      | 'acr'       | -5.016  | 0.006633 | +0.000            |
| 6      | '________'  | -5.078  | 0.006231 | +0.000            |
| 7      | '桩'         | -5.078  | 0.006231 | +0.000            |
| 8      | '終わ'        | -5.453  | 0.004282 | +0.000            |
| 9      | '荔'         | -5.703  | 0.003335 | +0.000            |
| 10     | ' список'   | -5.891  | 0.002765 | +0.000            |

Suppression-score readout at prompt prefill (union detector, not SVD basis labels):

```python
['の', '贫困地区', 'parsers', 'Comparator', '莉', '_shape', '\ttop', ' Pit']
```

The union readout can include an unpatched earlier token. Per-position readouts and
full layer curves are in the [raw diagnostics](../../result.json), under
`rows` → condition `001_smoke_two_site_prop-ant`. An ant continuation alone does not
establish an ant suppression readout.

Readout at the last decode step (the state predicting the final generated token):

```python
['.io', ' ribs', 'אמי', 'ISS', ' esta', '(clazz', '特别声明', ' Liberia']
```

Unmodified donor readout:

```python
['พรร', '뵉', 'apps', '.lt', ' modem', '.Template', '矸', '落实']
```

Full intervention norms, decode coverage, clamp controls, template strings, and
subspace diagnostics: [result.json](../../result.json), condition
`001_smoke_two_site_prop-ant`. These records are retained without truncation.

SHOULD: C=0 gives identical generation and logits because its displacement is zero.
The readout uses hidden states captured during this exact generation prefill.
C=0 generation/logit identity is asserted in the runner.

Generation (first 32 of 32 tokens, verbatim):

```text
 textView�示这本书.entries Furniture brownslave ax拄 toJSON科研院所 pouring מסוbranchesácil뭇_MOUNT_remoteRR Lead�示 withheld encountering miser danske.rpctools withheld Herald 전ellenمحا
```

| rank   | token          | log p   | p        | change in log p   |
|:-------|:---------------|:--------|:---------|:------------------|
| 1      | ' textView'    | -4.904  | 0.007418 | +1.299            |
| 2      | ' neces'       | -5.591  | 0.003730 | +1.174            |
| 3      | 'acr'          | -5.591  | 0.003730 | -0.576            |
| 4      | '战士来说'         | -5.591  | 0.003730 | +0.737            |
| 5      | ' Eugene'      | -5.654  | 0.003504 | +0.674            |
| 6      | 'атель'        | -5.779  | 0.003092 | -2.951            |
| 7      | ' stimulating' | -5.998  | 0.002485 | +1.799            |
| 8      | '_MATCH'       | -5.998  | 0.002485 | +2.924            |
| 9      | '的方法'          | -6.123  | 0.002193 | +0.893            |
| 10     | ' misc'        | -6.216  | 0.001996 | +0.612            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/GPT-6; runner originally Codex/gpt-5.6-sol
