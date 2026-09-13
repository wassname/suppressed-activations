---
row: dog-att-h8
expected_answer: 4
observed_answer: 8
verdict: NO TRANSFER
tokens: 37
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: attenuation
edit_site: h8
delta_anchor_layer: 20
---

# dog-att-h8

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: identity changed to dog but the answer STAYED 8 (answer-source/name-target mismatch); 'likely male' and the US-popularity claim are invented/uncertain.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", "getResponse", "\u0647\u064a", "\u5206\u884c", "\u0e08\u0e33\u0e19\u0e27\u0e19", " llevaron", " bilang"]

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

In this attenuation-recipe row the injected component is the TEMPLATE-MEAN delta (CONCEPT_TEMPLATES spider-vs-donor difference, position+template averaged, projected on the rank-4 attenuation basis, scalar norm-matched); the donor prompt rendered below played no role in the delta. The donor input (rendered):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that barks and is called man's best friend have?\nAnswer: "
```

## First-position top-10 output table (log p / p)

```json
[{"token_id": 23, "token": "8", "logp": -0.07802534103393555, "p": 0.9249410033226013, "delta_logp": 0.006264910101890564}, {"token_id": 19, "token": "4", "logp": -2.9530253410339355, "p": 0.05218159779906273, "delta_logp": 0.13126492500305176}, {"token_id": 21, "token": "6", "logp": -4.9530253410339355, "p": 0.007062011864036322, "delta_logp": -1.3687350749969482}, {"token_id": 17, "token": "2", "logp": -5.4530253410339355, "p": 0.004283326677978039, "delta_logp": 1.2562646865844727}, {"token_id": 16, "token": "1", "logp": -5.5780253410339355, "p": 0.00378002249635756, "delta_logp": 0.7562646865844727}, {"token_id": 15, "token": "0", "logp": -5.7030253410339355, "p": 0.0033358579967170954, "delta_logp": 1.7562646865844727}, {"token_id": 18, "token": "3", "logp": -6.2030253410339355, "p": 0.0020233001559972763, "delta_logp": -0.11873531341552734}, {"token_id": 22, "token": "7", "logp": -7.2030253410339355, "p": 0.0007443305803462863, "delta_logp": 0.7562646865844727}, {"token_id": 20, "token": "5", "logp": -7.7655253410339355, "p": 0.0004241067508701235, "delta_logp": 0.06876468658447266}, {"token_id": 24, "token": "9", "logp": -7.8280253410339355, "p": 0.00039841141551733017, "delta_logp": 1.2562651634216309}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal described is a dog, specifically a male who is likely to be the owner's best friend. Dogs have historically been the most popular choice in
```

## Full continuation

```text
8

The animal described is a dog, specifically a male who is likely to be the owner's best friend. Dogs have historically been the most popular choice in the United States.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-att-h8/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
