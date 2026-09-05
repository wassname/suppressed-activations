# Job 92 audit

Target: pueue job 92 tested the observed C=2 spider→dog component replacement against 32 equal-norm, equal-distance random replacements and generated with the intervention active only during prompt prefill. It ran at git revision `v0.1.1-12-g45e692b` and exited 0. Sources: [`job_92_script.py`](job_92_script.py), [`job_92_full.log`](job_92_full.log), [`job_92_summary.log`](job_92_summary.log), [`../research/spider_dog_c2_trial.json`](../research/spider_dog_c2_trial.json).

| stage | expected | observed | expected? | consequence |
|---|---|---|---|---|
| semantic C=2 | flip top-1 from 8 to 4 | p(4)=0.519, p(8)=0.278, top=`4` | yes | visible answer change |
| matched controls | semantic log odds above ≥95% of 32 controls | above 31/32; one random control was stronger and also top=`4` | yes | effect is specific by the chosen percentile rule, not unique |
| prompt-only generation | coherent continuation starting with 4 | `4. Hypothesis: ... has 4 legs.` | yes | avoids decode-time token repetition |
| random shown in generation | remain coherent and preferably unchanged | seed 0 starts with 8 | yes | illustrative only; the distribution is the control |
| removal | change source answer if the source component alone is necessary | remains 8 | no | removal remains negative evidence |

## Primary evidence

> base_log_odds=-2.750000
> semantic_C2_log_odds=+0.625000
> random_below_semantic=31/32
> random_top4=1/32
> empirical_one_sided_p=0.060606

Source: [`job_92_summary.log`](job_92_summary.log). The C=2 strength was chosen after job 90's dose sweep showed the top-1 flip; it is exploratory rather than held out.

The prompt-only continuation is coherent:

> replace_C=+2 '4.\nHypothesis: The animal that spins webs has 4 legs.\nIs the hypothesis entailed by the fact? ...'

The corresponding base starts:

> base '8.\nHypothesis: The animal that spins webs has 8 legs. ...'

## Hypotheses

### H1 [method | Highly Likely | 80%]
- **Mechanism:** the dog subspace replacement changes the spider prompt toward the dog-appropriate answer.
- **Evidence:** target-vs-source log odds move by 3.375 nats, top-1 flips, the output remains coherent, and 31/32 matched random effects are smaller.
- **Contrary evidence:** one random perturbation is stronger; C=2 was selected after inspection.
- **Discriminating test:** freeze C=2 and test new animal pairs or prompt paraphrases.
- **Action:** use this as one selected causal example with its control distribution and selection history.
- **Interpretability:** yes as exploratory evidence.

### H2 [evaluation | Likely | 65%]
- **Mechanism:** 32 controls are too few to estimate a small tail probability precisely.
- **Evidence:** with one control at least as strong, the smoothed empirical value is 2/33≈0.061 despite the 96.875th percentile rank.
- **Contrary evidence:** the planned discriminator was percentile rank, which passes.
- **Discriminating test:** run at least 256 fixed-seed matched controls without altering semantic settings.
- **Action:** increase controls before publishing a probability claim; otherwise report only `31/32`.
- **Interpretability:** yes.

### H3 [mechanism | Plausible | 40%]
- **Mechanism:** the target component acts through an answer association rather than a distinct dog intermediate.
- **Evidence:** the only measured downstream task maps dog to 4.
- **Contrary evidence:** target-free selected tokens are dog-related, not `4`, and persistent C=1 later verbalized `dog`.
- **Discriminating test:** compare against a direct 4-direction intervention or use the dog component in a different downstream task.
- **Action:** say the component replacement redirects the answer; do not claim a unique mechanistic route.
- **Interpretability:** partial.

## Decision

1. **Resolve-condition verdict:** met: top-1 is 4, 31/32 matched controls have lower target-vs-source log odds, and prompt-only output is coherent.
2. **Prediction check:** all three job-label predictions are supported; statistical significance was not predicted and is not established.
3. **Earliest unsupported link:** transfer to a new pair; a predeclared new pair supports it.
4. **Validity:** valid selected causal example, about 0.82–0.93; not valid as a population estimate.
5. **Highest-information clues:** +3.375-nat shift, 31/32 control rank, one random top-1 flip, coherent C=2 generation.
6. **Missing metrics:** larger random tail, new-pair replication, direct-answer control.
7. **Bugs requiring code changes:** none observed.
8. **Misconceptions requiring reinterpretation:** the single displayed random generation is not the control result; the full random distribution is.
9. **What would change the verdict:** failure on predeclared pairs would restrict the claim to this selected sample; many equally strong random controls would weaken specificity.
10. **Recommended next experiment:** preserve C=2 and all extraction settings, enlarge the control sample, then convert the validated path into the README and notebook.

Written by PI/gpt-5.4.
