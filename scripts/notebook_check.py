"""Check the executed public notebook. Written by PI/gpt-5.4."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def output_text(output: dict) -> str:
    parts = []
    text = output.get("text", "")
    parts.extend(text if isinstance(text, list) else [text])
    for value in output.get("data", {}).values():
        parts.extend(value if isinstance(value, list) else [value])
    return "".join(str(part) for part in parts)


def main() -> None:
    notebook = json.loads((ROOT / "nbs/demo.ipynb").read_text())
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert code_cells
    assert [cell["execution_count"] for cell in code_cells] == list(
        range(1, len(code_cells) + 1)
    )
    outputs = [output for cell in code_cells for output in cell["outputs"]]
    assert not any(output["output_type"] == "error" for output in outputs)

    text = "".join(output_text(output) for output in outputs)
    source = (ROOT / "nbs/demo.py").read_text()
    assert "'git':" in text and "-dirty" not in text
    assert "one vector at residual L26, final prompt token" in text
    assert "spins webs" in text and "man's best friend" in source
    assert text.count("Input (`repr`") == 2
    assert "what it is thinking but not saying" in text
    assert "Replacement readout" in text and "what we insert" in text
    assert "Spider" in text and "dog" in text and "canine" in text
    assert "8.\nHypothesis: The animal that spins webs" in text
    assert "4.\nHypothesis: The animal that spins webs" in text
    assert text.count("Generation (next 12 tokens, verbatim)") == 2
    assert text.count("| rank   | token") == 2
    assert "0.882568" in text and "0.490091" in text and "0.297255" in text
    assert "**8**" in text and "**4**" in text
    assert "matched-random" in source and "21 of 256" in source
    assert "2 + 2" in source and "semantic `spider → dog` swap" in source
    assert "GENERATION_TOKENS" in source and "generate(" in source
    assert "SUPPRESSED_ANT" not in source and '"ant":' not in source
    assert "jacobian" not in source.lower() and "j-space" not in source.lower()
    assert notebook["metadata"]["jupytext"]["formats"] == "py:percent,ipynb"
    print("PASS: executed notebook contains one spider-to-dog demo and two top-token tables")


if __name__ == "__main__":
    main()
