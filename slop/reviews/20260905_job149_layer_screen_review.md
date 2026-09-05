# Job 149 — rank-8 single-site layer-screen review

## Review

### Correct

- Job 149 completed successfully using `uv run scripts/spider_ant_demo.py` at source revision `v0.1.1-57-g46c007a` (`slop/audits/job_149_full.log:1-9`; `job_149_status.json`).
- The screen followed the preregistered discovery design: rank 8, residual layers 23–30, strengths `{1,2,4,8}`, last prompt token only, residual-norm restoration, and first-token scoring without rank-8 random controls or generation (`scripts/spider_ant_demo.py:45-57,188-214,427-483`; `slop/research/20260905_rank8_single_site_sample_predictions.md:3-14`).
- **Yes: residual layer 26 yields distinct Ant→6 and Dog→4 crossings.** More strongly, both occur at the same fixed dose, `C=4`, in separate single-site interventions:
  
  | Target component | Layer | C | Top | Relevant probabilities | Digit mass | Entropy | Distance |
  |---|---:|---:|---:|---|---:|---:|---:|
  | Ant | 26 | 4 | **6** | p6=.4871, p8=.3794, p4=.0453 | .9981 | 1.2107 | 17.2234 |
  | Dog | 26 | 4 | **4** | p4=.4901, p8=.2973, p6=.0965 | .9981 | 1.3999 | 18.2703 |

  Evidence: `result.json:7083-7166,9895-9978`.

- Layer 24 is a second, weaker shared-layer result only if target-specific doses are allowed:

  | Target component | Layer | C | Top | Relevant probabilities | Digit mass | Entropy | Distance |
  |---|---:|---:|---:|---|---:|---:|---:|
  | Ant | 24 | 4 | **6** | p6=.8859, p8=.0268 | .9976 | .5768 | 17.2965 |
  | Dog | 24 | 2 | **4** | p4=.5329, p8=.3662, p6=.0496 | .9980 | 1.1037 | 10.5300 |

  Evidence: `result.json:6403-6486,9130-9213`.

- Layer 26 is therefore the best confirmation candidate: it shares both layer and dose and has reasonably similar Ant/Dog distances. Layer 24 requires different doses and is unstable: Dog changes from top-4 at `C=2` to top-6 at `C=4` and `C=8` (`result.json:9215-9383`).

### Interpretation of entropy, digit mass, and distance

- Digit mass remains approximately **99.8%** for all four quoted rows. These crossings are not caused by probability escaping into arbitrary vocabulary. The increased L26 entropy is principally redistribution among digits.
- Relative to the clean Spider entropy `.5579`, the L26 rows are less decisive: Ant entropy is `1.2107` and Dog entropy is `1.3999`. Ant’s crossing is particularly narrow—only `.25` nats over `8`—while Dog is `.50` nats over `8`.
- The L26 perturbations are large despite norm restoration: `17.2234/25.3632 = 67.9%` and `18.2703/25.3632 = 72.0%` of the clean residual norm. Their distances differ by `1.0468`, about 6.1% of their mean. They are comparable, not exactly distance-matched.
- The effects require extrapolation: `C=1` leaves both targets at `8`; the shared crossing appears at `C=4`. This should be described as a strong, norm-restored sample-component extrapolation, not literal one-for-one replacement.

### Findings

- **Finding: P1 — this is discovery evidence, not an independent confirmation.**  
  The shared layer and dose were selected after inspecting 64 target/layer/dose rows. The research note explicitly reserved random controls and generation until after this screen. A public result therefore needs a new run frozen at L26/C4, with no fallback to L24 or another dose.

- **Finding: P1 — existing controls and generations do not test the rank-8 result.**  
  The 32 random controls, byte negative control, and displayed Spider generations belong to the separate rank-16 projected token-pair intervention at L26/C8. The rank-8 loop records logits only. They cannot be cited as controls or generations for the L26/C4 sample-component crossing (`scripts/spider_ant_demo.py:427-507`; `out/2026-09-05_205347_spider-ant/log.md`, “Rank-8 single-site sample-component screen”).

