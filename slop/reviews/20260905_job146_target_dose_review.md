# Job 146 target-coordinate dose review

Job 146 completed the preregistered C∈{1,2,4,8,12} target-only grid.

Ant crosses from 8 to 6 at C=8:

> `ant | C=4 | top 8 | p(6)=.2772 | p(8)=.5868`
>
> `ant | C=8 | top 6 | p(6)=.4284 | p(8)=.2944`
>
> `ant | C=12 | top 1 | p(6)=.1424 | p(8)=.1516`

Its generated continuation begins:

> `6. Hypothesis: The animal that spins webs has 6 legs.`

The edit applies during prompt prefill only, so text after the first token is ordinary autoregressive continuation rather than independent persistent-intervention evidence.

Dog does not cross to 4:

> `dog | C=4 | top 8 | p(4)=.1785 | p(8)=.7058`
>
> `dog | C=8 | top 8 | p(4)=.2467 | p(8)=.4609`
>
> `dog | C=12 | top 8 | p(4)=.1464 | p(8)=.3099`

Dog p(4) peaks at C=8 and then falls; off-target p(6) passes p(4) at C=12. Extending the dose would be post-hoc after the curve has entered degradation.

The existing public artifact reports a whole sample-component Spider→Dog replacement at C=2 that changes top-1 from 8 to 4. This uses an independently detected prompt-specific Dog component, not the target-token coordinate tested here.

Recommended next experiment: use the same whole sample-component replacement for both targets. Extract independent Ant-prompt and Dog-prompt components with the same rule, then replace the Spider component with each under one fixed layer, rank, norm matching, final-token position, and dose grid. This is one consistent intervention mode and already has a Dog positive result.

Verdict: valid negative for distinct target-coordinate Ant and Dog control. Job 146 gives an Ant-only crossing; Dog degrades before crossing.

— reviewer subagent, fresh context
