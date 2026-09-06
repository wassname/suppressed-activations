# Research journal

## 2026-09-06 -- Causal replacement depends on prompt format and token aggregation

This entry records the search for a spider-to-dog causal replacement that changes both the answer and the recomputed readout.

| model input and method | decoded answer | p(4) | p(8) | exact donor-readout overlap |
|---|---:|---:|---:|---:|
| raw Base | 8 | 0.056421 | 0.882568 | not applicable |
| raw, union, L24, last four source tokens, C=2 | 4 | 0.477770 | 0.421631 | 5/8 |
| raw, union, L24+L26, final source token, C=2 | 4 | 0.687441 | 0.252896 | 4/8 |
| user-message chat template, best tested L24 readout | 8 | about 0.000001 | about 0.0006 | 5/8 |

`p(4)` and `p(8)` are next-token probabilities at the first generation boundary. The exact-overlap column counts identical entries shared by the causal and unmodified donor top-eight readouts. Evidence: [raw layer combinations](out/2026-09-06_211653_layer-combo-raw/run.md), [chat layer combinations](out/2026-09-06_211800_layer-combo-chat-fact/run.md), and [default replication](out/2026-09-06_213629_causal-demo/conditions/000_default_default/run.md).

The raw L24, last-four, C=2 continuation was:

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

The corresponding recomputed readout was:

```python
['狗粮', '吠', 'สุนัข', ' собаки', ' canine', ' собак', ' perros', ' cão']
```

The hard-min persistent selector returned arbitrary-looking vocabulary because sparse nonnegative scores tied at zero. Replacing it with mean score times positive-position fraction removed the hard tie, but all tested persistent conditions still answered 8. The union selector reproduced the dog-like readout and answer change. Evidence: [hard-min run](out/2026-09-06_213326_persistent-direction-raw/run.md) and [soft-persistence run](out/2026-09-06_213454_persistent-direction-raw/run.md).

My read: it is very probable that the extra instruction and chat response format changed which state exists at the first generation boundary. It is likely that the union captures useful token-specific directions which the tested persistence reductions discard. A chat template with an assistant-prefilled partial fact is the next discriminator because it uses the official template while preserving digit-first completion.

The current evidence supports the raw union intervention and leaves the chat-template demonstration unresolved.

<!-- Written by Codex/gpt-5.6-sol. -->
