---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 8968
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_newconst_kimi.trace.jsonl
generated: 2026-09-09T12:54:32.491056+00:00
---

# bounded completion

## First call reasoning

We need need craft answer. Need propose distinct mechanisms implementation error/objective mismatch/unintended dynamic, predictions cheapest checks. Then one new continuous steering construction not shared_replace layer rerun, no layer. Need compare equations/projector alignment/donor-history.

We need infer candidate novel: local additive fixed delta with source rejection? Need persistence ant and dog. Could use bounded/norm-gated local additive delta, adaptive C / per-token blend based on alignment to preserve dog while ant persists. But must avoid shared_replace. Maybe "clipped additive steering": h' = h + C * min(1, radius / ||h||?) Δ? Need scientifically principled and distinguish dog/ant. Existing local fixed delta adds same Δ every decode; ant contradiction due interference, dog succeeds. Shared replace removes live source span and flips dog. New construction could additive with source nulling? But shared replace forbidden. Could do "residual compensation by target-anchor rejection": Δ_eff = projection of donor-source contrast onto complement of live source? That's still subtraction-like perhaps not same shared_replace but implementation via projector, effectively. Avoid frozen/sync.

No layer changes. L20 common. Donor-history maybe donor-history diagnostics. Candidate continuous steering, C=0 family, batch compatible, tiny CPU.

Potential candidate: "norm-preserving additive steering" with per-token norm matching and angular cap. h' = h + C α(h) Δ, α selected to stop once donor evidence threshold achieved. But scalar gate learned from prefill? To preserve dog but ant persistence, use bidirectional saturating injection based on target classifier margin. Yet classifier introduces objective. Could be "contrastive velocity steering": add Δ only to residual incremental drift, not every token. `h' = h + C β_t Δ` with β_t decays or saturates. Existing adds fixed every decode leading ant loop, dog robust. To make ant persist, maybe need transient early strong then release, while dog needs avoid oversteer. But dog under shared replace flips due source removal, additive fixed succeeds. Decayed additive likely dog succeeds, ant perhaps initial ant then revert (like sync ant). Need persistence require sustained support but bounded to avoid loop. Could use harmonic/gated amplitude based on target evidence.

Maybe "rank split": donor direction has persistent component stable across donor histories vs prompt transient. Use donor-history to estimate invariant direction Δ_inf and apply additively; unlike frozen replace. Candidate uses donor-history (currently absent from local) but only to derive a stabilized additive direction. For each decode, donor conditioned on source history, compute current donor-source mean? This is sync but no source span replacement. E.g. `h' = h + C * P (μ_donor(history_t) - μ_source(history_t))`, perhaps dynamic additive contrast. That's genuinely new relative fixed_delta and shared_replace. But could be huge live source/donor delta and dog maybe flips? Additive should keep dog; dynamic alignment may stabilize ant. It uses donor history and projector/alignment. Need equation.

Could use "whitened/bounded dynamic additive contrast":
`Δ_t = P( h_D,t - h_S,t )`; scale to fixed norm τ, then add `C Δ_t`. This is dynamic contrastive additive, not replacing live span. At t prefill maybe existing template contrast; decode donor forward with source-selected tokens (sync history), source hidden current h. No subtraction operation, just vector difference. C=0 identity. Continuous. Donor-history axis isolated from history-conditioned replacement? It changes fixed→dynamic while preserving add. This is one-axis from local fixed? Also projector same L20. Could answer likely.

But compare explicit equations, projector alignment, donor-history. Candidate: synchronized **additive contrast** at L20:
source hidden h_t and donor hidden d_t (same generated prefix, donor prompt separate; source uses its source prompt + generated tokens). `v_t = U U^T(d_t - h_t)`? If h is current source hidden and d donor hidden. `Δ_t = τ v/||v||`; `h'_t = h_t + C Δ_t`. This explicitly does not subtract component h. However because Δ includes `-P h`, geometrically includes negative source component. Yet operation isn't replacement; additive vector happens to depend on live h. Could be viewed as subtract-and-add if coefficient 1, but scaling to template norm and C. At C? h + C τ (Pd-Ph)/norm. At C ~ norm/τ it becomes replacement. Need avoid. If τ = norm of template mean difference ~? First applied local 23.61 prefill, sync L20 8.63? Candidate first decode maybe. C defaults common perhaps C=1/2. It's replacement only if scaling unity in raw component. Norm matching prevents exact replacement and preserves nonorthogonal? Yet still a live difference.

