# GPU plan: detector-c2 construction comparison + fresh/shared equivalence (NOT queued)
#
# Order (owner release + historical 862/863 precede everything):
# 1. Historical repro 862/863 (frozen main runner, already queued).
# 2. Fresh detector-c2 runs (production runner, single-spec CLI, 2 GPU jobs):
#    dog-name + ant-name naming prompts, template-detector condition 2
#    (D8_20_32_matchedFalse), max_new_tokens 128.
# 3. Shared-model batch of the same two specs
#    (`slop/gpu_detector_c2_batch_spec.json` via --batch-spec, 1 GPU job).
# 4. Equivalence gate (same assertions as b09_compare, adapted paths): input-ID gates,
#    full-logit sha, IDs, hook coverage; then read full continuations against the
#    predeclared rubric (transfer / partial with quoted defect / fail).
#
# Prior predictions (construction comparison, asymmetric): coherent donor-persistent
# naming transfer on the detector construction motivates isolating the responsible
# difference vs the looping band; looping/correction establishes nothing about M3/M5
# and does not rule out selector problems.
