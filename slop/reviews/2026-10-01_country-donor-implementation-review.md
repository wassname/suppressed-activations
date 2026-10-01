# Country-donor implementation review

**Verdict:** No concrete implementation blocker found for the supplied Sweden/Japan configuration. Launch provenance remains **unattested**, not disproven. This is a same-family static review, not scientific validation.

## Observed implementation

- **Signs and natural scale:** `scripts/english/08_jlens_one_pass.py:1686–1723` constructs `means[concepts[0]] - means[concepts[1]]`, then uses `"full_delta if reverse else -full_delta"`. With `["Sweden","Japan"]`, Sweden→Japan and arithmetic receive Japan−Sweden; reverse receives Sweden−Japan. Only random is norm-matched. The chat guard excludes donor rescaling, projection variants and reflection.
- **Actual concept keys:** `prepare_donors` stores means under configured names. Country diagnostic directions use `" Sweden"`/`" Japan"`, not animal slots. Compared with the relevant preparation/causal sections of `out/2026-10-01_145857_jlens-one-pass/source.py`, animal defaults retain spider/dog ordering, signs and the optional historical comparator.
- **Capital semantics:** `slop/audits/2026-10-01_country-donor-tokenization.json` records **without leading spaces** `"Stockholm": [18782,32393]` and `"Tokyo": [51076,15560]`. Script lines 1773–1789 derive labels from non-arithmetic cases and use their first IDs. Lines 1919–1930 compute Tokyo-first versus Stockholm-first log-odds change and explicitly save `"first token only; not a full multi-token answer probability"`. Positive favors Tokyo; reverse success has negative shift. Country rows do not receive animal `p8/p4` aliases.
- **Controls and coverage:** All three cases retain Base, donor and matched random; arithmetic expectations remain `4; even`. Script lines 1822–1895 apply the fixed delta at final prompt position and quarter-strength at each cached decode. Observers return no replacement. Stored original/requested/BF16-applied states permit signed-delta reconstruction. No country target-probe branch or current-input preparatory/backward pass is selected.
- **Supplied test evidence:** `country-donor-smoke.log` reports both seeds passing “8 generic prefills,9 trajectories” with exact requested/BF16/downstream states and unchanged weights/hooks/defaults. `country-animal-regression.log` reports both seeds passing twelve animal trajectories, early EOS and interruption retention. `country-launcher-smoke.log` records country `"actual_forwards": 296`, `"generated_tokens": 288` and animal 392/384: eight preparation forwards plus one forward per generated token. These are tiny random models, not country-editing results.

## Provenance qualification / nonblocking risk

`slop/audits/2026-10-01_chat-causal-launcher.py:22–39` verifies the supplied manifest and **listed** pins, archives source/inputs, and records donor hashes. However, `"for path,sha in manifest['pins'].items()"` does not require the selected config, donor config, launcher or imported helpers to be present; execution also reads working-tree input paths after initial verification.

**Affected inputs:** an incomplete manifest or files changed after verification. **Uncertainty:** no prospective production manifest/queue wrapper was supplied, so neither omission nor mutation is established. **Disproof/check:** inspect the actual frozen manifest and launch command, including selected configs, launcher/helpers, source identity, unchanged execution inputs and external 300-second timeout. The launcher itself does not enforce that timeout.

## Residual scientific limits

No pretrained country output exists here. Natural norm/context changes confound domain-only attribution; one selected pair and one random direction cannot establish general transfer. Capital prefixes can improve without correct capitals/currencies; arithmetic capital-token mass is not coherence. Evaluate complete continuations, both properties, country spills, wrong Bases and caps. Prompt-masked observer readouts do not certify hidden-not-said recovery.

Read AGENTS.md and ml-debug; executed no commands, inference, edits or delegation.

— **PI/OpenAI**