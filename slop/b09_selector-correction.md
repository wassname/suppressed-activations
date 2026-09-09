# Correction 2026-09-09 (PI/OpenAI): the template-detector KeyError claim was a
# mistaken control-flow reading. In scripts/oat_sweep.py the `columns[...]` lookup
# sits INSIDE `if cfg.template_state_span != "none"`. Span "none" takes the
# `persistent_shared_basis` branch (token_persistent_subspace: centered unit
# gain-weighted unembedding vocabulary-suppression selector) — the intended path.
# No production code was changed on the basis of the wrong claim; the smoke sweep
# now exercises span "none" directly (b09 check).
