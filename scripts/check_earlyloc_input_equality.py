# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
"""144-entry earlyloc spec vs the exact bank: list-equal rendered IDs per entry/side.
-- PI[glm-5p3-flash]"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.prompt import assistant_prefill_input_ids

BANK = Path(__file__).resolve().parents[1] / "out/2026-09-12_exact-input-bank-att3/manifest.json"
SPEC = Path(__file__).resolve().parents[1] / "slop/common_basis_earlyloc_batch.json"

def main() -> None:
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B",
                                        revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    bank = json.load(open(BANK))
    bank_by_cell = {}
    for name, e in bank["entries"].items():
        bank_by_cell.setdefault(e["cell_id"], {})[e["side"]] = e
    specs = json.load(open(SPEC))
    rows, n_fail, unique = [], 0, set()
    for spec in specs:
        dirname = Path(spec["output_dir"]).name
        cands = [c for c in bank_by_cell if c in dirname]
        assert len(cands) == 1, f"{dirname}: ambiguous/missing bank cell {cands}"
        cell_id = cands[0]
        for side in ("source", "donor"):
            prompt = spec["source_prompt"] if side == "source" else spec["target_prompt"]
            chat = assistant_prefill_input_ids(tok, prompt, device="cpu",
                                               instruction=spec["prefill_instruction"])
            got = chat["input_ids"][0].tolist()
            want = bank_by_cell[cell_id][side]["input_ids"]
            equal = got == want
            n_fail += (not equal)
            unique.add((cell_id, side))
            rows.append({"dir": dirname, "side": side, "cell": cell_id,
                         "list_equal_bank_ids": equal, "n_got": len(got), "n_bank": len(want)})
    out = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-earlyloc-input-equality.json"
    json.dump({"n_checks": len(rows), "n_fail": n_fail,
               "unique_prompt_sides": len(unique), "rows": rows}, open(out, "w"), indent=1)
    print(f"earlyloc spec: {len(rows)-n_fail}/{len(rows)} LIST-EQUAL to bank input_ids "
          f"({len(unique)} unique prompt-sides); {n_fail} failures")
    if n_fail:
        sys.exit(1)

if __name__ == "__main__":
    main()
