# Audit of pueue job 63

Job 63 tested whether a sample-specific component selected by the LM-head rise-and-fall score changes the next token when it is replaced by another sample's selected component.

Command, recorded in [`job_63_status.json`](job_63_status.json):

```bash
uv run --project ../do_qwens_reason_in_english python scripts/demo.py --output data/causal_demo.json
```

## Result

The complete 94-line log reports:

> source selected: [' heart', ' hearts', ' Heart', '-heart', ' Cards', ' jantung', ' cards', ' cardiac']  
> target selected: [' school', ' schools', ' scho', ' Schools', ' szko', ' School', ' المدرسة', 'عودة']  
> base: top='心' p(心)=0.5609 p(学校)=0.0000 log p(学校)/p(心)=-12.83 KL=0.000  
> replace: top='学校' p(心)=0.1099 p(学校)=0.1245 log p(学校)/p(心)=+0.12 KL=1.345

Source: [`job_63_full.log:6-9`](job_63_full.log#L6-L9).

All 32 matched-random replacements retain `心` as the top token. Their log probability ratios range from -13.67 to -11.66; the full rows are at [`job_63_full.log:10-41`](job_63_full.log#L10-L41). Removal retains `心` but lowers its probability:

> remove: top='心' p(心)=0.1860 p(学校)=0.0000 log p(学校)/p(心)=-9.77 KL=0.755

Source: [`job_63_full.log:42`](job_63_full.log#L42).

Interpretation: the semantic component replacement causes a large and target-specific shift on this prompt. This is very probable because the effect lies outside all 32 matched-random results and changes the greedy token. It does not establish transfer or show that suppression itself is causal.

## ML-debug form

| row | answer |
|---|---|
| log length; config | 94 lines. Qwen3.5-4B, rank 8, L22/L27/L32 extraction, residual L23-L30 intervention, committed code `67c683e`; config is stored in `data/causal_demo.json:metadata`. |
| each `SHOULD:` and observed line | The run has no `SHOULD:` lines. The queued decision required rank-1 heart/school selections, replaced top-1 学校, 32 random top-1 心, and four generations. Lines 6-9 and 10-41 satisfy the first three; lines 51-60 contain the four generations. |
| each cited number under a null | Base ratio -12.83; matched-random range -13.67 to -11.66; semantic +0.12; removal -9.77. These come from lines 8-42. |
| init/before update | No training or update occurs. The clean model predicts 心 with probability 0.5609 at line 8. |
| dummy at each stage | Thirty-two random rank-8 replacements match residual norm and per-layer perturbation norm. All retain 心; none approaches zero log odds. |
| baseline on val/held-out | This is a selected held-in demonstration, not a validation estimate. The baseline is the same prompt without hooks. |
| schedule | Not applicable; no optimization. |
| one full sample | Prompt and token IDs are in `data/causal_demo.json`; all 64-token outputs are quoted at lines 51-60. The replacement begins `学校 ... means "school"`, then detects the conflict with Herz and corrects itself. |
| worst step | No loss, gradient, or update. At C=2 the generation degenerates into a multiple-choice list, lines 84-93. |
| surprises | `replace_C=+0.5` says `心 ... means "school"` at line 80; the target concept enters the explanation before it changes the output token. Explained: a graded semantic intervention. `C=+2` degenerates at lines 84-93; explained: excessive intervention. |
| missing evidence | A prompt set, a different model, a semantically loaded non-suppressed target control, and random seeds over prompts are required for a general claim. |
| diagnoses | 60%: the selected source/target components carry the intended concept; for: rank-1 words, graded sweep, matched random; against: one selected pair. 20%: generic target residual content explains the result; for: target comes from a separate pass; against: random projections of that residual do not move the answer. 10%: evaluation leak; for: pair was selected after exploration; against: answer labels never enter extraction. 10% unknown. |
| fresh review | [`20260905_causal_demo_fresh_eyes.md`](../reviews/20260905_causal_demo_fresh_eyes.md) says: “This shows a causal effect on this sample, not transfer to a new prompt.” It flags omitted noisy basis rows, a thin final margin, and the lack of a semantically loaded non-suppressed control. README and Figure 2 now show all eight rows and the absolute probabilities. |
| cheapest separating test | Across many prompt pairs, compare the rise-and-fall subspace with another target-derived semantic subspace at identical rank and perturbation norm. The intended explanation predicts a larger target-token shift for rise-and-fall; generic target-content injection predicts similar shifts. |
| wall clock and GPU | Status records 50.9 seconds from start to end. Peak GPU memory was not logged. Model loading dominates; keeping the model resident would shorten repeated tests. |

## Alternative causes and controls

The headline number is the change in `log p(学校) - log p(心)`. Removing the source component alone shifts it by 3.06 nats, so part of the replacement effect comes from reducing the source concept. Adding the matched school component accounts for the remaining 9.89-nat shift. This arithmetic is descriptive, not an independent causal decomposition because the final norm restoration is nonlinear.

A useless method could score well by injecting any feature from the school prompt. The matched-random control rejects content-free perturbations at the same rank and norm, but it does not reject another semantic target-derived subspace. The README states this remaining comparison explicitly.

## Decision

Use this as a selected, sample-specific causal demonstration. Do not report it as transfer, frequency, or proof that suppression causes the computation.

Written by PI/gpt-5.4.
