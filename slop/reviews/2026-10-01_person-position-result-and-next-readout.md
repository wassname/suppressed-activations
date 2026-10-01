# 2718: result and next readout rule

**Recommend one prospective pre-assistant-boundary test, not promotion to v5.** Earlier positions expose useful author information, but do not establish J-lens superiority, clean thought/speech separation, or unseen generalisation.

## Evidence and interpretation

I read all **32 complete top32 lists** in `out/2026-10-01_145856_person-position-diagnostic/position_views.md`, its complete JSON summary, both preregistrations, original2716 data/report, AGENTS, goals/User voice/Interview and ml-debug. Raw position files were inspected selectively; this is **not exhaustive semantic review of every prompt position**.

`out/2026-10-01_145857_jlens-one-pass/position_reproduction.json` records:

> `"final_states_exact": true`, `"generation_traces_exact": true`, `"readout_rows_exact": 88`

Thus the diagnostic preserves the original final-position **0/4**, rather than correcting it. These are recorded checks, not checks I executed. Earlier states are explicitly `"fresh same-settings capture, not historical saved states"`.

### Names: useful but unequal evidence

All following observations come from the complete lists in `position_views.md`:

- **Orwell:** identifiable `Orwell` occurs in all four heads at both views. Boundary half-J begins `[' Winston', ' Orwell', 'George', ...]`; plain27 also puts Orwell second. George alone would be weaker, but Orwell following the distinguishing title is convincing availability evidence.
- **Rushdie:** both J heads and plain27 return `Salman` first at both views; plain24 does not return it. This is a contextually persuasive **partial-name recovery**, not a displayed Rushdie/full-name recovery. Muhammad/Mohammed/Hussein and other names make the surrounding list less selective. Do not discard Salman merely for lacking a surname, or automatically equate its alias hit with unambiguous identification.
- **Cao:** half-J does not return Cao in either top32; boundary masked rank is58. Plain27 boundary contains `曹`, `Cao`, `芹`; title-end contains `芹`. Together these are suggestive Cao-related evidence, stronger than one isolated fragment, but not a decoded full identity. `芹` also occurs in the **Wu plain24 title-end** list, weakening its specificity.
- **Wu:** neither view clearly returns Wu Cheng’en. Boundary J’s best alias is `Chen`, outside top32 at ranks45/47; plain27’s `Cheng` is also outside. Prefix scoring cannot turn Chen/Cheng or generic Chinese surnames into Wu identification.

**Equal controls matter:** plain27 matches the conspicuous Orwell/Salman evidence and supplies the strongest Cao fragments. No demonstrated J-over-plain advantage follows; half-erasure is not necessary for the observed Orwell/Salman recovery.

### Leakage and confounds

The same file shows definite input-equivalent content: `红楼梦` for *Dream of the Red Chamber*, `西游记` for *Journey to the West*, and `作者`/`作家` for author. Wu’s mask-only boundary list contains `中国`, ` Cina`, ` Tiongkok`, etc., overlapping actual **China** output. Half-erased Wu still contains `Chinese`/`Chinese` variants: answer-associated content, though adjectival association should not silently become a universal semantic-failure rule. Orwell’s `英国` overlaps the England/UK region without being an exact England synonym.

Both views are explicitly:

> “chosen after observing those curves”

Title-end selection uses labelled task structure. Selecting the best alias position is more directly oracle-based; pooling avoids explicit labels only if frozen independently, but introduces more opportunities for generic/preclue hits. Neither is a held-out comparator. Protocol/preclue occurrences cannot establish clue use; this limited semantic review does not certify their absence.

## One next rule and test

Freeze **the last token of `apply_chat_template(..., add_generation_prompt=False)`**, retaining J24/k32, final-greedy end-pass half-erasure, complete-input/output masks, and equally processed plain24/plain27 plus mask-only J. Assert that its token IDs are an exact prefix of the actual generation prompt; do not silently substitute “last user word.” This is a post2718 choice and end-pass readout, not information available to an earlier causal editor.

Run **one six-prompt development test**: four deterministically selected existing native-chat non-geography cases plus two existing translation prompts, frozen before inspecting boundary results. Compare boundary versus original final position on identical captures; print every complete list, actual output and a fixed preclue control. No v5, pooling, title-end rescue or alias expansion.

Boundary gains that remain clue-associated across tasks would justify a subsequent frozen unseen evaluation. Plain-control ties, preclue persistence or lost translation separation would weaken the rationale. No new full-name, purity or bidirectionality threshold is needed.

**ml-debug/residual limits:** pipeline reports18.296s,8.088GiB,8 forwards/8 tokens. Training loss/gradients are inapplicable. Competing explanations remain localization, title/cultural shortcuts and alias ambiguity; exact replay constrains—but does not independently eliminate—implementation error. No chance-calibrated identity statistic, seed spread, independent neural replication or causal necessity was established. This is same-family, read-only artifact review; no commands, inference, network, edits or delegation occurred. Country-donor work remains separate.

— **PI/OpenAI**