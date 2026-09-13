---
row: dog-inc-h8
expected_answer: 4
observed_answer: 8
verdict: NO TRANSFER
tokens: 19
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.117647
selector: increment
edit_site: h8
delta_anchor_layer: 20
---

# dog-inc-h8

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: mild repetition (canonical r2 .117647): 'The animal is the spider. It has eight legs. It is a spider.'
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", "getResponse", " resposta", "response", "_response", " respond", " response"]

## Exact input (repr)

```python
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

In this increment-recipe row the union basis U was built from the source AND donor prompt trajectories (multi-token selection); the injected component is the template-mean delta projected on that U. The donor input (rendered):

```python
"<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that barks and is called man's best friend have?\nAnswer: "
```

## First-position top-10 output table (log p / p)

```json
[{"token_id": 23, "token": "8", "logp": -0.11348673701286316, "p": 0.8927160501480103, "delta_logp": -0.02919648587703705}, {"token_id": 19, "token": "4", "logp": -2.3634867668151855, "p": 0.09409157931804657, "delta_logp": 0.7208034992218018}, {"token_id": 17, "token": "2", "logp": -5.7384867668151855, "p": 0.0032196366228163242, "delta_logp": 0.9708032608032227}, {"token_id": 18, "token": "3", "logp": -5.9884867668151855, "p": 0.002507455414161086, "delta_logp": 0.09580326080322266}, {"token_id": 21, "token": "6", "logp": -6.1134867668151855, "p": 0.002212821738794446, "delta_logp": -2.5291965007781982}, {"token_id": 16, "token": "1", "logp": -6.3634867668151855, "p": 0.00172334723174572, "delta_logp": -0.029196739196777344}, {"token_id": 20, "token": "5", "logp": -7.3634867668151855, "p": 0.0006339840474538505, "delta_logp": 0.47080326080322266}, {"token_id": 22, "token": "7", "logp": -7.4884867668151855, "p": 0.0005594889516942203, "delta_logp": 0.47080326080322266}, {"token_id": 15, "token": "0", "logp": -7.6759867668151855, "p": 0.0004638326645363122, "delta_logp": -0.21669673919677734}, {"token_id": 24, "token": "9", "logp": -8.050986289978027, "p": 0.0003187873517163098, "delta_logp": 1.033304214477539}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is the spider. It has eight legs. It is a spider.<|im_end|>
```

## Full continuation

```text
8

The animal is the spider. It has eight legs. It is a spider.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-inc-h8/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
