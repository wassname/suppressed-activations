# Transform scoreboard, 2026-10-03

PI/OpenAI, for wassname. Source: `scripts/english/09_transform_scoreboard.py`. Latest run `out/2026-10-02_234426_transform-scoreboard/run.md` (job 2853). Each rerun added rows: job 2848 the two "minus output subspace" rows, job 2853 the AntiPaSTO "suppressed" row. Earlier rows reproduce job 2843 exactly.

## What is scored

Each transform turns one forward pass into a score per vocabulary token. Its **top 8 tokens are scored as they are: no input mask, no output mask, no word removal.**

- **Scoreboard:** Wendler word translation, 4-shot, the same prompts as `04`. Hidden = tokens spelling the English or Chinese word; said = tokens of the output-language word; input = tokens of the input word.
- **Overlap and partial words:** a token that spells both the hidden word and the said or input word is removed from the hidden set. Prompts where the English word is spelled like the input or output word are skipped, as in `04`. Partial tokens count when they are a prefix of the word, 3+ characters (1 for Chinese), using the same rule as `q.is_prefix_hit`.
- **Score:** F1@8 = 2PR/(P+R), with P = hits/8 and R = hits/min(|hidden|, 8), averaged over prompts. **Pass** = hidden word in the top 8, and no said or input token in it.
- **Not circular:** each family's one setting (layer, rank) is chosen on the dev pair de→fr only. It is then frozen for the 5 test pairs (408 prompts) and the English sets. No transform uses English or Chinese word lists; those are used only to score.

## Results

| transform (setting chosen on de→fr) | test F1@8 ↑ | test pass ↑ | test: said in top 8 ↓ | English v3 F1 | English v4 F1 | TwoHopFact F1 |
|---|---:|---:|---:|---:|---:|---:|
| **J-lens minus output subspace (layer 28, rank 256)** | **.501** | 316/408 | 56/408 | .138 | .174 | .018 |
| plain lens minus output subspace (layer 28, rank 16) | **.501** | 299/408 | 67/408 | .040 | .129 | .009 |
| J-lens, layer 28 | .484 | 276/408 | 93/408 | .133 | **.205** | .013 |
| plain logit lens, layer 28 | .483 | 286/408 | 76/408 | .040 | .161 | .007 |
| churn subspace (WikiText PCA of layer 27→28 change, rank 1024) | .482 | 341/408 | 20/408 | .016 | .094 | .000 |
| write-not-read (MLP weights, layer 29, rank 1024) | .462 | 250/408 | 108/408 | .040 | .097 | .002 |
| your suppressed subspace (rank 32, per prompt) | .435 | 346/408 | 3/408 | .000 | .000 | .000 |
| rise-and-fall through J-lens (22→28→output) | .418 | **356/408** | 2/408 | .066 | .125 | .007 |
| attention output of layer 23, J-lens | .404 | 281/408 | 6/408 | **.225** | .047 | **.034** |
| your rise-and-fall, plain (22/27/32) | .257 | 301/408 | 0/408 | .000 | .000 | .000 |
| AntiPaSTO "suppressed" subspace (WikiText PCA of min(increases, decreases), rank 1024) | .360 | 273/408 | 66/408 | .040 | .031 | .000 |
| erased-variance subspace (WikiText, 27 vs 32, rank 1024) | .209 | 257/408 | 13/408 | .000 | .000 | .002 |
| weak-readout subspace (bottom of W_U, rank 1024) | .166 | 190/408 | 42/408 | .016 | .000 | .000 |

Set sizes: English v3 n=16, v4 n=8, TwoHopFact n=56 (6 had no scorable hidden word). Dev scores per family are in `run.md`; every layer and rank for every prompt is in `rows.json.gz`.

## Reading it

