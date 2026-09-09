"""Fresh vs shared-model batch on production detector-c2. -- PI/Grok"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(outdir):
    d = json.loads((ROOT / outdir / "result.json").read_text())
    assert len(d["rows"]) == 1, outdir
    return d


fresh_dog = load("out/2026-09-09_detector-c2-fresh-dog-name")
fresh_ant = load("out/2026-09-09_detector-c2-fresh-ant-name")
batch_dog = load("out/2026-09-09_detector-c2-dog-name")
batch_ant = load("out/2026-09-09_detector-c2-ant-name")
fd, fa = fresh_dog["rows"][0], fresh_ant["rows"][0]
bd, ba = batch_dog["rows"][0], batch_ant["rows"][0]
report = {"checks": []}


def check(name, ok, detail=""):
    report["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("PASS " if ok else "FAIL ") + name, detail)


gates = []
for label, fresh, batched, F, B in (
    ("dog", fd, bd, fresh_dog, batch_dog),
    ("ant", fa, ba, fresh_ant, batch_ant),
):
    gates.append((f"{label} resolved config identical", fresh["config"] == batched["config"]))
    for sample in ("source", "donor", "extraction_source", "extraction_donor"):
        gates.append((
            f"{label} rendered {sample} input IDs identical",
            F.get("rendered_inputs", {}).get(sample, {}).get("input_ids")
            == B.get("rendered_inputs", {}).get(sample, {}).get("input_ids"),
        ))
for name, ok in gates:
    check("GATE " + name, ok)
assert all(ok for _, ok in gates), "unequal inputs: output comparison refused"

for label, fresh, batched in (("dog", fd, bd), ("ant", fa, ba)):
    sha_f, sha_b = fresh.get("first_logits_sha256"), batched.get("first_logits_sha256")
    check(f"{label} full-logit sha identical", sha_f == sha_b, (sha_b or {}).get("steered", "")[:12])
    check(f"{label} generated IDs identical",
          fresh["generation"]["token_ids"] == batched["generation"]["token_ids"])
    check(f"{label} base+donor IDs identical",
          fresh["base_generation"]["token_ids"] == batched["base_generation"]["token_ids"]
          and fresh["donor_generation"]["token_ids"] == batched["donor_generation"]["token_ids"])
    check(f"{label} hook coverage identical",
          fresh["intervention_record"] == batched["intervention_record"])
    rec = batched["intervention_record"]
    ntok = len(batched["generation"]["token_ids"])
    check(f"{label} nonzero hook/decode coverage",
          all(v["decode_steps"] == ntok - 1 and v.get("perturbation_norm", 0) > 0 for v in rec.values()),
          {k: (v["decode_steps"], round(v["perturbation_norm"], 4)) for k, v in rec.items()})
    per = batched.get("persistence", {})
    check(f"{label} selector is vocab-suppression not peak contrast",
          per.get("basis_geometry") == "centered_unit_gain_weighted_unembedding"
          and per.get("shared_rank", 0) >= 1,
          {"basis_geometry": per.get("basis_geometry"), "shared_rank": per.get("shared_rank")})

Path("slop/gpu_detector_c2_compare.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print("DOG steered:\n", bd["generation"]["text"])
print("ANT steered:\n", ba["generation"]["text"])
assert all(c["ok"] for c in report["checks"]), "GPU fresh/shared comparison FAILED"
print("ALL GPU FRESH/SHARED CHECKS PASSED")
