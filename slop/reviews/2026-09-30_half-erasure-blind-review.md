# Blind readout review — 2026-09-30

**Result:** Half erasure retains more identifiable hidden concepts than full erasure on these saved rows. I found no definite same-answer leak in its reported passing rows, but this is not proof of semantic exclusion. Several other methods retain clear translations, number words, plurals, or answer fragments. Missing hidden concepts also cause many failures.

Signed: **PI/OpenAI, reviewer-openai**. Same OpenAI model family as the authoring/review workflow; not an independent-model-family assessment. Scientific review only, not goal sign-off.

## Scope and blindness

Read both requested AGENTS.md files first, then all **176 rows: 16 concepts × M0–M10**, including every generation and top32 list. Reads covered rows 1–45, 46–90, 91–135, and 136–176. Blind findings were recorded in a supervisor progress note before opening source, run log, or method key.

Subsequently read the complete 654-line `source.py`, 1,289-line `run.md`, method key, erasure traces, generation defaults, dataset/alias files, capture-test source/log, and relevant imported Python files. Read the ml-debug skill. No edits, commands, model inference, network access, or paid services.

## Blind findings

“Hidden present” below means recognizable concept-bearing text, not proof of a hidden computation. Definite leakage concerns the **actually generated answer**, even when that answer is wrong.

| ID | Clearly recognizable hidden concepts | Definite same-answer leakage |
|---|---|---|
| M0 | Horse, through Chinese horse tokens | None identified |
| M1 | Greece (`希腊`), horse, cow, duck | Austria `Wien`; cow `calf`; octopus `zero` |
| M2 | Greece, horse; cat through answer `kittens`, not separated | Portugal `Lisbon`, Germany `Berlin`, Greece `Athens`, Austria `Vienna`, Norway `Oslo`, Kenya `Nairobi`, cat `kittens` |
| M3 | Seven countries except Spain; horse, cow, goat, cat | Portugal `Lisboa`, Germany `柏林`, Austria `维也纳`, Thailand `曼谷`, chicken `four`, octopus `zero` |
| M4 | Portugal, Germany, Austria, Norway; horse, cow, goat | Chicken `four`, octopus `zero`, penguin `TWO` |
| M5 | Greece, horse | None identified |
| M6 | Horse | None identified |
| M7 | Portugal, Germany, Greece, Austria, Norway, Kenya; horse, cow, duck; cat via ambiguous `小猫` | Germany `柏林`, Greece `雅典`, Austria `Wien`/`维也纳`, Spain `巴塞罗那`, cow `calf`, goat `calves`/`小牛`, octopus `zero` |
| M8 | Seven countries except Spain; horse, cow, goat, cat | All eight generated city answers; cat `kitten`, chicken `four`, octopus `zero` |
| M9 | Greece, Norway, Kenya; horse, cow, duck | Germany `柏林`, Greece `雅典`, Austria `Wien`/`维也纳`, cow `calf`, goat `calves`, octopus `zero` |
| M10 | Seven countries except Spain; horse, cow, goat, cat | Chicken `four`, octopus `zero` |

Additional diagnostic **answer fragments**, distinct from complete translations:

- Spain/M1, M7, M9: `celona` with generation `" Barcelona.\nQuestion: What is the"`.
- Kenya/M7, M9: `airobi` with `" Nairobi.\nHypothesis: The"`.
- Thailand/M7: `angkok` with `" Bangkok.\nQuestion: What is the"`.

These long fragments strongly identify the answer in context. Conversely, `奥斯`/`Os` for Oslo and `里斯`/`リス` for Lisbon are suggestive but less uniquely identifying.

### Concrete distinctions

- **Translation leakage:** row 20, Thailand/M3, contains both `" Thailand"` and `"曼谷"` while generating Bangkok. Hidden recovery and answer leakage coexist.
- **Wrong answer still leaks:** row 11, goat/M7, generates `" calf.\nHypothesis: The"` and retains `" calves"` and `"小牛"`. Evaluating only the intended *kid* would miss this.
- **Number spelling counts:** row 10, penguin/M4, retains `" TWO"` while generating 2; row 16, chicken/M3, retains `" four"` while generating 4.
- **Related category is not identity:** row 27, cow/M4, has cows/cattle plus baby, pups, lamb, kittens. Those young-animal categories do not individually establish *calf* leakage.
- **Genuine ambiguity:** horse rows contain `小马`, `Pony`, sometimes `驹`; these can denote small/young horses or foals without specifically denoting a male *colt*. Cat `kits`, `kitty`, and `小猫` likewise need explicit annotation policy. Duck `呱`, `呱呱`, and `嘎` are plausible quack representations but not uniquely duck-specific. Octopus `nulla` plausibly denotes nothing/zero, but I did not classify it as definite.
- **Missing hidden concepts:** no method’s corresponding chicken, octopus, or penguin row visibly recovers that indicated animal. M0/M5/M6’s lack of definite answer leakage is therefore not evidence of broad success.

## After unblinding

Mapping: M0/M6 are half/full erased plain24; M1/M9 full/half erased plain27; M2 plain24; M3 masked J; M4 full-erased J; M5 masked plain24; M7 masked plain27; M8 J; M10 half-erased J.

The saved summary reports M10 **11/16**, M4 **7/16**, M3 **6/16** alias-checked joint passes. These are lexical metric counts, not independently verified semantic rates.

The four additional M10 versus M4 cases are Greece, Thailand, Kenya, and cat. Their hidden tokens remain visible under half erasure and disappear under full erasure. That is a concrete paired observation supporting a retention trade-off. My definite M10 leaks—chicken and octopus—already lack hidden recovery; they do not refute those eleven passing rows.

### 1. Same-generation capture: supported, with a precise limit

