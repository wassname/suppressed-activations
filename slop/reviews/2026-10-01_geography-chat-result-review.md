# Geography native-chat semantic review

**Result:** Oman and Qatar are recovered and ranked above their same-answer partners by both J methods. This is partial identity evidence, not clean suppression: input equivalents remain, and mask-only J also returns Chinese “Asia”. All four methods have **0/4 clean joint passes and 0/2 clean discriminating pairs** under the frozen criteria.

Reviewed the complete supplied files, including all 16 preregistered top-32 lists (512 entries) and their shared complete continuations. No commands, inference runs, edits, discovery, network access, or delegation.

## Baselines and unchanged lexical results

`out/2026-10-01_060504_jlens-one-pass/generation_traces.json` records:

| Case | Complete continuation | IDs | Correct / instruction-adherent |
|---|---|---|---|
| Oman | `Asia<|im_end|>` | `[37186, 248046]` | Yes / yes |
| Qatar | `Asia<|im_end|>` | `[37186, 248046]` | Yes / yes |
| Namibia | `Africa<|im_end|>` | `[71090, 248046]` | Yes / yes |
| Botswana | `Africa<|im_end|>` | `[71090, 248046]` | Yes / yes |

These are four trajectories, reused across methods—not 16 independent generations. Each stopped after two tokens. There is no later generated scaffold. The empty `<think>` block belongs to the rendered input.

The following values are preserved from `out/2026-10-01_060504_jlens-one-pass/paired_summary.json`, not replaced by semantic scores:

| Method | Lexical joint | Mean alias AUROC | Eligible n | Lexically discriminating pairs |
|---|---:|---:|---:|---:|
| erased0.5 J-lens | 2/4 | 0.8928571492433548 | 4 | 1/2 |
| erased0.5 plain24 | 0/4 | 0.8928571492433548 | 4 | 0/2 |
| erased0.5 plain27 | 0/4 | 0.8928571492433548 | 4 | 0/2 |
| mask-only J-lens | 2/4 | 0.8928571492433548 | 4 | 1/2 |

All names below omit their common `end-pass` prefix.

## Semantic annotations

Positions below are **one-based list positions**, not the frozen zero-based, strictly-greater-score ranks. All 512 entries were inspected. Entries not identified below provide no clear target identity or definite input/output equivalent in this review; that is not exhaustive multilingual certification.

`continents`, `continental`, and `Continental` repeat the input concept “continent”. `大陆` can mean mainland or continent; I flag it as **ambiguous input-equivalent evidence**, rather than making it necessary to any failure verdict. Likewise, unrelated countries and continents are not automatically output leaks.

