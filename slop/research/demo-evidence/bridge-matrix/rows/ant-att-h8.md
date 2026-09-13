---
row: ant-att-h8
expected_answer: 6
observed_answer: 8
verdict: NO TRANSFER
tokens: 50
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: attenuation
edit_site: h8
delta_anchor_layer: 20
---

# ant-att-h8

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: spider identity; FALSE biology (spiders described as hardworking social insects living in colonies — arachnids, not eusocial insects); ant properties leaked without the name change.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", " llevaron", "\u62e5\u6709\u7740", "getResponse", "\u958b\u7bb1\u6587", " mapView", "(fin"]

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

In this attenuation-recipe row the injected component is the TEMPLATE-MEAN delta (CONCEPT_TEMPLATES spider-vs-donor difference, position+template averaged, projected on the rank-4 attenuation basis, scalar norm-matched); the donor prompt rendered below played no role in the delta. The donor input (rendered):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that lives in colonies and follows pheromone trails have?\nAnswer: '
```

## First-position top-10 output table (log p / p)

```json
[{"token_id": 23, "token": "8", "logp": -0.06139713525772095, "p": 0.9404497146606445, "delta_logp": 0.022893115878105164}, {"token_id": 21, "token": "6", "logp": -3.436397075653076, "p": 0.03218042105436325, "delta_logp": 0.14789319038391113}, {"token_id": 19, "token": "4", "logp": -4.436397075653076, "p": 0.011838515289127827, "delta_logp": -1.3521068096160889}, {"token_id": 18, "token": "3", "logp": -5.436397075653076, "p": 0.004355146083980799, "delta_logp": 0.647892951965332}, {"token_id": 17, "token": "2", "logp": -5.686397075653076, "p": 0.003391791367903352, "delta_logp": 1.022892951965332}, {"token_id": 16, "token": "1", "logp": -5.686397075653076, "p": 0.003391791367903352, "delta_logp": 0.647892951965332}, {"token_id": 15, "token": "0", "logp": -6.686397075653076, "p": 0.0012477703858166933, "delta_logp": 0.772892951965332}, {"token_id": 22, "token": "7", "logp": -7.311397075653076, "p": 0.0006678833160549402, "delta_logp": 0.647892951965332}, {"token_id": 24, "token": "9", "logp": -7.623897075653076, "p": 0.0004886338720098138, "delta_logp": 1.4603934288024902}, {"token_id": 2972, "token": " **", "logp": -7.623897075653076, "p": 0.0004886338720098138, "delta_logp": 3.0228934288024902}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is the spider. Spiders are small, hardworking insects known for their ability to work together in organized groups to build and maintain colonies.
```

## Full continuation

```text
8

The animal is the spider. Spiders are small, hardworking insects known for their ability to work together in organized groups to build and maintain colonies. They play a crucial role in ecosystems as a primary food source for many other species.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-att-h8/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
