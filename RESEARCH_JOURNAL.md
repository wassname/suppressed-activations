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

## 2026-09-06 -- Assistant-prefill chat crosses at moderate strength

This entry resolves the earlier chat-template question with an assistant-prefill format.

| C | first answer | p(4) | p(8) | exact donor-readout overlap |
|---:|---:|---:|---:|---:|
| 2.0 | 8 | 0.373941 | 0.544081 | 3/8 |
| 2.5 | 4 | 0.684335 | 0.196065 | 4/8 |
| 3.0 | 4 | 0.809186 | 0.066422 | 5/8 |
| 4.0 | 4 | 0.824805 | 0.019398 | 6/8 |

Here, `C` scales the constructed component replacement, and `p(4)` and `p(8)` are next-token
probabilities at the first generation boundary. Every condition used the tokenizer's chat template
for extraction and generation, with the incomplete fact as an assistant-message prefill. Evidence:
[job 405 run table](out/2026-09-06_220932_chat-strength/run.md) and
[C=2.5 condition log](out/2026-09-06_220932_chat-strength/conditions/001_strength_C=2.5/run.md).

The continuation at the smallest measured crossing was:

```text
4.

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which is
```

The recomputed readout at that condition was:

```python
['狗粮', '吠', 'สุนัข', ' собаки', '养犬', ' собак', ' perros', ' dogg']
```

My read: C=2.5 is a better notebook setting than the C=2 prior because it is the smallest tested
value that changes the greedy answer while retaining a grammatical, on-topic continuation. This is
a selected single-prompt result, so it does not show that the method transfers a reusable dog
concept rather than a target-answer state.

The assistant-prefill chat demonstration now changes both the answer and the suppressed readout.

<!-- Written by Codex/gpt-5.6-sol. -->
