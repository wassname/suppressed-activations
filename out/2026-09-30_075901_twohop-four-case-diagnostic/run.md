---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
source_sha256: 3dcbe0634f4dbac419489c264c669e1ad34efc6ae52bd74f3b185c18b6549438
prior: out/2026-09-29_204246_twohop-english/result.json
forward_passes: 4
generations: 0
elapsed_seconds: 44.73
---
# Four-case localisation diagnostic

Written by PI/OpenAI.

Selection: first four previously answer-correct cases, in saved order. No success-rate claim.
SHOULD: frozen ranks reproduce exactly. If masking causes the misses, unmasked ranks improve. If location causes misses, the plain lens finds the bridge elsewhere. These label-selected locations are diagnostics, not a frozen method or causal evidence.

| bridge                |   frozen rank |   unmasked rank |   best last-token lens rank |   layer |   best anywhere lens rank | location   |
|:----------------------|--------------:|----------------:|----------------------------:|--------:|--------------------------:|:-----------|
| Bulgaria              |         29805 |           29838 |                         226 |      32 |                         0 | L28/P3     |
| Iceland               |         25669 |            1152 |                           8 |      32 |                         0 | L28/P3     |
| Turkey                |            14 |              14 |                           3 |      25 |                         0 | L27/P13    |
| Republic of the Congo |           849 |             850 |                           0 |      24 |                         0 | L6/P5      |

Input: "The capital of the country with the national anthem 'Mila Rodino' is"

Prior continuation: ':\nA. Sofia\nB.'

Stages: {"peak_any raw": {"r_hidden": 29838, "r_said": 51346, "ok": false, "top8": ["capital", "资本", "博士生导师", "Capital", "新老客户", " خار", "monster", "-capital"]}, "peak_any prompt mask": {"r_hidden": 29826, "r_said": 51332, "ok": false, "top8": ["资本", "博士生导师", "新老客户", " خار", "monster", "-capital", "หลวง", "外国语学校"]}, "peak_any output mask": {"r_hidden": 29817, "r_said": 51306, "ok": false, "top8": ["capital", "资本", "博士生导师", "Capital", "新老客户", " خار", "monster", "-capital"]}, "peak_any − prompt & output-layer words (dev winner)": {"r_hidden": 29805, "r_said": 51292, "ok": false, "top8": ["资本", "博士生导师", "新老客户", " خار", "monster", "-capital", "หลวง", "外国语学校"]}, "plain L27 raw": {"r_hidden": 19350, "r_said": 9655, "ok": false, "top8": [" ___", " capitale", "capital", "____", " capital", " capitals", "___", " ____"]}}

Input: "The capital of the country with the national anthem 'Lofsöngur' is"

Prior continuation: ' Reykjavík.\nA.'

Stages: {"peak_any raw": {"r_hidden": 1152, "r_said": 5721, "ok": false, "top8": ["外观设计", "หลวง", "新老客户", "ụy", "capital", "amt", " إب", "Capital"]}, "peak_any prompt mask": {"r_hidden": 1150, "r_said": 5716, "ok": false, "top8": ["外观设计", "หลวง", "新老客户", "ụy", "amt", " إب", "战神", "umos"]}, "peak_any output mask": {"r_hidden": 25677, "r_said": 1000000000, "ok": false, "top8": ["外观设计", "หลวง", "新老客户", "ụy", "capital", "amt", " إب", "Capital"]}, "peak_any − prompt & output-layer words (dev winner)": {"r_hidden": 25669, "r_said": 1000000000, "ok": false, "top8": ["外观设计", "หลวง", "新老客户", "ụy", "amt", " إب", "战神", "umos"]}, "plain L27 raw": {"r_hidden": 12392, "r_said": 30, "ok": false, "top8": [" ___", "capital", " capitale", " capital", "Capital", "____", " capitals", "___"]}}

Input: "The country with the national anthem 'İstiklâl Marşı' is led by president"

Prior continuation: ' Recep Tayyip Erdoğan.\nA.'

Stages: {"peak_any raw": {"r_hidden": 14, "r_said": 8939, "ok": true, "top8": ["elles", " ตุ", "urso", "edd", "кру", "eppe", " Annunci", "igl"]}, "peak_any prompt mask": {"r_hidden": 14, "r_said": 8935, "ok": true, "top8": ["elles", " ตุ", "urso", "edd", "кру", "eppe", " Annunci", "igl"]}, "peak_any output mask": {"r_hidden": 14, "r_said": 1000000000, "ok": true, "top8": ["elles", " ตุ", "urso", "edd", "кру", "eppe", " Annunci", "igl"]}, "peak_any − prompt & output-layer words (dev winner)": {"r_hidden": 14, "r_said": 1000000000, "ok": true, "top8": ["elles", " ตุ", "urso", "edd", "кру", "eppe", " Annunci", "igl"]}, "plain L27 raw": {"r_hidden": 7, "r_said": 0, "ok": false, "top8": [" Recep", " Nurs", " Турции", "土耳其", " турец", " ตุ", "悬浮", "Tur"]}}

Input: 'The country with Brazzaville as its capital is led by president'

Prior continuation: ' Denis Sassou Nguesso.\n'

Stages: {"peak_any raw": {"r_hidden": 850, "r_said": 5221, "ok": false, "top8": ["锦涛", " seques", " Bélgica", "上手", "lieben", " prospec", "大大小", "isiv"]}, "peak_any prompt mask": {"r_hidden": 850, "r_said": 5220, "ok": false, "top8": ["锦涛", " seques", " Bélgica", "上手", "lieben", " prospec", "大大小", "isiv"]}, "peak_any output mask": {"r_hidden": 849, "r_said": 5205, "ok": false, "top8": ["锦涛", " seques", " Bélgica", "上手", "lieben", " prospec", "大大小", "isiv"]}, "peak_any − prompt & output-layer words (dev winner)": {"r_hidden": 849, "r_said": 5204, "ok": false, "top8": ["锦涛", " seques", " Bélgica", "上手", "lieben", " prospec", "大大小", "isiv"]}, "plain L27 raw": {"r_hidden": 0, "r_said": 912, "ok": true, "top8": [" Congo", " angol", "掌", " pana", "ichel", " Bélgica", "过渡", "掌握"]}}

run.md: /workspace/2026/suppressed-activations/out/2026-09-30_075901_twohop-four-case-diagnostic/run.md
