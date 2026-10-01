# Native-v4 launcher review

## Blocking finding

**P1 — Coverage schema mismatch stops the launcher after capture, before rescoring.**

- `/workspace/2026/suppressed-activations/slop/audits/2026-10-01_native-v4-launcher.py:111`:
  > `[c['sequence_length'] for t in traces for c in t['coverage']]`
- `/workspace/2026/suppressed-activations/scripts/english/08_jlens_one_pass.py:405,411`:
  > `coverage = ... {b + 1: [] for b in {read_block, 26, 31}}`  
  > `coverage[residual_index].append(h.shape[1])`

**Observed source:** coverage is a dictionary mapping residual-layer indices to lists of sequence lengths, not a list of event dictionaries.

**Predicted behavior:** after any successful eight-case capture, JSON dictionary iteration yields strings such as `"24"`; indexing these with `'sequence_length'` raises `TypeError`. Replay, the 32 candidate rows, and the master summary are never reached. Captured scientific artifacts remain available; this is an execution blocker, not evidence against the method.

**Check that could disprove it:** exercise this exact assertion against a production capture trace. A successful result would require a different coverage schema than the reviewed source produces. Compare forward lengths with one layer’s coverage, while checking agreement across layers; do not concatenate all three layers.

## Coverage and limitations

Read all supplied files completely, including both instruction files and the ML-debug skill. No commands, inference, edits, network access, or delegation.

Source inspection supports:
- Exact eight-case transformation and unchanged labels/order; no old demonstration.
- Native-chat rendering, greedy 32-token cap, EOS union, verbatim/scoring-text separation, and failure retention.
- Same-generation prefill capture, disabled gradients, and no enabled current-input preparation branch.
- Replay guards on both full-model and inner-transformer calls.
- Exact legacy-row comparison and expected 144+32 cardinality.
- Source/data/contract/helper pins and copied provenance.
- Labels and generated text used for evaluation, not candidate ranking or prefix-mask construction.

**Postflight limitation:** launcher `check_replay` checks saved-score method keys and exclusion membership, but does not reconstruct candidate rankings from saved tensors. The smoke log reports reconstruction checks; those test implementations were outside scope.

**Execution evidence:** launcher-check.log explicitly says:
> “Full new launcher not yet exercised end-to-end”

The smoke log reports successful seed0/1 production capture/replay tests, including transformer blocking and score reconstruction, ending:
> “PASS tiny random CPU model only; no pretrained scientific generations”

These are implementation evidence, not new-v4 scientific results. Existing2673/2686 postflight evidence does not test the broken orchestration assertion.

Semantic purity, coherent-answer accuracy, paired gains, and the declared example-selection rule remain post-run review work. Their absence is a reporting limitation, not another demonstrated scientific blocker. Runtime, peak memory, actual EOS IDs, hash validity, and new-v4 outcomes were not independently executed or verified.

— PI/OpenAI