# AGENTS.md

Inherit the user's global agent instructions. `README.md` is the public result.

## Required causal-demo layout

Show one experiment as two complete, directly comparable conditions: `Base` and `Causal
intervention`. Each condition must show the same fields in the same order:

1. the exact input string as Python `repr`, including its trailing space;
2. the suppressed readout, presented as “what it is thinking but not saying”;
3. the exact next 32 generated tokens, verbatim;
4. the top-10 next-token table with token, log probability, and probability; the causal table also shows change in log probability from Base.

The public section must follow this template:

```markdown
## Are suppressed activations causal? Can changing this subspace change the answer?

To see if this subspace allows causal replacement, we repeat the spider/dog demonstration
from Gurnee et al. using our suppressed-activation method.

### Base

Input (`repr`, including the trailing space):

'Fact: The number of legs on the animal that spins webs is '

Readout (“what it is thinking but not saying”):

['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB']

Generation (next 32 tokens, verbatim):

8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:

[clean top-10 token/log-p/probability table]

### Causal intervention

Now we replace the suppressed component selected from the spider prompt with the component selected from a dog prompt. The input stays unchanged. The readout below is recomputed after the intervention.

Input (`repr`, unchanged):

'Fact: The number of legs on the animal that spins webs is '

Readout after intervention (“what it is thinking but not saying”):

[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']

Generation (next 32 tokens, verbatim):

4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process

[intervened top-10 token/log-p/probability/change-in-log-p table]

[target-input provenance, replacement pseudocode, and one short limitations paragraph]
```

Use fenced text blocks for the exact input and generation strings. These are model strings,
not explanations written by an agent. Keep the two 32-token generations byte-for-byte as
decoded by the pinned tokenizer. Do not replace them with a next-token label or a gloss such
as “the number of legs on a dog.”

The causal readout is the source input's detector output after intervention, not the dog
prompt's readout. The dog component comes from
`"Fact: The number of legs on the animal that barks and is called man's best friend is "`.

Use the measured probabilities: clean `p(8)=0.882568`; after C=4,
`p(4)=0.490091` and `p(8)=0.297255`. Bold expected `8` in the first table and `4`
in the second. Italicize alternative `4` in the first table and `8` in the second.

Do not add Ant, translation, a dose grid, or another generated prompt. Do not call C=4 a
literal `spider → dog` token swap. C=1 is the constructed component replacement and still
generates 8 first. C=4 changes 72% of the residual norm; 21 of 256 matched-random
interventions have an equal or larger effect; and a `2 + 2` target produces the same
first-token change.

The source of truth is
`out/2026-09-05_211609_causal-confirmation/result.json`. The readable report is
`out/2026-09-05_211609_causal-confirmation/recovered_log.md`.

## Intervention sweep metrics

Use the spider answer token `8` as $A_0$, the dog answer token `4` as $A_1$, clean
inference as $C_0$, and component replacement as $C_1$. Rank answer movement with:

$$
S_{\mathrm{swap}}
= \left[\log p(A_1 \mid C_1)-\log p(A_0 \mid C_1)\right]
- \left[\log p(A_1 \mid C_0)-\log p(A_0 \mid C_0)\right].
$$

The equivalent four-term form is:

$$
S_{\mathrm{swap}}
= \log p(A_0 \mid C_0)-\log p(A_1 \mid C_0)
-\log p(A_0 \mid C_1)+\log p(A_1 \mid C_1).
$$

Positive values mean movement from `8` toward `4`. This is a difference in log odds, in
nats. Call it `swap_log_odds_shift` in code and logs.

Report two coherence diagnostics separately. Name the first `bare_answer_mass`:

$$p_{\mathrm{valid}} = p(4)+p(8)$$

and

$$r_2 = 1 - \frac{\text{unique generated bigrams}}{\text{generated bigrams}}.$$

Compute $r_2$ on generated non-special token IDs. Define it as zero when there are fewer
than two such tokens. Low $p_{\mathrm{valid}}$ indicates that next-token probability moved
away from both bare answer tokens. It does not by itself show incoherence because a coherent
response can start with formatting or prose and state the answer later. High $r_2$ indicates
a repetitive continuation. Do not use a repetition logits processor as a metric because it
changes the distribution being measured.

## Intervention sweep design

Steering starts at prompt slice `-3:` (the final three prompt tokens) and continues
through every generated token by default. For a 32-token continuation this means one
prefill and 31 cached decode calls. Log and assert coverage. Label any deliberate
prompt-only control explicitly. Report the expected answer beside the observed answer:
spider Base is `8`, dog target is `4`, ant target is `6`. A matching digit alone is not
coherent concept replacement. Label prefill and final-decode readouts separately.

<!-- Written by Codex/GPT-6 from wassname's continuous-steering correction. -->

Use one-at-a-time sweeps. State one default for every axis from prior evidence. Vary one
axis while all other axes remain at those defaults. Include the default row once and identify
it in the results table. Do not select a different default separately for each axis.

Every condition writes a unique `run.md` with YAML frontmatter. It must contain the resolved
config, $S_{\mathrm{swap}}$, $p_{\mathrm{valid}}$, $r_2$, the exact input and suppressed
readout, the top-10 next-token table, and the exact generated continuation capped at 32 tokens.
State the actual token count if EOS stops generation early. The sweep root `run.md` contains
the cross-condition table and links each row to its condition log. `just results` rebuilds
that table from condition `run.md` frontmatter.

<!-- Written by Codex/gpt-5.6-sol from wassname's metric specification. -->

## Checks

Run `just notebook-smoke`, then queue `just notebook-run` through pueue for the GPU. Run
`just check` before pushing.

<!-- Written by PI/gpt-5.4 from Michael J. Clark's requested presentation. -->
