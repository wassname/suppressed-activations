"""Two-pass Spider→Ant suppressed-coordinate test. Written by PI/gpt-5.4."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import generate, layer_hooks, one_token, replace_output, top_tokens, trajectory
from suppressed_activation_subspace import suppressed_activation_subspace

MODEL = "Qwen/Qwen3.5-4B"
PROMPT = "Fact: The number of legs on the animal that spins webs is "
BLOCKS = tuple(range(22, 30))


def coordinate_swap(h, directions, strength, mask):
    pinv = torch.linalg.pinv(directions)
    coordinates = torch.einsum("bsd,sqd->bsq", h, pinv)
    delta = torch.einsum("bsq,sdq->bsd", coordinates.flip(-1) - coordinates, directions)
    return h + strength * delta * mask[None, :, None]


def hooks(directions, strength, mask):
    def make_hook():
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            if hidden.shape[1] == 1:
                return output
            patched = coordinate_swap(hidden.float(), directions, strength, mask).to(hidden.dtype)
            return replace_output(output, patched)
        return hook
    return {block: make_hook() for block in BLOCKS}


torch.set_grad_enabled(False)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
lm = model.model
ids = tokenizer(PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
residuals, clean_logits = trajectory(model, ids, lm.norm)
bases, selected = suppressed_activation_subspace(
    residuals.permute(1, 0, 2), model.lm_head.weight, 1 + lm.norm.weight,
    early_layer=23, peak_layer=25, output_layer=32, rank=8,
    normalize_unembedding_rows=True,
)
W = model.lm_head.weight.float()
gain = (1 + lm.norm.weight).float()
spider_id, ant_id = one_token(tokenizer, "Spider"), one_token(tokenizer, " Ant")
vectors = torch.stack([(W[spider_id] - W.mean(0)) * gain, (W[ant_id] - W.mean(0)) * gain])
coordinates = torch.einsum("td,sdk->stk", vectors, bases)
projected = torch.einsum("stk,sdk->std", coordinates, bases)
detected = (selected == spider_id).any(-1).float()
all_positions = torch.ones_like(detected)
id6, id8 = one_token(tokenizer, "6"), one_token(tokenizer, "8")
rows = []
for normalized in (False, True):
    token_vectors = projected / projected.norm(dim=-1, keepdim=True) if normalized else projected
    directions = token_vectors.transpose(1, 2)
    for mask_name, mask in (("all", all_positions), ("spider_detected", detected)):
        for strength in (1.0, 2.0):
            hs = hooks(directions, strength, mask)
            with layer_hooks(lm.layers, hs), torch.no_grad():
                logits = model(input_ids=ids, use_cache=False).logits[0, -1].float()
            logp = logits.log_softmax(-1)
            generation = generate(model, tokenizer, ids, lm.layers, hs, max_new_tokens=64)
            rows.append({
                "normalized": normalized, "mask": mask_name, "strength": strength,
                "top": top_tokens(tokenizer, logits, 10),
                "p6": float(logp[id6].exp()), "p8": float(logp[id8].exp()),
                "delta_logp6": float(logp[id6] - clean_logits.log_softmax(-1)[id6]),
                "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
                "generation": generation,
            })
result = {
    "prompt": PROMPT,
    "prompt_tokens": [tokenizer.decode([int(i)]) for i in ids[0]],
    "spider_detected_positions": detected.nonzero().flatten().tolist(),
    "clean": top_tokens(tokenizer, clean_logits, 10),
    "rows": rows,
}
Path("data/spider_ant_demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print("prompt tokens:", result["prompt_tokens"])
print("Spider selected at positions:", result["spider_detected_positions"])
for row in rows:
    print({k: row[k] for k in ("normalized", "mask", "strength", "p6", "p8", "delta_logp6", "log_odds_6_vs_8")}, "top=", row["top"][0]["token"])
    print(row["generation"]["text"])
