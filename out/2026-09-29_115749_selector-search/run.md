---
script: scripts/english/03_selector_search.py
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
k: 32
n_prompts: 120
selected_on: even-index prompts
reported_on: odd-index prompts
best_on_even: 'peak_any e22 p24-30 − prompt words'
---
# Selector search: find the hidden word without language info -- Claudypoo[opus-4.8]

success@32: best English-answer token rank < 32, best Chinese (said) and German (input) ranks >= 32.
Selection uses the even half only; the odd column is the held-out estimate for the selected row.
SHOULD: the winner's odd score is close to its even score; a large drop means the choice overfit.

| selector (sorted by even-half score)       | success@32 even (select)   | success@32 odd (report)   |   English in top-32 (all 120) |   Chinese in |   German in |   median best-English rank |
|:-------------------------------------------|:---------------------------|:--------------------------|------------------------------:|-------------:|------------:|---------------------------:|
| **peak_any e22 p24-30 − prompt words**     | 46/60                      | 46/60                     |                            95 |            4 |           0 |                          0 |
| peak_any e18 p22-30 − prompt words         | 43/60                      | 41/60                     |                            87 |            4 |           0 |                          1 |
| rise_fall 22/29/32 − prompt words          | 43/60                      | 42/60                     |                            85 |            0 |           0 |                          1 |
| rise_fall 22/29/32                         | 41/60                      | 34/60                     |                            96 |            0 |          24 |                          0 |
| rise_fall 22/27/32 (repo) − prompt words   | 40/60                      | 42/60                     |                            84 |            4 |           0 |                          1 |
| rise_fall 16/29/32 − prompt words          | 40/60                      | 33/60                     |                            73 |            0 |           0 |                          4 |
| rise_fall 20/29/32 − prompt words          | 40/60                      | 40/60                     |                            80 |            0 |           0 |                          1 |
| rise_fall 22/27/32 − prompt words          | 40/60                      | 42/60                     |                            84 |            4 |           0 |                          1 |
| rise_fall 16/29/32                         | 39/60                      | 32/60                     |                            84 |            0 |          16 |                          1 |
| rise_fall 20/29/32                         | 39/60                      | 36/60                     |                            91 |            0 |          20 |                          1 |
| rise_fall 22/28/32 − prompt words          | 39/60                      | 43/60                     |                            84 |            3 |           0 |                          1 |
| rise_fall 16/27/32 − prompt words          | 38/60                      | 38/60                     |                            78 |            3 |           0 |                          3 |
| rise_fall 20/27/32 − prompt words          | 38/60                      | 41/60                     |                            81 |            4 |           0 |                          1 |
| peak_any e18 p22-30                        | 37/60                      | 30/60                     |                            98 |            4 |          28 |                          0 |
| rise_fall 22/28/32                         | 37/60                      | 33/60                     |                            95 |            3 |          25 |                          0 |
| rise_fall 20/28/32                         | 36/60                      | 35/60                     |                            91 |            3 |          19 |                          1 |
| rise_fall 20/28/32 − prompt words          | 36/60                      | 42/60                     |                            80 |            3 |           0 |                          1 |
| peak_any e22 p24-30                        | 34/60                      | 27/60                     |                           105 |            4 |          44 |                          0 |
| rise_fall 16/27/32                         | 34/60                      | 26/60                     |                            88 |            3 |          26 |                          1 |
| rise_fall 16/28/32                         | 34/60                      | 36/60                     |                            86 |            3 |          14 |                          1 |
| rise_fall 16/28/32 − prompt words          | 32/60                      | 41/60                     |                            75 |            3 |           0 |                          2 |
| rise_fall 20/27/32                         | 31/60                      | 25/60                     |                            91 |            3 |          34 |                          0 |
| rise_fall 22/27/32 (repo)                  | 30/60                      | 26/60                     |                            94 |            3 |          37 |                          0 |
| max_l(z_l) - z_out, l24-30 − prompt words  | 30/60                      | 34/60                     |                            66 |            3 |           0 |                         11 |
| rise_fall 22/27/32                         | 30/60                      | 26/60                     |                            94 |            3 |          37 |                          0 |
| rise_fall 22/26/32 − prompt words          | 29/60                      | 30/60                     |                            59 |            0 |           0 |                         40 |
| max_l(z_l) - z_out, l24-30                 | 28/60                      | 31/60                     |                            76 |            3 |          16 |                          1 |
| rise_fall 20/26/32 − prompt words          | 28/60                      | 28/60                     |                            56 |            0 |           0 |                        121 |
| rise_fall 22/25/32 − prompt words          | 27/60                      | 28/60                     |                            55 |            0 |           0 |                        119 |
| rise_fall 20/26/32                         | 26/60                      | 19/60                     |                            67 |            0 |          27 |                          7 |
| rise_fall 16/26/32 − prompt words          | 25/60                      | 26/60                     |                            51 |            0 |           0 |                        799 |
| fall 27-32                                 | 24/60                      | 27/60                     |                            69 |            2 |          17 |                          7 |
| fall 27-32 − prompt words                  | 24/60                      | 34/60                     |                            59 |            2 |           0 |                         39 |
| rise_fall 16/26/32                         | 24/60                      | 20/60                     |                            60 |            0 |          17 |                         76 |
| rise_fall 22/26/32                         | 23/60                      | 18/60                     |                            70 |            0 |          35 |                          3 |
| mean_l(z_l) - z_out, l24-30                | 22/60                      | 23/60                     |                            53 |            0 |           9 |                        134 |
| rise_fall 20/25/32 − prompt words          | 22/60                      | 22/60                     |                            44 |            0 |           0 |                        351 |
| mean_l(z_l) - z_out, l24-30 − prompt words | 19/60                      | 24/60                     |                            43 |            0 |           0 |                        973 |
| rise_fall 16/25/32                         | 19/60                      | 17/60                     |                            44 |            0 |          11 |                        740 |
| rise_fall 16/25/32 − prompt words          | 17/60                      | 18/60                     |                            35 |            0 |           0 |                       2070 |
| rise_fall 22/25/32                         | 17/60                      | 16/60                     |                            66 |            0 |          42 |                         16 |
| rise_fall 20/25/32                         | 16/60                      | 15/60                     |                            54 |            0 |          32 |                         68 |
