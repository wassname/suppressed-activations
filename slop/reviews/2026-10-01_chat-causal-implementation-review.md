# Native-chat causal implementation review

— PI/OpenAI

Same-family static review, not independent-family, neural, or scientific approval. Read all supplied files, complete source08, applicable AGENTS.md, and ml-debug skill. No commands, inference runs, edits, or delegation performed.

## Verdict

No concrete execution blocker found for the specified configuration. One definite reporting defect should be corrected. Launcher readiness remains unverified: the supplied smoke exercises source08, not the launcher as a whole.

## Finding: incorrect arithmetic-control report

**Observed code:**  
`/workspace/2026/suppressed-activations/scripts/english/08_jlens_one_pass.py:1960` writes:

> “no random arithmetic condition was run.”

For native-chat arithmetic this is false. Lines1726–1727 restrict the old two-condition arithmetic override to `chat_causal_json is None`; native-chat retains Base, both donors, and matched random.

**Affected input:** `arithmetic_control`, case index2 in `data/dog_spider_joint_chat_v1.json`.

**Impact:** The generated case `run.md` contradicts its own table and can cause a reviewer to overlook the specificity control. This is a reporting defect, not evidence that generation is wrong.

**Check:** Render the native-chat arithmetic report and require that its control description agrees with all four `interventions.json` entries. Preserve the old description only for paths actually omitting random.

## Checks supported by static evidence

- **Generic-only preparation:** source08:623–671 captures raw final-position block15 outputs and averages each concept’s four states. The supplied donor configuration contains animal names but no evaluated properties or answers.
- **One-pass boundary:** donor-checkpoint execution leaves standalone `cases` empty. Each condition invokes `generate` once; the editing hook uses fixed donor deltas. Observer23 at source08:1812–1814 appends readouts and returns no replacement. Base probabilities are used for reporting, not editing.
- **Signs and controls:** source08:1613–1614 and1649–1653 implement positive spider-minus-dog for dog→spider/arithmetic and negative for spider→dog. The previous comparator is the hash-pinned **literal-name donor**, consistent with the appended parent decision, not the superseded indirect comparator.
- **Norm claims:** new donor remains unscaled; old donor retains its own natural norm; seed0 random matches the new requested norm. Documentation correctly disclaims orientation-only attribution. BF16 realized perturbations need not have exactly matching norms.
- **Schedule/accounting:** guards fix block15, observer23, last prompt position and decode0.25. Source08:1822–1828 checks one recorded edit/readout per generated token and singleton cached decode calls. Launcher:102’s surrounding completion accounting is supplemented by its explicit `len(events)==8+total_tokens<=392` assertion at line92: eight preparation forwards plus twelve trajectories capped at32.
- **Properties:** joint expectations are preserved separately from legacy digit labels. Arithmetic `expected_properties` remains `["4","even"]`, including random; `expected_answer="control"` is legitimate legacy metadata. Fixed 8→4 log-odds shift has the correct arithmetic; dog→spider success would have negative shift.
- **Old paths:** new serialization and EOS overrides are conditional. The diff does not replace existing completion behavior. This is static evidence, not comprehensive regression coverage.

## Smoke evidence and limitations

The third supplied log now ends:

> “PASS seed1:8 native generic prefills … early EOS coverage; interruption retains3 completed contexts”  
> “PASS tiny random CPU models only; no pretrained scientific result”

It also contains the seed0 PASS. Thus two-seed smoke completion is observed, rather than inferred from a running process.

The retained failures remain informative:
- First: `TypeError: '<' not supported between instances of 'int' and 'NoneType'` at EOS construction. The current fixture pins model EOS248044; production EOS configuration was not independently inspected here.
- Second: the fixture asserted every arithmetic `expected_answer` was `"4"`, incorrectly rejecting random’s `"control"` label.

The smoke checks exact means, signed vectors, requested/BF16/downstream states, hook ownership, unchanged weights/defaults, early EOS and interruption retention. It does not establish semantic steering.

## Residual risks / next verification

Before relying on launcher readiness, exercise its actual manifest/source-copy entry point with a tiny model. Source08 derives `ROOT` from `__file__`, whereas the launcher uses cwd; a relocated immutable source must retain a compatible path layout. No frozen launch invocation or manifest was supplied to resolve this risk.

Scientific alternatives remain untested: useful role-aligned transfer, shallow answer perturbation, nonspecific damage, and unknown implementation/runtime effects. Exact joint-property review and arithmetic/random comparison distinguish them; first-token odds alone do not. No pretrained causal run or broad old-path regression evidence was supplied.

## Parent repair and launcher check — PI/OpenAI

Corrected the native arithmetic report to say all four conditions should retain4 and even; legacy paths retain their old description. The full launcher smoke passes35s and asserts that the incorrect sentence is absent. It loads an immutable source copy under `.local/queued/`, then uses four fresh tiny models for eight preparation prefills and twelve conditions. Forward counts, signs, norms and the final report pass. The core two-seed smoke passed179s before this reporting-only fix; both earlier fixture-failure logs remain. This is parent verification, not a second reviewer approval or a pretrained result.