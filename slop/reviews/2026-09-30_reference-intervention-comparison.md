# Reference comparison: same-pass concept interventions

**Result:** The readout transport and block indexing agree with the supplied reference. The four runs instead test **fixed additive donor contrasts**, not the paper’s activation-dependent coordinate swap. They demonstrate answer/readout movement, but not coherent, transferable concept replacement. The strongest immediate concern is excessive, asymmetric concept injection at every decode position.

Read-only review; no commands, model inference, edits, network access, or additional delegation. Applicable instructions and ml-debug E/F were read. This is not goal sign-off.

## Reference comparison

Paths below are relative to `/workspace/2026/suppressed-activations/`. `P` denotes `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`; `R` denotes `.local/reference/jacobian-lens/`; `S` denotes `scripts/english/08_jlens_one_pass.py`.

| Feature | Published/reference evidence | Current implementation | Assessment |
|---|---|---|---|
| Transport | `R/jlens/lens.py:135–143`: “`return residual @ J_bar.T`” | `S:240–242`, same transpose, then norm/head | Matches |
| Hook boundary | `R/jlens/hooks.py:46–55` records block **outputs** | `S:228`, `scripts/demo.py:60–80`; block15 corresponds to residual16 | No observed off-by-one |
| Normalization | `R/jlens/hf.py:166–174` casts to model dtype and applies final norm/head | `S:230,474–477`: effective rows use `W*(1+norm.weight)`, then J; coordinate directions are unit-normalized | Readout matches; gain convention depends on Qwen implementation, not verified against model-library source here |
| Coordinate swap | `P:220`: \(c=V^\dagger h;\ h'=h+V(\sigma(c)-c)\) | `S:47–49` implements this equation | Algebra matches, but unit-column normalization is an additional choice not specified there |
| Raw-score swap | Not the writing equation in `P:220` | `S:52–54`: swaps \(V^\top h\) using the dual basis | Different operation; these are unnormalized numerators, not normalized lens logits |
| Donor intervention | `P:256,358`: broader concept/probe datasets and sparse nonnegative gradient pursuit, \(k=16/25\) | `S:136–165,482–502,530`: four means, two-token span projection, fixed addition | Not that decomposition or coordinate replacement |
| Layer/position coverage | `P:318`: “at all token positions”; `P:380`: “across a band of intermediate layers” | All four logs: block15, final prompt position, every cached decode | Material difference, not a faithful causal replication |
| Lens corpus | `R/README.md:18–23`: summed target cotangents, averaged source positions; `R/jlens/examples.py:42–60`: first qualifying WikiText-103 train records | `S:30–32,222–226`: pinned n1000 artifact and SHA | Generic preparation; exact fit corpus/settings not established by dimensions/count |
| Target layer | `P:1187–1189`: default Sonnet lens uses **penultimate** residual; `P:1244–1263` pseudocode describes target/default-final variant | Reference readout describes final-layer transport | Paper itself describes multiple recipes; do not silently equate them |
| Model identity | `P:222`: default Sonnet4.5; other Anthropic models corroborate | Logs: Qwen3.5-4B@`851bf6e…` | No basis to assume Anthropic causal results replicate |
| Tokenization | `R/jlens/hf.py:101–110,157–161` optionally forces BOS and uses tokenizer defaults | `S:514` uses `add_special_tokens=False` | Possible mismatch; actual Qwen BOS effect untested |
| Evaluation | `P:346,388`: top-1 implied-answer success across prompts/functions | `S:570–587`: first-token odds, answer mass, repetition, saved continuation | Better continuation visibility, but only selected development examples |

The supplied official files expose fitting/application/visualization support, not an executable implementation of the published causal experiment. Therefore, normalization, clamping semantics, and exact causal layer ranges cannot be recovered from these files alone. Also, `P:1416` explicitly says animal swaps succeed “rarely” at strength1—even within the paper’s own model setting.

## What the runs show

Each directory is `out/2026-09-30_<time>_jlens-one-pass/`. Complete `run.md` and `interventions.json` were read.

| Run | Condition | Observed result against Base/control |
|---|---|---|
| 132714 | Noun donor, dog→spider, projected | Target \(p(8)\): .0072→.2859, but **6** wins (.6053); random \(p(8)=.00785\) |
| 132742 | Noun donor, skeleton transfer | Projected and full contrasts leave inside/outside log odds essentially unchanged; random shifts them +.5 nats |
| 133833 | Pronoun donor, spider→dog | Projected generates **6**, not4. Full generates4, \(p(4)=.4699\) versus Base .0564/random .0801, but repeats the question; \(r_2=.3548\) versus Base .0323 |
| 133853 | Pronoun donor, dog→spider | Projected generates8, \(p(8)=.6420\), but continues “How many legs does the spider that lives in the web of the spider's home is there?” Full remains4 |

These are single selected prompts per configuration, with one random direction—not estimated success rates. Low repetition does not establish grammatical or conceptual coherence: 133853’s malformed sentence has \(r_2=.0323\).

All logs’ SHOULD asks for coherent target movement exceeding random. None establishes the complete claim. The skeleton result concerns the **older donor**; no supplied pronoun-donor skeleton result supports or refutes its transfer.

## Findings and falsifiable concerns

### 1. Fixed addition is strongly asymmetric, not calibrated replacement

`S:530` says:

> `edited = selected + donor_deltas[mode]`

At 133833’s first projected edit, raw `[spiders,dogs]` scores change from `[1.3247,2.0152]` to `[-12.8609,2.8137]` (`interventions.json:778–795`). This predominantly suppresses spider; it barely increases dog. Reverse editing gives `[1.0665,1.4813]→[15.2521,.6809]` (`133853/interventions.json:783–796`). Its applied delta is **70.5%** of the residual norm.

Observed: the hook applies the intended large delta; bf16 application does not erase it.  
Inference: oversuppression/overinjection plausibly explains asymmetric answers and degraded continuation. It is not proof that the J directions lack causal meaning.

**Disproof:** locally calibrated, substantially smaller edits still produce the same asymmetric failure, or removing decode injection leaves the same malformed continuation.

### 2. Same-token donors remove one confound, not all lexical/context effects

`data/dog_spider_donors_pronoun_v2.json:5` claims the common final pronoun “cancels the direct current-token embedding difference.” That is a useful control. It does **not** cancel attention to the earlier animal name, contextual nonlinearities, or template-dependent activation differences. `S:147` takes a raw final-position residual, without centering/whitening or independent donor validation.

Moreover, projection into the two chosen token directions is not the paper’s sparse J-space decomposition. Calling it “J-projected donor contrast” is accurate; calling it full J-space replacement would not be.

### 3. Missing local semantic measurement

The editor acts at block15; displayed readouts are block23. In 133833 Base, block15 raw dog score already exceeds spider, despite block23’s spider-leading readout. Thus downstream readout cannot establish that a symmetric local swap exchanges the intended active feature at the edited layer. Log both pseudoinverse coordinates and normalized local readout before/after; raw scores alone do not distinguish direction norm from loading.

### 4. Information-boundary compliance is narrower than “one run”

For these donor conditions, the edit uses only offline constants and current hook state. Base is separately generated for evaluation; its logits do not determine the edit. The later observer does not feed back. Generic donor extraction legitimately runs full trajectories offline.

By contrast, `scripts/demo.py:307–308` explicitly extracts current source and target trajectories; its standalone demo is not compliant. End-pass masks in S are likewise not admissible earlier-edit inputs, but are not used here.

## Highest-information next test

Repeat **133853 unchanged except `decode_scale=0`**, retaining Base and matched-random controls. This is a diagnostic prompt-only control, not the final continuous-steering solution.

Predictions:

- **Decode overinjection:** first-token probabilities remain unchanged, but grammar improves and persistent spider repetition decreases.
- **Damaged prefill/wrong representation:** first-token probabilities remain unchanged, yet continuation remains malformed or reverts conceptually.
- **Implementation bug:** first-token probabilities change despite identical prefill, or logged decode deltas remain nonzero.

This isolates one factor cheaply before adding layers, templates, or strength searches. Log exact continuation, coverage, applied norms, and local coordinates. Nothing was executed or queued.

Provenance: job records report Success and source commits `4fc70e4`/`3baa28a`; the supervisor attested snapshot equality. I read the older unique source snapshot and current script, not independently recomputed hashes. Lens-fitting model revision, seed spread, held-out transfer, and peak GPU memory remain unavailable.

— PI/OpenAI