## Review

### Correct / provenance and completeness

- **Observation:** Pueue job 132 ran `uv run scripts/spider_ant_demo.py` in the requested repository and completed successfully in about six minutes (`slop/audits/job_132_status.json:2-6`, `slop/audits/job_132_status.json:96-102`).
- **Observation:** The result records repository version `v0.1.1-39-g9b8f0d1` and model name `Qwen/Qwen3.5-4B` (`data/spider_ant_demo.json:2-8`).
- **Observation:** The prompt tokenization ends with token 13, `" "`, and the suppressed-token detector reports position 13, although the actual prompt text contains no literal “spider” (`data/spider_ant_demo.json:45-73`).
- **Observation:** The run structure calls for seven targeted condition families × two norm settings × thirteen doses = **182 targeted rows**, followed by nine positive doses × 32 seeds = **288 random-control rows** (`scripts/spider_ant_demo.py:299-314`, `scripts/spider_ant_demo.py:346-353`). The JSON sections run from `l26_dose_rows` at line 13625 to `l26_random_rows` at line 29049, and the random section ends with dose 24, seed 31 at lines 33355-33370. The full log likewise begins the L26 rows at line 653 and ends with dose 24, seed 31 at line 1193. I found no missing tail, crash, or partial condition block.
- **Observation:** All C=0 rows reproduce the same clean values: p6 `0.0266512521`, p8 `0.8825681806`, 6-vs-8 log odds `-3.5`, KL `0`; for example `slop/audits/job_132_full.log:656`, `:703`, `:729`, and `:755`.

### 1. Exact targeted conditions that changed top answer `8 → 6`

The source ordering identifying these otherwise unlabeled log blocks is fixed at `scripts/spider_ant_demo.py:299-314`. Exactly **ten** targeted rows had token `6` as rank 1:

| Method / position | Norm restored | C | p6 | p8 | 6-vs-8 log odds | KL | Entropy | Digit mass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mean_atomic_rank8 / final | yes | 12 | .432125 | .180136 | .875 | 1.2090 | 1.3934 | .998399 |
| mean_atomic_rank8 / final | yes | 16 | .529803 | .092066 | 1.750 | 1.8001 | 1.4122 | .998398 |
| mean_atomic_rank8 / final | yes | 20 | .412206 | .081168 | 1.625 | 1.9062 | 1.7153 | .996797 |
| lowercase_space_rank8 / final | yes | 12 | .343973 | .143389 | .875 | 1.3982 | 1.6692 | .997889 |
| lowercase_space_rank16 / final | no | 8 | .426663 | .084015 | 1.625 | 1.9038 | 1.6188 | .996580 |
| lowercase_space_rank16 / final | yes | 8 | .614656 | .057172 | 2.375 | 2.2609 | 1.4454 | .998408 |
| lowercase_space_rank16 / final | yes | 12 | .319762 | .091613 | 1.250 | 1.8537 | 2.1148 | .989283 |
| lowercase_space_rank64 / final | yes | 8 | .358517 | .022919 | 2.750 | 3.1140 | 3.1981 | .854252 |
| lowercase_space_rank64 / final | yes | 12 | .117573 | .021749 | 1.6875 | 3.2610 | 6.6947 | .354123 |
| lowercase_space_rank64 / final | yes | 16 | .171640 | .104105 | .500 | 1.7911 | 4.0370 | .723551 |

Evidence: mean-rank8 rows are logged at `slop/audits/job_132_full.log:675-698`; rank8 at `:774-781`; rank16 at `:793-828`; and rank64 at `:879-902`. The corresponding fully labeled JSON rows begin at `data/spider_ant_demo.json:15409`, `:15558`, `:15707`, `:21931`, `:22971`, `:24092`, `:24241`, `:28440`, `:28589`, and `:28738`.

**Observation:** All ten rows produced the exact same 64-token generation, including identical token IDs. The JSON confirms the same text at all ten locations (`data/spider_ant_demo.json:15554`, `:15703`, `:15852`, `:22076`, `:23116`, `:24237`, `:24386`, `:28585`, `:28734`, `:28883`).

Complete token IDs:

```text
[21, 13, 198, 39, 57296, 12807, 25, 561, 9572, 421, 43269, 78129,
 682, 220, 21, 13795, 13, 198, 3742, 279, 29094, 1157, 5509, 539,
 279, 2029, 30, 271, 248068, 198, 90700, 8340, 25, 271, 16, 13,
 220, 2972, 2014, 53983, 279, 5952, 64700, 198, 262, 348, 256,
 35495, 25, 328, 760, 1324, 314, 13795, 383, 279, 9572, 421,
 43269, 78129, 369, 220, 21, 1149]
```

