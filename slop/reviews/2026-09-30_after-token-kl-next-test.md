## Inherited decisions
2630 failed: probability weighting removed the rare-token diagnostic without improving joint recovery; matched and mismatched counts were equal for J24/plain27. Retire token-KL without rescue, reselection, or sweeps. Both goals remain open.

The supervisor approved **one question-span pooling test**, with the contract below.

## Diagnosis
Location is a defensible next hypothesis: a bridge concept may peak while its clue is processed, before the final position becomes answer-dominated. Source confirms `generate_readout` already captures every prefill position; persistence currently retains only the last.

However, pooling increases opportunities for **both hidden recovery and speech/input leakage**. Excluding demonstration positions prevents their direct selection, not their contextual influence. Consequently, hidden-only improvement is insufficient.

This is more tightly specified than inventing a sparse clamp whose executable reference remains unavailable.

## Drift / contradiction check
The comparator must remain the **final-layer distribution at the last prompt position**. Using each position’s local final distribution would introduce a second change and compare against predictions of upcoming prompt tokens, not the impending answer.

Full-state capture occurs during the scored generation—not a preliminary pass. End-pass readout remains inadmissible as feedback into earlier causal edits.

## Recommendation: approved contract

**Budget:** one local default-queue job,300-second TERM deadline plus15-second kill grace. Use all eight existing v4 prompts, one generation each, maximum eight new tokens each: **64 total**. No intervention, fitting, or question-specific preparation.

**Position boundary:** tokenize the complete unchanged prompt once with offsets. Eligible positions are non-special tokens whose spans are fully contained in the dataset’s case text, after its declared constant prefix. Exclude boundary-straddling tokens; assert the final prompt token is included. Use no labels, language identification, or clue annotations. Retain the full prompt as model input and for the existing prompt mask.

For each \(R\in\{\mathrm{J24},\mathrm{plain24},\mathrm{plain27}\}\):

\[
s_R(t)=\max_{i\in I}\left[p_R(t\mid h_i)-p_{F,\mathrm{last}}(t)\right].
\]

Normalize each vocabulary distribution **before masking**. Retain only positive scores, with unchanged full-prompt and greedy-final-token masks and \(k=32\). This is per-token maximum pooling, not a union of positionwise top32 lists. No erasure or token-KL composition.

**Controls:** identical last-position probability excess; equally pooled J24/plain24/plain27; pooled cyclic-mismatched-final subtraction retaining current masks; and un-subtracted pooled probabilities with identical masks. Keep incumbent half-plain27’s6/8 visible. These distinguish location benefit from subtraction benefit.

**Validity/evidence:** assert unchanged generated token IDs, cached last-position states, and existing scores against v4. Any discrepancy blocks interpretation as a position-only comparison. Persist complete prefill states, token offsets, eligible positions, masks, coverage, and each selected token’s maximizing position and score components. Log hidden/said peak provenance separately for evaluation only.

**Selection:** choose the pooled representation with highest alias-checked joint count; ties prefer **plain27 > J24 > plain24**. Promising requires **≥7/8**, strictly exceeding its own last-position and pooled mismatched controls. Report unchanged within-prompt AUROC and evaluable denominators; retain wrong/unscorable cases in the eight-case denominator.

Before new-example evaluation, symmetric blinded review must find no definite input/said leaks among the winner’s counted passes. No switching winners after review. Comparable un-subtracted performance precludes attributing improvement to subtraction.

## Risks / next decision
If recovery improves without exclusion, reject this pooled method—do not select a window afterward. Passing supports freezing for new examples, not generalisation or goal completion. No layer/window/k tuning is authorized.

## Need from main agent
None; contract settled. No implementation handoff here.

— **PI/OpenAI**