Alternative use donor-history to update Δ but not source current state: `v_t = P(d_t - μ_source_prompt)`; source anchor frozen, donor tracks history. That's donor-history-conditioned additive, avoids live source subtraction. Source prompt anchor fixed. This better: local Δ is donor-template minus spider template. Candidate Δ_t = P(d_t - μ_spider_template), norm matched. Donor evolves along generated source history; source span isn't subtracted. It uses donor history, additive. Dog prior may preserve; ant donor sees contradictory generated text and target signal may decay though.

Need ant persistence: perhaps donor history should condition donor on source-selected tokens. If source says Wait incorrect, donor may shift back. Could instead donor history maintain donor-selected tokens, while source generates? A parallel donor history after initial donor forced first token? Existing sync donor prompt + source-selected tokens, which contaminates donor when source contradicts. For persistence, donor should use donor-consistent history (teacher-forced canonical target answer) not source history. Yet then stale/frozen? Candidate could use "ratcheted target anchor": donor state refreshed only on source tokens whose target classifier/logit evidence increases; otherwise retain previous donor anchor. Then applied Δ doesn't collapse when generation resists. This is novel and aimed persistence. But complex and perhaps dynamic gate.

Maybe donor-history via EMA anchor: `a_t = (1-ρ)a_{t-1}+ρ d_t`, donor d_t conditioned on source-selected tokens; then additive steering `h'_t=h_t+CτP(a_t-μ_src)/norm`. This smooths target signal and avoids abrupt loop; dog maybe preserved due additive. But no strong reason ant persistence.

Could define "dual-anchor additive": combine stable template delta Δ0 and live donor-history delta Δt, with geodesic / orthogonalization and cap. `h'=h+C[λΔ0+(1-λ)τ P(d_t-μ_src)/...]`. This is new construction and continuous. C=0 identity. But tuning λ violates common defaults? Could fix λ .5. Candidate family. Yet candidate should be one.

Maybe exploit observed asymmetric animal behavior: dog coherent under local add; ant loops because same Δ every token likely overwrites syntax, and replace loses dog because source span subtraction removes needed common/web context? A "prefix-only persistence window" perhaps stronger first N tokens then decayed. Continuous steering can have time-varying coefficient. Dog likely maintain; ant maybe initial stable if strong early. But 895 transient indicates release restores spider. To persist ant, need maintain direction throughout; local fixed does persist token 蚂蚁 then wait loop. Need balanced amplitude schedule perhaps strong early then lower. Not compelling.

Could steer in *residual delta from previous token* rather than absolute h: velocity steering. Add only component of Δ orthogonal to current source direction? `v= PΔ - projection onto h`; preserves source magnitude and semantic content, rotates toward target. Norm-preserving rotation:
`h' = cos(Cθ) h + sin(Cθ) ||h|| Δ/||Δ||` perhaps continuous interpolation from h to normalized Δ. But unlike replace, only within 2D span and preserves norm. Could cause dog flip. Dog local add persistence suggests preserving source plus target. Maybe cap so target never dominates source: `h'=h+CΔ` with per-step clipping ensuring cosine similarity to original h stays >= floor. Local already maybe. Need ant persistence versus dog, not universal.

Could use token-specific only? Source strings unchanged, apply decode positions. Candidate maybe "semantic feature addition with KL trust region": adaptive per-token coefficient as max C subject to next-token KL(Base || steered) ≤ ε. This preserves fluency/dog, while repeated target feature maybe ant. But if KL cap too low, ant may revert. Could choose ε fixed. It is continuous and novel. Yet implementation requires base next logits each hook step and binary search, expensive but doable. Falsifiable.

Question likely expects brainstorm and candidate design based on results. We can be bold.

