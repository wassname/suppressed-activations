# Independent causal-outcome review

**Result:** The indirect-description donor changes subsequent text and slightly increases relative preference for `8`, but changes neither tested initial animal-property answer. Arithmetic remains `4`. The literal-name control changes the initial skeleton answer to `outside`, a useful local partial positive—not evidence that the new donor succeeded or that either donor coherently replaced the animal concept.

Read-only review: all enumerated files read completely, including all ten 32-token continuations, generated IDs, top-10 tables, prefill/final-decode readouts, and coverage arrays. Required AGENTS.md files and ml-debug skill were read. No commands, inference runs, edits, network, discovery, or delegation performed.

## 1. Actual answers, scored separately by property

Paths below are relative to `/workspace/2026/suppressed-activations`.

| Property | Condition | Expected initial answer | Actual affirmed initial answer | Outcome |
|---|---|---|---|---|
| Legs | Base | `4` | `4` | Baseline correct |
| Legs | Indirect donor | `8` | `4` | Target not reached |
| Legs | Literal-name control | `8` | `4` | Target not reached |
| Legs | Matched random | Control | `4` | Baseline answer retained |
| Skeleton | Base | `inside` | `inside` | Baseline correct |
| Skeleton | Indirect donor | `outside` | `inside` | Target not reached |
| Skeleton | Literal-name control | `outside` | `outside` | Local target answer reached |
| Skeleton | Matched random | Control | `inside` | Baseline answer retained |
| Arithmetic | Base | `4` | `4` | Baseline correct |
| Arithmetic | Indirect donor | `4` | `4` | Arithmetic retained |

These are property-specific observations on previously observed prompts, not a generalisation estimate or a universal two-property acceptance gate. There is no literal-name or random arithmetic trajectory.

### Legs: later `8` is not an affirmed answer

`out/2026-10-01_093718_jlens-one-pass/run.md`, indirect and literal conditions, both say:

> `4.`  
> `Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.`  
> `Does the hypothesis`

Base and random instead continue with a hypothesis ending `2.` and `Is the hypothesis`.

The initial answer remains `4` in all four trajectories. In `interventions.json`, every initial generated ID is `19`; donor trajectories introduce ID `23` only in the later hypothesis. Both donor continuations are identical across all 32 generated IDs; Base and random are likewise identical.

**Useful partial positive for both donors:** the intervention affects the continuation, including the hypothesis number, whereas this one random vector does not. This is not zero behavioural effect. It is not affirmed `8`, and it is not necessarily a contradiction: an NLI task can deliberately propose a false hypothesis.

### Skeleton: genuine local change only for the literal control

`out/2026-10-01_093729_jlens-one-pass/run.md` records:

- Base, indirect, random: initial `inside.`, later hypothesis `outside`.
- Literal: initial `outside.`, later hypothesis `inside`.

The corresponding first generated IDs are `4613` versus literal `4732`. The literal change is therefore an actual generated-answer change, not a table-order artefact. Its continuation preserves a readable fact/hypothesis contrast within the available window. The opposite hypothesis does **not** establish that the model retracts its initial answer.

This is useful partial evidence for local steering by the literal control. It cannot be reassigned to the indirect donor. Neither trajectory reaches a completed NLI judgement, so the result does not establish coherent concept transfer through subsequent reasoning.

### Arithmetic: answer preservation is narrower than text preservation

`out/2026-10-01_093740_jlens-one-pass/run.md` gives the exact input:

> `'Fact: An animal that barks is nearby. The sum of 2 and 2 is '`

Both trajectories affirm `4` and reproduce the barking-animal hypothesis. Base ends:

> `<think>`  
> `Thinking Process:`  
>   
> `1.`

Indirect instead ends:

> `<think>`  
>   
> `</think>`  
>   
> `Yes, the fact`

Thus arithmetic is preserved, but the whole continuation is not. The visible `Yes` is compatible with the stated nearby-animal fact; the explanation is capped, not fully assessed.

## 2. Numerical evidence and its limits

Source: the three property `run.md` files and `interventions.json` files.

| Property | Condition | p(source answer) | p(target answer) | Logged shift |
|---|---|---:|---:|---:|
| Legs | Base | 0.943579 | 0.007204 | 0 |
| Legs | Indirect | 0.944299 | 0.008170 | −0.125 |
| Legs | Literal | 0.934653 | 0.010383 | −0.375 |
| Legs | Random | 0.941424 | 0.007188 | 0 |
| Skeleton | Base | 0.255030 | 0.225063 | 0 |
| Skeleton | Indirect | 0.237425 | 0.209527 | 0 |
| Skeleton | Literal | 0.223296 | 0.253027 | −0.250 |
| Skeleton | Random | 0.243081 | 0.214518 | 0 |

