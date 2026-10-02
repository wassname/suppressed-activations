"""Write five new country-pair configs for the frozen all-position J coordinate swap, and check tokenisation.
Pairs fixed before any run. Same prompt templates and settings as data/sweden_japan_joint_chat_v2_allpos.json. — PI/OpenAI"""
import copy
import json
from pathlib import Path

from transformers import AutoTokenizer

PAIRS = [  # (country A, city in A, capital A, currency A), (country B, ...)
    (("Germany", "Munich", "Berlin", "EUR"), ("Brazil", "Rio de Janeiro", "Brasília", "BRL")),
    (("France", "Lyon", "Paris", "EUR"), ("India", "Mumbai", "New Delhi", "INR")),
    (("Canada", "Toronto", "Ottawa", "CAD"), ("Australia", "Sydney", "Canberra", "AUD")),
    (("Spain", "Barcelona", "Madrid", "EUR"), ("Mexico", "Guadalajara", "Mexico City", "MXN")),
    (("China", "Shanghai", "Beijing", "CNY"), ("Egypt", "Alexandria", "Cairo", "EGP")),
]
template = json.loads(Path("data/sweden_japan_joint_chat_v2_allpos.json").read_text())
donor_template = json.loads(Path("data/sweden_japan_donors_chat_v1.json").read_text())
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", local_files_only=True)
out_dir = Path("data/country_pairs_allpos_v1")
out_dir.mkdir(exist_ok=True)
ASK = "For the country containing {city}, give its capital and three-letter currency code. Reply only as '<capital>; <currency code>'."
ARITH = "A visitor from {city} is nearby. What is 2 + 2, and is that sum odd or even? Reply only as '<sum>; <odd or even>'."
for a, b in PAIRS:
    name = f"{a[0].lower()}_{b[0].lower()}"
    ids = [tok(" " + c, add_special_tokens=False).input_ids for c in (a[0], b[0])]
    assert all(len(i) == 1 for i in ids), (name, ids)
    first = [tok(c, add_special_tokens=False).input_ids[0] for c in (a[2], b[2])]
    assert first[0] != first[1], (name, first)
    donors = copy.deepcopy(donor_template)
    donors.update(concepts=[a[0], b[0]], selection=f"Concept names for the frozen all-position coordinate swap ({name}); no donor preparation is run.")
    (out_dir / f"{name}_concepts.json").write_text(json.dumps(donors, ensure_ascii=False, indent=1) + "\n")
    config = copy.deepcopy(template)
    config.update(selection="New pair, fixed before running, for a rate of the frozen all-position J coordinate swap chosen on Sweden/Japan (2739).",
                  donor_config=str(out_dir / f"{name}_concepts.json"))
    config["cases"] = [
        {"name": f"{a[0]}_to_{b[0]}", "relation": "country_properties", "reverse": False,
         "user_content": ASK.format(city=a[1]), "base_expected": [a[2], a[3]], "edited_expected": [b[2], b[3]]},
        {"name": f"{b[0]}_to_{a[0]}", "relation": "country_properties", "reverse": True,
         "user_content": ASK.format(city=b[1]), "base_expected": [b[2], b[3]], "edited_expected": [a[2], a[3]]},
        {"name": "arithmetic_control", "relation": "arithmetic_control", "reverse": False,
         "user_content": ARITH.format(city=a[1]), "base_expected": ["4", "even"], "edited_expected": ["4", "even"]},
    ]
    config["evaluation"] = {"notes": "Judge capital and currency from the full output; first-token probabilities are not full-name probabilities."}
    (out_dir / f"{name}_joint.json").write_text(json.dumps(config, ensure_ascii=False, indent=1) + "\n")
    print(name, "country ids", ids, "capital first ids", first)