Need no winner. Explicitly not choose. Mention diagnostics prefill-only labeled only. Mechanisms:
1 implementation error: decode hook applies fixed Δ at active token with stale scaling / positions? In code says same Δ. Could be C normalization mismatch causing repeated linear accumulation? Prediction perturb norm identical every decode and ant pathology emerges when > threshold. Check instrument h' norms/logits at decode; tiny CPU run.
2 objective mismatch: template mean-difference includes response style/entity and fails persistence objective; maximizing donor coordinate doesn't equal maintaining answer under generated contradictory context. Prediction Δ has components unrelated / first-token vs paragraph metric. Check decompose Δ into U components, ablate ranks? Is that layer/projector rerun? As check can inspect existing vectors, no run. Cheap check cosine and logits.
3 unintended dynamic: additive Δ creates positive feedback / attractor: ant token raises contradiction, model issues Wait; repeated same vector suppresses correction. Prediction output loops correlate with cumulative dose; delayed onset / periodicity and temporarily stopping after first token would break loop. Check existing continuation plus activation tracing; or no new GPU maybe analyze saved logits if available. Cheapest: parse 894 tokens and compare Δ decode positions unavailable; CPU smoke.

Other mechanisms maybe projector misalignment: dog prior causes enough, ant direction includes taxonomic conflict; replace removes spider features. But categorize distinct.

Candidate: dynamic **donor-anchored additive steering with target-state EMA and trust cap**? Need be "genuinely new" and aimed ant persistence while keeping dog. Let's formulate precise.

Maybe call "EMA-anchored additive contrast (EAAC)":
- Keep L20, same U from local c003.
- Build source anchor `s0 = U U^T μ_spider` (not live subtraction).
- Maintain donor anchor `a_t`. Donor forward is conditioned on donor prompt + target-consistent synthetic continuation? Hmm.
- We can derive donor history independently: at each decode donor model receives donor prompt plus *source-selected tokens*. This is same sync donor-history. `d_t = P h_D(...)`.
- EMA: `a_t=(1-ρ)a_{t-1}+ρd_t`, `a_0` donor template / donor prompt last.
- Direction `v_t = P(a_t - s0)`.
- Norm-match to τ = ||μ_donor - μ_spider|| and cap angle/cumulative? `Δ_t=τ v_t/||v_t||`.
- Apply additively `h'_t = h_t + C Δ_t`.
No replace. Continuous C. C=0 exact identity. Uses donor history. It compares fixed donor anchor to evolving target evidence. But if source says Wait, donor conditioned on that may drift spider; EMA resists. Is that enough? Could also "ratchet": update EMA only when donor coordinate evidence remains aligned: if cos(v_t,v_0)>0. This preserves target. But arbitrary classifier-free alignment. Candidate designed for persistence: target-anchor ratchet.
`a_t = a_{t-1}` if `cos(P(d_t-s0), Δ0) < 0`, else EMA update. Thus donor history can refine magnitude/direction but cannot cross source anchor/flip back. This is a genuinely novel continuously steered construction. The direction remains nonnegative target evidence. Does dog survive? Additive no source removal; likely. Ant persists because anchor doesn't follow correction back toward spider. But if source begins Wait immediately, initial a0 remains Δ0, so equivalent local fixed—still loop. EMA maybe not solve ant. Need alter direction perhaps use a more semantic persistent direction derived across donor histories, filtering lexical first token and retaining target property.

What causes ant loop? Fixed Δ too strong at every token. Maybe a norm floor/cap doesn't help. We need candidate aimed. Could use "target evidence deficit feedback controller" to adjust C_t: monitor target-vs-source logit margin for next token and add only enough to maintain ant. Dog might require low due prior; ant high. But without eval reserved? It's implementation mechanism. Continuous. `C_t = clip(k(m* - m_t),0,Cmax)` where m_t = logit target - logit source or donor classifier margin. This adaptive closed-loop steering can preserve dog with lower effective dose and sustain ant. But after ant token, subsequent paragraph target tokens are many, not one. Need target state classifier from hidden states, not reserved strings. Could train? No new training ideally. Use donor/source anchor projection margin:
`m_t = <P h_t - s0, Δ0>/τ`.
Steering controller: `C_t = clip(k(m_goal - m_t),0,Cmax)`, h'=h+C_t Δ0. This is closed-loop additive. If h already dog-like, dose shrinks, preserving dog; if ant evidence decays or spider rebounds, dose rises. But if ant condition causes contradiction, m maybe target enough after first token then controller shuts off and spider returns. Set goal maybe high and maintain floor. Could target margin goal from donor prefill `m_goal = <P μ_donor-s0, Δ0>/τ`, then keeps donor-level coordinate. This effectively integral/proportional control to donor coordinate, but only additive, not replacing. It could still overshoot? Formula:
`e_t = m_D - <P h_t-s0,u>`
`c_t = clip(C e_t, 0, Cmax)`
`h'=h + c_t τ u`
Equivalent proportional control. Since adding positive u increases coordinate next token but not instant? At same token output h' coordinate. Controller computed pre-edit. Could also anti-windup. Dog: if h already close dog coordinate, c low; ant: if h spiderlike, high. This seems genuinely aimed and no shared replace. It uses projector/alignment, no donor history perhaps. But prompt asks compare donor-history, not necessarily candidate uses all. New construction "closed-loop additive coordinate servo." C=0 identity. Common C as gain. Does this accidentally become replace? A controller seeks coordinate but doesn't subtract entire source span; only scalar projection along u. It leaves orthogonal source features intact. This could preserve dog context while ant persists. It is a strong candidate.

