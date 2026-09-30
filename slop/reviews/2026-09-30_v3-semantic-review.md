# Blind semantic audit — 48 rows

Read all 48 rows and every top32 entry. Method identities remained unknown; no key, README, result summary, or prior interpretation was consulted.

**Result:** strict joint passes with **no observed definite leak**: **M0 0/16; M1 2/16; M2 7/16**. These are descriptive annotations, not proof of exhaustive semantic exclusion or evidence of internal reasoning.

## Rules

- **H:** hidden concept recovery: **P** definite, **F** not recovered, **U** ambiguous.
- **I/O:** exclusion of input words / actually generated initial answer: **F** definite leakage; **P** no observed definite leakage. Ambiguous fragments are recorded separately, not silently counted as definite.
- **Joint:** P requires H=P and I=O=P. An unresolved hidden identification without another definite failure receives U.
- Word identity includes inflection, punctuation wrapping, clear translations and aliases. Related concepts alone do not qualify.
- The shared Japan/Tokyo example is input. Generation scaffolding after the initial answer is not treated as the answer.
- Quotes below preserve token text, except incidental leading spaces. A quoted witness is sufficient to establish failure; it is not necessarily the only witness.

Source for every row: `/workspace/2026/suppressed-activations/slop/audits/2026-09-30_v3-semantic-blind-rows.jsonl`; **L** is its line number.

## Complete annotation table

