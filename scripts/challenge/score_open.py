"""Score an external open-method adapter with the shared benchmark. — PI/OpenAI"""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback

import torch
from tabulate import tabulate


REQUIRED_METADATA = ("name", "author", "data", "access", "supervision", "code", "revision", "settings", "overlap")


def load_adapter(path):
    path = Path(path).resolve()
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("challenge_entry", path)
    entry = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = entry
    spec.loader.exec_module(entry)
    for key in REQUIRED_METADATA:
        assert key in entry.METADATA, f"METADATA missing {key}"
    assert callable(entry.calibrate) and callable(entry.method)
    json.dumps(entry.METADATA)
    return entry


def calibrate_entry(entry, model, tokenizer, texts):
    with torch.enable_grad():
        return entry.calibrate(model, tokenizer, texts)


def predict(entry, model, tokenizer, prompt, state, width):
    with torch.enable_grad():
        vector = entry.method(model, tokenizer, prompt, state)
    assert isinstance(vector, torch.Tensor) and vector.shape == (width,), "return one residual vector [d]"
    assert vector.is_floating_point() and torch.isfinite(vector).all(), "return a finite floating-point vector"
    return vector.detach()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adapter", type=Path, help="Python file exporting METADATA, calibrate and method")
    args = parser.parse_args()
    entry = load_adapter(args.adapter)
    root = Path(__file__).resolve().parents[2]
    out = root / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_{time.time_ns()}_open"
    out.mkdir(parents=True)
    manifest = {"entry": entry.METADATA, "argv": sys.argv, "adapter": str(args.adapter.resolve()),
                "adapter_sha256": hashlib.sha256(args.adapter.read_bytes()).hexdigest(),
                "benchmark_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()}
    (out / "adapter.py").write_bytes(args.adapter.read_bytes())
    with (out / "run.md").open("w") as log:
        def emit(text):
            print(text, flush=True)
            log.write(text + "\n\n")
            log.flush()

        emit(f"# Open-method evaluation\n\n```json\n{json.dumps(manifest, indent=2)}\n```")
        try:
            from common import MODEL, REVISION, W, model, tok
            from bench import TEST, calibration_prompts, f1, f1_ci, judge, prepare, read_vector, translation_prompts

            manifest.update(model=MODEL, model_revision=REVISION, test_pairs=TEST)
            (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
            emit(f"Model: {MODEL}, revision {REVISION}.\n\n## Calibration")
            texts = calibration_prompts()
            emit(f"First calibration text (repr):\n\n```text\n{texts[0]!r}\n```")
            state = calibrate_entry(entry, model, tok, iter(texts))
            emit("## Evaluation\n\nSHOULD: the adapter receives the prompt only, not evaluator labels or answers.")
            rows, skipped = [], []
            for item in translation_prompts(TEST, "test"):
                with torch.no_grad():
                    prepared = prepare(item)
                if prepared is None:
                    skipped.append({k: item[k] for k in ("split", "word", "prompt")})
                    continue
                _, leak_in, leak_out = prepared
                v = predict(entry, model, tok, item["prompt"], state, W.shape[1]).to(W.device)
                with torch.no_grad():
                    result = judge(read_vector(v, entry.METADATA["name"]), item, leak_in, leak_out)
                rows.append({k: item[k] for k in ("role", "split", "word", "prompt")} | result)
                if len(rows) == 1:
                    emit(f"First test prompt (repr):\n\n```text\n{item['prompt']!r}\n```\n\n"
                         f"Readout:\n\n```json\n{json.dumps(result, ensure_ascii=False)}\n```")
            assert rows, "no test prompts survived"
            with gzip.open(out / "rows.json.gz", "wt") as f:
                json.dump({"rows": rows, "skipped": skipped}, f, ensure_ascii=False)
            row = {"method": entry.METADATA["name"], "F1↑ (90% CI)": f"{f1(rows):.2f} ({f1_ci(rows)})",
                   "by": entry.METADATA["author"], **{k: entry.METADATA[k] for k in ("data", "access", "supervision")}}
            emit(f"## Result\n\n{len(rows)} scored; {len(skipped)} skipped. "
                 "[Per-prompt results](rows.json.gz), [provenance](manifest.json), [adapter](adapter.py).\n\n"
                 + tabulate([row], headers="keys", tablefmt="pipe", disable_numparse=True))
        except Exception:
            emit(f"## Failed\n\n```text\n{traceback.format_exc()}\n```")
            raise
        finally:
            emit(str((out / "run.md").relative_to(root)))


if __name__ == "__main__":
    main()
