# Spider→Ant confirmation

## Result

| prompt   |   clean top |   target top |   p(6) |   p(8) |   log p(6)/p(8) |   random below / 32 |   random top-6 / 32 |
|:---------|------------:|-------------:|-------:|-------:|----------------:|--------------------:|--------------------:|
| spider   |           8 |            6 | 0.6147 | 0.0572 |          2.3750 |                  30 |                   5 |
| byte     |           8 |            8 | 0.0024 | 0.9801 |         -6.0000 |                  24 |                   0 |

## Resolved configuration

```json
{
  "git_describe_at_start": "v0.1.1-50-gd8991f7",
  "started_at": "2026-09-05T20:24:43.595642+08:00",
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
  "ended_at": "2026-09-05T20:25:32.308281+08:00",
  "elapsed_seconds": 48.65907887299545,
  "peak_gpu_memory_gib": 12.921067237854004,
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

### C=1 swap endpoint

| target   |   expected |   C=1 top |   p(2) |   p(4) |   p(6) |   p(8) |   distance |
|:---------|-----------:|----------:|-------:|-------:|-------:|-------:|-----------:|
| ant      |          6 |         8 | 0.0093 | 0.0881 | 0.0367 | 0.8355 |     3.9999 |
| dog      |          4 |         8 | 0.0081 | 0.0991 | 0.0322 | 0.8301 |     2.9664 |
| bird     |          2 |         8 | 0.0074 | 0.0797 | 0.0293 | 0.8570 |     2.8354 |

### Components of the C=1 operation

| pair   | swap component   |   Δp(2) |   Δp(4) |   Δp(6) |   Δp(8) |   distance |
|:-------|:-----------------|--------:|--------:|--------:|--------:|-----------:|
| ant    | source           | +0.0018 | +0.0069 | -0.0003 | -0.0089 |    +3.6789 |
| ant    | target           | +0.0006 | +0.0135 | +0.0157 | -0.0312 |    +3.6390 |
| dog    | source           | +0.0008 | +0.0069 | -0.0003 | -0.0088 |    +2.6385 |
| dog    | target           | -0.0002 | +0.0229 | +0.0064 | -0.0301 |    +2.6148 |
| bird   | source           | +0.0018 | +0.0068 | -0.0003 | -0.0098 |    +3.1555 |
| bird   | target           | +0.0007 | +0.0141 | +0.0067 | -0.0233 |    +3.1113 |

### Equal-distance animal extrapolations

| target   |   expected |       C | top     |   p(expected) |   log p(expected)/p(8) |   random below / 32 |   distance |
|:---------|-----------:|--------:|:--------|--------------:|-----------------------:|--------------------:|-----------:|
| ant      |          6 |  8.0000 | 6       |        0.6147 |                 2.3750 |                  30 |    23.1858 |
| dog      |          4 | 11.0575 | 6       |        0.1267 |                 0.6250 |                  29 |    23.1858 |
| bird     |          2 | 11.6056 | 4/6 tie |        0.1127 |                -0.2500 |                  29 |    23.1858 |

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
