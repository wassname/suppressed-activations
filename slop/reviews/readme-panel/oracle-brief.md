# Oracle brief: review the README and the challenge concept

Repository: `/workspace/2026/suppressed-activations` (read-only). Please answer in about one page.

## What the author wants

The author's words, from the README "The challenge" section:

> In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors.

> Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

And from AGENTS.md: "having english thoughts is the eval not the training". The goal is a method that finds what a model thinks but does not say, including in settings where input, thought and output are all English. Translation, where English is the thought and other languages are input and output, is only the labelled scoreboard. The author wants to share this as a challenge with a leaderboard.

## Files

- `README.md`: the top ~60 lines are current (title, challenge, leaderboard). Everything from "## Current one-pass tests (2026-09-30)" down is older material, not yet cleaned up.
- `scripts/challenge/score.py`, `scripts/challenge/transforms.py`, `scripts/challenge/common.py`: the leaderboard code (~430 lines).
- `out/2026-10-03_194108_leaderboard/leaderboard.md`: the current table.

## Observations

- Translation prompts: 4-shot word translation between Russian, Korean, Arabic, Hindi and Thai (input and output), Qwen3.5-4B. English and Chinese count as hidden. Words come from MUSE bilingual dictionaries; 20 prompts per pair; settings chosen on ru→ko; 74 test prompts.
- A first headline, "share of the top 8 words in Latin or Han script", gave a random rank-256 subspace 0.77 and the best method 0.96, because random readouts list unrelated real Chinese words. The headline was then changed to "found": the English word or its Chinese translation is in the top 8, and none of the 8 is in the input or output script or is the model's next token. Random then scores 0.18, a prompt-independent fixed list 0.00, the best row 0.93.
- On 36 English-only two-hop questions (TwoHopFact), every transform scores about 0 on finding the bridge entity.
- Best rows use a lens or per-prompt vocabulary scores (marked ★). The best fixed subspace without a lens uses rank 1024 of 2560 dimensions.

## Questions

1. Is the challenge well posed? Can "found" be gamed, or does it reward something other than reading unsaid thoughts? Is it circular in any way?
2. Does success on translation plausibly transfer to the all-English setting the author cares about? If not, what would make it transfer?
3. What should the README say, and in what order, for a new reader to understand and enter the challenge? What should be cut?
4. What is the most important missing control, baseline, or related work?

Separate what you verified in the files from your opinion. Sign with your model name.
