"""Dev-only comparisons for Sandy's window method; no test-set selection. — PI/OpenAI"""
import json
import shutil
import subprocess
import time

import torch
from tabulate import tabulate

from unspoken_concepts import ROOT
from unspoken_concepts.metrics import f1


CONFIGS = [
    {"name": "mean window (default)", "k": 8, "normalize_first": False, "readout_window": True},
    {"name": "window 1", "k": 1, "normalize_first": False, "readout_window": True},
    {"name": "window 4", "k": 4, "normalize_first": False, "readout_window": True},
    {"name": "window 16", "k": 16, "normalize_first": False, "readout_window": True},
    {"name": "normalise tokens first", "k": 8, "normalize_first": True, "readout_window": True},
    {"name": "last-token middle", "k": 8, "normalize_first": False, "readout_window": False},
]


def main():
    out = ROOT / "out" / f"{time.strftime('%Y-%m-%d_%H%M%S')}_embedding-window-dev"
    out.mkdir(parents=True)
    for directory in ("src", "scripts/eval"):
        shutil.copytree(ROOT / directory, out / "code" / directory, ignore=shutil.ignore_patterns("__pycache__"))
    (out / "working-tree.diff").write_text(subprocess.check_output(["git", "diff"], cwd=ROOT, text=True))
    config = {"split": "dev ru→ko only", "configs": CONFIGS, "selection": "highest dev F1; ties keep earlier candidate",
              "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
    (out / "config.json").write_text(json.dumps(config, indent=2))
    started = time.monotonic()
    with (out / "run.md").open("w") as log, (out / "rows.jsonl").open("w") as raw:
        def report(text):
            print(text, flush=True)
            log.write(text + "\n")
            log.flush()
        report(f"# Embedding/output window: dev comparison\n\n```json\n{json.dumps(config, indent=2)}\n```\n")
        report("SHOULD: input embeddings equal the model's embedding lookup, not residual layer 16.\n"
               "TODO validate: averaging intermediate positions improves finding persistent concepts without leaking input/output.\n"
               "Six one-at-a-time candidates; no test prompts are evaluated. All exact prompts and readouts: [rows.jsonl](rows.jsonl).\n")
        from unspoken_concepts.benchmark import DEV, judge, prepare, read_vector, translation_prompts
        from unspoken_concepts.model import MODEL, REVISION, model, tok, vocab
        from unspoken_concepts.methods.embedding_window import embedding_window, pooled, window_components
        from unspoken_concepts.methods.minus_ends import minus_window, minus_ends
        from unspoken_concepts.methods.helpers import last
        report(f"## Model\n\n{MODEL} at {REVISION}\n")
        rows, skipped = [], []
        for item in translation_prompts(DEV, "dev"):
            prepared = prepare(item)
            if prepared is None:
                skipped.append(item["word"])
                continue
            s, leak_in, leak_out = prepared
            ids = tok(item["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.to(s["embeddings"].device)
            expected = model.get_input_embeddings()(ids)[0]
            torch.testing.assert_close(s["embeddings"], expected, rtol=0, atol=0)
            evaluated = []
            for cfg in CONFIGS:
                args = (cfg["k"], cfg["normalize_first"], cfg["readout_window"])
                v = embedding_window(s["hs"], s["embeddings"], {}, *args)
                middle, removed = window_components(s["hs"], s["embeddings"], *args)
                scores = read_vector(v, cfg["name"])
                window_ids = ids[0, -cfg["k"]:].tolist()
                row = {"method": cfg["name"], "remaining_fraction": ((middle - removed).norm() / middle.norm()).item(),
                       "effective_k": len(window_ids), "window_token_ids": window_ids,
                       "window_text": tok.decode(window_ids)} | judge(scores, item, leak_in, leak_out)
                evaluated.append(row)
            controls = {
                "layer-16 endpoint, matched mean": embedding_window(s["hs"], s["hs"][0], {}, 8, False, True),
                "layer-16 window adaptation": minus_window(s["hs"], s["embeddings"], {}, 8, "mean"),
                "minus ends, last token": minus_ends(s["hs"], s["embeddings"], {}),
                "mean window, no removal": pooled(s["hs"][1:-1], 8, False).mean(0),
                "mean over layers, last token": last(s["hs"]).mean(0),
            }
            for name, v in controls.items():
                evaluated.append({"method": name} | judge(read_vector(v, name), item, leak_in, leak_out))
            for row in evaluated:
                row.update(split=item["split"], word=item["word"], prompt=item["prompt"],
                           model_next_token=vocab[int(s["logits"].argmax())])
                raw.write(json.dumps(row, ensure_ascii=False) + "\n")
                rows.append(row)
            raw.flush()
            if len(rows) == len(evaluated):
                report(f"## First dev prompt, selected by dataset order\n\n```text\n{item['prompt']!r}\n```\n"
                       f"\nExpected intermediate: {item['word']!r}; model next token: {evaluated[0]['model_next_token']!r}.\n"
                       "\nEmbedding lookup equality: exact.\n")
                report(tabulate([{ "method": r["method"], "top 8": repr(r["top8"]),
                                   "found": r["hidden"], "leaked": r["leaked"]} for r in evaluated],
                                headers="keys", tablefmt="pipe") + "\n")
        assert rows, "no dev prompts survived"
        names = [c["name"] for c in CONFIGS] + list(controls)
        by_name = {name: [r for r in rows if r["method"] == name] for name in names}
        assert all(by_name.values()), "no dev prompts survived"
        selected = max(CONFIGS, key=lambda c: f1(by_name[c["name"]]))
        (out / "selection.json").write_text(json.dumps({"selected": selected, "dev_f1": f1(by_name[selected["name"]]),
                                                       "n": len(by_name[selected["name"]]), "configs_tried": len(CONFIGS)}, indent=2))
        summary = [{"method": name, "F1↑": f1(rs), "TP↑": sum(r["hidden"] for r in rs),
                    "FP↓": sum(r["leaked"] for r in rs), "FN↓": sum(not r["hidden"] for r in rs), "n": len(rs)}
                   for name, rs in by_name.items()]
        report(f"## Result\n\nSkipped: {skipped!r}. Elapsed: {time.monotonic()-started:.1f} s. "
               f"Peak allocated GPU memory: {torch.cuda.max_memory_allocated()/2**30:.2f} GiB.\n"
               f"\nDev-selected setting: {selected!r}. Freeze before evaluating test prompts.\n")
        report(tabulate(sorted(summary, key=lambda r: -r["F1↑"]), headers="keys", tablefmt="pipe", floatfmt=".3f"))
        report(f"\n{(out / 'run.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
