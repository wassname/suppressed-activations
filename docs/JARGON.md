# Jargon: which words the README uses

One word per idea, used the same way everywhere. Prefer the J-lens paper's terms
([Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/)), because it is the main source and it is
careful about what it claims. Evidence for each choice: [`slop/research/2026-10-06_framing_from_papers.md`](../slop/research/2026-10-06_framing_from_papers.md).

| say | meaning here | instead of | why |
|:----|:-------------|:-----------|:----|
| **unspoken concept** | something the model represents in its middle layers that is not in the input or the output | hidden thought, suppressed activation | J-lens paper: "unspoken words", "unspoken intermediate concept". Covers more than words |
| **unspoken word** | an unspoken concept that we can read out as a word; what the score checks | hidden word, hidden English, latent word | J-lens paper: "unspoken words, neither pure echoes of the input nor predictions of the next token". "Hidden" clashes with "hidden states" |
| **read / think / say** | the three parts of what activations can hold: the input, the unspoken concepts, the next output | input / latent / output space | plain words for the J-lens split. Say "can mix", not "every activation mixes" (no paper shows that activations separate into exactly these three parts) |
| **work in English** | only in the title, as a question: a callback to *Do Llamas Work in English?* and the global *work*space | as a finding ("Qwen works in English") | a question claims nothing; the finding is "concepts biased toward English" |
| **think, thoughts** | only as an analogy, in the read/think/say line and in wassname's goal paragraph | as a claim ("the model thinks X") | J-lens paper uses "thought processes" but treats it as an analogy |
| **concepts biased toward English** | why the unspoken words often come out in English | "thinks in English" | Wendler et al.: "the model's internal lingua franca is not English but concepts—concepts that are biased toward English" |
| **activations** | the numbers inside the model at each layer, for one prompt | residual stream, hidden states | define once; "residual stream" only in code |
| **subspace** | a set of directions in the activations | J-space, workspace | "J-space" and "workspace" are the paper's names for what they found with their lens; we cite them, we don't claim to find them |
| **method** | one function that turns activations into a vector | transform, geometry, entry | "entry" only for a submitted method; `@geometry` only in code |
| **output head** | the model's last matrix, which turns activations into word scores | unembedding, W_U, logit lens | rules need it; define once |
| **dictionary** | any word list, token list, translation table, or use of the output head inside a method | | the rule in one word |
| **input-language / output-language words** | words in the language being translated from / to | leak, false positive, FP | what the score penalises |
| **logit lens, J-lens** | not in the README text; only in the notebook and `docs/leaderboard.md` | | readers need the examples, not the tools |
| **suppression neurons, suppressed activations** | only in the background block: how the project started | in the title or main text | Gurnee 2024's suppression neurons are fixed neurons that push token groups down; the J-lens paper uses "suppressed" for an ablation. Both read as "an edit" |

Words to avoid outright: "latent" (jargon), "hidden" for the target (clashes with hidden states), "suppressed" for the
target (reads as an edit), "workspace" as our claim (needs causal tests we don't run).

<!-- Draft by PI/OpenAI, 2026-10-06, from the researcher's paper reading; not approved yet. -->
