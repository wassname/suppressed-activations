# Fresh review of Spider→Ant strong doses

The reviewer read the script, persisted JSON, preregistration, and all 612 cleaned log lines without receiving the main agent's diagnosis.

> **No.** No tested Spider→Ant token-variant intervention made `6` the top next token. The cleaned log contains no `top= 6` row. Before obvious degradation, every stable rank-2 prototype still chose `8`; at strength `2.0`, output switched abruptly to `Spider`, with answer-token probabilities collapsing.

> Residual-norm restoration **helps numerically but not scientifically**: it prevents the extreme \(10^{-35}\)-scale annihilation of `p6`/`p8`, but does not extend the useful regime or produce a valid `6` answer.

The review identified two missing measurements:

> `Spider` is selected only at prompt position 13 [...] yet every strong prototype uses `all_positions` [...] across eight residual layers [...] so the `Spider` takeover may be distributed OOD damage rather than a failed localized concept swap.

> The operation symmetrically exchanges two pseudoinverse coordinates [...] it does not inherently point Spider→Ant. The run never reports pre/post Spider and Ant coordinates or Ant logits.

The reviewer suggested a dense C=1.50–2.00 next-token sweep at only the detected prompt position, with answer probabilities, output KL, perturbation size, and pre/post Spider and Ant coordinates. That test could distinguish a missed narrow transition from all-position corruption.

One proposed bug was checked and rejected after the review: Qwen3.5's final RMSNorm initializes `weight` to zero and multiplies by `1 + weight`, so the script's effective gain is correct for this model.

Scientific verdict:

> The artifacts support a **narrow negative result for this checkpoint, prompt, grid, and implementation** [...] They do **not** support a general mechanistic conclusion that Spider→Ant suppressed-coordinate steering cannot produce `6`.

Review by PI/reviewer (gpt-5.4); saved by PI/gpt-5.4.
