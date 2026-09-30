# job2648 validity review

Read all scoped files, including the complete 49-line console, both complete run reports (240/230 lines), source, and intervention records. `out/2026-10-01_001654_country-swap/job.json` records `"result": "Success"`; this establishes process completion, not scientific success.

| Stage | Expected | Observed | Consequence |
|---|---|---|---|
| Baselines | Rome/euro | “ Rome.” / “ the Euro.” | Initial answers valid |
| Exchange | Current-state coordinate swap | Nonzero edits; approximately exchanged coordinates | Numerical implementation supported, independently unchecked |
| Coverage | Last prompt position plus cached decode | “Coverage: 32 calls” for all ten conditions | Recorded schedule matches contract |
| Outcome | Coherent Tokyo and yen | All five conditions retain identical continuations within each property | Frozen success condition unmet |

## Strongest defensible outcome

`slop/audits/2026-09-30_country-swap-preregistration.md` requires:

> both source baselines and both coherent target outcomes under the same primary are required; no alternate-winner, prompt, strength, layer or coverage rescue.

The primary produces neither target answer: **0/2 properties**, comprising one selected country pair, not independent swaps or a generalisation estimate. Its bare-answer log-odds shifts exceed the single random control on both properties: capital +0.0625 versus −0.0625; currency +0.25 versus 0 (`out/2026-10-01_001654_country-swap/console.log`). These distribution changes coexist with unchanged generated answers.

## Top bugs and misconceptions

1. **Numerical exchange is not semantic replacement.** In `out/2026-10-01_001715_jlens-one-pass/interventions.json`, primary prefill coordinates change from `[0.14933905005455017, 0.09499005973339081]` to `[0.09479998052120209, 0.14944912493228912]`, yet generation remains Rome. `out/2026-10-01_001654_country-swap/source.py:51–68` implements coordinate exchange, not score exchange. No definite algebra defect found. The earliest unsupported link is interpreting these coordinates as causally sufficient country identity; saved-tensor reconstruction can challenge implementation correctness, but cannot establish semantics.

2. **Currency first-token scoring does not measure the emitted answer.** `out/2026-10-01_001732_jlens-one-pass/run.md` reports Base `p( euro)=0.00139327`, while generation is “ the Euro.” The initial article and capitalization explain why low bare-answer mass does not invalidate Base or demonstrate incoherence. Full-answer probabilities are absent.

3. **NLI hypotheses are generated propositions under consideration, not endorsed assertions.** Both complete reports follow their initial answer with “Hypothesis:” and “Is the hypothesis true or false?” Thus “not Rome” and “the Dollar” do not independently establish contradictory beliefs or malformed output. Neither continuation explicitly names Italy. The 32-token caps leave the NLI judgment unfinished.

4. **Observer output cannot certify suppressed thought.** Both reports state “prompt-word removal only; no final-layer output mask.” Their readouts include the spoken answers Rome/Euro. Finding Italy alongside them does not satisfy hidden-found-and-said-excluded recovery.

## Coverage gaps and smallest next step

No independent tensor/hash verification or checker result was supplied. Lens fitting-model revision is explicitly unrecorded; target currency has only a prefill, not a complete answer. One random direction provides no null distribution.

Obtain the already-running CPU checker’s complete result, without new inference. Agreement across saved bases, applied states, coverage, and token IDs strengthens the narrow negative result; disagreement identifies an implementation/provenance issue before attributing failure to representation quality.

PI/OpenAI