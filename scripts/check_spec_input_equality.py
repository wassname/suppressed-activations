# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""Exact input equality: render each spec's source/donor through the runner's ACTUAL
assistant_prefill_input_ids (pinned tokenizer) and assert LIST equality with the bank
manifest's saved input_ids. 84 spec entries x 2 sides = 168 outcomes, saved.
-- PI[glm-5p3-flash]"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.prompt import assistant_prefill_input_ids

BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3/manifest.json"
SPEC = Path(__file__).resolve().parents[1] / "slop/common_basis_selsite_batch.json"

def main() -> None:
    bank = json.load(open(BANK))
    bank_by_cell = {}
    for name, e in bank["entries"].items():
        bank_by_cell.setdefault(e["cell_id"], {})[e["side"]] = e
    specs = json.load(open(SPEC))
    rows, n_fail = [], 0
    for spec in specs:
        dirname = Path(spec["output_dir"]).name
        cell_id = next((c for c in bank_by_cell if c in dirname), None)
        assert cell_id, f"no bank cell for {dirname}"
        for side in ("source", "donor"):
            prompt = spec["source_prompt"] if side == "source" else spec["target_prompt"]
            chat = assistant_prefill_input_ids(
                __import__("transformers", fromlist=["AutoTokenizer"]).AutoTokenizer,
                prompt, device="cpu", instruction=spec["prefill_instruction"]) if False else None
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B",
                                                revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
            chat = assistant_prefill_input_ids(tok, prompt, device="cpu",
                                               instruction=spec["prefill_instruction"])
            got = chat["input_ids"][0].tolist()
            want = bank_by_cell[cell_id][side]["input_ids"]
            equal = got == want
            n_fail += (not equal)
            rows.append({"dir": dirname, "side": side, "cell": cell_id,
                         "list_equal_bank_ids": equal,
                         "n_got": len(got), "n_bank": len(want),
                         "sha_got": __import__("hashlib").sha256(
                             json.dumps(got).encode()).hexdigest()[:12]})
    out = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-selsite-input-equality.json"
    json.dump({"n_checks": len(rows), "n_fail": n_fail, "rows": rows}, open(out, "w"), indent=1)
    print(f"input equality: {len(rows) - n_fail}/{len(rows)} LIST-EQUAL to bank input_ids; {n_fail} failures")
    if n_fail:
        for r in rows:
            if not r["list_equal_bank_ids"]:
                print("FAIL", r["dir"], r["side"], r["n_got"], "vs", r["n_bank"])
        sys.exit(1)

if __name__ == "__main__":
    main()
