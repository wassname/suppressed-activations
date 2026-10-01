# Indirect-description donor addition: prospective test

Written by PI/OpenAI. Implementation/smoke in progress; no GPU job queued yet.

## Question and decision

Can reusable donor preparation from indirect animal descriptions support coherent dog→spider property changes? This changes preparation data under ordinary addition. It is not J-subspace isolation, a new algebraic method, or an exact reference reproduction. Readout job2686 is separate and does not control this editor.

The same-family adviser compared description donors, offline naming optimization and learned local feature replacement in `slop/reviews/2026-10-01_next-causal-design.md`. Description donors need the smallest change and test property behavior directly. Naming optimization introduces an unprovided optimization/norm rule; probe replacement would revisit unresolved calibration assumptions. The parent's one addition to the eight-generation advice is a literal-name donor control on each property: ten generations total, frozen before outputs.

## Data and operation

`data/dog_spider_donors_indirect_v3.json` freezes two descriptions per animal crossed with two wrappers. Every prompt ends `. It`; neither animal name nor evaluated property/answer occurs in its text. Four final-It residual16 states per animal are averaged. Each completed preparation context is saved immediately; an interrupted context may not be saved.

The natural vector is δ = mean(spider) − mean(dog). No projection, normalization, dose fitting or output-based prompt replacement. Differing prefix lengths, ambiguous descriptions and the changed natural norm remain limitations.

Current-input pseudocode:

```text
δ ← offline mean(spider) − offline mean(dog)
block15 final prompt position: h ← h + δ
every cached decode:           h ← h + .25 × ((h + δ) − h)
```

The explicit decode operation records actual float32 operation order before BF16 casting. No backward pass, preliminary current-input pass, later-layer feedback or current-input donor extraction. The read-only observer is block23. Freeze reverse direction, last-prompt-one coverage, greedy32-token cap and seed0. The eight preparation prefills use only generic donor prompts.

## Conditions and controls

- Existing dog legs prompt: Base / indirect donor / literal-name donor / matched random. Expected4→8.
- Existing dog `skeleton_body` prompt: the same four conditions. Expectedinside→outside.
- Existing barking-animal `2+2` control: Base / indirect donor. Expected4 in both.

Reuse the exact strings in08's `RELATIONS`; no new heldouts and no v5. Literal donor is the unchanged common-It checkpoint `out/2026-09-30_133218_jlens-one-pass/donors.pt`, SHA572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5. It retains its natural norm, not the new donor norm. Random is one fixed Gaussian seed0 vector scaled to the new donor's requested norm, reused across properties/calls. Applied BF16 norms may differ. Ten trajectories, at most320 generated tokens; one default-queue job targeting300s.

## Predictions, interpretation and checks

SHOULD:8 completed preparation states reconstruct the saved means; all final tokens equal the pinned tokenization of ` It`; editor vectors are fixed across properties; prefill/decode coverage matches every generated token; requested and post-cast states reconstruct exactly; no extra evaluation forwards. These follow from the code/data contract, not a behavioral success claim.

TODO validate: the same indirect donor may move affirmed properties toward8/outside while preserving arithmetic and readable, noncontradictory continuations. Report actual initial generated answers, full continuations, top10, answer log odds/mass, repetition, and separately labelled prefill/final-decode readouts. A later NLI hypothesis mentioning8 is not an affirmed8 answer. Token-table tie order is not generation order.

Rough planning weights, not estimates from data:50% unchanged/insufficient transfer;20% useful partial/coherent transfer;20% nonspecific or contradictory changes;10% implementation/measurement/other. A missing or wrongly applied update invalidates scientific interpretation. Base and random distinguish no effect from nonspecific perturbation; the literal control shows whether behavior differs from the prior preparation without silently changing its scale. Neither isolates orientation from natural magnitude. One random seed supplies no null distribution.

Both properties changing coherently with arithmetic retained is informative, not a human-imposed universal threshold. One coherent property change is partial evidence. A result matching random, unchanged initial answers, or contradictory continuations weakens this fixed configuration only. Do not rescue it by dose/sign/layer/coverage/window/normalization changes. Numerical checks and negative results do not complete either research goal.

Before queueing: tiny real-pipeline tests at seeds0/1, fresh static implementation review, pinned source/data/helpers/reference/contract, and a launcher that retains completed outputs. Afterward: independent saved-state reconstruction and full-continuation review. No pretrained behavior has been observed for these new descriptions.