Need ensure ant persistence not just naming token. m_goal derived from donor prompt hidden state. At every decode, maintains coordinate along target contrast. Dog currently local additive succeeds; closed loop reduces unnecessary dosage, likely retains. Ant local fixed overdoes and loops; adaptive dose may avoid oversteering yet restore after drift. Nice.

Equation:
- U from same L20 attenuation SVD, rank 4.
- `u = Δ0/||Δ0||`, τ=||Δ0||.
- source coordinate `s_t = u^T U U^T h_t` maybe h already full; donor goal `s_D = u^T U U^T μ_donor`; source base `s_S = u^T U U^T μ_spider`.
- normalized error `e_t = clip((s_D - s_t)/(s_D-s_S), 0, 1)`.
- `c_t = C e_t` (or Cmax C). Then `h'_t = h_t + c_t τ u`.
No subtraction. If h_t reaches donor coordinate c=0. If spider baseline c=C. If exceeds target, no negative correction to avoid replacement and preserve dog. Could include lower deadband. C defaults C=0 and C=2? Candidate common dog+ant defaults: use C=0 and C=2 where C is max dose. But at C=2 could max twice template delta, local fixed C2 perhaps? Existing local runs maybe C? 893/894 probably C? Need maybe C=2? Not explicitly. They say first applied etc C2 for 910. Candidate C=0/C=2. At ant h may after Δ coordinate exceed target, c turns off next token. It creates pulse train; perhaps coherent.

Would this stop Wait loop? The loop arises after target token due oversteering syntax. Controller deactivates when target coordinate sufficient, allowing language model to produce paragraph. If target coordinate drops, reactivates. Dog: prior target coordinate already high, little/no dose, so no flip. This directly addresses objective mismatch and dynamic. Good.

Potential issue coordinate is rank-4, not single u. Better goal vector in U and saturate componentwise:
`x_t=U^T h_t`, `x_S=U^T μ_spider`, `x_D=U^T μ_donor`.
`e_t = clip((x_D-x_t)/(x_D-x_S),0,1)` elementwise, perhaps weights. Then `Δ_t=U (e_t ⊙ (x_D-x_S))`, scale norm τ. But if direction differs. Single contrast axis easiest.

Could use rank-4 coordinate servo:
`e_j=clip((x_D,j-x_t,j)/(x_D,j-x_S,j+eps),0,1)`
`g=U diag(w_j e_j)(x_D-x_S)`, normalized to τ. Apply. It preserves direction subspace and adaptive components. But denominator signs. Simpler scalar.

We must compare explicit edit equations, projector/alignment, donor-history in candidate and prior.

Cheapest checks:
- implementation error mechanism: Verify hook actually applies at decode and C scaling by instrumenting existing 894? Saved record lacks applied norms. Tiny CPU smoke real path mandatory candidate. For mechanism check can load code and 1-token CPU with counter, assert Δ constant, position ids.
- objective mismatch: compute cosine of Δ with donor continuation residual differences? Use saved activations/templates no GPU. Perhaps inspect logit effects of Δ on vocabulary: top boosted tokens are ant vs function words / Wait. Cheap CPU/GPU? model on CPU. Falsifiable prediction: Δ boosts `蚂蚁` but also discourse corrections and lowers content words. Check unembedding `W_U Δ` (if residual at L20 not final maybe use final head not exact), cheap.
- unintended dynamic: Predict 894's failure begins after self-generated token and applied additive causes recurrent drift; check hidden state cosine to Δ across 894 saved? no decode saved. Cheapest rerun 894 with tracing only? But constraints no candidate rerun? It's mechanism investigation, can run existing config with instrumentation maybe. Cheapest is reproduce 894 on tiny CPU real path and log every decode h norm/logit;
## Final answer call answer

