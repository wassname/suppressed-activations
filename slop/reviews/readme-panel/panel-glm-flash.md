All four files opened successfully (README, all three figures rendered). Cold-reader review follows.

---

## Cold-reader review: "Suppressed Activation Challenges" README

*Signed: GLM Flash*

**1. Central claim and challenge (my reconstruction).** LLMs translating between two non-English languages appear to pass through an intermediate "English thought": a mid-network layer where the English word for the answer has high logit-lens probability before being suppressed and replaced by the output language (Wendler et al.). The author builds a challenge around this: given a live forward pass, find a *general transform* — an arithmetic operation on the residual stream, not a vocabulary lookup — whose top-ranked decoded tokens surface that hidden English word (or its Chinese equivalent) while excluding input/output words. The motivation is interpretability-for-alignment: if we can isolate the "thought" subspace, we gain a handle for reading, auditing, and steering the model.

**2. Figures.**
- *cartoon.png*: pedagogical framing — robot translating French→Chinese "understands it in English" first, then converts. It sets expectations, carries no evidence.
- *wendler_fig2.png*: Llama-2-70B FR→ZH. Orange (English) rises near layer 40 to ~0.4, falls to zero by layer 80; blue (Chinese) rises from ~60 to ~0.5. Entropy bar drops around layer 45. This is the "rise-and-fall" phenomenon the transforms target. I got stuck on nothing here; it's clear.
- *language_pairs.png*: (a) Qwen3.5-4B FR→RU — English peaks ~0.49 at layer 28, then Russian rises — replicating the pattern in a smaller Qwen model. (b) pass rates on five held-out pairs: removing read/said words gets both methods to 92–99%, while the original un-cleaned methods sit at 11–63%. The intended takeaway is that the gain comes mostly from subtracting known words, not from the sophisticated transform. Stuck point: panel (a) is "mean of 78 words" but the word set/selection isn't named; panel (b) columns for rise-and-fall and plain lens differ by ≤1 prompt in some pairs, making the two top methods visually indistinguishable.

**3. Leaderboard.** One row = one transform applied per prompt; "found" = share of prompts whose top-8 decoded words include the hidden English word or its Chinese translation, with no input/output-language word and not the model's next token. Best row by **found↑**: "rise-and-fall, J-lens" at **0.93** (setting 28; transfer found 0.00). *Italic rows* are *controls* (plain lens, random subspace floor at 0.18, fixed list at 0.00) used to establish baselines. **★** marks transforms that use a lens or per-prompt vocabulary scores — making leaderboard winners and controls not methodologically independent, though the control rows also carry ★, so the comparison is apples-to-apples there. The random-subspace floor of 0.18 suggests some easy prompts inflate all methods.

**4. Ambiguities and tensions.**
- The text says "we can't cheat and find the English words by looking up English words," yet several transforms窥（peek）at the *said* word in the two-pass era and the current readout "removes prompt words and predicted-output spellings" — using the answer for masking is admitted; how this interacts with the no-cheating premise is addressed only obliquely ("masking alone carries the gain", "plain lens equals rise-and-fall when cleaned").
- "Transfer found" is 0.00 or near-zero across all leaderboard rows, undercutting the intro's hope that "the winning calculation will generalise to other settings." No row is highlighted as a positive transfer success.
- The "setting" column mixes formats ("28", "27/1024", "28/256") without explaining the semantics of the pair notation anywhere in-snapshot.
- The one-pass English section contradicts its own headline: 7/16 joint audit passes, but "0 confirmed" clean list recovery in the later Asia/chat subsection. Not contradictory per se — honest limitations — but a first-time reader cannot tell from the leaderboard alone which claims survive later probing.
- No definition of the scoring function's exact tie-breaking, or of "setting numbers" (5, 7), anywhere in the README.

**5. What I'd need to submit my own entry.**
- Access to `scripts/challenge/transforms.py` (CLI signature to copy an existing row).
- The pinned model checkpoint/cache and lens (model name is implied as Qwen3.5-4B but never stated in the visible text).
- The test-set prompt files (ar→hi, hi→th, th→ru, ko→ar, 74 prompts) — not linked here.
- A GPU-permitted environment (`uv run scripts/challenge/score.py`, ~7 min claimed).
- A precise definition of "distinct words" (case/whitespace rules) and how ties in the top-8 are resolved.

*Observations above are drawn only from the README snapshot and the three figures; I could open every image.*