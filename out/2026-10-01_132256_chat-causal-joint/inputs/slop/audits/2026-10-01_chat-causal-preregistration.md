# Native-chat joint-property causal attempt

— PI/OpenAI. Prospective development attempt; no pretrained outputs observed. Both goals stay open. Exact prompts: `data/dog_spider_donors_chat_v4.json` and `data/dog_spider_joint_chat_v1.json`. Decision discussion: `slop/reviews/2026-10-01_after-indirect-donor-next-attempt.md`.

## Why this attempt

Run2687's indirect donor changed neither initial property answer. The literal-name control changed skeleton position but not leg count. Later8 belonged to an NLI hypothesis. Offline donors ended at ` It`, while edited prompts ended at a space or ` the`. This supports testing context-dependent transfer, but does not diagnose it.

Change both preparation and evaluation to the same nonthinking native-chat assistant-start role. Ask two properties in one concise response, so a digit change alone is distinguishable from target-consistent behavior. This is a bundled method/frame development change, not an isolated role-alignment experiment. Known dog/spider concepts and prior failures informed selection; these are not unseen concepts.

## Fixed procedure

- Same pinned Qwen3.5-4B, tokenizer and J-lens; reuse08's preparation and intervention pipeline.
- Four literal-name generic instructions per animal, with system `Answer briefly. Do not explain.`. Eight ordinary offline prefills, no generated preparation text. Capture final-position residual16 (block15 output); average four states per animal. Donor configuration contains no tested properties or answers.
- Same system and tokenizer serialization for all three evaluation prompts. Save exact rendered strings/IDs and assistant-start suffix. Require all preparation/evaluation suffixes to match. No template fallback.
- Natural delta is mean(spider) minus mean(dog), with no fitted or rescaled dose. Positive for dog→spider and arithmetic; negative for spider→dog.
- Block15, last prompt position (`-1:` is an explicit exception to the repository default), then0.25 strength on every cached decode call. Observer23 records only and returns no replacement. No current-input prepass/backward or observer feedback.
- Four conditions per prompt: Base, new role-aligned donor, fixed previous literal-name donor, and one seed0 random direction matched to the new donor norm. Sign reverses consistently for both donors and random. The previous donor retains its own norm; no orientation-only claim.
- The previous donor is the fixed literal-name checkpoint with SHA572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5. It is selected as a useful existing partial-positive comparator, not promoted to the primary method or chosen separately per case.
- Greedy generation, no repetition modification, maximum32 new tokens; stop on tokenizer or model EOS. Preserve exact decoded text/IDs and actual token count. Expect one prefill plus n−1 cached calls for n generated tokens. Store requested and realized BF16 edits and verify downstream states.

Budget:8 generic forwards plus12 trajectories, at most392 forwards/384 generated tokens. One default-queue job, initially300s. No replacement prompts, automatic extension, parameter search or v5 use.

## Outcomes and decision

Base expected pairs are dog `(4, inside)`, spider `(8, outside)`, arithmetic `(4, even)`. Edited animal targets are the opposite animal's pair; arithmetic should remain `(4, even)` in all conditions.

Report each property, joint consistency, format compliance, exact output and arithmetic preservation separately. Number words or unambiguous paraphrases can be recognized in the semantic review, with quoted evidence; literal format matching is a separate diagnostic. Keep wrong baselines, partial/capped answers, contradictions and unscoreable text in the denominators. Do not mistake a hypothesis for an affirmed answer.

Two target-consistent properties provide evidence beyond a changed digit, not a universal user completion threshold. One-property movement is a partial result. Similar random behavior or arithmetic changes support nonspecific effects. Preserved arithmetic alone does not establish broad specificity. One random direction gives no null distribution. First-token8/4 log odds and repetition are diagnostics, not joint-property or coherence scores.

Before queue: real tiny-Qwen preparation and all12 conditions at seeds0/1; exact means, shared suffixes, sign/norm controls, requested/applied/downstream tensors, early-EOS coverage, unchanged weights/defaults and hook ownership. Preserve interruption artifacts. These tests and source review are not pretrained scientific validation.

Job2705 uses immutable08/launcher copies. Its consumed hashes were rechecked before this implementation: `2026-10-01_queued-reference-isolation.json`. Working08 may change; its shared helpers, cached cases, reference config and queued copies remain untouched.
