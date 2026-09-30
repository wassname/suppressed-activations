---
script: scripts/english/06_twohop_english.py
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
data: TwoHopFact (Yang et al. 2024), CC-BY-4.0
k: 32
per_category: 6
tried: 1027
max_tries_per_category: 20
bridge_unknown_to_model: 931
skipped_overlap_or_empty: 34
scored: 62
---
# Frozen selectors on English-only two-hop prompts -- Claudypoo[opus-4.8]

Hidden = bridge entity (e2), said = answer entity (e3). Scored only when the model names the bridge
when asked the first hop directly. Pass = bridge token in top 32, answer tokens not.

SHOULD: if the method generalises, the dev winner passes far more often than the plain logit lens.

| selector (frozen)                                   | pass, all   | pass, two-hop answer correct   | pass, answer wrong   |   bridge in top-32 |   answer in top-32 |   median bridge rank |
|:----------------------------------------------------|:------------|:-------------------------------|:---------------------|-------------------:|-------------------:|---------------------:|
| peak_any − prompt & output-layer words (dev winner) | 3/62        | 2/16                           | 1/46                 |                  3 |                  0 |                10654 |
| peak lens L27 − prompt & output-layer words         | 8/62        | 3/16                           | 5/46                 |                  8 |                  6 |                 4665 |
| rise_fall 22/27/32 (repo)                           | 1/62        | 0/16                           | 1/46                 |                  1 |                  0 |                19739 |
| peak logit lens L27                                 | 7/62        | 2/16                           | 5/46                 |                  8 |                 10 |                 2403 |

First six scored prompts where the two-hop answer is correct (dev winner):

- `The capital of the country with the national anthem 'Mila Rodino' is` → said `':\nA. Sofia\nB.'`; bridge **Bulgaria** at rank 29805; top-8 ['资本', '博士生导师', '新老客户', ' خار', 'monster', '-capital', 'หลวง', '外国语学校']
- `The capital of the country with the national anthem 'Lofsöngur' is` → said `'Reykjavík.\nA.'`; bridge **Iceland** at rank 25669; top-8 ['外观设计', 'หลวง', '新老客户', 'ụy', 'amt', ' إب', '战神', 'umos']
- `The country with the national anthem 'İstiklâl Marşı' is led by president` → said `'Recep Tayyip Erdoğan.\nA.'`; bridge **Turkey** at rank 14; top-8 ['elles', ' ตุ', 'urso', 'edd', 'кру', 'eppe', ' Annunci', 'igl']
- `The country with Brazzaville as its capital is led by president` → said `'Denis Sassou Nguesso.'`; bridge **Republic of the Congo** at rank 849; top-8 ['锦涛', ' seques', ' Bélgica', '上手', 'lieben', ' prospec', '大大小', 'isiv']
- `The country with Valletta as its capital is led by president` → said `'George Vella.\nA. Malta'`; bridge **Malta** at rank 9; top-8 [' па', '行之', '迫', '驳', 'tsy', 'ustralian', 'curso', '絡']
- `The company founded by Adrian Carmack has its headquarters in the country of` → said `'___.\nA. United States'`; bridge **id Software** at rank 7665; top-8 ['教育集团', 'ässig', 'やし', '本楼', ' competitiv', '_ROUND', ' diety', '往期精彩']