For this reverse-direction experiment, negative logged shifts favour the target.

- Legs: indirect improves target/source log odds by 0.125 nats, but even `p(4)` increases slightly. Literal improves them by 0.375 nats; neither overcomes the strong baseline preference for `4`.
- Skeleton: Base has a 0.125-nat inside advantage; literal reverses it to a 0.125-nat outside advantage. Indirect and random retain the original answer-pair odds, while lowering both probabilities.
- Arithmetic: `p(4)` changes from 0.985204 to 0.984637; the logged `4` versus `8` shift remains zero.

The complete top-10 tables contain ties—for example legs indirect `8` and `0`, and arithmetic indirect `5` and `2`. Their display order does not determine generated order. None of the initial generated-answer conclusions above requires resolving a winning-token tie.

### Repetition is not coherence

Reported `r2` is 0.032258 for nine trajectories and 0.064516 for indirect arithmetic. Low repeated-bigram rates do not distinguish:

- an affirmed answer from an unendorsed hypothesis;
- correct reasoning from an unfinished NLI prompt;
- stable behaviour from a changed thinking/answer format.

Arithmetic's doubled rate is not evidence of repetitive collapse; the visible continuation is short and contains repeated formatting. `verification.json` describes its scope as “non-special-token repetition,” but tokenizer special-token classification and the metric implementation are not in scope. I cannot independently certify whether the visible thinking markers were excluded correctly. A tokenizer-aware recomputation could resolve that narrow uncertainty.

Bare pair mass also is not semantic certification. Skeleton mass is below one half even in Base (0.480093); indirect lowers it to 0.446952, yet the generated text remains readable within the cap.

## 3. Readouts do not establish animal replacement

The prefill/final distinction matters:

- **Legs:** all four prefill lists remain dominated by `paw`, `claws`, `mammals`, dogs/canine and related vocabulary. Neither donor produces a visible spider-dominated top-32 readout. Final donor lists lead with `facts`/`factual`, while Base/random lead with `hypothesis`/`statement`.
- **Skeleton:** prefill lists remain spatial/anatomical (`underside`, `upside`, `side`, `inside`, `bones`, etc.). Final lists are mostly question punctuation and `true`/logical vocabulary for all four conditions.
- **Arithmetic:** both prefill lists begin with `4`; final Base is analysis-related, whereas indirect is fact-related.

These final readouts occur after different generated histories where trajectories diverge. They cannot isolate concept transfer from ordinary context dependence. Absence of spider words in a top-32 list also does not prove absence of a hidden spider representation.

Each property log explicitly says:

> “No standalone readout benchmark in this intervention run.”

The lens fitting model revision is also recorded as unknown. This experiment therefore does not complete the main readout claim.

## 4. Preparation and one-pass boundary

### What is new

`data/dog_spider_donors_indirect_v3.json` changes **preparation data**, not the algebra: two descriptions per animal crossed with two wrappers; four final-`It` states averaged per animal; natural spider-minus-dog addition.

The preparation prompts contain no explicit animal names or tested answer/property labels. All eight saved token sequences end in ID `1049`. Descriptions remain imperfectly identifying—for example “trained to sniff luggage at customs” is not logically unique to dogs—and prefix lengths vary.

`verification.json` reports natural norms:

> `"natural_delta_norm": 1.9573026895523071`  
> `"literal_delta_norm": 1.4303362369537354`

The new vector is about 37% larger. Random matches the new vector, not the literal vector. Consequently the observed literal/indirect difference does not isolate semantic orientation from magnitude, prefix length or descriptive content. The smaller literal vector doing more here does not establish a monotonic norm explanation either.

### Boundary supported, not independently certified

`preregistration.md` specifies:

> “No backward pass, preliminary current-input pass, later-layer feedback or current-input donor extraction.”

The documented operation edits block15, observes block23 without feedback, uses the last prompt position, then quarter-strength cached decoding. All ten coverage arrays show one prefill followed by 31 one-position decode entries. The selected prompt tokens are the trailing space for legs/arithmetic and ` the` for skeleton—not the offline donor's ` It`.

