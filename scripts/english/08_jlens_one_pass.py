"""Hidden-word readouts and same-pass spider/dog interventions. — PI/OpenAI"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
import time
from pathlib import Path
from functools import cache, partial

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
RELATIONS = {
    "legs": ((SPIDER, DOG), ("8", "4")),
    "skeleton": (("Fact: The skeleton of the animal that spins webs is on the ",
                  "Fact: The skeleton of the animal that barks and is called man's best friend is on the "),
                 ("outside", "inside")),
    "skeleton_body": (("Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the",
                       "Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"),
                      (" outside", " inside")),
}


def swap_coordinates(h, vectors, inverse):
    coordinates = h.float() @ inverse.T
    return h.float() + (coordinates.flip(-1) - coordinates) @ vectors.T


def swap_lens_scores(h, vectors, inverse):
    scores = h.float() @ vectors
    return h.float() + (scores.flip(-1) - scores) @ inverse


def reflect_donor_side(h, center, direction):
    margin = (h.float() - center) @ direction
    return h.float() - 2 * margin.clamp_max(0).unsqueeze(-1) * direction


def positive_token_kl_log_scores(logits, comparison_logits):
    log_p, log_q = logits.log_softmax(-1), comparison_logits.log_softmax(-1)
    difference = log_p - log_q
    eligible = difference > 0
    score = torch.full_like(difference, -torch.inf)
    score[eligible] = log_p[eligible] + difference[eligible].log()
    return score


def nuisance_coordinate(pair_means, old_direction):
    means = pair_means.double()
    assert means.ndim == 2 and means.shape[0] == 8
    assert torch.isfinite(means).all() and torch.isfinite(old_direction).all()
    center = means.mean(0)
    _, singular_values, Vh = torch.linalg.svd(means - center, full_matrices=False)
    tolerance = torch.finfo(torch.float64).eps * max(means.shape)
    assert singular_values[0] > 0 and singular_values[6] > tolerance * singular_values[0]
    basis = Vh[:7]
    direction = old_direction.double()
    retained = direction - (direction @ basis.T) @ basis
    retained_norm = retained.norm()
    assert retained_norm > tolerance and torch.isfinite(retained_norm)
    projected = retained / retained_norm
    return {"center": center.float(), "direction": projected.float(), "nuisance_basis": basis,
            "singular_values": singular_values, "retained_direction_norm": float(retained_norm),
            "rank_tolerance": float(tolerance * singular_values[0]), "norm_tolerance": tolerance,
            "rank": 7, "fit_dtype": "float64"}


def fit_nuisance_from_run(config, out):
    training = ROOT / config["training_run"]
    assert hashlib.sha256((training / "states.pt").read_bytes()).hexdigest() == config["training_states_sha256"]
    assert hashlib.sha256((training / "coordinate.pt").read_bytes()).hexdigest() == config["training_coordinate_sha256"]
    states = torch.load(training / "states.pt", weights_only=True, map_location="cpu")
    old = torch.load(training / "coordinate.pt", weights_only=True, map_location="cpu")
    keys = [f"{style}-{i}" for style in ("explicit", "indirect") for i in range(4)]
    dogs = torch.stack([states[k + "-dog"]["hidden"][-1].double() for k in keys])
    spiders = torch.stack([states[k + "-spider"]["hidden"][-1].double() for k in keys])
    fitted = nuisance_coordinate((dogs + spiders) / 2, old["direction"])
    fitted["provenance"] = {"model": q.MODEL, "model_revision": q.REVISION, "block_index": 15,
                            "source_concept": "dog", "target_concept": "spider", "training_run": str(training),
                            "training_states_sha256": config["training_states_sha256"],
                            "training_coordinate_sha256": config["training_coordinate_sha256"]}
    dm = (dogs.float() - fitted["center"]) @ fitted["direction"]
    sm = (spiders.float() - fitted["center"]) @ fitted["direction"]
    metrics = {"singular_values": fitted["singular_values"].tolist(), "retained_direction_norm": fitted["retained_direction_norm"],
               "rank_tolerance": fitted["rank_tolerance"], "norm_tolerance": fitted["norm_tolerance"], "rank": 7,
               "training_brackets": int(((dm < 0) & (sm > 0)).sum()),
               "max_training_midpoint_margin": float(((dm + sm) / 2).abs().max()),
               "limits": "Training midpoint invariance is constructed; no held-out or causal claim."}
    torch.save(fitted, out / "projection.pt")
    (out / "projection.json").write_text(json.dumps(metrics, indent=1))
    logger.info("## Offline context projection\n\n{}", json.dumps(metrics, indent=1))
    return fitted


def donor_margins(h, embeddings, center, direction, reference_embedding):
    raw = (h.float() - center) @ direction
    corrected = raw + (reference_embedding - embeddings.float()) @ direction
    return raw, corrected



def validate_donor_coordinates(model, tok, config_path, out, projected_coordinate=None):
    started = time.monotonic()
    config = json.loads(config_path.read_text())
    (out / "config.json").write_bytes(config_path.read_bytes())
    logger.info("## Resolved config\n\n```json\n{}\n```", json.dumps(config, indent=2))
    checkpoint_path = ROOT / config["donor_checkpoint"]
    assert hashlib.sha256(checkpoint_path.read_bytes()).hexdigest() == config["donor_sha256"]
    checkpoint = torch.load(checkpoint_path, weights_only=True, map_location="cpu")
    provenance = checkpoint["provenance"]
    assert provenance["block_index"] == config["block_index"] == 15
    assert {s["token_ids"][-1] for s in provenance["samples"]} == {config["reference_token_id"]}
    assert config["n_prefills"] == 16 and config["n_generated_tokens"] == 0
    center = (checkpoint["means"]["dog"] + checkpoint["means"]["spider"]) / 2
    difference = checkpoint["means"]["spider"] - checkpoint["means"]["dog"]
    direction = difference / difference.norm()
    assert torch.isfinite(direction).all()
    assert provenance["model"] == q.MODEL and provenance["model_revision"] == q.REVISION
    assert tok.decode([config["reference_token_id"]]) == config["reference_token_text"]
    embedding_layer = model.get_input_embeddings()
    device = embedding_layer.weight.device
    assert model.config.hidden_size == center.numel()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    reference_embedding = embedding_layer.weight[config["reference_token_id"]].detach().float().cpu()
    runtime_source = Path(sys.modules[type(model.model).__module__].__file__)
    (out / "provenance.json").write_text(json.dumps({
        "donor": provenance, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "helper_sha256": hashlib.sha256((ROOT / "scripts/demo.py").read_bytes()).hexdigest(),
        "runtime_model_source": str(runtime_source), "runtime_model_sha256": hashlib.sha256(runtime_source.read_bytes()).hexdigest(),
        "torch": torch.__version__, "transformers": sys.modules["transformers"].__version__,
        "python": sys.version, "cuda": torch.version.cuda, "use_cache": True, "logits_to_keep": 1,
    }, indent=1))
    torch.save({"center": center, "direction": direction, "reference_embedding": reference_embedding}, out / "coordinate.pt")
    candidate_method = "embedding subtraction" if projected_coordinate is None else "context projection"
    logger.info("## Sixteen prefills\n\nCandidate: {}.\n\nTODO validate: candidate dog<0<spider on all eight pairs. This is not causal success.", candidate_method)
    if projected_coordinate is None:
        logger.info("SHOULD: identical final embeddings preserve paired margin differences; at token1049 raw and corrected margins agree.")
    samples, tensors, pairs = [], {}, []
    for style, referents in config["referents"].items():
        for ending_index, ending in enumerate(config["endings"]):
            pair = {}
            for concept in ("dog", "spider"):
                key = f"{style}-{ending_index}-{concept}"
                prompt = config["prefix"].format(referent=referents[concept]) + ending
                ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
                captures = []

                def capture(_module, _args, output):
                    h = output[0] if isinstance(output, tuple) else output
                    captures.append(h[0].detach().clone())

                with layer_hooks(model.model.layers, {config["block_index"]: capture}):
                    model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=True, logits_to_keep=1)
                assert len(captures) == 1 and captures[0].shape == (ids.shape[1], center.numel())
                h = captures[0].cpu()
                embeddings = embedding_layer(ids)[0].detach().cpu()
                raw, corrected = donor_margins(h, embeddings, center, direction, reference_embedding)
                if projected_coordinate is None:
                    direct = ((h.float() - embeddings.float()) - (center - reference_embedding)) @ direction
                    assert torch.allclose(corrected, direct, atol=2e-5, rtol=2e-5)
                    reference_positions = ids[0].cpu() == config["reference_token_id"]
                    assert torch.equal(raw[reference_positions], corrected[reference_positions])
                else:
                    corrected = (h.float() - projected_coordinate["center"]) @ projected_coordinate["direction"]
                token_ids = ids[0].tolist()
                sample = {"key": key, "style": style, "ending_index": ending_index, "concept": concept,
                          "input": prompt, "input_repr": repr(prompt), "token_ids": token_ids,
                          "tokens": [tok.decode([i]) for i in token_ids], "raw_margins": raw.tolist(),
                          "corrected_margins": corrected.tolist(), "forward_calls": len(captures)}
                samples.append(sample)
                pair[concept] = sample
                tensors[key] = {"hidden": h, "embeddings": embeddings, "token_ids": ids[0].cpu()}
                torch.save(tensors, out / "states.pt")
                with (out / "samples.jsonl").open("a") as stream:
                    stream.write(json.dumps(sample, ensure_ascii=False) + "\n")
                logger.debug("### {}\n\nInput repr:\n```text\n{}\n```\n\nToken IDs: {}\n\nDecoded token pieces: {}\n\nNo generation.", key, repr(prompt), token_ids, repr(sample["tokens"]))
            dog, spider = pair["dog"], pair["spider"]
            assert dog["token_ids"][-1] == spider["token_ids"][-1]
            d0, s0 = dog["raw_margins"][-1], spider["raw_margins"][-1]
            d1, s1 = dog["corrected_margins"][-1], spider["corrected_margins"][-1]
            if projected_coordinate is None:
                assert abs((s0 - d0) - (s1 - d1)) < 2e-5
            pairs.append({"key": f"{style}-{ending_index}", "raw_dog": d0, "raw_spider": s0,
                          "corrected_dog": d1, "corrected_spider": s1, "pair_difference": s0 - d0,
                          "candidate_pair_difference": s1 - d1,
                          "raw_brackets": d0 < 0 < s0, "corrected_brackets": d1 < 0 < s1,
                          "final_token_id": dog["token_ids"][-1]})
    assert len(samples) == config["n_prefills"] and len(pairs) == 8
    results = {"pairs": pairs, "candidate_method": candidate_method,
               "candidate_coordinate": "coordinate.pt" if projected_coordinate is None else "projection.pt",
               "n_prefills": len(samples), "generated_tokens": 0,
               "raw_brackets": sum(p["raw_brackets"] for p in pairs),
               "corrected_brackets": sum(p["corrected_brackets"] for p in pairs),
               "ordered_pairs": sum(p["pair_difference"] > 0 for p in pairs),
               "candidate_ordered_pairs": sum(p["candidate_pair_difference"] > 0 for p in pairs),
               "candidate_passes_prerequisite": all(p["corrected_brackets"] for p in pairs),
               "peak_allocated_gib": torch.cuda.max_memory_allocated(device) / 2**30 if device.type == "cuda" else None,
               "elapsed_seconds": time.monotonic() - started}
    (out / "result.json").write_text(json.dumps(results, indent=1))
    rows = [[f'[{p["key"]}](samples.jsonl)', int(p["corrected_brackets"]), p["corrected_dog"],
             p["corrected_spider"], int(p["raw_brackets"]), p["raw_dog"], p["raw_spider"], p["candidate_pair_difference"]]
            for p in sorted(pairs, key=lambda p: (-p["corrected_brackets"], p["key"]))]
    table = tabulate(rows, headers=["pair", "bracket↑", "dog<0", "spider>0", "raw bracket↑", "raw dog", "raw spider", "gap↑"], tablefmt="pipe", floatfmt=".4f")
    logger.info("## Result\n\nCandidate brackets: {}/8; raw: {}/8; candidate ordered: {}/8. Required:8/8 candidate brackets.\n\n{}\n\nOne corrected candidate and unchanged raw control; earlier positions are diagnostic only.\n\nTime: {:.2f}s; peak allocated VRAM: {}GiB. Raw states/embeddings: states.pt; raw coordinate: coordinate.pt; candidate coordinate: {}; full prompts: samples.jsonl; metrics: result.json.\n\n{}",
                results["corrected_brackets"], results["raw_brackets"], results["candidate_ordered_pairs"], table,
                results["elapsed_seconds"], results["peak_allocated_gib"], results["candidate_coordinate"], (out / "run.md").relative_to(ROOT))
    return results



def generate_readout(model, ids, read_block):
    states, coverage = {}, {b + 1: [] for b in {read_block, 26, 31}}

    def capture(residual_index, _module, _args, output):
        h = output[0] if isinstance(output, tuple) else output
        if not coverage[residual_index]:
            states[residual_index] = h[0].detach().clone()
        coverage[residual_index].append(h.shape[1])

    hooks = {r - 1: partial(capture, r) for r in coverage}
    with layer_hooks(model.model.layers, hooks):
        generated = model.generate(ids, max_new_tokens=8, do_sample=False, use_cache=True)
    tokens = generated[0, ids.shape[1]:].tolist()
    expected = [ids.shape[1]] + [1] * (len(tokens) - 1)
    assert all(lengths == expected for lengths in coverage.values()), coverage
    return states, tokens, coverage


def disjoint_labels(positive, negative):
    shared = set(positive) & set(negative)
    return sorted(set(positive) - shared), sorted(set(negative) - shared), sorted(shared)


def fit_affine(X, Y):
    X_mean, Y_mean = X.mean(0), Y.mean(0)
    Xc, Yc = X - X_mean, Y - Y_mean
    gram = Xc.T @ Xc
    ridge = 0.01 * gram.trace() / X.shape[1]
    eye = torch.eye(X.shape[1], device=X.device)
    transform = eye + torch.linalg.solve(gram + ridge * eye, Xc.T @ (Yc - Xc))
    return transform, Y_mean - X_mean @ transform


def rms(h):
    return h.float() * torch.rsqrt(h.float().square().mean(-1, keepdim=True) + 1e-6)


def fit_forecast(model, tok, block, corpus_path, out):
    corpus = json.loads(corpus_path.read_text())
    assert len(corpus["texts"]) == 36
    assert len(set(corpus["texts"])) == 36
    sources, targets, validation = [], [], []
    logger.info("SHOULD: offline forecast beats plain lens at predicting held-out final-layer argmax tokens")
    for text in corpus["texts"]:
        ids = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=128).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        assert ids.shape[1] > 16
        sources.append(rms(res[block + 1]))
        targets.append(rms(res[32]))
        if len(sources) > 32:
            validation.append((res[block + 1], res[32]))
    X, Y = torch.cat(sources[:32]), torch.cat(targets[:32])
    transform, bias = fit_affine(X, Y)
    Xv, Yv = torch.cat(sources[32:]), torch.cat(targets[32:])
    metrics = {"fit_tokens": len(X), "validation_tokens": len(Xv), "ridge_fraction": 0.01}
    for name, predicted in (("plain", Xv), ("forecast", Xv @ transform + bias)):
        correct, kl_sum, final_correct = 0, 0.0, 0
        for source, target in validation:
            for x, y in zip(source.split(32), target.split(32), strict=True):
                estimate = x if name == "plain" else (rms(x) @ transform + bias).to(x.dtype)
                lp_true = model.lm_head(model.model.norm(y)).float().log_softmax(-1)
                lp_estimate = model.lm_head(model.model.norm(estimate)).float().log_softmax(-1)
                matched = lp_true.argmax(-1) == lp_estimate.argmax(-1)
                correct += int(matched.sum())
                kl_sum += float((lp_true.exp() * (lp_true - lp_estimate)).sum())
            final_correct += int(matched[-1])
        metrics[name + "_argmax_agreement_all_positions"] = correct / len(Xv)
        metrics[name + "_argmax_agreement_final_positions"] = final_correct / len(validation)
        metrics[name + "_kl_nats_per_position"] = kl_sum / len(Xv)
        metrics[name + "_residual_mse"] = float((predicted - Yv).square().mean())
    provenance = {k: v for k, v in corpus.items() if k != "texts"}
    provenance.update(model=q.MODEL, model_revision=q.REVISION, block_index=block,
                      corpus_sha256=hashlib.sha256(corpus_path.read_bytes()).hexdigest(), max_tokens=128, skip_tokens=0)
    torch.save({"transform": transform.cpu(), "bias": bias.cpu(), "provenance": provenance}, out / "forecast.pt")
    (out / "calibration.json").write_text(json.dumps({"provenance": provenance, "metrics": metrics}, indent=1))
    logger.info(f"Offline calibration: {metrics}")
    return transform, bias, metrics


def prepare_donors(model, tok, block, config_path, out):
    config = json.loads(config_path.read_text())
    assert config["block_index"] == block
    assert config["concepts"] == ["spider", "dog"]
    means, samples, sample_states = {}, [], {}
    for concept in config["concepts"]:
        states = []
        for template in config["templates"]:
            prompt = template.format(concept=concept)
            ids = tok(prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
            res, _ = trajectory(model, ids, model.model.norm)
            h = res[block + 1][-1].float()
            states.append(h)
            samples.append({"concept": concept, "input_repr": repr(prompt), "token_ids": ids[0].tolist(),
                            "residual_norm": float(h.norm())})
        stacked = torch.stack(states)
        means[concept] = stacked.mean(0).cpu()
        sample_states[concept] = stacked.cpu()
    difference_norm = float((means["dog"] - means["spider"]).norm())
    assert difference_norm > 0
    provenance = {"model": q.MODEL, "model_revision": q.REVISION, "block_index": block, "config": config,
                  "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(), "samples": samples,
                  "difference_norm": difference_norm}
    torch.save({"means": means, "sample_states": sample_states, "provenance": provenance}, out / "donors.pt")
    (out / "donors.json").write_text(json.dumps(provenance, indent=1))
    report = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nblock_index: {block}\nn_prompts: {len(samples)}\n---\n"
              "# Offline donor calibration\n\nWritten by PI/OpenAI.\n\n"
              "Four fixed generic templates per animal, no leg-count question or answer labels. Raw last-position residual means; no normalisation or fitted strength. No experimental input was run.\n\n"
              f"SHOULD: means differ. Observed difference norm={difference_norm:.6f}. This does not establish useful steering.\n\n"
              + tabulate([[s["concept"], s["input_repr"], s["residual_norm"]] for s in samples], headers=["concept", "input repr", "residual norm"], tablefmt="pipe")
              + f"\n\nCheckpoint: {out / 'donors.pt'}\nrun.md: {out / 'run.md'}\n")
    (out / "run.md").write_text(report)
    print(report)


def translation_cases(per_pair, label_ids):
    tables = {lang: s4.load_lang(lang) for lang in s4.LANGS}
    cases, skipped = [], []
    for src, tgt in s4.PAIRS:
        if tgt == "zh":
            continue
        words = [{"en": en, src: tables[src][en], tgt: tables[tgt][en], "zh": tables["zh"][en]}
                 for en in tables[src] if en in tables[tgt] and en in tables["zh"]]
        rng, retained = random.Random(0), 0
        for i, w in enumerate(words):
            shots = rng.sample([x for j, x in enumerate(words) if j != i], 4)
            if set(label_ids(w["en"])) & (set(label_ids(w[src])) | set(label_ids(w[tgt]))):
                skipped.append({"pair": f"{src}→{tgt}", "word": w["en"], "reason": "overlapping English/input/output prefix labels"})
                continue
            prompt = "".join(f'{s4.NAME[src]}: "{s[src]}" - {s4.NAME[tgt]}: "{s[tgt]}"\n' for s in shots)
            prompt += f'{s4.NAME[src]}: "{w[src]}" - {s4.NAME[tgt]}: "'
            cases.append({"prompt": prompt, "concept": w["en"], "answer": w[tgt], "input_word": w[src],
                          "hidden_aliases": [w["en"], w["zh"]], "hidden_alias_min_chars": [3, 1],
                          "answer_aliases": [w[tgt]], "pair": f"{src}→{tgt}", "split": s4.ROLE.get((src, tgt), "test")})
            retained += 1
            if retained == per_pair:
                break
        assert retained == per_pair, (src, tgt, retained)
    return {"author": "PI/OpenAI", "prefix": "", "cases": cases, "skipped": skipped,
            "reference_revision": q.WENDLER_COMMIT,
            "selection": f"First{per_pair} prefix-label-eligible words per pair in pinned CSV order; four-shot prompts use seed0 and script04 sampling. No output filtering. de→fr is development, five other de/fr/ru pairs are test; de→zh remains historical reference. English/Chinese hidden labels and their prefix lengths affect scoring only. Frozen after English development; no translation retuning. Concepts recur across language pairs, so prompts are not independent concepts."}


def main(block_index=15, readout_block_index=23, reverse=False, prompt_positions=3,
         calibration_json: Path | None = None, forecast_checkpoint: Path | None = None, cases_json: Path | None = None,
         end_pass_readout=False, swap_logits=False, output_mask_max_n=20, plural=False, translation_per_pair=0,
         prepare_donors_json: Path | None = None, donor_checkpoint: Path | None = None,
         equal_donor_norm=False, relation="legs", erase_output=False, answer_alias_audit_json: Path | None = None,
         erase_strength=1.0, decode_scale=1.0, donor_norm: float | None = None,
         replay_readout_run: Path | None = None, donor_reflection=False,
         validate_donor_coordinates_json: Path | None = None, fit_nuisance=False,
         reflection_coordinate_checkpoint: Path | None = None, token_kl=False):
    if token_kl:
        assert end_pass_readout and output_mask_max_n == 1 and readout_block_index == 23
    if fit_nuisance:
        assert validate_donor_coordinates_json is not None
    if reflection_coordinate_checkpoint is not None:
        assert donor_reflection and reverse and block_index == 15 and prompt_positions == 1
    if donor_reflection:
        assert donor_checkpoint is not None and donor_norm is None and not equal_donor_norm and decode_scale == 1.0
    torch.set_grad_enabled(False)
    started = time.monotonic()
    out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_jlens-one-pass"
    out.mkdir(parents=True)
    logger.add(out / "stderr.log")
    if validate_donor_coordinates_json is not None:
        logger.remove()
        logger.add(sys.stdout, level="INFO", format="{message}\n", colorize=False)
        logger.add(out / "run.md", level="DEBUG", format="{message}\n", colorize=False)
        logger.info("---\nblock_index: 15\nn_prefills: 16\nn_generated_tokens: 0\n---\n# Donor coordinate validation\n\n— PI/OpenAI\n\nCommand:\n```text\n{}\n```", " ".join(sys.argv))
    logger.info("Loading pinned model; no input-specific preparation")
    (out / "runtime.json").write_text(json.dumps({"torch": torch.__version__, "transformers": sys.modules["transformers"].__version__,
                                                "cuda": torch.version.cuda, "python": sys.version}, indent=1))
    (out / "source.py").write_bytes(Path(__file__).read_bytes())
    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
    special_ids = set(tok.all_special_ids) | {i for i, token in tok.added_tokens_decoder.items() if token.special}
    (out / "tokenizer_special_ids.json").write_text(json.dumps({"eos_id": tok.eos_token_id,
        "all_special_ids": tok.all_special_ids, "r2_excluded_ids": sorted(special_ids)}, indent=1))
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16,
                                                local_files_only=True).cuda().eval()
    model.generation_config.to_json_file(out / "generation_defaults.json")
    if validate_donor_coordinates_json is not None:
        fitted = fit_nuisance_from_run(json.loads(validate_donor_coordinates_json.read_text()), out) if fit_nuisance else None
        validation = validate_donor_coordinates(model, tok, validate_donor_coordinates_json, out, fitted)
        if fitted is not None:
            fitted["validation"] = {"passed": validation["candidate_passes_prerequisite"], "n_pairs": 8,
                                    "run": str(out), "result_sha256": hashlib.sha256((out / "result.json").read_bytes()).hexdigest(),
                                    "config_sha256": hashlib.sha256(validate_donor_coordinates_json.read_bytes()).hexdigest()}
            torch.save(fitted, out / "projection.pt")
            return out
        return
    if prepare_donors_json is not None:
        prepare_donors(model, tok, block_index, prepare_donors_json, out)
        return
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
    word_index = s4.WordIndex(vocab_norm)

    @cache
    def label_ids(word, min_chars=3):
        return tuple(i for i, t in enumerate(vocab) if q.is_prefix_hit(t, word, min_chars))

    def readout(h, use_j=True, matrix=J):
        transported = h.float() @ matrix.T if use_j else h.float()
        return model.lm_head(model.model.norm(transported.to(W.dtype))).float()

    def top_words(h, mask, matrix=J):
        z = readout(h, matrix=matrix).masked_fill(mask, -torch.inf)
        return [vocab[t] for t in z.topk(32).indices.tolist()]

    assert not (calibration_json is not None and forecast_checkpoint is not None)
    forecasting = calibration_json is not None or forecast_checkpoint is not None
    if calibration_json is not None:
        transform, bias, calibration_metrics = fit_forecast(model, tok, read_block, calibration_json, out)
    if forecast_checkpoint is not None:
        saved = torch.load(forecast_checkpoint, weights_only=True)
        assert saved["provenance"]["model_revision"] == q.REVISION
        assert saved["provenance"]["block_index"] == read_block
        transform, bias = saved["transform"].cuda(), saved["bias"].cuda()
        calibration_metrics = json.loads((forecast_checkpoint.parent / "calibration.json").read_text())["metrics"]

    assert not (cases_json is not None and translation_per_pair)
    uses_dataset = cases_json is not None or translation_per_pair > 0
    if donor_checkpoint is not None:
        assert not (uses_dataset or forecasting or end_pass_readout)
        cases, concepts, answers = [], [], []
        selection = "Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run."
    elif uses_dataset:
        dataset = translation_cases(translation_per_pair, label_ids) if translation_per_pair else json.loads(cases_json.read_text())
        cases = [{**c, "prompt": dataset["prefix"] + c["prompt"]} for c in dataset["cases"]]
        concepts, answers = [c["concept"] for c in cases], [c["answer"] for c in cases]
        selection = dataset["selection"]
        (out / "cases.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=1))
    else:
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
        selection = "Four selected countries and four simple development prompts; currency previously answered100% gold, not euro."
    if answer_alias_audit_json is not None:
        assert cases_json is not None
        annotations = json.loads(answer_alias_audit_json.read_text())
        for concept, aliases in annotations["extra_answer_aliases"].items():
            matches = [c for c in cases if c["concept"] == concept]
            assert len(matches) == 1, concept
            matches[0]["answer_aliases"] = [*matches[0]["answer_aliases"], *aliases]
        (out / "answer_alias_audit.json").write_text(json.dumps(annotations, ensure_ascii=False, indent=1))
        selection += " Posthoc scoring annotations: " + annotations["selection"]
    readouts, erasure_traces, generation_traces, activation_cache = [], [], [], []
    contrast_components, kl_components, kl_masks = [], [], []
    if replay_readout_run is not None:
        assert end_pass_readout and not forecasting and uses_dataset
        replay_states = torch.load(replay_readout_run / "prefill.pt", map_location="cpu", weights_only=True)
        replay_traces = json.loads((replay_readout_run / "generation_traces.json").read_text())
        assert len(replay_states) == len(replay_traces) == len(cases) > 1
        assert [c["prompt"] for c in cases] == [t["prompt"] for t in replay_traces]
        def reject_forward(*_):
            raise AssertionError("Cached readout scoring must not call the transformer")
        model.register_forward_pre_hook(reject_forward)
        model.model.register_forward_pre_hook(reject_forward)
        (out / "replay_source.json").write_text(json.dumps({"run": str(replay_readout_run.resolve()),
            "model_forward_calls": 0, "mismatch_rule": "next case cyclically; retain original masks",
            "sha256": {n: hashlib.sha256((replay_readout_run / n).read_bytes()).hexdigest()
                       for n in ("prefill.pt", "generation_traces.json", "source.py")}}, indent=1))
    assert not erase_output or end_pass_readout
    for case_index, (case, concept, answer) in enumerate(zip(cases, concepts, answers, strict=True)):
        ids = tok(case["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        if replay_readout_run is None:
            res, generated_ids, coverage = generate_readout(model, ids, read_block)
        else:
            res = {layer: state.unsqueeze(0).cuda() for layer, state in replay_states[case_index].items()}
            generated_ids = replay_traces[case_index]["token_ids"]
            coverage = replay_traces[case_index]["coverage"]
        assert set(res) == {read_block + 1, 27, 32}
        h = res[read_block + 1]
        case["said_text"] = tok.decode(generated_ids)
        generation_traces.append({"case_index": case_index, "prompt": case["prompt"], "token_ids": generated_ids,
                                  "tokens": [vocab[t] for t in generated_ids], "coverage": coverage,
                                  "generation_overrides": {"max_new_tokens": 8, "do_sample": False, "use_cache": True}})
        activation_cache.append({r: state[-1].cpu() for r, state in res.items()})
        (out / "generation_traces.json").write_text(json.dumps(generation_traces, ensure_ascii=False, indent=1))
        torch.save(activation_cache, out / "prefill.pt")
        mask = q.prompt_word_mask(case["prompt"], vocab_norm, "cuda")
        hidden, said, ambiguous_intended = disjoint_labels(label_ids(concept), label_ids(answer))
        canonical_evaluable = bool(hidden and said)
        if not uses_dataset:
            hidden_aliases = [concept, concept + "s"] if concept in ("dog", "bird") else [concept]
            answer_aliases = [answer, {"2": "two", "4": "four"}[answer]] if answer in ("2", "4") else [answer]
        else:
            hidden_aliases, answer_aliases = case["hidden_aliases"], case["answer_aliases"]
        hidden_rules = zip(hidden_aliases, case["hidden_alias_min_chars"], strict=True) if "hidden_alias_min_chars" in case else [(a, 3) for a in hidden_aliases]
        hidden_alias_ids = sorted({t for a, minimum in hidden_rules for t in label_ids(a, minimum)})
        input_label_ids = set(label_ids(case["input_word"])) if "input_word" in case else set()
        said_alias_ids = sorted({t for a in answer_aliases for t in label_ids(a)})
        actual_words = sorted(set(re.findall(r"[^\W_]+", case["said_text"].lower())))
        unscorable_actual_words = [a for a in actual_words if not label_ids(a)]
        actual_said_ids = sorted({t for a in actual_words for t in label_ids(a)})
        actual_hidden_ids, actual_said_ids, ambiguous_actual = disjoint_labels(hidden_alias_ids, actual_said_ids)
        hidden_alias_ids, said_alias_ids, _ = disjoint_labels(hidden_alias_ids, said_alias_ids)
        hidden_is_said = any(a.casefold() in actual_words for a in hidden_aliases)
        actual_evaluable = hidden_is_said or bool(actual_hidden_ids and actual_said_ids and not unscorable_actual_words)
        expected_observed = any(re.search(r"\b" + re.escape(a) + r"\b", case["said_text"], re.IGNORECASE) for a in answer_aliases)
        alias_negatives = set(actual_said_ids) | (set(said_alias_ids) if expected_observed else set())
        checked_hidden, checked_said, _ = disjoint_labels(actual_hidden_ids, alias_negatives)
        checked_evaluable = hidden_is_said or bool(actual_evaluable and checked_hidden and checked_said)
        scores = {"J-lens": readout(h[-1]), "plain lens": readout(h[-1], False)}
        components, kl_names = {}, set()
        if end_pass_readout:
            final_logits = model.lm_head(model.model.norm(res[32][-1])).float()
            output_mask = s4.output_word_mask(final_logits, vocab_norm, word_index, max_n=output_mask_max_n)
            if token_kl:
                kl_masks.append({"case_index": case_index, "prompt_mask_ids": mask.nonzero().flatten().tolist(),
                                 "output_mask_ids": output_mask.nonzero().flatten().tolist()})
            for name, z in (("J-lens", scores["J-lens"]), ("plain24", scores["plain lens"]),
                            ("plain27", readout(res[27][-1], False))):
                scores["end-pass " + name] = z.masked_fill(output_mask, -torch.inf)
                assert z.shape == final_logits.shape and torch.isfinite(z).all() and torch.isfinite(final_logits).all()
                difference = z - final_logits
                log_ratio = z.log_softmax(-1) - final_logits.log_softmax(-1)
                assert torch.allclose(difference - difference[0], log_ratio - log_ratio[0], atol=1e-4, rtol=1e-4)
                contrast_name = "end-pass logit contrast " + name
                scores[contrast_name] = difference.masked_fill(output_mask, -torch.inf)
                components[contrast_name] = (z, final_logits)
                if token_kl:
                    kl_name = "end-pass positive token-KL " + name
                    scores[kl_name] = positive_token_kl_log_scores(z, final_logits).masked_fill(output_mask, -torch.inf)
                    components[kl_name] = (z, final_logits)
                    kl_names.add(kl_name)
                excess = z.softmax(-1) - final_logits.softmax(-1)
                scores["end-pass probability contrast " + name] = excess.masked_fill(output_mask | (excess <= 0), -torch.inf)
                if replay_readout_run is not None:
                    other_h = replay_states[(case_index + 1) % len(cases)][32].cuda()
                    other_logits = model.lm_head(model.model.norm(other_h)).float()
                    mismatch_name = "end-pass mismatched logit contrast " + name
                    scores[mismatch_name] = (z - other_logits).masked_fill(output_mask, -torch.inf)
                    components[mismatch_name] = (z, other_logits)
                    if token_kl:
                        kl_name = "end-pass mismatched positive token-KL " + name
                        scores[kl_name] = positive_token_kl_log_scores(z, other_logits).masked_fill(output_mask, -torch.inf)
                        components[kl_name] = (z, other_logits)
                        kl_names.add(kl_name)
            scores["end-pass negative final control"] = (-final_logits).masked_fill(output_mask, -torch.inf)
            if erase_output:
                output_id = int(final_logits.argmax())
                direction = W[output_id].float()
                for name, state in (("J-lens", h[-1].float() @ J.T), ("plain24", h[-1]), ("plain27", res[27][-1])):
                    normalized = model.model.norm(state.to(W.dtype)).float()
                    removed = (normalized @ direction) / direction.square().sum() * direction
                    for strength in dict.fromkeys((1.0, erase_strength)):
                        erased = normalized - strength * removed
                        expected_score = (1 - strength) * (normalized @ direction)
                        assert abs(float(erased @ direction - expected_score)) < 1e-3 * float(normalized.norm() * direction.norm())
                        z = model.lm_head(erased.to(W.dtype)).float()
                        scores[f"end-pass erased{strength:g} " + name] = z.masked_fill(output_mask, -torch.inf)
                        erasure_traces.append({"concept": concept, "method": name, "strength": strength, "output_token": vocab[output_id],
                                               "relative_removed_norm": float(strength * removed.norm() / normalized.norm()),
                                               "output_score_before": float(normalized @ direction), "output_score_after": float(z[output_id])})
                (out / "erasure_traces.json").write_text(json.dumps(erasure_traces, ensure_ascii=False, indent=1))
        if forecasting:
            forecast_h = rms(h[-1]) @ transform + bias
            scores["forecast"] = model.lm_head(model.model.norm(forecast_h.to(W.dtype))).float()
            scores["final-layer oracle (not deployable)"] = model.lm_head(model.model.norm(res[32][-1])).float()
            for baseline in ("plain lens", "forecast", "final-layer oracle (not deployable)"):
                excess = scores["J-lens"].softmax(-1) - scores[baseline].softmax(-1)
                scores["J minus " + baseline] = excess.masked_fill(excess <= 0, -torch.inf)
        for name, score in scores.items():
            z = score.masked_fill(mask, -torch.inf)
            rh, rs = s4.ranks_of_best(z, hidden), s4.ranks_of_best(z, said)
            hidden_token = hidden[int(z[hidden].argmax())] if hidden else None
            top_ids = z.argsort(descending=True, stable=True)[:32] if name in kl_names else z.topk(32).indices
            top = [t for t in top_ids.tolist() if torch.isfinite(z[t])]
            selected = set(top)
            if name in components:
                intermediate_logits, comparison_logits = components[name]
                contrast_components.append({"case_index": case_index, "method": name, "token_ids": top,
                    "tokens": [vocab[t] for t in top], "intermediate_logits": intermediate_logits[top].tolist(),
                    "comparison_logits": comparison_logits[top].tolist(),
                    "intermediate_log_probs": intermediate_logits.log_softmax(-1)[top].tolist(),
                    "comparison_log_probs": comparison_logits.log_softmax(-1)[top].tolist(),
                    "cutoff_score": float(z[top[-1]]) if top else None,
                    "cutoff_ties": int((z == z[top[-1]]).sum()) if top else 0})
            if name in kl_names:
                lp, lq = intermediate_logits.log_softmax(-1), comparison_logits.log_softmax(-1)
                difference = lp-lq
                signed = (intermediate_logits-comparison_logits).masked_fill(mask | output_mask, -torch.inf)
                excess = lp.exp()-lq.exp()
                excess = excess.masked_fill(mask | output_mask | (excess <= 0), -torch.inf)
                tracked = sorted(selected | set(checked_hidden) | set(checked_said))
                kl_components.append({"case_index": case_index, "method": name, "selected_ids": top,
                    "hidden_label_ids": checked_hidden, "said_label_ids": checked_said,
                    "diagnostic_ranks": "strictly greater score count; ties share rank",
                    "eligible_n": int(torch.isfinite(z).sum()),
                    "cutoff_ties": int((z == z[top[-1]]).sum()) if top else 0,
                    "tokens": [{"id": t, "token": vocab[t], "log_p": float(lp[t]), "log_q": float(lq[t]),
                                "difference": float(difference[t]), "eligible": bool(torch.isfinite(z[t])),
                                "log_score": float(z[t]) if torch.isfinite(z[t]) else None,
                                "signed_contrast_rank": s4.ranks_of_best(signed, [t]),
                                "probability_excess_rank": s4.ranks_of_best(excess, [t])} for t in tracked]})
            auc = None
            if actual_evaluable and not hidden_is_said:
                positives, negatives = z[actual_hidden_ids, None], z[actual_said_ids][None, :]
                auc = float(((positives > negatives).float() + 0.5 * (positives == negatives).float()).mean())
            checked_auc = None
            if checked_evaluable and not hidden_is_said:
                positives, negatives = z[checked_hidden, None], z[checked_said][None, :]
                checked_auc = float(((positives > negatives).float() + 0.5 * (positives == negatives).float()).mean())
            readouts.append({"method": name, "prompt": case["prompt"], "concept": concept, "case_index": case_index,
                             "generation_token_ids": generated_ids,
                             "emitted_word_piece_hits": [vocab[t] for t in top if t in generated_ids and re.search(r"[^\W_]", vocab[t])],
                             "alias_checked_pass": checked_evaluable and not hidden_is_said and bool(selected.intersection(checked_hidden)) and not selected.intersection(set(checked_said) | input_label_ids),
                             "alias_checked_auroc": checked_auc, "alias_checked_evaluable": checked_evaluable,
                             "alias_checked_hidden_found": bool(selected.intersection(checked_hidden)),
                             "alias_checked_said_excluded": not selected.intersection(checked_said),
                             **{key: case[key] for key in ("pair", "split") if key in case},
                             "input_hits": [vocab[t] for t in top if t in input_label_ids],
                             "answer": answer, "r_hidden": rh, "r_said": rs,
                             "pass": bool(selected.intersection(hidden)) and not selected.intersection(said) if canonical_evaluable else None,
                             "canonical_evaluable": canonical_evaluable,
                             "hidden_aliases": hidden_aliases, "answer_aliases": answer_aliases,
                             "alias_pass": bool(selected.intersection(hidden_alias_ids)) and not selected.intersection(said_alias_ids) if hidden_alias_ids and said_alias_ids else None,
                             "actual_words": actual_words, "token_pair_auroc": auc,
                             "intended_answer_observed": expected_observed,
                             "actual_pass": actual_evaluable and not hidden_is_said and bool(selected.intersection(actual_hidden_ids)) and not selected.intersection(set(actual_said_ids) | input_label_ids),
                             "actual_evaluable": actual_evaluable, "unscorable_actual_words": unscorable_actual_words,
                             "hidden_is_said": hidden_is_said,
                             "ambiguous_intended_tokens": [vocab[t] for t in ambiguous_intended],
                             "ambiguous_actual_tokens": [vocab[t] for t in ambiguous_actual],
                             "actual_said_hits": [vocab[t] for t in top if t in actual_said_ids],
                             "best_hidden_token": vocab[hidden_token] if hidden_token is not None else None, "baseline_generation": case["said_text"],
                             "hidden_excluded_variants": [vocab[t] for t in hidden_alias_ids if not torch.isfinite(z[t])],
                             "top32": [vocab[t] for t in top]})
        (out / "readout.json").write_text(json.dumps(readouts, ensure_ascii=False, indent=1))
        (out / "contrast_components.json").write_text(json.dumps(contrast_components, ensure_ascii=False, indent=1))
        if token_kl:
            (out / "token_kl_components.json").write_text(json.dumps(kl_components, ensure_ascii=False, indent=1))
            (out / "token_kl_masks.json").write_text(json.dumps(kl_masks, indent=1))
        logger.info(f"Readout {concept}: baseline={case['said_text']!r}; ambiguous scoring tokens={[vocab[t] for t in ambiguous_intended]}; canonical_evaluable={canonical_evaluable}; unscorable_actual_words={unscorable_actual_words}")
    if forecasting or end_pass_readout:
        description = ("End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. "
                       f"Use script04's word mask with top_p=0.9, max_n={output_mask_max_n} (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. "
                       if end_pass_readout else
                       "Fit32 generic WikiText records, validate4; no task/language labels. Fit RMS-normalised source/final residual pairs by ridge regression toward the identity map (ridge=0.01*mean Gram diagonal), with an intercept. "
                       "Current-input readout receives residual24 only. Score=max(p_J-p_forecast,0), excluding zero scores; compare J-minus-plain to isolate the fitted forecast's contribution. ")
        if end_pass_readout:
            description += "Logit contrast subtracts separately final-normalised vocabulary logits, retaining signed scores; probability contrast retains positive probability differences. Negative-final and cyclic mismatched-final scores are diagnostic controls. No generated text or labels enter these rankings. "
        if token_kl:
            description += ("Positive token-KL contribution: p_R*max(log(p_R)-log(p_F),0), normalized over the full vocabulary before masking. "
                            "Rank positive contributions by log(p_R)+log(log(p_R)-log(p_F)); others are ineligible. Ties use ascending token ID. "
                            "This is not total KL. Same transform/masks apply to J24/plain24/plain27 and cyclic-mismatched-final controls. "
                            "No erasure is combined with this score. Token components, eligibility and masks are saved separately. "
                            "TODO validate: probability weighting reduces rare-denominator dominance, without hiding spoken-word leaks. ")
        if replay_readout_run is not None:
            description += f"Posthoc rescoring of {replay_readout_run}; no transformer forwards or new generations. See replay_source.json for hashes and mismatch ordering. "
        table = tabulate([[r["concept"], r["method"], r["actual_pass"], r["token_pair_auroc"], r["r_hidden"], r["r_said"], r["pass"], r["alias_pass"]] for r in readouts],
                         headers=["concept", "method", "actual pass", "token-pair AUROC", "hidden rank", "intended answer rank", "literal pass", "alias pass"], tablefmt="pipe")
        md = (f"---\ntoken_kl: {str(token_kl).lower()}\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nreadout_block_index: {read_block}\n"
              f"calibration_json: {calibration_json}\nforecast_checkpoint: {forecast_checkpoint}\ncases_json: {cases_json}\ntranslation_per_pair: {translation_per_pair}\nend_pass_readout: {str(end_pass_readout).lower()}\noutput_mask_max_n: {output_mask_max_n}\nerase_output: {str(erase_output).lower()}\nerase_strength: {erase_strength}\nanswer_alias_audit_json: {answer_alias_audit_json}\nk: 32\nelapsed_seconds: {time.monotonic()-started:.2f}\n---\n"
              "# Hidden-word readout comparison\n\nWritten by PI/OpenAI.\n\n"
              f"{description}"
              f"Same layer, final position, k32 and prompt mask as before. Selection: {selection} "
              "When erase_output is true, additional readouts remove the normalised activation's projection onto the greedy output token's unembedding row, then apply the same masks. Full erasure and the requested fractional strength are compared on identical states. No language or concept labels determine that projection; erasure_traces.json records the removed norm and residual target score. This is a new method, not a scorer-only repair. "
              "When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. "
              "Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; "
              "this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. "
              "States and output token IDs are captured during that same generation, with one prefill and cached decode calls, not a separate trajectory pass. generation_traces.json records coverage and token pieces; prefill.pt stores last-position states for later readout analysis only. Historical cached continuations are regenerated with the same eight-token cap. Scoring definitions are unchanged. "
              "Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. "
              "The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. "
              "A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC and remain in the full denominator. These are lexical passes, not a verified lower bound on semantic success. "
              "Token-pair AUROC compares unambiguous hidden and said token variants, with half credit for ties; it is undefined when the hidden concept is said or a class is empty. It is not top32 recovery. "
              "Final-layer oracle is an evaluation-only contrast control, not an admissible same-layer method. Calibration all-position agreement is token-weighted teacher forcing; final-position agreement has four units. Adjacent records may share articles. No interventions in this run.\n\n"
              f"SHOULD: {'end-pass masking improves joint recovery over unmasked readouts; compare J with equally masked plain lenses.' if end_pass_readout else 'forecast beats plain held-out argmax agreement and KL; J-minus-forecast improves joint readout over both J and J-minus-plain. If oracle contrast also fails, forecast error alone cannot explain it.'}\n\n"
              f"Calibration: {calibration_metrics if forecasting else 'not used'}\n\n{table}\n\n")
        for r in readouts:
            md += f"Input: {r['prompt']!r}\n\nBaseline: {r['baseline_generation']!r}\n\n{r['method']}: {r['top32']}\n\n"
        summaries = []
        for name in dict.fromkeys(r["method"] for r in readouts):
            rows = [r for r in readouts if r["method"] == name]
            correct = [r for r in rows if r["intended_answer_observed"]]
            aucs = [r["token_pair_auroc"] for r in rows if r["token_pair_auroc"] is not None]
            checked_aucs = [r["alias_checked_auroc"] for r in rows if r["alias_checked_auroc"] is not None]
            summaries.append({"method": name, "joint_pass": sum(r["actual_pass"] for r in rows), "n": len(rows),
                              "unscored_n": sum(not r["actual_evaluable"] for r in rows),
                              "alias_checked_joint_pass": sum(r["alias_checked_pass"] for r in rows),
                              "alias_checked_mean_auroc": sum(checked_aucs) / len(checked_aucs) if checked_aucs else None,
                              "alias_checked_auroc_n": len(checked_aucs),
                              "alias_checked_correct_joint_pass": sum(r["alias_checked_pass"] for r in correct),
                              "alias_unscored_n": sum(not r["alias_checked_evaluable"] for r in rows),
                              "mean_token_pair_auroc": sum(aucs) / len(aucs) if aucs else None, "auroc_n": len(aucs),
                              "correct_answer_joint_pass": sum(r["actual_pass"] for r in correct), "correct_answer_n": len(correct)})
        (out / "summary.json").write_text(json.dumps(summaries, indent=1))
        groups = []
        if translation_per_pair:
            for split in ("dev", "test"):
                for name in dict.fromkeys(r["method"] for r in readouts):
                    rows = [r for r in readouts if r["split"] == split and r["method"] == name]
                    aucs = [r["alias_checked_auroc"] for r in rows if r["alias_checked_auroc"] is not None]
                    groups.append({"split": split, "method": name, "metric": "alias_checked", "joint_pass": sum(r["alias_checked_pass"] for r in rows),
                                   "n": len(rows), "mean_auroc": sum(aucs) / len(aucs) if aucs else None,
                                   "auroc_n": len(aucs), "unscored_n": sum(not r["alias_checked_evaluable"] for r in rows)})
            (out / "groups.json").write_text(json.dumps(groups, indent=1))
        summary_md = "\n## Fixed-set readout results\n\nPrimary joint pass finds a hidden alias and excludes both actual lexical words and predeclared aliases of an observed expected answer. Literal-only counts are shown separately. Unscored rows remain in the denominator. Expected-answer columns use frozen alias matching, not human accuracy: a valid unlisted synonym can miss. Neither metric proves internal reasoning.\n\n"
        for category in ("current", "end-pass", "oracle"):
            group = sorted([r for r in summaries if ("oracle" if "oracle" in r["method"] else "end-pass" if r["method"].startswith("end-pass") else "current") == category], key=lambda r: r["alias_checked_joint_pass"], reverse=True)
            if not group:
                continue
            summary_md += {"current": "### Current-layer methods\n\n", "end-pass": "### End-of-pass readout (not for earlier edits)\n\n", "oracle": "### Evaluation-only future-information controls\n\n"}[category]
            summary_md += tabulate([[f"[{r['method']}](readout.json)", f"{r['alias_checked_joint_pass']}/{r['n']}", r["alias_checked_mean_auroc"],
                                    f"{r['alias_checked_correct_joint_pass']}/{r['correct_answer_n']}", f"{r['joint_pass']}/{r['n']}", r["alias_unscored_n"]] for r in group],
                                   headers=["method", "alias-checked joint↑", "AUROC↑", "expected-answer joint↑", "literal joint↑", "unscored"], tablefmt="pipe", floatfmt=".3f") + "\n\n"
        if groups:
            summary_md += "### Translation development/test splits\n\n" + tabulate(
                [[r["split"], r["method"], f"{r['joint_pass']}/{r['n']}", r["mean_auroc"], r["unscored_n"]] for r in groups],
                headers=["split", "method", "joint↑", "AUROC↑", "unscored"], tablefmt="pipe", floatfmt=".3f") + "\n\n"
        (out / "run.md").write_text(md + summary_md + f"run.md: {out / 'run.md'}\n")
        print(summary_md, f"run.md: {out / 'run.md'}", sep="\n\n")
        return out
    # Fixed vocabulary directions require no unmodified pass on the current input. — PI/OpenAI
    concept_tokens = (" spiders", " dogs") if plural else (" spider", " dog")
    concept_ids = [tok(s, add_special_tokens=False).input_ids for s in concept_tokens]
    assert all(len(t) == 1 for t in concept_ids), concept_ids
    rows = W[[t[0] for t in concept_ids]].float() * gain
    raw_vectors_j, raw_vectors_plain = (rows @ J_edit).T, rows.T
    logger.info(f"Raw J direction norms {concept_tokens}: {raw_vectors_j.norm(dim=0).tolist()}")
    vectors_j = raw_vectors_j if swap_logits else raw_vectors_j / raw_vectors_j.norm(dim=0)
    vectors_plain = raw_vectors_plain if swap_logits else raw_vectors_plain / raw_vectors_plain.norm(dim=0)
    swap = swap_lens_scores if swap_logits else swap_coordinates
    inverse_j, inverse_plain = torch.linalg.pinv(vectors_j), torch.linalg.pinv(vectors_plain)
    donor_deltas = {}
    if donor_checkpoint is not None:
        donor = torch.load(donor_checkpoint, weights_only=True)
        assert donor["provenance"]["model_revision"] == q.REVISION
        assert donor["provenance"]["block_index"] == block
        full_delta = (donor["means"]["spider"] - donor["means"]["dog"]).cuda()
        full_delta = full_delta if reverse else -full_delta
        native_donor_norm = float(full_delta.norm())
        assert native_donor_norm > 0
        donor_direction = full_delta / full_delta.norm()
        donor_center = ((donor["means"]["spider"] + donor["means"]["dog"]) / 2).cuda()
        if donor_reflection:
            source_name, target_name = ("dog", "spider") if reverse else ("spider", "dog")
            source_margin = (donor["means"][source_name].cuda() - donor_center) @ donor_direction
            target_margin = (donor["means"][target_name].cuda() - donor_center) @ donor_direction
            assert abs(float(source_margin) + native_donor_norm / 2) < 1e-5
            assert abs(float(target_margin) - native_donor_norm / 2) < 1e-5
        raw_donor_center, raw_donor_direction = donor_center, donor_direction
        reflection_mode = "conditional donor reflection"
        if reflection_coordinate_checkpoint is not None:
            fitted = torch.load(reflection_coordinate_checkpoint, weights_only=True, map_location="cpu")
            assert fitted["validation"]["passed"] and fitted["validation"]["n_pairs"] == 8
            assert fitted["provenance"]["model_revision"] == q.REVISION and fitted["provenance"]["block_index"] == block
            assert (fitted["provenance"]["source_concept"], fitted["provenance"]["target_concept"]) == ("dog", "spider")
            donor_center, donor_direction = fitted["center"].cuda(), fitted["direction"].cuda()
            assert abs(float(donor_direction.norm()) - 1) < 1e-6
            reflection_mode = "context-projected donor reflection"
        if donor_norm is not None:
            assert donor_norm > 0
            full_delta = full_delta * (donor_norm / full_delta.norm())
        projected_delta = full_delta @ inverse_j.T @ vectors_j.T
        noise = torch.randn(full_delta.shape, device="cuda", generator=torch.Generator(device="cuda").manual_seed(0))
        donor_deltas = {"J-projected donor contrast": projected_delta, "full donor contrast": full_delta,
                        "norm-matched full donor contrast": full_delta * (projected_delta.norm() / full_delta.norm()),
                        "matched-random delta": noise * (projected_delta.norm() / noise.norm())}
        if equal_donor_norm:
            assert projected_delta.norm() > 0
            donor_deltas = {"norm-matched J donor projection": projected_delta * (full_delta.norm() / projected_delta.norm()),
                            "full donor contrast": full_delta,
                            "matched-random delta": noise * (full_delta.norm() / noise.norm())}
        if donor_reflection:
            donor_deltas = {"full donor contrast": full_delta}
            reflection_noise = noise / noise.norm()
        donor_info = {"checkpoint": str(donor_checkpoint), "conditional_reflection": donor_reflection, "sha256": hashlib.sha256(donor_checkpoint.read_bytes()).hexdigest(),
                      "provenance": donor["provenance"], "native_donor_norm": native_donor_norm, "requested_donor_norm": donor_norm,
                      "delta_norms": {k: float(v.norm()) for k, v in donor_deltas.items()}}
        if reflection_coordinate_checkpoint is not None:
            donor_info["coordinate"] = {"checkpoint": str(reflection_coordinate_checkpoint),
                                        "sha256": hashlib.sha256(reflection_coordinate_checkpoint.read_bytes()).hexdigest(),
                                        "provenance": fitted["provenance"], "validation": fitted["validation"]}
        (out / "donor_provenance.json").write_text(json.dumps(donor_info, indent=1))
        logger.info(f"Offline donor delta norms: {donor_info['delta_norms']}")
    prompt_pair, answer_pair = RELATIONS[relation]
    source_prompt = prompt_pair[1] if reverse else prompt_pair[0]
    mask = q.prompt_word_mask(source_prompt, vocab_norm, "cuda")
    ids = tok(source_prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
    answer_ids = [tok(s, add_special_tokens=False).input_ids for s in answer_pair]
    assert all(len(a) == 1 for a in answer_ids), answer_ids
    a0, a1 = [a[0] for a in answer_ids]
    expected_base, expected_target = answer_pair[::-1] if reverse else answer_pair
    prompt_start = -prompt_positions
    conditions = {}
    modes = ("Base", *donor_deltas) if donor_checkpoint is not None else ("Base", "J-lens swap", "plain-lens swap", "matched-random delta")
    if donor_reflection:
        modes = ("Base", reflection_mode, "full donor contrast", "matched-random reflection control")
        if reflection_coordinate_checkpoint is not None:
            modes = ("Base", "raw donor reflection", reflection_mode, "full donor contrast", "matched-random reflection control")
    for mode in modes:
        if donor_reflection:
            active_center, active_direction = ((raw_donor_center, raw_donor_direction) if mode == "raw donor reflection"
                                               else (donor_center, donor_direction))
        calls, readings = [], []
        rng = torch.Generator(device="cuda").manual_seed(0)

        def hook(_module, _args, output):
            h = output[0] if isinstance(output, tuple) else output
            start = prompt_start if not calls else 0
            selected = h[:, start:].float()
            if mode == "Base":
                edited = selected
            elif donor_reflection and mode in (reflection_mode, "raw donor reflection", "matched-random reflection control"):
                edited = reflect_donor_side(selected, active_center, active_direction)
                if mode == "matched-random reflection control":
                    edited = selected + (edited - selected).norm(dim=-1, keepdim=True) * reflection_noise
            elif donor_checkpoint is not None:
                edited = selected + donor_deltas[mode]
            elif mode == "plain-lens swap":
                edited = swap(selected, vectors_plain, inverse_plain)
            else:
                edited = swap(selected, vectors_j, inverse_j)
                if mode == "matched-random delta":
                    noise = torch.randn(selected.shape, device="cuda", generator=rng)
                    edited = selected + noise / noise.norm(dim=-1, keepdim=True) * (edited - selected).norm(dim=-1, keepdim=True)
            phase_scale = decode_scale if calls else 1.0
            if phase_scale != 1.0:
                edited = selected + phase_scale * (edited - selected)
            changed = h.clone()
            changed[:, start:] = edited.to(h.dtype)
            calls.append({"positions": selected.shape[1], "sequence_length": h.shape[1], "scale": phase_scale,
                          "relative_delta_norm": float((edited - selected).norm() / selected.norm()),
                          "applied_relative_delta_norm": float((changed[:, start:].float() - selected).norm() / selected.norm()),
                          "raw_J_pair_before": (selected[0, -1] @ raw_vectors_j).tolist(),
                          "raw_J_pair_after": (changed[0, -1].float() @ raw_vectors_j).tolist(),
                          "edit_basis_coordinates_before": (selected[0, -1] @ inverse_j.T).tolist(),
                          "edit_basis_coordinates_after": (changed[0, -1].float() @ inverse_j.T).tolist()})
            if donor_reflection:
                margin = (selected - active_center) @ active_direction
                requested_margin = (edited - active_center) @ active_direction
                realized_margin = (changed[:, start:].float() - active_center) @ active_direction
                if mode in (reflection_mode, "raw donor reflection"):
                    assert torch.allclose(requested_margin, margin.abs(), atol=1e-5, rtol=1e-5)
                calls[-1].update(donor_margin_before=margin.flatten().tolist(),
                                 donor_margin_requested=requested_margin.flatten().tolist(),
                                 donor_margin_after=realized_margin.flatten().tolist(),
                                 source_side=(margin < 0).flatten().tolist(),
                                 requested_delta_norm=(edited - selected).norm(dim=-1).flatten().tolist(),
                                 applied_delta_norm=(changed[:, start:].float() - selected).norm(dim=-1).flatten().tolist())
            if len(calls) == 1:
                calls[-1].update(local_jlens_before=top_words(selected[0, -1], mask, J_edit),
                                 local_jlens_after=top_words(changed[0, -1], mask, J_edit))
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
        assert calls[0]["positions"] == ids[:, prompt_start:].shape[1], calls
        assert all(c["positions"] == 1 and c["sequence_length"] == 1 for c in calls[1:]), calls
        lp = generated.scores[0][0].float().log_softmax(-1)
        if mode == "Base":
            base_lp = lp.clone()
        kept = [t for t in tokens if t not in special_ids]
        bigrams = list(zip(kept, kept[1:]))
        top = lp.topk(10).indices.tolist()
        conditions[mode] = {"input_repr": repr(source_prompt), "generation": tok.decode(tokens), "token_ids": tokens,
                            "selected_prompt_token_ids": ids[0, prompt_start:].tolist(),
                            "selected_prompt_tokens": [vocab[t] for t in ids[0, prompt_start:].tolist()],
                            "n_tokens": len(tokens), "prefill_readout": readings[0], "final_decode_readout": readings[-1],
                            "coordinate_kind": ("raw" if mode == "raw donor reflection" or reflection_coordinate_checkpoint is None else "context projection") if donor_reflection else None,
                            "coverage": calls, "top10": [{"token": vocab[t], "log_p": float(lp[t]),
                                                          "p": float(lp[t].exp()), "delta_log_p": float(lp[t] - base_lp[t])} for t in top],
                            "expected_answer": expected_base if mode == "Base" else expected_target if not mode.startswith("matched-random") else "control",
                            "answer_0": answer_pair[0], "answer_1": answer_pair[1],
                            "p_answer0": float(lp[a0].exp()), "p_answer1": float(lp[a1].exp()),
                            "answer_log_odds_shift": float(lp[a1] - lp[a0] - base_lp[a1] + base_lp[a0]),
                            "answer_pair_mass": float(lp[a0].exp() + lp[a1].exp()),
                            "r2": 1 - len(set(bigrams)) / len(bigrams) if bigrams else 0.0}
        if relation == "legs":
            r = conditions[mode]
            r.update(p8=r["p_answer0"], p4=r["p_answer1"], swap_log_odds_shift=r["answer_log_odds_shift"], bare_answer_mass=r["answer_pair_mass"])
        (out / "interventions.json").write_text(json.dumps(conditions, ensure_ascii=False, indent=1))
        logger.info(f"{mode}: {tok.decode(tokens)!r}; p({answer_pair[0]})={conditions[mode]['p_answer0']:.3f}, p({answer_pair[1]})={conditions[mode]['p_answer1']:.3f}")

    if donor_reflection:
        reflected_norm = conditions[reflection_mode]["coverage"][0]["requested_delta_norm"]
        random_norm = conditions["matched-random reflection control"]["coverage"][0]["requested_delta_norm"]
        assert all(abs(a - b) < 1e-5 * (1 + a) for a, b in zip(reflected_norm, random_norm, strict=True))
        target_prompt = prompt_pair[0] if reverse else prompt_pair[1]
        target_ids = tok(target_prompt, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        target_probe = {"input_repr": repr(target_prompt), "expected_answer": expected_target,
                        "role": "Clean target prefill after this experiment's interventions; no generation or feedback to editing"}
        def observe_target_margin(_module, _args, output):
            state = output[0] if isinstance(output, tuple) else output
            target_probe["donor_margin"] = float((state[0, -1].float() - donor_center) @ donor_direction)
        with layer_hooks(model.model.layers, {block: observe_target_margin}):
            target_logits = model(target_ids, attention_mask=torch.ones_like(target_ids), use_cache=True).logits[0, -1].float()
        target_lp = target_logits.log_softmax(-1)
        target_probe.update(top10=[{"token": vocab[t], "log_p": float(target_lp[t])} for t in target_lp.topk(10).indices.tolist()],
                            p_answer0=float(target_lp[a0].exp()), p_answer1=float(target_lp[a1].exp()))
        (out / "clean_target_probe.json").write_text(json.dumps(target_probe, ensure_ascii=False, indent=1))

    table = tabulate([[m, r["answer_log_odds_shift"], r["p_answer1"], r["p_answer0"], r["answer_pair_mass"], r["r2"]]
                      for m, r in conditions.items()], headers=["condition", "answer_log_odds_shift", f"p({answer_pair[1]})", f"p({answer_pair[0]})", "answer_pair_mass", "r2"], tablefmt="pipe")
    read_table = tabulate([[r["concept"], r["method"], r["r_hidden"], r["r_said"], r["pass"]] for r in readouts],
                          headers=["concept", "readout", "hidden rank", "answer rank", "joint pass"], tablefmt="pipe") if readouts else "No standalone readout benchmark in this intervention run."
    edit_description = ("Offline donor contrast: delta=mean(target)-mean(source) in raw residual units. "
                        f"Requested donor norm={donor_norm}; a specified norm rescales this contrast and is not an unscaled component replacement. "
                        "J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. "
                        f"Equal-donor-norm={equal_donor_norm}: when true, compare full contrast, J projection and random at the full contrast's norm. "
                        f"Random uses one fixed seed0 direction at the same absolute norm as the {'full contrast' if equal_donor_norm else 'projection'}, reused at every edited position. "
                        "Only the saved generic donor checkpoint is used; no preliminary pass on the current input. "
                        if donor_checkpoint is not None else
                        f"Intervention: {'raw lens-numerator swap through the dual basis' if swap_logits else 'unit-direction coordinate swap'}. "
                        "No source/donor activation extraction. Coordinate equation: h + V(swap(pinv(V)h) - pinv(V)h). "
                        "Raw-score variant: h + pinv(V).T(swap(V.T h) - V.T h), swapping unnormalised lens numerators rather than guaranteed semantic features. ")
    if donor_reflection:
        edit_description = ("Conditional donor reflection: u=unit(mean(target)-mean(source)), c=(mean(target)+mean(source))/2, "
                            "a=(h-c)@u, h'=h-2*min(a,0)*u. Raw generic means; no dose rescaling or current-input preparation. "
                            "This is a new method, not the reference sparse J-space clamp. Full-strength update is evaluated at every covered call, "
                            "and can be zero on the target side. Natural full-donor addition is not norm matched. Random uses one seed0 direction "
                            "with the proposed reflection norm from its own current state; later gates/doses are not trajectory matched. "
                            "The clean-target diagnostic runs after this experiment's conditions and never controls editing. ")
    if reflection_coordinate_checkpoint is not None:
        edit_description = ("Context-projected reflection: remove the top7 centered generic pair-mean directions from the old donor axis; "
                            "center on the mean of those generic pair means. Fit used the observed2627 generic data, then passed8/8 new generic pairs. "
                            "Training midpoint invariance is constructed, not validation. Apply h'=h-2*min((h-c)@u,0)*u continuously. "
                            "Raw reflection and natural addition are separate controls. Random uses the candidate's proposed norm on its own state; "
                            "later doses are not trajectory matched. No embedding subtraction, current-question preparation, dose or rank adjustment. "
                            f"Coordinate checkpoint: {reflection_coordinate_checkpoint}. ")
    steering_schedule = "prompt-only control" if decode_scale == 0 else "prompt and continuous decode"
    md = (f"---\nreflection_coordinate_checkpoint: {reflection_coordinate_checkpoint}\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nlens_sha256: {LENS_SHA}\nsteering_schedule: {steering_schedule}\n"
          f"block_index: {block}\nresidual_index: {block + 1}\nreadout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nswap_logits: {str(swap_logits).lower()}\nplural: {str(plural).lower()}\nprompt_slice: '{prompt_start}:'\nk: 32\nseed: 0\ndecode_scale: {decode_scale}\ndonor_norm: {donor_norm}\ndonor_checkpoint: {donor_checkpoint}\ndonor_reflection: {str(donor_reflection).lower()}\nequal_donor_norm: {str(equal_donor_norm).lower()}\nrelation: {relation}\nelapsed_seconds: {time.monotonic()-started:.2f}\n---\n"
          "# Same-pass intervention pilot\n\nWritten by PI/OpenAI.\n\n"
          f"Reference: {REFERENCE}. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.\n\n"
          f"Rule: edit block {block}, observe block {read_block}, last-position readout, prompt-word removal only; no final-layer output mask. "
          "The observer never controls the edit; it returns no activation replacement. "
          f"Expected answer movement is {expected_base} to {expected_target}. Positive answer_log_odds_shift favours {answer_pair[1]} over {answer_pair[0]}; reverse success has a negative shift. "
          "For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. "
          "J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. "
          f"{edit_description} Schedule: {steering_schedule}. Prompt slice {prompt_start}:; decode deltas are multiplied by {decode_scale}. Concept token strings: {concept_tokens!r}.\n\n"
          f"Selection: {selection} Previously chosen spider/dog example. "
          "Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.\n\n"
          f"SHOULD: intervention changes {expected_base} toward {expected_target} "
          "with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.\n\n"
          f"{read_table}\n\n{table}\n")
    if donor_reflection:
        md += (f"\nClean source prefill donor margin: {conditions['Base']['coverage'][0]['donor_margin_before']}. "
               f"Clean target margin: {target_probe['donor_margin']:.6f}. Expected source negative, target positive. "
               "[Post-intervention target diagnostic](clean_target_probe.json); no recentering or dose selection.\n")
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
        if donor_reflection:
            source_calls = sum(any(c['source_side']) for c in r['coverage'])
            updated_calls = sum(any(v > 0 for v in c['applied_delta_norm']) for c in r['coverage'])
            requested_sum = sum(sum(c['requested_delta_norm']) for c in r['coverage'])
            applied_sum = sum(sum(c['applied_delta_norm']) for c in r['coverage'])
            section += (f"\nSource-side calls: {source_calls}; calls with nonzero applied updates: {updated_calls}. "
                        f"Sum of requested/applied delta norms: {requested_sum:.6f}/{applied_sum:.6f}. "
                        "Per-call margins and doses are in interventions.json.\n")
        leg_metrics = (f"swap_log_odds_shift: {r['swap_log_odds_shift']}\nbare_answer_mass: {r['bare_answer_mass']}\n" if relation == "legs" else "")
        frontmatter = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nblock_index: {block}\n"
                       f"readout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nswap_logits: {str(swap_logits).lower()}\nplural: {str(plural).lower()}\nk: 32\nstrength: 1\ndecode_scale: {decode_scale}\nprompt_slice: '{prompt_start}:'\ncontinuous: {str(decode_scale != 0).lower()}\nsteering_schedule: {steering_schedule}\nmax_new_tokens: 32\nseed: 0\n"
                       f"donor_checkpoint: {donor_checkpoint}\nreflection_coordinate_checkpoint: {reflection_coordinate_checkpoint}\ndonor_norm: {donor_norm}\ndonor_reflection: {str(donor_reflection).lower()}\nequal_donor_norm: {str(equal_donor_norm).lower()}\nrelation: {relation}\nexpected_answer: {r['expected_answer']!r}\nn_tokens: {r['n_tokens']}\n"
                       f"answer_0: {answer_pair[0]!r}\nanswer_1: {answer_pair[1]!r}\nanswer_log_odds_shift: {r['answer_log_odds_shift']}\nanswer_pair_mass: {r['answer_pair_mass']}\n{leg_metrics}r2: {r['r2']}\n---\n")
        (condition_dir / "run.md").write_text(frontmatter + section + "\nWritten by PI/OpenAI.\n")
        md += f"\n[{mode}]({condition_dir.name}/run.md)\n\n" + section
    (out / "run.md").write_text(md)
    print(read_table, table, f"run.md: {out / 'run.md'}", sep="\n\n")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-index", type=int, default=15, help="Edit block, default midpoint (15).")
    parser.add_argument("--readout-block-index", type=int, default=23, help="Observation block only, default 23.")
    parser.add_argument("--reverse", action="store_true", help="Apply the same symmetric swap to the dog prompt; expected answer 4 to 8.")
    parser.add_argument("--prompt-positions", type=int, default=3, help="Final prompt positions to edit; 0 selects all. Cached decode is always covered.")
    parser.add_argument("--calibration-json", type=Path, help="Fit a reusable output forecast on generic text, evaluate readouts only.")
    parser.add_argument("--forecast-checkpoint", type=Path, help="Reuse an offline forecast unchanged; evaluate readouts only.")
    parser.add_argument("--cases-json", type=Path, help="Fixed labelled readout probes; labels only score outputs.")
    parser.add_argument("--end-pass-readout", action="store_true", help="Readout only: use final-layer output mask, never for an earlier intervention.")
    parser.add_argument("--replay-readout-run", type=Path, help="Rescore saved prefill states/generations without model forwards; include a cyclic mismatched-final control.")
    parser.add_argument("--swap-logits", action="store_true", help="Intervention variant: exchange raw lens scores via dual directions, not unit-direction coordinates.")
    parser.add_argument("--output-mask-max-n", type=int, default=20, help="End-pass mask candidate count;1 masks only the greedy next token.")
    parser.add_argument("--plural", action="store_true", help="Use spiders/dogs direction tokens instead of spider/dog; prompts stay unchanged.")
    parser.add_argument("--translation-per-pair", type=int, default=0, help="Frozen translation evaluation: first N eligible words per de/fr/ru pair, no output filtering.")
    parser.add_argument("--prepare-donors-json", type=Path, help="Extract reusable generic donor means, save donors.pt and stop; no experimental input.")
    parser.add_argument("--validate-donor-coordinates-json", type=Path, help="Validate donor coordinates on frozen generic prefills; no generation or intervention.")
    parser.add_argument("--token-kl", action="store_true", help="Compare positive token-KL contribution ranking with matched plain and cached mismatched-final controls.")
    parser.add_argument("--fit-nuisance", action="store_true", help="Fit the frozen top7 context projection from saved generic states before new-context validation.")
    parser.add_argument("--reflection-coordinate-checkpoint", type=Path, help="Use a validated offline context-projected coordinate for reverse donor reflection.")
    parser.add_argument("--donor-checkpoint", type=Path, help="Compare fixed offline donor contrasts and controls; no standalone readout benchmark.")
    parser.add_argument("--answer-alias-audit-json", type=Path, help="Posthoc answer-alias annotations for scoring only; original cases remain frozen.")
    parser.add_argument("--donor-reflection", action="store_true", help="One-way full-strength fold of the local donor coordinate; raw means, adaptive own-state random control.")
    parser.add_argument("--donor-norm", type=float, help="Rescale donor contrast to this norm before building matched controls; default retains its natural norm.")
    parser.add_argument("--decode-scale", type=float, default=1.0, help="Multiply intervention deltas during cached decode only; prefill remains unchanged.")
    parser.add_argument("--erase-strength", type=float, default=1.0, help="Requested output-erasure fraction, compared with full erasure on the same captured states.")
    parser.add_argument("--erase-output", action="store_true", help="End-pass comparison: remove the activation component along the predicted output-token direction before unembedding.")
    parser.add_argument("--equal-donor-norm", action="store_true", help="Compare full donor, its J projection and a fixed random direction at the full donor norm.")
    parser.add_argument("--relation", choices=tuple(RELATIONS), default="legs", help="Keep the concept pair and donor fixed; test another answer property.")
    main(**vars(parser.parse_args()))
