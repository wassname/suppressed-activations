"""Fresh vs shared-model batch equivalence on tiny CPU model. -- PI/OpenAI"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(outdir):
    d = json.loads((ROOT / outdir / "result.json").read_text())
    assert len(d["rows"]) == 1, outdir
    return d


fresh_dog = load("out/b09_cpu_fresh_dog")
fresh_ant = load("out/b09_cpu_fresh_ant")
batch_dog = load("out/b09_cpu_batch_dog")
batch_ant = load("out/b09_cpu_batch_ant")
batch_rep = load("out/b09_cpu_batch_dog_repeat")
fd, fa = fresh_dog["rows"][0], fresh_ant["rows"][0]
bd, ba, br = batch_dog["rows"][0], batch_ant["rows"][0], batch_rep["rows"][0]
report = {"checks": []}


def check(name, ok, detail=""):
    report["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("PASS " if ok else "FAIL ") + name, detail)


loads = [json.loads(line) for line in Path("slop/b09_load_calls.log").read_text().splitlines()]
fresh_lines = [l for l in loads if "batch-spec" not in json.dumps(l["argv"])]
batch_lines = [l for l in loads if "batch-spec" in json.dumps(l["argv"])]
check("loader calls: 2 fresh + 1 batch", len(fresh_lines) == 2 and len(batch_lines) == 1,
      f"fresh={len(fresh_lines)} batch={len(batch_lines)}")
check("loader used tiny model on cpu",
      all(l["model"] == "wassname/qwen3-5lyr-tiny-random" and l["device"] == "cpu" for l in loads))
gates = []
for label, fresh, batched in (("dog", fd, bd), ("ant", fa, ba), ("dog_repeat_vs_fresh_dog", fd, br)):
    gates.append((f"{label} resolved config identical", fresh["config"] == batched["config"]))
    for sample in ("source", "donor", "extraction_source", "extraction_donor"):
        gates.append((f"{label} rendered {sample} input IDs identical",
              fresh.get("rendered_inputs", {}).get(sample, {}).get("input_ids") ==
              batched.get("rendered_inputs", {}).get(sample, {}).get("input_ids")))
for name, ok in gates:
    check("GATE " + name, ok)
assert all(ok for _, ok in gates), "unequal inputs: output comparison refused"
for label, fresh, batched in (("dog", fd, bd), ("ant", fa, ba), ("dog_repeat_vs_fresh_dog", fd, br)):
    check(f"{label} full-logit sha identical",
          fresh["first_logits_sha256"] == batched["first_logits_sha256"],
          fresh["first_logits_sha256"]["steered"][:12])
    check(f"{label} generated IDs identical",
          fresh["generation"]["token_ids"] == batched["generation"]["token_ids"])
    check(f"{label} base+donor IDs identical",
          fresh["base_generation"]["token_ids"] == batched["base_generation"]["token_ids"]
          and fresh["donor_generation"]["token_ids"] == batched["donor_generation"]["token_ids"])
    check(f"{label} hook coverage identical",
          fresh["intervention_record"] == batched["intervention_record"])
    rec = batched["intervention_record"]
    check(f"{label} nonzero hook/decode coverage",
          all(v["decode_steps"] > 0 and v["perturbation_norm"] > 0 for v in rec.values()),
          {k: (v["decode_steps"], round(v["perturbation_norm"], 4)) for k, v in rec.items()})
check("batch ant ran after dog yet equals fresh ant (reorder, non-vacuous)",
      ba["generation"]["token_ids"] == fa["generation"]["token_ids"]
      and ba["first_logits_sha256"] == fa["first_logits_sha256"])
check("extraction cache hit on shared source in batch",
      len((batch_ant.get("extraction_cache") or {}).get("hits", [])) > 0,
      (batch_ant.get("extraction_cache") or {}).get("hits"))
for label, row in (("dog", bd), ("ant", ba), ("dog_repeat", br)):
    per = row.get("persistence", {})
    check(f"{label} selector is vocab-suppression, not peak contrast",
          per.get("basis_geometry") == "centered_unit_gain_weighted_unembedding"
          and per.get("shared_rank", 0) >= 1
          and "template_contrast" not in str(per.get("selector", "")),
          {"basis_geometry": per.get("basis_geometry"), "shared_rank": per.get("shared_rank"),
           "selector": per.get("selector", "<absent>")})
check("runner persists rendered input IDs (source/donor/extraction)",
      all(set(v.get("rendered_inputs", {})) == {"source", "donor", "extraction_source", "extraction_donor"}
          and all(len(x["input_ids"]) > 0 and len(x["rendered"]) > 0 for x in v["rendered_inputs"].values())
          for v in (batch_dog, batch_ant)),
      {k: len(v["input_ids"]) for k, v in batch_dog["rendered_inputs"].items()})
report["runtimes"] = {k: v.get("elapsed_seconds") for k, v in
                      (("fresh_dog", fresh_dog), ("fresh_ant", fresh_ant), ("batch_dog", batch_dog),
                       ("batch_ant", batch_ant), ("batch_repeat", batch_rep))}
report["model_load_seconds"] = {k: v.get("model_load_seconds") for k, v in
                                (("fresh_dog", fresh_dog), ("fresh_ant", fresh_ant),
                                 ("batch_dog", batch_dog), ("batch_ant", batch_ant))}
report["rendered_inputs"] = batch_dog["rendered_inputs"]
Path("slop/b09_batch_cpu_check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print("runtimes:", json.dumps(report["runtimes"]))
assert all(c["ok"] for c in report["checks"]), "batch CPU check FAILED"
print("ALL BATCH CPU CHECKS PASSED")
