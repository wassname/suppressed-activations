# Spider→Ant confirmation

## Result

| prompt   |   clean top |   target top |   p(6) |   p(8) |   log p(6)/p(8) |   random below / 32 |   random top-6 / 32 |
|:---------|------------:|-------------:|-------:|-------:|----------------:|--------------------:|--------------------:|
| spider   |           8 |            6 | 0.6147 | 0.0572 |          2.3750 |                  30 |                   5 |
| byte     |           8 |            8 | 0.0024 | 0.9801 |         -6.0000 |                  24 |                   0 |

## Resolved configuration

```json
{
  "git_describe_at_start": "v0.1.1-57-g46c007a",
  "started_at": "2026-09-05T20:53:47.070674+08:00",
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
  "target_leg_strengths": [
    1.0,
    2.0,
    4.0,
    8.0,
    12.0
  ],
  "sample_rank": 8,
  "sample_layers": [
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30
  ],
  "sample_strengths": [
    1.0,
    2.0,
    4.0,
    8.0
  ],
  "random_control_count": 32,
  "max_new_tokens": 64,
  "status": "complete",
  "ended_at": "2026-09-05T20:54:48.677691+08:00",
  "elapsed_seconds": 61.6017024180037,
  "peak_gpu_memory_gib": 12.970771789550781,
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

### Separately norm-restored sides of the C=1 operation

| pair   | swap component   |   Δp(2) |   Δp(4) |   Δp(6) |   Δp(8) |   distance |
|:-------|:-----------------|--------:|--------:|--------:|--------:|-----------:|
| ant    | source           | +0.0018 | +0.0069 | -0.0003 | -0.0089 |    +3.6789 |
| ant    | target           | +0.0006 | +0.0135 | +0.0157 | -0.0312 |    +3.6390 |
| dog    | source           | +0.0008 | +0.0069 | -0.0003 | -0.0088 |    +2.6385 |
| dog    | target           | -0.0002 | +0.0229 | +0.0064 | -0.0301 |    +2.6148 |
| bird   | source           | +0.0018 | +0.0068 | -0.0003 | -0.0098 |    +3.1555 |
| bird   | target           | +0.0007 | +0.0141 | +0.0067 | -0.0233 |    +3.1113 |

### Target-coordinate dose sweep

| target   |   target C |   top |   p(2) |   p(4) |   p(6) |   p(8) |   distance |
|:---------|-----------:|------:|-------:|-------:|-------:|-------:|-----------:|
| ant      |     1.0000 |     8 | 0.0074 | 0.0699 | 0.0424 | 0.8514 |     3.6390 |
| ant      |     2.0000 |     8 | 0.0079 | 0.0846 | 0.0747 | 0.8029 |     7.1057 |
| ant      |     4.0000 |     8 | 0.0138 | 0.0794 | 0.2772 | 0.5868 |    13.0971 |
| ant      |     8.0000 |     6 | 0.0744 | 0.0352 | 0.4284 | 0.2944 |    20.9721 |
| ant      |    12.0000 |     1 | 0.0979 | 0.0075 | 0.1424 | 0.1516 |    25.2138 |
| dog      |     1.0000 |     8 | 0.0065 | 0.0793 | 0.0331 | 0.8525 |     2.6148 |
| dog      |     2.0000 |     8 | 0.0071 | 0.0985 | 0.0411 | 0.8247 |     5.1524 |
| dog      |     4.0000 |     8 | 0.0114 | 0.1785 | 0.0657 | 0.7058 |     9.8081 |
| dog      |     8.0000 |     8 | 0.0429 | 0.2467 | 0.1496 | 0.4609 |    16.9334 |
| dog      |    12.0000 |     8 | 0.1292 | 0.1464 | 0.1659 | 0.3099 |    21.5125 |
| bird     |     1.0000 |     8 | 0.0074 | 0.0705 | 0.0333 | 0.8593 |     3.1113 |
| bird     |     2.0000 |     8 | 0.0074 | 0.0698 | 0.0423 | 0.8502 |     6.0870 |
| bird     |     4.0000 |     8 | 0.0129 | 0.0840 | 0.0654 | 0.7969 |    11.3584 |
| bird     |     8.0000 |     8 | 0.0538 | 0.0690 | 0.1290 | 0.6550 |    18.7942 |
| bird     |    12.0000 |     8 | 0.1589 | 0.0402 | 0.1801 | 0.3364 |    23.1526 |

### Ant target component, C=8

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

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

### Rank-8 single-site sample-component screen

```text
[ant target readout: ;font, _unix, Kate,  สถาบัน,  Soldier,  división, 在校园,  соци]
[dog target readout: 吠,  собаки, 狗粮, dog, Dog,  Dog, สุนัข,  canine]
```

| target sample   |   target clean |   layer |      C | source top   |   p(2) |   p(4) |   p(6) |   p(8) |   distance |
|:----------------|---------------:|--------:|-------:|:-------------|-------:|-------:|-------:|-------:|-----------:|
| ant             |              6 |      23 | 1.0000 | 8            | 0.0068 | 0.0442 | 0.0345 | 0.8885 |     2.3775 |
| ant             |              6 |      23 | 2.0000 | 8            | 0.0074 | 0.0427 | 0.0622 | 0.8583 |     4.7090 |
| ant             |              6 |      23 | 4.0000 | 8            | 0.0092 | 0.0282 | 0.2084 | 0.7273 |     9.0040 |
| ant             |              6 |      23 | 8.0000 | 6            | 0.0143 | 0.0209 | 0.7829 | 0.1542 |    15.4450 |
| ant             |              6 |      24 | 1.0000 | 8            | 0.0077 | 0.0344 | 0.0442 | 0.8874 |     5.1441 |
| ant             |              6 |      24 | 2.0000 | 8            | 0.0101 | 0.0215 | 0.2307 | 0.7106 |     9.9222 |
| ant             |              6 |      24 | 4.0000 | 6            | 0.0303 | 0.0126 | 0.8859 | 0.0268 |    17.2965 |
| ant             |              6 |      24 | 8.0000 | 6            | 0.0920 | 0.0205 | 0.7705 | 0.0299 |    24.8439 |
| ant             |              6 |      25 | 1.0000 | 8            | 0.0097 | 0.0557 | 0.0338 | 0.8717 |     6.2826 |
| ant             |              6 |      25 | 2.0000 | 8            | 0.0158 | 0.0627 | 0.1171 | 0.7636 |    11.9374 |
| ant             |              6 |      25 | 4.0000 | 6            | 0.0450 | 0.0578 | 0.7038 | 0.0578 |    20.0316 |
| ant             |              6 |      25 | 8.0000 | 6            | 0.0338 | 0.0491 | 0.5986 | 0.1040 |    27.4471 |
| ant             |              6 |      26 | 1.0000 | 8            | 0.0075 | 0.0556 | 0.0382 | 0.8697 |     5.0475 |
| ant             |              6 |      26 | 2.0000 | 8            | 0.0093 | 0.0470 | 0.0775 | 0.8332 |     9.7565 |
| ant             |              6 |      26 | 4.0000 | 6            | 0.0189 | 0.0453 | 0.4871 | 0.3794 |    17.2234 |
| ant             |              6 |      26 | 8.0000 | 6            | 0.0228 | 0.0426 | 0.7548 | 0.0702 |    25.3131 |
| ant             |              6 |      27 | 1.0000 | 8            | 0.0067 | 0.0440 | 0.0388 | 0.8840 |     4.3863 |
| ant             |              6 |      27 | 2.0000 | 8            | 0.0067 | 0.0341 | 0.0562 | 0.8787 |     8.5941 |
| ant             |              6 |      27 | 4.0000 | 8            | 0.0103 | 0.0318 | 0.1109 | 0.8194 |    15.8629 |
| ant             |              6 |      27 | 8.0000 | 8            | 0.0349 | 0.0396 | 0.2582 | 0.6193 |    25.2263 |
| ant             |              6 |      28 | 1.0000 | 8            | 0.0076 | 0.0562 | 0.0301 | 0.8787 |     5.3030 |
| ant             |              6 |      28 | 2.0000 | 8            | 0.0077 | 0.0500 | 0.0303 | 0.8863 |    10.3667 |
| ant             |              6 |      28 | 4.0000 | 8            | 0.0111 | 0.0438 | 0.0386 | 0.8794 |    18.9814 |
| ant             |              6 |      28 | 8.0000 | 8            | 0.0190 | 0.0516 | 0.0851 | 0.8071 |    29.7048 |
| ant             |              6 |      29 | 1.0000 | 8            | 0.0068 | 0.0500 | 0.0303 | 0.8859 |     5.5764 |
| ant             |              6 |      29 | 2.0000 | 8            | 0.0076 | 0.0495 | 0.0385 | 0.8769 |    10.9487 |
| ant             |              6 |      29 | 4.0000 | 8            | 0.0094 | 0.0539 | 0.0611 | 0.8433 |    20.3289 |
| ant             |              6 |      29 | 8.0000 | _unix        | 0.0011 | 0.0038 | 0.0080 | 0.0591 |    32.6810 |
| ant             |              6 |      30 | 1.0000 | 8            | 0.0068 | 0.0500 | 0.0303 | 0.8857 |     6.4192 |
| ant             |              6 |      30 | 2.0000 | 8            | 0.0076 | 0.0493 | 0.0384 | 0.8745 |    12.6236 |
| ant             |              6 |      30 | 4.0000 | 8            | 0.0093 | 0.0534 | 0.0605 | 0.8352 |    23.5664 |
| ant             |              6 |      30 | 8.0000 | _unix        | 0.0007 | 0.0026 | 0.0044 | 0.0469 |    38.3140 |
| dog             |              4 |      23 | 1.0000 | 8            | 0.0074 | 0.0549 | 0.0485 | 0.8594 |     2.4778 |
| dog             |              4 |      23 | 2.0000 | 8            | 0.0086 | 0.0716 | 0.1181 | 0.7699 |     4.9028 |
| dog             |              4 |      23 | 4.0000 | 6            | 0.0126 | 0.1533 | 0.5350 | 0.2527 |     9.3387 |
| dog             |              4 |      23 | 8.0000 | 6            | 0.0717 | 0.2501 | 0.3212 | 0.0632 |    15.8645 |
| dog             |              4 |      24 | 1.0000 | 8            | 0.0081 | 0.1118 | 0.0283 | 0.8258 |     5.4441 |
| dog             |              4 |      24 | 2.0000 | 4            | 0.0142 | 0.5329 | 0.0496 | 0.3662 |    10.5300 |
| dog             |              4 |      24 | 4.0000 | 6            | 0.0531 | 0.3053 | 0.5034 | 0.0322 |    18.2831 |
| dog             |              4 |      24 | 8.0000 | 6            | 0.1148 | 0.0290 | 0.6608 | 0.0226 |    25.9121 |
| dog             |              4 |      25 | 1.0000 | 8            | 0.0080 | 0.1109 | 0.0318 | 0.8196 |     6.5947 |
| dog             |              4 |      25 | 2.0000 | 8            | 0.0133 | 0.1615 | 0.0594 | 0.7239 |    12.6851 |
| dog             |              4 |      25 | 4.0000 | 6            | 0.0399 | 0.2295 | 0.4288 | 0.1577 |    21.4118 |
| dog             |              4 |      25 | 8.0000 | 9            | 0.0447 | 0.0737 | 0.1378 | 0.0836 |    29.0979 |
| dog             |              4 |      26 | 1.0000 | 8            | 0.0065 | 0.0893 | 0.0290 | 0.8468 |     5.2860 |
| dog             |              4 |      26 | 2.0000 | 8            | 0.0085 | 0.1506 | 0.0381 | 0.7651 |    10.2983 |
| dog             |              4 |      26 | 4.0000 | 4            | 0.0190 | 0.4901 | 0.0965 | 0.2973 |    18.2703 |
| dog             |              4 |      26 | 8.0000 | 4            | 0.0501 | 0.2542 | 0.1747 | 0.0935 |    26.6845 |
| dog             |              4 |      27 | 1.0000 | 8            | 0.0074 | 0.0797 | 0.0259 | 0.8573 |     4.5735 |
| dog             |              4 |      27 | 2.0000 | 8            | 0.0079 | 0.1238 | 0.0276 | 0.8071 |     9.0033 |
| dog             |              4 |      27 | 4.0000 | 8            | 0.0090 | 0.2965 | 0.0276 | 0.6278 |    16.6840 |
| dog             |              4 |      27 | 8.0000 | 4            | 0.0132 | 0.7224 | 0.0408 | 0.1612 |    26.4343 |
| dog             |              4 |      28 | 1.0000 | 8            | 0.0067 | 0.0638 | 0.0235 | 0.8801 |     5.4839 |
| dog             |              4 |      28 | 2.0000 | 8            | 0.0075 | 0.0713 | 0.0232 | 0.8687 |    10.7785 |
| dog             |              4 |      28 | 4.0000 | 8            | 0.0116 | 0.1096 | 0.0314 | 0.8099 |    19.8384 |
| dog             |              4 |      28 | 8.0000 | 8            | 0.0382 | 0.3202 | 0.0810 | 0.4659 |    30.9903 |
| dog             |              4 |      29 | 1.0000 | 8            | 0.0067 | 0.0634 | 0.0264 | 0.8746 |     5.8055 |
| dog             |              4 |      29 | 2.0000 | 8            | 0.0075 | 0.0709 | 0.0261 | 0.8642 |    11.4289 |
| dog             |              4 |      29 | 4.0000 | 8            | 0.0094 | 0.0787 | 0.0290 | 0.8466 |    21.2446 |
| dog             |              4 |      29 | 8.0000 | 8            | 0.0156 | 0.1153 | 0.0374 | 0.7520 |    33.9643 |
| dog             |              4 |      30 | 1.0000 | 8            | 0.0067 | 0.0565 | 0.0267 | 0.8831 |     6.6595 |
| dog             |              4 |      30 | 2.0000 | 8            | 0.0076 | 0.0562 | 0.0265 | 0.8791 |    13.1256 |
| dog             |              4 |      30 | 4.0000 | 8            | 0.0086 | 0.0559 | 0.0264 | 0.8740 |    24.5274 |
| dog             |              4 |      30 | 8.0000 | 8            | 0.0134 | 0.0467 | 0.0283 | 0.7305 |    39.6826 |

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
