# Executed Public Notebook Review

## Review

- **Correct — execution integrity:** All six code cells have consecutive execution counts `1` through `6` (`nbs/demo.ipynb:24,157,272,319,388,461`). Their timestamps are sequential, with each cell idle before the next begins (`nbs/demo.ipynb:28-31,161-164,276-279,323-326,392-395,465-468`). There are no `error` outputs or null counts. The only stderr is a harmless `TqdmWarning` and model download/load progress (`nbs/demo.ipynb:39,173-204`). Jupytext completed execution, wrote the notebook, and the post-execution checker reported:
  > `PASS: executed notebook has one-site extraction, two targets, signed doses, and exact continuations`
  
  (`slop/audits/job_156_full.log:1-9`). The generation cell also asserts exactly 64 generated tokens for clean and every intervention (`nbs/demo.py:263-284`).

- **Correct — provenance:** The executed output records:
  > `'git': 'v0.1.1-62-g31670e0'`  
  > `'model': 'Qwen/Qwen3.5-4B'`  
  > `'revision': '851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a'`
  
  (`nbs/demo.ipynb:46-48`). There is no `-dirty` suffix, and the full repository HEAD is `31670e08c4f73fdc352fa7bddc6733c38ea80d52` (`.git/refs/heads/main:1`), matching the displayed short hash. Both tokenizer and model are loaded using the same frozen revision (`nbs/demo.py:120-122`). Job 150 transparently records its earlier code provenance while using the identical model and tokenizer revision (`out/2026-09-05_211609_causal-confirmation/recovered_log.md:19,25-26`).

- **Correct — executed values and fixed controls agree:** Every overlapping control value matches job 150:
  - Ant C1: top 8, p(6) `0.0382`, p(8) `0.8697`, log odds `-3.1250`, distance/residual `0.1990`.
  - Ant C4: top 6, p(6) `0.4871`, p(8) `0.3794`, log odds `+0.2500`, distance/residual `0.6791`.
  - Dog C1: top 8, p(4) `0.0893`, p(8) `0.8469`, log odds `-2.2500`, distance/residual `0.2084`.
  - Dog C4: top 4, p(4) `0.4901`, p(8) `0.2973`, log odds `+0.5000`, distance/residual `0.7203`.
  
  Compare notebook output (`nbs/demo.ipynb:408-416`) with fixed-control rows (`out/2026-09-05_211609_causal-confirmation/recovered_log.md:10-13`). The Spider, Ant, and Dog selected vocabulary rows also agree exactly (`nbs/demo.ipynb:337-341`; `recovered_log.md:64-67`). Displayed C4 generations begin with 6 and 4 (`nbs/demo.ipynb:512-513,552-553`), matching both job 150 targeted and forced-token continuations (`recovered_log.md:108-135,272-299`).

- **Correct — controls are represented without overclaiming:** The notebook accurately states:
  > “only 238/256 and 235/256 matched random effects were smaller”
  
  (`nbs/demo.ipynb:615-616`), matching the fixed-control percentiles (`recovered_log.md:75-76`). Its arithmetic-control statement is also accurate: three-plus-three exceeded Ant’s effect, while two-plus-two equaled Dog’s Δ log odds (`recovered_log.md:88-89`; `slop/reviews/20260905_job150_confirmation_review.md:89-90`).

- **Correct — LM-head rise-and-fall method only:** Extraction calls the repository’s `suppressed_activation_subspace` directly (`nbs/demo.py:53,135-145`). That implementation computes normalized LM-head logits, layer-25 rise versus layer 23, layer-25 fall versus layer 32, their positive minimum, selected centered effective unembedding rows, and a QR basis (`suppressed_activation_subspace.py:22-41`). No J-space, Jacobian, or corresponding import appears in the notebook. Intervention uses repository `replace(..., restore_norm=True)` through `operation="replace"` at block 25/residual L26 (`nbs/demo.py:169-187`; `scripts/demo.py:124-152`).

- **Correct — C1 versus C4 is explicit and empirically visible:** The opening says:
  > “`C=1` replaces the source component with the target component at the same norm. `C>1` extrapolates past that replacement.”
  
  (`nbs/demo.py:22-24`), and reiterates:
  > “`C=1` is the replacement endpoint; larger magnitudes are extrapolations.”
  
  (`nbs/demo.py:227-229`). The table makes the distinction concrete: C1 leaves top token 8 for both targets, whereas extrapolated C4 changes it to 6 or 4 (`nbs/demo.ipynb:408-416`).

- **Correct — interpretation is clear:** The notebook explicitly calls the result:
  > “transfer of the target prompt's next-answer state, not proof that an Ant or Dog concept was transferred”
  
  (`nbs/demo.py:26-28`). It further explains that forced-first-token continuations make the longer text “not separate evidence for persistent animal information” (`nbs/demo.py:255-259`) and concludes that the experiment:
  > “does not identify a transferable animal direction”
  
  (`nbs/demo.py:301-304`). This agrees with the job 150 review’s finding of generic answer/completion-state transfer and first-token forcing (`slop/reviews/20260905_job150_confirmation_review.md:46-65`).

- **Correct — minimal and hackable:** The notebook has six focused code cells, keeps model, revision, device, prompts, outputs, layers, rank, token count, and strengths together in one environment-overridable configuration cell (`nbs/demo.py:56-88`), and delegates reusable mechanics to repository functions rather than duplicating them.

**No issues found.**

- **Merge verdict:** **OK**.