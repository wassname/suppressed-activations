"""Check the single public causal demonstration. Written by PI/gpt-5.4."""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "out/2026-09-05_211609_causal-confirmation/result.json"


def selected_tokens(sample: dict) -> list[str]:
    return [row["token"].strip() for row in sample["selected"]]


def main() -> None:
    data = json.loads(RESULT.read_text())
    readme = (ROOT / "README.md").read_text()
    agents = (ROOT / "AGENTS.md").read_text()

    assert not data["metadata"]["git_describe_at_start"].endswith("-dirty")
    assert data["metadata"]["model_revision"] == data["metadata"]["tokenizer_revision"]
    assert data["metadata"]["intervention_layer"] == 26
    assert data["metadata"]["rank"] == 8
    assert data["metadata"]["strength"] == 4

    source_tokens = selected_tokens(data["sources"]["spider"])
    target_tokens = selected_tokens(data["targets"]["dog"])
    assert "Spider" in source_tokens
    assert {"dog", "Dog", "canine"} <= set(target_tokens)

    clean = data["conditions"]["spider_clean"]["metrics"]
    dog_c1 = data["conditions"]["dog_C1"]["metrics"]
    dog_c4 = data["conditions"]["dog_C4"]["metrics"]
    assert clean["top"][0]["token"] == "8"
    assert dog_c1["top"][0]["token"] == "8"
    assert dog_c4["top"][0]["token"] == "4"
    assert math.isclose(clean["p_8"], 0.882568, abs_tol=1e-6)
    assert math.isclose(dog_c4["p_expected"], 0.490091, abs_tol=1e-6)
    assert math.isclose(dog_c4["p_8"], 0.297255, abs_tol=1e-6)
    assert math.isclose(
        dog_c4["delta_log_odds_expected_vs_8"], 3.25, abs_tol=1e-6
    )

    assert data["random_summary"]["dog"]["below"] == 235
    assert data["random_summary"]["dog"]["random_top_expected"] == 27
    arithmetic = data["conditions"]["two_plus_two_C4"]["metrics"]
    assert arithmetic["top"][0]["token"] == "4"
    assert arithmetic["delta_log_odds_expected_vs_8"] == 3.25
    assert data["generations"]["spider_dog_C4"]["token_ids"] == data["generations"][
        "spider_forced_4"
    ]["token_ids"]

    required = (
        "Are suppressed activations causal?",
        "Suppressed readout: `['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB']`",
        "Target suppressed readout: `['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']`",
        "source = h_spider @ S_spider @ S_spider.T",
        "`C=1` is the constructed replacement and still answers `8`",
        "Re-extracted suppressed readout: `[' Silk', 'Spider', ' spiders'",
        "21 of 256 matched-random interventions",
        "prompt-specific next-answer-state intervention",
    )
    assert all(text in readme for text in required)
    assert "ant → 6" not in readme
    assert "64-token greedy continuations" not in readme
    assert "figs/causal_demo" not in readme
    assert "one demonstration" in agents
    assert "Do not add Ant, translation, long-generation" in agents

    print("PASS: README contains one measured spider-to-dog demonstration")


if __name__ == "__main__":
    main()
