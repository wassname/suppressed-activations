---
row: dog-att-h20
expected_answer: 4
observed_answer: 4
verdict: TRANSFER
tokens: 65
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.015873
selector: attenuation
edit_site: h20
delta_anchor_layer: -1
---

# dog-att-h20

- expected answer: 4 — observed: 4 — TRANSFER
- judgment: TRANSFER: answer 4 + dog identity, sustained donor description; 'short history of being raised by humans' questionable (attributed: uncertain claim). Historical success, byte-exact replay.
- readout (production-saved, detector readout — separate from the top-10 table):
  [" contradictions", " respuesta", " risposta", " pia", "\u5411\u8bb0\u8005", " rendimiento", "getResponse", "renders"]

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
[{"token_id": 19, "token": "4", "logp": -0.03183978050947189, "p": 0.9686617851257324, "delta_logp": 3.05245041847229}, {"token_id": 17, "token": "2", "logp": -3.6568398475646973, "p": 0.025813959538936615, "delta_logp": 3.052450180053711}, {"token_id": 12937, "token": " Four", "logp": -6.656839847564697, "p": 0.0012852014042437077, "delta_logp": 3.864950656890869}, {"token_id": 16, "token": "1", "logp": -7.031839847564697, "p": 0.0008833050960674882, "delta_logp": -0.6975498199462891}, {"token_id": 23, "token": "8", "logp": -7.281839847564697, "p": 0.0006879187421873212, "delta_logp": -7.197549819946289}, {"token_id": 15, "token": "0", "logp": -7.406839847564697, "p": 0.0006070861127227545, "delta_logp": 0.05245018005371094}, {"token_id": 561, "token": " The", "logp": -7.781839847564697, "p": 0.0004172438057139516, "delta_logp": 3.864950656890869}, {"token_id": 37150, "token": " Dogs", "logp": -7.781839847564697, "p": 0.0004172438057139516, "delta_logp": 9.646200180053711}, {"token_id": 18, "token": "3", "logp": -7.906839847564697, "p": 0.00036821633693762124, "delta_logp": -1.822549819946289}, {"token_id": 21, "token": "6", "logp": -8.594339370727539, "p": 0.00018515090050641447, "delta_logp": -5.010048866271973}]
```

## Generation — first 32 tokens (preview)

```text
4

The animal is a dog, which is a domesticated canine known for its loyalty and ability to understand human commands. Dogs typically have a short history of
```

## Full continuation

```text
4

The animal is a dog, which is a domesticated canine known for its loyalty and ability to understand human commands. Dogs typically have a short history of being raised by humans, often serving as companions, hunters, or working partners. They are generally friendly and adaptable, making them popular family pets around the world.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-att-h20/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
