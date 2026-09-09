"""Verify repaired notebook: markdown rendering, links, counts. -- PI/OpenAI"""
import json
import re
from pathlib import Path

nb = json.loads(Path("2026-09-09_development-evidence.ipynb").read_text())
md_out, stream_out, errors = 0, 0, 0
md_text = ""
for cell in nb["cells"]:
    for out in cell.get("outputs", []):
        if out.get("output_type") == "error":
            errors += 1
        if out.get("output_type") == "display_data" and "text/markdown" in out.get("data", {}):
            md_out += 1
            md_text += "".join(out["data"]["text/markdown"])
        if out.get("output_type") == "stream":
            stream_out += 1
links = re.findall(r"\]\(([^)]+)\)", md_text)
missing = [l for l in links if not (Path(".").resolve() / l).exists()]
fences = md_text.count("```text")
first32 = re.findall(r"First 32 of (\d+) generated", md_text)
report = (
    "repaired notebook verification\n"
    f"cells: {len(nb['cells'])}, errors: {errors}\n"
    f"markdown displays: {md_out}, plain-text streams: {stream_out}\n"
    f"fenced text blocks: {fences}\n"
    f"first32 length labels: {first32}\n"
    f"links: {len(links)}, missing targets: {missing}\n"
    "strict decode equality + single model/revision asserted at execute time (no error = passed)\n"
)
print(report)
Path("../audits/2026-09-09_notebook-verify.log").write_text(report)
assert errors == 0 and not missing and stream_out == 0
print("ALL CHECKS PASSED")
