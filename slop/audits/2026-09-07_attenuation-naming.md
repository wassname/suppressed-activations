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

## Local-span comparison, jobs 661/662

All 51 stdout lines for each run and every nonzero full continuation were read. Ant local spans produce spider, beeswax bee, or beehive/bee; no correct ant identity. The article confound still applies.

Dog local L20-selected span produces coherent dog descriptions through EOS in all four C2 conditions (natural/matched magnitude, last3/all content). Late L25-selected matched spans loop, natural spans remain spider. This supports direction quality, not merely stronger perturbation, as a useful change in this example. The local natural condition begins:

> **dog**.
>
> Description:
> The dog is a domesticated canine that has been raised by humans for thousands of years to serve as companions, working partners, and family members.

Full sources: [ant local](../../out/2026-09-08_attenuation-local-ant/result.json), [dog local](../../out/2026-09-08_attenuation-local-dog/result.json). Ant all16 C0/coverage checks independently pass. Dog checks and fresh independent review remain to do. Do not interpret this one development naming task as broad reliability.

## Follow-up, jobs 665-669

Dog local all16 coverage/C0 checks now pass; continuous_review confirms the coherent outputs. At matched last3/C2 both local and late selectors have perturbation norm18.9395, so size alone does not explain coherent versus looping behavior. One local dog held-out direction grows (.0624 to .0894 mean square); the selection is not uniformly held-out attenuated. None of its top-eight suppressed readouts names dog.

The `known as the` suffix control does not fix ant: job665 remains spider and mixes in nectar-gathering traits. Job666 late-span dog names dog but explicitly says dogs do not spin webs, then gives a coherent dog description. This is no loop, but not unqualified replacement. The wording also changes from `called a`, so it is not an isolated article effect.

Job667 local ant rank1/2/4 and C0/1/2/3/4 gives spider, bees, or beehive. All49 stdout lines and every nonzero full generation read. Rank2 and rank4 at C2 produce the same coherent bee description; C3/4 produce hive-as-animal errors. All15 coverage/C0 checks pass. This does not support more strength or lower rank as sufficient here. [Rank sweep](../../out/2026-09-08_attenuation-rank-ant/result.json).

Fixed local dog (rank4,L20,C2,last3) transfers to original leg count in668 and common-article naming in669, both through EOS without correction. Full outputs read and coverage checked. Leg output starts `4.` then `The animal is a domestic dog, a popular companion known for its loyalty and ability to understand basic commands.` Naming starts ` **dog**.` and gives a domesticated-canine description. [Legs](../../out/2026-09-08_attenuation-local-legs-dog/result.json), [naming](../../out/2026-09-08_attenuation-local-name-the-dog/result.json).

Next discriminator671 uses unrestricted template difference for ant naming. svd_review found no ant/bee label or sign error. If unrestricted also gives bee, reviewer recommends comparing final-template-token extraction with three-token averaging, keeping continuous intervention coverage unchanged, and adding bee as a clean distractor. Spider/ant separation alone cannot prove ant specificity.

## Full-difference discriminator, jobs 671/672

Both completed successfully; all21 stdout lines and full generation strings read. The unrestricted L20/C2 template difference gives ` **ant**.` followed by a coherent colony/division-of-labor description. Thus changing extraction averaging is not the next priority: projection introduces the naming failure in this paired example. [Full difference](../../out/2026-09-08_full-template-name-the-ant/result.json).

The added clean bee diagnostic leaves generation exactly equal to667row12. Bee scores are mostly positive on the spider-ant centroid axis. Ant remains higher than bee within matched templates, so the span is not proven devoid of ant information; the zero threshold is not ant-specific. [Bee diagnostic](../../out/2026-09-08_clean-bee-distractor-ant/result.json).

Job674 compares P d + alpha (I-P)d at alpha0/.25/.5/.75/1, each rescaled to the full difference norm. All edits stay L20/C2/last3 plus every decode token. Mixed-space edits are not suppressed-only. CPU checks verify endpoint recovery and constant total norm; the runner logs selected and discarded per-token perturbation norms. Reviewer svd_review cautions that rescaling also decreases the selected component, so if an intermediate mixture improves, compare against a pure selected edit at the same selected magnitude before crediting discarded content alone.
