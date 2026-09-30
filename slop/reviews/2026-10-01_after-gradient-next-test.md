## Choose (a): frozen half-erasure on four new geography prompts

This is the smallest attempt with existing positive evidence: `README.md` reports “seven J passes, all geography,” under a posthoc semantic audit. Test whether that restricted result survives ordinary chat and distinguishes countries when the answer stays the same.

| Option | Decision |
|---|---|
| (a) Frozen half-erasure | Choose: direct transfer attempt, four generations, existing implementation. |
| (b) Predicted-token gradient×activation | Defer: attributes the spoken token, which may emphasize answer production rather than distinguish hidden concepts. Requires explicitly disclosed backward computation and a new attribution-to-word rule. |
| (c) Online component intervention | Defer: current evidence does not identify a component with demonstrated property transfer. Another selected answer flip would not resolve that gap. |

### Evidence behind the choice

`out/2026-10-01_045248_jlens-one-pass/gradient_pursuit_selection.json` records `"paired_gains": []` and `"new_vs_native_matching_pursuit": []`. `fit_comparison.json` shows remaining J energy falling from 0.897644 to 0.877486. Refitting improved reconstruction without the intended recovery gain.

The complete `case_comparison.md` supports the semantic cautions: violin occurs before “played by Sherlock Holmes,” and its baseline says “the woodwind family.” Hamlet’s list contains both `" HAM"` and `" Shakespeare"`; the former is ambiguous, the latter definite answer leakage. These observations do not justify rescuing GP. Keep v5 unused.

### Prospective contract

Use four user messages following this exact pattern:

> Answer with only the continent name: On which continent is the country whose capital is Muscat?

Substitute **Muscat, Doha, Windhoek, Gaborone**, yielding intended hidden countries Oman/Qatar and Namibia/Botswana, with shared answers Asia and Africa respectively.

These are proposed inputs, not verified-new concepts. The supervisor confirmed a pre-inference inventory check is available. Check all previous inventories, including TwoHopFact, before freezing; disclose any overlap rather than claiming concept novelty. Fix labels and aliases before inference.

Use the pinned tokenizer’s native chat template with `enable_thinking=False`, `add_generation_prompt=True`; inspect rendered text/token IDs and EOS policy before submission. Remove the old Japan/Tokyo demonstration prefix. This is explicitly a new prompt setting.

Keep J24, last-prefill position, k32, greedy-output mask1, and half-erasure unchanged. End-of-pass information is permitted for this readout. Actual generated words enter scoring only, never filtering or ranking.

### Controls and distinguishing observation

From each unchanged generation trajectory, compare:

- Equally masked/half-erased plain24 and plain27.
- Mask-only J24, to test whether erasure contributes.
- Each country’s rank against its same-answer partner’s rank, using frozen identity aliases.

A useful positive is a semantically clean hidden-country readout that changes appropriately between both members of a correctly answered pair despite their shared answer. An unchanged list containing both countries, or a list explained by continent/topic priors, does not demonstrate pair discrimination.

Inspect all32 entries symmetrically for input/actual-output equivalents and ambiguous fragments. Report lexical and reviewed semantic counts separately, AUROC with its eligible denominator, baseline accuracy, prompt successes/4 and discriminating pairs/2. Retain wrong answers, truncations and unscorable cases. Select any displayed demo after inspection and disclose that selection. No universal-success threshold.

### Execution boundary and limitations

Minimally extend `scripts/english/08_jlens_one_pass.py` for native chat and configurable generation length; its current `generate_readout` hardcodes eight tokens. Preserve the old default. Use four greedy continuations, maximum32 tokens each, recording actual EOS counts and same-trajectory capture coverage. One local pueue-default job, 300s plus15s grace; no parallel inference pipeline.

Success supports a selected geography readout demo, not causal necessity or goal2. Failure leaves both goals open.

PI/OpenAI; same-family advice, not signoff. No execution or edits.