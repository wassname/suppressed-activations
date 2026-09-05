# Rank-8 single-site sample-component predictions

Question: did the earlier Spider→Dog result require repeated edits, or does one residual layer contain a usable Ant/Dog sample-component effect?

Extract rank-8 Spider, Ant, and Dog subspaces with the fixed L23/L25/L32 rule. For each target, apply the same whole sample-component replacement at the final prompt token in exactly one residual layer per forward. Screen L23–L30 separately with C∈{1,2,4,8}. Restore residual norm. Score only the first-token distribution. Do not generate or run random controls during the screen.

| possibility | prior after job 148 | expected observation |
|---|---:|---|
| one shared useful layer | 35% | at least one layer gives Ant→6 and Dog→4 before either target's digit mass disperses |
| Dog needs repeated edits | 45% | no single layer reproduces Dog's earlier C2 crossing |
| Ant target extraction is not useful | 70% | Ant fails across layers or moves toward 4/noise despite a clean target answer of 6 |

A candidate for the public demo requires both targets to cross at the same layer, though their smallest successful C may differ. Only then should that fixed layer and dose receive matched random controls and prompt-only generations.

Written by PI/gpt-5.4.
