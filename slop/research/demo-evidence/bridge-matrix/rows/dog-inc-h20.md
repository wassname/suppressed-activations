---
row: dog-inc-h20
expected_answer: 4
observed_answer: 8
verdict: NO TRANSFER
tokens: 74
eos_count: 1
capped: False
canonical_r2_nonspecial: 0.000000
selector: increment
edit_site: h20
delta_anchor_layer: 20
---

# dog-inc-h20

- expected answer: 4 — observed: 8 — NO TRANSFER
- judgment: NO TRANSFER: coherent spider; the 'insects' mention = the web prey, not an identity error.
- readout (production-saved, detector readout — separate from the top-10 table):
  ["\u30fb\u30fb\u30fb\u30fb", "\u30fb\u30fb", "\u3055\u307e\u3056\u307e", "\u30fb\u30fb\u30fb\u3002", "\uff65\uff65\uff65", " powers", " answers", "\u30fb\u30fb\u30fb\u30fb\u30fb\u30fb\u30fb\u30fb"]

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
[{"token_id": 23, "token": "8", "logp": -0.32830101251602173, "p": 0.7201462388038635, "delta_logp": -0.24401076138019562}, {"token_id": 19, "token": "4", "logp": -1.453300952911377, "p": 0.23379726707935333, "delta_logp": 1.6309893131256104}, {"token_id": 16, "token": "1", "logp": -4.203300952911377, "p": 0.014946158975362778, "delta_logp": 2.1309890747070312}, {"token_id": 21, "token": "6", "logp": -4.703300952911377, "p": 0.009065303951501846, "delta_logp": -1.1190106868743896}, {"token_id": 17, "token": "2", "logp": -4.828300952911377, "p": 0.008000101894140244, "delta_logp": 1.8809890747070312}, {"token_id": 18, "token": "3", "logp": -5.328300952911377, "p": 0.004852307494729757, "delta_logp": 0.7559890747070312}, {"token_id": 20, "token": "5", "logp": -6.328300952911377, "p": 0.0017850641161203384, "delta_logp": 1.5059890747070312}, {"token_id": 15, "token": "0", "logp": -6.453300952911377, "p": 0.0015753136249259114, "delta_logp": 1.0059890747070312}, {"token_id": 22, "token": "7", "logp": -7.015800952911377, "p": 0.0008975865785032511, "delta_logp": 0.9434890747070312}, {"token_id": 57087, "token": "Eight", "logp": -7.265800952911377, "p": 0.0006990411784499884, "delta_logp": 1.3184895515441895}]
```

## Generation — first 32 tokens (preview)

```text
8

The animal is a spider, an arachnid known for its eight legs and ability to create intricate webs. They are typically found in various environments around
```

## Full continuation

```text
8

The animal is a spider, an arachnid known for its eight legs and ability to create intricate webs. They are typically found in various environments around the world, where they hunt by waiting for prey to become entangled in their silk. Despite their reputation for being dangerous, most spiders are harmless to humans and play an important role in controlling insect populations.<|im_end|>
```

Provenance: batchwork ../suppressed-activations-batchwork/out/2026-09-13_bridge-matrix-193115/dog-inc-h20/result.json
(runner row); producer task 1344; model Qwen/Qwen3.5-4B rev
851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
