# Unspoken Concepts Challenge

<!-- Generated from README.qmd by `just docs`; edit README.qmd, not this file. -->

<img src="figs/cartoon.png" data-fig-alt="Cartoon. Title: Translating Arabic to Russian, the model thinks partly in English. Subtitle: Challenge: find the thinking part, without using a dictionary. Three shaded curves over layers: grey READ: Arabic, شاي (tea), high early, arrow not this; orange THINK: English, tea drink coffee vodka, peaking in the middle, arrow find this; blue SAY: Russian, чай (tea), rising at the end, arrow or this. The curves are drawn by hand; the English words are a real readout." alt="Cartoon. Title: Translating Arabic to Russian, the model thinks partly in English. Subtitle: Challenge: find the thinking part, without using a dictionary. Three shaded curves over layers: grey READ: Arabic, شاي (tea), high early, arrow not this; orange THINK: English, tea drink coffee vodka, peaking in the middle, arrow find this; blue SAY: Russian, чай (tea), rising at the end, arrow or this. The curves are drawn by hand; the English words are a real readout." width="720" />

Figure 1: **The challenge.** The model reads Arabic and says Russian; part of what it thinks in between can be read as English. The curves are drawn by hand; the English words are a real readout (J-lens, layer 23, Arabic→Russian "tea").

In AI models we want to find where they process their concepts. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable matrices. The problem is that we don't understand how to read them.

These giant matrices are called activations, and they can mix what the model reads, what it is thinking, and what it is about to say. This makes it difficult to disentangle them, but this challenge uses a simple translation setting to separate them. This lets us invite participants to find a way to isolate the activations, in the residual stream, that do the thinking but are never verbalised.

If we could read and understand the model's concepts, it would improve many things. It would allow us to interpret, steer, and align models on their own concepts. Even getting closer will help with challenges like fragile chain of thought ([Korbak *et al.*, 2025](<https://arxiv.org/abs/2507.11473>)), eval awareness ([Needham *et al.*, 2025](<https://arxiv.org/abs/2505.23836>)), and alignment ([Marks *et al.*, 2025](<https://arxiv.org/abs/2503.10965>)); ([Clark, 2026](<https://wassname.com/agenda-character.html>)).

## Unspoken concepts

