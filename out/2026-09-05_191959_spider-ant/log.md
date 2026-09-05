# Spider→Ant rank and position screen

- pueue job: 132
- source revision recorded at artifact write: `v0.1.1-39-g9b8f0d1`
- model: `Qwen/Qwen3.5-4B`
- prompt: `Fact: The number of legs on the animal that spins webs is `
- extraction: L23→L25→L32
- intervention: L26 only
- full records: [`result.json`](result.json)
- full process output: [`pueue.log`](pueue.log)

## Readout

```text
[thoughts before: 丝绸, -web, Web, Disc, 的战, Spider, web, WEB]
```

## Primary condition: lowercase-space rank 8, final position, norm restored

C=1 is the exact coordinate swap. C>1 extrapolates beyond it.

| C | top | p(6) | p(8) | log p(6)/p(8) | KL from clean | entropy |
|---:|---:|---:|---:|---:|---:|---:|
| -4 | 8 | .0277 | .9176 | -3.500 | .0165 | .4380 |
| -2 | 8 | .0242 | .9073 | -3.625 | .0060 | .4803 |
| -1 | 8 | .0241 | .9056 | -3.625 | .0038 | .4796 |
| 0 | 8 | .0267 | .8826 | -3.500 | .0000 | .5579 |
| .5 | 8 | .0267 | .8838 | -3.500 | .0001 | .5509 |
| 1 | 8 | .0296 | .8656 | -3.375 | .0021 | .6023 |
| 2 | 8 | .0368 | .8370 | -3.125 | .0098 | .6877 |
| 4 | 8 | .0547 | .7554 | -2.625 | .0587 | .8648 |
| 8 | 8 | .2295 | .3339 | -.375 | .6724 | 1.4562 |
| 12 | **6** | **.3440** | .1434 | **+.875** | 1.3982 | 1.6692 |
| 16 | 2 | .2027 | .1230 | +.500 | 1.5495 | 2.0117 |
| 20 | Web | .0035 | .0031 | +.125 | 5.2288 | .2318 |
| 24 | Web | .0001 | .0001 | .000 | 8.4405 | .0414 |

At C=12 the target changed from `8` to `6`. The targeted change exceeded 30 of 32 matched random rotations. The preregistered requirement was 31 of 32, so this does not establish a specific Spider→Ant effect.

## Rank and position diagnostics

| condition | first stable top-6 row | p(6) | p(8) | KL | entropy |
|---|---|---:|---:|---:|---:|
| mean rank 8, final | restored C=12 | .4321 | .1801 | 1.2090 | 1.3934 |
| lowercase rank 8, final | restored C=12 | .3440 | .1434 | 1.3982 | 1.6692 |
| lowercase rank 16, final | restored C=8 | **.6147** | .0572 | 2.2609 | 1.4454 |
| lowercase rank 32, final | none | — | — | — | — |
| lowercase rank 64, final | restored C=8 | .3585 | .0229 | 3.1140 | 3.1981 |
| mean/lowercase rank 8, preceding ` is` position | none | — | — | — | — |

The effect is specific to the final trailing-space position in this prompt. Increasing rank is not monotonic: rank 16 works at a lower dose, rank 32 does not, and rank 64 changes the broader distribution more.

## Exact 64-token continuation

All ten targeted rows whose first token changed to `6` produced the same 64 token IDs and decoded text:

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

The hook acts on the prompt pass only. This continuation is therefore conditioned on the changed first token `6`; it is not independent evidence that the model represented an ant.

## Decision

The run found several stable `8→6` first-token changes, including lowercase rank 16 at C=8. The preregistered rank-8 primary missed its matched-random requirement by one control. A focused confirmation must compare rank 16 C=8 against matched controls and an unrelated prompt whose clean answer is also `8`.

Written by PI/gpt-5.4.