- **Finding: P1 — animal identity is confounded with direct answer-state transfer.**  
  Each operation uses a separately extracted full target-prompt basis and the target prompt’s final-token hidden state. Those target prompts already cleanly answer `6` or `4`. Thus the result can reflect transfer of a number/completion state, lexical prompt state, or animal semantics; it does not isolate a shared “Spider→Ant/Dog” representation. “Shared” currently means only the residual layer/site—and at L26 the dose—not a shared direction or operator.

- **Finding: P2 — target-basis diagnostics are asymmetric.**  
  Dog’s selected tokens are recognizably dog-related, while Ant’s are `;font, _unix, Kate, ...`, with no clear ant semantics. These should be labeled basis diagnostics, not “thoughts,” and included as a caveat (`result.json:5801-5865`; `log.md`, rank-8 readout).

- **Finding: P2 — reproducibility metadata is incomplete.**  
  The Git source is recorded, but `model_revision` is `null`. A public run must pin and record the exact Hugging Face model and tokenizer commit hashes (`result.json:1-52`).

## Exact fixed confirmation run

Use a dedicated confirmation path; do not rerun the layer/dose search and then select again.

### Frozen primary conditions

- Model: `Qwen/Qwen3.5-4B`, exact pinned model and tokenizer revisions.
- Precision/evaluation: bf16, CUDA, `eval()`, gradients disabled.
- Source and Ant/Dog target prompts: exactly those in job 149.
- Extraction: early/peak/output residual layers `23/25/32`; rank `8`; normalized unembedding rows.
- Intervention: residual layer **26** only, final source-prompt token only, norm restoration enabled.
- Strength: **C=4 only**.
- Conditions: clean, Ant component, Dog component. Retain `C=0` and `C=1` as sham/direct-replacement controls, not alternate candidates.
- Never fall back to another layer, dose, prompt, or random seed based on results.

### Required controls

1. **Matched random rotations:** 256 preregistered seeds `0…255` for each target. Compute distance from the actual Ant or Dog L26/C4 sample patch, then match that exact distance at the same token and layer.
2. **Byte source negative control:** apply the analogous frozen Ant and Dog sample interventions to the existing byte prompt. If these also produce 6 and 4, the effect is generic answer transfer.
3. **Answer-only targets:** extract rank-8 components from fixed prompts  
   - `Fact: The result of adding three and three is `  
   - `Fact: The result of adding two and two is `  
   and apply them to Spider at L26/C4. This directly tests the number-state confound.
4. **Position control:** apply each same-distance perturbation at the penultimate source token.
5. Report all controls regardless of outcome; do not replace failed controls post hoc.

### Required readouts

For every primary and control condition, save:

- top-20 vocabulary tokens and all ten digit probabilities;
- expected-token rank and top-1 label;
- `p(expected)`, `p(8)`, `p(other target digit)`;
- log-odds expected/8 and expected/other-target-digit, plus change from clean;
- digit mass, digit-conditional probabilities, entropy, and KL from clean;
- residual norms before/after, perturbation norm, and perturbation/residual ratio;
- empirical random-control percentile and permutation count;
- source/target selected-token diagnostics, clearly not described as hidden “thoughts.”

### Required deterministic generations

Generate 64 greedy tokens, saving raw token IDs and decoded text, for:

- clean Spider;
- Spider + Ant L26/C4;
- Spider + Dog L26/C4;
- matched-random seed 0 for each target-specific distance;
- clean byte and byte + Ant/Dog;
- both answer-only controls;
- clean Ant and Dog target prompts;
- clean Spider with first token forcibly set to `6` and, separately, `4`.

The forced-token continuations distinguish a substantive continuation effect from merely changing the first emitted digit. Random seed 0 must be fixed in advance, not selected for presentation.

## Conclusion

Job 149 answers its discovery question positively: **L26/C4 is one shared rank-8, single-site setting that yields distinct Ant→6 and Dog→4 first-token crossings.** The probabilities remain almost entirely on digits and the target distances are similar, but the interventions are large, extrapolative, and post-screen selected. Without rank-8-specific random, byte, answer-only, positional, and generation controls, it is not yet suitable as a public mechanistic demonstration.

- **Merge/publication verdict: BLOCK for a public demo; OK as an exploratory screen.**

Signed: **reviewer — 2026-09-05**