"""Recover saved experiment evidence without model inference. -- PI/OpenAI"""
import hashlib
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = [
    ("local-dog", "2026-09-08_051304_attenuation-local-dog", [3, 11]),
    ("frozen-synchronized-ant", "2026-09-08_131500_synchronized-attenuation-ant", [5, 11]),
    ("band-dog", "2026-09-08_133000_synchronized-band-dog", [9]),
    ("band-ant", "2026-09-08_133000_synchronized-band-ant", [9]),
    ("fixed-dog-legs", "2026-09-08_134000_fixed-band-dog-legs", [9]),
    ("fixed-ant-legs", "2026-09-08_134000_fixed-band-ant-legs", [9]),
    ("fixed-dog-name", "2026-09-08_134000_fixed-band-dog-name", [9]),
    ("fixed-ant-name", "2026-09-08_134000_fixed-band-ant-name", [9]),
]


def main():
    records = []
    lines = ["# Recovered intervention references", "", "Saved model outputs, not new inference. -- PI/OpenAI", ""]
    for name, directory, indices in CASES:
        path = ROOT / "out" / directory / "result.json"
        data = json.loads(path.read_text())
        for index in indices:
            row = next(r for r in data["rows"] if int(r["condition_id"].split("_", 1)[0]) == index)
            cfg = row["config"]
            checks = {}
            for layer, trace in row["intervention_record"].items():
                assert trace["decode_steps"] == len(row["generation"]["token_ids"]) - 1
                checks[layer] = {key: trace[key] for key in ("prefill_positions", "decode_steps", "perturbation_norm")}
            matching = {}
            if "code_sha256" in data:
                for module, digest in data["code_sha256"].items():
                    head_bytes = subprocess.check_output(["git", "show", f"a49e4cf:{module}"], cwd=ROOT)
                    matching[module] = hashlib.sha256(head_bytes).hexdigest() == digest
            argv = data["argv"]
            record = {"name": name, "path": str(path.relative_to(ROOT)), "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "condition": row["condition_id"], "git": data["git"], "argv": argv,
                      "code_matches_a49e4cf": matching, "config": cfg,
                      "source_prompt": data["source_prompt"], "target_prompt": data["target_prompt"],
                      "prefill_instruction": row["prefill_instruction"], "extraction_instruction": row["extraction_instruction"],
                      "coverage": checks, "generation": row["generation"], "base": row["base_generation"], "donor": row["donor_generation"]}
            records.append(record)
            lines += [f"## {name}: {row['condition_id']}", "", f"[Original condition](../../out/{directory}/{row['log']}) | [raw result](../../out/{directory}/result.json)", "",
                      f"Recorded git: `{data['git']}`. Current-source hash matches: `{matching}`.", "",
                      f"Config: `{json.dumps(cfg, ensure_ascii=False)}`", "",
                      f"Recorded argv: `{shlex.join(argv)}`", "",
                      f"Coverage: `{json.dumps(checks)}`", ""]
            for field, label in (("base_generation", "Base"), ("donor_generation", "Donor"), ("generation", "Intervention")):
                lines += [f"### {label} ({len(row[field]['token_ids'])} tokens)", "", "```text", row[field]["text"], "```", ""]
    destination = ROOT / "slop/audits/2026-09-09_recovered-references"
    destination.with_suffix(".json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    destination.with_suffix(".md").write_text("\n".join(lines))
    print(f"Recovered {len(records)} conditions; all recorded decode counts equal N-1.")
    for r in records:
        print(r["name"], r["condition"], "hash_matches", r["code_matches_a49e4cf"], "tokens", len(r["generation"]["token_ids"]))
    print(destination.with_suffix(".md").relative_to(ROOT))


if __name__ == "__main__":
    main()
