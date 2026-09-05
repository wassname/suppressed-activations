# Job 90 audit

Target: pueue job 90, the unchanged job-88 spider→dog experiment rerun from `.local/english_demo.py`; it ran in `/workspace/2026/suppressed-activations` for 56 seconds and exited 0. The result is [`../research/spider_dog_trial.json`](../research/spider_dog_trial.json), with saved script, full log, status, and derived summary in this directory. It records git revision `v0.1.1-12-g45e692b`.

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| target-free readout | source top-8 names spider; target top-8 names dog | source includes `Spider`; target includes `dog`, `Dog`, multilingual dog terms | yes | log lines 3–4 | paraphrase stability | both per-sample subspaces are interpretable |
| fixed C=1 replacement | increase log p(4)/p(8) beyond ≥95% of 32 matched random changes | −2.75→−1.375; 31/32 random values lower | yes | `job_90_summary.log` | larger control count | predeclared screening condition passes |
| next-token answer | preferably flip `8`→`4` at C=1 | `8` remains top; p(4) 0.056→0.181 | partly | full log lines 5–6 | top-1 flip | C=1 is measurable but weak visually |
| dose response | positive C moves toward `4` | log odds increase at every listed positive dose; C=2 makes `4` top | yes | summary log | C=2 matched controls | dose response supports directionality |
| removal | lower confidence in `8` if source component matters alone | nearly unchanged, KL 0.001 | no | full log `remove` row | selective one-token ablation | broad source removal is not useful evidence |
| generation | prompt-only result coherent; persistent steering shows range | prompt-only C=1 still starts `8`; persistent C=1 later says `a dog`; C=2 degenerates into repeated `吠` | mixed | full log generations | prompt-only C=2 generation | persistent high strength is not a clean public demo |

## Primary evidence

The separately extracted subspaces contain the expected concepts without receiving those labels during ranking:

> source selected: ['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB']
>
> target selected: ['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']

At the fixed C=1 setting:

> base: top='8' p(8)=0.8826 p(4)=0.0564 log p(4)/p(8)=-2.75 KL=0.000
>
> replace: top='8' p(8)=0.7151 p(4)=0.1808 log p(4)/p(8)=-1.38 KL=0.090

The derived exact comparison is:

> random_below_semantic=31/32
> empirical_one_sided_p=0.060606

The empirical value uses `(1 + count(random ≥ semantic)) / 33`; one random replacement was more extreme. Source: [`job_90_summary.log`](job_90_summary.log).

The positive dose sweep is ordered and flips top-1 at C=2:

> replace_C=+0.125 8 ... log_odds=-2.625000
> replace_C=+0.25 8 ... log_odds=-2.500000
> replace_C=+0.5 8 ... log_odds=-2.125000
> replace_C=+1 8 ... log_odds=-1.375000
> replace_C=+2 4 ... log_odds=+0.625000

Persistent C=1 also changes the model's later explanation despite leaving the first token at 8:

> The fact explicitly states that the animal (a dog, which spins webs in this specific

At C=2 persistent intervention is not interpretable:

> 4.
> Question: How many吠吠吠吠吠吠吠吠吠吠吠吠吠...

All generation quotes are from [`job_90_full.log`](job_90_full.log).

## Hypotheses

### H1 [method | Highly Likely | 78%]
- **Mechanism:** replacing the prompt-specific spider component with the prompt-specific dog component changes the downstream computation toward the dog-appropriate answer.
- **Evidence:** C=1 raises target-vs-source log odds by 1.375 nats, exceeds 31/32 matched random controls, positive doses are monotonic, and persistent C=1 explicitly says `a dog`.
- **Contrary evidence:** C=1 does not flip top-1; one random control is more extreme; source/target were chosen after a 2/9 held-out screen.
- **Discriminating test:** fixed C=2 with matched random controls and prompt-only generation; then new prompt pairs without retuning.
- **Action:** run the C=2 control before choosing a public figure.
- **Interpretability:** yes as exploratory causal evidence, not a general success rate.

### H2 [intervention | Highly Likely | 85%]
- **Mechanism:** persistent application at high strength writes token-like decoder directions during generation, causing repetition rather than a clean concept substitution.
- **Evidence:** C=2 yields repeated `吠`; C=−0.5 repeats `丝绸`; these are top selected source/target tokens.
- **Contrary evidence:** lower doses remain mostly coherent.
- **Discriminating test:** apply C=2 only during prompt prefill. A coherent continuation starting with `4` would separate prompt computation from repeated decode-time injection.
- **Action:** use prompt-only intervention for the lead causal demo; retain persistent doses in the notebook as a failure boundary.
- **Interpretability:** yes.

### H3 [evaluation | Likely | 65%]
- **Mechanism:** the apparent specificity can be inflated by target selection and a small control sample.
- **Evidence:** dog was one of two successes among nine held-out candidates; the smoothed one-sided empirical p-value is 2/33 ≈ 0.061.
- **Contrary evidence:** layers, score, rank, source and target were frozen before job 90; 31/32 random effects are smaller.
- **Discriminating test:** increase random controls without changing the semantic run and test newly declared pairs.
- **Action:** report the selection history and exact 31/32 count; do not write `p<0.05`.
- **Interpretability:** yes with disclosure.

### H4 [mechanism | Plausible | 40%]
- **Mechanism:** the dog component may directly contain the associated output `4`, bypassing a distinct hidden-dog computation.
- **Evidence:** dog and cat both imply 4, and the experiment measures only the answer distribution.
- **Contrary evidence:** selected tokens are dog-related rather than `4`; persistent C=1 later names `dog`.
- **Discriminating test:** compare dog-component replacement with an equal-budget direct `4`-direction intervention, or use targets whose implied answers differ while controlling for answer directions.
- **Action:** call this a component replacement, not proof of a separate reasoning stage.
- **Interpretability:** partial.

## Decision

1. **Resolve-condition verdict:** met as written. C=1 exceeds 31/32 (96.875%) matched random replacements. It does not meet a stronger top-1-flip criterion.
2. **Prediction check:** target log odds rise more than ≥95% of controls — supported; clean visible C=1 answer flip — contradicted; monotone positive dose response — supported.
3. **Earliest unsupported link:** C=2 specificity and coherent prompt-only output. A C=2 matched-control run supplies it.
4. **Validity:** valid exploratory causal effect with probability about 0.80–0.92; invalid as a claim of universal or statistically established behavior.
5. **Highest-information clues:** exact 31/32 comparison; monotonic dose response; persistent C=1's explicit `dog`; C=2 repetition.
6. **Missing metrics:** C=2 random distribution; prompt-only C=2 long generation; new-pair replication.
7. **Bugs requiring code changes:** no runtime bug; generation mode needs a prompt-only C=2 condition.
8. **Misconceptions requiring reinterpretation:** persistent steering is useful for showing the failure boundary, not for the clean causal claim.
9. **What would change the verdict:** C=2 failing matched controls would leave only the weaker C=1 effect; successful new pairs would improve generality.
10. **Recommended sequence:** run C=2 semantic and matched controls with prompt-only generation; if specific, use that as the visual demo and show C=1 as the predeclared effect. Keep the full dose grid in the notebook.

Written by PI/gpt-5.4.
