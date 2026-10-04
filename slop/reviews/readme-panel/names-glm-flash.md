**Guesses (based only on the first-page README):**

1. **found** — fraction of prompts where the target English/Chinese word appears somewhere in the output words (any rank). Higher better. Confidence: medium.
2. **leaked** — fraction of prompts where the "hidden" word shows up in text the model actually says, i.e., trivially copyable from the surface transcript rather than from activations. Lower better. Medium.
3. **share** — the fraction of attention/activation mass, or of prompts, captured by the found subspace; plausibly the proportion of the hidden word's signal relative to all words scored. Higher better. Low.
4. **TP** — true positive rate: among prompts that truly contain the concept, fraction flagged. Higher better. Medium.
5. **hits** — count or share of prompts where the hidden word is among the top scored words (any threshold). Higher better. Low.
6. **hidden hit@8** — fraction of prompts where the true hidden (English/Chinese) meaning word is in the top-8 scored words. Higher better. Medium-high.
7. **said hit@8** — same but where the hit is the word the model is about to say in that language — measures finding the answer only because it's predictable from output. Higher = leakage-ish; context-dependent. Medium.
8. **hit@8 hidden, not said** — the strict/deconfounded metric: top-8 contains the hidden concept word and none of the 8 matches the word the model will say — exactly the README's pass condition. Higher better. Medium-high.
9. **pass** — boolean per-prompt pass indicator (averaged): top-8 contains the target English/Chinese word and none of the 8 is from input/output language or the about-to-be-said word — precisely the leaderboard definition. Higher better. High.
10. **pass rate** — same as (9) but as percentage/share of prompts rather than mean of 0/1; likely redundant with `pass`. Higher better. Medium.
11. **AUROC hidden vs said** — area under ROC separating "hidden concept" word scores from "about-to-be-said" word scores within a prompt; measures whether the transform distinguishes mind-content from mere output prediction. Higher better. High.
12. **transfer found** — pass/found rate on the held-out translation pairs the transform wasn't tuned on — the generalization test the README emphasizes ("any winning calculation will generalise"). Higher better. Medium.

**Missing info:** table itself isn't supplied, so rank-order consistency between columns can't be checked; whether `share`/`hits` are per-prompt fractions or counts; whether "said" hits are removed from `found`.

**Recommended self-explanatory names:** `hidden_word_in_top8`, `answer_word_not_in_top8` (or `no_output_leak`), `strict_pass_share` (per README definition), `auroc_hidden_vs_about_to_say`, `heldout_pairs_pass`. These state the condition, the reference word set, and whether higher is better without a caption.

— GLM Flash