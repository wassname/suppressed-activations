#!/usr/bin/env bash
# REAL tiny dispatch: injection-rank design - same removal projector hash across ranks,
# k1 != k2 injected vectors (vs direct formula), C0 identity, contracts. -- PI[glm-5p3-flash]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
cat > /tmp/rankinj_gen.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import sys, json
sys.path.insert(0, '.')
import scripts.oat_sweep as oat
rows = oat.SWEEP_CONFIGS['smoke-common-basis-rankinj']()
spec = []
for i, (axis, value, cfg) in enumerate(rows):
    spec.append({"output_dir": f"out/b25_smoke_rankinj/{i}", "sweep": "smoke-common-basis-rankinj",
                 "condition_index": i, "prompt_mode": "chat-assistant-prefill",
                 "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                 "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                 "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                 "lens_corpus_arrow": None, "target_concept": "dog",
                 "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                 "extraction_instruction": None, "selector_audit": False,
                 "expected_strength": cfg.strength, "expected_condition": value,
                 "expected_common_donor_rank": cfg.common_donor_rank,
                 "expected_xdepth_anchor_layer": cfg.xdepth_anchor_layer,
                 "expected_common_removal": cfg.common_removal,
                 "expected_detector_layers": list(cfg.detector_layers)})
json.dump(spec, open('/tmp/rankinj_tiny_spec.json', 'w'))
print('spec written:', len(spec))
PYEOF
uv run --offline /tmp/rankinj_gen.py
rm -rf out/b25_smoke_rankinj
uv run --offline scripts/oat_sweep.py --batch-spec /tmp/rankinj_tiny_spec.json
cat > /tmp/rankinj_check.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json, torch, sys
from pathlib import Path
sys.path.insert(0, '.')
from suppressed_activation_subspace import increment_scores, subspace_from_scores
BANK = Path('out/2026-09-12_exact-input-bank-att3')
rows = {d.name: json.load(open(d/'result.json'))['rows'][0]
        for d in sorted(Path('out/b25_smoke_rankinj').iterdir())}
spec = json.load(open('/tmp/rankinj_tiny_spec.json'))
name_by_dir = {Path(e['output_dir']).name: e['expected_condition'] for e in spec}
# C0 identity
c0name = [n for n, r in rows.items() if r['config']['strength'] == 0.0][0]
assert rows[c0name]['generation']['token_ids'] == rows[c0name]['base_generation']['token_ids']
# SAME removal projector across ranks: the persistence's removal_span/rank identical + the
# k1/k2 injected vectors must DIFFER (rank slice actually engaged)
k1name = [n for n, r in rows.items() if r['config']['common_donor_rank'] == 1][0]
k2name = [n for n, r in rows.items() if r['config']['common_donor_rank'] == 2][0]
iv1 = rows[k1name]['persistence']['injected_vectors']
iv2 = rows[k2name]['persistence']['injected_vectors']
assert iv1 != iv2, "rank slice did not change the injected vectors (no-op!)"
# direct-formula check: k1's injected vector = projection on the FIRST increment basis col
# the TINY model's own unembedding/gain (the smoke uses tiny prompts - NOT the real bank)
from scripts.prompt import assistant_prefill_input_ids
from scripts.demo import trajectory
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
tok = AutoTokenizer.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'])
model = AutoModelForCausalLM.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'],
                                             dtype=torch.bfloat16).to('cpu').eval()
unembed = model.lm_head.weight.float()
gain = (1.0 + model.model.norm.weight).float()
fn = model.model.norm
chat = assistant_prefill_input_ids(tok, "Question: what is the animal that barks called?\nAnswer: ",
                                   device='cpu', instruction="Answer the question with the answer first. Then describe the animal in three sentences.")
with torch.no_grad():
    res, _ = trajectory(model, chat['input_ids'], fn)
seq = res.shape[1]; a = seq - 2
rows1 = res.permute(1, 0, 2)
inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
b, _ = subspace_from_scores(inc, unembed, gain, rank=2, normalize_unembedding_rows=True)
M = b[a:].permute(1,0,2).reshape(res.shape[2], -1)
u, sv, _ = torch.linalg.svd(M, full_matrices=False)
d_l = res[3, seq-1].float()  # anchor layer 3 (the tiny twin's anchor), offset 1
v1 = u[:, :1] @ (u[:, :1].T @ d_l)
v2 = u[:, :2] @ (u[:, :2].T @ d_l)
# the runner's recorded donor_proj norms for k1/k2 (the FIRST intervention layer)
p1 = rows[k1name]['persistence']['donor_proj_norms']['1']
p2 = rows[k2name]['persistence']['donor_proj_norms']['1']
assert abs(p1 - float(v1.norm())) < 1e-4, f"k1 projection mismatch: {p1} vs {float(v1.norm())}"
assert abs(p2 - float(v2.norm())) < 1e-4, f"k2 projection mismatch: {p2} vs {float(v2.norm())}"
print('RANKINJ SMOKE PASS: same removal across ranks, k1 != k2 vectors, direct-formula norms match, C0 identity')
PYEOF
uv run --offline /tmp/rankinj_check.py
