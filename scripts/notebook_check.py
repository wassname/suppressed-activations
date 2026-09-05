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
    source = (ROOT / "nbs/demo.py").read_text()
    assert "'git':" in text and "-dirty" not in text
    assert "one vector at residual L26, final prompt token" in text
    assert "Spider" in text and "dog, target" in text
    assert "spider after ant, C=4" in text and "spider after dog, C=4" in text
    assert "target/source log odds" in text and "distance/residual" in text
    assert all(value in text for value in ("-1.0000", "+0.0000", "+1.0000", "+4.0000", "+8.0000"))
    assert "animal that spins webs has 6 legs" in text
    assert "animal that spins webs has 4 legs" in text
    assert "238/256" in source and "235/256" in source
    assert "not proof that an Ant or Dog concept" in source
    assert notebook["metadata"]["jupytext"]["formats"] == "py:percent,ipynb"
    print("PASS: executed notebook has one-site extraction, two targets, signed doses, and exact continuations")


if __name__ == "__main__":
    main()