# Independent Scientific Brainstorm

## Three Mechanisms for 893→910 Dog Loss

### Mechanism A: Implementation Error — Stale/Drifting Target Coordinates

**Hypothesis:** The `shared_replace` target `d` is computed from donor prompt residuals, but the projection `U Uᵀ d` does not actually align with where the donor direction *points* in the live decode. In frozen mode (911), `d` is stale by construction. In sync mode (910), the donor history shares tokens with the source but the residual at the edit position may diverge as decode progresses, causing the replace to pull toward an increasingly wrong attractor.

**Falsifiable prediction:** If stale target coordinates are the cause, then applied_norm should decay monotonically in 910 (sync, tracking target) but stay large and constant in 911 (frozen, stale target). Observed: 910 dog last applied = 1.47, 911 dog last applied = 2.81 — both decay but 911 decays less. This is *weakly consistent* but does not isolate the mechanism.

**Cheapest check:** Extract `U Uᵀ d` (the projected target vector) at each decode step for 910 dog C=2, and compute cosine similarity between `U Uᵀ d` and the actual direction from spider→dog in activation space (e.g., the local-c003 Δ). If cosine similarity decays across decode, the target is drifting.

### Mechanism B: Objective Mismatch — Subtraction Removes What Addition Preserves

**Hypothesis:** Local-c003 `fixed_delta` adds Δ without removing anything. The model's own spider representation remains in the residual, and the added dog component must compete with it. For dog (high prior, coherent paragraph), the dog direction wins. For ant (low prior, contradictory), the spider representation reasserts. `shared_replace` removes the live spider span, which *should* help, but the removal may also destroy contextual scaffolding (residual stream structure) that the model needs to produce *any* coherent animal paragraph — including dog.

**Falsifiable prediction:** If subtraction destroys scaffolding, then `shared_replace` at C=2 should produce *shorter, less coherent* output for both animals compared to `fixed_delta` at the same layer. 910 dog produced a spider paraphrase (coherent but wrong animal). 911 dog produced a mash (less coherent). 893 dog produced a coherent dog paragraph. The pattern is consistent with scaffolding destruction.

**Cheapest check:** Run 910 construction (sync L20 C=2) but modify `replace` to `h' = h + C·(U Uᵀ d − α·U Uᵀ h)` with α=0.5 (partial subtraction). If partial subtraction preserves dog better than full subtraction, scaffolding destruction is implicated.

### Mechanism C: Unintended Dynamic — Replace Creates a Moving Target That the Model Corrects Against

**Hypothesis:** In sync mode, the donor history follows the source-selected tokens. As the model generates spider tokens (because the edit pushed it there), the donor history accumulates spider tokens, so the donor residual itself becomes more spider-like, weakening the dog signal in subsequent replace steps. This is a self-undermining feedback loop: the edit causes the model to generate spider tokens, which causes the donor to become more spider-like, which weakens future edits.

**Falsifiable prediction:** If this feedback loop exists, then in 910 dog, the applied_norm should decay *faster* than in 911 (frozen), because frozen at least maintains a constant (stale but dog-consistent) target. Observed: 910 last applied = 1.47, 911 last applied = 2.81. Consistent.

**Cheapest check:** In 910 sync, log the cosine similarity between `U Uᵀ d` (donor component) and `U Uᵀ (μ_dog − μ_spider)` (the intended direction) at each decode step. If it decays with decode step, the feedback loop is confirmed.

---

## One New Continuously Steered Construction: **Dual-Gate Interpolated Replace**

**Name:** `gated_replace` — continuous steering, L20, C as a gate on subtraction only.

**Motivation:** 893 shows addition-without-subtraction preserves dog coherence. 910/911 show full subtraction loses dog. The failure is likely that subtraction removes spider-span components that are *load-bearing for coherent animal description* (shared features like "four legs," "domesticated," "small"). The fix: separate the addition and subtraction coefficients, and tie subtraction to a *gate* that is active only when the live residual is *already* closer to spider than to donor.

**Edit equation:**