| Method / case | Clear hidden identity | Definite input equivalents | Definite actual-output equivalents | Other ambiguity or qualification |
|---|---|---|---|---|
| J-half / Oman | ` Oman` #5 | ` continents` #14; `continental` #29 | None observed | `大陆` #10; ` Oce`, ` Euras` fragments. Partner ` Qatar` #21 is not Oman evidence. |
| J-half / Qatar | ` Qatar` #5 | ` continents` #9; `continental` #24; ` Continental` #30 | None observed | `大陆` #12; ` Oce`, ` Scandin` fragments. |
| J-half / Namibia | None | ` continents` #6; ` Continental` #11; ` continental` #13; `continental` #14 | `非洲` #12; ` Afrika` #21 | `大陆` #4; `南非` means South Africa, not Namibia; directional and regional associations do not identify Namibia. |
| J-half / Botswana | None | ` continents` #16; `continental` #20 | `非洲` #8; ` Afrika` #30 | `大陆` #6; `南非` is not Botswana. ` Oce`, ` Euras` remain fragments. |
| plain24-half / Oman | None | None definite | None definite | `大陆` #12; `祖国` (“homeland”) is country-related but not an exact referent; ` 동아` can suggest East Asia but is incomplete/ambiguous. ` Oce`, ` premi`, `inį`, ` vaid` do not establish identity. |
| plain24-half / Qatar | None | None definite | None observed | `خلي` is incomplete/ambiguous, not Qatar identity. ` Oce`, ` specif`, `IRTH`, `влека`, `inį` and other fragments do not supply identity. |
| plain24-half / Namibia | None | None definite | None observed | `大陆` #9; ` Bunda`, ` Lâm`, `xia`, `IRTH`, and other unrelated words/fragments are not Namibia evidence. |
| plain24-half / Botswana | None | None definite | None observed | `大陆` #32; ` Bunda`, `ardia`, `itic`, `xia`, `خلي`, `IRTH` do not identify Botswana. |
| plain27-half / Oman | None | ` continental` #11 | `亚洲` #4 | `大陆` absent. `<think>` #16 repeats an input protocol token, not generated thought. ` آسی`, ` Euras`, ` Oce`, ` Antar`, ` 동아`, `-A`, `_A`, `[A` are incomplete/ambiguous; Asian subregions are associations, not exact Asia equivalents. |
| plain27-half / Qatar | None | ` continental` #17; ` continents` #19 | `亚洲` #2 | `<think>` #25 is input protocol. ` châu` can mean continent but is polysemous; `ทวี`, ` آسی`, ` Euras`, ` Oce`, ` Antar` are incomplete/ambiguous. |
| plain27-half / Namibia | None | ` continental` #3; ` continents` #8; ` continente` #18; `continental` #24 | `非洲` #1; ` Afrika` #2; ` África` #7; `Afrique` #17; ` Afrique` #29 | `洲`, `大陆`, ` châu` are context-sensitive continent evidence. ` kont`, ` конт`, ` Kont`, ` Афри`, ` Af`, `AF`, `ทวี`, ` 남아`, replacement character remain ambiguous/incomplete. ` Afro` is Africa-related, not country identity. |
| plain27-half / Botswana | None | ` continental` #3; ` continents` #6; ` continente` #8; `continental` #24 | `非洲` #1; ` Afrika` #5; ` África` #9; `Afrique` #16; ` Afrique` #32 | Same fragment cautions; additionally `_CONT`, `,A`, ` Rhodes`, and ` continuum` do not establish Botswana identity. |
| mask-only J / Oman | ` Oman` #9 | ` continents` #12; `continental` #22 | `亚洲` #8 | `大陆` #15; ` Oce`, ` Euras` fragments. Partner ` Qatar` #26 is separately retained. |
| mask-only J / Qatar | ` Qatar` #9 | ` continents` #7; `continental` #19 | `亚洲` #11 | `大陆` #17; ` Oce`, ` Scandin`, ` Euras` fragments. |
| mask-only J / Namibia | None | ` continents` #9; `continental` #15; ` Continental` #26 | `非洲` #3; ` África` #8; ` Afrika` #11; ` Afrique` #16; `Afrique` #30 | `大陆` #10; `frica` #20 is a strong Africa fragment but not needed for failure. |
| mask-only J / Botswana | None | ` continents` #21; `continental` #22 | `非洲` #3; ` África` #8; ` Afrika` #10; ` Afrique` #18; `Afrique` #26 | `大陆` #16; `frica` #32 is a strong Africa fragment, not Botswana. |

Primary evidence: `out/2026-10-01_060504_jlens-one-pass/case_comparison.md` and corresponding `top32` fields in `readout.json`.

### Counts and frozen paired ranks

“No observed” means no definite equivalent found; ambiguities above remain open.

| Method | Clear identities | No definite input leak observed | No definite output leak observed | Clean joint | Clean pairs |
|---|---:|---:|---:|---:|---:|
| J-half | 2/4 | 0/4 | 2/4 | 0/4 | 0/2 |
| plain24-half | 0/4 | 4/4* | 4/4* | 0/4 | 0/2 |
| plain27-half | 0/4 | 0/4 | 0/4 | 0/4 | 0/2 |
| mask-only J | 2/4 | 0/4 | 0/4 | 0/4 | 0/2 |

\* Includes flagged ambiguous entries; not a cleanliness certificate. Treating `大陆` as an input equivalent would reduce plain24’s input count to 1/4 without changing any joint or pair conclusion.

Exact saved own/partner ranks:

| Method | Oman | Qatar | Namibia | Botswana |
|---|---:|---:|---:|---:|
| J-half | 4/18 | 4/131 | 121547/936 | 766/142010 |
| plain24-half | 8833/8275 | 599/41654 | 14503/30713 | 18665/46474 |
| plain27-half | 2986/11326 | 1337/89217 | 26396/197 | 122/67049 |
| mask-only J | 8/24 | 8/164 | 83562/1636 | 1962/103668 |

Both J methods show the correct directional distinction for the Asia pair with each own identity actually returned. Failed exclusion does **not** erase this evidence. Neither African country is clearly recovered. Under preregistration, the absence of a clean pair leaves the proposed clean demonstration unsupported; it does not imply the method has no identity information.

