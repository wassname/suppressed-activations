**Withdrawals and narrowing**

I withdraw the blacklist discriminator and the claim that repeated‑edit dynamics alone cause failures; the data are equally consistent with a poor semantic axis. My earlier assertion that static linear interventions cannot work for continuous steering is also withdrawn—the requirement is intentional, and the issue is whether the particular axis and dose are correct.

**Bounded discriminator (replacing blacklist)**  
At each token, compute the source coordinate $c_{\text{source}} = h\cdot v_{\text{source}}$ (with $v$ normalized). If $c_{\text{source}}$ rises above a threshold calibrated on clean donor continuations, temporarily increase the edit strength toward the target direction. This bounds unwanted source reactivation without relying on token occurrence.

**Comparison to separate bad dose from bad direction**  
Run the exact same spider‑dog axis with *continuous* edit strengths scaled geometrically: e.g., $0.25,0.5,1,2,4\times$ the default coefficient swap. For each strength, generate multiple completions and score them for:
- Correct donor digit (4)
- Coherent explanation that includes “dog” and does **not** retract, invent riddles, or revert to spider
- No contradictory biology (e.g., “dogs have eight legs”)

If **no strength** yields coherent, stable dog completions, the axis is unlikely to be a valid semantic separator; it may be a lexical co‑occurrence direction that cannot support continuous steering.  
If a **narrow strength window** gives coherent results while others fail, dose is critical, and a donor‑margin clamp (using the successful coordinate difference) becomes plausible. The clamp would then enforce that *margin*, not an arbitrary swap.

**What this would and would not establish**  
Success at a tuned strength would show that the gradient‑derived direction can be scaled into a useful edit, but it would **not** prove the axis captures a genuine concept independent of the specific (spider, dog) pair or the corpus. Failure across all strengths suggests the axis is unsuitable, and alternative source‑donor separation methods (e.g., contrastive projections on natural prompts) must be pursued. The test pins down whether the current failures are due to overshoot or axis invalidity, without requiring a separate semantic detector.

**Note on the margin formula**  
The earlier minimal‑norm correction for a target coefficient deficit $a$ is $\frac{a}{d\cdot d}\,d$, where $d=v_{\text{target}}-v_{\text{source}}$; the factor $2$ appears only when $v$ columns are orthogonal and unit‑norm. I will not embed an unverified scaling. The proposed clamp would use the empirically successful margin from the dose sweep, applied as a threshold.