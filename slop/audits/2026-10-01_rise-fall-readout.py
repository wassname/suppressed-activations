"""Rise-and-fall (L22/27/32) top-32 on the saved v3/v4/translation prompts, same masks as 08 end-pass. — PI/OpenAI
One prefill per prompt. Parity: residuals24/27/32 vs saved prefill.pt and masked plain27 top-32 vs saved rows."""
import json
from pathlib import Path
import runpy

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_grad_enabled(False)
g = runpy.run_path("scripts/english/08_jlens_one_pass.py")["main"].__globals__
q, s4, trajectory = g["q"], g["s4"], g["trajectory"]
from suppressed_activation_subspace import suppressed_activation_scores

RUNS = ["out/2026-09-30_125330_jlens-one-pass", "out/2026-09-30_142814_jlens-one-pass", "out/2026-09-30_125500_jlens-one-pass"]
tok = AutoTokenizer.from_pretrained(q.MODEL, revision=q.REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(q.MODEL, revision=q.REVISION, dtype=torch.bfloat16, local_files_only=True).cuda().eval()
W, gain = model.lm_head.weight, 1.0 + model.model.norm.weight.float()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]
vocab_norm = [t.strip().lower() for t in vocab]
word_index = s4.WordIndex(vocab_norm)
out_rows, parity = [], []
for run in RUNS:
    rows = json.loads((Path(run) / "readout.json").read_text())
    saved_states = torch.load(Path(run) / "prefill.pt", weights_only=True)
    plain27 = {r["case_index"]: r for r in rows if r["method"] == "end-pass plain27"}
    for index, ref in sorted(plain27.items()):
        ids = tok(ref["prompt"], return_tensors="pt", add_special_tokens=False).input_ids.cuda()
        res, _ = trajectory(model, ids, model.model.norm)
        state_error = max(float((res[k][-1].float().cpu() - saved_states[index][k].float()).abs().max()) for k in (24, 27, 32))
        final_logits = model.lm_head(model.model.norm(res[32][-1])).float()
        mask = q.prompt_word_mask(ref["prompt"], vocab_norm, "cuda") | s4.output_word_mask(final_logits, vocab_norm, word_index, max_n=1)
        z27 = model.lm_head(model.model.norm(res[27][-1])).float().masked_fill(mask, -torch.inf)
        top27 = [vocab[t] for t in z27.topk(32).indices.tolist()]
        parity.append({"run": run, "case_index": index, "max_state_error": state_error, "plain27_top32_equal": top27 == ref["top32"]})
        rf = suppressed_activation_scores(res[None, :, -1], W, gain, early_layer=22, peak_layer=27, output_layer=32)[0]
        for name, z in (("rise-and-fall", rf), ("rise-and-fall masked", rf.masked_fill(mask, -torch.inf))):
            out_rows.append({**{k: ref[k] for k in ("prompt", "concept", "case_index", "hidden_aliases", "answer_aliases",
                                                    "actual_words", "intended_answer_observed")},
                             "run": run, "method": name, "top32": [vocab[t] for t in z.topk(32).indices.tolist()]})
Path("slop/audits/2026-10-01_rise-fall-readout.json").write_text(json.dumps({"rows": out_rows, "parity": parity}, ensure_ascii=False, indent=1))
print(f"cases={len(parity)} plain27 parity={sum(p['plain27_top32_equal'] for p in parity)}/{len(parity)} "
      f"max state error={max(p['max_state_error'] for p in parity):.4g}")
print("example", out_rows[0]["concept"], out_rows[1]["top32"][:12])
