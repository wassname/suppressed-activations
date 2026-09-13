---
row: ant-att-h20
expected_answer: 6
observed_answer: 6
verdict: TRANSFER
tokens: 65
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: attenuation
edit_site: h20
delta_anchor_layer: -1
---

# ant-att-h20

- expected answer: 6 — observed: 6 — TRANSFER
- judgment: TRANSFER: answer 6 + ant identity, sustained ant description; 'hardworking' anthropomorphism (attributed: uncertain claim). Historical success, byte-exact replay.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", "\u68a6\u60f3\u7684", "\":@\"", "getResponse", " piccolo", " persistence", "debit"]

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
[{"token_id": 21, "token": "6", "logp": -0.018352463841438293, "p": 0.9818149209022522, "delta_logp": 3.5659377574920654}, {"token_id": 23, "token": "8", "logp": -4.643352508544922, "p": 0.009625374339520931, "delta_logp": -4.559062480926514}, {"token_id": 18, "token": "3", "logp": -5.268352508544922, "p": 0.005152091383934021, "delta_logp": 0.8159375190734863}, {"token_id": 16, "token": "1", "logp": -6.518352508544922, "p": 0.0014760988997295499, "delta_logp": -0.18406248092651367}, {"token_id": 19, "token": "4", "logp": -7.268352508544922, "p": 0.0006972597911953926, "delta_logp": -4.1840620040893555}, {"token_id": 17, "token": "2", "logp": -7.893352508544922, "p": 0.00037321625859476626, "delta_logp": -1.1840624809265137}, {"token_id": 22, "token": "7", "logp": -8.643352508544922, "p": 0.00017629488138481975, "delta_logp": -0.6840624809265137}, {"token_id": 18117, "token": " Six", "logp": -8.768352508544922, "p": 0.00015557969163637608, "delta_logp": 2.8159379959106445}, {"token_id": 15, "token": "0", "logp": -9.268352508544922, "p": 9.436385153094307e-05, "delta_logp": -1.8090624809265137}, {"token_id": 20, "token": "5", "logp": -9.393352508544922, "p": 8.327580144396052e-05, "delta_logp": -1.5590624809265137}]
```

## Generation — first 32 tokens (preview)

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. These social creatures live in vast colonies and communicate
```

## Full continuation

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. These social creatures live in vast colonies and communicate with one another using chemical signals called pheromones. Despite their tiny size, ants are incredibly resilient and can be found in almost every habitat on Earth.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-att-h20/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
