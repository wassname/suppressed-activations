# Polar readout audit

**Result:** The recorded negative result is supported; no arithmetic/dataflow defect was confirmed in the inspected evidence. This is not full implementation certification: earlier large-file responses were truncated, leaving complete source/artifact coverage unverified. All 56 compact rows and all 679 console lines were subsequently inspected.

## Findings and limits

- **Counts agree.** `.local/status-check/job2642-polar-readouts.jsonl` records Q/J/plain24/plain27/mismatch/unsubtracted/early-prefix passes of **1/4/1/5/1/1/0 out of eight**, matching `out/2026-09-30_205519_jlens-one-pass/console.log`. Q’s sole pass is Thursday, also passed by mismatch and unsubtracted. Thus these inputs show neither superiority nor subtraction benefit.

- **AUROC is not retrieval success.** In `out/2026-09-30_205519_jlens-one-pass/readout.json`, triangle’s polar-unsubtracted row has `"alias_checked_auroc": 0.9985815286636353` but `"alias_checked_hidden_found": false`. The compact violin row similarly reports AUROC 0.9478 and failure despite displaying `提琴`. These observations support an English-token retrieval failure, not absence of semantic information. A separately preregistered multilingual evaluation could test that distinction; retroactively changing aliases would not repair this result.

- **Controls cannot establish suppressed reasoning.** `out/2026-09-30_205519_jlens-one-pass/console.log` explicitly states: “Early prefix misses later topic priors” and “Other-label sets are not topic-matched.” Full-versus-prefix gains therefore remain compatible with ordinary topical activation. Topic-matched counterfactuals would distinguish that alternative; they were not run here.

- **Denominator matters.** The same console records violin’s baseline as `"the woodwind family"`; the report’s expected-answer denominator is seven, versus eight for actual-output evaluation. Neither denominator should be described as eight correct-answer trials.

**Uncertainty:** `verification.json` records independent reconstruction success, but no verification commands were executed during this review. Complete untruncated source review and replay of the supplied checker could disprove the tentative absence of implementation defects. The negative result applies to this fixed candidate and development set—not all polar readouts, hidden concepts, or causal editing.

— **PI/OpenAI**