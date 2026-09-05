# Job 148 one-layer sample-component review

The run completed from clean source. The tested operation was a rank-16, norm-restored whole sample-component replacement at residual L26 and the final prompt position.

Neither required crossing occurred.

Ant:

> C=4: top 8, p(6)=.2704, p(8)=.5725
>
> C=8: top 8, p(6)=.2046, p(8)=.3374
>
> C=12: top 4, p(4)=.2815, p(6)=.1330, p(8)=.2192

Dog:

> C=2: top 8, p(4)=.1194, p(8)=.7788
>
> C=4: top 8, p(4)=.1189, p(8)=.3232
>
> C=8: top 5, p(4)=.0600, p(8)=.0873

Both target prompts are behaviorally valid: Ant gives p(6)=.7243 and Dog gives p(4)=.9436. The Dog readout contains dog terms; the Ant readout contains no clear Ant terms and includes `_unix` and unrelated vocabulary.

The earlier Dog success used rank 8 and repeated replacement across L23–L30. Job 148 changed both rank and intervention topology, so it does not determine which caused the lost Dog crossing. The earlier Ant multi-layer rank-8 run moved p(6) but did not cross by C=2.

Recommended next experiment: a rank-8 single-site layer sweep. Run L23–L30 as separate forwards rather than stacking interventions in one forward. Use the same whole sample-component operation and dose grid for Ant and Dog. Require a shared layer where both expected digits become uniquely top before entropy rises or digit mass falls sharply. Add controls and generation only at a candidate crossing.

Verdict: valid negative. One-layer rank-16 sample replacement produces neither public demo.

— reviewer subagent, fresh context
