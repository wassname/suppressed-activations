---
row: ant-inc-h20
expected_answer: 6
observed_answer: 8
verdict: NO TRANSFER
tokens: 58
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: increment
edit_site: h20
delta_anchor_layer: 20
---

# ant-inc-h20

- expected answer: 6 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: coherent spider description.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" minera", ".answer", " \u041a\u043e\u043d\u043a\u0443\u0440\u0441", "\tanswer", " answers", " ndr", " \u043a\u043e\u043d\u043a\u0443\u0440\u0441", " respuestas"]

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
[{"token_id": 23, "token": "8", "logp": -0.29594120383262634, "p": 0.7438311576843262, "delta_logp": -0.21165095269680023}, {"token_id": 21, "token": "6", "logp": -1.7959412336349487, "p": 0.16597115993499756, "delta_logp": 1.7883490324020386}, {"token_id": 19, "token": "4", "logp": -2.670941114425659, "p": 0.06918708235025406, "delta_logp": 0.4133491516113281}, {"token_id": 16, "token": "1", "logp": -4.670941352844238, "p": 0.009363451041281223, "delta_logp": 1.66334867477417}, {"token_id": 17, "token": "2", "logp": -5.545941352844238, "p": 0.0039032672066241503, "delta_logp": 1.16334867477417}, {"token_id": 18, "token": "3", "logp": -5.670941352844238, "p": 0.003444621106609702, "delta_logp": 0.4133486747741699}, {"token_id": 15, "token": "0", "logp": -6.670941352844238, "p": 0.0012672052253037691, "delta_logp": 0.7883486747741699}, {"token_id": 22, "token": "7", "logp": -6.920941352844238, "p": 0.0009869005298241973, "delta_logp": 1.03834867477417}, {"token_id": 20, "token": "5", "logp": -7.045941352844238, "p": 0.0008709366666153073, "delta_logp": 0.7883486747741699}, {"token_id": 24, "token": "9", "logp": -7.920941352844238, "p": 0.00036306038964539766, "delta_logp": 1.1633491516113281}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid known for spinning intricate webs to catch insects. It typically has eight legs, which it uses for walking and sensing its
```

## Full continuation

```text
8

The spider is an arachnid known for spinning intricate webs to catch insects. It typically has eight legs, which it uses for walking and sensing its environment. Despite its reputation for being creepy, many spiders are harmless to humans and play a vital role in controlling pest populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/ant-inc-h20/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
