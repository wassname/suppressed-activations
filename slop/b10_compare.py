"""C=0 identity on span-none vocab path: steered == clean source. -- PI/OpenAI"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(outdir):
    d = json.loads((ROOT / outdir / "result.json").read_text())
    assert len(d["rows"]) == 1, outdir
    return d


fresh_dog = load("out/b10_cpu_fresh_dog")
fresh_ant = load("out/b10_cpu_fresh_ant")
batch_dog = load("out/b10_cpu_batch_dog")
batch_ant = load("out/b10_cpu_batch_ant")
fd, fa = fresh_dog["rows"][0], fresh_ant["rows"][0]
bd, ba = batch_dog["rows"][0], batch_ant["rows"][0]
report = {"checks": []}


def check(name, ok, detail=""):
    report["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("PASS " if ok else "FAIL ") + name, detail)


loads = [json.loads(line) for line in Path("slop/b10_load_calls.log").read_text().splitlines()]
check("loader calls: 2 fresh + 1 batch",
      sum("batch-spec" not in json.dumps(l["argv"]) for l in loads) == 2
      and sum("batch-spec" in json.dumps(l["argv"]) for l in loads) == 1)
gates = []
for label, fresh, batched in (("dog", fd, bd), ("ant", fa, ba)):
    gates.append((f"{label} resolved config identical", fresh["config"] == batched["config"]))
    assert fresh["config"]["strength"] == 0.0, "not a C=0 condition"
    for sample in ("source", "donor", "extraction_source", "extraction_donor"):
        gates.append((f"{label} rendered {sample} input IDs identical",
              fresh.get("rendered_inputs", {}).get(sample, {}).get("input_ids") ==
              batched.get("rendered_inputs", {}).get(sample, {}).get("input_ids")))
for name, ok in gates:
    check("GATE " + name, ok)
assert all(ok for _, ok in gates), "unequal inputs: output comparison refused"
for label, fresh, batched in (("dog", fd, bd), ("ant", fa, ba)):
    check(f"{label} steered logits == clean source logits",
          batched["first_logits_sha256"]["steered"] == batched["first_logits_sha256"]["base"] == fresh["first_logits_sha256"]["base"],
          batched["first_logits_sha256"]["steered"][:12])
    check(f"{label} steered IDs == clean source IDs",
          batched["generation"]["token_ids"] == batched["base_generation"]["token_ids"] == fresh["base_generation"]["token_ids"])
    rec = batched["intervention_record"]
    ntok = len(batched["generation"]["token_ids"])
    check(f"{label} hooks installed: coverage covers actual generation",
          all(v["decode_steps"] == ntok - 1 and len(v["prefill_positions"]) > 0 for v in rec.values()),
          {k: (v["decode_steps"], v["prefill_positions"]) for k, v in rec.items()})
    check(f"{label} perturbation norms are zero (C=0, not nonzero)",
          all(v["perturbation_norm"] == 0.0 for v in rec.values()),
          {k: v["perturbation_norm"] for k, v in rec.items()})
    check(f"{label} fresh/batch steered identical", fresh["generation"]["token_ids"] == batched["generation"]["token_ids"])
Path("slop/b10_batch_cpu_check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
assert all(c["ok"] for c in report["checks"]), "C=0 identity check FAILED"
print("ALL C=0 CHECKS PASSED")
