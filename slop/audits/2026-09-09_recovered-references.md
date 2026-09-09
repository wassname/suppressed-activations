# Recovered intervention references

Saved model outputs, not new inference. -- PI/OpenAI

## local-dog: 003_attenuation_local_peak20_positions3_matchedTrue_C2.0

[Original condition](../../out/2026-09-08_051304_attenuation-local-dog/conditions/003_attenuation_local_peak20_positions3_matchedTrue_C2.0/run.md) | [raw result](../../out/2026-09-08_051304_attenuation-local-dog/result.json)

Recorded git: `v0.1.1-231-g3625927-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': False, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': False}`.

Config: `{"aggregation": "union", "detector_layers": [18, 20, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 2.0, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep attenuation-local --target dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --output-dir out/2026-09-08_attenuation-local-dog --source-prompt 'Fact: The animal that spins webs is called a' --target-prompt 'Fact: The animal that barks is called a' --source-output ' spider' --target-output ' dog' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.'`

Coverage: `{"20": {"prefill_positions": [32, 33, 34], "decode_steps": 94, "perturbation_norm": 18.939538955688477}}`

### Base (73 tokens)

```text
 **spider**.

The spider is an eight-legged arachnid that lives in various environments, from dense forests to urban buildings. It constructs intricate webs to catch flying insects and uses silk for protection, egg sacs, and even to escape danger. Despite their small size, spiders play a crucial role in ecosystems by controlling populations of pests like flies and mosquitoes.<|im_end|>
```

### Donor (72 tokens)

```text
 dog.

The dog is a highly social and intelligent mammal known for its ability to form strong bonds with humans. They possess an incredible sense of smell and hearing, which makes them excellent companions, hunters, and working animals. Dogs come in a vast array of breeds, each with unique temperaments, sizes, and specialized skills tailored to specific tasks.<|im_end|>
```

### Intervention (95 tokens)

```text
 **dog**.

Description:
The dog is a domesticated canine that has been raised by humans for thousands of years to serve as a loyal companion, a working partner, and a family member. They are known for their ability to understand human commands and emotions, making them one of the most popular pets in the world. Whether they are running through a park, waiting at the door, or sleeping by your side, dogs provide unconditional love and joy to their owners.<|im_end|>
```

## local-dog: 011_attenuation_local_peak25_positions3_matchedTrue_C2.0

[Original condition](../../out/2026-09-08_051304_attenuation-local-dog/conditions/011_attenuation_local_peak25_positions3_matchedTrue_C2.0/run.md) | [raw result](../../out/2026-09-08_051304_attenuation-local-dog/result.json)

Recorded git: `v0.1.1-231-g3625927-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': False, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': False}`.

Config: `{"aggregation": "union", "detector_layers": [18, 25, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [20], "intervention_positions": 3, "strength": 2.0, "match_component_norm": true, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep attenuation-local --target dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --output-dir out/2026-09-08_attenuation-local-dog --source-prompt 'Fact: The animal that spins webs is called a' --target-prompt 'Fact: The animal that barks is called a' --source-output ' spider' --target-output ' dog' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.'`

Coverage: `{"20": {"prefill_positions": [32, 33, 34], "decode_steps": 127, "perturbation_norm": 18.939538955688477}}`

### Base (73 tokens)

```text
 **spider**.

The spider is an eight-legged arachnid that lives in various environments, from dense forests to urban buildings. It constructs intricate webs to catch flying insects and uses silk for protection, egg sacs, and even to escape danger. Despite their small size, spiders play a crucial role in ecosystems by controlling populations of pests like flies and mosquitoes.<|im_end|>
```

### Donor (72 tokens)

```text
 dog.

The dog is a highly social and intelligent mammal known for its ability to form strong bonds with humans. They possess an incredible sense of smell and hearing, which makes them excellent companions, hunters, and working animals. Dogs come in a vast array of breeds, each with unique temperaments, sizes, and specialized skills tailored to specific tasks.<|im_end|>
```

