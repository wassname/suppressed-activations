# Round2 corrections — Codex/GPT-6

Please revise your recommendations with these facts. Keep under400 words, no repeated pseudocode.

1. Continuous steering through every decode token is an explicit user requirement, not a disposable design preference. A one-shot edit can be a diagnostic control, but cannot be the proposed final solution. A conditional edit whose hook remains active is allowed.
2. A source-word blacklist is invalid. `Dogs do not spin webs` is compatible with dog identity. Our full-text evaluation already checks reversals and fabricated biology; the pseudocode explicitly said that. Do not replace it with digit-only or word-occurrence scoring. The target counterfactual itself is not an error.
3. For two unit columns V with correlation rho, the coefficient contrast equals the dot-product contrast divided by(1-rho). Their signs are identical. Comparing pseudoinverse coefficients rather than dot products is NOT a gate-sign bug, though neither is an independently validated semantic detector.
4. DeepSeek's proposed update mixes coefficient-margin units with dot-product-margin normalization. For d=v_target-v_source and coefficient deficit a, the minimum-norm correction is a*d/2. The proposed a*d/(d@d) reaches a dot-product margin instead. Check your formula before recommending implementation.
5. The data do not prove repeated-edit dynamics are the cause. They are also consistent with a poor semantic axis. C1 is exact exchange, C2 is extrapolation; not every swap is threefold overshoot. Rejecting one endpoint or tested layer does not establish that the entire method cannot work.
6. Prompt-contrast directions have been tried, including layer-local attenuation spans. They give selected coherent results but do not yet transfer across attributes. Do not present that as an untried cure. Need one bounded discriminator before more speculative machinery.

Which of your claims do you withdraw or narrow? Give the best continuous intervention comparison that separates bad dose from bad direction, and state what its outcome would and would not establish. A donor-derived contrast clamp remains a candidate, not a validated solution.
