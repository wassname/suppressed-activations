## Review

### Scope and provenance

**Observation.** Repository-root `AGENTS.md` is absent: reading `/workspace/2026/suppressed-activations/AGENTS.md` returned `ENOENT`, and no applicable parent `AGENTS.md` was found. All other requested artifacts were read completely.

**Observation.** Job 130 ran:

- Command: `"uv run scripts/spider_ant_demo.py"`
- Working directory: `"/workspace/2026/suppressed-activations"`
- Start: `"2026-09-05T18:59:21.482394916+08:00"`
- End: `"2026-09-05T19:03:12.439627051+08:00"`
- Result: `"Success"`  
  (`slop/audits/job_130_status.json:2-6,96-102`)

The result records `"git_describe": "v0.1.1-36-ge715150"` (`data/spider_ant_demo.json:2-4`). Because the script invokes `git describe --always --dirty` (`scripts/spider_ant_demo.py:271-275`) and the description has no `-dirty` suffix, the worktree was recorded as clean. Current `main` resolves the matching prefix to full SHA:

`e71515050ba09c487fee290244a4cf969c13ff59`

Model: `"Qwen/Qwen3.5-4B"`; extraction layers `[23,25,32]`; intervention residual layers L23–L30.

**Full-log completeness.** `slop/audits/job_130_full.log` begins with successful fetch/load progress and the exact prompt tokens (`lines 1-6`), contains all preceding experiment output, and ends with all eight complete single-layer rows, L23 through L30 (`lines 645-652`). There is no traceback or truncation marker, and status independently reports success. The final newline is the only content after the L30 row.

---

## 1. Single-layer result

**Observation.** No L23–L30 single-layer intervention produced top token `6`, top `Spider`, or a collapsed next-token distribution. Every row remained:

- top token `8`
- `rank6 = 3`
- low KL from clean
- entropy between `0.5515177249908447` and `0.6807247996330261`

This exactly matches the preregistered repetition prediction: `"every one-layer row keeps a noncollapsed distribution; most remain top 8"`—in fact, all eight remained top `8` (`slop/research/20260905_spider_ant_single_layer_screen_predictions.md:9`).

| Residual layer | p6 | p8 | Δlog p6 | KL(clean‖after) | Entropy |
|---:|---:|---:|---:|---:|---:|
| 23 | 0.03012005053460598 | 0.880236804485321 | 0.12235498428344727 | 0.000274776917649433 | 0.5640539526939392 |
| 24 | 0.028870252892374992 | 0.8437123894691467 | 0.07997560501098633 | 0.00827344786375761 | 0.6651847958564758 |
| 25 | 0.028571562841534615 | 0.8349834680557251 | 0.06957578659057617 | 0.01283285766839981 | 0.6807247996330261 |
| **26** | **0.037240006029605865** | **0.8475787043571472** | **0.3345475196838379** | **0.0061715408228337765** | **0.6594594717025757** |
| 27 | 0.02648904360830784 | 0.8771966695785522 | -0.006104946136474609 | 0.0005415964988060296 | 0.5674562454223633 |
| 28 | 0.03013301081955433 | 0.8806156516075134 | 0.12278509140014648 | 0.0003503902116790414 | 0.5622231960296631 |
| 29 | 0.026665201410651207 | 0.8830302953720093 | 0.0005233287811279297 | 0.00009979943570215255 | 0.5565026998519897 |
| 30 | 0.026691846549510956 | 0.8839125037193298 | 0.001522064208984375 | 0.00015951035311445594 | 0.5515177249908447 |

Source: `data/spider_ant_demo.json:13001-13605`; corresponding complete log rows are `job_130_full.log:645-652`.

---

## 2. Strongest layer and scientific health

**Observation.** L26 is the strongest single layer for increasing p6:

- `p6 = 0.037240006029605865`
- `delta_logp6 = 0.3345475196838379`
- log-odds `6` versus `8` improve from clean `-3.5` to `-3.125`
- top remains `8` with `p8 = 0.8475787043571472`
- `rank6 = 3`
- `KL = 0.0061715408228337765`
- `entropy = 0.6594594717025757`
- perturbation norm `3.356153726577759` against residual norm `25.363208770751953`  
  (`data/spider_ant_demo.json:13236-13308`, especially `13291-13307`)

**Inference.** L26 is **distributionally healthy**: it does not collapse, and its KL is small. It is **not yet scientifically established as Ant steering**. This is one prompt, one deterministic direction, one extrapolated strength, no matched random/null condition, and no top-`6` generation. The preregistration explicitly says the screen `"cannot by itself establish causal Ant steering without a matched random condition and coherent generation"` (`slop/research/...predictions.md:13`).

---

## 3. Does this support repeated application as the collapse cause?

**Observation.**