```
h' = h + C_add · Δ_fixed + C_sub · g(h) · (U Uᵀ d − U Uᵀ h)
```

Where:
- `Δ_fixed = U Uᵀ (μ_donor − μ_spider)` scaled to full norm (same as local-c003)
- `C_add` = the steering coefficient (continuous, e.g., 0 to 2)
- `C_sub` = a separate subtraction coefficient (continuous, e.g., 0 to 1)
- `g(h) = σ(β · (cos(h, μ_spider) − cos(h, μ_donor)))` — a sigmoid gate that is ≈1 when the live hidden state is closer to spider (subtraction active) and ≈0 when already closer to donor (subtraction inactive)
- `β` = temperature (e.g., 10)
- `d` = frozen donor-prompt residual (same as 911; not synced, to avoid the feedback loop from Mechanism C)

**Why this is genuinely new:**
- It is not `fixed_delta` (which has no subtraction term at all)
- It is not `shared_replace` (which always subtracts with C_sub = C_add)
- It is not a layer change (stays at L20)
- It introduces a *state-dependent gate* on subtraction, which none of the existing constructions have
- C=0 in this family means C_add = 0 and C_sub = 0, which is identity (same as other constructions)

**Sweep plan (one `--batch-spec`):**
- Grid: C_add ∈ {0, 1, 2}, C_sub ∈ {0, 0.5, 1}
- 9 cells × 2 animals (dog, ant) = 18 runs
- Naming questions only (same strings as 893/894)
- C_add=0, C_sub=0 is the identity baseline in the same family
- C_add=2, C_sub=0 is equivalent to local-c003 (893/894 reproduction check)
- C_add=2, C_sub=1 is equivalent to 911 (frozen replace reproduction check)
- The interesting cells are C_add=2, C_sub=0.5 and C_add=1, C_sub=0.5

**What each outcome would mean:**

| Outcome | Interpretation |
|---|---|
| C_add=2, C_sub=0.5 keeps dog coherent AND ant persistent | Partial gated subtraction is the correct mechanism |
| C_add=2, C_sub=0.5 keeps dog but ant still loops | Ant failure is not about subtraction magnitude; need donor-history or direction quality |
| C_add=2, C_sub=0.5 loses dog like C_sub=1 | Any subtraction at all destroys scaffolding; gate needs to be stricter |
| All C_sub>0 cells lose dog | 893's add-only approach is load-bearing; pursue direction quality instead |

**Implementation notes:**
- Reuses existing attenuation SVD projector (L20)
- Reuses existing frozen donor-prompt residual extraction
- New code: the gate function `g(h)` and the split C_add/C_sub in the hook
- Tiny CPU smoke: verify gate output ∈ [0,1] and identity at C=0
- Isolated runner, full continuations
- `--batch-spec` compatible

**Explicitly not:**
- Not another layer (L20 throughout)
- Not `shared_replace` frozen/sync (those are 908/895/910/911)
- Not prefill-only
- Not a winner declaration — this is one construction to test, pending results

---

## Comparison of Edit Equations, Projector/Alignment, and Donor-History

| Axis | `fixed_delta` (893) | `shared_replace` frozen (911) | `shared_replace` sync (910) | `gated_replace` (proposed) |
|---|---|---|---|---|
| **Addition** | C · Δ (fixed) | None (replace only) | None (replace only) | C_add · Δ (fixed) |
| **Subtraction** | None | C · U Uᵀ h | C · U Uᵀ h | C_sub · g(h) · U Uᵀ h |
| **Target** | Template Δ | Frozen donor prompt | Live donor (synced) | Frozen donor prompt |
| **Projector** | Attenuation SVD L20 | Attenuation SVD L20 | Attenuation SVD L20 | Attenuation SVD L20 |
| **Donor-history** | None | None | Follows source tokens | None |
| **State-dependent** | No | No | No | Yes (gate g(h)) |
| **C=0 identity** | Yes | Yes | Yes | Yes |

The key gap in existing constructions: none of them *conditionally* subtract. `fixed_delta` never subtracts. `shared_replace` always subtracts. `gated_replace` subtracts only when the live state warrants it, which may preserve the scaffolding that 893 relies on while still removing spider-specific content when it is dominant.

-- PI/Grok

## Completion

- outcome: `completed_after_follow_up`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_newconst_kimi.trace.jsonl`