| L | Method | Hidden concept | Actual answer | H: decisive evidence | I: decisive evidence | O: decisive evidence | Ambiguous / related, not counted as definite | Joint |
|---:|:---:|---|---|---|---|---|---|:---:|
| 1 | M1 | Finland | Helsinki | F: absent | P | P | “stad” = city, not Finland or capital; “located” related to containing | F |
| 2 | M2 | Netherlands | Amsterdam | P: “Netherlands” | P | P | “City” is broader than capital | P |
| 3 | M1 | bear | honey | P: “bears” | P | P | “ney” could finish honey, but also many other words; not diagnostic | P |
| 4 | M1 | Chile | Santiago | F: absent | F: “省会” contains capital meaning, qualified as provincial capital | P | “lima” is another capital; “Chin” not Chile | F |
| 5 | M0 | Sweden | Stockholm | P: “Sweden”, “瑞典”, “Sverige” | F: “capitals” ← capital | P | “ストック”, “.stock”, “Сто” could begin Stockholm but are ambiguous; “Thụy” incomplete country translation | F |
| 6 | M0 | bear | honey | P: “bear”, “bears” | F: “甜的”, “甜甜的” ← sweet | F: “miel”, “蜂蜜” = honey | “treats” related food; “蜂巢” = hive, not honey | F |
| 7 | M1 | Peru | Lima | F: absent | F: “省会” contains qualified capital meaning | P | “rome” another capital; “Chin” not Peru | F |
| 8 | M0 | Netherlands | Amsterdam | P: “荷兰”, “Netherlands” | F: “capitals”, “Capitals” | P | “terdam” shared by Rotterdam/Amsterdam; “дам” ambiguous; “鹿” alone not Rotterdam | F |
| 9 | M0 | rabbit | carrot | F: absent | F: “roots”, “_root”, “raíz”, “根” ← root | P | “tuber” related vegetable category; “icama” suggests jicama, not carrot | F |
| 10 | M0 | Finland | Helsinki | P: “Finland”, “芬兰” | F: “capitale”, “首都” ← capital | P | “赫尔” could begin Helsinki, but other names too; “Fin” alone ambiguous | F |
| 11 | M0 | bat | mammals | F: absent | F: “animals” ← animal; “飞行” ← flying | P | Birds, orders, “noct”, “Verte” are related categories/fragments, not bat or mammals | F |
| 12 | M0 | Denmark | Copenhagen | P: “DK” country-code alias | F: “capitals”, “首都”, “-capital” | F: “København” = Copenhagen | “Den”, “デン” ambiguous alone; recovery relies on DK, not these fragments | F |
| 13 | M1 | beetle | **4** | F: absent | F: “(number”, “:number”, “.numberOf” ← number | P | “spinner” not beetle; no four equivalent | F |
| 14 | M2 | Italy | Rome | P: “Italy” | P | P | Bologna is another Italian city, not Rome | P |
| 15 | M0 | Chile | Santiago | F: absent | F: “capitals”, “首都”, “Hauptstadt” | P | “Ch” not diagnostic Chile; “地亚”, “圣”, “大圣” insufficient for Santiago | F |
| 16 | M1 | crab | 10 | F: absent | F: “shells”, “殼” ← shell; “_number” ← number | P | “exactly”, “multiplied” are numerical relations, not ten | F |
| 17 | M0 | crab | 10 | F: absent | F: “totaled” ← total | P | “الأرج” may begin Arabic legs; “exactly”, “greater” not ten | F |
| 18 | M2 | Chile | Santiago | F: absent | P | P | “Buenos”, “Ciudad”, other cities do not identify Chile or Santiago | F |
| 19 | M1 | butterfly | caterpillar | F: absent | F: “larvae” ← larval; “insects” ← insect; “stade”, “стадии” ← stage | P | “ướ” may occur in Vietnamese butterfly but is not diagnostic; “crawler”, larvae are not uniquely caterpillar | F |
| 20 | M2 | butterfly | caterpillar | P: “butterfly”, “butterflies” | F: “larvae”, “insects” | P | “worms”, “nymph”, “baby” are not identical to caterpillar | F |
| 21 | M2 | Switzerland | Bern | P: “Switzerland” | P | P | Zurich/Zürich not Bern | P |
| 22 | M2 | bear | honey | U: “Teddy” suggests teddy bear, but can be a personal name | F: “sweets” ← sweet | P | “candy”, chocolates and other foods not honey; “Rabbit” not bear | F |
| 23 | M0 | snake | **4** | P: “snakes”, “snake” | F: “tongues”, “舌头” ← tongue; “.numberOf” | P | “zero”, “ZERO” are **not** leaks of the generated four | F |
| 24 | M0 | Peru | Lima | P: “秘鲁” = Peru | F: “capitals”, “首都”, “Hauptstadt” | P | “usco”, “クス” suggest Cusco but are incomplete; “Lime” not a clear Lima alias | F |
| 25 | M1 | whale | **gills** | F: absent | F: “organs” ← organ; “breathed”, “breathe” ← breathing | P | “lungs” is not gills; underwater/swimming do not identify whale | F |
| 26 | M0 | whale | **gills** | F: absent | F: “organs”, “органами” ← organ; “breathe” ← breathing | P | “bale”, “Kasat” suggest whale-related words but are ambiguous; lungs/肺 are not gills | F |
| 27 | M1 | rabbit | carrot | F: absent | F: “roots”, “_root”, “-root”, “根” | P | “rots” could finish carrots but is independently a word; “ikon” not diagnostic | F |
| 28 | M1 | Netherlands | Amsterdam | P: “荷兰” = Netherlands | P | P | “鹿” alone is deer, not definite Rotterdam; “Haga”, “stad” related geography | P |
| 29 | M2 | rabbit | carrot | F: absent | F: “roots”, “Roots”, “vegetables”, “根” | P | “萝卜” = radish/turnip, not unambiguous carrot; “tuber” related | F |
| 30 | M2 | Finland | Helsinki | P: “Finland” | P | P | Other countries/cities are not Helsinki | P |
| 31 | M2 | Peru | Lima | P: “Peru” | P | P | Other capitals are not Lima | P |
| 32 | M0 | Switzerland | Bern | P: “瑞士” = Switzerland | F: “capitals”, “首都”, “Hauptstadt” | P | “日内” suggests Geneva translation but also means within the day; “Жен”, “_gene” ambiguous | F |
| 33 | M0 | Italy | Rome | F: absent | F: “capitals”, “首都”; **“东京” = shared-example Tokyo** | P | Other capitals, including Beijing and Washington, do not identify Italy/Rome | F |
| 34 | M0 | beetle | **4** | F: absent | F: “_leg”, “.numberOf”, “NumberOf” | F: “four”, “FOUR”, “fours”, “四条” | “ZERO” is an alternative answer, not the generated answer | F |
| 35 | M2 | Sweden | Stockholm | P: “Sweden” | P | P | Rotterdam is not input Gothenburg; other capitals are not Stockholm | P |
| 36 | M2 | bat | mammals | F: absent | F: “animals”, “Animals”, “animals” | P | “creatures”, “beasts” broader than mammals; birds/insects not bat | F |
| 37 | M2 | beetle | **4** | F: absent | F: “animals”, “Animals”, “的动物” ← animal | F: “four”, “fours”, “FOUR”, “四条” | “six” is not substituted for generated four | F |
| 38 | M1 | Sweden | Stockholm | U: “Thụy” incomplete; can occur in Vietnamese Sweden **or Switzerland** | P | P | “Haga” not uniquely Sweden; “stad” city; “called” is not in this prompt | U |
| 39 | M2 | crab | 10 | F: absent | P | P | “counted” related to number/total, not identical; other number words exclude ten | F |
| 40 | M2 | Denmark | Copenhagen | P: “Denmark” | P | P | Other capitals are not Copenhagen | P |
| 41 | M1 | Switzerland | Bern | F: absent | F: “/is” ← is | P | “日内” incomplete/ambiguous Geneva; “Luân” not Bern or Switzerland | F |
| 42 | M2 | whale | **gills** | P: “whales”, “whale”, “鲸” | F: “oceans” ← ocean | P | “lungs”, other organs and body parts are not gills; “respiratory” related to breathing | F |
| 43 | M0 | butterfly | caterpillar | F: absent | F: “larvae”, “insects”; “называется” ← is called | P | “หนอน” = worm/larva broadly; “crawler”, “worm”, “ấu” not uniquely caterpillar; “蛹” pupa | F |
| 44 | M2 | snake | **4** | P: “snakes” | F: “(number” ← number | P | Alternative number words do not include four; Gecko/lizard are not snake aliases | F |
| 45 | M1 | bat | mammals | F: absent | F: “属” ← belongs; “Flight”, “-flight” express flying | P | “哺乳” = suckling/lactation, also prefix of mammal; not unambiguous mammals alone. “superclass”, orders related to class | F |
| 46 | M1 | snake | **4** | F: absent | F: “:number”, “(number”, “.numberOf” | P | Gecko, “shed”, “licked” associated with reptiles but do not identify snake | F |
| 47 | M1 | Denmark | Copenhagen | F: absent | P | P | “stad” city; “Haga”, “lima” other geography; “greve” ambiguous | F |
| 48 | M1 | Italy | Rome | F: absent | P | P | “oglio” Italian-looking fragment, not Italy; “北京” Beijing is neither Tokyo nor Rome | F |

## Aggregates

Counts are over **all 16 rows per method**, including wrong initial answers.

| Method | Hidden P | Hidden U | Hidden F | Definite input leak | Definite answer leak | Joint P: no observed definite leak | Joint U | Joint F |
|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M0 | 8 | 0 | 8 | 16 | 3 | 0/16 | 0 | 16 |
| M1 | 2 | 1 | 13 | 10 | 0 | 2/16 | 1 | 13 |
| M2 | 10 | 1 | 5 | 7 | 1 | 7/16 | 0 | 9 |
| **Total** | **20** | **2** | **26** | **33** | **4** | **9/48** | **1** | **38** |

Joint-pass rows:
- **M1:** bear L3; Netherlands L28.
- **M2:** Netherlands L2; Italy L14; Switzerland L21; Finland L30; Peru L31; Sweden L35; Denmark L40.

## Interpretation and checks

### Observed

- M0 recovers eight hidden concepts, but every row exposes input-word content.
- All four definite answer-leak rows have direct semantic witnesses: honey translations, Copenhagen’s Danish name, or words for the **actually generated four**.
- Wrong answers remain material: beetle and snake generated **4**; whale generated **gills**. Lungs and zero therefore do **not** establish output leakage in those rows.
- The shared example matters: M0/Italy exposes “东京” despite Tokyo not belonging to that case’s target geography.
- Recovery rates alone miss the joint requirement: M2 butterfly, whale and snake recover their concepts but also leak input.

### Uncertainty and possible disconfirmation

- **Qualified capital translations:** “省会” means provincial capital, not unrestricted national capital. I counted its explicit capital component as lexical input leakage, not as complete semantic equivalence of the phrases. Rejecting that compositional rule removes M1 input-leak flags at L4/L7, but neither becomes a joint pass because Chile/Peru remain unrecovered.
- **Country code:** M0/Denmark recovery depends on accepting “DK” as the clear country-code alias. A policy requiring full names would downgrade H, without changing its joint failure.
- **Fragments:** “ney”, “terdam”, “赫尔”, “ストック”, “日内”, “Thụy” and “哺乳” can invite completion from context. The displayed fragments do not uniquely establish those completions. A bilingual lexical adjudication could revise their ambiguity status; adjoining top32 candidates are ranked alternatives, not a generated phrase.
- **Multilingual breadth:** a missed definite translation could reduce the reported no-observed-leak pass count. In particular, the two M1 passes retain ambiguous fragment caveats. They are not certified semantic exclusion.
- Nothing here distinguishes a genuine hidden intermediate from association, prompt-topic readout, or candidate-list breadth. The data establish visible word identities, not causal mediation or actual internal reasoning.

## ML-debug evidence boundary

| Check | Evidence / limitation |
|---|---|
| Full data inspection | All 48 supplied rows; all 32 candidates per row, 1,536 entries total |
| Example linking input, answer and readout | L34: input includes “number of legs”; generation begins “4.”; readout includes “.numberOf”, “_leg”, “four” |
| Null / baseline scale | No random, shuffled or separate baseline-readout control supplied; no chance-adjusted claim |
| Configuration, training, gradients, schedules, timing, memory | Not present in the permitted artifact; unknown, not inferred |
| Alternative explanations | Association rather than hidden reasoning; multilingual exclusion gaps; differing candidate-list specificity |
| Distinguishing checks | Bilingual adjudication of flagged fragments tests lexical labels; matched association controls and causal tests would be needed for reasoning claims |
| Execution | File reads only; no commands, edits, model calls, network access or delegation |

This is an independent annotation audit, **not project-goal sign-off**.

— **PI/OpenAI**