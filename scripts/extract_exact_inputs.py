# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Exact-input trajectory extraction for the 12 dev pairs — executable spec + preflight.

Contract (supervisor-reviewed 2026-09-12):
- model Qwen/Qwen3.5-4B revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a (pinned, asserted)
- wrapper EXACTLY the batch-spec instruction: 'Answer the question with the answer first.
  Then describe the animal in three sentences.' (asserted per prompt)
- PREFLIGHT (CPU, no model): rendered token-ID arrays for all 24 prompts must EQUAL the
  corresponding saved actual-run arrays (out/2026-09-10_eval-candidate-C1.5-*/result.json
  rendered_inputs input_ids) — hash equality recorded per entry; queue only after this passes
- capture: full 33xseqx2560 float32 trajectory per prompt (source AND donor), 24 forwards,
  no generation; torch.no_grad (grad disabled) throughout; hook boundary = residual entering
  block b (h_b): output_hidden_states[b] for b in 0..31 plus the final pre-norm hidden (h32)
  — the trajectory() definition in scripts/demo.py, reused directly
- per-entry rendered_input_sha256 + token IDs saved for ALL future reuse checks

-- PI[glm-5p3-flash]"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch

MODEL = "Qwen/Qwen3.5-4B"
REAL_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
REVISION = os.environ.get("SUPPRESSED_REVISION") or (
    REAL_REVISION if os.environ.get("SUPPRESSED_MODEL", MODEL) == MODEL else None)
assert REVISION == REAL_REVISION, f"revision must be pinned, got {REVISION!r}"
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
WRAPPER = "Answer the question with the answer first. Then describe the animal in three sentences."
ROOT = Path(__file__).resolve().parents[1]


def rendered_input_ids(tokenizer, prompt: str, device: str) -> dict:
    from scripts.prompt import assistant_prefill_input_ids
    chat = assistant_prefill_input_ids(tokenizer, prompt, device=device, instruction=WRAPPER)
    ids = chat["input_ids"][0].cpu()
    return {"chat": chat, "ids": ids, "sha": hashlib.sha256(ids.numpy().tobytes()).hexdigest()}


def preflight(batch_spec: Path) -> dict:
    """CPU-only: rendered token-ID arrays must EQUAL the actual-run saved arrays."""
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    cells = json.loads(batch_spec.read_text())
    checks, failures = [], []
    for cell in cells:
        cid = cell["id"]
        run = json.loads((ROOT / f"out/2026-09-10_eval-candidate-C1.5-{cid}/result.json").read_text())
        run_rendered = run["rendered_inputs"]
        for side, key in (("source", "source_prompt"), ("donor", "target_prompt")):
            got = rendered_input_ids(tokenizer, cell[key], "cpu")
            run_ids = run_rendered[side]["input_ids"]
            equal = list(got["ids"]) == list(run_ids)
            checks.append({"cell": cid, "side": side, "sha": got["sha"],
                           "ids_equal_actual_run": equal, "n_tokens": len(got["ids"])})
            if not equal:
                failures.append(f"{cid}/{side}: rendered IDs differ from the actual run")
    return {"wrapper": WRAPPER, "revision": REVISION, "checks": checks, "failures": failures}


def capture(batch_spec: Path, output_dir: Path) -> None:
    # preflight BEFORE the model load (fail fast, no GPU seconds wasted)
    pf = preflight(batch_spec)
    assert not pf["failures"], f"preflight failed — not capturing: {pf['failures'][:3]}"
    torch.set_grad_enabled(False)  # no grad anywhere (the 2026-09-10 autograd OOM lesson)
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from scripts.demo import trajectory
    from scripts.prompt import assistant_prefill_input_ids

    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    final_norm = model.model.norm
    output_dir.mkdir(parents=True, exist_ok=True)
    # weights saved once for CPU selector calculation (no repeated GPU capture)
    torch.save(final_norm.weight.detach().float().cpu(), output_dir / "final_norm_weight.pt")
    torch.save((1.0 + final_norm.weight).detach().float().cpu(), output_dir / "norm_gain.pt")
    torch.save(model.lm_head.weight.detach().float().cpu(), output_dir / "unembedding.pt")
    manifest = {"model": MODEL, "revision": REVISION, "wrapper": WRAPPER,
                "hook_boundary": "h_b = residual entering block b: hidden_states[b] for b in "
                                 "0..31 + final pre-norm hidden as h32 (scripts/demo.trajectory)",
                "dtype": "float32 saved (bf16 compute)", "grad": "disabled",
                "versions": {"torch": torch.__version__, "transformers": transformers.__version__},
                "spec_source_sha256": hashlib.sha256(batch_spec.read_bytes()).hexdigest(),
                "this_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                               check=True, text=True,
                                               capture_output=True).stdout.strip(),
                "preflight": pf, "entries": {}}
    for cell in json.loads(batch_spec.read_text()):
        cid = cell["id"]
        for side, key in (("source", "source_prompt"), ("donor", "target_prompt")):
            name = f"{cid}-{side}"
            chat = assistant_prefill_input_ids(tokenizer, cell[key], device=DEVICE,
                                               instruction=WRAPPER)
            ids = chat["input_ids"][0].cpu()
            # CAPTURE ID EQUALITY against the preflight reference arrays (asserted per entry)
            ref = next(x for x in pf["checks"] if x["cell"] == cid and x["side"] == side)
            assert list(ids) == list(ref["ids"]) and ref["ids_equal_actual_run"], \
                f"{name}: capture IDs != preflight/actual-run reference"
            residuals, _ = trajectory(model, chat["input_ids"], final_norm)
            assert residuals.shape == (33, chat["input_ids"].shape[1], 2560)
            torch.save(residuals.float().cpu(), output_dir / f"{name}_residuals.pt")
            manifest["entries"][name] = {
                "rendered_input_sha256": hashlib.sha256(ids.numpy().tobytes()).hexdigest(),
                "input_ids": ids.tolist(),
                "token_labels": [tokenizer.decode([int(t)]) for t in ids],
                "seq_len": int(residuals.shape[1]), "cell_id": cid, "side": side,
            }
        print(f"{cid}: captured")
    json.dump(manifest, open(output_dir / "manifest.json", "w"), indent=1)
    print(f"wrote {output_dir/'manifest.json'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-spec", type=Path, default=ROOT / "slop/eval_fresh_batch.json")
    ap.add_argument("--output-dir", type=Path, default=ROOT / "out/2026-09-12_exact-input-bank")
    ap.add_argument("--preflight-only", action="store_true")
    a = ap.parse_args()
    if a.preflight_only:
        pf = preflight(a.batch_spec)
        (ROOT / ".local/preflight/exact_input_preflight.json").parent.mkdir(parents=True, exist_ok=True)
        (ROOT / ".local/preflight/exact_input_preflight.json").write_text(json.dumps(pf, indent=1))
        print(f"preflight: {len(pf['checks'])} checks, {len(pf['failures'])} failures")
        for f in pf["failures"]:
            print("FAIL", f)
        sys.exit(1 if pf["failures"] else 0)
    capture(a.batch_spec, a.output_dir)
