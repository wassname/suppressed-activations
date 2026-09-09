Diagnostic: unequal-input comparison, NOT batch leakage. Fresh-dog CLI passed a literal
backslash-n in target_prompt (shell quoting bug in b08_run_check.sh DOG_TGT) while the
batch spec carried a real newline. Donor content_end 50 vs 49; donor hashes/IDs differ;
base+steered full-logit hashes match. Fixed by deriving fresh argv from the same spec.
