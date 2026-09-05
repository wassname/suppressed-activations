import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/workspace/2026/suppressed-activations")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import top_tokens, trajectory

MODEL = "Qwen/Qwen3.5-4B"
EARLY, PEAK, OUTPUT = 23, 25, 32
CASES = [
    ("spider", "spins webs", "8"),
    ("bee", "produces honey", "6"),
    ("elephant", "has a trunk and tusks", "4"),
    ("dog", "barks and is called man's best friend", "4"),
    ("cat", "purrs and says meow", "4"),
    ("sheep", "grows wool on a farm", "4"),
    ("owl", "is a bird known for hooting at night", "2"),
    ("crab", "has claws and walks sideways", "10"),
    ("butterfly", "emerges from a chrysalis with colorful wings", "6"),
    ("cricket", "is an insect that chirps and jumps", "6"),
]


def variants(tokenizer, word):
    result = {}
    for text in (word, " " + word, word.capitalize(), " " + word.capitalize(), word + "s", " " + word + "s"):
        ids = tokenizer(text, add_special_tokens=False).input_ids
        if len(ids) == 1:
            result[text] = ids[0]
    return result


torch.set_grad_enabled(False)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
invalid_cases = [hidden for hidden, _, _ in CASES if not variants(tokenizer, hidden)]
if invalid_cases:
    raise ValueError(f"Hidden concepts need at least one single-token variant: {invalid_cases}")
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
language_model = model.model
W = model.lm_head.weight.float()
gain = (1.0 + language_model.norm.weight).float()
row_norm = (W * gain).norm(dim=-1).clamp_min(1e-8)
rows = []

for hidden, description, expected in CASES:
    prompt = f"Fact: The number of legs on the animal that {description} is "
    input_ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    residuals, clean_logits = trajectory(model, input_ids, language_model.norm)
    h = residuals[[EARLY, PEAK, OUTPUT], -1].float()
    h = h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)
    z = ((h * gain) @ W.T) / row_norm
    rise = z[1] - z[0]
    fall = z[1] - z[2]
    rise -= rise.mean()
    fall -= fall.mean()
    score = torch.minimum(rise.clamp_min(0), fall.clamp_min(0))
    token_ids = variants(tokenizer, hidden)
    ranked = sorted(
        (int((score > score[token_id]).sum()) + 1, text, token_id)
        for text, token_id in token_ids.items()
    )
    best_rank, best_variant, _ = ranked[0]
    top_ids = score.topk(12).indices.tolist()
    clean_top = top_tokens(tokenizer, clean_logits, 5)
    clean_matches = clean_top[0]["token"].strip().lower() == expected.lower()
    row = {
        "hidden": hidden,
        "prompt": prompt,
        "expected": expected,
        "clean_top": clean_top,
        "clean_matches": clean_matches,
        "rank": best_rank,
        "variant": best_variant,
        "top12": [tokenizer.decode([token_id]) for token_id in top_ids],
    }
    rows.append(row)
    print(
        f"hidden={hidden:10} expected={expected:>2} top={clean_top[0]['token']!r:12} "
        f"correct={str(clean_matches):5} rank={best_rank:7} top12={row['top12']}"
    )

payload = {
    "metadata": {
        "git_describe": subprocess.run(
            ["git", "describe", "--always", "--dirty"], cwd="/workspace/2026/suppressed-activations",
            check=True, text=True, capture_output=True,
        ).stdout.strip(),
        "model": MODEL,
        "layers": [EARLY, PEAK, OUTPUT],
        "score": "rise-and-fall divided by effective LM-head row norm",
        "rule_selection": "layers selected on spider only; all other animals held out",
        "excluded_nonatomic_concepts": ["firefly", "kangaroo"],
    },
    "rows": rows,
}
Path("slop/research/english_animal_target_scan.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
