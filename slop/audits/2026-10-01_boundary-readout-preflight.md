# Boundary readout launch checks

— PI/OpenAI. No pretrained boundary result yet.

- Core tiny BF16 Qwen tests at seeds0/1 pass:132 old final-position rows exact+48 boundary/preclue rows, identical full generations/final states, no cached forwards, raw-head consistency and corrupt-template-prefix rejection.83s. `boundary-readout-smoke.log`.
- Actual immutable-path coordinator passes with one fresh tiny model,192 forwards for192 generated tokens,180 rows and72 selected-position lists; six-case provenance checks and grouped reporting executed.20s. `boundary-launcher-smoke.log`.
- Initial freeze whitespace check stops on four lines of verbatim tiny-model tab output in the two smoke logs. Preserve these bytes; scope the repeated check to exclude those two logs and the saved whitespace report, not source/data.
- Same-family read-only review found no concrete blocker. Tiny J matrices are identity and raw-head reconstruction reuses the helper; these are plumbing checks, not independent learned-J validation. Production also asserts equality with the separate existing final-position scoring path using the learned J. Do not relax a parity failure.
- Selection: first4 native-v4 cases, translation source indices0/40 (de→fr/fr→de, bothcloud). Native translation wrapper is a declared change. Nuage's prior canonical scoreability limitation remains; no replacement or v5 use.
- One inference capture per input; final/boundary/preclue share states/generation. Position selection uses chat metadata only. Every selected head uses the same complete-input masks and final-greedy output direction; preclue is not an independent early causal measurement.
- Production manifest pins08, coordinator, shared helpers/checker, both source datasets, six-case data, contract and dependency files. Immutable source/launcher copies do not sandbox imported files: hold those pins unchanged through execution.

Options/predictions are in `boundary-readout-preregistration.md`. A frozen boundary may expose identities beyond person examples; persistent preclue hits would instead implicate prior/mask effects. Plain ties do not imply J superiority. Full lists/generations, including wrong/capped/unscoreable results, decide interpretation; no aggregate lexical/AUROC-only promotion. No fitting, optimizer or gradient schedule applies. One default-lane job,300s cap, at most192 generated-token forwards. Both goals remain open.
