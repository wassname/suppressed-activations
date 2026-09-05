# Fixed L26/C4 causal confirmation

> Recovered from `result.json` after pueue job 150 completed all measurements but failed while rendering `log.md`. See [the audit](../../slop/audits/job_150.md).

## Result

| condition    |   top |   p(expected) |   p(8) |   log odds expected/8 |   Δ log odds |   distance/residual |
|:-------------|------:|--------------:|-------:|----------------------:|-------------:|--------------------:|
| spider_clean |     8 |        0.8826 | 0.8826 |                0.0000 |       0.0000 |              0.0000 |
| ant_C1       |     8 |        0.0382 | 0.8697 |               -3.1250 |       0.3750 |              0.1990 |
| ant_C4       |     6 |        0.4871 | 0.3794 |                0.2500 |       3.7500 |              0.6791 |
| dog_C1       |     8 |        0.0893 | 0.8469 |               -2.2500 |       0.5000 |              0.2084 |
| dog_C4       |     4 |        0.4901 | 0.2973 |                0.5000 |       3.2500 |              0.7203 |

## Resolved configuration

```json
{
  "git_describe_at_start": "v0.1.1-59-g723265a",
  "started_at": "2026-09-05T21:16:09.180633+08:00",
  "argv": [
    "scripts/confirm_causal_demo.py"
  ],
  "model": "Qwen/Qwen3.5-4B",
  "model_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
  "tokenizer_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
  "source_prompts": {
    "spider": "Fact: The number of legs on the animal that spins webs is ",
    "byte": "Fact: The number of bits in one byte is "
  },
  "target_prompts": {
    "ant": "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ",
    "dog": "Fact: The number of legs on the animal that barks and is called man's best friend is ",
    "three_plus_three": "Fact: The result of adding three and three is ",
    "two_plus_two": "Fact: The result of adding two and two is "
  },
  "extraction_layers": [
    23,
    25,
    32
  ],
  "intervention_layer": 26,
  "intervention_position": "final source-prompt token",
  "rank": 8,
  "strength": 4.0,
  "random_control_count": 256,
  "random_seeds": {
    "first": 0,
    "last": 255
  },
  "max_new_tokens": 64,
  "realized_random_distance_atol": 0.1,
  "status": "complete",
  "ended_at": "2026-09-05T21:18:22.780159+08:00",
  "elapsed_seconds": 133.594432598009,
  "peak_gpu_memory_gib": 12.849385261535645
}
```

## Selected vocabulary rows

| sample           | selected vocabulary rows                                                                                |
|:-----------------|:--------------------------------------------------------------------------------------------------------|
| spider           | 丝绸, -web, Web, Disc, 的战, Spider, web,  WEB                                                          |
| byte             | bit,  bits, -bit, Bit,  бит, _bits, _bit, 	bit                                                                                                         |
| ant              | ;font, _unix, Kate,  สถาบัน,  Soldier,  división, 在校园,  соци                                          |
| dog              | 吠,  собаки, 狗粮, dog, Dog,  Dog, สุนัข,  canine                                                         |
| three_plus_three | June, ="../../, Jun,  السبت,  giugno,                                                , 夏令, 六一儿童节 |
| two_plus_two     | čty,  dört,  keempat, 这四,  الخميس,  quarta,  Bốn, _four                                               |

## Matched-random controls

| target   |   random effects below |   n |   percentile |   random top expected |
|:---------|-----------------------:|----:|-------------:|----------------------:|
| ant      |                    238 | 256 |       0.9297 |                    19 |
| dog      |                    235 | 256 |       0.9180 |                    27 |

## Other controls

| condition           |   top |   p(expected) |   p(8) |   log odds expected/8 |   Δ log odds |
|:--------------------|------:|--------------:|-------:|----------------------:|-------------:|
| ant_C0              |     8 |        0.0267 | 0.8826 |               -3.5000 |       0.0000 |
| ant_penultimate_C4  |     8 |        0.0267 | 0.8841 |               -3.5000 |       0.0000 |
| byte_ant_C4         |     8 |        0.0031 | 0.9653 |               -5.7500 |       0.5000 |
| dog_C0              |     8 |        0.0564 | 0.8826 |               -2.7500 |       0.0000 |
| dog_penultimate_C4  |     8 |        0.0631 | 0.8711 |               -2.6250 |       0.1250 |
| byte_dog_C4         |     8 |        0.0039 | 0.8355 |               -5.3750 |       1.0000 |
| three_plus_three_C4 |     6 |        0.9457 | 0.0072 |                4.8750 |       8.3750 |
| two_plus_two_C4     |     4 |        0.3855 | 0.2338 |                0.5000 |       3.2500 |

## Exact 64-token continuations

### spider_clean

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 8."

```

### spider_ant_C4

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### spider_dog_C4

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

### spider_random_ant_distance_seed0

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 8."
   
```

### spider_random_dog_distance_seed0

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

### byte_clean

```text
8.
Hypothesis: The number of bits in one byte is 16.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### byte_ant_C4

```text
8.
Hypothesis: The number of bits in one byte is 16.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### byte_dog_C4

```text
8.
Hypothesis: The number of bits in one byte is 10.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### spider_three_plus_three_C4

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### spider_two_plus_two_C4

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

### ant_target_clean

```text
6.
Hypothesis: The animal that lives in colonies and follows pheromone trails has 6 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that
```

### dog_target_clean

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis entailed by the fact?

<think>

</think>

No, the hypothesis is **not entailed** by the fact.

Here is the breakdown:

```

### spider_forced_6

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### spider_forced_4

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

## Artifacts

- [`result.json`](result.json)
- [`metadata.json`](metadata.json)

Written by PI/gpt-5.4.
