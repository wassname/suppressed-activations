# /// script
# requires-python = ">=3.12"
# dependencies = ["accelerate>=1.10", "torch>=2.8", "transformers>=5.5"]
# ///
"""Causal selector comparison: maximum-agreement pair vs consensus rank-1 patch at L25.

Per prompt (source spider, donors dog/ant), on clean forwards with the existing detector:
select the post-prefix position pair with maximum signed component cosine (deterministic
tie-break), take its rank-1 span direction; comparator is the rank-1 consensus over all
post-prefix positions. Patch equation, identical across selectors:

    h' = h + C * ( (t . u_don) u_don - (h . u_src) u_src )

with u_src/u_don the source's and donor's own unit directions and t the donor residual averaged
over the donor's own selected positions. The edit lies in span{u_src, u_don}, so the orthogonal
source residual is preserved; no component-norm matching; the source input string is unchanged.
Coverage is last-3 prefill positions plus every cached decode step, identical across selectors.
Random controls match each semantic condition's actual per-position/per-step perturbation norms.
Written by PI[claude]; brief: slop/2026-09-10_causal_selector_brief.md.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from torch import Tensor

from suppressed_activation_subspace import component, suppressed_activation_subspace

MODEL = os.environ.get("SUPPRESSED_MODEL", "Qwen/Qwen3.5-4B")
REAL_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
REVISION = os.environ.get("SUPPRESSED_REVISION") or (
    REAL_REVISION if MODEL == "Qwen/Qwen3.5-4B" else None
)
DEVICE = os.environ.get("SUPPRESSED_DEVICE", "cuda")
EARLY_LAYER = int(os.environ.get("SUPPRESSED_EARLY_LAYER", "23"))
PEAK_LAYER = int(os.environ.get("SUPPRESSED_PEAK_LAYER", "25"))
OUTPUT_LAYER = int(os.environ.get("SUPPRESSED_OUTPUT_LAYER", "32"))
INTERVENTION_LAYER = PEAK_LAYER
RANK = int(os.environ.get("SUPPRESSED_RANK", "8"))
PREFIX_END = 10  # positions 0-9 are the shared template prefix in all four prompts
LAST3 = 3
STRENGTHS = (1.0, 2.0)
MAX_NEW_TOKENS = int(os.environ.get("SUPPRESSED_TOKENS", "64"))

PROMPTS = {
    "source": "Fact: The number of legs on the animal that spins webs is ",
    "dog": "Fact: The number of legs on the animal that barks and is called man's best friend is ",
    "ant": "Fact: The number of legs on the animal that lives in colonies and follows pheromone trails is ",
}
SOURCE_OUTPUT = "8"
DONOR_OUTPUTS = {"dog": "4", "ant": "6"}


def one_token(tokenizer, text: str) -> int:
    ids = tokenizer(text, add_special_tokens=False).input_ids
    if len(ids) != 1:
        raise ValueError(f"{text!r} is {len(ids)} tokens: {ids}")
    return ids[0]


def max_agreement_pair(components: Tensor) -> tuple[int, int, float]:
    """Post-prefix pair with maximum signed cosine; ties broken by smaller i then j."""
    norms = components.norm(dim=-1).clamp_min(1e-12)
    unit = components / norms.unsqueeze(-1)
    cos = (unit @ unit.T)
    best = max(((float(cos[i, j]), i, j)
                for i in range(PREFIX_END, components.shape[0])
                for j in range(i + 1, components.shape[0])),
               key=lambda t: (t[0], -t[1], -t[2]))
    return best[1], best[2], best[0]


def rank1_span(components: Tensor) -> Tensor:
    """Unit top singular direction of stacked components [n, hidden], in hidden space.

    For n < hidden the left singular vectors are n-dimensional row-space mixing coefficients;
    the direction that combines the rows lives in Vh[0] ([hidden]).
    """
    _, _, vh = torch.linalg.svd(components.float(), full_matrices=False)
    return vh[0] / vh[0].norm()


def main(output_dir: Path) -> None:
    torch.set_grad_enabled(False)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REVISION, dtype=torch.bfloat16, attn_implementation="sdpa"
    ).to(DEVICE).eval()
    blocks = model.model.layers
    final_norm = model.model.norm
    unembedding = model.lm_head.weight
    norm_gain = 1.0 + final_norm.weight

    from scripts import demo as demo_mod

    ids = {n: tokenizer(p, return_tensors="pt", add_special_tokens=False).input_ids.to(DEVICE)
           for n, p in PROMPTS.items()}
    res = {}
    for name in PROMPTS:
        r, logits = demo_mod.trajectory(model, ids[name], final_norm)
        res[name] = {"residuals": r, "logits": logits,
                     "labels": [tokenizer.decode([int(t)]) for t in ids[name][0]]}
    # Per-position bases over ALL positions; selection runs over ALL post-prefix positions
    # (the brief's domain), e.g. dog's maximum pair (' called'@14, ' '@20) lies outside last-3.
    bases = {}
    comps = {}
    for name in PROMPTS:
        seq_len = res[name]["residuals"].shape[1]
        b, _ = suppressed_activation_subspace(
            res[name]["residuals"].permute(1, 0, 2),
            unembedding, norm_gain, early_layer=EARLY_LAYER, peak_layer=PEAK_LAYER,
            output_layer=OUTPUT_LAYER, rank=RANK, normalize_unembedding_rows=True,
        )
        bases[name] = b  # [seq_len, hidden, rank]
        comps[name] = torch.stack([
            component(res[name]["residuals"][INTERVENTION_LAYER, p].float(), b[p])
            for p in range(seq_len)
        ])  # [seq_len, hidden]

    selections = {}
    post_prefix = {n: list(range(PREFIX_END, res[n]["residuals"].shape[1])) for n in PROMPTS}
    for name in PROMPTS:
        i, j, cos = max_agreement_pair(comps[name])
        assert i >= PREFIX_END and j >= PREFIX_END
        post = post_prefix[name]
        selections[name] = {
            "pair": {"i": int(i), "j": int(j), "cosine": cos,
                     "tokens": [res[name]["labels"][i], res[name]["labels"][j]],
                     "post_prefix_indices": post},
            "pair_direction": rank1_span(comps[name][[post.index(i), post.index(j)]]),
            "consensus_direction": rank1_span(comps[name][post]),
        }
        print(f"{name}: max-agreement pair {selections[name]['pair']}")

    answer_ids = {n: one_token(tokenizer, o) for n, o in
                  (("source", SOURCE_OUTPUT), *DONOR_OUTPUTS.items())}

    # ---- patch machinery: shared-coordinate replacement, no norm matching ----
    def build_patch(u_src: Tensor, u_don: Tensor, donor_target: Tensor, strength: float,
                    record: dict | None, matched_norms: dict | None = None,
                    rand_dir: Tensor | None = None):
        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            active = 1 if hidden.shape[1] == 1 else LAST3
            start = hidden.shape[1] - active
            h = hidden[:, start:].float()
            semantic = (donor_target @ u_don) * u_don - (h @ u_src).unsqueeze(-1) * u_src
            if matched_norms is not None:
                # random control: match this call's actual per-position semantic norms; decode
                # steps match step-by-step (partial beyond the semantic trajectory's length,
                # declared post-hoc, reusing the last step's norm).
                if hidden.shape[1] > 1:
                    # prefill norms are window-relative (LAST3 entries), not absolute indices
                    ref = torch.as_tensor(matched_norms["prefill"][:active],
                                          device=h.device).float()
                else:
                    step = sum(1 for c in (record or {}).get("calls", []) if c["seq_len"] == 1)
                    idx = min(step, len(matched_norms["decode"]) - 1)
                    ref = torch.as_tensor([matched_norms["decode"][idx]], device=h.device).float()
                rand_vec = rand_dir.reshape(1, 1, -1).expand_as(semantic)
                delta = rand_vec * semantic.norm(dim=-1, keepdim=True).clamp_min(1e-12)
                scale = ref.reshape(1, -1, 1) / delta.norm(dim=-1, keepdim=True).clamp_min(1e-12)
                delta = delta * scale
                patched = h + delta  # norm-matched: strength already inside the reference
            else:
                delta = semantic
                patched = h + strength * delta
            if record is not None:
                record.setdefault("calls", []).append({
                    "seq_len": int(hidden.shape[1]), "active": active,
                    "positions": list(range(start, hidden.shape[1])),
                    "perturbation_norm_by_position": (patched - h).norm(dim=-1)[0].tolist(),
                })
            full = torch.cat([hidden[:, :start], patched.to(hidden.dtype),
                              hidden[:, start + active:]], dim=1)
            return (full, *output[1:]) if isinstance(output, tuple) else full
        return {INTERVENTION_LAYER - 1: hook}

    def run(name: str, u_src: Tensor, u_don: Tensor, donor_target: Tensor, strength: float,
            matched_norms: dict | None = None, rand_dir: Tensor | None = None,
            max_new_tokens: int = MAX_NEW_TOKENS):
        record: dict = {}
        hooks = build_patch(u_src, u_don, donor_target, strength, record,
                            matched_norms=matched_norms, rand_dir=rand_dir)
        logits = demo_mod.run_forward(model, ids["source"], blocks, hooks)
        gen = demo_mod.generate(model, tokenizer, ids["source"], blocks, hooks,
                                max_new_tokens=max_new_tokens)
        if strength == 0:
            torch.testing.assert_close(logits, res["source"]["logits"].float(), rtol=0, atol=0)
            record["zero_strength_identity"] = "logits identical to clean source"
        prefill = [c for c in record["calls"] if c["seq_len"] > 1]
        decode = [c for c in record["calls"] if c["seq_len"] == 1]
        assert prefill and prefill[0]["active"] == LAST3
        record["coverage"] = {
            "prefill_positions": prefill[0]["positions"], "decode_calls": len(decode),
            "generated_tokens": len(gen["token_ids"]),
            "ended_at_eos": gen["token_ids"][-1] in (tokenizer.eos_token_id, tokenizer.pad_token_id),
        }
        return {"logits": logits, "generation": gen, "record": record}

    # ---- conditions ----
    results = []
    donor_t = {}
    for donor in ("dog", "ant"):
        L = res[donor]["residuals"]
        pair = selections[donor]["pair"]
        donor_t[donor] = {
            "pair": (L[INTERVENTION_LAYER, pair["i"]] + L[INTERVENTION_LAYER, pair["j"]]).float() / 2,
            "consensus": L[INTERVENTION_LAYER, post_prefix[donor]].float().mean(0),
        }

    for donor in ("dog", "ant"):
        u_don_pair = selections[donor]["pair_direction"]
        u_don_cons = selections[donor]["consensus_direction"]
        u_src_pair = selections["source"]["pair_direction"]
        u_src_cons = selections["source"]["consensus_direction"]
        selectors = {
            "max_agreement_pair": (u_src_pair, u_don_pair, donor_t[donor]["pair"]),
            "consensus": (u_src_cons, u_don_cons, donor_t[donor]["consensus"]),
        }
        for sel_name, (u_src, u_don, t) in selectors.items():
            for strength in (0.0, *STRENGTHS):
                r = run(f"{donor}/{sel_name}/C{strength}", u_src, u_don, t, strength)
                r.update({"donor": donor, "selector": sel_name, "strength": strength})
                results.append(r)
        # matched-random per semantic condition
        for sel_name, (u_src, u_don, t) in selectors.items():
            for strength in STRENGTHS:
                key = f"{donor}/{sel_name}/C{strength}"
                sem = next(r for r in results
                           if r.get("donor") == donor and r.get("selector") == sel_name
                           and r.get("strength") == strength)
                prefill_call = [c for c in sem["record"]["calls"] if c["seq_len"] > 1][0]
                decode_calls = [c for c in sem["record"]["calls"] if c["seq_len"] == 1]
                gen = torch.Generator(device=DEVICE).manual_seed(zlib.crc32(key.encode()))  # deterministic
                rand_dir = torch.linalg.qr(
                    torch.randn(1, u_src.shape[0], device=DEVICE, generator=gen)
                ).Q.squeeze(0)
                r = run(key, u_src, u_don, t, strength,
                        matched_norms={"prefill": prefill_call["perturbation_norm_by_position"],
                                       "decode": [c["perturbation_norm_by_position"][0]
                                                  for c in decode_calls]},
                        rand_dir=rand_dir)
                r.update({"donor": donor, "selector": f"{sel_name}_random", "strength": strength})
                results.append(r)
            # declare coverage mismatch explicitly rather than forcing a match
            sem_last = next(r for r in results if r.get("donor") == donor
                            and r.get("selector") == sel_name and r.get("strength") == STRENGTHS[-1])
            rand_last = next(r for r in results if r.get("donor") == donor
                             and r.get("selector") == f"{sel_name}_random"
                             and r.get("strength") == STRENGTHS[-1])
            if (sem_last["record"]["coverage"]["generated_tokens"]
                    != rand_last["record"]["coverage"]["generated_tokens"]):
                results.append({"note": f"coverage mismatch {donor}/{sel_name}: semantic "
                                 f"{sem_last['record']['coverage']['generated_tokens']} vs random "
                                 f"{rand_last['record']['coverage']['generated_tokens']} tokens; "
                                 "norm matching declared partial beyond the shorter trajectory"})

    # clean references
    clean_source_gen = demo_mod.generate(model, tokenizer, ids["source"], blocks, {},
                                         max_new_tokens=MAX_NEW_TOKENS)
    for donor in ("dog", "ant"):
        clean_donor_gen = demo_mod.generate(model, tokenizer, ids[donor], blocks, {},
                                            max_new_tokens=MAX_NEW_TOKENS)
        results.append({"donor": donor, "selector": "clean_donor",
                        "generation": clean_donor_gen})
    results.append({"selector": "clean_source", "generation": clean_source_gen})

    def summarize(logits):
        logp = logits.log_softmax(-1)
        return {f"p_{a}": float(logp[answer_ids[a]].exp()) for a in answer_ids} | {
            "top_tokens": [{"token_id": int(i), "token": tokenizer.decode([int(i)]),
                            "logp": float(logp[i])} for i in logp.topk(10).indices]}

    out = {
        "metadata": {
            "model": MODEL, "revision": REVISION, "device": DEVICE,
            "detector_layers": [EARLY_LAYER, PEAK_LAYER, OUTPUT_LAYER],
            "intervention_layer": INTERVENTION_LAYER, "rank": RANK,
            "prefix_end": PREFIX_END, "last3": LAST3, "strengths": list(STRENGTHS),
            "max_new_tokens": MAX_NEW_TOKENS,
            "prompts": PROMPTS, "answers": {"source": SOURCE_OUTPUT, **DONOR_OUTPUTS},
            "equation": "h' = h + C*((t.u_don)u_don - (h.u_src)u_src); no norm matching",
            "git_describe": subprocess.run(["git", "describe", "--always", "--dirty"],
                                           check=True, text=True, capture_output=True).stdout.strip(),
        },
        "selections": {n: {k: v for k, v in s.items() if not k.endswith("_direction")}
                         | {"tokens_with_positions": [
                               {"position": int(p), "token": res[n]["labels"][int(p)]}
                               for p in (s["pair"]["i"], s["pair"]["j"])]}
                       for n, s in selections.items()},
        "clean_answers": {n: {f"p_{a}": float(res[n]["logits"].softmax(-1)[answer_ids[a]].exp())
                              for a in answer_ids} for n in PROMPTS},
        "runs": [{"donor": r.get("donor"), "selector": r.get("selector"),
                  "strength": r.get("strength"),
                  "metrics": summarize(r["logits"]) if "logits" in r else None,
                  "generation": r.get("generation"), "coverage": r.get("record", {}).get("coverage"),
                  "zero_strength_identity": r.get("record", {}).get("zero_strength_identity"),
                  "note": r.get("note"),
                  "calls": r.get("record", {}).get("calls")}
                 for r in results],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    for r in out["runs"]:
        if r.get("metrics"):
            g = (r["generation"] or {}).get("text", "").replace("\n", " ")[:100]
            print(f"{str(r['donor']):6s} {r['selector']:22s} C={r['strength']!s:4s} "
                  f"p8={r['metrics']['p_source']:.3f} p4={r['metrics']['p_dog']:.3f} "
                  f"p6={r['metrics']['p_ant']:.3f} | {g}")
        else:
            print(f"clean {r['selector']}: {(r['generation'] or {}).get('text', '')[:80]!r}")
    print(f"\noutput: {output_dir / 'result.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    main(parser.parse_args().output_dir)
