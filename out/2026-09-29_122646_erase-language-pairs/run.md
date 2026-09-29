---
script: scripts/english/04_erase_and_language_pairs.py
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
k: 32
pairs: ['de->zh', 'de->fr', 'fr->ru', 'ru->fr', 'de->ru', 'ru->de', 'fr->de']
dev_pair: de->fr
reference_pair: de->zh
skipped_per_pair: {"de\u2192zh": 17, "de\u2192fr": 33, "fr\u2192ru": 26, "ru\u2192fr": 26, "de\u2192ru": 17, "ru\u2192de": 17, "fr\u2192de": 33}
---
# Erasing input embeddings, and frozen selectors on unseen language pairs -- Claudypoo[opus-4.8]

Which language does Qwen think in? Mean logit-lens probability at the last token (max over layers):

| pair   | English max p   | Chinese max p   | input max p   | output max p   |
|:-------|:----------------|:----------------|:--------------|:---------------|
| de→zh  | 0.36 @L27       | 0.57 @L32       | 0.01 @L27     | 0.57 @L32      |
| de→fr  | 0.59 @L28       | 0.09 @L27       | 0.02 @L27     | 0.49 @L30      |
| fr→ru  | 0.49 @L28       | 0.13 @L29       | 0.03 @L30     | 0.39 @L32      |
| ru→fr  | 0.59 @L28       | 0.10 @L28       | 0.01 @L25     | 0.47 @L31      |
| de→ru  | 0.51 @L28       | 0.12 @L29       | 0.01 @L27     | 0.45 @L32      |
| ru→de  | 0.52 @L27       | 0.13 @L29       | 0.02 @L26     | 0.46 @L31      |
| fr→de  | 0.53 @L27       | 0.09 @L29       | 0.04 @L30     | 0.48 @L31      |

SHOULD: on pairs without zh, a Chinese peak well above zero means Qwen also thinks in Chinese.

| selector (top-32; pass = hidden in, input and output out)   | de→zh (ref)   | de→fr (dev)   | fr→ru (test)   | ru→fr (test)   | de→ru (test)   | ru→de (test)   | fr→de (test)   |
|:------------------------------------------------------------|:--------------|:--------------|:---------------|:---------------|:---------------|:---------------|:---------------|
| rise_fall 22/27/32 (repo)                                   | 45/103        | 44/76         | 43/78          | 45/78          | 48/88          | 55/88          | 37/76          |
| peak_any − prompt words (frozen 03 winner)                  | 84/103        | 64/76         | 64/78          | 71/78          | 67/88          | 75/88          | 64/76          |
| rise_fall 22/27/32, erased                                  | 46/103        | 45/76         | 51/78          | 54/78          | 47/88          | 61/88          | 40/76          |
| peak_any, erased                                            | 50/103        | 39/76         | 52/78          | 46/78          | 52/88          | 52/88          | 37/76          |
| peak logit lens L27                                         | 4/103         | 14/76         | 11/78          | 9/78           | 15/88          | 10/88          | 14/76          |

| English-only passes (Chinese not counted)   | de→zh   | de→fr   | fr→ru   | ru→fr   | de→ru   | ru→de   | fr→de   |
|:--------------------------------------------|:--------|:--------|:--------|:--------|:--------|:--------|:--------|
| rise_fall 22/27/32 (repo)                   | 45/103  | 44/76   | 43/78   | 45/78   | 47/88   | 54/88   | 37/76   |
| peak_any − prompt words (frozen 03 winner)  | 84/103  | 64/76   | 64/78   | 69/78   | 67/88   | 75/88   | 64/76   |
| rise_fall 22/27/32, erased                  | 46/103  | 45/76   | 48/78   | 54/78   | 45/88   | 60/88   | 39/76   |
| peak_any, erased                            | 50/103  | 39/76   | 50/78   | 46/78   | 52/88   | 52/88   | 37/76   |
| peak logit lens L27                         | 4/103   | 14/76   | 11/78   | 9/78    | 15/88   | 10/88   | 14/76   |

| failure counts: hidden missing / output in / input in   | de→zh    | de→fr   | fr→ru   | ru→fr   | de→ru   | ru→de   | fr→de   |
|:--------------------------------------------------------|:---------|:--------|:--------|:--------|:--------|:--------|:--------|
| rise_fall 22/27/32 (repo)                               | 25/2/33  | 5/1/28  | 17/3/17 | 8/2/23  | 19/6/19 | 14/1/19 | 13/1/27 |
| peak_any − prompt words (frozen 03 winner)              | 16/3/0   | 2/11/0  | 4/10/0  | 1/6/0   | 6/15/0  | 6/7/0   | 5/7/0   |
| rise_fall 22/27/32, erased                              | 19/10/36 | 4/1/29  | 19/3/8  | 9/0/15  | 20/5/21 | 12/1/15 | 12/1/27 |
| peak_any, erased                                        | 12/13/38 | 2/9/31  | 2/13/15 | 2/6/26  | 6/18/24 | 5/5/27  | 5/7/31  |
| peak logit lens L27                                     | 4/90/64  | 2/45/43 | 4/54/43 | 1/49/55 | 4/61/46 | 2/46/68 | 4/39/45 |
