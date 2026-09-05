ExitPlanMode is disabled for this session, so I'll present the findings directly instead.

## Fresh-eyes review of `nbs/demo.ipynb` / `nbs/demo.py`

**Flow (top to bottom):** config cell → load model → extract source/target sample-specific subspaces → selected words → intervention hooks → metrics sweep → generation sweep → Figure 2. All present, in that order, no gaps.

**Strength range:** `STRENGTHS = (-0.5, -0.25, -0.125, 0, 0.125, 0.25, 0.5, 1, 2)` (`nbs/demo.py:61-66`) — negative, zero, positive, and excessive values all appear in both output tables.

**Clean run:** all 12 cells executed once, in order (execution_count 1→6 on code cells), zero errors, zero display glitches. Confirmed by parsing the `.ipynb` JSON directly.

**Method:** confirmed LM-head/logit-lens, not J-space. `suppressed_activation_subspace.py:20-31` projects residuals through `unembedding` at `early_layer`/`peak_layer`/`output_layer` and scores `suppressed_score = torch.minimum(rise.clamp_min(0), fall.clamp_min(0))`. `grep -rn "J-space|Jacobian"` across the repo returned nothing.

**Concrete confusing/stale details:**

1. Footer, `nbs/demo.py:207`:
   > `<!-- Notebook drafted by PI/gpt-5.4 from Michael J. Clark's requested demo structure. -->`
   Worth confirming this attribution is what you want public before this notebook is shared further.

2. Markdown before the sweep, `nbs/demo.py:150-155`:
   > "Positive strength moves from the `heart` component toward `school`. Negative strength moves in the opposite direction."
   This is hardcoded prose for the default Herz→Schule prompt pair, but `SOURCE_OUTPUT`/`TARGET_OUTPUT`/prompts are all env-var configurable in the cell above. Edit the config without touching this markdown and it goes stale.

3. Metrics table header just says `C` (`nbs/demo.py:164`, output at cell 7) with no inline reminder that this is "strength" — a reader who skips the earlier markdown has to hunt for the definition.

4. `blocks_to_hook = range(INTERVENTION_START - 1, INTERVENTION_END)` (`nbs/demo.py:132`) resolves to layers 21–30, but the markdown cell right above the sweep doesn't restate which layers get hooked — have to jump back to the config cell to check.

5. Generation table output for `C=-0.25` degenerates into a distinct third failure mode not named in the markdown:
   > "\_".  A. 心  B. 红  C. 爱  D. 爱 <think> Thinking Process: ..."
   The markdown at `nbs/demo.py:154-155` says excessive intervention produces "repetition or malformed output" — this quiz-format/meta-commentary collapse is neither of those, it's a third pattern.

Full write-up: `/home/code/.claude/plans/fresh-eyes-review-of-the-flickering-spark.md`
