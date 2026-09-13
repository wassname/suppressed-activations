# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "torch>=2.8", "transformers>=5.5"]
# ///
"""Selection-dispatch negative controls for paired_score (maintained): toggling the
option changes the selected IDs AND U; swapping the inputs swaps the score masks;
identical inputs fail informatively. -- PI[glm-5p3-flash]"""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scripts.oat_sweep import increment_union_basis
from scripts.demo import trajectory
from scripts.prompt import assistant_prefill_input_ids

TOK = AutoTokenizer.from_pretrained("wassname/qwen3-5lyr-tiny-random")
MODEL = AutoModelForCausalLM.from_pretrained("wassname/qwen3-5lyr-tiny-random",
                                             dtype=torch.bfloat16).eval()


def samples():
    out = {}
    for name, q in (("source", "spider"), ("dog", "dog")):
        ids = assistant_prefill_input_ids(
            TOK, f"Question: what is the animal that is a {q} called?\nAnswer: ",
            device="cpu", instruction="Answer the question with the answer first.")["input_ids"]
        res, _ = trajectory(MODEL, ids, MODEL.model.norm)
        out[name] = {"residuals": res.float(), "content_end": ids.shape[1]}
    return out


S = dict(readout_positions=2, common_source_rank=4, common_donor_rank=4, persistent_rank=4,
         selection_end_offset=0)


def test_toggle_changes_selection():
    smp = samples()
    cfg0 = SimpleNamespace(**S, paired_score=False)
    cfg1 = SimpleNamespace(**S, paired_score=True)
    sh0, d0 = increment_union_basis(smp["source"], smp["dog"], cfg0, MODEL_UNEMB, MODEL_GAIN)
    sh1, d1 = increment_union_basis(smp["source"], smp["dog"], cfg1, MODEL_UNEMB, MODEL_GAIN)
    assert d0["selected_token_ids"] != d1["selected_token_ids"], \
        "toggling paired_score did not change the selection"
    assert not torch.allclose(sh0, sh1), "toggling paired_score did not change U"
    assert d1["paired_score"] is True and d0["paired_score"] is False
    print("toggle: selected IDs and U change OK")


def test_swap_swaps_masks():
    smp = samples()
    cfg1 = SimpleNamespace(**S, paired_score=True)
    sh_ab, d_ab = increment_union_basis(smp["source"], smp["dog"], cfg1, MODEL_UNEMB, MODEL_GAIN)
    sh_ba, d_ba = increment_union_basis(smp["dog"], smp["source"], cfg1, MODEL_UNEMB, MODEL_GAIN)
    half = len(d_ab["selected_token_ids"]) // 2  # per-side block (2 pos x rank)
    assert d_ab["selected_token_ids"][:half] == d_ba["selected_token_ids"][half:] and \
        d_ab["selected_token_ids"][half:] == d_ba["selected_token_ids"][:half], \
        "swap did not swap the masks"
    print("swap: masks change OK")


def test_identical_inputs_fail():
    smp = samples()
    cfg1 = SimpleNamespace(**S, paired_score=True)
    try:
        increment_union_basis(smp["source"], smp["source"], cfg1, MODEL_UNEMB, MODEL_GAIN)
    except ValueError as e:
        assert "no positive candidates" in str(e)
        print("identical inputs: informative failure OK")
        return
    raise AssertionError("identical inputs did not fail")


MODEL_UNEMB = MODEL.lm_head.weight.float()
MODEL_GAIN = 1.0 + MODEL.model.norm.weight.float()  # the production RMSNorm gain

if __name__ == "__main__":
    test_toggle_changes_selection()
    test_swap_swaps_masks()
    test_identical_inputs_fail()
    print("PAIRED DISPATCH TESTS PASS")
