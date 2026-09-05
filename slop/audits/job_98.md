# Job 98 audit

Job 98 tested the requested Spider→Ant coordinate swap with ordinary LM-head directions, both directly and after projection into the prompt's detected rank-8 suppressed subspace. It used Qwen3.5-4B, L23–L30, all prompt positions, and C∈{0.5,1,2}. Sources: [`job_98_script.py`](job_98_script.py), [`job_98_full.log`](job_98_full.log), [`../research/spider_ant_coordinate_trial.json`](../research/spider_ant_coordinate_trial.json).

| stage | expected | observed | consequence |
|---|---|---|---|
| readout | rank-8 contains Spider | `Spider` appears at rank 6 | detector works on this sample |
| direct C=1 swap | move 8 toward 6 | p(6) 0.027→0.030; top remains 8 | requested causal result fails |
| within-S C=1 swap | move 8 toward 6 while staying in detected S | p(6) 0.027→0.034; top remains 8 | requested causal result fails |
| C=2 | stronger movement toward 6 | top becomes `Spider`; p(6), p(8) near zero | excessive intervention writes token-like content |
| projection | Ant has material component in S | norm fraction 0.235 | failure is not explained by exactly zero overlap |

> direct_C=1 top= 8 p6= 0.0298 p8= 0.8697 log6/8= -3.375
>
> projected_inside_S_C=1 top= 8 p6= 0.0336 p8= 0.8670 log6/8= -3.250
>
> direct_C=2 top= Spider p6= 0.0000 p8= 0.0000 log6/8= -2.680

### H1 [method | Highly Likely | 80%]
- **Mechanism:** LM-head word directions are readable correlates here but do not implement the same causal coordinate system as J-lens vectors.
- **Evidence:** both direct and within-S swaps leave 8 top at C=1; C=2 produces `Spider`, not 6.
- **Contrary evidence:** only one layer range, position scope, capitalization, and direction scaling were tested.
- **Test/action:** run a bounded layer/position/scaling grid before concluding.

### H2 [intervention | Likely | 65%]
- **Mechanism:** swapping at every prompt position and eight layers overapplies a local final-position readout direction.
- **Evidence:** extraction is at the final prompt position; C=2 becomes token-like output.
- **Contrary evidence:** the J-lens precedent uses clamped swaps over broad scopes.
- **Test/action:** test each layer separately at final position and all positions, without retuning the detector.

### H3 [target | Likely | 65%]
- **Mechanism:** `Ant` is not represented by the chosen capitalization/scaling or is absent from this LM-head-derived subspace.
- **Evidence:** the ant prompt ranked ant 14,798 and only 23.5% of the Ant row norm lies in S.
- **Contrary evidence:** 23.5% is nonzero; four atomic ant spellings exist.
- **Test/action:** compare the four atomic spellings and unit versus raw effective rows in one declared grid.

Decision: the requested Spider→Ant result failed under the tested default. The causal claim is invalid for this operator with probability 0.9–0.98. The next bounded test is a layer, position, spelling, and scaling grid; if no robust region moves 8→6, keep Spider→Ant as a negative result and do not put it in the headline demo.

Written by PI/gpt-5.4.
