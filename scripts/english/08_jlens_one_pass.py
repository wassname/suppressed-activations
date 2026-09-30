"""Fixed-layer J-lens readout and same-pass spider/dog coordinate swap. — PI/OpenAI"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import torch
from huggingface_hub import hf_hub_download
from loguru import logger
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.demo import layer_hooks, replace_output, trajectory

spec = importlib.util.spec_from_file_location("s4", ROOT / "scripts/english/04_erase_and_language_pairs.py")
s4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s4)
q = s4.q
LENS_REVISION = "16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a"
LENS_FILE = "qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt"
LENS_SHA = "1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e"
REFERENCE = "https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e"
SPIDER = "Fact: The number of legs on the animal that spins webs is "
DOG = "Fact: The number of legs on the animal that barks and is called man's best friend is "


def swap_coordinates(h, vectors, inverse):
    coordinates = h.float() @ inverse.T
    return h.float() + (coordinates.flip(-1) - coordinates) @ vectors.T


def main(block_index=15, readout_block_index=23, reverse=False, all_prompt_positions=False):
    torch.set_grad_enabled(False)
    started = time.monotonic()
    out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_jlens-one-pass"
    out.mkdir(parents=True)
    logger.add(out / "stderr.log")
    logger.info("Loading pinned model and reusable lens; no fitting or input-specific preparation")
    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16,
                                                local_files_only=True).cuda().eval()
    path = hf_hub_download("neuronpedia/jacobian-lens", filename=LENS_FILE, revision=LENS_REVISION,
                           local_files_only=True)
    assert hashlib.file_digest(open(path, "rb"), "sha256").hexdigest() == LENS_SHA
    lens = torch.load(path, map_location="cpu", weights_only=True)
    W = model.lm_head.weight
    assert lens["d_model"] == W.shape[1] and lens["n_prompts"] == 1000
    block, read_block = block_index, readout_block_index
    J_edit = lens["J"][block].float().cuda()
    J = lens["J"][read_block].float().cuda()
    gain = (1 + model.model.norm.weight).float()
    vocab = [tok.convert_tokens_to_string([t]) if t is not None else ""
             for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
    vocab_norm = [t.strip().lower() for t in vocab]

    def readout(h, use_j=True):
        transported = h.float() @ J.T if use_j else h.float()
        return model.lm_head(model.model.norm(transported.to(W.dtype))).float()

    def top_words(h, mask):
        z = readout(h).masked_fill(mask, -torch.inf)
        return [vocab[t] for t in z.topk(32).indices.tolist()]

    prior_path = ROOT / "out/2026-09-29_204246_twohop-english/result.json"
    prior = next(iter(json.loads(prior_path.read_text()).values()))
    cases = [r for r in prior if r["two_hop_correct"]][:4]
    concepts = ["Bulgaria", "Iceland", "Turkey", "Congo"]
    answers = ["Sofia", "Reykjavík", "Erdoğan", "Nguesso"]
    fresh = [
        ("Fact: The capital of the country shaped like a boot is ", "Italy", "Rome"),
        ("Fact: The currency used in the country shaped like a boot is ", "Italy", "euro"),
        ("Fact: The number of legs on the animal that barks is ", "dog", "4"),
        ("Fact: The number of legs on the animal with feathers and a beak is ", "bird", "2"),
    ]
    cases += [{"prompt": p} for p, _, _ in fresh]
    concepts += [c for _, c, _ in fresh]
    answers += [a for _, _, a in fresh]
    readouts = []
    for case, concept, answer in zip(cases, concepts, answers, strict=True):
        ids = tok(case["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        h = res[read_block + 1]
        if "said_text" not in case:
            generated = model.generate(ids, max_new_tokens=8, do_sample=False)
            case["said_text"] = tok.decode(generated[0, ids.shape[1]:])
        mask = q.prompt_word_mask(case["prompt"], vocab_norm, "cuda")
        hidden = [i for i, t in enumerate(vocab) if q.is_prefix_hit(t, concept, 3)]
        said = [i for i, t in enumerate(vocab) if q.is_prefix_hit(t, answer, 3)]
        assert hidden and said and not set(hidden) & set(said)
        for name, use_j in (("J-lens", True), ("plain lens", False)):
            z = readout(h[-1], use_j).masked_fill(mask, -torch.inf)
            rh, rs = s4.ranks_of_best(z, hidden), s4.ranks_of_best(z, said)
            hidden_token = hidden[int(z[hidden].argmax())]
            readouts.append({"method": name, "prompt": case["prompt"], "concept": concept,
                             "answer": answer, "r_hidden": rh, "r_said": rs, "pass": rh < 32 <= rs,
                             "best_hidden_token": vocab[hidden_token], "baseline_generation": case["said_text"],
                             "top32": [vocab[t] for t in z.topk(32).indices.tolist()]})
    (out / "readout.json").write_text(json.dumps(readouts, ensure_ascii=False, indent=1))
    # Fixed vocabulary directions require no unmodified pass on the current input. — PI/OpenAI
    concept_ids = [tok(s, add_special_tokens=False).input_ids for s in (" spider", " dog")]
    assert all(len(t) == 1 for t in concept_ids), concept_ids
    rows = W[[t[0] for t in concept_ids]].float() * gain
    vectors_j = (rows @ J_edit).T
    vectors_plain = rows.T
    vectors_j = vectors_j / vectors_j.norm(dim=0)
    vectors_plain = vectors_plain / vectors_plain.norm(dim=0)
    inverse_j, inverse_plain = torch.linalg.pinv(vectors_j), torch.linalg.pinv(vectors_plain)
    source_prompt = DOG if reverse else SPIDER
    mask = q.prompt_word_mask(source_prompt, vocab_norm, "cuda")
    ids = tok(source_prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    a8, a4 = [tok(s, add_special_tokens=False).input_ids for s in ("8", "4")]
    assert len(a8) == len(a4) == 1
    a8, a4 = a8[0], a4[0]
    a0, a1 = a8, a4
    expected_base, expected_target = ("4", "8") if reverse else ("8", "4")
    prompt_start = 0 if all_prompt_positions else -3
    conditions = {}
    for mode in ("Base", "J-lens swap", "plain-lens swap", "matched-random delta"):
        calls, readings = [], []
        rng = torch.Generator(device="cuda").manual_seed(0)

        def hook(_module, _args, output):
            h = output[0] if isinstance(output, tuple) else output
            start = prompt_start if not calls else 0
            selected = h[:, start:].float()
            if mode == "Base":
                edited = selected
            elif mode == "plain-lens swap":
                edited = swap_coordinates(selected, vectors_plain, inverse_plain)
            else:
                edited = swap_coordinates(selected, vectors_j, inverse_j)
                if mode == "matched-random delta":
                    noise = torch.randn(selected.shape, device="cuda", generator=rng)
                    edited = selected + noise / noise.norm(dim=-1, keepdim=True) * (edited - selected).norm(dim=-1, keepdim=True)
            changed = h.clone()
            changed[:, start:] = edited.to(h.dtype)
            calls.append({"positions": selected.shape[1], "sequence_length": h.shape[1],
                          "relative_delta_norm": float((edited - selected).norm() / selected.norm())})
            if read_block == block:
                readings.append(top_words(changed[0, -1], mask))
            return replace_output(output, changed)

        def observe(_module, _args, output):
            h = output[0] if isinstance(output, tuple) else output
            readings.append(top_words(h[0, -1], mask))

        hooks = {block: hook}
        if read_block != block:
            hooks[read_block] = observe
        with layer_hooks(model.model.layers, hooks):
            generated = model.generate(ids, max_new_tokens=32, do_sample=False, repetition_penalty=1.0,
                                       use_cache=True, return_dict_in_generate=True, output_scores=True)
        tokens = generated.sequences[0, ids.shape[1]:].tolist()
        assert len(calls) == len(tokens) == len(readings), calls
        assert calls[0]["positions"] == (ids.shape[1] if all_prompt_positions else 3), calls
        assert all(c["positions"] == 1 and c["sequence_length"] == 1 for c in calls[1:]), calls
        lp = generated.scores[0][0].float().log_softmax(-1)
        if mode == "Base":
            base_lp = lp.clone()
        kept = [t for t in tokens if t not in tok.all_special_ids]
        bigrams = list(zip(kept, kept[1:]))
        top = lp.topk(10).indices.tolist()
        conditions[mode] = {"input_repr": repr(source_prompt), "generation": tok.decode(tokens), "token_ids": tokens,
                            "n_tokens": len(tokens), "prefill_readout": readings[0], "final_decode_readout": readings[-1],
                            "coverage": calls, "top10": [{"token": vocab[t], "log_p": float(lp[t]),
                                                          "p": float(lp[t].exp()), "delta_log_p": float(lp[t] - base_lp[t])} for t in top],
                            "expected_answer": expected_base if mode == "Base" else expected_target if mode != "matched-random delta" else "control",
                            "p8": float(lp[a8].exp()), "p4": float(lp[a4].exp()),
                            "swap_log_odds_shift": float(lp[a1] - lp[a0] - base_lp[a1] + base_lp[a0]),
                            "bare_answer_mass": float(lp[a0].exp() + lp[a1].exp()),
                            "r2": 1 - len(set(bigrams)) / len(bigrams) if bigrams else 0.0}
        (out / "interventions.json").write_text(json.dumps(conditions, ensure_ascii=False, indent=1))
        logger.info(f"{mode}: {tok.decode(tokens)!r}; p8={conditions[mode]['p8']:.3f}, p4={conditions[mode]['p4']:.3f}")

    table = tabulate([[m, r["swap_log_odds_shift"], r["p4"], r["p8"], r["bare_answer_mass"], r["r2"]]
                      for m, r in conditions.items()], headers=["condition", "swap_log_odds_shift", "p4", "p8", "bare_answer_mass", "r2"], tablefmt="pipe")
    read_table = tabulate([[r["concept"], r["method"], r["r_hidden"], r["r_said"], r["pass"]] for r in readouts],
                          headers=["concept", "readout", "hidden rank", "answer rank", "joint pass"], tablefmt="pipe")
    md = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nlens_sha256: {LENS_SHA}\n"
          f"block_index: {block}\nresidual_index: {block + 1}\nreadout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nprompt_slice: '{prompt_start}:'\nk: 32\nseed: 0\nelapsed_seconds: {time.monotonic()-started:.2f}\n---\n"
          "# Same-pass J-lens pilot\n\nWritten by PI/OpenAI.\n\n"
          f"Reference: {REFERENCE}. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.\n\n"
          f"Rule: edit block {block}, observe block {read_block}, last-position readout, prompt-word removal only; no final-layer output mask. "
          "The observer never controls the edit; it returns no activation replacement. "
          f"Expected answer movement is {expected_base} to {expected_target}. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. "
          "J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. "
          f"Intervention swaps coordinates along unit W*norm_gain*J directions, prompt slice {prompt_start}: plus every decode step. "
          "No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).\n\n"
          "Selection: four previously answer-correct English cases, four fixed new simple English prompts, and the previously chosen spider/dog example. "
          "Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. "
          "This is the second observer layer tested; edit layer/strength remain the successful midpoint configuration. One causal pair is not a generalisation rate.\n\n"
          f"SHOULD: J-lens recovers hidden words better than the same-layer plain lens. The swap should change {expected_base} toward {expected_target} "
          "with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.\n\n"
          f"{read_table}\n\n{table}\n")
    for case in cases:
        md += f"\nReadout input: {case['prompt']!r}\n\nBaseline continuation (up to 8 tokens): {case['said_text']!r}\n"
    for mode, r in conditions.items():
        condition_dir = out / mode.lower().replace(" ", "-")
        condition_dir.mkdir()
        section = f"# {mode}\n\nInput:\n```text\n{r['input_repr']}\n```\n\nPrefill readout: {r['prefill_readout']}\n\n"
        section += f"Generation ({r['n_tokens']} tokens):\n```text\n{r['generation']}\n```\n\n"
        section += tabulate([[x['token'], x['log_p'], x['p'], x['delta_log_p']] for x in r['top10']],
                           headers=['token', 'log p', 'p', 'delta log p'], tablefmt='pipe') + "\n"
        section += f"\nFinal-decode readout: {r['final_decode_readout']}\n\nCoverage: {len(r['coverage'])} calls; prompt slice {prompt_start}:, then one position per decode.\n"
        frontmatter = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nblock_index: {block}\n"
                       f"readout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nk: 32\nstrength: 1\nprompt_slice: '{prompt_start}:'\ncontinuous: true\nmax_new_tokens: 32\nseed: 0\n"
                       f"expected_answer: {r['expected_answer']!r}\nn_tokens: {r['n_tokens']}\n"
                       f"swap_log_odds_shift: {r['swap_log_odds_shift']}\nbare_answer_mass: {r['bare_answer_mass']}\nr2: {r['r2']}\n---\n")
        (condition_dir / "run.md").write_text(frontmatter + section + "\nWritten by PI/OpenAI.\n")
        md += f"\n[{mode}]({condition_dir.name}/run.md)\n\n" + section
    (out / "run.md").write_text(md)
    print(read_table, table, f"run.md: {out / 'run.md'}", sep="\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-index", type=int, default=15, help="Edit block, default midpoint (15).")
    parser.add_argument("--readout-block-index", type=int, default=23, help="Observation block only, default 23.")
    parser.add_argument("--reverse", action="store_true", help="Apply the same symmetric swap to the dog prompt; expected answer 4 to 8.")
    parser.add_argument("--all-prompt-positions", action="store_true", help="Match the reference's all-position intervention; default remains final three.")
    main(**vars(parser.parse_args()))
