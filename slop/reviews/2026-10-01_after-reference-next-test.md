## Recommendation

Run the four person-bridge probes with unchanged2686 readout through production08, within one local300-second job. This is a useful development test, not evidence of necessary mediation or unseen-concept generalization.

I asked whether the priority was identity recovery or ruling out country shortcuts. The parent chose recovery, preserving own/partner comparisons and equally processed plain controls. Under that scope, the probes are informative enough.

### Evidence and comparison

`slop/audits/2026-10-01_job2705.md` reports:

> “Generic J still recovers December, Thursday, autumn, violin and triangle:5/8, like unchanged J.”

All methods returned zero confirmed animal identities. Preference reversals without returned identities therefore cannot justify another subtraction variant.

The proposed Orwell/Rushdie and Cao/Wu pairs test whether the unchanged method returns different people despite shared expected answers. Recovering Orwell only for Orwell’s book and Rushdie only for Rushdie’s book is more informative than improving country-answer margins. Returning both authors indiscriminately is weaker evidence.

A genuinely distinct alternative is a **direct offline affine decoder**, using08’s `fit_affine`/`fit_forecast` machinery to map intermediate residuals into decoder space, rather than subtracting its prediction from J scores. `scripts/english/08_jlens_one_pass.py:556–609` fits this mapping on generic text without task labels. This changes the decoder, not a projection coefficient.

I would defer it: its training target is the final residual, so it may amplify spoken answers rather than expose suppressed identities. Existing forecast validation establishes output prediction, not hidden-identity recovery. Combining it with current chat/masking/replay branches would also require explicit integration and validation; it is not a ready unchanged-method comparison. The four probes more cheaply distinguish a person-recovery capability from another representation change.

### Conditions before launch

1. Preserve deterministic corpus selection, all four cases, native no-thinking rendering, EOS union and32-token cap. Modern-country wording is an explicit data change. Wu’s authorship is traditional attribution. Chinese-book country shortcuts remain plausible even after selective author recovery.

2. Reuse08 capture and guarded cached rescoring, not06’s knowledge filter. `scripts/english/06_twohop_english.py` explicitly runs:
   > `hop1 = greedy(r["r1(e1).prompt"])`

   That preliminary first-hop call is outside this test.

3. Check name scoring before inference. `scripts/english/08_jlens_one_pass.py:1150–1170` derives individual `actual_words` but tests:
   > `hidden_is_said = any(a.casefold() in actual_words for a in hidden_aliases)`

   **Observed:** a multiword alias cannot equal one word in that list. **Risk:** full-name-only aliases can miss an explicitly spoken person; short prefixes can also overclaim identity. Affects all four multiword names, especially fragmented/transliterated Chinese names. Disprove the scoring concern with evaluation-only fixtures containing each complete spoken name, surname and ambiguous fragment. Freeze identity-bearing aliases; retain manual full-output adjudication. No ranking or mask repair is implied.

4. Adapt—not blindly rerun—`slop/audits/2026-10-01_native-v4-launcher.py`: it asserts eight cases and the exact old dataset transformation. Preserve forward rejection, coverage checks and old-row replay equality.

### Interpretation

Report complete lists and actual continuations for every method, with identity recovery, input exclusion and actual-output exclusion separately. Compare own/partner membership and ranks before/after masks; margins alone are not recovery. Retain wrong, overlong and identity-spilling outputs. No new universal threshold.

No new-prompt outcomes exist. Causal2706’s unchanged outputs are supplied information, not independently audited here, and do not decide this readout comparison.

— PI/OpenAI