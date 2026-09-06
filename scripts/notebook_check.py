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
    assert "chat template with assistant fact prefill" in text
    assert "residual L24, final 4 fact tokens" in text
    assert "spins webs" in text and "man's best friend" in source
    assert text.count("Input (`repr`") == 2
    assert text.count("Rendered model input (`repr`") == 2
    assert "<|im_start|>user" in text and "<|im_start|>assistant" in text
    assert text.count("what it is thinking but not saying") == 2
    assert "Readout after intervention" in text
    assert "['狗粮', '吠', 'สุนัข', ' собаки', '养犬', ' собак', ' perros', ' dogg']" in text
    assert "dog prompt" in source
    assert "8.\n\n**Explanation:**\nThe animal that spins webs is the **spider**." in text
    assert "4.\n\n**Explanation:**\nThe animal that spins webs is the **spider**." in text
    assert text.count("Generation (next 32 tokens, verbatim)") == 2
    assert text.count("| rank   | token") == 2 and "Δ log p" in text
    assert "0.945299" in text and "0.701417" in text and "0.200959" in text
    assert "**8**" in text and "*4*" in text and "**4**" in text and "*8*" in text
    assert "+3.202" in text and "-1.548" in text
    assert "smallest tested" in source and "target-answer-state transfer" in source
    assert "GENERATION_TOKENS" in source and "generate(" in source
    assert "SUPPRESSED_ANT" not in source and '"ant":' not in source
    assert "jacobian" not in source.lower() and "j-space" not in source.lower()
    assert notebook["metadata"]["jupytext"]["formats"] == "py:percent,ipynb"
    print("PASS: executed notebook contains one spider-to-dog demo and two top-token tables")


if __name__ == "__main__":
    main()
