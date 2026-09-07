# Named-coordinate swap

Written by Codex, 2026-09-07.

User request: "do the proepr swap and measure the results".

The local global-workspace paper, methods "Writing", specifies
`c = pinv(V) @ h; h_new = h + V @ (flip(c) - c)`.
Here V has two normalized, centered, RMS-gain-weighted unembedding columns,
for ` spider` and ` ant` or ` dog`. The projected variant first projects both
columns into the shared persistent source/donor span (four vectors each).
This reproduces the swap operation, not the paper's J-lens estimator.

Jobs 512 and 513 use Qwen3.5-4B, official assistant-prefill formatting, L24,
last three prompt positions and all cached decode positions, 32 output tokens.
C = 0, .25, .5, 1, 2, 4 scales the displacement, with no norm restoration.
C=1 exchanges coordinates; C=.5 equalizes them; C>1 extrapolates.
Only one layer is edited, so repeated swaps across layers cannot cancel directly.

Question: does named-coordinate exchange give selective, coherent animal transfer?
The raw-direction comparison removes the suppression-space constraint; the
projected comparison retains it. Both use identical generation and evaluation.
Expectations: C0 identity and coordinate exchange follow algebra and are tested.
Semantic transfer is an unvalidated hypothesis. Wrong directions, source removal,
and target-to-source reversal during decode can all prevent useful transfer.
The coordinate trace distinguishes reversal from an inactive hook.

Independent review by Codex (`swap_review`):
> With unit-length source/target vectors, C=1 is a reflection along their difference.
> It preserves residual norm naturally. C=.5 removes the source-target contrast;
> C>1 extrapolates.

> Dynamic swapping during generation can turn a target-dominant state back toward
> source. This is mathematically correct swapping, not persistent target clamping.

Production-hook synthetic tests pass: nonorthogonal coordinates exchanged,
orthogonal complement and untouched prefix unchanged, swap twice returns input,
and cached singleton edited. Real runs assert exact C0 logits and generation,
three prefill positions and one hook call per subsequent generated token.
Logs retain all continuations and per-step coordinates. A correct digit alone
does not establish a coherent donor concept. No new random controls in this grid.

## Completed jobs 512 and 513

Both jobs succeeded, executing commit `325d005` with only user README/.gitignore
changes dirty. Full stdout read: 41 of 41 clean lines for each job. All 24
continuations inspected, without selecting by metric. Model revision:
`851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Runtime dependency versions were not
copied into the artifacts; the cached uv environment was reused.

| stage | expected | observed | expected? | evidence | missing | consequence |
|---|---|---|---|---|---|---|
| extraction | identical assistant-prefill template | exact rendered inputs in each run.md | yes | source and donor repr | no held-out prompts | development only |
| C0 | identity | four rows match base exactly | yes | generation and p_target/p_source | full logits not persisted | runner asserts full logits |
| swap | coordinate exchange | maximum float32 coordinate error 0.00000620 | yes | coordinate_trace, independently checked | post-bfloat16 coordinates | numerical limit remains |
| coverage | last3 plus full decode | positions [33,34,35], decode_steps31 | yes | all24 intervention_record objects | none for requested coverage | not stopped early |
| ant | answer6 and ant | no6; raw C2/C4 name ant | no | ant result.json | other consequences | partial identity effect |
| dog | answer4 and dog | three4; all mix dog/spider | partial | dog result.json | longer generations | not coherent replacement |
| persistence | suppress unrelated content | projected ant readout becomes punctuation | no | rank4 C4 readout | causal direction estimator | projection may discard useful content |
| artifacts | complete demos per condition | 24 run.md files, two result.json and tables | yes | links below | random controls | no selectivity claim |

Sources: [ant](../../out/2026-09-07_coordinate-swap-ant/result.json),
[dog](../../out/2026-09-07_coordinate-swap-dog/result.json).
These are our model outputs, not independent demonstrations from the paper.

Ant base `p_target=0.015244761481881142`, clean donor
`p_target=0.8998122215270996`. Raw C1 log-odds shift is zero; C4 is +0.75 nats.
Its entire C4 continuation is:

```text
8.

