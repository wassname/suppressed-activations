## Second opinion

### Verified in the supplied files

The leaderboard is a reproducible **token-recovery benchmark**, not yet a validated hidden-thought benchmark. `score.py` selects settings on ru→ko, then evaluates four other language pairs. The published table reports 74 translation prompts and 36 English-only questions. Its winning row scores 0.93 on translation and 0.00 on English transfer; attention-output J-lens reaches 0.06 transfer.

“Found” requires a labelled English/Chinese token among eight distinct token spellings, without script-defined leakage or the exact next-token ID. These are not necessarily eight complete words. The scorer does not check translation correctness, full generated answers, or semantic leakage. English transfer labels use individual words from bridge aliases, so recovering one component of a multiword name can count.

The README contradicts itself: its challenge section says German/French/Russian; the current benchmark uses Russian/Korean/Arabic/Hindi/Thai. Best methods use vocabulary-space lenses; the best fixed-subspace row retains 1024/2560 dimensions.

### Assessment

**1. Well posed, with a narrower claim.**  
The operational metric is reasonably clear. The interpretation—“precisely isolates unsaid thoughts”—is not established. Recovering an English equivalent of the input could mean decoding shared lexical semantics, not observing an internal English reasoning step.

The metric remains gameable. A submission could restrict scores to Latin/Han tokens and suppress output-logit leaders, optimizing cleanliness rather than identifying hidden computation. The entry API exposes residuals and logits, and runs arbitrary Python without an enforced information boundary. Published prompts also permit memorization. A fixed-list control rules out only one particularly weak shortcut.

Evaluation against English labels is not inherently circular. However, selecting token unembedding directions with vocabulary scores and then showing those directions recover tokens is insufficient evidence for an independently discovered thought subspace. The README’s claim that any winning calculation will generalise is unsupported.

**2. Transfer is a hypothesis, presently failing.**  
Translation provides an unusually convenient separation between scripts. In all-English tasks, script filtering cannot distinguish inputs, answers and intermediate concepts. The observed transfer failures matter, although tokenization and strict leakage rules could conceal partial recovery.

Transfer would become credible through frozen, label-free methods evaluated on held-out concepts and task families, with full-entity scoring and matched leakage policies. Causal edits should change several properties consistently associated with the recovered entity, not merely move one answer token.

**3. Recommended README order.**

1. Goal: discover task-relevant representations not explicitly output.
2. Caveat: translation is a labelled proxy, not proof of English thoughts.
3. Exact submission contract, permitted fitting data, forbidden label access, and separate fixed-subspace/readout tracks.
4. Metric, exclusions, split construction and limitations.
5. Current table, prominently including failed English transfer.
6. Setup, dependencies, data preparation, hardware and minimal submission example.
7. References and linked historical research.

Move everything below the current leaderboard into an archive. Cut the broad virtue/eval-awareness promises and the assertion that prior translation results prove models “think in English.”

**4. Most important missing control.**  
Add a strong **input-semantic decoder baseline**: recover English equivalents directly from source-token embeddings or early representations, under the same scoring rules. If it matches the winner, translation success need not involve suppressed thoughts. Also report target recall separately from cleanliness; the combined score conflates two problems.

— OpenAI GPT-5