Complete decoded generation:

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

### 2. Preregistered rank-8 lowercase primary versus random controls

- **Observation:** The preregistration required top `6`, a coherent continuation, a noncollapsed distribution, and a larger 6-vs-8 change than at least 31/32 matched random rotations (`slop/research/20260905_spider_ant_l26_dose_predictions.md:3-20`).
- **Observation:** The only top-6 rank-8 lowercase primary is final-position, norm-restored C=12: log odds `.875`, or a `+4.375` change from clean (`slop/audits/job_132_full.log:774`).
- **Observation:** Two controls exceed it:
  - seed 2: log odds `2.25`, p6 `.837071`, top `6` (`slop/audits/job_132_full.log:1067`);
  - seed 11: log odds `4.125`, p6 `.844161`, top `6` (`slop/audits/job_132_full.log:1076`).
  All other C=12 controls are below `.875`.
- **Conclusion:** **No. It beat 30/32, not the required 31/32.** At C=8 it also trails the same two seeds: targeted log odds `-.375`, versus seed 2 at `1.125` and seed 11 at `3.5` (`slop/audits/job_132_full.log:773`, `:1035`, `:1044`).

### 3. Rank and position comparison

#### Lowercase rank

- **Rank 8:** First and only flip is restored C=12. It has the least KL among lowercase flips, 1.398, and retains `.998` digit mass.
- **Rank 16:** Flips earlier at C=8 in both raw and restored forms. Restored C=8 has the largest p6 (`.615`) while retaining `.998` digit mass, but KL is already 2.261. It remains top-6 at restored C=12, then loses to `2`/non-digit outputs.
- **Rank 32:** **Never makes 6 top.** Positive C=2 and C=4 make `4` top; stronger doses move through `3`, `LOG`, `s`, and high-entropy distributions (`slop/audits/job_132_full.log:850-857`).
- **Rank 64:** Restored C=8/12/16 make 6 top, but with substantial generic disruption. At C=8 digit mass is only `.854`; at C=12 it falls to `.354` and entropy reaches `6.695` (`slop/audits/job_132_full.log:879-902`). Raw rank64 never flips and eventually produces whitespace.
- **Inference:** Rank is markedly nonmonotonic: 16 performs better than 8 at a lower nominal dose, 32 fails, and 64 flips only with much less distributional integrity. The decreasing two-vector condition numbers do not explain that nonmonotonic behavioral pattern (`data/spider_ant_demo.json:33372-33397`).

#### Final versus previous position

- **Observation:** Final-position mean-rank8 flips at restored C=12/16/20, whereas the same mean direction at the preceding ` is` position leaves `8` top at every dose and stays near clean even at C=24 (`slop/audits/job_132_full.log:653-725`).
- **Observation:** Lowercase rank8 at the preceding position is similarly inert across all doses (`slop/audits/job_132_full.log:726-751`), while final-position lowercase rank8 has a strong positive-dose response and flips at restored C=12 (`:752-784`).
- **Inference:** The effect is localized to the final prompt position, not the preceding ` is` position. Note that this “detected/final” position is the trailing space token, not a lexical spider token (`data/spider_ant_demo.json:45-63`).

### 4. Semantic effect versus generic perturbation

**Observations supporting a structured direction:**

- Positive doses usually raise 6-vs-8 odds, and negative doses suppress them for ranks 16/32/64. This sign dependence is not pure random noise.
- Low-dose rank8 retains almost all probability on digits.

**Observations against a specific Spider→Ant semantic effect:**

- Before `6` becomes top, `4` commonly becomes top; stronger doses yield `2`, `1`, `Web`, whitespace, letters, and `LOG`, rather than a selective transition from spider-like 8 to ant-like 6.
- KL and entropy rise substantially around flips. Rank64 C=12, for example, has entropy `6.695` and only `.354` digit mass.
- Random rotations also make `6` top and two preregistered controls are stronger than the rank8 primary.
- None of the ten 64-token continuations mentions an ant. They merely condition on the generated `6` and restate that the web-spinning animal has six legs.
- All ten continuations are byte-for-byte identical despite substantially different intervention directions and next-token distributions.

