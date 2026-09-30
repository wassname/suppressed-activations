Task2655 is inconclusive, not a scientific 0/8 result. Same-family review by PI/OpenAI.

Paths below use `R = /workspace/2026/suppressed-activations/out/2026-10-01_020831_jlens-one-pass/`.

Observed: all five `R/console.log` lines comprise “Loading pinned model; no input-specific preparation” and weight-loading progress through “426/426”. `R/job.json` records exit124 and approximately300s elapsed. The first message occurs approximately257s after task start; nothing identifies what consumed that interval. `R/artifact_timestamps.json` records dictionary persistence, then one cached trace. `R/source.py` copies replay tokens before scoring. That trace is not new generation or a completed case.

Top static risks/misconceptions:

1. **Incomplete execution provenance.** `R/launcher.py` checks helper/cache/data hashes, but source equality and helper persistence occur after `ns['main'](...)` returns. Source is checked for stability, not against a predetermined digest. Imported helper implementations and dependency versions are outside this bounded evidence. Check supplied source/data digests and completed postflight assertions on retry; present evidence cannot establish full execution equivalence.

2. **Resource exposure remains.** `R/source.py` loads the full model with `.cuda().eval()` even for replay, then constructs dense dictionaries using `(W.float() * gain) @ J`. Chunked normalization does not bound these full allocations. This affects every replay input; it establishes neither OOM nor the timeout cause. Completion and peak-memory measurements would test whether this blocks the proposed budget.

3. **Alias recovery is not semantic certification.** `R/launcher.py` explicitly says “Aliases are incomplete; prior absence is not semantic certification or counterfactual necessity.” Eight development cases and two prefix diagnostics cannot establish generalization or necessary hidden reasoning. Inspect all paired gains/losses before advancing.

Cheapest next test: the proposed unchanged-method repeat. The inspected `slop/audits/2026-10-01_pursuit-launcher.py` adds stage timestamps and repeated120s snapshots while retaining the main invocation. Preflight versus import timestamps distinguish those intervals; snapshots localize unfinished work without proving its cause. The600s+15s outer deadline remains a proposal, not verified execution evidence. This review need not gate that repeat.