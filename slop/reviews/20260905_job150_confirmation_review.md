# Job 150 fresh confirmation audit

## Review

- **Correct:** The saved scientific artifact is usable despite the final rendering crash.
- **Finding: P1:** The preregistered animal-specificity criterion failed for both targets.
- **Finding: P1:** The evidence supports first-token answer/completion-state transfer, not animal semantics.
- **Finding: P2:** The position control is directionally positive but confounded by substantially smaller realized perturbations.
- **Finding: P2:** `log.md` is stale and must not be used as the result report.
- **Merge verdict:** **BLOCK** for an animal-semantics claim and for merging the crashing renderer unchanged. **OK with notes** for retaining `result.json` as a usable negative/mechanistic-control result.

## 1. Artifact integrity after the crash

**Usable: yes.** The failure happened after all scientific measurements and generations had completed and after both structured artifacts were written:

- All generated rows were asserted to contain 64 tokens before serialization (`scripts/confirm_causal_demo.py:522`).
- Metadata was changed to `"status": "complete"` before constructing the artifact (`scripts/confirm_causal_demo.py:528-547`).
- `metadata.json` and `result.json` were written before `render_log(...)` was invoked (`scripts/confirm_causal_demo.py:549-552`).
- The crash was solely in the reporting expression  
  > `sources | targets.items()`  
  at `scripts/confirm_causal_demo.py:302`, producing `TypeError: unhashable type: 'dict'` (`slop/audits/job_150_full.log:7-17`). The intended expression was presumably `(sources | targets).items()`.
- Saved metadata identifies the requested code revision as `"v0.1.1-59-g723265a"` and the frozen model revision (`out/2026-09-05_211609_causal-confirmation/metadata.json:2,8`). It records L26, final-prompt-token, rank 8, C=4, 256 controls (`metadata.json:25-29`) and says `"status": "complete"` with an end time and 133.59-second scientific runtime (`metadata.json:36-38`).
- The complete JSON reaches both seed 255 rows—Ant starts at seed 0 on `result.json:2444` and reaches seed 255 at `result.json:41459`; Dog starts at seed 0 on `result.json:41614` and reaches seed 255 at `result.json:80629`—then contains summaries and every generation through the final closing brace.
- Pueue nevertheless correctly reports process exit failure (`slop/audits/job_150_status.json:97-103`) because rendering raised after those writes.

The only unusable artifact is `log.md`, which remains:

> `Status: running`

at `out/2026-09-05_211609_causal-confirmation/log.md:3`. It is stale presentation output, not evidence that computation was incomplete.

## 2. Prediction-by-prediction outcome

The frozen predictions are at `slop/research/20260905_l26c4_confirmation_predictions.md:19-23`.

| Prediction | Outcome | Evidence |
|---|---|---|
| Ant and Dog exceed at least 95% of 256 matched random rotations | **FAIL, both** | Ant: 238/256 below, percentile **0.9296875**; Dog: 235/256 below, percentile **0.91796875** (`result.json:80783-80792`). Thus 18 Ant controls and 21 Dog controls tied or exceeded the structured effect. |
| Answer-only components reproduce much of the animal digit movement | **PASS strongly** | Ant C4 has Δlog-odds(6/8) **3.75** (`result.json:989`), while three-plus-three gives **8.375** (`result.json:2269`). Dog C4 gives **3.25** (`result.json:1789`), exactly matched by two-plus-two at **3.25** (`result.json:2429`). |
| Final-token intervention is stronger than penultimate | **PASS operationally, qualified** | Ant: **3.75 versus 0.0** (`result.json:989,1149`). Dog: **3.25 versus 0.125** (`result.json:1789,1949`). However, the position comparison is not distance matched; see confounds below. |
| Byte prompt keeps top answer 8 | **PASS** | Byte-Ant leaves p(8)=**0.965277**, p(6)=**0.003072** (`result.json:1289-1290`); Byte-Dog leaves p(8)=**0.835522**, p(4)=**0.003869** (`result.json:2089-2090`). Both generated continuations begin with 8 (`result.json:81208-81346`). |
| Targeted continuation matches forced-first-token continuation after token one | **PASS exactly for both targeted cases** | Spider-Ant and forced-6 have identical 64-token arrays/text (`result.json:80865-80932`, `81624-81691`); Spider-Dog and forced-4 likewise match (`result.json:80934-81001`, `81693-81760`). Generation was greedy, not sampled: `do_sample=False` (`scripts/confirm_causal_demo.py:204-213`). |

## 3. Best explanation

### Primary behavioral explanation: first-token forcing

The animal interventions changed Spider’s first-token distribution:

- Ant: p(6)=**0.487144**, p(8)=**0.379388**, log-odds(6/8)=**0.25**, Δ=**3.75** (`result.json:969-989`).
- Dog: p(4)=**0.490091**, p(8)=**0.297255**, log-odds(4/8)=**0.5**, Δ=**3.25** (`result.json:1769-1789`).

Once that first token was supplied without an intervention, the resulting greedy continuation was exactly reproduced. Therefore the apparent 64-token behavior needs no persistent transferred animal fact: the model simply conditions normally on the changed first digit.

