import json, glob, os, sys
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", use_fast=False)

cells = sorted(glob.glob("out/2026-09-10_two-site-str-*/"))
out_lines = []
for d in cells:
    r = json.load(open(os.path.join(d, "result.json")))
    row = r["rows"][0]
    g = row.get("generation")
    ids = None
    if isinstance(g, dict):
        ids = g.get("token_ids")
        text = tok.decode(ids) if ids else "NO_IDS"
    elif isinstance(g, list):
        text = " ".join(str(x) for x in g)
    else:
        text = str(g)
    cell = os.path.basename(d.rstrip("/"))
    ft = row.get("first_token")
    r2 = row.get("repeated_bigram_fraction")
    out_lines.append("="*90)
    out_lines.append(f"{cell} | first_token={ft!r} | r2={r2}")
    out_lines.append(repr(text)[:900])
    out_lines.append("")

# Also decode the FULL generation from result.json for prop-ant C0.05 and C0.15
# and prop-dog C0.3 (the '1. Yes' case), printing full text and token count.
for target in ["prop-ant-C0.05", "prop-ant-C0.15", "prop-dog-C0.3", "prop-dog-C0.6"]:
    d = f"out/2026-09-10_two-site-str-{target}/"
    r = json.load(open(os.path.join(d, "result.json")))
    row = r["rows"][0]
    g = row.get("generation")
    ids = g.get("token_ids") if isinstance(g, dict) else None
    if ids:
        text = tok.decode(ids)
        out_lines.append("#"*90)
        out_lines.append(f"FULL {target}: {len(ids)} tokens")
        out_lines.append(repr(text))
        out_lines.append("")

print("\n".join(out_lines))
