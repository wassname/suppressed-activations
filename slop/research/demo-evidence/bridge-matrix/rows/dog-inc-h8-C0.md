---
row: dog-inc-h8-C0
expected_answer: 4
observed_answer: 8
verdict: CONTROL (C0, zero edit)
tokens: 58
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: increment
edit_site: h8
delta_anchor_layer: 20
---

# dog-inc-h8-C0

- expected answer: 4 — observed: 8 — CONTROL (C0, zero edit)
- judgment: CONTROL: identical to the paired Base generation (zero edit).
- readout (production-saved, detector readout — separate from the top-10 table):
  [" respuesta", " risposta", "getResponse", "\u62e5\u6709\u7740", " resposta", "response", "_response", " respond"]

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
[{"token_id": 23, "token": "8", "logp": -0.08429025113582611, "p": 0.9191644191741943, "delta_logp": 0.0}, {"token_id": 19, "token": "4", "logp": -3.0842902660369873, "p": 0.045762501657009125, "delta_logp": 0.0}, {"token_id": 21, "token": "6", "logp": -3.5842902660369873, "p": 0.027756361290812492, "delta_logp": 0.0}, {"token_id": 18, "token": "3", "logp": -6.084290027618408, "p": 0.0022783814929425716, "delta_logp": 0.0}, {"token_id": 16, "token": "1", "logp": -6.334290027618408, "p": 0.0017744052456691861, "delta_logp": 0.0}, {"token_id": 17, "token": "2", "logp": -6.709290027618408, "p": 0.0012195296585559845, "delta_logp": 0.0}, {"token_id": 15, "token": "0", "logp": -7.459290027618408, "p": 0.0005760649801231921, "delta_logp": 0.0}, {"token_id": 20, "token": "5", "logp": -7.834290027618408, "p": 0.00039592329994775355, "delta_logp": 0.0}, {"token_id": 22, "token": "7", "logp": -7.959290027618408, "p": 0.0003494011180009693, "delta_logp": 0.0}, {"token_id": 57087, "token": "Eight", "logp": -8.584290504455566, "p": 0.00018702083616517484, "delta_logp": 0.0}]
```

## Generation — first 32 tokens (preview)

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect
```

## Full continuation

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect its eggs. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-inc-h8-C0/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
