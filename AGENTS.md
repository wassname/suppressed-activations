# AGENTS.md

Inherit the user's global agent instructions. `README.md` is the public result. Keep its
story shorter than the implementation history.

## Causal demonstration

The README and notebook contain one demonstration: spider source prompt to dog target
prompt on Qwen3.5-4B. Do not add Ant, translation, long-generation, or repeated-layer
demonstrations to this section.

Use the measured contents below:

- source prompt: `Fact: The number of legs on the animal that spins webs is `
- source suppressed readout: `丝绸, -web, Web, Disc, 的战, Spider, web, WEB`
- clean top answer: `8`, with `p=0.882568`
- target prompt: `Fact: The number of legs on the animal that barks and is called man's best friend is `
- target suppressed readout: `吠, собаки, 狗粮, dog, Dog, Dog, สุนัข, canine`
- operation: replace the source rank-8 projection with the norm-matched target projection
  at residual L26 and the final source-prompt token
- `C=1`: constructed replacement; top answer remains `8`
- `C=4`: selected extrapolation; top answer is `4`, with `p(4)=0.490091` and
  `p(8)=0.297255`
- source readout re-extracted after C=4: `Silk, Spider, spiders, 丝绸, silk, -web, spider, Spider`

Show two top-10 next-token tables, before and after. Bold `8` before and `4` after. The
notebook must reproduce the same continuous demonstration and must not generate a different
follow-up prompt.

Do not describe C=4 as a literal `spider → dog` token swap. It changes 72% of the residual
norm; 21 of 256 matched-random interventions have an equal or larger effect; and a `2 + 2`
target prompt produces the same answer change. The supported interpretation is a
prompt-specific next-answer-state intervention, not transferred dog identity.

The source of truth is
`out/2026-09-05_211609_causal-confirmation/result.json`. The readable report is
`out/2026-09-05_211609_causal-confirmation/recovered_log.md`.

## Checks

Run `just notebook-smoke`, then queue `just notebook-run` through pueue for the GPU. Run
`just check` before pushing.

<!-- Written by PI/gpt-5.4 from Michael J. Clark's requested presentation. -->