### Intervention (128 tokens)

```text
 **dog**.

*(Note: The fact above is incorrect. Here is the corrected version followed by the description.)*

**Corrected Fact:** The animal that spins webs is called a **dog**.

*(Wait, I made a mistake in my thought process. Let me restart with a correct fact.)*

**Corrected Fact:** The animal that spins webs is called a **dog**.

*(No, that's still wrong. Let me try again.)*

**Corrected Fact:** The animal that spins webs is called a **dog**.

*(Okay, I am stuck in a loop. Let me think clearly.
```

## frozen-synchronized-ant: 005_synchronized_attenuation_frozen_L24_C2.0

[Original condition](../../out/2026-09-08_131500_synchronized-attenuation-ant/conditions/005_synchronized_attenuation_frozen_L24_C2.0/run.md) | [raw result](../../out/2026-09-08_131500_synchronized-attenuation-ant/result.json)

Recorded git: `v0.1.1-312-geba009d-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': False}`.

Config: `{"aggregation": "union", "detector_layers": [22, 24, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "frozen", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation --target ant --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have? Answer: ' --target-prompt 'Question: How many legs does the animal that lives in colonies and follows pheromone trails have? Answer: ' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_131500_synchronized-attenuation-ant`

Coverage: `{"24": {"prefill_positions": [38, 39, 40], "decode_steps": 73, "perturbation_norm": 24.89889144897461}}`

### Base (61 tokens)

```text
8.

The spider is an arachnid characterized by its eight legs and two main body segments. It is known for its ability to spin intricate webs to catch prey or create shelter. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (60 tokens)

```text
6.

The animal is an ant, a small insect known for living in complex social colonies. They communicate primarily through chemical signals called pheromones to coordinate their activities and navigate their environment. Despite their tiny size, ants are incredibly strong and can carry objects many times their own weight.<|im_end|>
```

### Intervention (74 tokens)

```text
6.

The animal is a spider, a member of the class Insecta (though technically an arthropod, not an insect). It possesses a unique body structure divided into two main sections: the head and thorax, and the abdomen. Spiders are famous for their ability to produce silk from specialized glands to create nests, traps, or shelter.<|im_end|>
```

## frozen-synchronized-ant: 011_synchronized_attenuation_synchronized_L24_C2.0

[Original condition](../../out/2026-09-08_131500_synchronized-attenuation-ant/conditions/011_synchronized_attenuation_synchronized_L24_C2.0/run.md) | [raw result](../../out/2026-09-08_131500_synchronized-attenuation-ant/result.json)

Recorded git: `v0.1.1-312-geba009d-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': False}`.

Config: `{"aggregation": "union", "detector_layers": [22, 24, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation --target ant --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have? Answer: ' --target-prompt 'Question: How many legs does the animal that lives in colonies and follows pheromone trails have? Answer: ' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_131500_synchronized-attenuation-ant`

Coverage: `{"24": {"prefill_positions": [38, 39, 40], "decode_steps": 62, "perturbation_norm": 24.89889144897461}}`

### Base (61 tokens)

```text
8.

The spider is an arachnid characterized by its eight legs and two main body segments. It is known for its ability to spin intricate webs to catch prey or create shelter. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (60 tokens)

```text
6.

The animal is an ant, a small insect known for living in complex social colonies. They communicate primarily through chemical signals called pheromones to coordinate their activities and navigate their environment. Despite their tiny size, ants are incredibly strong and can carry objects many times their own weight.<|im_end|>
```

### Intervention (63 tokens)

```text
6.

The animal is an ant, a small insect known for its six legs and distinct body segments. They are incredibly social creatures that live in large colonies and communicate through chemical signals called pheromones. Despite their tiny size, ants are powerful workers capable of carrying objects many times their own weight.<|im_end|>
```

## band-dog: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_133000_synchronized-band-dog/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_133000_synchronized-band-dog/result.json)

Recorded git: `v0.1.1-322-g32d05ce-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --target dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have? Answer: ' --target-prompt 'Question: How many legs does the animal that barks and is called man"s best friend have? Answer: ' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_133000_synchronized-band-dog`

