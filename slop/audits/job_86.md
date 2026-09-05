# Job 86 audit

Target: pueue job 86, `uv run python /tmp/scan_animal_targets.py`, in `/workspace/2026/suppressed-activations`; it ran 2026-09-05 15:09:00–15:09:12 +08 and exited 1. The executed temporary script is preserved as [`job_86_script.py`](job_86_script.py). Exact git provenance was meant to be written only after the loop, so the crash prevented it; imported tracked code had no local diff, but this is weaker than run-time metadata.

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| model/extraction | Qwen3.5-4B residuals at L23/L25/L32 | weights loaded; spider and bee rows printed | yes | `job_86_full.log:1-7` | per-case residual checks | first two rows are usable |
| held-in source | spider clean `8`, hidden rank ≤32 | clean `8`, rank 6 | yes | `job_86_full.log:6` | prompt-echo control | source rule remains plausible, not established |
| held-out target | a correct answer and hidden animal rank ≤32 | bee clean `6`, rank 3726 | no | `job_86_full.log:7` | remaining ten targets | bee rejects the criterion; family scan incomplete |
| vocabulary validation | each named concept has a one-token LM-head row | `firefly` had no one-token variant | no | `job_86_repro.log:1-4` | preflight validation | indexing an empty ranking crashed |
| artifact persistence | JSON with all rows and run metadata | absent because write occurs after loop | no | `job_86_script.py:86-99` | complete result file | no full scan result exists |
| resolve condition | advance only a correct target with rank ≤32 | no passing target before crash | unclear | job label; `job_86_status.json` | unexecuted targets | condition is not judgeable for the planned scan |

## Chronology and primary evidence

The full cleaned log is 12 of 12 lines in [`job_86_full.log`](job_86_full.log). The model loaded and the held-in case behaved as predicted:

> hidden=spider     expected= 8 top='8'          correct=True  rank=      6 top12=['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB', ' стане', 'amet', '.att', ' Bomb']

The first held-out case answered correctly but missed the hidden-concept threshold by over two orders of magnitude:

> hidden=bee        expected= 6 top='6'          correct=True  rank=   3726 top12=[' Sting', 'Kate', ' fungerer', ';font', ' 인프라', 'Disc', ' городу', '在校园', '中国品牌', '화로', 'راتيج', 'Added']

The next case crashed before its row was printed:

> best_rank, best_variant, _ = ranked[0]
> IndexError: list index out of range

The standalone reproduction used the same tokenizer and exact candidate strings:

> [('firefly', [10479, 20979]), (' firefly', [3807, 20979]), ('Firefly', [16207, 20979]), (' Firefly', [6438, 20979]), ('fireflys', [10479, 20979, 82]), (' fireflys', [3807, 20979, 82])]
> one_token_variants: []
> next operation: ranked[0]
> IndexError: list index out of range

Source: [`job_86_repro.log`](job_86_repro.log). This almost certainly localizes the crash: `variants()` retains only length-one encodings (`job_86_script.py:31-37`), then line 66 assumes at least one remains.

## Hypotheses

### H1 [bug | Almost Certain | 99%]

- **Mechanism:** `firefly` has no one-token encoding, so `ranked` is empty and `ranked[0]` raises.
- **Evidence:** [`job_86_repro.log`](job_86_repro.log) says `one_token_variants: []` followed by `IndexError: list index out of range`; [`job_86_script.py:61-66`](job_86_script.py) shows the unguarded index.
- **Contrary evidence:** None; the failure reproduced without model inference.
- **Discriminating test:** validate every concept's variants before loading the model. Zero invalid concepts means this cause is absent; any zero-length result predicts the same crash.
- **Fix/action:** fail before model load with the offending concept list, then use only atomic concepts for this unchanged scoring test.
- **Interpretability:** partial; spider and bee rows precede the crash, but the planned scan does not.

### H2 [method | Likely | 65%]

- **Mechanism:** the row-normalized L23/L25/L32 rule is specific to spider rather than shared across indirectly described animals.
- **Evidence:** [`job_86_full.log:7`](job_86_full.log) reports the correct bee answer but hidden rank 3726 against the predeclared rank-32 threshold.
- **Contrary evidence:** only one held-out atomic animal completed, so a later target can still pass.
- **Discriminating test:** rerun all prevalidated atomic targets under the unchanged layers and score. Multiple rank-≤32 targets support a family rule; none supports source specificity.
- **Fix/action:** finish the target scan before any intervention or layer change.
- **Interpretability:** yes for bee; it is a credible negative under the fixed rule.

### H3 [measurement | Chances a little better than even | 55%]

- **Mechanism:** spider's rank 6 partly measures lexical prompt echo from `webs`, not an inferred latent animal.
- **Evidence:** [`job_86_full.log:6`](job_86_full.log) places `-web`, `Web`, `Spider`, `web`, and `WEB` together in the top 12 while the prompt says `spins webs`.
- **Contrary evidence:** the exact token `Spider` is not stated in the prompt and ranks 6; prompt-token exclusion alone would not remove it.
- **Discriminating test:** use matched descriptions that imply spider without a `web` morpheme, such as eight-legged arachnid descriptors, and compare spider rank under the fixed rule.
- **Fix/action:** add a lexical-overlap control only after the fixed held-out scan, so the scan rule remains unchanged.
- **Interpretability:** partial; the rank is real, but its interpretation as hidden reasoning is not secure.

## Decision

1. **Resolve-condition verdict:** not judgeable. The condition was “advance only hidden rank at most 32 and correct clean top-1”; bee did not pass, and ten planned targets did not produce rows.
2. **Prediction check:** spider rank ≤32 — supported (rank 6); each held-out candidate advances only if clean-correct and rank ≤32 — bee contradicted it (rank 3726), remaining candidates unresolved.
3. **Earliest unsupported link:** candidate vocabulary validity. A preflight showing at least one atomic token variant per concept supports it.
4. **Validity:** “invalid” means the artifact represents the full planned candidate scan. `P(full-scan result is invalid) ≈ 0.98–1.00`; classification: invalid overall, with a credible negative bee row.
5. **Highest-information clues:** (1) exact tokenizer reproduction of the empty variants; (2) bee's correct answer but rank 3726; (3) spider's top-12 cluster is dominated by web variants.
6. **Missing metrics:** (1) remaining atomic target ranks; (2) lexical-overlap control for spider; (3) matched-random intervention only if a target passes.
7. **Bugs requiring code changes:** H1 → prevalidate atomicity before loading Qwen and report invalid candidates explicitly.
8. **Misconceptions requiring reinterpretation:** H3 → do not call spider rank 6 evidence of an abstract intermediate until it survives a lexical-overlap control.
9. **What would change the verdict:** a complete rerun with run-time git metadata and all valid candidate rows would make the scan judgeable; at least one held-out correct rank-≤32 target would meet the screening condition.
10. **Recommended sequence:** first preflight and remove non-atomic concepts without changing layers or score; rerun the same fixed rule; only then test an intervention. Changing token aggregation and layers together would destroy attribution.

Written by PI/gpt-5.4.
