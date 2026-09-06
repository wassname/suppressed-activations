# AGENTS.md

Inherit the user's global agent instructions. `README.md` is the public result.

## Required causal-demo layout

The README and notebook contain one continuous Spider-to-Dog demonstration. Do not split it
into separate “before”, “replacement”, “controls”, or “continuation” demonstrations. Do not
add Ant, translation, a dose grid, or generated follow-up text.

Use this order and wording shape:

```markdown
## Are suppressed activations causal? Can changing this subspace change the answer?

To see if this subspace allows causal replacement, we repeat the spider/dog demonstration
from Gurnee et al. using our suppressed-activation method.

Prompt: **Fact: The number of legs on the animal that spins webs is**

Readout: `['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB']`

Answer: **8**, the number of legs on a spider.

[clean top-10 token/log-p/probability table]

We replace this suppressed component with one extracted from:

Target prompt: **Fact: The number of legs on the animal that barks and is called man's best friend is**

Replacement readout: `['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']`

After applying it to the original prompt:

Prompt: **Fact: The number of legs on the animal that spins webs is**

Answer: **4**, the number of legs on a dog.

[intervened top-10 token/log-p/probability table]

For each complete prompt, an unmodified first pass extracts a separate subspace. We then
change one residual vector at L26 and the final source-prompt token:

[replacement pseudocode]

[one short limitations paragraph]
```

The dog rows are the replacement prompt's readout. They are not the source prompt's readout
after intervention. If the post-intervention readout is reported, label it separately; its
measured value is `[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']`.

Use the measured probabilities: clean `p(8)=0.882568`; after C=4,
`p(4)=0.490091` and `p(8)=0.297255`. Bold `8` in the first table and `4` in the
second.

Do not call C=4 a literal `spider → dog` token swap. C=1 is the constructed component
replacement and still answers 8. C=4 changes 72% of the residual norm; 21 of 256
matched-random interventions have an equal or larger effect; and a `2 + 2` target produces
the same answer change. The supported interpretation is a prompt-specific next-answer-state
intervention.

The source of truth is
`out/2026-09-05_211609_causal-confirmation/result.json`. The readable report is
`out/2026-09-05_211609_causal-confirmation/recovered_log.md`.

## Checks

Run `just notebook-smoke`, then queue `just notebook-run` through pueue for the GPU. Run
`just check` before pushing.

<!-- Written by PI/gpt-5.4 from Michael J. Clark's requested presentation. -->
