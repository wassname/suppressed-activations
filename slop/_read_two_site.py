import json, glob, os

# Deterministic read of the 8 two-site-strength cells.
cells = sorted(glob.glob("out/2026-09-10_two-site-str-*/"))
print("cell | answer_patch_strength | L20 strength | answer_patch_layer | target | first_token | r2 | bare_answer_mass | generation (first 120 chars)")
print("-"*180)
for d in cells:
    rp = os.path.join(d, "result.json")
    r = json.load(open(rp))
    row = r["rows"][0]
    cfg = row.get("config", {})
    # find answer_patch fields, may be nested
    def find(dct, key):
        if isinstance(dct, dict):
            if key in dct:
                return dct[key]
            for v in dct.values():
                res = find(v, key)
                if res is not None:
                    return res
        return None
    ap_s = find(cfg, "answer_patch_strength")
    ap_l = find(cfg, "answer_patch_layer")
    strength = find(cfg, "strength")
    il = find(cfg, "intervention_layer")
    target = find(r, "target_concept") or cfg.get("target_concept")
    ft = row.get("first_token")
    r2 = row.get("repeated_bigram_fraction")
    bam = row.get("bare_answer_mass")
    gen = row.get("generation") or ""
    if not gen:
        gen = row.get("generation_tokens") and "".join(str(t) for t in row["generation_tokens"])
    # generation may be list of tokens; get text via 'generation'
    gentext = row.get("generation")
    if isinstance(gentext, list):
        gentext = " ".join(str(x) for x in gentext)
    print(f"{os.path.basename(d.rstrip('/'))} | {ap_s} | {strength} | {ap_l} | {target} | {ft!r} | {r2} | {bam} | {str(gentext)[:120]!r}")
    print("   config keys containing patch/answer:", {k:v for k,v in cfg.items() if 'patch' in k or 'answer' in k or 'span' in k})
