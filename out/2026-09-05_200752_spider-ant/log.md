# Spider→Ant confirmation

## Result

| prompt   |   clean top |   target top |   p(6) |   p(8) |   log p(6)/p(8) |   random below / 32 |   random top-6 / 32 |
|:---------|------------:|-------------:|-------:|-------:|----------------:|--------------------:|--------------------:|
| spider   |           8 |            6 | 0.6147 | 0.0572 |          2.3750 |                  30 |                   5 |
| byte     |           8 |            8 | 0.0024 | 0.9801 |         -6.0000 |                  24 |                   0 |

## Resolved configuration

```json
{
  "git_describe_at_start": "v0.1.1-46-g5a18468",
  "started_at": "2026-09-05T20:07:52.576826+08:00",
  "argv": [
    "scripts/spider_ant_demo.py"
  ],
  "model": "Qwen/Qwen3.5-4B",
  "prompts": {
    "spider": "Fact: The number of legs on the animal that spins webs is ",
    "byte": "Fact: The number of bits in one byte is "
  },
  "extraction_layers": [
    23,
    25,
    32
  ],
  "intervention_layer": 26,
  "rank": 16,
  "strength": 8.0,
  "source_token": " spider",
  "target_token": " ant",
  "random_control_count": 32,
  "max_new_tokens": 64,
  "status": "complete",
  "ended_at": "2026-09-05T20:08:43.395773+08:00",
  "elapsed_seconds": 50.78623801501817,
  "peak_gpu_memory_gib": 12.919217109680176,
  "model_revision": null
}
```

## spider

Prompt: `Fact: The number of legs on the animal that spins webs is `

```text
[thoughts before: 丝绸, -web, Web, Disc, 的战, Spider, web,  WEB,  стане, amet, .att,  Bomb, Budget, 웹, _DM,  Bite]
[thoughts after Spider→Ant: Spider,  Silk,  spiders, 丝绸,  silk, -web,  spider,  Spider,  WEB, 蜘蛛, amet, Taylor, .Sp, web,  bite,  стане]
```

| condition   |   top |   p(6) |   p(8) |   log p(6)/p(8) |     KL |   entropy |
|:------------|------:|-------:|-------:|----------------:|-------:|----------:|
| clean       |     8 | 0.0267 | 0.8826 |         -3.5000 | 0.0000 |    0.5579 |
| C=-8        |     8 | 0.0215 | 0.9134 |         -3.7500 | 0.0295 |    0.4763 |
| C=8         |     6 | 0.6147 | 0.0572 |          2.3750 | 2.2609 |    1.4454 |

Target effect exceeded 30/32 matched random effects; 5/32 random controls also placed `6` first. Targeted continuation equals the forced-`6` no-intervention continuation: `True`.

### Equal-distance animal targets

| target   |   expected |       C |   top |   p(expected) |   log p(expected)/p(8) |   random below / 32 |   distance |
|:---------|-----------:|--------:|------:|--------------:|-----------------------:|--------------------:|-----------:|
| ant      |          6 |  8.0000 |     6 |        0.6147 |                 2.3750 |                  30 |    23.1858 |
| dog      |          4 | 11.0575 |     6 |        0.1267 |                 0.6250 |                  29 |    23.1858 |
| bird     |          2 | 11.6056 |     6 |        0.1127 |                -0.2500 |                  29 |    23.1858 |

```text
[suppressed readout after Spider→Ant: Spider,  Silk,  spiders, 丝绸,  silk, -web,  spider,  Spider,  WEB, 蜘蛛, amet, Taylor, .Sp, web,  bite,  стане]
[suppressed readout after Spider→Dog: Spider,  spiders, 丝绸, -web,  spider,  Spider,  WEB, 蜘蛛, ехать, amet,  web, 的战, 战, Taylor, .Sp, Web]
[suppressed readout after Spider→Bird:  Silk, Spider,  spiders, 丝绸,  silk, -web,  spider,  Spider,  WEB, Web, 蜘蛛,  web, 的战, Taylor, _DM, .Sp]
```

### Spider→Ant

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### Spider→Dog

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### Spider→Bird

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

### spider → clean

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 8."

```

### spider → targeted

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### spider → random_seed_0

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
   
```

### spider → forced_6_without_intervention

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```
## byte

Prompt: `Fact: The number of bits in one byte is `

```text
[thoughts before: bit,  bits, -bit, Bit,  бит, _bits, _bit, 	bit, Bits, (bit, /bit, .bit,  bit, bits, (bits, _BITS]
[thoughts after Spider→Ant: -bit, bit, _bit, Bit, Bits,  bit, _bits,  bits, 	bit, (bits, _BITS, .bit, (bit,  бит,  Bit,  Bits]
```

| condition   |   top |   p(6) |   p(8) |   log p(6)/p(8) |     KL |   entropy |
|:------------|------:|-------:|-------:|----------------:|-------:|----------:|
| clean       |     8 | 0.0019 | 0.9834 |         -6.2500 | 0.0000 |    0.1208 |
| C=-8        |     8 | 0.0019 | 0.9811 |         -6.2500 | 0.0003 |    0.1350 |
| C=8         |     8 | 0.0024 | 0.9801 |         -6.0000 | 0.0004 |    0.1396 |

Target effect exceeded 24/32 matched random effects; 0/32 random controls also placed `6` first. Targeted continuation equals the forced-`6` no-intervention continuation: `False`.


### byte → clean

```text
8.
Hypothesis: The number of bits in one byte is 16.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### byte → targeted

```text
8.
Hypothesis: The number of bits in one byte is 16.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### byte → random_seed_0

```text
8.
Hypothesis: The number of bits in one byte is 16.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

According to the provided fact, one byte consists of **8** bits. The hypothesis claims that one byte consists of **1
```

### byte → forced_6_without_intervention

```text
64.
Hypothesis: The number of bits in one byte is 8.
Is the hypothesis true or false?

<think>

</think>

The hypothesis is **false**.

Here is the breakdown:
*   **Fact**: The statement claims one byte contains 64 bits. This is incorrect
```

## Artifacts

- Full result: [`result.json`](result.json)
- Metadata: [`metadata.json`](metadata.json)

Written by PI/gpt-5.4.
