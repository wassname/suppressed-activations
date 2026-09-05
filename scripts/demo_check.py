"""Check the committed causal demo. Written by PI/gpt-5.4."""

import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "data/causal_demo.json").read_text())
    spider_ant = json.loads((ROOT / "data/spider_ant_demo.json").read_text())
    metadata = data["metadata"]
    readme = (ROOT / "README.md").read_text()
    assert not metadata["git_describe"].endswith("-dirty")
    assert metadata["source_hidden_word"] in {
        row["token"].strip().lower() for row in data["source_selected_tokens"]
    }
    assert metadata["target_hidden_word"] in {
        row["token"].strip().lower() for row in data["target_selected_tokens"]
    }
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
    assert len(random_rows) == metadata["random_control_count"]
    semantic_odds = rows["replace"]["log_odds_target_vs_source"]
    random_odds = [row["metrics"]["log_odds_target_vs_source"] for row in random_rows]
    assert sum(value < semantic_odds for value in random_odds) / len(random_odds) >= 0.95

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

    spider_row = next(
        row for row in spider_ant["rows"]
        if row["normalized"] and row["mask"] == "all" and row["strength"] == 1
    )
    assert spider_ant["clean"][0]["token"] == "8"
    assert spider_row["top"][0]["token"] == "8"
    assert spider_row["delta_logp6"] > 0
    assert "Spider" in spider_ant["selected_tokens_at_final"]

    required_readme_text = (
        "Fact: The number of legs on the animal that spins webs is",
        "the animal that barks and is called man's best friend",
        "source = h @ S_spider @ S_spider.T",
        "248 of 256",
        "Gurnee et al., Figures",
        "Ours come from the LM-head rise-and-fall score",
        "scripts/spider_ant_demo.py",
        "0.121 nats",
    )
    assert all(text in readme for text in required_readme_text)

    png = (ROOT / "figs/causal_demo.png").read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", png[16:24])
    assert width >= 2400 and height >= 800
    svg = (ROOT / "figs/causal_demo.svg").read_text()
    assert "Clean next token: 8" in svg and "248/256 random effects are smaller" in svg
    print("PASS: causal demo README, figure, provenance, controls, metrics, and generations")


if __name__ == "__main__":
    main()