Wes Gurnee and colleagues at Anthropic showed that models represent words in their middle layers that they never say. They describe ([Gurnee *et al.*, 2026](<https://transformer-circuits.pub/2026/workspace/>)):

> a small, evolving set of unspoken words, neither pure echoes of the input nor predictions of the next token, naming the concepts the model is currently reasoning with

Similar to their Figure 12, where they show that a model will think the word spider without ever saying it, we show a multilingual version (Table 1). Spider, in any language, is in **bold**; the answer, eight, is in *italics*.

Table 1: **Qwen reads an Arabic question, thinks spider in English, and says 8.** J-lens readout at the last prompt token, top 8 words, verbatim.

|  | model | English\* |
|:---|:---|:---|
| **input** | سؤال: كم عدد أرجل الطائر؟<br>Ответ: два<br>سؤال: كم عدد أرجل الحيوان الذي يغزل شبكة من خيوط الحرير؟<br>Ответ: | Question: How many legs does a bird have?<br>Answer: two<br>Question: How many legs does the animal that spins a web from silk threads have?<br>Answer: |
| **thoughts**, layer 22 | insects **spiders** insect ？ 昆虫 3 。 2 | insects **spiders** insect ? insect 3 . 2 |
| layer 24 | **spiders** **spider** **蜘蛛** **蛛** insects claws 爬 legs | **spiders** **spider** **spider** **spider** insects claws crawl legs |
| layer 26 | legs **spiders** **spider** eyes **蜘蛛** limbs venom claws | legs **spiders** **spider** eyes **spider** limbs venom claws |
| layer 28 | legs leg 腿 -leg \_leg -legged *eight* 腿部 | legs leg leg -leg \_leg -legged *eight* leg |
| layer 30 | *eight* *8* *八* *-eight* *восемь* six *八个* *huit* | *eight* *8* *eight* *-eight* *eight* six *eight* *eight* |
| **output** | *8* | *8* |

As you can see, while Llamas work in English, Qwens also work in Chinese.

\*marked English translations for illustration only; the model does not see them, think them, or output them in English

Following Animorphs ([Applegate, 1996](<https://en.wikipedia.org/wiki/Animorphs>)), which uses braces `⟨ ⟩` to mark mental communication, we use the same notation for internal readouts of the models activations.

## The setting: translation

In the notable paper "Do Llamas Work in English?" ([Wendler *et al.*, 2024](<https://arxiv.org/abs/2402.10588>)), Wendler and colleagues found that when a model translates from one language to another, it thinks in its native language, the language of the internet: English (and, as it turns out, Qwen also works in Chinese). When a multilingual model translates between two non-English languages, say Arabic to Russian, it takes a detour through English along the way. They are careful about what that means: "the model's internal lingua franca is not English but concepts—concepts that are biased toward English."

For us this is a helpful way to narrow in on where the model does its thinking. We want to find the subspace of the activations in the residual stream. And those activations should contain English, but not Arabic or Russian.

We use Qwen3.5-4B, a model trained mostly on English and Chinese. We test translation between Arabic, Russian, Hindi, Thai and Korean, and we use Arabic to Russian as the example throughout. These languages are fairly distant from English, with few tokens in common. We never use English or Chinese as the input or output language, but if the unspoken word shows up in either, we count it.

<details>

<summary>

How this started

</summary>

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52) "suppression neurons" ([Gurnee *et al.*, 2024](<https://arxiv.org/abs/2401.12181>)) (neurons that push down a group of related words) can be found in the residual stream.

For the test, I tried to isolate the suppressed English from the output language in the "Do Llamas Work in English?" plot.

<img width="480" alt="Line plot from Wendler et al. (2024), Figure 2: Llama-2-70B translating into Chinese. x-axis: layer 0 to 80; y-axis: logit-lens probability 0 to 1. The English word (orange) is near zero until layer 40, rises to about 0.4 by layer 50, stays there, then falls to zero by layer 80. The Chinese answer (blue) stays near zero until layer 60 and rises to about 0.5 at layer 80. A colour bar on top shows entropy falling from high to low around layer 45." src="https://arxiv.org/html/2402.10588v4/70b_zh_probas_ent.png" />

*Llama-2-70B translating into Chinese ([Wendler et al. 2024](https://arxiv.org/html/2402.10588v4), Fig. 2): the English word (orange) rises mid-network, then falls as the Chinese answer (blue) rises.*

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

</details>

## The rules

Of course we can't cheat and looking up English words. We are looking for a way to find the model's concepts, and it should even work when deployed to an English chat interface, or other settings where the languages of the input, output, and intermediate are mixed. So proposed solutions should use this interface:

``` python
def calibrate(texts: Iterable[Float[Tensor, "layers tokens d"]]) -> dict:
    # texts: unlabelled text, layers 16 to 32 (WikiText, and the dev prompts without their answers)
    mean = torch.stack([hs[:, -1].mean(0) for hs in texts]).mean(0)
    return {"mean": mean}

def method(hs: Float[Tensor, "layers tokens d"], state: dict) -> Float[Tensor, "d"]:
    # hs: the residual stream for one prompt, layers 16 to 32, all prompt tokens
    # state: what calibrate() returned; you may also use any model weights, including the output head as a matrix
    v = hs[:, -1].mean(0) - state["mean"]
    return v  # one residual-stream vector, which should hold the unspoken concept and not the input or output
```

*Note this uses [JaxTyping](https://github.com/patrick-kidger/jaxtyping) syntax to show tensor shapes.*

The method has to find the place in the activations. We can't assume we know the best layer for a new model, so the method gets the last half of the layers and has to work out which layer, or mix of layers, to use.

The returned vector should happen to hold the unspoken concept. We read it with the model's output head and keep the top 8 words. A prompt succeeds if the unspoken word is among them and no input- or output-language word is. The score is F1 over prompts: 1.00 means every prompt succeeded. You may use the output head as a matrix, for example its main directions, but not to score individual words.

Each method has one fixed setting (for example a rank). You can try settings on the dev pair, Russian to Korean; we only report the test pairs.

## Leaderboard

Please submit your own as an issue or PR!

| method | by | F1↑ | 90% CI | Δ vs random | found↑ | showed input/output words↓ | fitted on |
|:---|:---|---:|---:|---:|---:|---:|:---|
| [minus ends, least-explained layer](scripts/challenge/transforms.py#L167 "As 'minus ends', but keep the one layer the two states explain least (picked per prompt, no labels)") |  | **0.82** | 0.80–0.85 | +0.21 (+0.17 to +0.25) | 93% | 33% | nothing |
| [minus ends](scripts/challenge/transforms.py#L162 "Layers 17-31 minus the span of this prompt's layer-16 and output-layer states, averaged") |  | 0.79 | 0.77–0.82 | +0.18 (+0.14 to +0.22) | 92% | 40% | nothing |
| [minus ends, recent tokens](scripts/challenge/transforms.py#L174 "As 'minus ends', but average the layer-16 and output states over the last 8 tokens first") | [Sandy Fraser](https://github.com/z0u) | 0.79 | 0.76–0.81 | +0.17 (+0.13 to +0.21) | 91% | 41% | nothing |
| [layer-change PCA](scripts/challenge/transforms.py#L123 "Each layer projected on the top PCs of that layer's change on calibration text, averaged over layers 16-31") |  | 0.78 | 0.76–0.80 | +0.16 (+0.13 to +0.20) | 93% | 46% | calibration text |
| [net-change PCA](scripts/challenge/transforms.py#L130 "Mean over layers, projected on the top PCs of h32 - h16 on calibration text (AntiPaSTO without the output-head step)") |  | 0.78 | 0.76–0.80 | +0.16 (+0.13 to +0.20) | **95%** | 49% | calibration text |
| [minus output PCA](scripts/challenge/transforms.py#L147 "Mean over layers, minus the top PCs of output-layer activations on calibration text") |  | 0.77 | 0.75–0.79 | +0.15 (+0.12 to +0.19) | **95%** | 53% | calibration text |
| [AntiPaSTO subspace](scripts/challenge/transforms.py#L136 "Mean over layers, projected on AntiPaSTO's suppressed subspace (github.com/wassname/AntiPaSTO)") |  | 0.76 | 0.73–0.79 | +0.15 (+0.10 to +0.19) | 78% | 28% | calibration text |
| *[mean over layers](scripts/challenge/transforms.py#L108 "Logit lens of the last token, averaged over layers 16-32 (control)")* |  | 0.72 | 0.70–0.74 | +0.11 (+0.07 to +0.15) | 93% | 65% | nothing |
| *[random subspace](scripts/challenge/transforms.py#L113 "Mean over layers, projected on a random rank-1024 subspace (control)")* |  | 0.61 | 0.57–0.65 |  | 65% | 47% | random seed |
| [weak head directions](scripts/challenge/transforms.py#L142 "Mean over layers, projected on the directions the output head reads least") |  | 0.23 | 0.18–0.28 | -0.38 (-0.44 to -0.32) | 22% | 69% | nothing |
| *[mean calibration text](scripts/challenge/transforms.py#L118 "Ignores the prompt: the mean layer-28 activation on calibration text (control)")* |  | 0.00 | 0.00–0.00 | -0.61 (-0.65 to -0.57) | 0% | **0%** | calibration text |

Qwen3.5-4B, 209 test prompts (ar→ru, ar→hi, hi→th, th→ru, ko→ar). 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random subspace on the same prompts. Hover a name for what it does. [Per-prompt rows](out/2026-10-06_152532_leaderboard/rows.json.gz), commit 456c320e.

Methods that use token scores or the J-lens are in the [reference table](docs/leaderboard/README.md).

The best geometry method so far, "minus ends, least-explained layer", gets F1 0.82 without being told the layer. The plain logit lens at a layer picked by hand gets 0.85, and methods that read word scores get up to 0.96 (reference table).

<img src="figs/layers.png" id="fig-layers" data-fig-alt="One panel over layers 16 to 31. Shaded areas: logit-lens probability of input-language words (grey), the unspoken word (orange, peaking near layer 28) and output-language words (blue, rising at layers 30 to 31). Green lines: share of prompts where the method finds the unspoken word with nothing leaked; red lines: share where input- or output-language words show; solid for minus ends, dashed for the plain logit lens." alt="Where the unspoken word is, and how often a method gets it cleanly. Shaded: our cartoon with real data, the logit-lens probability of input-language words (READ), the unspoken word (THINK) and output-language words (SAY), averaged over the test prompts. Lines: share of prompts where the top 8 words hold the unspoken word and nothing leaked (green), and where they show input- or output-language words (red), for &quot;minus ends&quot; at each layer (solid) and the plain logit lens (dashed). Made by notebook.py, Part 2." />

## Enter

Add your method to [`transforms.py`](scripts/challenge/transforms.py) with `@geometry`, and anything it needs from calibration text to `calibrate()`. Run `uv run scripts/challenge/score.py` on one GPU (it downloads the model and data on first run), and open an issue or a pull request with your method and its score.

## Limitations

**Single tokens.** We are searching for concepts, but because we don't know where they are, we limit ourselves to scoring single-token words as a proxy. This is supported by both papers we build on: Wendler et al. found the English detour using single-token words, and the J-lens reads out one token at a time, yet Gurnee et al. find it "is sufficient to uncover a great deal of important structure." They name the same gap ([Gurnee *et al.*, 2026](<https://transformer-circuits.pub/2026/workspace/>)):

> The Jacobian lens is an imperfect tool, which we believe only approximately and incompletely captures the model's underlying workspace structure. **For instance, it only identifies vectors associated with concepts that correspond to single tokens in the model's vocabulary, but many important concepts correspond to multiple tokens**

**English and Chinese only.** We look for all concepts, including ones that belong to no language, but we only score the ones that show up as English or Chinese words. So a method that hill-climbs this score might overfit to English and do poorly on other concepts.

**Simple tasks.** Like Wendler et al., our tasks are simple. They say of theirs that the tasks "provide a highly controlled, yet toy-like, context for studying the internal language of LLMs."

## Related work

- Dumas *et al.* ([2024](<https://arxiv.org/abs/2411.08745>)) use the same word-translation setup and patch activations: "we can change the concept without changing the language and vice versa through activation patching alone."
- Bayazit *et al.* ([2026](<https://arxiv.org/abs/2609.00155>)) compare probes: "decoding-based probes, which rely on output-space decodability, retain sharper language-specific and more English-biased signals."
- Schut *et al.* ([2025](<https://arxiv.org/abs/2502.15603>)) find an English pivot in open-ended generation.
- Wu *et al.* ([2024](<https://arxiv.org/abs/2411.04986>)) describe a shared middle-layer "semantic hub" across languages.
- Zhong *et al.* ([2025](<https://aclanthology.org/2025.findings-acl.1350/>)) find that models trained on several languages can use more than one latent language.
- Patchscopes ([Ghandeharioun *et al.*, 2024](<https://arxiv.org/abs/2401.06102>)), LatentQA ([Pan *et al.*, 2024](<https://arxiv.org/abs/2412.08686>)) and the tuned lens ([Belrose *et al.*, 2023](<https://arxiv.org/abs/2303.08112>)) are other readouts.

## Citation

If you use the method or figure, please cite [`CITATION.cff`](CITATION.cff). GitHub exposes this as *Cite this repository* button.
