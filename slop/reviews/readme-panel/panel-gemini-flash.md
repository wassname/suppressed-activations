### 1. Central Claim and Challenge

**Claim:** Multilingual models route semantic concepts through an internal pivot language (primarily English, and to a lesser extent Chinese) during translation or reasoning tasks before suppressing it in final layers to emit the target token. 
**Challenge:** Given activations from a single forward pass where input/output share no script with English or Chinese, construct a generic transform mapping activations to vocabulary scores that isolates this latent concept in its top-8 tokens—without leaking the input, output, or predicted word, and without using target-word lookup.

---

### 2. The Figures

- **`cartoon.png`**:
  - *Shows:* A French speaker asking a robot to translate to Chinese; the robot internally reasons in English before answering in Chinese. A magnifying glass inspects hidden activations for English tokens.
  - *Takeaway:* Conceptual motivation: intermediate English thoughts exist and can be isolated via general transforms.
  - *Stuck point:* Suggests models deliberately "think" in English sentences ("Okay — first I understand it in English"), which anthropomorphizes what the paper operationalizes merely as logit-lens token peaks.

- **`wendler_fig2.png`**:
  - *Shows:* Layerwise logit-lens probabilities and entropy for Llama-2-70B translating into Chinese. English probability (orange) surges around layer 40–50 (~0.4) while entropy drops, before collapsing toward layer 80 as Chinese probability (blue) climbs to ~0.5.
  - *Takeaway:* English appears in intermediate layers and is actively suppressed near the output.
  - *Stuck point:* The colorbar shows entropy falling, but lacks numeric axis labels directly mapped to the layer curves.

- **`language_pairs.png`**:
  - *Shows:* Panel (a): Mean logit-lens trajectories in Qwen3.5-4B (fr→ru); English peaks at layer 28 (~0.49) before Russian takes over at layer 32. Panel (b): Pass rates across 5 unseen pairs comparing four methods.
  - *Takeaway:* Intermediate English emergence replicates in Qwen. Furthermore, masking out read and said words boosts recovery from 11–18% (plain lens) to over 90%.
  - *Stuck point:* Panel (b) reveals that simple lexical masking explains almost all gain over the baseline lens, undermining the necessity of specialized "rise-and-fall" mechanics.

---

### 3. The Leaderboard

- **One row:** An evaluation of a specific activation transform function (mapping residual stream/layer activations to token rankings) evaluated on a held-out test split.
- **Main score (`found↑`):** The fraction of test prompts where the top-8 words contain the correct English or Chinese concept, with no words from the input/output scripts or the model's next token.
- **Best row:** `[rise-and-fall, J-lens]` with `found = 0.93` (and minimal leak of `0.01`).
- **Formatting conventions:**
  - `★`: Uses a lens or per-prompt vocabulary scores.
  - *Italics*: Baseline control methods (e.g., `plain lens`, `random subspace (floor)`, `fixed list (control)`).

---

### 4. Ambiguities, Omissions, and Contradictions

1. **Test Languages Discrepancy ("The challenge" vs. Leaderboard footnote):** "The challenge" explicitly states: *"We test on translation between German, French and Russian."* However, the leaderboard table footnote specifies: *"test = ar→hi, hi→th, th→ru, ko→ar (74 prompts); each setting chosen on ru→ko."*
2. **Evaluation Metrics & Top-K Inconsistency:** The challenge rules demand evaluating the *top 8 words*, but the "Current one-pass tests" and "Earlier translation results" evaluate *top 32 tokens*.
3. **Model Identity:** "The challenge" and Section 2 mention Qwen (and Llama-2), but the leaderboard fails to explicitly specify which base model is evaluated in that table.
4. **Causal vs. Correlational Claims ("Are suppressed activations causal?"):** The narrative claims to swap spider to dog, but admits $C=4$ shifts 72% of residual variance, random directions duplicate the effect in 21/256 runs, "2 + 2" prompts achieve the same shift, and readout tokens still say "Spider".

---

### 5. Requirements to Submit an Entry

To submit an entry, a participant still lacks:
1. Exact specification of the model name, checkpoint, and precision loaded by `score.py`.
2. Input signature, expected return format, and available runtime arguments for functions in `transforms.py`.
3. Clear specification of allowable layers and forward hooks during the test pass.
4. Access to the ground-truth target dictionaries and evaluation prompts (`data/`).

— Gemini Flash