---
requested_model: deepseek/deepseek-v4-pro-0813
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 8060
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_deepseek-v4-pro-0813_span_pass1_deepseek.trace.jsonl
generated: 2026-09-09T14:12:22.915238+00:00
---

# bounded completion

## First call reasoning

We need answer as scientific exploration. Need reconstruct method from evidence/pseudocode. Need list distinctions, assumptions, possible failure modes, alternative formulations, experiments that matter. Need separate material directly shows vs inference. State observation would change mind. Uncertainties/missing evidence. Math/pseudocode where clarifies proposed test. Do not pick winner.

We need parse provided evidence. Need reason deeply.

We have pseudocode span_corrected_delta. Construction: U orthonormal projector rank r=4 fitted from templates? Need infer maybe attenuation subspace from prior? We have only pseudocode. Evidence from Qwen3.5-4B. Continuous steering L20 C=2. Prompts legs/property. Results.

Central question: does attenuation subspace encode name/concept pointer WITHOUT attribute bindings, or C=2 reflection overshoot attribute coordinates? Cheap test discriminates.

Need produce organized exploration. Need not assume framing complete. We can include distinctions, assumptions, possible failure modes, alternative formulations, experiments.

Need be careful: "Do not edit code, fabricate results, or pick winner." We can propose tests, not execute. Need separate material directly shows vs inference.

Let's understand setup.

We have model Qwen/Qwen3.5-4B. They fit U rank 4 from templates. Δ = U U^T (μ_target - μ_spider), norm-matched. At each decode step at edited position, span = P h, patched = h + C(Δ - span), C=2. So U-span component reflected about Δ; orthogonal complement unchanged. This is equivalent in U coords P h' = (1-C)P h + C Δ. C=2: P h' = 2Δ - P h. So overshoots relative to target mean if live P h has opposite? Need understand.