## Findings and interpretation limits

### 1. AUROC is mechanically favorable after masking—not strong ranking evidence

`out/2026-10-01_060504_jlens-one-pass/source.py` computes:

> `positives, negatives = z[checked_hidden, None], z[checked_said][None, :]`

and awards half credit for equality, after output and prompt masking to `-torch.inf`.

Observed in `readout.json`: the four preregistered methods all have per-case AUROCs **1.0, 1.0, 0.5714285969734192, 1.0**, and `r_said: 1000000000`. Namibia lists six excluded hidden variants:

> `"nam", " nam", " Nam", "Nam", " NAM", "NAM"`

with best remaining token `" nami"`.

**Static interpretation:** finite positive labels beat masked negative labels regardless of their vocabulary rank; masked positives tie masked negatives. This explains why the same high aggregate accompanies unrelated controls and failed recovery. The numerical pattern is consistent with one finite Namibia label and six masked labels receiving tie credit. I did not independently reconstruct mask tensors or scores.

**Disproving check:** independently inspect all positive/negative label scores and mask membership from saved states. Finding finite said-label scores driving meaningful ordering would contradict the all-masked explanation.

### 2. Empty lexical input-hit arrays do not establish input exclusion

`source.py` defines:

> `input_label_ids = set(label_ids(case["input_word"])) if "input_word" in case else set()`

The geography data has no `input_word`. Thus `"input_hits": []` is not evidence against the observed `continents`/`continental` leaks. The prompt mask is a separate mechanism and demonstrably does not remove these returned variants.

**Disproving check:** show these variants are not input equivalents under an explicitly different semantic rule. The frozen rule does not provide such an exemption.

### 3. Vocabulary granularity limits the interpretation of African failures

`country-vocabulary-entries.json` contains only:

> `"ĠQatar": 40536, "ĠOman": 78331`

That exact-key result does not demonstrate inability to represent Namibia or Botswana. The scoring labels include ambiguous pieces; saved best tokens include `" nami"`, `" Bot"`, and `"bots"`, outside the returned lists. A single-vocabulary-token readout can disadvantage multi-piece names. This measurement limitation coexists with the observed semantic failure to recover these identities; neither establishes absence of an internal country concept.

No retrospective replacement cases or fragment promotion is justified.

## ML-debug evidence and residual risks

- **Log/config:** full `console.log` read; job 2673 reports `"Success"`. Frozen native chat, greedy generation, cap32, J24, mask1, half-erasure, k32 are corroborated by launcher/source and artifacts.
- **Expected versus observed:** source’s SHOULD says masking improves joint recovery; lexical J improves from 0/4 unmasked to 2/4 masked. Semantic cleanliness does not follow.
- **Controls/null:** plain controls recover 0/4 identities; negative-final control shares the high AUROC. Exchangeable unmasked labels would suggest AUROC 0.5, but these masks invalidate that as the operative null. No random/shuffled numerical reconstruction was supplied.
- **Training/init/schedule/loss/gradients:** not applicable; this is frozen inference/readout, not training.
- **Full sample:** Muscat rendered input and `Asia<|im_end|>` were inspected alongside its complete lists and coverage `[31,1]`. Gaborone uses `[32,1]`.
- **Competing explanations:** output-label masking explains AUROC saturation; multilingual/morphological gaps explain false lexical cleanliness; vocabulary granularity may contribute to African misses. A numerical implementation error remains unexcluded by this semantic review. No fabricated calibrated percentages are assigned.
- **Three ways stronger claims fail:** lexical exclusion misses translations; token-prefix ranks need not rank identities; selected geography pairs need not generalize. All three are directly relevant here.
- **Independent checks:** runtime assertions are visible; tiny tests are parent-reported, not independently inspected here. No new independent numerical reconstruction was executed. Helper implementations are outside the exact read scope.
- **Cost:** `pipeline.json` reports 43.07231281790882 seconds, peak allocated 8.077771663665771 GiB, four trajectories/eight generated tokens; no stage-level GPU breakdown.
- **Selection/causality:** four deliberate geography probes, two dependent pairs, prior corpus overlap. City-to-continent association could bypass a necessary country step. No necessity, intervention, broad-generalization, or research-goal-completion claim follows.
- This is same-family semantic annotation, not independent-family validation or goal signoff.

**Signed: PI/OpenAI**