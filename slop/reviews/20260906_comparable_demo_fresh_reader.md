## Review

### Finding

- **P1 — Required probabilities are rounded rather than reported at the specified precision.** `AGENTS.md:71-73` requires `p(8)=0.882568`, `p(4)=0.490091`, and intervened `p(8)=0.297255`. The public tables instead show `0.883`, `0.490`, and `0.297` at `README.md:129` and `README.md:163-164`; the executed notebook repeats those values at `nbs/demo.ipynb:290` and `nbs/demo.ipynb:378-379`. This comes from `floatfmt=".3f"` in `nbs/demo.py:137`. Smallest fix: render probability values to six decimal places, regenerate the notebook, and synchronize the README tables.

### Correct

- The causal section has exactly two conditions, `Base` and `Causal intervention` (`README.md:106,140`).
- Both conditions present the same spider input, a clearly labeled mind-like readout, a fenced verbatim 12-token generation, and a ten-row token/log-probability/probability table in the same order (`README.md:108-137,142-171`).
- The generated strings are explicitly labeled as model generations and isolated in `text` fences; no explanatory prose appears inside them (`README.md:120-125,154-159`). The notebook asserts twelve generated token IDs for both conditions (`nbs/demo.py:145,196`).
- The dog list is labeled “Replacement readout (‘what we insert’)” and is populated from `target['selected']` (`README.md:148`; `nbs/demo.py:208`). Its provenance is explicitly the unmodified dog-prompt pass (`README.md:174-179`), not a post-intervention detector result.
- The extraction is the LM-head rise-and-fall construction: L23→L25 rise and L25→L32 fall (`nbs/demo.py:90-93`), using `model.lm_head.weight` (`nbs/demo.py:103`) and `suppressed_activation_subspace` (`nbs/demo.py:112-121`).
- The intervention defaults to L26 and C=4 (`nbs/demo.py:63,65`) and hooks one block only (`nbs/demo.py:177-185`). The hook modifies `hidden[:, -1:]`, confirming the final input position (`scripts/demo.py:124-127`).
- The C4 caveat comes after the complete comparison and concisely explains that C1 still yields 8, C4 is extrapolative, the detector remains spider-like, the perturbation is large, random controls sometimes match it, and an arithmetic target reproduces the first-token change (`README.md:190-196`). It does not interrupt the demo.
- The supplied audit records successful notebook execution and notebook validation (`slop/audits/job_280_full.log:1-4`).

## Cold-reader paraphrase

For the unchanged spider prompt, Qwen’s rise-and-fall readout contains spider/web-like vocabulary and the model generates 8; at the same prompt, replacing one final-token L26 residual component with a separately extracted dog-prompt component at amplified strength C4 changes the generation to 4 and shifts the next-token distribution. However, C1 does not change the answer, C4 is a large perturbation, matched random controls can sometimes produce an equally large effect, and an unrelated `2 + 2` target causes the same first-token change, so this demonstrates causal sensitivity of the answer state rather than transfer of “dog identity.”

## Merge verdict

**BLOCK** on the explicit probability-precision requirement. Aside from that presentation mismatch, the six requested fresh-reader comprehension checks pass.