"""Check the executed public notebook. Written by PI/gpt-5.4."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    notebook = json.loads((ROOT / "nbs/demo.ipynb").read_text())
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert code_cells
    assert all(cell["execution_count"] is not None for cell in code_cells)
    outputs = [output for cell in code_cells for output in cell["outputs"]]
    assert not any(output["output_type"] == "error" for output in outputs)

    text = "".join(
        "".join(output.get("text", output.get("data", {}).get("text/plain", [])))
        for output in outputs
    )
    assert "'git':" in text and "-dirty" not in text
    assert "'source': [' heart'" in text
    assert "'target': [' school'" in text
    assert all(value in text for value in ("-0.5000", "+0.0000", "+1.0000", "+2.0000"))
    assert "学校" in text and "____" in text
    assert any("image/png" in output.get("data", {}) for output in outputs)
    assert notebook["metadata"]["jupytext"]["formats"] == "py:percent,ipynb"
    print("PASS: executed notebook has clean provenance, both directions, excessive doses, and Figure 2")


if __name__ == "__main__":
    main()
