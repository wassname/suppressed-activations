"""Fixed-layer J-lens readout and same-pass spider/dog coordinate swap. — PI/OpenAI"""

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
from functools import cache

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


def swap_lens_scores(h, vectors, inverse):
    scores = h.float() @ vectors
    return h.float() + (scores.flip(-1) - scores) @ inverse


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
    means, samples = {}, []
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
        means[concept] = torch.stack(states).mean(0).cpu()
    difference_norm = float((means["dog"] - means["spider"]).norm())
    assert difference_norm > 0
    provenance = {"model": q.MODEL, "model_revision": q.REVISION, "block_index": block, "config": config,
                  "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(), "samples": samples,
                  "difference_norm": difference_norm}
    torch.save({"means": means, "provenance": provenance}, out / "donors.pt")
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


def main(block_index=15, readout_block_index=23, reverse=False, all_prompt_positions=False,
         calibration_json: Path | None = None, forecast_checkpoint: Path | None = None, cases_json: Path | None = None,
         end_pass_readout=False, swap_logits=False, output_mask_max_n=20, plural=False, translation_per_pair=0,
         prepare_donors_json: Path | None = None, donor_checkpoint: Path | None = None):
    torch.set_grad_enabled(False)
    started = time.monotonic()
    out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_jlens-one-pass"
    out.mkdir(parents=True)
    logger.add(out / "stderr.log")
    logger.info("Loading pinned model and reusable lens; no input-specific preparation")
    (out / "runtime.json").write_text(json.dumps({"torch": torch.__version__, "transformers": sys.modules["transformers"].__version__,
                                                "cuda": torch.version.cuda, "python": sys.version}, indent=1))
    (out / "source.py").write_bytes(Path(__file__).read_bytes())
    tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16,
                                                local_files_only=True).cuda().eval()
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

    def readout(h, use_j=True):
        transported = h.float() @ J.T if use_j else h.float()
        return model.lm_head(model.model.norm(transported.to(W.dtype))).float()

    def top_words(h, mask):
        z = readout(h).masked_fill(mask, -torch.inf)
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
    readouts = []
    for case, concept, answer in zip(cases, concepts, answers, strict=True):
        ids = tok(case["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        h = res[read_block + 1]
        if "said_text" not in case:
            generated = model.generate(ids, max_new_tokens=8, do_sample=False)
            case["said_text"] = tok.decode(generated[0, ids.shape[1]:])
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
        if end_pass_readout:
            final_logits = model.lm_head(model.model.norm(res[32][-1])).float()
            output_mask = s4.output_word_mask(final_logits, vocab_norm, word_index, max_n=output_mask_max_n)
            for name, z in (("J-lens", scores["J-lens"]), ("plain24", scores["plain lens"]),
                            ("plain27", readout(res[27][-1], False))):
                scores["end-pass " + name] = z.masked_fill(output_mask, -torch.inf)
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
            top = [t for t in z.topk(32).indices.tolist() if torch.isfinite(z[t])]
            selected = set(top)
            auc = None
            if actual_evaluable and not hidden_is_said:
                positives, negatives = z[actual_hidden_ids, None], z[actual_said_ids][None, :]
                auc = float(((positives > negatives).float() + 0.5 * (positives == negatives).float()).mean())
            checked_auc = None
            if checked_evaluable and not hidden_is_said:
                positives, negatives = z[checked_hidden, None], z[checked_said][None, :]
                checked_auc = float(((positives > negatives).float() + 0.5 * (positives == negatives).float()).mean())
            readouts.append({"method": name, "prompt": case["prompt"], "concept": concept,
                             "alias_checked_pass": checked_evaluable and not hidden_is_said and bool(selected.intersection(checked_hidden)) and not selected.intersection(set(checked_said) | input_label_ids),
                             "alias_checked_auroc": checked_auc, "alias_checked_evaluable": checked_evaluable,
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
        logger.info(f"Readout {concept}: baseline={case['said_text']!r}; ambiguous scoring tokens={[vocab[t] for t in ambiguous_intended]}; canonical_evaluable={canonical_evaluable}; unscorable_actual_words={unscorable_actual_words}")
    if forecasting or end_pass_readout:
        description = ("End-of-pass readout: intermediate J-lens or plain lens, with identical prompt and final-layer output-word masks. "
                       f"Use script04's word mask with top_p=0.9, max_n={output_mask_max_n} (default20;1 retains only the greedy next token). Readout finishes at residual32; this information cannot guide an earlier edit. No forecast is fitted or used. "
                       if end_pass_readout else
                       "Fit32 generic WikiText records, validate4; no task/language labels. Fit RMS-normalised source/final residual pairs by ridge regression toward the identity map (ridge=0.01*mean Gram diagonal), with an intercept. "
                       "Current-input readout receives residual24 only. Score=max(p_J-p_forecast,0), excluding zero scores; compare J-minus-plain to isolate the fitted forecast's contribution. ")
        table = tabulate([[r["concept"], r["method"], r["actual_pass"], r["token_pair_auroc"], r["r_hidden"], r["r_said"], r["pass"], r["alias_pass"]] for r in readouts],
                         headers=["concept", "method", "actual pass", "token-pair AUROC", "hidden rank", "intended answer rank", "literal pass", "alias pass"], tablefmt="pipe")
        md = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nreadout_block_index: {read_block}\n"
              f"calibration_json: {calibration_json}\nforecast_checkpoint: {forecast_checkpoint}\ncases_json: {cases_json}\ntranslation_per_pair: {translation_per_pair}\nend_pass_readout: {str(end_pass_readout).lower()}\noutput_mask_max_n: {output_mask_max_n}\nk: 32\nelapsed_seconds: {time.monotonic()-started:.2f}\n---\n"
              "# Hidden-word readout comparison\n\nWritten by PI/OpenAI.\n\n"
              f"{description}"
              f"Same layer, final position, k32 and prompt mask as before. Selection: {selection} "
              "When forecast_checkpoint is set, all fitting/validation occurred in that checkpoint's prior run; no fitting occurs on these inputs. "
              "Pass now uses actual top32 membership, not optimistic tied ranks. Explicit noun plurals and English number words affect alias scoring only; "
              "this is not exhaustive semantic alias scoring. Actual pass uses lexical words from the entire saved eight-token continuation, ignoring punctuation; generation is scoring only. "
              "Shared prefixes such as Bra for Brazil/Brasília are removed from both scoring classes, not from the readout. A hidden alias actually said in the continuation forces failure. "
              "The primary alias-checked metric also excludes every predeclared answer alias when an expected answer is observed (e.g. Lisboa after Lisbon, six after6). This is still not exhaustive semantic exclusion. Literal-only scores remain in JSON for comparison. "
              "A word without any eligible vocabulary prefix is explicitly unscorable. Such actual-output rows cannot earn a joint pass or AUROC; they remain in the full denominator, so the joint count is a conservative count of verified passes. "
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
        return
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
        projected_delta = full_delta @ inverse_j.T @ vectors_j.T
        assert full_delta.norm() > 0
        noise = torch.randn(full_delta.shape, device="cuda", generator=torch.Generator(device="cuda").manual_seed(0))
        donor_deltas = {"J-projected donor contrast": projected_delta, "full donor contrast": full_delta,
                        "norm-matched full donor contrast": full_delta * (projected_delta.norm() / full_delta.norm()),
                        "matched-random delta": noise * (projected_delta.norm() / noise.norm())}
        donor_info = {"checkpoint": str(donor_checkpoint), "sha256": hashlib.sha256(donor_checkpoint.read_bytes()).hexdigest(),
                      "provenance": donor["provenance"], "delta_norms": {k: float(v.norm()) for k, v in donor_deltas.items()}}
        (out / "donor_provenance.json").write_text(json.dumps(donor_info, indent=1))
        logger.info(f"Offline donor delta norms: {donor_info['delta_norms']}")
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
    modes = ("Base", *donor_deltas) if donor_checkpoint is not None else ("Base", "J-lens swap", "plain-lens swap", "matched-random delta")
    for mode in modes:
        calls, readings = [], []
        rng = torch.Generator(device="cuda").manual_seed(0)

        def hook(_module, _args, output):
            h = output[0] if isinstance(output, tuple) else output
            start = prompt_start if not calls else 0
            selected = h[:, start:].float()
            if mode == "Base":
                edited = selected
            elif donor_checkpoint is not None:
                edited = selected + donor_deltas[mode]
            elif mode == "plain-lens swap":
                edited = swap(selected, vectors_plain, inverse_plain)
            else:
                edited = swap(selected, vectors_j, inverse_j)
                if mode == "matched-random delta":
                    noise = torch.randn(selected.shape, device="cuda", generator=rng)
                    edited = selected + noise / noise.norm(dim=-1, keepdim=True) * (edited - selected).norm(dim=-1, keepdim=True)
            changed = h.clone()
            changed[:, start:] = edited.to(h.dtype)
            calls.append({"positions": selected.shape[1], "sequence_length": h.shape[1],
                          "relative_delta_norm": float((edited - selected).norm() / selected.norm()),
                          "applied_relative_delta_norm": float((changed[:, start:].float() - selected).norm() / selected.norm()),
                          "raw_J_pair_before": (selected[0, -1] @ raw_vectors_j).tolist(),
                          "raw_J_pair_after": (changed[0, -1].float() @ raw_vectors_j).tolist()})
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
                          headers=["concept", "readout", "hidden rank", "answer rank", "joint pass"], tablefmt="pipe") if readouts else "No standalone readout benchmark in this intervention run."
    edit_description = ("Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. "
                        "J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. "
                        "Random uses one fixed seed0 direction at the same absolute norm as the projection, reused at every edited position. "
                        "Only the saved generic donor checkpoint is used; no preliminary pass on the current input. "
                        if donor_checkpoint is not None else
                        f"Intervention: {'raw lens-numerator swap through the dual basis' if swap_logits else 'unit-direction coordinate swap'}. "
                        "No source/donor activation extraction. Coordinate equation: h + V(swap(pinv(V)h) - pinv(V)h). "
                        "Raw-score variant: h + pinv(V).T(swap(V.T h) - V.T h), swapping unnormalised lens numerators rather than guaranteed semantic features. ")
    md = (f"---\nmodel: {q.MODEL}@{q.REVISION}\nlens_revision: {LENS_REVISION}\nlens_sha256: {LENS_SHA}\n"
          f"block_index: {block}\nresidual_index: {block + 1}\nreadout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nswap_logits: {str(swap_logits).lower()}\nplural: {str(plural).lower()}\nprompt_slice: '{prompt_start}:'\nk: 32\nseed: 0\ndonor_checkpoint: {donor_checkpoint}\nelapsed_seconds: {time.monotonic()-started:.2f}\n---\n"
          "# Same-pass intervention pilot\n\nWritten by PI/OpenAI.\n\n"
          f"Reference: {REFERENCE}. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.\n\n"
          f"Rule: edit block {block}, observe block {read_block}, last-position readout, prompt-word removal only; no final-layer output mask. "
          "The observer never controls the edit; it returns no activation replacement. "
          f"Expected answer movement is {expected_base} to {expected_target}. Positive swap_log_odds_shift always favours 4 over 8; reverse success has a negative shift. "
          "J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. "
          f"{edit_description} Prompt slice {prompt_start}: plus every decode step. Concept token strings: {concept_tokens!r}.\n\n"
          f"Selection: {selection} Previously chosen spider/dog example. "
          "Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. "
          "Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.\n\n"
          f"SHOULD: intervention changes {expected_base} toward {expected_target} "
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
                       f"readout_block_index: {read_block}\nreverse: {str(reverse).lower()}\nswap_logits: {str(swap_logits).lower()}\nplural: {str(plural).lower()}\nk: 32\nstrength: 1\nprompt_slice: '{prompt_start}:'\ncontinuous: true\nmax_new_tokens: 32\nseed: 0\n"
                       f"donor_checkpoint: {donor_checkpoint}\nexpected_answer: {r['expected_answer']!r}\nn_tokens: {r['n_tokens']}\n"
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
    parser.add_argument("--calibration-json", type=Path, help="Fit a reusable output forecast on generic text, evaluate readouts only.")
    parser.add_argument("--forecast-checkpoint", type=Path, help="Reuse an offline forecast unchanged; evaluate readouts only.")
    parser.add_argument("--cases-json", type=Path, help="Fixed labelled readout probes; labels only score outputs.")
    parser.add_argument("--end-pass-readout", action="store_true", help="Readout only: use final-layer output mask, never for an earlier intervention.")
    parser.add_argument("--swap-logits", action="store_true", help="Intervention variant: exchange raw lens scores via dual directions, not unit-direction coordinates.")
    parser.add_argument("--output-mask-max-n", type=int, default=20, help="End-pass mask candidate count;1 masks only the greedy next token.")
    parser.add_argument("--plural", action="store_true", help="Use spiders/dogs direction tokens instead of spider/dog; prompts stay unchanged.")
    parser.add_argument("--translation-per-pair", type=int, default=0, help="Frozen translation evaluation: first N eligible words per de/fr/ru pair, no output filtering.")
    parser.add_argument("--prepare-donors-json", type=Path, help="Extract reusable generic donor means, save donors.pt and stop; no experimental input.")
    parser.add_argument("--donor-checkpoint", type=Path, help="Compare fixed offline donor contrasts and controls; no standalone readout benchmark.")
    main(**vars(parser.parse_args()))
