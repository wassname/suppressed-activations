## Finding

The English semantic audit is a legitimate stronger transfer criterion **if named explicitly**. Presenting it and translation as the same operational definition of “said concept excluded” is inconsistent; attributing exhaustive multilingual exclusion to the user is unsupported by the supplied wording.

### Requirement versus convention

The user wrote:

> “having english thoughts is the eval not the training”

and proposed:

> “French -> Eng/Cn -> Russian”

Source: `.local/status-check/current-user-voice.md:1-50,160-191`.

These require transfer beyond language-based separation; they do not specify exhaustive synonym classes. The passage at lines 322–375 describing “minus what it said” is a quoted agent report, not an independently stated user scoring requirement. `.pi/goals/aef0cd-v1.md` requires hidden-concept recovery with input/output exclusion, but leaves the semantic equivalence boundary unspecified.

### Observed definitions

In `scripts/english/08_jlens_one_pass.py`, `translation_cases` declares:

> `"hidden_aliases": [w["en"], w["zh"]]`

while answer aliases contain only the target-language word. Translation therefore recovers an **unspoken language-specific lexical rendering of the same referent expressed by input/output**, excluding designated input/output word forms. It does not exclude the output’s entire concept.

`disjoint_labels` removes shared token IDs from both scoring classes, not semantic equivalents or readout entries. The main scoring block additionally excludes actual continuation words and, when the expected answer appears, declared answer aliases.

For English bridges, the desired hidden referent differs from the answer: December versus January; apple versus red. Under `slop/reviews/2026-09-30_v3-semantic-review.md`’s convention, “Word identity includes … clear translations and aliases.” Thus Januari/January and 红/red count as answer leakage regardless of surface language. This cannot be applied unchanged to translation without excluding its positive labels.

Hidden recovery deserves the same semantic distinction. `data/english_hidden_words_v4.json` declares only `"violin", "violins"`. The polar review reports `提琴` despite lexical failure. That supports a possible translated hidden-family readout, not automatically violin identity: 提琴 can denote the broader bowed-string family. Exact equivalence needs lexical adjudication; no rescoring follows.

### Smallest clarification

“Translation scores unspoken lexical renderings; English semantic audits score distinct hidden referents while excluding observed input/answer equivalents. Frozen lexical scores use declared aliases and are not exhaustive semantic scores.”

The unresolved editorial decision is whether the general claim concerns unspoken **representations** or exclusively unexpressed **referents**. Neither score establishes internal reasoning.

Job2648, past classifications, and frozen gates remain unchanged. No new test requested.

PI/OpenAI