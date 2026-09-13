# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8",
#                 "transformers>=5.5"]
# ///
"""Approved bounded capture: THREE unique bridge inputs (spider source shared by
both pairs, dog donor, ant donor) via the existing extractor machinery; NO generation,
NO templates, NO model-based construction after the capture. Manifest first
(pre-model): dedup + exact-ID-equality asserts + tokenizer validation. -- PI[glm-5p3-flash]"""
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
OUT = ROOT / "out" / f"2026-09-13_bridge-capture-{time.strftime('%H%M%S')}"
_frozen = json.loads((ROOT / "slop" / "replay_frozen_candidate_batch.json").read_text())
PROMPTS = {"source": _frozen[4]["source_prompt"],          # the exact historical strings
           "dog": _frozen[4]["target_prompt"],
           "ant": _frozen[6]["target_prompt"]}


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
    rendered = {"source": rendered["dog-source"], "dog": rendered["dog-donor"],
                "ant": rendered["ant-donor"]}
    assert len(unique) == 3, f"expected 3 unique inputs, got {len(unique)}"
    # tokenizer validation BEFORE model load
    from transformers import AutoTokenizer
    tok_check = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=REAL_REVISION)
    for name, prompt in PROMPTS.items():
        got = rendered_input_ids(tok_check, prompt, "cpu")  # the full wrapper rendering
        assert got["ids"].tolist() == list(unique[name]), \
            f"{name}: rendered IDs != saved bridge IDs"
    manifest = {"n_unique_inputs": 3, "dedup": "dog-source == ant-source (asserted)",
                "wrapper": WRAPPER, "model": MODEL, "revision": REAL_REVISION,
                "inputs": {}, "dtype_device": None}
    for name, ids in unique.items():
        manifest["inputs"][name] = {
            "n_tokens": len(ids), "ids_sha256": hashlib.sha256(
                torch.tensor(ids).numpy().tobytes()).hexdigest(),
            "rendered_repr": rendered[name]}
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
        res, _ = trajectory(model, got["ids"].unsqueeze(0).to("cuda"), final_norm)
        torch.save(res.detach().float().cpu(), OUT / f"{name}_residuals.pt")
        manifest["inputs"][name]["captured"] = True
        print(f"captured {name}: {tuple(res.shape)}")
    manifest["capture_count"] = sum(1 for v in manifest["inputs"].values() if v.get("captured"))
    manifest["git_describe"] = subprocess_run_git()
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    manifest["file_sha256"] = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                               for f in OUT.glob("*.pt")}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")

def subprocess_run_git():
    import subprocess
    return subprocess.run(["git", "describe", "--always", "--dirty"], check=True,
                          text=True, capture_output=True).stdout.strip()


if __name__ == "__main__":
    main()
