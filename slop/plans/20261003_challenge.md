# Suppressed Activation Challenges: Find Where Llamas Work

Goal (wassname): find a fixed transform or subspace that reads what a model thinks but does not say, scored by a
non-circular leaderboard, then share it as a challenge. Steering uses the same object. — PI/OpenAI, 2026-10-03

- [ ] goal A: a clean, fast leaderboard that cannot be gamed by language lookup
  - [x] distant in/out languages (ru, ko, ar, hi, th); English and Chinese are the hidden languages
  - [x] said/input = any token in the input or output Unicode script, plus the model's next token
  - [x] headline "unsaid" = share of top 8 distinct words in English/Chinese; exact-word "found" as a check
  - [x] 20 prompts per pair; settings chosen on ru→ko only; English two-hop set used only to report
  - [x] gpt-6.1-sol code review applied (exact words, special tokens, dev-only grid, fixed-list control)
  - [ ] run job 2929 (word lists, then scoreboard); read skipped prompts and top-8 examples per row
  - ~~[ ] top-40% probability cutoff~~ - rise-and-fall scores are not probabilities, so rows would not compare
  - ~~[ ] Wendler de/fr pairs~~ - wassname: too close to English
  - failure modes: a row scores high by listing generic English (the fixed-list control shows this);
    many prompts skipped for formatting; word lists too small after model screening
  - deliverable: `out/<run>_leaderboard/leaderboard.md`
- [ ] goal B: README is a challenge a new reader can enter
  - [ ] title "Suppressed Activation Challenges: Find Where Llamas Work"; Wendler Fig. 2 at top (done)
  - [ ] replace the leaderboard section with the 2929 output; ★ = uses a lens; links to each transform
  - [ ] short related work: Dumas et al. 2024, Bayazit et al. 2026, Schut et al. 2025, Gurnee et al. 2026
  - [ ] steering section from the country-swap draft (7/10 and 6/10, controls 0/10)
  - [ ] delete old scripts 09/10/11 and the 2026-10-02 slop scoreboard runs from the README path
  - [ ] frontier models each rewrite the README from scratch for a new reader; wassname picks
  - failure modes: README says more than the numbers show; old sections contradict the new table
  - deliverable: uncommitted README diff for wassname
- [ ] goal C: better transforms (open research)
  - [ ] untried: contrastive PCA of overwritten states; cross-language invariant subspace; transfer neurons
  - [ ] English transfer is the open problem: hidden word sits at the clue tokens, not the last token
  - failure modes: a gain that is only rank (check against the random-subspace row)

## UAT / Verification
- `out/<run>_leaderboard/leaderboard.md`: fixed-list and random rows sit below the methods on "unsaid";
  if not, the metric does not measure thought and goal A is not done.
- `git diff README.md`: one leaderboard, numbers match leaderboard.md, every row links to code.

## Appendix
- Review: `slop/reviews/2026-10-03_challenge-code-review.md`. Related work notes: `slop/research/2026-10-03_related-work.md`.
- Country-swap steering draft: `slop/drafts/2026-10-02_readme-country-swap-section.md`.
