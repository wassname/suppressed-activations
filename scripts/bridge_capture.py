# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8",
#                 "transformers>=5.5"]
# ///
"""Approved bounded capture (supervisor seq 21): THREE unique bridge inputs — spider
source (shared by both pairs), dog donor, ant donor — via the EXISTING extractor
machinery, NO generation, NO templates. Manifest prepared FIRST from the ACTUAL saved
bridge rendered_inputs with the dedup + exact-ID-equality asserts BEFORE model load.
After the capture: the ACTUAL production paired-builder (the increment-routed
span-correction construction through run_with_bundle, spy-captured) — its U/deltas
saved for the CPU analysis (33-point centered readout traces etc.). No new score/rank.
-- PI[glm-5p3-flash]"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
torch.set_grad_enabled(False)
import scripts.oat_sweep as oat
from scripts.extract_exact_inputs import rendered_input_ids, WRAPPER, MODEL, REAL_REVISION

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "out" / "2026-09-13_bridge-matrix-193115"
BASIS_DIR = ROOT / "out" / "2026-09-13_cpu-basis-check-131429"
OUT = ROOT / "out" / f"2026-09-13_bridge-capture-{time.strftime('%H%M%S')}"
PROMPTS = {  # exact historical prompts (verified against the saved bridge runs)
    "source": "Question: How many legs does the animal that spins webs have?\nAnswer: ",
    "dog": "Question: How many legs does the animal that barks and is called man's best friend have?\nAnswer: ",
    "ant": "Question: How many legs does the animal that lives in colonies and follows pheromone trails have?\nAnswer: "}


def main():
    # ---- manifest FIRST, from the ACTUAL saved bridge rendered_inputs, CPU only
    inputs, rendered = {}, {}
    for donor in ("dog", "ant"):
        run = json.load(open(BRIDGE / f"{donor}-att-h20" / "result.json"))
        ri = run["rendered_inputs"]
        inputs[f"{donor}-source"] = ri["source"]["input_ids"]
        inputs[f"{donor}-donor"] = ri["donor"]["input_ids"]
        rendered[f"{donor}-source"] = ri["source"]["rendered"]
        rendered[f"{donor}-donor"] = ri["donor"]["rendered"]
    # dedup assert: the two sources are the same prompt
    assert inputs["dog-source"] == inputs["ant-source"], \
        "the two pair sources differ — dedup to 3 is invalid"
    unique = {"source": inputs["dog-source"], "dog": inputs["dog-donor"],
              "ant": inputs["ant-donor"]}
    assert len(unique) == 3, f"expected 3 unique inputs, got {len(unique)}"
    manifest = {"n_unique_inputs": 3, "dedup": "dog-source == ant-source (asserted)",
                "wrapper": WRAPPER, "model": MODEL, "revision": REAL_REVISION,
                "inputs": {}, "dtype_device": None}
    for name, ids in unique.items():
        manifest["inputs"][name] = {
            "n_tokens": len(ids), "ids_sha256": hashlib.sha256(
                torch.tensor(ids).numpy().tobytes()).hexdigest(),
            "rendered_repr": repr(rendered[name])[:400]}
    print("MANIFEST (pre-model): 3 unique inputs;",
          {k: v["n_tokens"] for k, v in manifest["inputs"].items()})

    # ---- capture: 3 forwards, no generation
    torch.set_grad_enabled(False)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from scripts.demo import trajectory
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REAL_REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REAL_REVISION, dtype=torch.bfloat16,
        attn_implementation="sdpa").to("cuda").eval()
    final_norm = model.model.norm
    manifest["dtype_device"] = {"compute": "bfloat16", "device": "cuda",
                                "saved_dtype": "float32"}
    manifest["code_sha256"] = {
        p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        for p in ("scripts/oat_sweep.py", "scripts/demo.py",
                  "suppressed_activation_subspace.py", "scripts/bridge_capture.py")}
    OUT.mkdir(parents=True, exist_ok=True)
    torch.save(final_norm.weight.detach().float().cpu(), OUT / "final_norm_weight.pt")
    torch.save((1.0 + final_norm.weight).detach().float().cpu(), OUT / "norm_gain.pt")
    torch.save(model.lm_head.weight.detach().float().cpu(), OUT / "unembedding.pt")
    for name, prompt in PROMPTS.items():
        got = rendered_input_ids(tokenizer, prompt, "cuda")
        assert got["ids"].tolist() == list(unique[name]), \
            f"{name}: actual forward input IDs != manifest"
        res, _ = trajectory(model, got["ids"].to("cuda"), final_norm)
        torch.save(res.detach().float().cpu(), OUT / f"{name}_residuals.pt")
        manifest["inputs"][name]["captured"] = True
        print(f"captured {name}: {tuple(res.shape)}")
    manifest["capture_count"] = 3
    manifest["git_describe"] = subprocess_run_git()
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")

    # ---- the ACTUAL production paired-builder: increment-routed span-correction
    # construction on the same inputs; spy-capture the actual U/deltas
    batch_row = json.load(open(ROOT / "slop" / "replay_frozen_candidate_batch.json"))[4]
    oat.SWEEP_CONFIGS["bridge-inc-h20"] = lambda: [
        (f, n, replace(c, delta_anchor_layer=20, basis_selector="increment"))
        for f, n, c in oat.SWEEP_CONFIGS["span-correction-sweep"]()]
    spec = dict(batch_row, sweep="bridge-inc-h20")
    spec["output_dir"] = str(OUT / "production-construction")
    obs = {}
    orig = oat.intervention_hooks

    def spy(*a, **kw):
        hooks = orig(*a, **kw)
        if kw.get("operation") == "span_corrected_delta":
            obs["shared"] = a[0].clone()
            obs["fixed_deltas"] = {k: v.clone() for k, v in kw["fixed_deltas"].items()}
        return hooks

    oat.intervention_hooks = spy
    try:
        d = Path(spec["output_dir"])
        d.mkdir(parents=True, exist_ok=True)
        oat.run_with_bundle(bundle, d, extraction_cache={"revision": bundle["revision"]},
                            batch_spec={"batch_file": "bridge-capture", "index": 4,
                                        "spec": dict(spec)},
                            expected_detector_layers=None,
                            **oat.strip_spec_metadata(spec))
    finally:
        oat.intervention_hooks = orig
    torch.save({"U_production": obs["shared"].clone(),
                "deltas_production": {k: v.clone() for k, v in obs["fixed_deltas"].items()}},
               OUT / "production_U_deltas.pt")
    print(f"PRODUCTION U captured: {tuple(obs['shared'].shape)} | "
          f"result: {OUT / 'manifest.json'}")


def subprocess_run_git():
    import subprocess
    return subprocess.run(["git", "describe", "--always", "--dirty"], check=True,
                          text=True, capture_output=True).stdout.strip()


if __name__ == "__main__":
    main()
