# Job 93 audit

Target: pueue job 93 enlarged job 92's fixed C=2 matched-random sample from 32 to 256 seeds without changing extraction or intervention settings. It ran at git revision `v0.1.1-12-g45e692b` and exited 0. Sources: [`job_93_script.py`](job_93_script.py), [`job_93_full.log`](job_93_full.log), [`job_93_summary.log`](job_93_summary.log), and [`../research/spider_dog_c2_256.json`](../research/spider_dog_c2_256.json).

| stage | expected | observed | expected? | consequence |
|---|---|---|---|---|
| semantic reproducibility | same C=2 result as job 92 | log odds +0.625, top=`4` | yes | deterministic result reproduced |
| control enlargement | seeds 0–31 reproduce and 224 new controls complete | 256 rows persisted | yes | tail estimate is less discrete |
| relative effect | semantic remains above ≥95% of controls | 248/256 below semantic (96.875th percentile) | yes | selected effect remains uncommon under matched random directions |
| random top-1 | random directions sometimes flip the answer at this budget | 13/256 produce top=`4` | yes | top-1 flip alone is weak evidence |
| empirical tail | quantify controls at least as strong | 8/256; smoothed one-sided p=9/257=0.0350 | yes | descriptive only because C=2 was selected after job 90 |

## Primary evidence

> semantic_C2_log_odds=+0.625000
> random_below_semantic=248/256
> random_at_least_semantic=8/256
> semantic_percentile_strict=96.8750
> random_top4=13/256
> empirical_one_sided_p=0.035019
> random_mean=-2.327148
> random_min=-5.000000
> random_max=+2.250000

Source: [`job_93_summary.log`](job_93_summary.log).

## Hypotheses

### H1 [method | Highly Likely | 80%]
- **Mechanism:** the separately found dog component targets the dog-appropriate answer more strongly than a typical equal-budget direction.
- **Evidence:** the semantic effect is at the 96.875th percentile of 256 matched controls and reproduces job 92 exactly.
- **Contrary evidence:** eight controls are at least as strong; source/target and C=2 were selected through earlier exploratory runs.
- **Discriminating test:** freeze the complete rule and run new source-target pairs.
- **Action:** publish this as a selected example with `248/256`, not a population success rate.
- **Interpretability:** yes as exploratory causal evidence.

### H2 [control | Likely | 65%]
- **Mechanism:** large equal-budget random rotations often disrupt the answer, and some happen to favor `4` because 4 is already the clean runner-up.
- **Evidence:** 13/256 random controls make `4` top-1; clean p(4)=0.056 and rank 2.
- **Contrary evidence:** only eight match the semantic log-odds effect; semantic selection is related to dog content.
- **Discriminating test:** use another target answer that is not the clean runner-up, or compare target-rank change across new pairs.
- **Action:** plot the full log-odds distribution rather than claiming that random never flips.
- **Interpretability:** yes.

### H3 [statistics | Almost Certain | 95%]
- **Mechanism:** the p=0.035 value is descriptive because strength C=2 was chosen after inspecting job 90.
- **Evidence:** job 90's dose sweep selected the top-1-flipping strength before jobs 92–93.
- **Contrary evidence:** random seeds 32–255 were unseen, so the expanded control tail itself was held out.
- **Discriminating test:** predeclare C=2 on a new pair before running either semantic or random effects.
- **Action:** report the empirical count and selection history; do not call it confirmatory significance.
- **Interpretability:** yes.

## Decision

1. **Resolve-condition verdict:** met. The exact semantic percentile and tail are recorded without changing the rule.
2. **Prediction check:** the effect remained above 95% of controls — supported; random top-1 flips were more common than the 32-seed run suggested — 13/256 observed.
3. **Earliest unsupported link:** pair-level replication. A frozen new pair would support it.
4. **Validity:** valid for this selected sample and fixed random-control comparison, about 0.90–0.97; not confirmatory evidence of generality.
5. **Highest-information clues:** 248/256 strict rank, 13/256 random top-1 flips, exact reproduction of semantic logits.
6. **Missing metrics:** new-pair effects and a target that is not the clean runner-up.
7. **Bugs requiring code changes:** none observed.
8. **Misconceptions requiring reinterpretation:** top-1 flip is not sufficient; the log-odds location within the random distribution is the useful comparison.
9. **What would change the verdict:** many predeclared pair replications would support generality; failure would retain only the selected-example claim.
10. **Recommended next action:** convert this exact path into the public script, figure, and notebook; keep the multilingual result as provenance and the held-out scan in the audit trail.

Written by PI/gpt-5.4.