`pipeline.json` reports 328 forward calls: eight preparation calls plus ten times 32 evaluation calls. This is consistent with one ordinary autoregressive trajectory per condition, **not** one forward call for a complete answer.

Nonzero requested/applied norms show that saved edit records are not simply zero updates. For example legs indirect prefill records applied norm `1.9568161964416504`; literal records `1.430823564529419`.

What could invalidate the boundary:

1. Extra preliminary/current-input forwards omitted from the recorded counter.
2. A block23 observer or diagnostic influencing the edit or subsequent token selection.
3. Donor construction consuming evaluation activations or answer-based selection.
4. Coverage records not corresponding to the actual tensors propagated downstream.

The scoped files supply coverage summaries and a passed numerical verification, not executable source, a complete ordered hook/forward event trace, or independent neural replay. These failure modes are **not observed**, but are not independently ruled out here. Source hashes pin identities without proving implementation semantics.

`verification.json` itself correctly qualifies its result:

> “not independent neural/hardware/semantic certification”

## 5. ml-debug audit and discriminating checks

| Required item | Evidence or limitation |
|---|---|
| Log/config completeness | All scoped files read to EOF; intervention JSON lengths 4250, 4234 and 2118 lines. Qwen3.5-4B; block15/residual16; observer23; `prompt_slice: '-1:'`; `decode_scale: 0.25`; seed0; 32-token cap. |
| SHOULD versus observation | Preparation “means differ”: reported norm 1.957303. Property SHOULDs require target movement/coherence beyond random: indirect legs has small odds/text movement, skeleton does not; literal skeleton changes locally. Arithmetic SHOULD retains4: observed; full coherence unresolved. |
| Null/chance scale | Base and one random vector provide the numerical scales above. No random-seed distribution, shuffled donor, or meaningful uniform-vocabulary semantic chance estimate supplied. |
| Initial/demo evidence | No training updates. Base supplies pre-intervention behaviour. All ten complete capped samples inspected. |
| Dummy/baseline/heldout | Initial-answer persistence matches indirect on every evaluated prompt. Literal differs on skeleton only. No heldout cases; logs explicitly say “two already-observed properties.” |
| Learning-rate schedule, losses, gradients | Not applicable to fixed-vector inference; no training schedule or optimisation claimed. |
| Surprise | Literal skeleton changes despite smaller norm; explained: magnitude alone does not determine directional effect. Indirect arithmetic format changes despite unchanged answer odds; explained: first-token metrics omit later behaviour. Neither establishes a mechanism. |
| Missing trust evidence | Source/event-trace audit, independent replay, tokenizer-aware repetition recomputation, completed semantic continuations, donor identity validation and replication. |
| Fresh review | This is the requested fresh same-family review without supplied outcome diagnosis. No additional reviewer launched. |
| Runtime | Pipeline reports 39.20 seconds and peak allocated 8.153 GiB; property stages 10.84/10.25/6.79 seconds. Preparation-specific timing unavailable. |

**Competing explanations, subjective weights rather than measured posteriors:** 45% insufficient/context-dependent semantic transfer; 30% lexical/template or other nonspecific perturbation; 10% implementation/cache/hook error; 5% evaluation/measurement error; 10% unknown. The preserved initial answers and changing later templates support the first two; nonzero edits and numerical verification weigh against a simple missing-update bug, but do not exclude implementation faults. Explicit generated IDs weigh against answer-scoring error; metric implementation remains uninspected.

**Cheapest checks, recommendations only:**

- Audit the pinned source and ordered events for observer feedback, hidden forwards and actual edit propagation. Passing numerical reconstruction alone does not distinguish correct execution from correctly reconstructed wrong execution.
- Review longer continuations under an explicitly authorised follow-up, without changing the frozen donor/configuration. Coherent transfer predicts stable target-consistent affirmed claims; a template effect predicts target mentions confined to proposed hypotheses or unstable continuation behaviour.
- Separately validate donor referents and eventually compare norm-controlled preparation variants. That could distinguish semantic preparation from magnitude/length confounds, but would be a new experiment, not a rescue of these ten results.

**Research decision:** retain the indirect donor's small legs odds/text effect and arithmetic preservation as bounded positive observations. Retain literal skeleton as a control-specific local partial positive. Do not claim indirect superiority, isolated hidden-component replacement, full semantic coherence, or failure of the general idea.

— PI/OpenAI