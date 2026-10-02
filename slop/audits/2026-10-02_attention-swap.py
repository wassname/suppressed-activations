"""Edit what layer-23 attention delivers: swap the Sweden/Japan coordinates in the attention output at the last prompt
token and every generated token. One pass; the only offline input is the fixed token directions. — PI/OpenAI

    V = [J23^T (g*W[" Sweden"]), J23^T (g*W[" Japan"])]      # J23: block 23 output -> final, as in the readout
    a' = a + V (flip(c) - c),  c = pinv(V) a                    # a = layer-23 attention output at the edited position

Controls: Base, same swap with plain token directions, random direction with the J-swap norm on the condition's own state.
Same three native-chat cases as 2719/2722; Base must reproduce 2722 Base text.
"""
import hashlib
import json
from pathlib import Path
import runpy

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
g = runpy.run_path("scripts/english/08_jlens_one_pass.py")["main"].__globals__
q, native_prompt, coordinate_swap_bases, swap_coordinates = g["q"], g["native_prompt"], g["coordinate_swap_bases"], g["swap_coordinates"]
LAYER = 23
CONFIG = json.loads(Path("data/sweden_japan_joint_chat_v1.json").read_text())
SYSTEM = json.loads(Path(CONFIG["donor_config"]).read_text())["system"]
REFERENCE = json.loads(Path("out/2026-10-01_175940_native-coordinate-joint/pipeline.json").read_text())["case_runs"]
LENS = Path("/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt")
assert hashlib.sha256(LENS.read_bytes()).hexdigest() == g["LENS_SHA"]
J = torch.load(LENS, weights_only=True, map_location="cpu")["J"][LAYER].cuda().float()
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
ids_c = [tok(s, add_special_tokens=False).input_ids for s in (" Sweden", " Japan")]
assert ids_c == [[22466], [6124]]
rows_c = W[[22466, 6124]] * gain
bases = coordinate_swap_bases((rows_c @ J).T, rows_c.T)
noise = torch.randn(W.shape[1], device="cuda", generator=torch.Generator(device="cuda").manual_seed(0))
random_direction = noise / noise.norm()
EOS = sorted({tok.eos_token_id, 248044})


def rms(h):
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def attn_readout(a, mask):
    z = (W @ (gain * rms(a @ J.T))).masked_fill(mask, -torch.inf)
    return [vocab[t] for t in z.topk(8).indices.tolist()]


results = []
for index, case in enumerate(CONFIG["cases"]):
    prompt, _ = native_prompt(tok, SYSTEM, case["user_content"])
    ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    mask = q.prompt_word_mask(prompt, vocab_norm, "cuda")
    reference_base = json.loads((Path(REFERENCE[index]["run"]) / "interventions.json").read_text())["Base"]
    assert REFERENCE[index]["case"] == case
    for mode in ("Base", "J swap", "plain swap", "matched random"):
        calls = []

        def hook(_module, _args, output):
            a = output[0]
            selected = a[:, -1:].float()
            if mode == "Base":
                edited = selected
            else:
                basis = bases["raw plain" if mode == "plain swap" else "raw J"]
                edited = swap_coordinates(selected, basis["vectors"], basis["inverse"])
                if mode == "matched random":
                    edited = selected + (edited - selected).norm(dim=-1, keepdim=True) * random_direction
            changed = a.clone()
            changed[:, -1:] = edited.to(a.dtype)
            inv = bases["raw J"]["inverse"]
            calls.append({"positions": a.shape[1], "coords_before": (selected[0, -1] @ inv.T).tolist(),
                          "coords_after": (changed[0, -1].float() @ inv.T).tolist(),
                          "relative_change": float((changed[:, -1:].float() - selected).norm() / selected.norm())})
            if len(calls) == 1:
                calls[0]["attn_readout_before"] = attn_readout(selected[0, -1], mask)
                calls[0]["attn_readout_after"] = attn_readout(changed[0, -1].float(), mask)
            return (changed,) + tuple(output[1:])

        handle = model.model.layers[LAYER].self_attn.register_forward_hook(hook)
        try:
            out = model.generate(ids, max_new_tokens=32, do_sample=False, repetition_penalty=1.0, use_cache=True,
                                 eos_token_id=EOS, return_dict_in_generate=True, output_scores=True)
        finally:
            handle.remove()
        tokens = out.sequences[0, ids.shape[1]:].tolist()
        assert len(calls) == len(tokens) and calls[0]["positions"] == ids.shape[1] and all(c["positions"] == 1 for c in calls[1:])
        text = tok.decode(tokens)
        if mode == "Base":
            assert tokens == reference_base["token_ids"], (text, reference_base["generation"])
        lp = out.scores[0][0].float().log_softmax(-1)
        results.append({"case": case["name"], "mode": mode, "expected_base": case["base_expected"], "target": case["edited_expected"],
                        "input_repr": repr(prompt), "generation": text, "n_tokens": len(tokens),
                        "top5": [(vocab[t], round(float(lp[t].exp()), 4)) for t in lp.topk(5).indices.tolist()],
                        "first_call": calls[0], "mean_relative_change": sum(c["relative_change"] for c in calls) / len(calls)})
        print(f"{case['name']:18s} {mode:15s} {text!r:40s} change={results[-1]['mean_relative_change']:.3f} "
              f"coords {[round(x, 2) for x in calls[0]['coords_before']]}->{[round(x, 2) for x in calls[0]['coords_after']]}", flush=True)
        print(f"   attn23 readout before {calls[0]['attn_readout_before']}\n   after  {calls[0]['attn_readout_after']}", flush=True)
Path("slop/audits/2026-10-02_attention-swap.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
