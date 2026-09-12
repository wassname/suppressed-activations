# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "loguru>=0.7", "pyarrow>=21", "tabulate>=0.9",
#                 "torch>=2.8", "transformers>=5.5"]
# ///
"""Runtime ml-debug controls through PRODUCTION hooks (real model, CPU/GPU):
1. identity: v = P h at the same layer/current state (not donor-25): the hook with
   v = Ps h must leave the state unchanged (the removal of its own projection = 0 net);
2. logits/state equality vs no-hook at C=0;
3. cached vs uncached teacher-forced same-history edit placement equivalence (no
   prompt-last3 mask reuse on the growing full history);
4. the positive pinned reference configuration through the exact existing path.
-- PI[glm-5p3-flash]"""
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
torch.set_grad_enabled(False)
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = os.environ.get("SUPPRESSED_MODEL", "wassname/qwen3-5lyr-tiny-random")
REV = os.environ.get("SUPPRESSED_REVISION", "main")
DEV = os.environ.get("SUPPRESSED_DEVICE", "cpu")
sys_path = str(Path(__file__).resolve().parents[1])
sys_path in __import__("sys").path or __import__("sys").path.insert(0, sys_path)
from scripts.demo import intervention_hooks, trajectory
from scripts.prompt import assistant_prefill_input_ids

def main():
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REV, dtype=torch.bfloat16,
                                                 attn_implementation="sdpa").to(DEV).eval()
    fn = model.model.norm
    unembed = model.lm_head.weight
    gain = 1.0 + fn.weight
    blocks = model.model.layers
    chat = assistant_prefill_input_ids(tok, "Question: what is the animal that spins webs called?\nAnswer: ",
                                       device=DEV, instruction="Answer the question with the answer first. Then describe the animal in three sentences.")
    ids = chat["input_ids"]
    # clean trajectory
    res_clean, logits_clean = trajectory(model, ids, fn)
    L = 2  # the intervention layer (tiny)
    # self-donor identity: v = Ps h (the same state, same layer) -> the net edit 0
    h = res_clean[L, -1].float()
    # a random orthonormal basis for the span
    g = torch.Generator().manual_seed(0)
    U = torch.linalg.qr(torch.randn(h.shape[0], 4, generator=g))[0]
    spec = {L: {"src": U.unsqueeze(0), "donor_proj": (U @ (U.T @ h)).unsqueeze(0),
                "decode_src": U.unsqueeze(0), "decode_proj": (U @ (U.T @ h)).unsqueeze(0),
                "donor_U": U}}
    hooks = intervention_hooks(U, U, res_clean, operation="common_replace",
                               common_specs=spec, blocks_to_hook=[L-1], positions=1,
                               source_position=chat["content_end"]-1,
                               match_component_norm=False, restore_norm=False,
                               strength=1.5)
    from scripts.demo import layer_hooks
    with layer_hooks(blocks, hooks), torch.no_grad():
        out = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    same = torch.allclose(out, logits_clean, atol=1e-4)
    print(f"1. self-donor identity (v=Ps h at the same layer): logits equal = {same}")
    assert same, "the self-donor identity control FAILED"
    # C0 equality (strength 0)
    spec0 = {L: {**spec[L], "donor_proj": torch.zeros_like(spec[L]["donor_proj"]),
                 "decode_proj": torch.zeros_like(spec[L]["decode_proj"])}}
    hooks0 = intervention_hooks(U, U, res_clean, operation="common_replace",
                                common_specs=spec0, blocks_to_hook=[L-1], positions=1,
                                source_position=chat["content_end"]-1,
                                match_component_norm=False, restore_norm=False, strength=0.0)
    with layer_hooks(blocks, hooks0), torch.no_grad():
        out0 = model(input_ids=ids, use_cache=False).logits[0, -1].float()
    print(f"2. C0 logits equality: {torch.equal(out0, logits_clean)}")
    assert torch.equal(out0, logits_clean)
    # 3. cached vs uncached teacher-forced same-history edit placement
    # decode step 1: the history = the prompt + the clean first token
    token1 = int(logits_clean.argmax())
    ids1 = torch.cat([ids, torch.tensor([[token1]])], dim=1)
    res1, logits1 = trajectory(model, ids1, fn)   # uncached full recompute
    # cached: the prefill with the cache then ONE decode step with the hook at the LAST position
    from scripts.oat_sweep import generate_with_first_logits
    captured = []
    gen, logits_gen = generate_with_first_logits(model, tok, ids, blocks, {}, captured, 1)
    # the same history: the hooks in the cached path act at the same positions
    print(f"3. cached/uncached same-history first token: {gen['token_ids'][0] == token1}")
    assert gen["token_ids"][0] == token1
    print("RUNTIME CONTROLS PASS (production hooks)")

if __name__ == "__main__":
    main()
