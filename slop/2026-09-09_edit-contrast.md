# How local-c003, frozen, and synchronized actually edit

From `scripts/demo.py` `intervention_hooks` / `replace`, `scripts/oat_sweep.py`
`generate_synchronized_donor`, and saved `intervention_record` on 893/894/895/908.
Equal first-step perturbation is **not** an equal decode trajectory.

## Four axes

| | local-c003 (893 dog / 894 ant) | frozen L24 (908) | synchronized L24 (895 ant) |
|---|---|---|---|
| **Projector** | attenuation SVD on template peak−output contrast; `persistent_rank` 4. `direction_estimator`: `matched_template_mean_difference`. Template delta **is** applied (`fixed_delta`). | Same attenuation SVD span. `direction_estimator`: `template_attenuation_donor_coordinate_replacement`. Template delta **is not** applied (`edit_measurement`). | Same as frozen. |
| **Source subtraction** | None. `operation=fixed_delta`: `h + C * Δ` with Δ = template mean-difference scaled to full-delta norm (`match_component_norm` True on Δ, not on live h). | Yes. `shared_replace` → `replace`: `h + C * (component(donor_h, U) − component(h, U))`. Live source span is removed. `match_component_norm` False. | Yes. Same `replace` against the **current** donor hidden state. |
| **Donor-history conditioning** | None. Δ is computed once from templates. Same vector every decode (hooks on `generate_with_first_logits`). No `replacement_trace`. | Frozen **donor-prompt** residuals (`target["residuals"]`, last 3 then last 1). `decode_target`: frozen final donor prompt coordinates. Donor tokens never follow the source continuation. | Each step: donor forward on **unchanged donor prompt + source-selected tokens**. `synchronized_history.donor_conditioning` quotes that. Separate KV caches. |
| **Edited positions** | Prefill last 3 (`[40,41,42]` on naming). Decode: `active_positions=1` on the new token. Edit **L20**. | Prefill last 3; decode last 1. Edit **L24**. | Prefill last 3 (`target_position=content_end-1`); decode `target_position=0` on the new donor token. Edit **L24**. |

## Saved per-decode evidence (not first-step only)

895 sync ant L24 `replacement_trace` n=89: applied_norm 31.889 → 3.24 (step 1) → median 1.20 → last 0.62. Sum 184.
908 frozen ant L24 n=128: **same first 31.889**, then 6.00 → median 11.46 → last 11.11. Sum 1550.
908 frozen dog L24: first 34.75 → last 7.65. Sum 1290.

So 908 vs 895 sharing first-step 31.889 only means the **prefill replace** matched. Decode: frozen keeps a large replace toward stale donor-prompt coordinates; sync’s replace shrinks as the two histories share tokens.

893/894 store only prefill `perturbation_norm` (23.61 / 19.76) and `relative_perturbation_by_position` on the three prefill tokens. No per-decode applied_norm for `fixed_delta`.

C=0 frozen (908): applied_norm 0, steered IDs = Base.

## Continuations (judge bodies)

- 893 local L20 dog: persistent donor (`狗` + dog paragraph to EOS).
- 894 local L20 ant: contradictory donor (`蚂蚁` + Wait/loop).
- 895 sync L24 ant: transient donor (`蚂蚁` then restore spider paragraph).
- 908 frozen L24 dog/ant: contradictory donor (name then Wait/incorrect loop to 128).

## One construction-level experiment (not a layer cell)

**Question:** does 894 loop because local-c003 **adds** Δ without removing the live spider span, while 893 dog still wins on prior? Falsify by using the **same L20 attenuation projector as 893/894** but `shared_replace` with **frozen donor-prompt coordinates** (existing `synchronized-attenuation` frozen L20 C0/C2, both animals, naming questions, one `--batch-spec`).

| outcome | reads as |
|---|---|
| dog stays coherent, ant becomes coherent | add-without-subtract was the ant failure |
| dog breaks | 893 depended on add-without-subtract |
| ant still loops / reverts | subtract vs add is not the ant persistence gap |

C=0 is in the same batch. Source unchanged, continuous steering. Do not run property or legs prompts here. Do not treat first-step perturbation equality as a cause.

-- PI/Grok
