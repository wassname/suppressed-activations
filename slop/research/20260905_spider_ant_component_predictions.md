# Spider→Ant whole-component predictions

Question: does the same independently extracted whole-component replacement that changed spider→dog also change the spider answer from 8 toward 6 when the target prompt implies an ant?

Source prompt:

> Fact: The number of legs on the animal that spins webs is 

Target prompt:

> Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is 

The extraction rule remains L23/L25/L32, rank 8, row-normalized rise-and-fall score. The intervention remains residual L23–L30 with norm restoration. No layer, rank, or strength changes follow from this run.

| possibility | prior | expected observation |
|---|---:|---|
| Ant target has no useful suppressed component | 60% | target readout lacks Ant; C≤2 leaves 8 top or changes it nonspecifically |
| whole target trajectory works despite poor Ant token rank | 20% | positive C raises `log p(6) − log p(8)` monotonically and makes 6 top before generation collapses |
| target prompt directly selects answer-like `6` content | 10% | readout contains 6 or number terms; answer changes but does not isolate an Ant intermediate |
| excessive intervention causes unrelated output | 10% | KL rises without selective 6-vs-8 movement; text repeats target lexical tokens |

The result that supports the same mechanism as the dog demo is: the clean target answers 6, its selected readout contains Ant-related content but not the answer token, positive strengths move 6-vs-8 log odds, and prompt-only output changes to 6 before persistent generation becomes malformed.

A negative result rejects only this prompt and fixed extraction rule. It does not reject whole-component replacement in general.

## Result from jobs 117 and 119

The Ant target cleanly answers `6` with probability 0.7243. Its rank-8 suppressed readout is
`;font`, `_unix`, `Kate`, `สถาบัน`, `Soldier`, `división`, `在校园`, and `соци`, so it does
not expose a coherent Ant intermediate.

Positive replacement strength moves `log p(6) − log p(8)` from −3.500 at C=0 to −1.125 at
C=2. This raises p(6) from 0.0267 to 0.2304, about 8.6 times, but 8 remains top at every
tested strength. Negative strength moves the contrast in the opposite direction. At C=2,
persistent generation repeats `_unix`, one of the target readout tokens.

The run supports a substantial signed association between the target component and the answer
6. It does not satisfy the predeclared same-mechanism criterion because no Ant terms appear and
the answer does not flip. The target component may transport decoder-aligned lexical or
answer-related content rather than an Ant concept.

Written by PI/gpt-5.4.
