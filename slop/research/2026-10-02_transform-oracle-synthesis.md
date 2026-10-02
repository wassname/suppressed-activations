# Transform/subspace brainstorm: oracle synthesis

PI/OpenAI, 2026-10-02. Brief: `2026-10-02_transform-subspace-brief.md`. Four independent answers, same brief, no peer views shared:
`2026-10-02_transform-oracle-{astra,fable,gemini,muse}.md` (Astra = gpt-6-astra, Fable = claude-fable-5-1, Gemini = gemini-3.8-flash, Muse = muse-spark-1.3-contributor).

## Where they agree (4/4)

The most diagnostic observation is that masking more predicted words leaves translation unchanged but removes the hidden word in English (v4 .184 → .061). Their shared reading: in translation, script/language separates hidden from spoken; in English, both are in the same semantic field and the same late-layer directions. Generic variance subspaces pick format variance, not suppression.

> "The task is therefore a nuisance-removal problem, not a discovery problem." — Fable

> "Not said is not equivalent to unlikely at the output: an intermediate concept can remain output-compatible." — Astra

## Proposals, grouped

| idea | who | fits on | one pass, no labels? | status here |
|---|---|---|---|---|
| remove the will-be-said component in residual space: per prompt ⊥ h32 | Gemini #1 | nothing | yes | job 2761 |
| same, offline: ridge A from mid state to h32 on WikiText, read the residual x − Ax | Fable #1 (Muse #2 related) | WikiText | yes | job 2761 |
| project out a generic output-token subspace before the J-lens | Muse #1 | WikiText predictions | yes | not run (likely also removes hidden words, which the model also predicts often) |
| fall-only in logit space, ReLU(z27 − z32), no rise condition | Fable #2 | nothing | yes | job 2760 ("fall-only J") |
| read the attention-block output at the last position (what was retrieved) | Fable #3 | layer choice on translation | yes | not yet; needs attention hooks |
| contrastive PCA of overwritten vs surviving states | Gemini #3 | WikiText | yes | not yet |
| cross-lingual invariant complement (pairs sharing the hidden word) | Muse #3 | translation pairs | language used to form pairs offline | not yet |
| supervised role adapter (hidden vs spoken) on known two-step chains | Astra #1–3 | English chains with known intermediates | labels offline | conflicts with "English thoughts are the eval, not the training"; report separately if ever run |
| difference with an abridged prompt | Gemini #2 | — | **no**, second prompt | excluded |

## Scoring concerns raised

- F1@8 on 8–16 prompts moves ~.1 per hit; treat differences under .1 as noise (Fable).
- One-token hidden word may undercount distributed intermediates, e.g. Thor→Thursday (Fable, Muse). Muse suggests also reporting rank(hidden) − rank(spoken).
- Missing diagnostic: does the hidden word reach the top 8 at any layer in English? If not, no fixed final-position transform can win (Fable).
