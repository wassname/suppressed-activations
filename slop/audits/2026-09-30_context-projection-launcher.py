"""One bounded validation-then-causal job; fixed settings, no retry. — PI/OpenAI"""

import gc
import json
import runpy
import sys
from pathlib import Path

import torch
from loguru import logger


def run():
    root = Path.cwd()
    main = runpy.run_path(sys.argv[1])["main"]
    validation = main(validate_donor_coordinates_json=Path(sys.argv[2]), fit_nuisance=True)
    result = json.loads((validation / "result.json").read_text())
    manifest = {"validation": str(validation), "passed": result["candidate_passes_prerequisite"],
                "causal_runs": [], "max_generated_tokens": 320, "author": "PI/OpenAI"}
    manifest_path = validation / "pipeline.json"
    manifest_path.write_text(json.dumps(manifest, indent=1))
    logger.remove()
    logger.add(sys.stderr)
    if not manifest["passed"]:
        logger.info("Prerequisite failed; no causal generations for this candidate. Both goals remain open.")
        print(validation / "run.md")
        return
    assert result["n_prefills"] == 16 and result["corrected_brackets"] == 8
    for relation in ("legs", "skeleton_body"):
        gc.collect()
        torch.cuda.empty_cache()
        logger.remove()
        logger.add(sys.stderr)
        output = main(block_index=15, readout_block_index=23, reverse=True, prompt_positions=1,
                      decode_scale=1.0, plural=True, donor_reflection=True, relation=relation,
                      donor_checkpoint=root / "out/2026-09-30_133218_jlens-one-pass/donors.pt",
                      reflection_coordinate_checkpoint=validation / "projection.pt")
        manifest["causal_runs"].append({"relation": relation, "path": str(output)})
        manifest_path.write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    run()