This is meaningful rather than purely guaranteed by implementation. The hook stops being reapplied during one-token decode (`scripts/confirm_causal_demo.py:180-201`), but altered prefill state can still persist through cached context. Indeed Byte-Dog retains first token 8 yet changes later text from “16” to “10” (`result.json:81208,81346`). Exact Spider target/forced equality is therefore an empirical property of these targeted runs.

### Best representational explanation: generic answer/completion-state transfer

Animal semantics are not supported because the preregistration explicitly required animal effects to be stronger than answer-only controls (`slop/research/20260905_l26c4_confirmation_predictions.md:25`). Instead:

- Three-plus-three is more than twice Ant’s log-odds movement: **8.375 versus 3.75**.
- Two-plus-two exactly matches Dog’s movement: **3.25 versus 3.25**.
- The arithmetic interventions also produce the same forced-6/forced-4 Spider continuations (`result.json:81415,81484`).

Thus the most economical interpretation is transfer of an answer/completion state encoding “6” or “4,” whose visible consequence is principally first-token forcing.

### Random-large-perturbation remains an unresolved null

Random perturbation is not the best positive explanation, because answer-only directions reproduce the intended digits systematically. But it cannot be rejected for the animal interventions:

- Both animal effects miss the fixed 95% gate.
- Random rotations themselves made the expected digit top-ranked in **19/256 Ant controls (7.42%)** and **27/256 Dog controls (10.55%)** (`result.json:80785-80792`).
- The displayed Dog-distance seed-0 random continuation is exactly the same forced-4 continuation as the structured Dog result (`result.json:81072-81139`).

Therefore the ranking is:

1. **First-token forcing** for the observed continuation behavior.
2. **Generic answer/completion-state transfer** for directional content.
3. **Random large perturbation** as a still-live null for animal effects.
4. **Animal semantics**, unsupported.

## 4. Quantitative evidence and strongest confounds

### Main quantities

- Clean Spider starts at p(8)=**0.882568**, p(6)=**0.026651**, p(4)=**0.056421** (`result.json:371-529`).
- Ant C4 moves log-odds(6/8) from **−3.5 to +0.25**, Δ **3.75** (`result.json:652,972,989`).
- Dog C4 moves log-odds(4/8) from **−2.75 to +0.5**, Δ **3.25** (`result.json:1452,1772,1789`).
- At C1, effects are only **0.375** for Ant and **0.5** for Dog (`result.json:829,1629`), showing that the first-token flips depend on extrapolated C4.
- Arithmetic controls: three-plus-three reaches p(6)=**0.945722**, p(8)=**0.007221** (`result.json:2249-2250`); two-plus-two reaches p(4)=**0.385500**, p(8)=**0.233818** (`result.json:2409-2410`).

### Strongest confounds

1. **Very large extrapolated intervention.** Applied perturbations are **17.224 / 25.363 = 0.679** of residual norm for Ant and **18.270 / 25.363 = 0.720** for Dog (`result.json:996-997,1796-1797`). The preregistration itself warns that “C=4 is an extrapolation, not an exact replacement” (`confirmation_predictions.md:25`).

2. **Random null not cleared.** The empirical percentiles are only 92.97% and 91.80%, below the fixed 95% requirement. This directly blocks the planned specificity claim.

3. **Answer controls were not given their own matched-random distributions.** They strongly favor answer-state transfer, but the script computes 256-way random summaries only for Ant and Dog (`scripts/confirm_causal_demo.py:426-466`). Consequently, arithmetic-control superiority is mechanistically suggestive rather than itself randomness-controlled.

4. **Penultimate-site comparison changes realized dose.** Ant penultimate distance is **12.091**, ratio **0.384**, versus final **17.224**, ratio **0.679** (`result.json:1156-1157,996-997`). Dog is **12.457/0.396** versus **18.270/0.720** (`result.json:1956-1957,1796-1797`). The observed reduction therefore cannot cleanly isolate token position.

5. **Byte control uses different source geometry.** Byte interventions are even larger relative perturbations—**0.989** and **0.978** of residual norm (`result.json:1317,2117`)—and still preserve top token 8. This supports context dependence, but one unrelated prompt does not distinguish semantic gating from differing residual geometry.

6. **Only greedy continuation was tested.** The prediction says “sampled digit,” but implementation uses `do_sample=False` (`scripts/confirm_causal_demo.py:204-213`). Exact continuation equivalence is established only for deterministic greedy decoding.

## 5. Smallest next decision

**Do not publish or label job 150 as confirmation of animal semantics. Mark the frozen candidate as failing its preregistered specificity gate, retain `result.json` as a valid negative/mechanistic result, and do not rerun the expensive experiment merely to repair rendering.**

If the program continues, the smallest discriminating follow-up is to obtain matched-random percentiles for the two arithmetic answer controls, with the position comparison also distance-matched. That directly tests answer-state transfer against the still-live large-random-perturbation explanation without reopening prompt/layer/rank/dose selection.