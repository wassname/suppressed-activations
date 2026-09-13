

def test_real_noncomplete_joint_smoke():
    """REAL tiny run of the NON-COMPLETE joint-removal path (sweep smoke_common_basis_joint,
    condition joint_removal_C1.5) through the actual run_with_bundle. The cc25c2b refactor
    deleted the Pu definition and only this path crashed; mocked dispatch tests cannot see
    it. If joint_support is unhooked from run_with_bundle again, this fails with that
    NameError. -- PI[glm-5p3-flash]"""
    import json
    import os
    from pathlib import Path
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ["SUPPRESSED_MODEL"] = "wassname/qwen3-5lyr-tiny-random"
    os.environ["SUPPRESSED_REVISION"] = "main"
    os.environ["SUPPRESSED_DEVICE"] = "cpu"
    import torch
    torch.set_grad_enabled(False)
    import scripts.oat_sweep as oat
    import scripts.test_registration as tr
    from scripts.prompt import assistant_prefill_input_ids

    tok = __import__("transformers").AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
    src = assistant_prefill_input_ids(tok, "Question: what is the animal that spins webs called?\nAnswer: ",
                                      device="cpu", instruction="Answer the question with the answer first. Then describe the animal in three sentences.")
    tgt = assistant_prefill_input_ids(tok, "Question: what is the animal that barks and is called man's best friend called?\nAnswer: ",
                                      device="cpu", instruction="Answer the question with the answer first. Then describe the animal in three sentences.")
    spec = {"output_dir": ".local/dispatch-smoke", "sweep": "smoke-common-basis-joint",
            "condition_index": 1, "prompt_mode": "chat-assistant-prefill",
            "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
            "target_prompt": "Question: what is the animal that barks and is called man's best friend called?\nAnswer: ",
            "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
            "lens_corpus_arrow": None, "target_concept": "dog",
            "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
            "extraction_instruction": None, "selector_audit": False,
            "expected_condition": "joint_removal_C1.5"}
    spec = {**spec, "expected_condition": "joint_removal_C1.5", "expected_strength": 1.5}
    oat.validate_specs([spec], oat.SWEEP_CONFIGS)  # the original NameError fired later, in the hook build
    bundle = oat.load_bundle()
    import time
    out = Path(f".local/dispatch-smoke-noncomplete-joint-{time.strftime('%H%M%S')}")
    out.mkdir(parents=True, exist_ok=True)
    # spy: capture the built spec to confirm the non-complete joint branch ran
    built = {}
    orig = oat.intervention_hooks

    def spy(*a, **kw):
        hooks = orig(*a, **kw)
        if kw.get("operation") == "common_replace" and kw.get("common_specs"):
            built["spec"] = kw["common_specs"]
            built["complete_rank_mode"] = None
        return hooks
    oat.intervention_hooks = spy
    try:
        oat.run_with_bundle(bundle, out, extraction_cache={"revision": bundle["revision"]},
                            batch_spec={"batch_file": "inline-dispatch-smoke", "index": 0, "spec": dict(spec)},
                            expected_detector_layers=None, **oat.strip_spec_metadata(spec))
    finally:
        oat.intervention_hooks = orig
    assert "spec" in built, "non-complete joint run never built common_replace specs"
    L = next(iter(built["spec"]))
    rank = built["spec"][L]["src"].shape[-1]
    # the pre-refactor failure mode was NameError BEFORE any spec existed; completion
    # plus a nonempty joint-support basis is the regression property
    assert rank >= 1, f"empty joint-support basis: {rank}"


if __name__ == "__main__":
    test_validate_and_dispatch()
    test_real_noncomplete_joint_smoke()
    print("DISPATCH TESTS PASS (incl. real non-complete joint run)")
