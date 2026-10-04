# Oracle brief: what transform should we try next?

Repository `/workspace/2026/suppressed-activations` (read-only). Answer in about one page.

## Goal (wassname's words, README)

> We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

From AGENTS.md: "having english thoughts is the eval not the training". The real target is reading what a model thinks but does not say, including in all-English settings.

## Setup

- Qwen3.5-4B, 4-shot word translation between Russian, Korean, Arabic, Hindi, Thai. Hidden word = the English word or its Chinese translation.
- A transform maps one forward pass (residuals at the last prompt token for all 33 layers, layer-23 attention output, final logits) to a score per vocabulary token. Top 8 words are scored per prompt: TP if the hidden word is there, FP if any input/output-language word or the model's next token is there. F1 = 2TP/(2TP+FP+FN) over prompts.
- Rules: no word lists, language labels or test prompts. Fitting on generic text (300 WikiText texts) is allowed. Settings chosen on ru→ko only.
- English-only transfer: 102 TwoHopFact questions; hidden = bridge entity; FP = words of the question or its answer.

## Current results

Read `out/2026-10-04_182050_leaderboard/leaderboard.md` (149 test prompts, 90% bootstrap CIs) and `scripts/challenge/transforms.py` (all transforms, ~190 lines).

Summary: best simple row is layer-change PCA (top-1024 PCs of x[l+1]−x[l] on WikiText, rank 1024 of 2560) F1 0.91 (0.88–0.93). Logit lens 0.87, random rank-1024 subspace 0.85. Using an external Jacobian lens, per-prompt rise-and-fall reaches 0.96. English-only F1 ≤ 0.09 for every row. Earlier observation (README archive, not in this brief): the bridge entity in two-hop questions is readable at the clue-entity token positions in 36/62 questions, but at the last token only 12/62.

## Questions

1. Propose 3–5 concrete transforms to try next that obey the rules. For each: one-line intuition, pseudocode (a few lines), and the most likely way it fails.
2. Why might every row fail on English-only questions? Is the last-token, top-8, logit-space scoring itself the problem? What would you change, without making the score circular?
3. Which one experiment gives the most information per GPU hour?

Separate what you checked in the files from your opinion. Sign with your model name.