**Inference:** There is evidence that the projected direction can perturb the digit-answer manifold in a signed way, but the combined entropy/KL, competing-token, rank nonmonotonicity, and random-control results look more like a **generic answer/digit perturbation with a 6-favoring component** than a demonstrated Spider→Ant semantic substitution.

### 5. Likely bugs and confounds

- **Finding: P1 — continuation coherence is self-conditioning, not independent semantic evidence.** Hooks return without intervention whenever sequence length is one (`scripts/spider_ant_demo.py:47-52`, `:72-80`). After the forced first token, generation proceeds from the model’s own `6`, which naturally causes it to rewrite the fact as “...is 6.” The identical ten continuations reinforce this confound. Smallest fix: report first-token steering separately and generate intervention-on versus intervention-off continuations conditioned on the same first token.
- **Finding: P1 — controls do not satisfy the preregistered effect threshold.** Two of 32 C=12 controls exceed the primary. Any positive semantic claim should therefore be withheld.
- **Finding: P1 — matching is asserted but not audited.** Random rows record no residual norm, requested perturbation norm, or achieved perturbation norm, despite the preregistration naming failed norm/distance checks as a bug criterion. The source calculates a target distance but does not serialize validation (`scripts/spider_ant_demo.py:71-82`, `:346-372`). Smallest fix: record target and random before/after norms and distances.
- **Finding: P1 — random controls match only the norm-restored target.** `matched_random_hook` hardcodes `restore_norm=True` (`scripts/spider_ant_demo.py:77`), so the same controls are not valid matches for raw targeted rows. Restrict inference to restored rows or add raw-matched controls.
- **Finding: P1 — no held-out semantic prompt.** The subspace, token pair, intervention position, and measured answer all use one web/spider prompt. Direct digit-logit susceptibility cannot be separated from animal semantics.
- **Finding: P2 — rank comparisons are not perturbation-norm matched.** For example, achieved perturbation norms are about 20.93 for rank8 C=12, 23.19 for rank16 C=8, and 30.04 for rank64 C=8 (`data/spider_ant_demo.json:21920-22076`, `:24080-24237`, `:28430-28585`). Nominal C is therefore not a common physical dose across ranks.
- **Finding: P2 — “C=1 is the exact swap” only applies to raw rows.** Norm restoration rescales the complete residual after the swap, so restored C=1 no longer has the exact swapped coordinates described by the preregistration.
- **Finding: P2 — BF16 discretization produces many `.125`-spaced log-odds and exact ties.** The model is loaded in bfloat16 (`scripts/spider_ant_demo.py:86-90`), so marginal rankings and ties should not be overinterpreted.
- **Finding: P2 — the full log is complete but not self-describing.** Its L26 print omits `method` and `mask` (`scripts/spider_ant_demo.py:440-446`); interpretation depends on source loop order or the JSON.
- **Finding: P2 — provenance is incomplete for exact reproduction.** Git metadata is useful, but there is no script hash, dependency lock/hash, CUDA/library version, or pinned Hugging Face model revision. `from_pretrained` receives only the mutable model name (`scripts/spider_ant_demo.py:17`, `:87-88`).

### 6. Cheapest confirmatory run

Run only the **restored lowercase-rank8 final-position C=12** condition, with:

1. the original web-spinning prompt;
2. an unrelated, identically formatted clean-8 prompt, e.g. `Fact: The number of bits in one byte is `;
3. C=0 and C=-12 targeted controls on both prompts;
4. 32 newly seeded, achieved-distance-and-norm-verified random rotations at C=12 on each prompt;
5. full 64-token generations for every targeted or random row whose top token is `6`, plus a same-first-token (`6`) no-intervention generation control.

This is roughly 70 short forward passes after one model load and directly tests specificity.

**Expected if semantic:** original C=12 approximately reproduces p6 `.344`, p8 `.143`, and top `6`; unrelated-byte C=12 stays near clean `8`; C=-12 moves opposite; primary beats at least 31/32 new controls; its continuation differs meaningfully from the no-intervention continuation and supplies ant-related content.

**Expected if generic, currently more likely:** the unrelated 8-answer prompt also shifts toward `6` or suffers comparable digit redistribution; multiple random controls rival the primary; competitors such as `4`/`2` appear; and all top-6 continuations reduce to the same self-conditioned text pattern.

### Merge verdict

**BLOCK** any claim that job 132 demonstrated specific Spider→Ant steering. The run artifacts themselves are complete and useful, but the preregistered random-control criterion failed and the present evidence is more consistent with generic digit-answer perturbation.
Reviewed by PI/reviewer (gpt-5.4).
