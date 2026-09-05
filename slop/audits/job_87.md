# Job 87 audit

Target: pueue job 87, `uv run python /tmp/scan_animal_targets.py`, in `/workspace/2026/suppressed-activations`; it ran 2026-09-05 15:13:18–15:13:30 +08 and exited 0. The result records git revision `v0.1.1-12-g45e692b`, Qwen3.5-4B, fixed layers L23/L25/L32, and a rise-and-fall score divided by effective LM-head row norm. Sources: [`job_87_script.py`](job_87_script.py), [`job_87_full.log`](job_87_full.log), [`job_87_status.json`](job_87_status.json), and [`../research/english_animal_target_scan.json`](../research/english_animal_target_scan.json).

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| vocabulary preflight | every tested concept has a one-token variant | all ten cases passed; firefly and kangaroo were excluded before the run | yes | script lines 36–39; result metadata | phrase-level concepts | prior crash removed without changing score |
| held-in rule check | spider clean `8`, rank ≤32 | clean `8`, rank 6 | yes | log line 3 | lexical-overlap control | fitted source reproduces |
| held-out screening | a correct target with rank ≤32 | dog rank 4 and cat rank 21; both clean `4` | yes | log lines 6–7 | replication prompts | screening condition passes on 2/9 held-out cases |
| negative cases | score should not be assumed universal | bee 3726, cricket 1485, five correct-answer cases near 74k; elephant/crab answered incorrectly | yes | log lines 4–12 | uncertainty across templates | method is sample-specific and sparse |
| persistence | rows plus provenance | JSON contains ten rows and metadata | yes | result JSON | package hashes | run is auditable enough for the next experiment |

## Primary evidence

The held-in source reproduces:

> hidden=spider     expected= 8 top='8'          correct=True  rank=      6 top12=['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB', ' стане', 'amet', '.att', ' Bomb']

Two held-out prompts pass the predeclared rank-32 and clean-answer condition:

> hidden=dog        expected= 4 top='4'          correct=True  rank=      4 top12=['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine', ' соба', ' chiens', ' собак', '狗狗']
>
> hidden=cat        expected= 4 top='4'          correct=True  rank=     21 top12=[' Kitty', ' Adjustment', ' кошки', 'Warehouse', ' gatos', '섬', ' кошка', ' Warehouse', 'Hospital', ' кош', ' kucing', 'струи']

Most held-out prompts fail, including a clean-correct insect case:

> hidden=cricket    expected= 6 top='6'          correct=True  rank=   1485 top12=[' attac', 'крой', ' fungerer', ' Skinny', ' Geography', ' poja', ' Sushi', '躬', '在校园', 'нто', 'Kate', ' Waste']

All quotes are from [`job_87_full.log`](job_87_full.log).

## Hypotheses

### H1 [method | Highly Likely | 80%]

- **Mechanism:** under the fixed row-normalized rule, the ordinary LM head exposes an unspoken animal concept for some prompts, not only the fitted spider prompt.
- **Evidence:** dog and cat were held out from rule selection and rank 4 and 21 while their clean answers are correct.
- **Contrary evidence:** 7/9 held-out concepts fail the joint condition; only two pass.
- **Discriminating test:** repeat fixed dog/cat templates with paraphrases predeclared before inference. Stable hidden ranks support concept readout; large rank swings support template specificity.
- **Action:** use dog as the fixed target for a spider→dog intervention, with random subspace controls, before broadening claims.
- **Interpretability:** yes as target-free readout; causal relevance remains untested.

### H2 [measurement | Likely | 65%]

- **Mechanism:** spider success is partly amplified by lexical proximity between `webs` and spider-token rows, while dog/cat show that exact prompt-token identity is not necessary.
- **Evidence:** spider top 12 contains four `web` variants; dog top 12 contains multilingual dog terms even though the prompt only says `barks` and `man's best friend`.
- **Contrary evidence:** semantic relations can be legitimate latent readout; the exact hidden words are absent from all three prompts.
- **Discriminating test:** compare fixed-rule ranks across paraphrases that remove or alter the strongest lexical clue.
- **Action:** describe the observation as a sample-specific LM-head readout, not proof of a prompt-independent concept axis.
- **Interpretability:** yes with this caveat.

### H3 [evaluation | Likely | 60%]

- **Mechanism:** screening nine held-out cases and advancing two produces a selected demonstration, so the intervention can overstate generality if shown alone.
- **Evidence:** dog and cat pass while bee, sheep, owl, butterfly, and cricket answer correctly but rank outside 32.
- **Contrary evidence:** the screening rule and threshold were written before job 87; this is not layer tuning on dog/cat.
- **Discriminating test:** report the full 2/9 screening result beside the chosen example and evaluate new prompts without retuning.
- **Action:** retain the complete scan as provenance and call dog a held-out found example rather than a universal result.
- **Interpretability:** yes if selection is disclosed.

## Decision

1. **Resolve-condition verdict:** met. Dog (rank 4, correct clean top-1) and cat (rank 21, correct clean top-1) satisfy the predeclared condition.
2. **Prediction check:** the job-86 prediction that a held-out animal may rank ≤32 is supported by dog and cat; the stronger implicit expectation of a broad family rule is contradicted by 7/9 held-out failures.
3. **Earliest unsupported link:** causal relevance. A matched intervention that selectively changes `8` toward `4` more than random rank-matched replacements would support it.
4. **Validity:** valid for the screening claim with probability about 0.90–0.98. It is not yet valid evidence of steering or prompt-invariant representation.
5. **Highest-information clues:** dog rank 4 with multilingual dog variants; cat rank 21; full 2/9 held-out pass count.
6. **Missing metrics:** spider→dog answer log-odds under the actual intervention; matched-random distribution; paraphrase stability.
7. **Bugs requiring code changes:** none observed in job 87. Job 86's atomic-token bug is fixed by the preflight.
8. **Misconceptions requiring reinterpretation:** “generalizes” must mean the fixed detector found held-out samples, not that one global subspace transfers; each subspace is still extracted per sample.
9. **What would change the verdict:** a failed spider→dog intervention would preserve the readout finding but reject causal use; new held-out paraphrases can strengthen or weaken the template-generalization claim.
10. **Recommended next experiment:** freeze L23/L25/L32, row normalization, rank, source prompt, target prompt, hook layers, and strength; compare spider→dog component replacement against random rank-matched replacements. Do not tune on the answer change.

Written by PI/gpt-5.4.