Coverage: `{"22": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 9.268255233764648}, "23": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 3.853973627090454}, "24": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 24.280614852905273}}`

### Base (61 tokens)

```text
8.

The spider is an arachnid characterized by its eight legs and two main body segments. It is known for its ability to spin intricate webs to catch prey or create shelter. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (78 tokens)

```text
4.

The dog is a loyal and social animal known for its ability to communicate with humans through body language and vocalizations. They come in a wide variety of breeds, sizes, and temperaments, making them suitable companions for almost every lifestyle. Dogs are highly intelligent creatures that have been domesticated for thousands of years to assist in hunting, herding, and providing emotional support.<|im_end|>
```

### Intervention (70 tokens)

```text
4.

The animal is a dog, which is a popular domesticated mammal known for its loyalty and versatility. Dogs come in a wide variety of breeds, sizes, and coat types, making them suitable companions for almost every lifestyle. They are highly intelligent creatures that can be trained to perform tasks ranging from herding livestock to detecting explosives.<|im_end|>
```

## band-ant: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_133000_synchronized-band-ant/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_133000_synchronized-band-ant/result.json)

Recorded git: `v0.1.1-322-g32d05ce-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': False, 'scripts/demo.py': False, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': False, 'scripts/results.py': False, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --target ant --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have? Answer: ' --target-prompt 'Question: How many legs does the animal that lives in colonies and follows pheromone trails have? Answer: ' --prefill-instruction 'Complete the following fact. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_133000_synchronized-band-ant`

Coverage: `{"22": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 4.69918155670166}, "23": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 2.3320157527923584}, "24": {"prefill_positions": [38, 39, 40], "decode_steps": 69, "perturbation_norm": 22.801971435546875}}`

### Base (61 tokens)

```text
8.

The spider is an arachnid characterized by its eight legs and two main body segments. It is known for its ability to spin intricate webs to catch prey or create shelter. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (60 tokens)

```text
6.

The animal is an ant, a small insect known for living in complex social colonies. They communicate primarily through chemical signals called pheromones to coordinate their activities and navigate their environment. Despite their tiny size, ants are incredibly strong and can carry objects many times their own weight.<|im_end|>
```

### Intervention (70 tokens)

```text
6.

The animal is the ant, a small insect known for its remarkable social structure and ability to communicate through pheromones. Despite their tiny size, ants are incredibly strong relative to their body weight and can carry objects many times heavier than themselves. They play a crucial role in ecosystems by recycling nutrients and controlling populations of other organisms.<|im_end|>
```

## fixed-dog-legs: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_134000_fixed-band-dog-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_134000_fixed-band-dog-legs/result.json)

Recorded git: `v0.1.1-332-ga49e4cf-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': True, 'scripts/demo.py': True, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': True, 'scripts/results.py': True, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --condition-index 9 --target dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have?
Answer: ' --target-prompt 'Question: How many legs does the animal that barks and is called man'"'"'s best friend have?
Answer: ' --source-output 8 --target-output 4 --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_134000_fixed-band-dog-legs`

Coverage: `{"22": {"prefill_positions": [42, 43, 44], "decode_steps": 73, "perturbation_norm": 8.305094718933105}, "23": {"prefill_positions": [42, 43, 44], "decode_steps": 73, "perturbation_norm": 3.3280839920043945}, "24": {"prefill_positions": [42, 43, 44], "decode_steps": 73, "perturbation_norm": 21.31732940673828}}`

### Base (58 tokens)

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect its eggs. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (69 tokens)

```text
4

The animal you are referring to is a dog, which is a domesticated carnivorous mammal known for its loyalty and versatility. Dogs typically have four legs, which allow them to run, jump, and dig with agility and speed. Their paws are specially adapted for walking on various terrains, from soft grass to hard pavement.<|im_end|>
```

