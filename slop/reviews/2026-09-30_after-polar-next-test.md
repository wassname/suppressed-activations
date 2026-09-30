## Inherited decisions
2642’s polar candidate failed: Q1/8 versus original J4/8 and plain275/8. Numerical verification passed; retire Q without spectral/layer/window rescue or alternate-winner promotion. Both goals remain open. Reserved v5 stays unrun.

## Diagnosis
Return to causal editing rather than another readout-score change. Country swaps have stronger reported reference results, but on different models/assays—not evidence this test will succeed.

The reference distinguishes pair-coordinate exchange, sparse decomposition, and clean-pass clamping. Our next test uses **raw pair-coordinate exchange only**, explicitly not an exact reproduction.

## Recommendation: supervisor-approved contract

**One job:** default local queue;300-second TERM deadline plus15-second kill grace. Two properties, five conditions each, maximum32 generated tokens per condition: **320 total**, plus two post-condition clean-target prefills. No other test selected.

Exact source strings, without demonstration or trailing space:

```text
'Fact: The capital of the country shaped like a boot is'
'Fact: The currency used in the country shaped like a boot is'
```

Expected source answers: Rome, euro. Desired intervention answers: Tokyo, yen.

Post-condition target diagnostics replace `shaped like a boot` with `known as the Land of the Rising Sun`. Their states/logits never control editing.

**Primary algorithm:** freeze concept token strings `' Italy'`, `' Japan'`. With pinned checkpoint \(J_{15}\), unembedding rows \(W_s,W_t\), and actual final-norm gain \(g=1+\mathrm{norm.weight}\),

\[
V=\bigl([W_s;W_t]\operatorname{diag}(g)J_{15}\bigr)^\top,\quad
c=V^\dagger h,\quad h'=h+V(Sc-c),
\]

where \(S\) exchanges the two coordinates. No column normalization, midpoint, fitted dose, or raw-inner-product exchange.

Apply at block15/output residual16, **final prompt position only**, then every cached decode position; \(\alpha=1\). Block23 observation is read-only and never feeds the editor.

**Five fixed conditions per property:**
1. Base.
2. Raw J-coordinate exchange—sole primary candidate.
3. Unit-column J-coordinate exchange.
4. Raw plain-column exchange, omitting \(J_{15}\).
5. Seed0 random-direction control, scaled to the primary update norm computed from that control’s **own current state**.

Only prefill random/candidate norm equivalence is expected; later trajectories and doses differ.

**Preflight:** freeze bare answer strings `' Rome'`, `' Tokyo'`, `' euro'`, `' yen'`. Assert single-token encodings for all six frozen strings; abort rather than substitute spellings. Require two independent columns for each exchange basis using a recorded standard SVD rank tolerance. Save bases/pseudoinverses and verify coordinate exchange before and after casting.

## Criterion and evidence
Retain both cases regardless of correctness. The boot-currency prompt **with trailing space previously produced “100% gold”**; this exact no-space form is untested. A wrong Base makes the assay invalid—not grounds to replace the prompt/property.

Promising requires correct Base initial answers and the **same primary rule** producing coherent Tokyo and yen answers, with greater target-directed bare-answer log-odds movement than random on both. Report bare-answer probabilities separately: an initial article can make first-token metrics nondiagnostic.

Save exact continuations, top10 distributions, local coordinates/update norms, coverage, and prefill/final-decode readouts. Explicit retained-Italy assertions or malformed text fail coherence. Repeating the unchanged clue in an NLI hypothesis alone does not; otherwise identity may remain inconclusive.

No alternate control becomes the winner. Success supports further frozen testing—not dog→spider success, hidden-readout generalisation, or goal completion.

## Risks / need from main agent
Raw-coordinate scaling may distort activations; one random direction gives weak specificity evidence. Target prefills cannot establish continuation coherence. Scope is settled; no implementation handoff supplied here.

— **PI/OpenAI**