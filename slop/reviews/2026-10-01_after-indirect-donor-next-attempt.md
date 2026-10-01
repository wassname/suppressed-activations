# Next attempt: role-aligned donors and concise joint properties

## Inherited decisions

One bounded development attempt, using source08 and pinned Qwen3.5-4B. Offline preparation is reusable; evaluated inputs supply no preparation states, backward pass, or later-layer feedback. Keep block15, last prompt position, decode strength0.25, and32-token cap. This deliberately retains the previous experiment’s `-1:` exception to the repository’s `-3:` default.

The parent approved changing both the task frame and donor preparation. This is not a diagnosis of the old failure. Job2705 remains untouched.

## Diagnosis and evidence

The supplied review reports indirect donor target answers **0/2**, literal control **1/2**, random **0/2**. Indirect arithmetic retained4 but changed formatting. Later8 appeared in an NLI hypothesis, not an affirmed answer.

The reviewer’s decisive observation:

> “The selected prompt tokens are the trailing space for legs/arithmetic and ` the` for skeleton—not the offline donor's ` It`.”

Role-dependent transfer, weak answer-boundary perturbation, and template effects remain competing hypotheses. Historical selected full-donor steering changed the initial answer in1/4 property/direction cases; preserve that partial positive without treating it as a general rate.

## Options and selection

| Option | Mechanism and useful observation | Decision |
|---|---|---|
| Existing donor, concise property task | Removes NLI ambiguity; could reveal coherent behavior without changing preparation | Comparator |
| New generic donors at matching assistant-start role | Reduces preparation/intervention role mismatch while improving answer assessability | **Selected** |
| Offline fitted/localized direction | Changes representation geometry rather than task alignment | Defer: more fitting assumptions |

Selection is prospective but informed by known dog/spider development failures. No parameter search or unseen-transfer claim.

## Exact proposed prompts

Serialize every prompt identically using the pinned tokenizer:

`apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)`

Then tokenize with `add_special_tokens=False`. Save rendered strings and IDs; verify nonthinking serialization and identical terminal assistant-start suffix/token across preparation and evaluation. Do not silently substitute another template.

Every message list contains system text:

```text
Answer briefly. Do not explain.
```

### Offline preparation

For each `concept` in `spider`, `dog`, use these four user strings, substituting the literal concept:

```text
Consider a {concept}.
Focus on a {concept}.
Picture a {concept}.
Keep a {concept} in mind.
```

These eight contexts contain no tested properties or answers. Animal names are permitted offline, not in evaluated inputs or requested outputs.

### Evaluation: three fixed user strings

```text
For the animal that barks and is called man's best friend, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.
```

```text
For the animal that spins webs to catch flies, give its usual number of legs and whether its skeleton is inside or outside its body. Reply only as '<number>; <inside or outside>'.
```

```text
An animal that barks is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'.
```

Expected Base answers: `4; inside`, `8; outside`, `4; even`. Intended edited animal answers: `8; outside`, `4; inside`. Arithmetic should remain `4; even`.

## Procedure, controls, and budget

Capture each preparation context’s block15 output at its final prompt token. Average four states per animal. Set `delta = mean_spider − mean_dog`, without normalization or fitted strength.

Run four conditions on each evaluation prompt:

1. Base: zero update.
2. New donor: natural delta.
3. Existing job2687 indirect donor: its unchanged natural delta.
4. Random: one seed0 Gaussian direction, normalized to the new delta’s norm.

Use positive delta for dog→spider and arithmetic; negative delta for spider→dog, including the corresponding random sign. Record old/new norms: this does **not** isolate orientation.

At prefill, add delta at the last position; at every cached decode, add0.25delta. Greedy generation, no repetition processor, maximum32 tokens. Base is a separate scored trajectory; none of its activations or outputs controls editing.

Budget: eight preparation forwards plus12 trajectories, at most392 forwards and384 generated tokens. Queue locally with an initial300-second allowance. Preserve incomplete conditions; no replacement prompts or automatic extension.

Observer block23 only records readouts and returns no replacement. Assert one prefill plus `n_tokens−1` cached calls, actual downstream updates, disabled gradients, and total forward accounting.

## Distinguishing observations and risks

- **Useful transfer:** affirmed target-consistent properties within one continuation, beyond random, with arithmetic preserved.
- **Shallow perturbation:** only one property changes. Report this partial result, not coherent replacement.
- **Template/scoring shortcut:** apparent gains are formatting, hypotheses, or uncompleted text. Inspect exact generations.
- **Nonspecific damage:** random behaves similarly, arithmetic changes, or outputs deteriorate.
- **Implementation error:** coverage, serialization, or applied-state checks fail.

Report each property and joint consistency separately. Keep wrong baselines, partial answers, contradictions, and capped outputs in denominators. Joint consistency is evidence beyond a digit, not a universal success gate. One random vector supplies no null distribution; matching assistant-start roles does not guarantee matching semantic states.

## Feasibility / drift check

Source08 supports mean preparation and continuous addition, but is **not ready through flags alone**: indirect mode hardcodes ` It`; ordinary donor random uses the projected norm; arithmetic drops other controls. A small explicit prompt/condition path is needed.

No executor handoff now. Before any source/helper change, check2705’s completed state. No new experiment, independent-family review, or scientific validation occurred here.

Evidence:  
/workspace/2026/suppressed-activations/slop/reviews/2026-10-01_indirect-donor-result-review.md  
/workspace/2026/suppressed-activations/scripts/english/08_jlens_one_pass.py:612

— PI/OpenAI

## Parent decision before implementation

Proceed with the bundled native-chat development attempt. One deliberate change to this proposal: use the fixed literal-name donor (`out/2026-09-30_133218_jlens-one-pass/donors.pt`) as the previous-donor comparator, not the indirect donor. It has the observed skeleton-only partial positive and uses explicit animal names like the new preparation. This is the same comparator for all three prompts, not a per-case winner; differences in templates, role and natural norm still prevent an isolated role-effect claim. The new role-aligned donor remains primary.

Exact prospective data: `data/dog_spider_donors_chat_v4.json` and `data/dog_spider_joint_chat_v1.json`. No neural run has evaluated them. Keep all12 conditions and the8 generic prefills; no dose/layer search. — PI/OpenAI
