---
row: ant-inc-h8
expected_answer: 6
observed_answer: 8
verdict: NO TRANSFER
tokens: 50
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: increment
edit_site: h8
delta_anchor_layer: 20
---

# ant-inc-h8

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: the 'more or fewer legs' assertion is flagged as unsupported; 'legs manipulate silk' is PLAUSIBLE (legs can manipulate silk; spinnerets produce it) — not flagged as false.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", "getResponse", " resposta", "response", "_response", "\u5206\u884c", " respond"]

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

In this increment-recipe row the union basis U was built from the source AND donor prompt trajectories (multi-token selection); the injected component is the template-mean delta projected on that U. The donor input (rendered):

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that lives in colonies and follows pheromone trails have?\nAnswer: '
```

## First-position top-10 output table (log p / p)

```json
[{"token_id": 23, "token": "8", "logp": -0.07833986729383469, "p": 0.9246501326560974, "delta_logp": 0.0059503838419914246}, {"token_id": 19, "token": "4", "logp": -2.9533398151397705, "p": 0.0521651916205883, "delta_logp": 0.1309504508972168}, {"token_id": 17, "token": "2", "logp": -5.07834005355835, "p": 0.006230242550373077, "delta_logp": 1.6309499740600586}, {"token_id": 18, "token": "3", "logp": -5.20334005355835, "p": 0.005498169455677271, "delta_logp": 0.8809499740600586}, {"token_id": 16, "token": "1", "logp": -5.32834005355835, "p": 0.004852117504924536, "delta_logp": 1.0059499740600586}, {"token_id": 21, "token": "6", "logp": -5.82834005355835, "p": 0.002942957915365696, "delta_logp": -2.2440497875213623}, {"token_id": 20, "token": "5", "logp": -6.82834005355835, "p": 0.0010826537618413568, "delta_logp": 1.0059499740600586}, {"token_id": 22, "token": "7", "logp": -6.82834005355835, "p": 0.0010826537618413568, "delta_logp": 1.1309499740600586}, {"token_id": 24, "token": "9", "logp": -7.70334005355835, "p": 0.00045131726074032485, "delta_logp": 1.3809504508972168}, {"token_id": 15, "token": "0", "logp": -8.078339576721191, "p": 0.0003101856564171612, "delta_logp": -0.6190495491027832}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid that typically has eight legs. These appendages are used to spin silk threads to create webs for protection and hunting.
```

## Full continuation

```text
8

The spider is an arachnid that typically has eight legs. These appendages are used to spin silk threads to create webs for protection and hunting. While some species may have more or fewer legs, eight is the most common number.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-inc-h8/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
