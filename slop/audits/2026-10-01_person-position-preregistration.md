# Person-bridge position diagnostic

— PI/OpenAI. Declared after2716; not a new success rate or a frozen deployable selector.

2716 returns no author identities in four prompts, while primary lists contain country alternatives. Its `prefill.pt` keeps only final-position states (`state[-1]` in08), despite capturing complete prefill states transiently. Earlier states cannot be inspected without recapture. The prior chat proposal to inspect saved earlier states was premature.

One short local/default-queue run will recapture the exact four2716 inputs through `scripts/english/08_jlens_one_pass.py`, at the same model/layers/native template/greedy32-token cap, and retain full prefill states. No first-hop filter, new prompts, k/mask/strength change or v5. Assert complete generated IDs, final states and every existing88 readout row equal the recorded2716 capture/replay. A mismatch stops interpretation; preserve partial artifacts.

During the same pipeline, inspect every prefill position using the four frozen readout heads (half J24/plain24/plain27 and mask-only J24). Use the same complete-input and final-greedy output masks and half-erasure direction as2716. These are end-of-pass diagnostics, not information available to an earlier editor. No transformer call beyond the four ordinary generations; at most128 calls, expected8 if outputs reproduce.

Save each position's consumed prefix, full top32 IDs/text/scores, unmasked and masked alias ranks, best alias IDs and final-position exact-score parity. Persist all positions, including protocol/early positions. Alias labels are used only for the diagnostic ranks, never to construct a direction, mask or top32. Label-selected best position is explicitly oracle analysis and not a deployable rule. Ambiguous `George`, `Cao`, `Wu` or short fragments do not automatically identify people; names before a distinguishing clue do not establish its use.

Predictions: (1) a location problem permits clear names after the corresponding book cue, before the final country answer position; (2) a broader representation/shortcut problem need not reveal names anywhere under these heads; (3) implementation inconsistency changes the replicated final states, IDs or scores. Complete-prefix provenance discriminates generic preclue hits from context-dependent recovery. An absence across these positions still does not prove absence from other layers or nonlinear representations.

Tiny real-pipeline testing must check defaults, all-position coverage and final-score equality before queueing. Keep source/inputs immutable. Judge a new position selector only after this diagnostic motivates one; do not promote per-case oracle positions or select a larger k. The new causal country-pair proposal remains separate and unimplemented.
