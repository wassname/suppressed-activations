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

## 2026-09-06 -- Executed notebook reproduces the chat intervention

This entry records the final notebook execution rather than the preceding sweep.

| condition | first answer | p(4) | p(8) | suppressed readout |
|---|---:|---:|---:|---|
| Base | 8 | 0.028546 | 0.945299 | web-related |
| Causal intervention | 4 | 0.701417 | 0.200959 | dog-related |

The causal table reports `delta log p(4)=+3.202` and `delta log p(8)=-1.548` relative to Base.
Both continuations contain exactly thirty-two generated tokens. They begin with the different
answers and then identify the unchanged subject as a spider. Evidence: [executed
notebook](nbs/demo.ipynb) from pueue job 406.

My read: the notebook is a successful single-example causal demonstration under the requested
L24, final-four-token prior, with C increased from the unsuccessful value of two to the smallest
tested crossing at two and a half. The causal interpretation remains limited by configuration
selection on this prompt and by the possibility that the intervention transfers an answer state
rather than animal identity.

The public notebook now contains the complete result needed to inspect this example.

<!-- Written by Codex/gpt-5.6-sol. -->

## 2026-09-07 -- Fixed spider-to-ant transfer fails

This entry tests whether the selected spider-to-dog configuration transfers to an ant donor.

| condition | first token | p(6) | p(8) | swap log-odds change |
|---|---:|---:|---:|---:|
| Base | 8 | 0.015245 | 0.943160 | 0.000 |
| C=2 | 8 | 0.008095 | 0.935690 | -0.625 |
| C=2.5 | 8 | 0.007667 | 0.886223 | -0.625 |
| C=3 | 8 | 0.006092 | 0.797945 | -0.750 |
| C=4 | 2 | 0.004487 | 0.403940 | -0.375 |

The swap log-odds change is the intervention-induced change in `log p(6) - log p(8)`.
The fixed held-out condition is C=2.5; the other rows are a diagnostic strength sweep. The
unmodified donor readout was `['Social', 'social', ' vor', 'V', ' vaya', 'ocial', ' sociales',
' división']`. Evidence: [job 485 run table](out/2026-09-07_182300_chat-ant-strength/run.md)
and [fixed C=2.5 condition](out/2026-09-07_102128_chat-ant-heldout/conditions/000_default_default/run.md).

The clean donor generated `6.` followed by an explanation that identified the animal as an ant,
with `p(6)=0.899812`. Evidence: [job 487 donor check](out/2026-09-07_183000_chat-ant-donor-check/conditions/000_default_default/run.md).

My read: the current spider-to-dog demo is probably pair-specific. The ant result is more
consistent with a detector that selected an unrelated subspace than with an intervention that was
only too weak, because every tested strength reduced the target answer probability even though the
clean donor answered correctly. The donor readout may encode the prompt's social-colony feature
rather than the answer, so a different ant wording could distinguish prompt-specific detector
failure from a broader lack of transfer. That would be a new development test rather than part of
this held-out result.

The fixed configuration does not produce a working ant demonstration.

<!-- Written by Codex/gpt-5.6-sol. -->
