# 2719: bounded negative; establish readout location before another editor

**Observed:** natural country-donor addition changed neither capital nor currency in either direction. This rejects the frozen setting, not country editing or one-pass intervention generally.

Paths below are repository-relative. Let **R** = `out/2026-10-01_154006_country-donor-joint/`.

## Complete outcome and denominator

I inspected all nine complete continuations and all eighteen 32-entry observer lists in `R/conditions_compact.jsonl`, against the three linked case reports:

| Case report | Base | Donor | Random |
|---|---|---|---|
| `out/2026-10-01_154019_chat-causal-0/run.md` | `Stockholm; SEK<\|im_end\|>` | identical | identical |
| `out/2026-10-01_154025_chat-causal-1/run.md` | `Tokyo; JPY<\|im_end\|>` | identical | identical |
| `out/2026-10-01_154030_chat-causal-2/run.md` | `4; even<\|im_end\|>` | identical | identical |

Thus donor capital transfer **0/2**, currency transfer **0/2**, joint transfer **0/2**; random likewise. Arithmetic preservation is **1/1 per condition**, not a third successful concept transfer. Bases are correct **3/3**. Nine trajectories are not nine independent causal tests: this is **one selected country pair, two directions, one arithmetic input**. No capped, malformed, or country-name-spilling outputs were dropped.

`R/verification.json` reports `"all_conditions_same_token_ids": true` for every case. All trajectories terminate after respectively 5, 6, and 4 tokens, including EOS.

## Mechanics, probabilities, and misconceptions

- **Coverage:** `R/forward_trace.jsonl` accounts for eight generic prefills plus 45 generation calls = **53 forwards**, gradients disabled. Each trajectory has one prefill plus N−1 cached calls. Frozen `R/source.py` applies the signed donor at block15/final prompt position and quarter-strength during every decode; block23 observers never feed the edit. Final-decode readout is the state **predicting EOS**, not a further pass consuming EOS.
- **Nonzero intervention:** `R/console-clean.log` quotes `"difference norm=1.071719"`; verification reports applied prefill relative norms about 0.116 on country inputs. This constrains “hook did nothing,” although saved-state verification is not independent neural replication.
- **Probability semantics:** `R/source.py` computes `lp[a1] - lp[a0] - base_lp[a1] + base_lp[a0]`. Here those IDs mean **Tok versus Stock**, not Tokyo versus Stockholm. Donor shifts are approximately zero forward and **+0.125 reverse—opposite the desired reverse movement**. Random shifts are −0.25 and −0.125. Tiny Base nonzero shift is cancellation, not intervention.
- Arithmetic’s country-prefix mass near zero does **not** indicate incoherence: its complete answer remains correct. Likewise, `r2=0` cannot certify semantic transfer.
- **Observers:** all three Sweden prefills retain Stockholm and Sweden/瑞典; all Japan prefills foreground Tokyo, including translated city/input forms. Arithmetic lists contain `4` and punctuation. All nine final lists foreground terminal/formatting tokens. These prompt-masked observers demonstrably include spoken answers; they are **not hidden-versus-said readout successes**.

No concrete executed-path blocker was found. The inherited exception-cleanup issue in `R/inputs/scripts/demo.py:70–79`—`handle.remove()` occurs after the forward without `finally`—affects failed preparation, not this completed result.

## Diagnosis and one next action

**Recommendation: complete the already-planned prospective boundary-readout test before selecting another causal method; do not redesign it here.** Supervisor dialogue confirmed this sequencing and that no frozen transport dataset/target exists.

Competing explanations remain:

1. **Task-conditioned representation mismatch:** generic “Consider Sweden” contrasts need not transport the state resolving Gothenburg into country properties. A reusable offline task-conditioned map could address this, but template/answer transport could also improve latent MSE without editing a hidden concept.
2. **Readout/location mismatch:** these observers mostly expose answers or termination. Learning where meaningful identity readout occurs offers a better basis for specifying a counterfactual target, but readable identity alone would not prove causal mediation.
3. **Implementation/evaluation error or unknown mechanism:** saved updates, correct Bases, and full-text inspection constrain these alternatives; fresh neural replay could still expose discrepancies.

The earlier `out/2026-10-01_132256_chat-causal-joint/donor_axis_diagnostic.json` places edited dog near the generic spider endpoint without transfer, while clean spider is also dog-side. That discourages endpoint-clamp rescue; it does not prove causal absence.

2648 coordinate exchange, 2706 natural animal addition, and 2719 are different bounded negatives. Changed preparation wording, tasks, and natural norms prevent an isolated domain-effect claim. No unseen-concept evidence, seed spread, or universal impossibility follows. No dose/sign/layer/window rescue is recommended.

— PI/OpenAI