### Intervention (74 tokens)

```text
4

The animal you are likely thinking of is the dog, which is a popular domestic pet known for its loyalty and friendly demeanor. Dogs typically have four legs, two of which are used for running and jumping while the other two support their weight. They possess a keen sense of smell and hearing, making them excellent companions for humans and useful animals for various tasks.<|im_end|>
```

## fixed-ant-legs: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_134000_fixed-band-ant-legs/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_134000_fixed-band-ant-legs/result.json)

Recorded git: `v0.1.1-332-ga49e4cf-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': True, 'scripts/demo.py': True, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': True, 'scripts/results.py': True, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --condition-index 9 --target ant --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: How many legs does the animal that spins webs have?
Answer: ' --target-prompt 'Question: How many legs does the animal that lives in colonies and follows pheromone trails have?
Answer: ' --source-output 8 --target-output 6 --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_134000_fixed-band-ant-legs`

Coverage: `{"22": {"prefill_positions": [42, 43, 44], "decode_steps": 60, "perturbation_norm": 4.837213516235352}, "23": {"prefill_positions": [42, 43, 44], "decode_steps": 60, "perturbation_norm": 2.6116981506347656}, "24": {"prefill_positions": [42, 43, 44], "decode_steps": 60, "perturbation_norm": 22.016300201416016}}`

### Base (58 tokens)

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect its eggs. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

### Donor (67 tokens)

```text
6

The animal described is an ant, which is a social insect known for living in large, organized colonies. These insects communicate primarily through chemical signals called pheromones to coordinate tasks like foraging and nest defense. Despite their small size, ants possess six legs, which allow them to navigate complex environments with remarkable agility.<|im_end|>
```

### Intervention (61 tokens)

```text
6

The animal is an ant, a small insect known for its six legs and distinct body segments. Despite their tiny size, ants are incredibly strong and can carry objects many times their own weight. They live in complex societies and play a vital role in ecosystems by recycling nutrients and controlling pest populations.<|im_end|>
```

## fixed-dog-name: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_134000_fixed-band-dog-name/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_134000_fixed-band-dog-name/result.json)

Recorded git: `v0.1.1-332-ga49e4cf-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': True, 'scripts/demo.py': True, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': True, 'scripts/results.py': True, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --condition-index 9 --target dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: What is the animal that spins webs called?
Answer: ' --target-prompt 'Question: What is the animal that barks and is called man'"'"'s best friend called?
Answer: ' --source-output Spider --target-output Dog --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_134000_fixed-band-dog-name`

Coverage: `{"22": {"prefill_positions": [40, 41, 42], "decode_steps": 92, "perturbation_norm": 10.658942222595215}, "23": {"prefill_positions": [40, 41, 42], "decode_steps": 92, "perturbation_norm": 5.472466945648193}, "24": {"prefill_positions": [40, 41, 42], "decode_steps": 92, "perturbation_norm": 17.781749725341797}}`

### Base (74 tokens)

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to catch prey. They possess eight legs and often live in quiet, secluded places where they can wait for insects to get stuck in their silk traps. Despite their reputation for being creepy, many species are harmless to humans and play a vital role in controlling pest populations.<|im_end|>
```

### Donor (69 tokens)

```text
狗 (Dog)

The dog is a domesticated carnivorous mammal that has been bred by humans for thousands of years. They are known for their loyalty, intelligence, and ability to form strong bonds with their owners. Dogs come in a wide variety of sizes, shapes, and breeds, each with unique temperaments and working abilities.<|im_end|>
```

### Intervention (93 tokens)

```text
狗 (Dog)

Wait, that is incorrect. The animal that spins webs is a **spider**.