**Explanation:**
The animal that spins webs is an **ant**. Ants belong to the class *Insecta* (insects).
```

The corresponding readout is `[' ant', ' Ant', 'Ant', '.ant', ' ANT', '_ant', '抗', ' antim']`.
Projected C4 instead produces first token2 with valid answer mass0.112.
Thus a positive log-odds shift can coexist with degraded answer probability.

Dog base p4=0.0285. Raw C1 p4=0.1147, C2 p4=0.4633, C4 p4=0.3435.
Raw C2 has +3.625 nats log-odds shift and valid answer mass0.872:

```text
4.

**Explanation:**
The animal that spins webs is a **dog** (specifically, a spider). Spiders are classified as arachn
```

Projected C4 has the largest dog score, +5.625 nats and p4=0.6076,
but still says dog "or more accurately" spider. No generated explanation
establishes a consistent donor concept. This describes these 24 outputs only.

### Competing explanations

1. Method, highly likely (80%): these directions affect animal words more than
   the leg-count computation. Evidence: ant C4 says "Ants belong to the class
   *Insecta* (insects)." but starts8. Contrary evidence: dog C2 starts4.
   Test: hold named directions fixed and move the single edit earlier in depth;
   earlier answer transfer would support a timing explanation instead. Cost:
   another small forward/generation grid. Interpretation remains partial.
2. Method, likely (60%): continuous dynamic swaps undo some target content.
   Evidence: raw dog C2 has target>source coordinates before 10/31 decode edits;
   generation says "a **dog** (specifically, a spider)." Contrary evidence:
   ant C4 retains ant identity despite 12/31 such edits. Test: compare one-sided
   source-dominant-only coordinate exchange at otherwise identical settings.
   Fewer self-corrections would support this mechanism. This changes the operation
   and must be labelled separately. Interpretation remains partial.
3. Bug, remote (5%): realized model-dtype patch differs materially from the
   intended float32 swap. Evidence: production code ends `patched.to(hidden.dtype)`;
   current coordinate traces precede that cast. Contrary evidence: all synthetic
   algebra and exact C0 checks pass, and semantic outputs move. Test: record
   post-cast coordinates and residual norm on the same selected conditions.
   Large coordinate error would require fixing numerical precision. Current
   interpretation is partial, not invalidated by an observed bug.
4. Measurement, almost certain (95%): digit and overlap scores alone overstate
   semantic success. Evidence: dog C2 says "a **dog** (specifically, a spider)."
   Contrary evidence: the digit4 and dog readout are real partial effects.
   Action: preserve full generations and add a second concept consequence before
   claiming replacement. Unknown mechanisms remain possible (20% rough prior).

### ML-debug checks and decision

- SHOULD C0 identity: passed, runner asserts complete first-logit tensors and IDs.
- Initial demo: spider8, clean ant6; donor baseline exceeds all ant interventions.
- Dummy/null: C0 is the measured null, not a uniform-vocabulary assumption.
- Held-out comparison: absent. These are two development prompts, one greedy run.
- Schedule, losses and gradients: not applicable, no training.
- Worst condition: projected ant C4, answer2 and p6+p8=0.112.
- Surprise: ant identity changes while leg count remains8; explained at the level
  of distinct observable effects, causal mechanism still unresolved.
- Missing evidence: post-cast coordinates, other concept consequences, matched
  random controls and held-out phrasings. No stochastic seed claim is made.
- Fresh review (`swap_review`, Codex): "No swap-equation or coverage bug found."
  It independently read all24 generations and checked all traces; this is a
  second analysis of the same evidence, not an independent replication.
- Runtime: ant33.92s and dog30.67s internally, about1.8-2s per condition after load;
  peak allocated GPU memory13.805GB each. Queue waits are excluded.

Resolve "answer6 coherence" and "answer4 coherence": not met. Measurement is
credible for this implementation; broader concept-replacement efficacy is
inconclusive. Estimated probability a hidden bug materially invalidates these
measurements: 5-15%, not a measured frequency.

Highest-information clues: ant names ant without6; dog gives4 but self-corrects
to spider; hook coverage and algebra pass. No code bug is established. The
highest-information next comparison is the same named pair at earlier single
layers, retaining the continuous coverage and no norm restoration. Keep a
source-dominant-only swap comparison separate so timing and operation effects
remain distinguishable. A consistent donor readout, digit and second consequence
on held-out prompts would change the semantic verdict.
