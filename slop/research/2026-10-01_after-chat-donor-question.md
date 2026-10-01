# Next causal decision after the native-chat donor test

— PI/OpenAI. No next intervention selected or implemented. Readout job2716 is queued independently; its source/helpers/data remain frozen.

Goal: coherently change an unspoken concept in one current-input inference pass. Generic offline preparation is allowed; current-input prepasses/backwards and later-layer editor feedback are not. Local GPU/default queue only; one short job initially capped300s. No automatic dose/sign/layer/window rescue. Preserve partial positives without making experiments or diagnostics into goal completion.

## Observations

2706: correct concise Bases (`4; inside`, `8; outside`, `4; even`), unchanged in all twelve conditions. Both new role-aligned and previous literal donor change0/2 animal properties, arithmetic remains correct. Primary natural delta0.920599, old literal1.430336, random matches primary; block15, last prompt position only, quarter decode. Exact saved F32/BF16 updates survive, about9.5% of residual norm. Dog/spider prefill readouts retain their original identities.

Posthoc saved-state geometry, not a fitted feature or an editor input:

- Generic mean endpoints along the normalized spider-minus-dog direction, centered at their midpoint: dog−0.460300, spider+0.460300.
- Actual dog before edit−0.493004, after BF16 edit+0.428820. It nearly reaches the generic spider endpoint but still answers4/inside.
- Actual spider before edit−0.382797, after edit−1.301908. Both clean task states are on the generic dog side, despite distinct correct answers.
- Actual task-pair coordinate gap0.110207, versus generic gap0.920599. Only0.005983 of the squared task-state difference lies on that axis. This difference also contains wording/length/context effects; it is not isolated concept ground truth.

Interpretation: the direction is not a reliable context-independent class coordinate here. But a cosine/axis fraction or same-sign states alone cannot prove absence of a causal feature. In particular, an exact endpoint clamp is poorly motivated as an immediate fix: dog already nearly reaches that endpoint. No fitted cutoff or dose change follows from this diagnostic.

Sources: `out/2026-10-01_132256_chat-causal-joint/{verification.json,donor_axis_diagnostic.json,semantic_review.md}` and `slop/audits/2026-10-01_job2706.md`.

## Options to compare

1. **Same addition rule, a different concept family.** A small country-pair joint-property task (e.g. unspoken Sweden/Japan, capital and currency) with natural generic native-chat donors and matched random/arithmetic controls. Prior readout evidence is strongest on countries; the local reference paper reports country swaps easier than animal swaps. This is a new domain test, not a claim of reproducing that paper. The old2648 explicit Italy/Japan raw-coordinate swap failed; it was not natural donor addition and not an implicit-country task. Need exact cues, distinct properties, factual/tokenizer checks and honest selection history. Production08 would require clearly named configurable concepts/answer tokens, not pretending country states are dog/spider keys.
2. **Context-conditioned offline transport.** Fit an identity-regularized affine source-to-target activation map on paired generic contexts, rather than adding one average delta. Concept and context variability, held preparation examples and decode distribution must be addressed. More implementation/calibration cost; lower latent MSE would not itself establish causal transfer. Existing affine helpers forecast final states, not this task. No current questions/answers may enter fitting or be used to choose its strength.
3. **Another endpoint/reflection or coverage change.** Defer absent a new mechanistic reason: prior reflection/context-coordinate checks failed, dog now reaches the nominal endpoint, and automatic window/layer/dose rescue is excluded.

Please compare the first two concretely and identify one small next attempt, or reject both with a better bounded alternative. Ask one material supervisor question before finalizing. Preserve uncertainty about which variables drive behavior. Do not invent sparse-clamp details, universal bidirectionality/property thresholds, or a paid-service dependency. Reuse08 rather than create another production inference path.

Relevant prior distinctions: `slop/research/2026-09-30_causal-reference-followup.md`; prior country run `slop/audits/2026-10-01_job2648.md`; current source/config `scripts/english/08_jlens_one_pass.py`, `data/dog_spider_donors_chat_v4.json`, `data/dog_spider_joint_chat_v1.json`. No additional inference is authorized by this brief alone.
