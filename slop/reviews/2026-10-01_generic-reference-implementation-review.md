# Generic-reference implementation review

**Result:** One CLI blocker; two provenance/recovery gaps. No arithmetic defect found in the scoped scoring path. This is implementation review, not scientific approval.

Read the supplied files, diff, complete three smoke logs, applicable AGENTS.md, and ml-debug skill. No commands, edits, network access, or pretrained inference performed.

## Findings

### 1. Blocker: neither new path is exposed through the CLI

`scripts/english/08_jlens_one_pass.py:766–778` accepts `prepare_reference_json` and `reference_checkpoint`, but the complete parser at `:1907–1952` registers neither argument before:

> `main(**vars(parser.parse_args()))`

**Affected inputs:** command-line invocations using `--prepare-reference-json` or `--reference-checkpoint`. These should fail as unrecognized arguments rather than prepare/rescore references.

The smoke bypasses argparse: `slop/audits/2026-10-01_chat-main-smoke.py:62` calls `g['main'](prepare_reference_json=...)`, and `:152–155` similarly supplies `reference_checkpoint` directly.

**Discriminator:** invoke the actual entry point with each new option; both should parse and reach their guarded branches. Not executed here. This is not a blocker for deliberate Python-function invocation.

### 2. Medium: same-revision, wrong-reference provenance is accepted

`scripts/english/08_jlens_one_pass.py:898–902` checks only:

> `assert (reference["model"], reference["revision"]) == (q.MODEL, q.REVISION)`

It does not validate the frozen reference content, rendered prompt/input IDs, or one-prefill coverage. The SHA recorded at `:911–915` identifies whichever checkpoint was supplied; it is not an expected-digest check.

**Affected inputs:** a checkpoint from another prompt or capture procedure with the same model/revision and compatible state tensors. Static inspection predicts acceptance, despite the fixed reference in `data/generic_readout_reference_v1.json:3` and preregistration.

The smoke’s only altered-reference test changes `revision` (`slop/audits/2026-10-01_chat-main-smoke.py:193–204`).

**Discriminator:** preserve model/revision while changing reference content, IDs, or coverage; require rejection against the frozen specification. No such failure test is evidenced. This is an integrity gap, not evidence that the supplied checkpoint is wrong.

### 3. Medium: interrupted preparation loses its input-specific audit record

`scripts/english/08_jlens_one_pass.py:435–444` performs `generate_readout(...)` **before** writing the config/prompt/input IDs to `reference.pt`, `reference.json`, or `run.md`.

**Affected inputs:** an exception/interruption during the generic forward, or after it but before artifact writing. Runtime/source files exist, but the consumed reference input and attempted-call status are not durably recorded. Retrying also cannot establish a total one-prefill budget from these artifacts alone.

**Discriminator:** inject a forward exception and inspect the preparation directory. Persisted input/config and explicit incomplete status would disprove this gap. The retained first fixture failure demonstrates the exception location, but does not test recovery or preserved preparation metadata.

## Verified behavior and remaining blindspots

- `:423–426`, `:900–907`, `:1233–1242`, and `:1283–1305` implement transport → native BF16 norm → FP32 subtraction → full projection vector then half multiplication → BF16 head, **without a second norm**.
- All six candidates reuse `W[final_logits.argmax()]`, the original current-case direction. One CPU seed0 unit vector is shared across representations/cases and scaled only to each normalized reference’s pre-projection norm.
- Preparation uses one-token generation and discards its token identity. Ranking uses prompt/output/extension masks, not labels or continuation IDs. Selection is full-vocabulary `topk(32)` followed by finite filtering (`:1307–1316`); ties retain existing PyTorch semantics, not a new stable-ID guarantee.
- Norm reporting is correctly distinguished: `:1297–1303` records separately projected reference norm, separately BF16-cast reference norm, and the **actual difference between rounded candidate/base decoder states**. These quantities need not match. However, the smoke never reads `reference_traces.json`; numerical reporting remains untested.
- The final supplied log states, for both seeds, “56 rows/44 unchanged,12 centered candidates” and “no cached forwards.” It ends “tiny random CPU model only; no pretrained scientific generations.” Earlier logs preserve the cached-guard failure and `KeyError: 'states'`, consistent with the reported fixture corrections.
- Smoke evidence covers tiny random CPU BF16 weights, two cases per seed—not pretrained GPU behavior or all twelve planned cases. Training/loss/schedule diagnostics are inapplicable.

**Signed: PI/OpenAI**

## Parent repair evidence — PI/OpenAI

Added both CLI options; actual CLI subprocesses reach their pre-model guards. Added fixed-config/rendered-input/IDs/coverage/completed-state validation, including same-revision mutation tests. Preparation now writes its exact input and explicit incomplete status before the forward; an injected exception preserves that record. Tests also reconstruct every reported norm, including realized BF16 decoder changes.

`slop/audits/2026-10-01_generic-reference-smoke.log`: review-fix run passes51s, seeds0/1, with zero-reference parity, unchanged old rows, no cached forwards, wrong-reference rejection and preserved incomplete metadata. The reviewer did not rerun these repairs. Full twelve-case launcher smoke also passes87s:264 old rows exact plus72 candidates, one generic prefill and zero cached-case forwards. No pretrained reference has been observed.
