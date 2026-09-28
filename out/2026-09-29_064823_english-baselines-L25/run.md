---
script: scripts/english/01_detector_baselines_and_pair_transfer.py
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
layers: {early: 22, peak: 27, out: 32}
rank_detect: 32
rank_patch: 8
patch_residuals: [25, 26, 27, 28, 29, 30, 31, 32]
n_q1: 120
n_pairs: 50
---
# English-setting baselines -- Claudypoo[opus-4.8]

## Q1. Which top-32 selector contains the answer word? (Wendler 4-shot de->zh prompt, all words)

English hit = a selected token is a >=3-char prefix of the English word. Chinese hit = a selected token is a prefix of the Chinese word.

| selector (top-32 tokens)   | English answer in set   | Chinese answer in set   |
|:---------------------------|:------------------------|:------------------------|
| rise_and_fall (repo)       | 94/120                  | 3/120                   |
| peak logit lens            | 116/120                 | 105/120                 |
| fall only                  | 69/120                  | 2/120                   |
| rise only                  | 114/120                 | 101/120                 |
| output logits (sanity)     | 67/120                  | 118/120                 |

rise_and_fall top-8 examples: [{"word": {"en": "book", "de": "Buch", "zh": "书"}, "top8": [" book", " books", " BOOK", " booking", " Book", ".books", " Volume", " Booking"]}, {"word": {"en": "cloud", "de": "Wolke", "zh": "云"}, "top8": [" cloud", " clouds", " Cloud", "_cloud", "-cloud", "/cloud", " обла", "cloud"]}, {"word": {"en": "bag", "de": "Tasche", "zh": "包"}, "top8": [" bag", " port", " sac", " Cases", " cases", " case", " ang", "-facing"]}]

## Q2. Does replacing the component move the answer to the target word? (zero-shot prompt, fixed consecutive pairing)

SHOULD: rise_and_fall well above random; if peak logit lens ≈ rise_and_fall, the fall term adds nothing causally.

| replacement at L25-L32, last token, prefill    |   pairs | top-1 = target zh   | top-1 = source zh   |   median Δ log-odds (nats) |
|:-----------------------------------------------|--------:|:--------------------|:--------------------|---------------------------:|
| rise_and_fall (repo)                           |      50 | 22/50               | 12/50               |                      12.36 |
| peak logit lens                                |      50 | 34/50               | 0/50                |                      31.54 |
| English answer tokens (oracle)                 |      50 | 5/50                | 0/50                |                      19.25 |
| Chinese answer tokens (oracle)                 |      50 | 50/50               | 0/50                |                      34.37 |
| random rotation, matched to rise_and_fall norm |      50 | 0/50                | 50/50               |                       0.06 |
| full residual (upper bound)                    |      50 | 50/50               | 0/50                |                      21.12 |

| rise_and_fall pairs                              |   n | top-1 = target zh   |
|:-------------------------------------------------|----:|:--------------------|
| English answer in both rank-8 selections = True  |  16 | 9/16                |
| English answer in both rank-8 selections = False |  34 | 13/34               |

First-token generations (24 tokens, patch on prompt only):

**Herz → Schule** (want 学校)

- rise_and_fall (repo): `'school" (学校).\nA. True\nB. False\n\n<think>\nThinking Process:\n\n1.  **'`
- full residual (upper bound): `'学校" (xuéxiào), which means "school" in English. This is a common mistake, as "'`

**Buch → Wolke** (want 云)

- rise_and_fall (repo): `'云" (yún).\nA. 正确\nB. 错误\n\n<think>\nThinking Process:\n\n1'`
- full residual (upper bound): `'云" (yún).\nA. 正确\nB. 错误\n\n<think>\nThinking Process:\n\n1'`

**Wolke → Tasche** (want 包)

- rise_and_fall (repo): `'口袋" (píngdài), which means "pocket" in English. This is a fascinating example of'`
- full residual (upper bound): `'包" (bāo), which means "cloud" in Chinese. This is a fascinating example of how words can'`

**Tasche → Mund** (want 口)

- rise_and_fall (repo): `'口" (kǒu), which means "mouth" in Chinese. This is a fascinating example of how words'`
- full residual (upper bound): `'口" (kǒu), which means "mouth" in Chinese. This is a fascinating example of how words'`

**Mund → Berg** (want 山)

- rise_and_fall (repo): `'Mouth". The German word "Mund" is a noun that refers to the mouth, which is the opening in'`
- full residual (upper bound): `'山" (shān), which means "mountain". This is a very interesting and unusual translation. The word'`

**Berg → Tuch** (want 布)

- rise_and_fall (repo): `'山" (shān), which means "mountain". The word "Berg" is a noun in German'`
- full residual (upper bound): `'布爾格" (Bù\'ěrgé). This word is also used in the context of the "B'`
