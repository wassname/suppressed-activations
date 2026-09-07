# Attenuation naming tests, jobs 658-660

Written by Codex/GPT-6. These naming failures include an article confound: source ends `called a`, ant donor ends `called an`. Definite-article controls are queued as 665/666. Do not treat this as a clean rejection of ant transfer.

## ML-debug evidence

- Logs/config: all 55 stdout lines read for each coverage sweep. Qwen3.5-4B, pinned revision in JSON; L12/16/20, positions3/all, C0/1/2, rank4 L25-to-L32 attenuation span, matched difference norm, no residual renormalization. Extraction and generation use official templates with deliberately different user instructions.
- SHOULD: `C=0 gives identical generation and logits because its displacement is zero.` Runner assertions passed. Independent token-ID equality checks pass all zero controls. Hidden states come from the generation call, not a separate readout forward.
- Null: all zero controls reproduce spider. The next-token score concerns ` ant` or ` dog` versus ` spider`; bold formatting competes, so these probabilities are not total animal-answer probabilities.
- Initial samples: unmodified source names spider and describes eight legs. Clean donors name ant/dog and describe them coherently; full strings are in each condition log.
- Dummy/baseline: no intervention preserves correct source identity. No tested nonzero coverage condition gives an unambiguously correct target description. A large log-odds change can coexist with a fictional insect or correction loop.
- Held-out: this is a new naming consequence of a configuration selected on leg counts, but the article mismatch confounds ant failure. No random matched control in this particular sweep. Earlier random controls cannot establish specificity here.
- Schedule: no training or learning-rate schedule.
- Full samples: ant L20/all/C2 says ` **beeswax ant**.` then claims wax production and hive-like structures. Dog L20/C2 repeats `**Corrected Fact:** The animal that spins webs is called a **dog**.` Full verbatim outputs are linked below.
- Worst step: dog repetition fraction .386, max128 truncation. Loss and gradients are not applicable. This is sustained intervention, not an early steering stop.
- Surprise: local-span smoke says ` **beeswax bee**.`. Chasing now: source article may constrain direct ant naming; span may also mix social-insect features.
- Missing evidence: matched grammatical suffix control, semantic specificity controls, correct full-vocabulary readout, layer-local span generalization.
- Working diagnoses, not fitted probabilities: semantic mixture/selector limitation45%; article/task-format confound35%; implementation bug5%; evaluation decoder/calibration bug10%; unknown5%. Mixture evidence is invented wax biology; against it, article control is untested. Coverage/C0 checks argue against missed hooks but do not validate the selector. Clean implicit midpoint errors support calibration problems; those cannot alone explain the generated fiction.
- Independent review: continuous_review verified all36 conditions: `All C=0 generations exactly match their stored base token IDs`; `All decode counts equal generated token count minus one`. Last3=[32,33,34], all content=[25:35]. Reviewer warns that grammatical fiction is not semantic coherence.
- Cheapest discriminator: replace `a/an` by common `the`, keep intervention fixed. Article explanation predicts better ant naming; persistent fictional species would favor concept mixture. Local-span comparison separately tests representation mismatch.
- Runtime/memory: ant elapsed79.0078s, peak13,728,242,688 bytes; dog77.7179s, peak13,725,563,904 bytes (JSON). Reuse loaded model across conditions, as the runner does.

The local-span smoke fits L20-to-L32 attenuation. One held-out direction increases mean square from .2153 to .3918 despite decreasing on fit templates. Positive training eigenvalues do not guarantee held-out attenuation. svd_review recommended comparing local versus L25 spans at fixed L20, including natural and matched magnitudes; jobs661/662 implement that comparison.

Sources: [ant coverage](../../out/2026-09-08_attenuation-coverage-ant/result.json), [dog coverage](../../out/2026-09-08_attenuation-coverage-dog/result.json), [local smoke](../../out/2026-09-08_attenuation-local-ant-smoke/result.json).
