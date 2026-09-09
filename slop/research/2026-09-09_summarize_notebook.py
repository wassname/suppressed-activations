"""Summarize executed development-evidence notebook outputs. -- PI/OpenAI"""
import json
import re
from pathlib import Path

nb = json.loads(Path("slop/research/2026-09-09_development-evidence.ipynb").read_text())
full = ""
errors = 0
for cell in nb["cells"]:
    for out in cell.get("outputs", []):
        if out.get("output_type") == "error":
            errors += 1
        text = out.get("text", "")
        full += "".join(text) if isinstance(text, list) else text
statuses = re.findall(r"32-token preview \[([A-Z-]+)", full)
loops = len(re.findall(r"loop=True", full))
mismatch = full.count("MISMATCH")
report = (
    "notebook: slop/research/2026-09-09_development-evidence.ipynb\n"
    f"cells: {len(nb['cells'])}, errors: {errors}\n"
    f"preview statuses: {statuses}\n"
    f"random rows with loop flag: {loops}\n"
    f"MISMATCH lines: {mismatch}\n"
)
print(report)
Path("slop/audits/2026-09-09_notebook-verify.log").write_text(report)