`source.py:57–73` captures a clone only on each layer’s first hook call, inside the same `model.generate(...)`, and asserts coverage:

> `expected = [ids.shape[1]] + [1] * (len(tokens) - 1)`

Thus the readouts use **prefill states from the generation that supplied the continuation**, not final-decode states and not a separate trajectory pass. Hooks return no replacement; `scripts/demo.py` removes its own handles in `finally`.

The archived capture log reports passes on tiny Llama and hybrid Qwen3.5 for two seeds, including early EOS and hook ownership. It explicitly says:

> “full-size BF16 parity remains to be tested”

I did not execute those checks. The test imports the current production helper, not the archived source snapshot; its provenance is consequently supportive rather than conclusive for this artifact.

### 2. Erasure controls are paired correctly, but target one token—not the whole answer

`source.py:338–348` uses the same captured state and masks for both strengths:

> `removed = (normalized @ direction) / direction.square().sum() * direction`

Full erasure removes this projection; half erasure removes half. Erasure traces support the arithmetic: Germany/J changes the target score from approximately 25.59 to −0.00085/full and 12.8125/half.

**Important observed limitation:** the erased token is `" a"` for horse, cow, and duck, and `" "` for chicken, octopus, and penguin. It is not colt, calf, quack, or the answer digit. This follows `output_id = int(final_logits.argmax())`; the traces confirm it.

Consequently, persistent calf/zero/four representations are not evidence that projection arithmetic failed. The method often never targeted that answer representation.

Also, zeroing a logit is neither zeroing probability nor removing a semantic concept. The subsequent mask excludes selected spellings; correlated translations can remain.

### 3. Scorer limitations materially affect interpretation

- `source.py:319–328` extracts lexical words from the full continuation, but adds declared answer aliases only when an expected answer is observed.
- The prefix predicate in `scripts/english/01_detector_baselines_and_pair_transfer.py` is:

  > `word.lower().startswith(t)`

  It misses suffix fragments such as `celona` and `airobi`. It also misses *calves* when actual output is *calf*, unless separately supplied as an alias. Goat’s declared aliases are kid/kids, so its wrong calf answer does not activate a calf synonym set.
- Posthoc translated-answer annotations were selected from earlier **J-lens** passes. Applying that same list to all methods is computationally symmetric but not semantically comprehensive: plain27 exposes other translations/fragments.
- AUROC uses **already masked** scores (`source.py:368–373`). Suppressing negative tokens can improve it mechanically. Cat/M3 has actual-output AUROC 1 while its list still includes `小猫` and `kitty`. High AUROC is not semantic separation or top32 recovery.
- `run.md` calls the count a “conservative count of verified passes.” Keeping unscorable rows in the denominator is conservative in one respect; incomplete semantic negatives prevent interpreting that phrase as a verified lower bound on semantic success.

### 4. Provenance and causal interpretation remain limited

Positive evidence: model/tokenizer revisions are pinned; lens download uses a revision and SHA check; dataset, source, generation defaults, and states are saved.

Unresolved: the archived script imports live helper files rather than immutable copies. Its lens check verifies dimensions and prompt count, not the model revision used to fit the lens. The source itself says that fitting revision is unrecorded. This review did not independently verify checkpoint bytes, raw-state tensors, or blind-export equality.

The prompts designate plausible intermediates. They do not establish that the model computed those intermediates rather than answering by association. Broad lists of countries or animals can recover a label without isolating a specific hidden thought.

## Cheapest distinguishing tests

1. **No inference required:** rescore the saved rows against one method-blind annotation table of actual answers, including translations, plurals, and diagnostic fragments; retain separate “definite,” “broader category,” and “ambiguous” columns. This separates lexical-score inflation from genuine visible retention.
2. **No inference required:** join erasure targets to saved generation pieces and explicitly flag article/whitespace targets. The saved traces already predict six affected prompts.
3. **Before claiming a robust half-erasure advantage:** freeze strength and annotation policy, then evaluate new prompts. This separates useful retention from selection on these sixteen examples.
4. **Capture concern:** a future authorized full-size BF16 parity check should compare hooked/unhooked generation and reconstructed prefill logits. No such run was performed here.

### Compact ml-debug assessment

- Config/log: complete run read; residual24, k32, mask1, strengths 1 and 0.5; elapsed 18.93 seconds. GPU memory absent.
- SHOULD: masking should improve joint recovery over unmasked methods. Logged lexical counts support that comparison, not exhaustive semantic exclusion.
- Baselines/nulls: plain24 and masked/plain27 controls present; random/shuffled semantic baseline and independent seed/prompt spread absent.
- Training/init/LR/gradient diagnostics: not applicable; no fitting in this run.
- Competing explanations, nonexclusive subjective confidence: incomplete semantic scorer coverage **>95%**; answer-target mismatch **>95%**; broad category/association shortcut **70%**; material capture implementation defect **10%** given static code and tiny-model tests. Unknown full-size/provenance effects remain unquantified.
- This single implementation does not settle whether suppressed-concept readout is possible. No further reviewer was launched.

## Limits and inspection targets

Manual multilingual interpretation is fallible; ambiguous young-animal terms remain unresolved. No formal adjudicated semantic rate, statistical superiority, internal-reasoning claim, or generalization claim is established.

`/workspace/2026/suppressed-activations/slop/audits/2026-09-30_readout-blind-rows.jsonl`

`/workspace/2026/suppressed-activations/out/2026-09-30_123008_jlens-one-pass/source.py:319`

`/workspace/2026/suppressed-activations/out/2026-09-30_123008_jlens-one-pass/erasure_traces.json`

`/workspace/2026/suppressed-activations/out/2026-09-30_123008_jlens-one-pass/run.md:1260`