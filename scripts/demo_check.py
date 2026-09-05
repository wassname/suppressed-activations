"""Check the committed causal demo. Written by PI/gpt-5.4."""

import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "data/causal_demo.json").read_text())
    metadata = data["metadata"]
    readme = (ROOT / "README.md").read_text()
    assert not metadata["git_describe"].endswith("-dirty")
    assert data["source_selected_tokens"][0]["token"].strip() == metadata["source_hidden_word"]
    assert data["target_selected_tokens"][0]["token"].strip() == metadata["target_hidden_word"]
    selected = {
        row["token"].strip()
        for group in (data["source_selected_tokens"], data["target_selected_tokens"])
        for row in group
    }
    assert metadata["source_output"] not in selected
    assert metadata["target_output"] not in selected

    rows = {row["condition"]: row["metrics"] for row in data["interventions"]}
    assert rows["base"]["top"][0]["token"] == metadata["source_output"]
    assert rows["replace"]["top"][0]["token"] == metadata["target_output"]
    assert rows["remove"]["p_source"] < rows["base"]["p_source"]

    random_rows = [
        row for row in data["interventions"] if row["condition"].startswith("random_seed=")
    ]
    assert len(random_rows) == 32
    assert all(row["metrics"]["top"][0]["token"] == metadata["source_output"] for row in random_rows)

    semantic = data["diagnostics"]["replace"]
    random = data["diagnostics"]["random"]
    assert semantic.keys() == random.keys()
    for layer in semantic:
        difference = abs(semantic[layer]["perturbation_norm"] - random[layer]["perturbation_norm"])
        assert difference < 1e-4

    generations = {row["condition"]: row for row in data["generations"]}
    assert generations.keys() == {"base", "replace", "random", "remove"}
    assert all(len(row["token_ids"]) == metadata["max_new_tokens"] for row in generations.values())
    assert generations["base"]["text"].startswith(metadata["source_output"])
    assert generations["replace"]["text"].startswith(metadata["target_output"])
    assert generations["random"]["text"].startswith(metadata["source_output"])
    assert generations["remove"]["text"].startswith(metadata["source_output"])

    required_readme_text = (
        metadata["source_prompt"],
        metadata["target_prompt"],
        "source_component = h @ S_source @ S_source.T",
        "residual norm fixed",
        "None of 32 random",
        "Gurnee et al., Figures",
        "uses only the LM-head rise-and-fall method",
        "figs/causal_demo.png",
    )
    assert all(text in readme for text in required_readme_text)
    for row in generations.values():
        assert row["text"][:40] in readme

    png = (ROOT / "figs/causal_demo.png").read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", png[16:24])
    assert width >= 2400 and height >= 800
    svg = (ROOT / "figs/causal_demo.svg").read_text()
    assert "Clean next token" in svg and "Only replacement favors school" in svg
    print("PASS: causal demo README, figure, provenance, controls, metrics, and generations")


if __name__ == "__main__":
    main()