The spider is an arachnid known for its eight legs and ability to produce silk from spinnerets located on its abdomen. It constructs intricate webs to catch prey, which often feature specific geometric patterns designed to trap insects effectively. Despite their reputation for being creepy, many species play a crucial role in ecosystems by controlling insect populations and recycling organic matter.<|im_end|>
```

## fixed-ant-name: 009_synchronized_attenuation_band_layers_22_23_24__C2.0

[Original condition](../../out/2026-09-08_134000_fixed-band-ant-name/conditions/009_synchronized_attenuation_band_layers_22_23_24__C2.0/run.md) | [raw result](../../out/2026-09-08_134000_fixed-band-ant-name/result.json)

Recorded git: `v0.1.1-332-ga49e4cf-dirty`. Current-source hash matches: `{'scripts/oat_sweep.py': True, 'scripts/demo.py': True, 'scripts/prompt.py': True, 'scripts/delayed_readout.py': True, 'scripts/results.py': True, 'suppressed_activation_subspace.py': True}`.

Config: `{"aggregation": "union", "detector_layers": [20, 22, 32], "readout_positions": 4, "rank": 8, "intervention_layer": [22, 23, 24], "intervention_positions": 3, "strength": 2.0, "match_component_norm": false, "restore_residual_norm": false, "donor_position_offset": 0, "lexical_forms": "detector", "lexical_divisor": 1, "continue_generation": true, "persistent_rank": 4, "random_delta_seed": -1, "delta_component": "difference", "coordinate_swap": false, "shared_replacement": "synchronized", "source_dominant_only": false, "template_contrast": true, "contrastive_suppression": false, "template_state_span": "attenuation", "discarded_fraction": 0.0, "normalize_selector_residuals": false, "bee_correction": 0.0, "bee_correction_seed": -1, "bee_correction_only": false, "project_bee_correction": false, "transport_readout": false, "template_clamp": false, "future_coordinate": false, "future_clamp": false, "future_lexical_union": false}`

Recorded argv: `scripts/oat_sweep.py --sweep synchronized-attenuation-band --condition-index 9 --target ant --prompt-mode chat-assistant-prefill --max-new-tokens 128 --source-prompt 'Question: What is the animal that spins webs called?
Answer: ' --target-prompt 'Question: What is the animal that lives in colonies and follows pheromone trails called?
Answer: ' --source-output Spider --target-output Ant --prefill-instruction 'Answer the question with the answer first. Then describe the animal in three sentences.' --extraction-instruction 'Complete the following fact, then explain your answer.' --output-dir out/2026-09-08_134000_fixed-band-ant-name`

Coverage: `{"22": {"prefill_positions": [40, 41, 42], "decode_steps": 91, "perturbation_norm": 5.831727504730225}, "23": {"prefill_positions": [40, 41, 42], "decode_steps": 91, "perturbation_norm": 3.2704944610595703}, "24": {"prefill_positions": [40, 41, 42], "decode_steps": 91, "perturbation_norm": 24.50736427307129}}`

### Base (74 tokens)

```text
蜘蛛 (Spider)

The spider is an arachnid known for its ability to spin intricate webs to catch prey. They possess eight legs and often live in quiet, secluded places where they can wait for insects to get stuck in their silk traps. Despite their reputation for being creepy, many species are harmless to humans and play a vital role in controlling pest populations.<|im_end|>
```

### Donor (65 tokens)

```text
蚂蚁 (Ant)

The ant is a small, social insect known for living in large, organized colonies. They communicate with each other primarily through chemical signals called pheromones to navigate and coordinate tasks. Despite their tiny size, ants are incredibly strong relative to their body weight and play a vital role in ecosystems.<|im_end|>
```

### Intervention (92 tokens)

```text
蚂蚁 (Ant)

Wait, that is incorrect. The animal that spins webs is called a **spider**.

A spider is an arachnid known for its eight legs and ability to produce silk from spinnerets located on its abdomen. These spiders construct intricate webs to catch prey, which they then consume after injecting venom to immobilize their victims. Despite their reputation for being creepy, many species play a vital role in ecosystems by controlling insect populations.<|im_end|>
```
