---
experiment: country-coordinate-swap
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
block_index: 15
readout_block_index: 23
prompt_slice: "-1:"
continuous: true
strength: 1
max_new_tokens: 32
seed: 0
---
# One country pair, two properties

-- PI/OpenAI

SHOULD: correct Rome/euro Base answers become coherent Tokyo/yen under the SAME raw-coordinate rule, with greater target-directed bare-answer log odds than random on both. Initial text and numeric comparisons below are not a semantic verdict. An article can obscure first-token answer movement. Wrong Base invalidates the assay; do not replace prompts or promote a control. Inspect complete32-token continuations and source-country disclosure. No sparse decomposition or clean-pass clamp. Random matches the primary proposal norm on its own state; later doses differ. One selected pair, two dependent properties, five conditions each, no tuning. The prior trailing-space currency prompt failed; these exact no-space prompts were fixed before this run. Each property has one clean-target prefill AFTER its conditions, with no feedback to editing. Pinned source/helpers and full local tensors are saved; unmodified source/target passes never prepare the editor.

| condition                                                                                                           |   answer log-odds shift | expected   | initial text (not judged)   |   bare-answer mass |      r2 |   tokens |
|:--------------------------------------------------------------------------------------------------------------------|------------------------:|:-----------|:----------------------------|-------------------:|--------:|---------:|
| [capital: Base](../2026-10-01_001715_jlens-one-pass/base/run.md)                                                    |                -0.00000 | Rome       | ' Rome.'                    |            0.51495 | 0.06452 |       32 |
| [capital: raw J-coordinate exchange](../2026-10-01_001715_jlens-one-pass/raw-j-coordinate-exchange/run.md)          |                 0.06250 | Tokyo      | ' Rome.'                    |            0.51190 | 0.06452 |       32 |
| [capital: unit J-coordinate exchange](../2026-10-01_001715_jlens-one-pass/unit-j-coordinate-exchange/run.md)        |                 0.06250 | Tokyo      | ' Rome.'                    |            0.51240 | 0.06452 |       32 |
| [capital: raw plain-coordinate exchange](../2026-10-01_001715_jlens-one-pass/raw-plain-coordinate-exchange/run.md)  |                 0.12500 | Tokyo      | ' Rome.'                    |            0.50443 | 0.06452 |       32 |
| [capital: matched-random delta](../2026-10-01_001715_jlens-one-pass/matched-random-delta/run.md)                    |                -0.06250 | control    | ' Rome.'                    |            0.51217 | 0.06452 |       32 |
| [currency: Base](../2026-10-01_001732_jlens-one-pass/base/run.md)                                                   |                 0.00000 | euro       | ' the Euro.'                |            0.00141 | 0.03226 |       32 |
| [currency: raw J-coordinate exchange](../2026-10-01_001732_jlens-one-pass/raw-j-coordinate-exchange/run.md)         |                 0.25000 | yen        | ' the Euro.'                |            0.00126 | 0.03226 |       32 |
| [currency: unit J-coordinate exchange](../2026-10-01_001732_jlens-one-pass/unit-j-coordinate-exchange/run.md)       |                 0.18750 | yen        | ' the Euro.'                |            0.00134 | 0.03226 |       32 |
| [currency: raw plain-coordinate exchange](../2026-10-01_001732_jlens-one-pass/raw-plain-coordinate-exchange/run.md) |                 0.00000 | yen        | ' the Euro.'                |            0.00141 | 0.03226 |       32 |
| [currency: matched-random delta](../2026-10-01_001732_jlens-one-pass/matched-random-delta/run.md)                   |                 0.00000 | control    | ' the Euro.'                |            0.00142 | 0.03226 |       32 |
