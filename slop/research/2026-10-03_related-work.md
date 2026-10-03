# Related work for the "find where llamas work" challenge

PI/OpenAI, 2026-10-03. Search via copilot_search (GitHub Copilot web search); every arXiv ID below was checked against the arXiv API (title matches). Abstract quotes are from the arXiv API. One-line summaries not in quotes are Copilot's, not checked against the full papers.

## Has anyone run this challenge?

Not that I found: there is no leaderboard of label-free transforms scored on translation and then applied to English-only tasks. The search summary says: "There is not yet one universally accepted benchmark that directly measures arbitrary hidden/unverbalized thoughts." The closest pieces are below.

## Closest work

| paper | relation to us |
|---|---|
| [Dumas et al. 2024, Separating Tongue from Thought](https://arxiv.org/abs/2411.08745) (Wendler co-author) | Same word-translation setup. Shows by patching that concept and output language are separable: "we can change the concept without changing the language and vice versa through activation patching alone." Causal, but not a readout transform. |
| [Bayazit, AlKhamissi, Bosselut 2026, Lingua Franca or Probing Artifact?](https://arxiv.org/abs/2609.00155) | Warns that the "latent language" depends on the probe: "decoding-based probes, which rely on output-space decodability, retain sharper language-specific and more English-biased signals." All our rows read through the output head, so this applies to us. |
| [Schut, Gal, Farquhar 2025, Do Multilingual LLMs Think In English?](https://arxiv.org/abs/2502.15603) | English-pivot result for open-ended generation; English-derived steering vectors work better than target-language ones. |
| [Wu et al. 2024, The Semantic Hub Hypothesis](https://arxiv.org/abs/2411.04986) | Shared middle-layer semantic space across languages and modalities. |
| [Zhong et al. 2025, non-English-centric LLMs](https://aclanthology.org/2025.findings-acl.1350/); [Trinley et al. 2025, Aya-23](https://arxiv.org/abs/2507.20279) | Balanced multilingual models use several latent languages, not only English. Qwen may use Chinese too, which is why Chinese counts as hidden. |
| [Tezuka & Inoue 2025, Transfer Neurons](https://arxiv.org/abs/2509.17030) | MLP neurons that move representations into and out of a shared space; candidate source of a subspace. |
| [Separating Syntax from Language 2026](https://arxiv.org/abs/2609.01356) | Splits output production into word order and surface language. |
| [Gurnee et al. 2026, Global Workspace / Jacobian lens](https://transformer-circuits.pub/2026/workspace/) | The J-lens used here; concept swaps in J-lens coordinates. |
| [Yang et al. 2024, latent multi-hop reasoning (TwoHopFact)](https://aclanthology.org/2024.acl-long.550.pdf) and SOCRATES in the [same repo](https://github.com/google-deepmind/latent-multi-hop-reasoning) | Our English transfer set uses TwoHopFact. Copilot says SOCRATES is a filtered successor with fewer shortcuts (not checked). |
| [Patchscopes 2024](https://arxiv.org/abs/2401.06102), [LatentQA 2024](https://arxiv.org/abs/2412.08686), [Tuned lens 2023](https://arxiv.org/abs/2303.08112) | Other readouts. Patchscopes and LatentQA decode with a second prompt or a trained decoder, so they are not one-pass transforms; the tuned lens is trained to predict the final output, so it would score as "said". |

## Do we need a related-work section?

For sharing, a short one helps: 4 to 6 links, saying what is new here, which is the leaderboard and the "no language lookup" rule. Dumas et al. and Bayazit et al. are the two a reader would ask about first.
