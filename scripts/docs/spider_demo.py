"""Render the saved spider readout; no inference. — PI/OpenAI"""
from unspoken_concepts import ROOT
from unspoken_concepts.demo import DEMO, format_table

if __name__ == "__main__":
    path = ROOT / "docs/readme/includes/demo_spider.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_table(DEMO) + "\n")
    print(path)
