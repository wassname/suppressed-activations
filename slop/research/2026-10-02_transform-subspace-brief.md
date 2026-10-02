# Brief: transforms or subspaces that read "thought but not said" content

Author: PI/OpenAI (for oracle consultation). Please answer in about one page.

## Goal

Find a fixed readout transform or subspace for a language model's residual stream that returns what the model computes internally but does not say. Score: per-prompt F1 of the top-k vocabulary list against the hidden word, while the spoken word and input words stay out of the list.

Training/selection setting: word translation (e.g. French→Chinese) in Qwen3.5-4B. The intermediate English word is the hidden word; language labels are used only for scoring, never by the method. Evaluation setting: English-only two-step questions, where input, hidden word and output are all English, e.g. "The capital of the country containing Gothenburg is" (hidden Sweden, said Stockholm), "The day after the weekday named after Thor is" (hidden Thursday). A method that works by detecting "English tokens" therefore cannot transfer.

## Constraints

- One forward pass on the current input. Reusable offline fitting on other data is allowed.
- No labels at inference. Language labels only for scoring.
- Local single 24 GB GPU; jobs of a few minutes.
- Available: per-layer residual stream at all positions, the model's weights, a pretrained Jacobian lens (averaged Jacobian from layer l to the final layer, fitted on 1000 WikiText prompts; readout = W_U norm(J_l h_l)).

## Observations (last prompt token, top-8, input-word filter only unless stated)

| readout | translation F1@8 (48) | English v3 F1@8 (16) | English v4 F1@8 (8) |
|---|---:|---:|---:|
| plain logit lens, layer 27 | .446 | .056 | .113 |
| Jacobian lens, layer 29 | .461 | .133 | .170 |
| per-prompt rise-and-fall: tokens whose logit rises L22→27 and falls 27→32 | .164 (top-32) | 0 | 0 |
| fixed subspace: top-k eigvecs of Cov(rms h27) − Cov(rms h32), 300 WikiText texts, k=16…1024 | 0 to .176 | 0 | 0 |
| same, whitened (generalised eig, smallest kept-variance fraction) | 0 to .205 | ≤.01 | ≤.01 |

- Without an output-word filter, the spoken answer is in the plain-lens top 8 for 11/16 English v3 prompts. The J-lens at layer 29 has it in 14/16. In English, excluding speech is the main difficulty, not finding the hidden word.
- Removing more final-layer predicted words (top 5 or 20) barely changes translation but removes the hidden word in English (v4 F1 .184 → .061).
- Reading at the end of the clue phrase (e.g. at "Gothenburg") helps when the hidden word is a direct attribute of the clue entity (Sweden), and fails when it needs composition (Thor → Thursday gives Norse, Odin, Loki).
- Leading directions of the generic variance subspaces read as punctuation and formatting tokens.
- J-lens lists at late layers are mostly whole English words, with few fragments or other scripts, but contain same-category alternatives (other capitals, other weekdays).

## Question

Propose 3–5 concrete transforms or subspaces worth testing next, in rough priority order. For each give:

1. the construction (pseudocode or an equation), and what data it is fitted on;
2. why it should separate hidden content from spoken content in an all-English setting, not just English from Chinese;
3. a cheap test that would falsify it.

Also say which of the observations above you think is most diagnostic, and if you think the framing or scoring itself is flawed, say so.