- **"Minus output subspace"** is a fixed projection: it removes the top-r principal directions of the final-layer activation on 300 WikiText texts, then reads through the J-lens or plain lens. It gives the best test F1 (.501 vs .484) and cuts the spoken word from 93 to 56 lists for the J-lens. The gain is small, and English hardly moves.
- **F1 barely separates the top methods on translation** (.48–.50). F1 rewards finding the hidden word and puts little weight on whether the spoken word is also in the list. The **pass** column and the **said** column separate them.
- **Best at leaving out the spoken word without masks:** rise-and-fall through the J-lens (356/408, spoken word in only 2 lists), then your suppressed subspace (346/408, 3 lists). These are your method and the version read through the J-lens.
- **Best fixed subspace (the same for every prompt):** churn, rank 1024 (341/408, spoken word in 20 lists). It is fitted on WikiText with no labels, so it can be used directly for steering. But rank 1024 is 40% of the 2560 dimensions, so it is a weak restriction.
- **English transfer is poor for every transform without masks.** Inputs and spoken answers fill the top 8. Attention output at layer 23 is the best on v3 (.225) and TwoHopFact (.034); the J-lens at layer 28 is best on v4 (.205).

Examples (top 8, unfiltered):

```text
fr→ru: nuage → облако             suppressed subspace: cloud, 云, cloud, clouds, Cloud, Cloud, -cloud, 云的
English: Gothenburg → Stockholm  attention L23 J:   Swedish, 瑞典, Sweden, Sweden, Scandinavian, 北欧, Göteborg, Nordic
                                 J-lens L28:        Stockholm, Sweden, Sweden, Swedish, 瑞典, stockholm, Göteborg, Oslo
```

## Steering with the same kind of object

Swapping two token directions' J-lens coordinates at layer 15, at every prompt position, is steering inside a 2-dimensional J-lens subspace. It needs one pass and no preparation on the current input.

| question template | target country's two answers | another single country | partial / unchanged | plain-lens swap | random edit |
|---|---:|---:|---:|---:|---:|
| capital + currency | 7/10 | 2/10 | 0 / 1 | 0/10 | 0/10 |
| continent + currency | 6/10 | 1/10 | 1 / 2 | 0/10 | 0/10 |

Same 5 country pairs, fixed before running. The failures are the same pairs in both templates (Germany→Brazil, Mexico→Spain, China→Egypt). Draft README section: `slop/drafts/2026-10-02_readme-country-swap-section.md`.

## Known limits

- One model (Qwen3.5-4B); one prompt format per set; small English sets.
- The pass column counts spelled tokens only. A translation of the said word is missed unless it is spelled the same.
- **The fixed subspaces work only at rank 1024 of 2560.** On de→fr, churn at layer 27 scores F1 .000, .156 and .495 at ranks 64, 256 and 1024. Write-not-read, erased-variance, weak-readout and the AntiPaSTO "suppressed" subspace behave the same way; AntiPaSTO scores .000, .030 and .390 on dev. One departure from the README for AntiPaSTO: magnitudes are RMS-normalised per layer. So none of them isolates the hidden word in a small subspace; they come close to the plain lens as rank grows. Churn's lower said count (20 vs 76 for the plain lens) suggests the 1536 dimensions it drops include much of the output direction. That is a lead, not a finding.

## What I would try next

1. **Steering with the scoreboard's best fixed subspace.** For the country questions, use the "minus output subspace" or churn basis in place of the 2-token J-lens basis. If it steers as well, readout and steering use one object.
2. **A per-prompt subspace through the J-lens.** Your suppressed subspace and rise-and-fall through the J-lens are the best at leaving out the spoken word (346 and 356 of 408). Building your rank-32 subspace from J-lens rise-and-fall scores, not plain-lens scores, would combine the two.
3. **English stays the open problem.** With no masks, the spoken answer and input words fill the top 8 for every transform. The hidden word is readable at the clue's own tokens (36 of 62 two-step questions), not at the last token. A readout that works on English needs a label-free way to pick those positions.
