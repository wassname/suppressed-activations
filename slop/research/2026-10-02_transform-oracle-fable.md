# Oracle answer: transforms/subspaces for "thought but not said"

**Most diagnostic observation.** The sentence "In English, excluding speech is the main difficulty, not finding the hidden word," together with v4 F1 falling .184→.061 when more final-layer words are filtered. Inference: the hidden and spoken words live in nearly the same late-layer direction family (both are "the answer-shaped concept"), so any readout aligned with W_U will rank them together. Variance-difference subspaces failed because they capture *position/format* variance (punctuation), not *semantic suppression*. The task is therefore a nuisance-removal problem, not a discovery problem.

**Framing caveat.** The scoring excludes the spoken word by filtering, but the method is also required not to *read* it. That is fine, but F1@8 on 8–16 prompts is extremely noisy (one hit ≈ .1); treat differences <.1 as nothing. Also, "hidden word" as a single vocabulary token conflates concept and token; on Thor→Thursday the hidden concept may be "Thor's day", which never appears as one token.

## Proposals (priority order)

**1. Output-nullspace projection of the J-lens (fitted on WikiText).**
Construction: collect J_l h_l (layer 29) and final h_32 on the 1000 WikiText prompts. Fit a linear map A minimising ‖A J_l h_l − h_32‖ (ridge). Readout = W_U norm(J_l h_l − A J_l h_l), i.e. the residual after removing the part predictable as "what will be said". Fit on generic text, no labels.
Why: spoken content is by definition the component that survives to the final layer; what survives is predictable from mid-layer state; the residual is what the model computes but discards. This is language-independent.
Falsifier: on translation, the hidden English word should stay in the top-8 while the Chinese answer drops out *without* the output filter. If the Chinese word stays, A is not capturing output flow and the idea is dead in an afternoon.

**2. Suppression-direction subspace from paired positions, not covariance of raw states.**
Construction: for each WikiText token position, take d = norm(h27) − norm(h32) projected through W_U, keep only the components whose logit *decreases* (d>0 in logit space): s = ReLU(W_U norm(h27) − W_U norm(h32)). Fit PCA on these s vectors in vocab space, then map back to residual space via the pseudo-inverse of W_U (or simply score prompts with their own s vector as per-prompt readout: top-k of s).
Why: the rise-and-fall test failed because it required a rise L22→27; that constraint is unmotivated. Pure "present at 27, gone at 32" is the direct definition of suppressed content. Being in logit space removes punctuation-dominance since formatting tokens do not fall.
Falsifier: per-prompt top-k of s on translation should beat .164; on English v3 it should produce Sweden/Thursday without producing Stockholm (which rises, so d<0). If s is dominated by generic frequent tokens, apply a WikiText mean-s subtraction before concluding failure.

**3. Attention-output readout from mid-layer heads at the final position.**
Construction: for layers 20–28, take the attention-block output a_l (before adding to residual), readout W_U norm(J_{l+1} a_l). Select, on translation only, the layer whose list contains the hidden word most often; freeze that layer.
Why: composition questions (Gothenburg→Sweden→Stockholm) move the intermediate entity to the last position via attention; the MLP then rewrites it into the answer. Reading the attention contribution isolates "what was retrieved" from "what was computed next" regardless of language. The "read at Gothenburg" observation already supports this partly.
Falsifier: if the chosen layer's list on Thor contains Norse/Odin but never Thursday, the retrieved content is the clue not the intermediate, and this approach fails on exactly the hard cases.

**4. Contrastive LDA direction, fitted on translation only, transferred to English.**
Construction: w = Σ⁻¹(μ_hidden − μ_spoken) where μ are mean unembedding rows of hidden vs spoken words from the 48 translation prompts; apply rank-1 projection removal at h29 before J-lens.
Why: tests whether a "to be said" direction exists independent of language. Risk: it will simply learn Chinese-vs-English, which is exactly the trap in the brief — so it is lowest priority and mainly a control.
Falsifier: if it improves translation and leaves English at zero, the direction is a language detector; discard.

**Missing information:** per-layer hidden-word rank curves for English prompts (does Sweden ever reach top-8 at *any* layer?). If not, no fixed transform at the final position can win and the problem is positional, which makes proposal 3 the only live one.

— Claude (Claude Code, Anthropic)