Intervention transfers animal identity (name) in every C=2 cell, but not bound attributes. Example legs-dog-C2: first says '2' (wrong digit? Actually prompt "How many legs does animal that spins webs have?" Correct spider 8; dog target 4. They expected maybe dog legs should "4"? But result first='2' answer=None r=0.078. Text says "The animal is a dog... Dogs typically have four legs, but the question asks for the answer first, so I am confirming that the standard number of legs for a dog is four, not two." Weird: first digit '2'? Maybe answer before text, it generated '2' despite text saying dog has four legs. Could be due to prompt interpretation? It says dog "2"? Need note. Let's parse: For legs-dog-C2, output starts "2" then newline "The animal is a dog..." text acknowledges dog typically four legs, but "question asks for answer first ... confirming standard number of legs for a dog is four, not two." This is dissociation: identity transferred to dog, but digit not transferred? Actually first token '2' not '4' or '8'; text says dogs have four legs but output digit '2'. Could be maybe "2" is answer? It says "standard number of legs for a dog is four, not two." So yes digit output incorrect relative to dog. Bound attribute leg count not transferred.

But legs-dog-RAND shows first='4' answer='4' n=56, text kept spider identity: "The animal is known as a spider, and it is domesticated by humans for its ability to spin webs. Spiders are also known for their intelligence and their ability to communicate with their pack. They are also known for their ability to hunt and eat their prey." So random direction moved digit to target correct value 4 while text kept spider identity. This shows digit movement and identity movement separable.

Need answer central: "does attenuation subspace plausibly encode a name/concept pointer WITHOUT attribute bindings, or does C=2 reflection overshoot attribute coordinates? What cheap test discriminates?"

We need reconstruct method, then analyze.

Need list distinctions:

- Identity/name vs bound attributes vs unbound factual associations.
- U-span component vs complement.
- Raw mean difference vs projected norm-matched delta.
- C values: identity C=0; set C=1; reflection C=2.
- Template source/target means from residual streams at layer 20.
- Random direction as control (disruption, not content).
- Continuous steering at every decode step at edited position vs one-shot activation patch.
- Prompt restatement artifact: spin = mentions "spins webs" in row, not identity.
- First token numeric answer vs subsequent text/properties.
- Attribute questions may be Yes/No vs open generation.

Assumptions:
- U rank r=4 meaningful; maybe from PCA/ICA? Need infer. They call attenuation subspace maybe principal components? We don't know. Need state missing evidence: how U was fitted from templates; what rank selected; whether shared across animals; which layer; whether at residual stream after certain block.
- Norm matching to raw mean difference after projection assumes projection doesn't change norm much? Actually they scale to match norm of raw difference. If projected norm is small, scaling up amplifies directions, possibly overshoot/instability. Need compute? Missing r/d ratio; projected fraction depends cos. Could be issue.
- Reflection C=2 assumes linearity and that double distance from live span to delta transfers target semantics. Could overshoot attribute coordinates if U has mixed name and attributes.
- Continuous patch assumes hidden residual can be replaced independently and model is linear in that subspace during decoding.
- Identity vs attributes may be encoded in different subspaces or same coordinate axes with different scaling.
- Random control matched norm; but random_delta norm equals projected delta norm? Actually random_delta scaled to ‖Δ‖, where Δ is projected+norm-matched. So random has same norm but random direction possibly mostly orthogonal? Need check. In pseudocode: random_delta = randn_like(Δ); random_delta = random_delta * ‖Δ‖ / ‖random_delta‖. So random vector same norm as Δ, not necessarily in U-span? Wait Δ = U U^T (raw) then norm-matched. Δ lies in U-span. random_delta is random in full D, norm-matched to ‖Δ‖. Then patched = h + C(random_delta - span). Since random_delta not in U-span, update includes orthogonal component C*random_delta (since span in U-span). That may disrupt more than real because Δ confined to U. But pseudocode comment says same reflection, different delta direction; yes random_delta in full space not projected. Could be a weakness: random control has larger orthogonal component, may disrupt context non-specifically. However evidence says random controls on naming had bigger applied norms and produced garbage; but in this batch they used matched norm? They note "random controls on naming had bigger applied norms (208.5 vs 26.8 real)" maybe from earlier; here maybe random direction norm matched? For legs-dog-RAND it moved digit to 4, so not too disruptive? Need discuss.

Need reconstruct from "Earlier base for context (naming questions, 912, same construction)": Both dog and ant named coherently with no correction loop: dog "狗 (Dog)" + dog paragraph to EOS; ant " Ant" + ant paragraph. C=0 identity held (steered == Base). Random controls on naming had bigger applied norms (208.5 vs 26.8 real) and produced garbage, so random is a conservative disruption check.

Need maybe include norm values 208.5 vs 26.8 real; likely applied norm mismatch? Wait "Random controls on naming had bigger applied norms (208.5 vs 26.8 real)" This suggests in naming random controls not norm matched? Actually maybe random controls before norm matching? They say random controls had bigger applied norms; maybe because C=2 and random_delta norm? Need not rely.

Need consider central question: "does attenuation subspace plausibly encode a name/concept pointer WITHOUT attribute bindings, or does the C=2 reflection overshoot attribute coordinates? What cheap test discriminates?"

We need provide analysis. Need think about what evidence indicates.

The C=2 patch sets U-span coordinate to 2Δ - P h. If source spider has live P h (spider vector). Let δ_target = μ_target - μ_spider (projected and norm-matched). Then P h around μ_spider? Let's define spider template mean μ_s. At decode on spider prompt, P h presumably near μ_s? Maybe with prompt context. Then relative to μ_s: let x = P h - μ_s. Target desired maybe μ_t = μ_s + Δ_raw? Since Δ = P(μ_t - μ_s) norm-matched. At C=2, P h' = 2Δ - P h. Relative to μ_s? Need compute; if Δ ≈ P(μ_t - μ_s). If we center at μ_s: P h = μ_s + x. Then C=1 gives μ_s + Δ (if Δ is difference? Actually P h' = Δ, not μ_s + Δ; they treat Δ as full target? Wait Δ = U U^T (μ_target - μ_spider) then norm matched. This is a difference, not target vector. Patching to Δ seems to replace span with difference, not source+delta. That's odd. In equation P h' = (1-C)P h + C Δ. At C=1, P h' = Δ, not μ_spider + Δ. So if h live source component is near μ_spider, C=1 sets to μ_target - μ_spider (projected), which could be a vector representing target relative to source, not target absolute. Does residual stream encode absolute concepts or relative relation? Usually patch would be h_source + Δ. Their formula h' = h + C(Δ - span) implies if span ≈ μ_s, then at C=1 h' = h + Δ - μ_s? Wait h' = h + C(Δ - span) in full residual. If span = P h. In U coords, P h' = Δ. But h' full = h + Δ - P h. So if h = μ_s, h' = μ_s + Δ - μ_s = Δ in U-span, and orthogonal unchanged. So the component is set to Δ, which is a difference vector. Perhaps this is intended: they call "template attenuation delta" maybe Δ itself encodes target concept? In activation patching, one can set residual to target mean, not difference. But here Δ is mean difference. Norm matching maybe because then norm similar? Need flag as potential confusion. But evidence naming transferred, so perhaps Δ direction is enough to steer due to linear directions with sign, and setting to difference acts similar? Hmm.

Let's reconstruct formula exactly:
Δ = U (Uᵀ (μ_target - μ_spider))       # project template mean difference into U-span
Δ = Δ * ‖μ_target - μ_spider‖ / ‖Δ‖     # norm-match
# At each step:
span = U (Uᵀ h)                      # live source component, P h
patched = h + C (Δ - span)
# U-span: P h' = (1-C) P h + C Δ
# C=0 -> P h ; C=1 -> Δ ; C=2 -> 2Δ - P h

If base source h has P h = maybe near 0? If residual stream is mean-centered? Typically residual stream after pre-training maybe not zero mean globally. If P h is not μ_s but some arbitrary, then shifting to Δ is huge. In their naming results C=2 transfers identity, so reflection works.

Could be that Δ is not just difference but after norm matching can be high norm; C=2 amplifies further. In U coordinates P h' = 2Δ - P h. If |Δ| ~ |μ_target - μ_spider| and P h maybe arbitrary, then the resulting vector may not equal target mean. Overshoot possible.

Central question asks: "does attenuation subspace plausibly encode a name/concept pointer WITHOUT attribute bindings, or does C=2 reflection overshoot attribute coordinates? What cheap test discriminates?"

We need answer likely from evidence: In every C=2 real cell, identity transferred. Bound attributes did not. One C=2 random direction cell showed digit moved while text kept spider identity. This suggests digit movement and identity movement are separable. Does U encode name pointer without attributes? Or C=2 reflection overshoot attribute coordinates? We need propose discriminator.

Need think about possible models:
1. Pointer-only subspace: U captures a "name/concept pointer" direction (e.g., animal identity) but not attributes. Then C=2 reflection moves name token, but downstream attribute computations are fed from unmodified complement or from live source context, leading attribute answers remain spider-like (or inconsistent). But why random direction moved digit? Random direction maybe accidentally moved digit by moving hidden state toward target numeric answer? Could be because numeric digit responses are low-dimensional and random perturbation sometimes induces correct number? Need not.

2. Overshoot attributes: U contains both identity and attribute coordinates. C=2 reflection about Δ overshoots attribute coordinate, yielding "too much target" that saturates? Actually if target dog has legs=4, source spider legs=8. What does "overshoot" mean along leg coordinate? Suppose leg count encoded as scalar z_legs; spider z=8, dog z=4. Direction Δ (dog-spider) might be negative on z_legs. C=2 reflection about Δ in z_legs coordinate: z' = 2Δ_z - z_source. If Δ_z roughly target - source (if projected), then z' = 2(target-source) - source = 2 target - 3 source? Wait depending coordinate baseline. Could overshoot beyond target, maybe to lower than dog? For legs: source spider 8, target dog 4. If Δ_z = μ_t - μ_s = -4 (if direct), C=2 gives z' = 2*(-4) - 8 = -16? That would not produce '2' or '4.' So not straightforward.

But if we consider normalized coordinates or centering? Hmm.

Actually U-span maybe encodes linear features. The reflection about Δ is: z' = 2Δ - z. If we assume z_source is spider feature coordinate and Δ is target feature direction? Might produce weird.

Observed legs-dog-C2 first digit '2'. Is '2' maybe halfway? spider legs=8, dog=4, half? 2 is maybe overshoot below dog? If dog target 4, 2 is below dog. Overshoot attribute toward "man's best friend" maybe dog puppy? Not clear. Text says dog has four legs, but digit is 2. Could be from prompt: "How many legs does the animal that spins webs have?" Maybe it first outputs "2" as answer to "animal that spins webs"?? No. Hmm.

Need not overfit specific numbers. The evidence says dog-legs answered "2" while describing a dog and text says four legs. That's dissociation between generated final answer token and text. The key dissociation: when asked "How many legs", the model's first token is not target value or source value; but text can mention dog and four legs. The bound attribute (leg count) not transferred as answer.

Legs-ant-C2: first='6' answer='6' n=61 r2=0.000. Spider has 8 legs; ant has 6 legs. Target ant; correct ant legs=6. So in ant case digit moved to correct target! Text "The red ant ..." So for ant, identity and leg count both moved. Wait prompt legs-ant-C2 expects target ant; first token '6' correct. So bound attribute transferred in ant case? The evidence in central question says "dog-legs answered '2' while describing a dog ... dog-property named dog, said 'Dogs are mammals', but answered 'No' to 'is it a mammal'; ant-property named ant but answered 'No' ...". It doesn't mention ant legs as failure; ant legs was correct 6. So maybe leg count not consistently failed; dog legs specific failure maybe due to source/target? Need note: the central question states "intervention transfers animal identity (the name) in every C=2 cell, but does not transfer bound attributes (leg count, class membership): dog-legs answered '2' while describing a dog (and text says a dog has four legs); dog-property named dog, said 'Dogs are mammals', but answered 'No' to 'is it a mammal'; ant-property named ant but answered 'No' to a yes-antennae question and then looped." It omits ant legs correct. But evidence includes ant legs correct 6. So "does not transfer bound attributes" is too broad? Maybe only some bound attributes failed. Need incorporate.

Actually legs-dog-C2 first='2' but text says dog typically four legs. They classify this as bound attribute not transferred because first numeric answer '2' not 4. But it's not source 8 either; it's maybe an incidental incorrect digit. If source spider remained, answer would be 8 (as C=0 likely). So patch changed digit from 8 to 2, not 4. Could be overshoot in leg-count direction producing "2" below dog. That might support overshoot attribute coordinate. For ant legs C=2, first='6' correct target. Why ant not overshoot? Maybe because ant leg count is closer to spider (8->6) and overshoot still maybe 6? hmm.

Let's compute possibility: Reflection about Δ. Suppose in leg coordinate z_source (spider prompt) = 8 (or maybe transformed). Target dog desired 4. Δ_z maybe not equal -4 depending projection/norm. It sets C=2 to z' = 2Δ_z - z_source. For ant: source spider z=8, target ant z=6. If Δ_z = -2, then z' = 2*(-2)-8 = -12, not 6. So if the coordinate was directly linear leg count, ant would overshoot not produce 6. Since ant produced 6, linear scalar model invalid. So model not simple.

Maybe the first token digit is generated from downstream unmodified contexts; intervention only affects hidden at certain positions; answer token maybe from earlier layers? Need think.

The design edits four positions: prefill last 3, then decode last 1. So all token positions in prompt residual at layer20? Need clarify. "Generation path, every decode step at the edited position": for each decode step at the edited position, patch that position. "Four edits per animal. Edited positions: prefill last 3, then decode last 1." Means they patch at layer20 at the last three token positions of prefill and the newly generated token (last 1) maybe? Need infer.
## Final answer call answer

# Reconstruction of the method

The construction operates as follows:

1. **Templates.** For a source concept (spider) and a target concept (dog or ant), the mean residual at layer 20 is computed from template prompts. The raw mean difference \(\mu_{\text{target}} - \mu_{\text{spider}}\) is projected into the span of an orthonormal basis \(U\) (rank 4). The projected delta is then norm-matched to the raw mean-difference norm, yielding \(\Delta\).

2. **Live steering.** During decoding at the edited position, the live

## Completion

- outcome: `completed_after_follow_up`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_deepseek-v4-pro-0813_span_pass1_deepseek.trace.jsonl`
