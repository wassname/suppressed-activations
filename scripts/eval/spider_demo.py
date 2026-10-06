"""Rerun the measured spider readout; one GPU. — PI/OpenAI"""
import copy
import json
import time

import torch

from unspoken_concepts import ROOT
from unspoken_concepts.benchmark import top_words
from unspoken_concepts.demo import DEMO, format_table
from unspoken_concepts.model import MODEL, REVISION, forward, readout, vocab
from unspoken_concepts.methods.jacobian_lens import jlens

if __name__ == "__main__":
    result = copy.deepcopy(DEMO)
    with torch.no_grad():
        res, _, logits = forward(result["prompt"])
        for row in result["readouts"]:
            scores = readout(jlens(res[row["layer"], -1].float(), row["layer"]))
            row["words"] = [vocab[t].strip() for t in top_words(scores)]
    result["answer"] = vocab[int(logits.argmax())].strip()
    result["provenance"] = {"model": MODEL, "revision": REVISION,
                            "lens": "published Qwen3.5-4B J-lens; last prompt token"}
    out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_spider_demo"
    out.mkdir(parents=True)
    (out / "spider_demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(format_table(result), f"\n{out / 'spider_demo.json'}")
