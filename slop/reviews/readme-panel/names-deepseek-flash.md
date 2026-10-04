## Guess the column names

Context from the page: a row "passes" if its top‑8 words include the English (or Chinese) word for the meaning, and none of the 8 is an input/output‑language word or the word about to be said.

1. `found` — fraction of prompts where the hidden word appears in the top‑8. Higher better. Medium.
2. `leaked` — fraction where a top‑8 word is from the input/output language or is the imminent output word (contamination). Lower better. Medium.
3. `share` — ambiguous; likely fraction of prompts meeting some criterion (pass share). Higher better. Low.
4. `TP` — true positives: prompts correctly recovering the hidden word. Higher better. Medium.
5. `hits` — raw count of hidden‑word hits in the top‑8, without the leakage penalty. Higher better. Medium‑low.
6. `hidden hit@8` — fraction with the hidden word in the top‑8 (no leakage check). Higher better. High.
7. `said hit@8` — fraction where the word the model is about to say is in the top‑8; a predictability baseline, not a success metric. Ambiguous. Low.
8. `hit@8 hidden, not said` — hidden word in top‑8 and it is *not* the word about to be said: the genuinely suppressed concept. Higher better. High.
9. `pass` — fraction passing the full strict rule. Higher better. High.
10. `pass rate` — same as `pass`, but as a percentage; redundant. Higher better. Medium.
11. `AUROC hidden vs said` — separability of hidden‑word vs imminent‑output‑word scores. Higher better. Medium.
12. `transfer found` — `found` on an unseen/held‑out language pair; generalisation. Higher better. Low.

**Names I would ship:** `hidden hit@8`, `hit@8 hidden, not said`, `pass rate`. Drop `TP`, `share`, `found`, `leaked`, `hits` — cryptic, and `found`/`hits` collide. Keep `AUROC hidden vs said` only if a caption defines it. Best set for a captionless table: `hidden hit@8`, `said hit@8`, `hit@8 hidden, not said`, `pass rate`.

Missing: no caption, no units, no row sorting — a reader can't tell count from fraction, or baseline from success.

— pi-quick-oracles (DeepSeek Flash)