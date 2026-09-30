# Input-prefix implementation review

**Verdict:** No demonstrated blocker for the specified four-case cached comparison. One conditional reporting defect; launcher end-to-end validation remains missing. This is not scientific or goal signoff.

## Reviewed evidence

Read all enumerated files completely, both AGENTS.md files and the ml-debug skill. With supervisor permission, also read complete `scripts/english/03_selector_search.py` and `04_erase_and_language_pairs.py` to resolve import interactions. No commands, inference runs, edits, network access or delegation.

### Implementation checks

Observed in `scripts/english/08_jlens_one_pass.py`:

- Lines 604–613 implement complete lowercased regex-word anchoring, length ≥3, using `value.startswith(word)`. No labels or generated text enter this helper.
- Lines 1177–1197 preserve the old mask, record newly excluded IDs and all matching originating words, and save four full-vocabulary original score tensors.
- Candidate scores derive from existing half-erased J/plain scores and mask-only J. Surviving scores are asserted equal. Selection subsequently uses full-vocabulary `topk(32)`, rather than deleting entries from saved lists.
- Replay uses saved states and token IDs. Forward-rejection hooks cover the model and transformer before scoring. Norm/head calls remain permitted; these are not transformer forwards.
- Cyclic mismatch controls are omitted only under the new flag, as requested.
- Known `art→article` overmasking and retained `name→nam` masking are explicitly disclosed.

The supplied smoke log records, for **each of seeds 0 and 1**:

> “44 rows/36 originals exact,8 candidate full-vocabulary top32 refills, exclusion origins, saved-score reconstruction, transformer calls blocked”

These are observed log claims backed by corresponding smoke assertions, not independently rerun results. The smoke uses real tiny BF16 Qwen computation but replaces pretrained loading, lens loading and CUDA placement.

Import concern resolved: `03_selector_search.py` and `04_erase_and_language_pairs.py` temporarily set:

> `_argv, sys.argv = sys.argv, sys.argv[:1]`

Thus `01_detector_baselines_and_pair_transfer.py` does **not** receive the launcher's source pathname in its import-time integer argument parser.

## Finding: conditional nullable-AUROC reporting failure

**Location:** `/workspace/2026/suppressed-activations/slop/audits/2026-10-01_input-prefix-launcher.py:64`

> `'mean_alias_auroc':sum(r['alias_checked_auroc'] for r in rs)/4`

**Observed contract:** `08_jlens_one_pass.py` initializes `checked_auc = None` and retains it when a row is unscorable or its hidden concept was said. Its own summary filters undefined AUROCs and records their denominator. The supplied smoke log contains unscored rows and blank AUROC cells.

**Consequence:** A cached case with undefined AUROC causes this launcher summary to raise `TypeError`, after readout artifacts have been produced but before `paired_summary.json` and `pipeline.json` complete.

**Affected inputs:** Cached continuations containing an unscorable word, the hidden concept, or another condition making checked AUROC undefined.

**Uncertainty/severity:** Conditional reporting defect, **not a demonstrated blocker for the pinned four cases**. Their original cached rows were outside the supplied review evidence. Prefix masking alone does not change AUROC evaluability.

**Disproving check for this launch:** Confirm every original row used by the eight summarized methods has numeric `alias_checked_auroc`. For general schema correctness, preserve undefined values and report the scored denominator, as the main script already does.

## Residual risks and interpretation

- The launcher has not been exercised end-to-end. Static inspection supports its 72-old-plus-16-new assertions, but does not establish that they pass against the actual pinned cache.
- SHA constants are visible in the launcher and the supplied smoke prints the requested source SHA. I did not independently compute hashes or inspect queued copies.
- `preregistration.md` is copied from a live, unhashed review document after scoring (`launcher.py:42`). This does not affect ranking, but the copied document alone cannot establish which preregistration bytes existed before execution.
- Postmask AUROC can improve solely because negatives become `-inf`. Empty `input_hits` are uninformative for these cases, which supply no `input_word`.
- Full-vocabulary refill and lexical passes do not certify clean semantic exclusion or country identity. The launcher correctly leaves semantic review pending; identity **/4**, clean joint **/4**, and discriminating-pair **/2** review remain separate work.

## ML-debug review notes

- **Question isolated:** Does adding the frozen complete-input-prefix mask remove qualifying repeats while retaining unchanged score computation?
- **Control:** Original methods and equally processed plain lenses; smoke reports exact preservation of 36 original rows per seed.
- **Predicted discriminator:** Reconstructed candidate top32 from saved original tensors plus logged exclusions must match emitted IDs/scores; this is asserted in the supplied smoke.
- **Competing explanations for later improvement:** Actual removal of input repeats; replacement by other semantic leaks; inflated lexical/AUROC scoring. Inspect replacement entries and country/partner ranks to distinguish them.
- **Scale:** Exact equality and row counts are structural checks, not chance-adjusted scientific performance. No claim that one method outperforms another is made.
- **Missing evidence:** Real pinned-cache launcher output, independent hash checks, and semantic review. Training schedule, loss and gradient diagnostics are inapplicable; exact consumed production samples and per-stage GPU measurements were not supplied.
- No additional experiment or command was executed or queued.

**Signed: PI/OpenAI**