- Every one-layer C=2 row is healthy and top `8`.
- The same C=2 operation across L23–L30 yields top `Spider`, `rank6 = 248274`, `p6 = 1.1769110281448947e-34`, `KL = 76.46316528320312`, and entropy `5.839451091560477e-07` (`data/spider_ant_demo.json:11097-11103`).
- Its coordinates and norms explode through the stack. By L30, residual norm is `166.37449645996094` and perturbation norm is `646.3381958007812` (`data/spider_ant_demo.json:11168-11175`).
- In contrast, L30 alone has residual norm `45.771087646484375`, perturbation norm `6.31770133972168`, and remains top `8`.

**Inference.** Yes—this is strong evidence that repeated/composed application, rather than any independently unstable L23–L30 layer, causes the multi-layer Spider collapse. It does not distinguish pure repeated-operator amplification from amplification plus intervening transformer dynamics; a cumulative layer-count ablation would locate that transition.

---

## 4. Likely bugs or misconceptions

- **Finding: P1 — C=2 is an unstable over-relaxation, not “twice an exact swap.”**  
  `coordinate_swap` computes `h + strength * (swap(h) - h)` (`scripts/spider_ant_demo.py:32-36`). For source/target dual coordinates `(s,t)`, C=2 gives `(2t-s, 2s-t)`, so:
  
  `d_after = (source_after-target_after) = -3*(source_before-target_before)`.
  
  Every application reverses and triples the antisymmetric coordinate. Without intervening dynamics, eight repetitions imply gain `3^8 = 6561`. The observed alternating coordinate explosion is therefore expected operator behavior, not evidence of a Spider-specific causal feature.

- **Finding: P1 — “Spider collapse” describes the first-token distribution, not necessarily collapsed generated text.**  
  Hooks explicitly return unchanged output whenever `hidden.shape[1] == 1` (`scripts/spider_ant_demo.py:43-47`), so cached autoregressive decoding is not continuously intervened upon. The generated continuations can remain coherent after the forced first token. Any claim of whole-sequence collapse must state this prefill-only behavior.

- **Finding: P2 — p6 is indirect evidence for Ant semantics.**  
  The swapped directions represent Spider/Ant token prototypes, while the endpoint metric is the unrelated output token `6`. A p6 increase alone may reflect generic digit-logit movement rather than a Spider→Ant concept substitution.

- **Finding: P2 — the reported geometry does not condition-check the actual mean-atomic two-vector basis.**  
  The stored condition numbers, `2030.85107421875` raw and `1403.467529296875` unit, are computed over all eight matched token vectors (`scripts/spider_ant_demo.py:260-267`; `data/...json:13621-13644`). The intervention instead uses the two-vector `mean_atomic` prototype. Its Gram matrix, cosine, singular values, and pseudoinverse condition number should be reported directly.

- **Finding: P2 — metric resolution is limited by bfloat16 logits.**  
  The many exact `0.125`-spaced log-odds readings indicate substantial quantization. L26’s `+0.375` log-odds shift is visible, but very small differences such as L29/L30 should not be interpreted finely without float32 output projection/logits.

- **Finding: P2 — “scientifically healthy” needs controls, not merely low KL.**  
  KL and entropy establish noncollapse, but no random-direction baseline, alternate prompts, sign reversal, or replication establishes specificity.

---

## 5. Cheapest next test

**Recommendation.** Run a no-generation cumulative layer-count ablation at C=2, adding hooks in order:

`{L23}`, `{L23,L24}`, …, `{L23,…,L30}`.

Only seven new prefill forwards are needed because the one-layer and eight-layer endpoints already exist. Record top token, rank6, p6/p8, KL, entropy, residual/perturbation norms, and:

`r = (source_after-target_after)/(source_before-target_before)`.

**Explicit expected readings:**

1. At every C=2 hook, `r` should equal approximately `-3.0`; failure indicates an implementation or coordinate-recording error.
2. The L23 endpoint should reproduce:
   - top `8`
   - `rank6 = 3`
   - `p6 = 0.03012005053460598`
   - `KL = 0.000274776917649433`
   - entropy `0.5640539526939392`
3. The full L23–L30 endpoint should reproduce:
   - top `Spider`
   - `rank6 = 248274`
   - `p6 = 1.1769110281448947e-34`
   - `KL = 76.46316528320312`
   - entropy `5.839451091560477e-07`
4. If repetition is causal, increasing hook count will reveal an intermediate threshold where alternating coordinate magnitude, perturbation/residual ratio, and KL rise sharply before the Spider takeover. If no cumulative configuration reproduces that progression, reject the repetition-only explanation.

After that mechanism check, the next scientific test should be an L26-only dose/sign sweep with norm-matched random directions.

## Merge verdict

**OK with notes.** The job completed successfully and the single-layer evidence is internally consistent. The main caution is that C=2 implements an algebraically amplifying over-relaxation, so the multi-layer collapse should not be interpreted as successful Ant steering.

Reviewed by PI/reviewer (gpt-5.4).