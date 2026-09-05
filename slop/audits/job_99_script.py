import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.demo import layer_hooks, one_token, replace_output, top_tokens, trajectory

MODEL = "Qwen/Qwen3.5-4B"
PROMPT = "Fact: The number of legs on the animal that spins webs is "
BLOCKS = tuple(range(22, 30))
TARGETS = ("Ant", " Ant", "ant", " ant")


def coordinate_swap(h, directions):
    c = h @ torch.linalg.pinv(directions).T
    return h + (c.flip(-1) - c) @ directions.T


def make_hooks(block_ids, directions, final_position_only):
    def make_hook():
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            if final_position_only:
                patched = coordinate_swap(hidden[:, -1:].float(), directions)
                hidden = torch.cat([hidden[:, :-1], patched.to(hidden.dtype)], dim=1)
            else:
                hidden = coordinate_swap(hidden.float(), directions).to(hidden.dtype)
            return replace_output(output, hidden)
        return hook
    return {block: make_hook() for block in block_ids}


torch.set_grad_enabled(False)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
lm = model.model
ids = tokenizer(PROMPT, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
residuals, clean_logits = trajectory(model, ids, lm.norm)
W = model.lm_head.weight.float()
gain = (1 + lm.norm.weight).float()
spider_id = one_token(tokenizer, "Spider")
id6, id8 = one_token(tokenizer, "6"), one_token(tokenizer, "8")
rows = []
for target in TARGETS:
    ant_id = one_token(tokenizer, target)
    for centered in (False, True):
        base = W - W.mean(0) if centered else W
        vectors = torch.stack([base[spider_id] * gain, base[ant_id] * gain], dim=-1)
        for normalized in (False, True):
            directions = vectors / vectors.norm(dim=0, keepdim=True) if normalized else vectors
            modes = [(f"L{block + 1}", (block,)) for block in BLOCKS] + [("L23-L30", BLOCKS)]
            for layer_name, block_ids in modes:
                for final_only in (True, False):
                    hooks = make_hooks(block_ids, directions, final_only)
                    with layer_hooks(lm.layers, hooks), torch.no_grad():
                        logits = model(input_ids=ids, use_cache=False).logits[0, -1].float()
                    logp = logits.log_softmax(-1)
                    rows.append({
                        "target": target,
                        "centered": centered,
                        "normalized": normalized,
                        "layers": layer_name,
                        "positions": "final" if final_only else "all",
                        "top": top_tokens(tokenizer, logits, 5),
                        "p6": float(logp[id6].exp()),
                        "p8": float(logp[id8].exp()),
                        "log_odds_6_vs_8": float(logp[id6] - logp[id8]),
                    })
rows.sort(key=lambda row: row["log_odds_6_vs_8"], reverse=True)
result = {"prompt": PROMPT, "clean": top_tokens(tokenizer, clean_logits, 10), "rows": rows}
Path("slop/research/spider_ant_grid.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
for row in rows[:20]:
    print({key: row[key] for key in ("target", "centered", "normalized", "layers", "positions", "p6", "p8", "log_odds_6_vs_8")}, "top=", row["top"][0]["token"])
print("n", len(rows), "top6", sum(row["top"][0]["token"].strip() == "6" for row in rows))
