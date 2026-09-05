# Job 99 audit

Job 99 checked whether job 98 failed because of Ant spelling, LM-head row scaling/centering, layer, or prompt-position scope. It tested 288 fixed C=1 combinations. Sources: [`job_99_script.py`](job_99_script.py), [`job_99_full.log`](job_99_full.log), [`../research/spider_ant_grid.json`](../research/spider_ant_grid.json).

| stage | expected | observed | consequence |
|---|---|---|---|
| grid completion | 4 spellings × 4 row forms × 9 layer scopes × 2 position scopes | 288 rows | implementation questions were covered |
| answer flip | a non-isolated region changes 8→6 | 0/288 top-1 outputs were 6 | direct LM-head coordinate swap fails |
| best movement | p(6) materially rises | 0.0267→0.0382; Δlog p(6)=+0.360 nats | small directional effect only |

> {'target': ' Ant', 'centered': False, 'normalized': False, 'layers': 'L23', 'positions': 'final', 'p6': 0.03820384293794632, 'p8': 0.8695154190063477, 'log_odds_6_vs_8': -3.125} top= 8
>
> n 288 top6 0

### H1 [method | Highly Likely | 85%]
Direct LM-head token coordinates do not reproduce the J-lens Spider→Ant causal swap. Evidence: zero flips across the declared grid. Contrary evidence: every test used a static word coordinate rather than a token-specific suppressed subspace. Next test: a two-pass per-position subspace swap.

### H2 [scope | Unlikely | 30%]
A single layer or all-position scope was the missing condition. Evidence against: every L23–L30 layer and the full range, at final and all positions, failed. Next test: vary the subspace by prompt position, not merely the hook scope.

### H3 [target encoding | Highly Unlikely | 15%]
A capitalization or row-norm convention explains failure. Evidence against: four atomic spellings and all centered/unit combinations failed. Next action: do not search more token spellings.

Decision: valid negative result for static LM-head coordinates, probability about 0.95. The next distinct test is a first pass that computes one suppressed subspace per prompt position followed by an all-position second-pass swap.

Written by PI/gpt-5.4.
