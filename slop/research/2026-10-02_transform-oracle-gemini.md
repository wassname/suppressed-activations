### Diagnostic Observation & Conceptual Critique

**Most diagnostic observation:** *Removing final-layer predicted words (top-5/20) barely affects translation but drops English v4 F1 from .184 to .061.* 

**Critique of framing/scoring:** In multilingual translation, language-space orthography trivially isolates the intermediate concept (English letters vs. Chinese hanzi). In English two-step reasoning, however, intermediate concepts and final outputs share the semantic category (e.g., *Sweden/Stockholm*, *Thursday/Friday*). Because late transformer layers sharpen competitive distributions over the same semantic field, the hidden word remains high in output-head probability late into the forward pass. Treating suppression as a generic "rise-and-fall" across fixed layers fails because the transition layer varies per prompt.

---

### Proposed Transforms / Subspaces

#### 1. Per-Prompt Dynamic Orthogonal Projection to Late Stream ($P^\perp_{L_{\text{late}}}$)
* **Construction:** Run the forward pass to obtain $h_l$ at the last prompt position for layers $l \in [20, 32]$. Do not subtract output logits post-unembedding; project the residual vector itself orthogonal to the late/final residual vector before projecting to the vocabulary:
  $$\hat{h}_l = \left( I - \frac{h_L h_L^T}{\|h_L\|^2} \right) h_l, \quad \text{logits}_l = W_U \text{norm}(\hat{h}_l)$$
  Take $l \approx 26\text{--}28$. Zero offline fitting required.
* **Why it separates hidden from spoken in English:** The late residual stream $h_L$ carries the strongly aligned direction of the planned spoken output and its immediate category competitors. Projecting orthogonal to $h_L$ in representation space strips the commitment direction of the final answer while preserving orthogonal semantic features generated at mid-layers.
* **Cheap falsification test:** Compute cosine similarity $\cos(h_{27}, h_{32})$ on English v4. If it exceeds 0.95, or if $\text{logits}_{27}$ yields mostly unigram syntax noise/punctuation after projection, the hypothesis fails.

#### 2. Contrastive Clue-Conditioned Residual Difference ($\Delta h_{\text{clue}}$)
* **Construction:** Compute $h_l(\text{prompt})$ at the last token. In parallel, run an abridged baseline prompt that drops the relational wrapper (e.g., `"The capital of the country containing Gothenburg is"` vs. `"Gothenburg is"` or simply masking the clue entity). Read out via:
  $$\text{readout} = W_U \text{norm}(J_l (h_l(\text{full}) - h_l(\text{base})))$$
  Can be run on the fly via a 2-prompt batch.
* **Why it separates hidden from spoken in English:** The base prompt activates the entity and its direct categorical attributes (*Gothenburg* $\to$ *Sweden*), whereas the full prompt routes attention forward to resolve the query (*Stockholm*). Taking the difference cancels early entity-level semantics and late template-completion formatting, isolating the active derivation step.
* **Cheap falsification test:** Run on 5 prompts; if the top-10 tokens of $\Delta h_l$ are syntactic template artifacts (`capital`, `country`, `is`) rather than intermediate entities, falsified.

#### 3. Task-Agnostic "Suppression Subspace" via Contrastive PCA (cPCA)
* **Construction:** Collect intermediate states $h_{27}$ on WikiText or translation data. Form two sets of vectors:
  - $X_{\text{supp}}$: residual states at $l=27$ on prompts where the top-$k$ tokens at $l=27$ were subsequently displaced/suppressed by $l=32$.
  - $Y_{\text{surv}}$: residual states where $l=27$ predictions matched $l=32$ predictions.
  Find projection matrix $V_k$ maximizing $\mathrm{Tr}(V^T (C_{\text{supp}} - \alpha C_{\text{surv}}) V)$ via contrastive PCA. Readout: $W_U \text{norm}(V_k V_k^T h_{27})$.
* **Why it separates hidden from spoken in English:** Unlike generic covariance differences $\mathrm{Cov}(h_{27}) - \mathrm{Cov}(h_{32})$ which isolate generic variance (syntax/punctuation), cPCA targets directions specific to tokens that get overwritten during step-composition.
* **Cheap falsification test:** If the leading eigenvectors of $(C_{\text{supp}} - \alpha C_{\text{surv}})$ continue to decode into formatting/punctuation tokens for $\alpha \in [0.5, 2.0]$, the method fails.

---
*Signed: Gemini*