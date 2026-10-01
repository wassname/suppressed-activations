# Person-position implementation review

**Verdict: no demonstrated blocker for the bounded diagnostic.** Historical/full-size parity remains a runtime gate, not something the tiny tests establish.

Read AGENTS.md, goal/User voice, ml-debug, preregistration, launcher, smoke code/logs, relevant production path/CLI and historical scoring implementation. No commands, inference, edits or delegation performed.

## Observed safeguards

- `scripts/english/08_jlens_one_pass.py:405–421` captures `h[0].detach().clone()` on the **first** hook call, preserving complete prefill states before cached decoding. The added persistence at lines 1147–1149 retains those states, not final-decode activations.
- Lines 1342–1373 iterate `range(h.shape[0])`, including protocol positions; save consumed token prefixes and four heads’ top32 IDs/text/scores. `full_mask = mask | output_mask | extension_mask` reuses the complete-input and final-prefill greedy-output masks. Half-erasure uses the same direction, native normalization, FP32 projection and BF16 head as the historical source.
- Labels enter alias ranking/membership, not head construction, masks or top32 selection.
- Lines 1613–1627 compare serialized complete generation traces, final-position states and complete readout rows against the reference. Final-position score tensors also require exact equality inside the position loop.
- `slop/audits/2026-10-01_person-position-launcher.py` checks four traces, cached coverage, gradients disabled, observed forward lengths and `"readout_rows_exact" == 88`. The production path calls one ordinary generation per case; position scoring adds no transformer call.
- Both supplied smoke logs end with `"PASS real four-case diagnostic ... no extra forwards. Tiny model only."` Seed1 additionally records launcher completion and 128 forwards/128 tokens. These are plumbing checks, not scientific evidence.

## Actionable limitations

1. **Raw best-alias identity is not recorded.**  
   `scripts/english/08_jlens_one_pass.py:1357–1364` chooses `best_id` using masked `z`, while separately reporting `"raw_alias_rank"`. For cases where the mask removes the highest raw alias, that ID does not identify the alias responsible for the raw rank. Add distinct raw/masked best IDs; use null when all aliases are masked. This is an auditability limitation, not a demonstrated ranking defect. A check comparing raw and masked alias argmaxes on each row would establish affected cases.

2. **Snapshot immutability is conditional.**  
   The launcher copies source/manifest before inference, but executes `runpy.run_path(str(source))` and reads dataset/reference files from their original paths. Its pin loop checks only supplied entries. No production position manifest was supplied here; required-pin completeness and immutable imported dependencies remain unverified. Before queueing, verify the manifest covers source, dataset, historical artifacts and relevant imports, and that those paths remain immutable.

## Interpretation limits

Protocol/preclue hits cannot demonstrate use of the book clue. Complete-input masks and final-position output direction contain later information even when the residual prefix is early: this is explicitly posthoc readout, not an earlier editor.

BF16 ties, prefix aliases and label-selected positions remain confounds. Exact full-size mismatch must stop interpretation; do not replace that requirement with a new tolerance. No absence claim extends beyond these heads/layers.

— **PI/OpenAI**, static same-family review; not neural certification.