import json
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import generate, layer_hooks, metrics, one_token, replace_output, top_tokens, trajectory
from suppressed_activation_subspace import component, suppressed_activation_subspace

MODEL = "Qwen/Qwen3.5-4B"
PROMPT = "Fact: The number of legs on the animal that spins webs is "
EARLY, PEAK, OUTPUT = 23, 25, 32
BLOCKS = range(22, 30)
RANK = 8
STRENGTHS = (0.5, 1.0, 2.0)


def unit(x):
    return x / x.norm(dim=-1, keepdim=True)


def coordinate_swap(h, directions, strength):
    coordinates = h @ torch.linalg.pinv(directions).T
    swapped = coordinates.flip(-1)
    return h + strength * ((swapped - coordinates) @ directions.T)


def hooks(blocks, directions, strength, prefill_only=False):
    def make_hook():
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            if prefill_only and hidden.shape[1] == 1:
                return output
            patched = coordinate_swap(hidden.float(), directions, strength).to(hidden.dtype)
            return replace_output(output, patched)
        return hook
    return {block: make_hook() for block in blocks}


torch.set_grad_enabled(False)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
language_model = model.model
input_ids = tokenizer(PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
residuals, clean_logits = trajectory(model, input_ids, language_model.norm)
unembedding = model.lm_head.weight.float()
gain = (1 + language_model.norm.weight).float()
basis, selected = suppressed_activation_subspace(
    residuals[:, -1][None], model.lm_head.weight, 1 + language_model.norm.weight,
    early_layer=EARLY, peak_layer=PEAK, output_layer=OUTPUT, rank=RANK,
    normalize_unembedding_rows=True,
)
basis = basis[0]
spider_id = one_token(tokenizer, "Spider")
ant_id = one_token(tokenizer, "Ant")
effective = (unembedding - unembedding.mean(0)) * gain
direct = unit(torch.stack([effective[spider_id], effective[ant_id]], dim=-1))
projected_rows = component(torch.stack([effective[spider_id], effective[ant_id]]), basis)
projected = unit(projected_rows).T

rows = [{"condition": "base", "top": top_tokens(tokenizer, clean_logits, 10)}]
for name, directions in (("direct", direct), ("projected_inside_S", projected)):
    rows[0][f"{name}_ant_projection_fraction"] = float(projected_rows[1].norm() / effective[ant_id].norm())
    for strength in STRENGTHS:
        with layer_hooks(language_model.layers, hooks(BLOCKS, directions, strength)), torch.no_grad():
            logits = model(input_ids=input_ids, use_cache=False).logits[0, -1].float()
        row = metrics(tokenizer, logits, clean_logits, spider_id, ant_id)
        logp = logits.log_softmax(-1)
        rows.append({
            "condition": f"{name}_C={strength:g}",
            "top": top_tokens(tokenizer, logits, 10),
            "p8": float(logp[one_token(tokenizer, "8")].exp()),
            "p6": float(logp[one_token(tokenizer, "6")].exp()),
            "log_odds_6_vs_8": float(logp[one_token(tokenizer, "6")] - logp[one_token(tokenizer, "8")]),
            "p_spider": row["p_source"],
            "p_ant": row["p_target"],
        })

for name, directions in (("direct", direct), ("projected_inside_S", projected)):
    for strength in (1.0, 2.0):
        result = generate(
            model, tokenizer, input_ids, language_model.layers,
            hooks(BLOCKS, directions, strength, prefill_only=True), max_new_tokens=64,
        )
        rows.append({"condition": f"{name}_C={strength:g}_generation", **result})

result = {
    "metadata": {
        "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"], check=True, text=True, capture_output=True).stdout.strip(),
        "model": MODEL,
        "prompt": PROMPT,
        "layers": [EARLY, PEAK, OUTPUT],
        "intervention_residual_layers": [block + 1 for block in BLOCKS],
        "selected_tokens": [tokenizer.decode([int(i)]) for i in selected[0]],
        "source_token": "Spider",
        "target_token": "Ant",
    },
    "rows": rows,
}
Path("slop/research/spider_ant_coordinate_trial.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print("selected:", result["metadata"]["selected_tokens"])
for row in rows:
    if "log_odds_6_vs_8" in row:
        print(row["condition"], "top=", row["top"][0]["token"], "p6=", f"{row['p6']:.4f}", "p8=", f"{row['p8']:.4f}", "log6/8=", f"{row['log_odds_6_vs_8']:+.3f}")
    elif "text" in row:
        print("\n", row["condition"], "\n", row["text"])
print("ant projection fraction:", float(projected_rows[1].norm() / effective[ant_id].norm()))
