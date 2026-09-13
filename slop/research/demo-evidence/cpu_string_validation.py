import json, os, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, ".")
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
report = []
THINK = "<think>\n\n</think>"
for donor in ("dog", "ant"):
    r = json.load(open(f"out/2026-09-10_replay-C1.5-legs-{donor}/result.json"))
    ri = r["rendered_inputs"]
    row = r["rows"][0]
    src_ids = ri["source"]["input_ids"]
    src_re = ri["source"]["rendered"]
    re_ids = tok(src_re, add_special_tokens=False).input_ids
    assert re_ids == src_ids, f"{donor}: rendered text != saved ids"
    assert src_re.endswith(" "), f"{donor}: source prompt lacks trailing space"
    assert tok.decode([src_ids[-1]]) == " ", f"{donor}: last token is not a space"
    assert THINK in src_re, f"{donor}: saved empty think missing from rendered input"
    for name, gen in (("base", row["base_generation"]), ("steered", row["generation"])):
        ids = gen["token_ids"]
        assert tok.decode(ids) == gen["text"], f"{donor}/{name}: text != decode(ids)"
        report.append({"donor": donor, "gen": name, "n_tokens": len(ids),
                       "ends_im_end": gen["text"].endswith("<|im_end|>")})
    d_re = ri["donor"]["rendered"]
    assert d_re.endswith(" ") and THINK in d_re
    report.append({"donor": donor, "source_n_ids": len(src_ids),
                   "donor_n_ids": len(ri["donor"]["input_ids"]),
                   "source_tail_ids": src_ids[-3:],
                   "source_tail_decoded": repr(tok.decode(src_ids[-3:]))})
print(json.dumps(report, indent=1))
print("CPU STRING VALIDATION PASS")
