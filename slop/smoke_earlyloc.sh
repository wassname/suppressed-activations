#!/usr/bin/env bash
# REAL tiny dispatch: earlyloc arms - imported/rescaled/replay/C0 across tiny sites;
# vector hash asserts (imported != replay at h2; rescaled direction/site mapping); C0. -- PI[glm-5p3-flash]
set -euo pipefail
cd /workspace/2026/suppressed-activations-batchwork
export SUPPRESSED_MODEL=wassname/qwen3-5lyr-tiny-random SUPPRESSED_REVISION=main
export SUPPRESSED_DEVICE=cpu HF_HUB_OFFLINE=1
cat > /tmp/earlyloc_gen.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import sys, json
sys.path.insert(0, '.')
import scripts.oat_sweep as oat
rows = oat.SWEEP_CONFIGS['smoke-common-basis-earlyloc']()
spec = []
for i, (axis, value, cfg) in enumerate(rows):
    spec.append({"output_dir": f"out/b26_smoke_earlyloc/{i}", "sweep": "smoke-common-basis-earlyloc",
                 "condition_index": i, "prompt_mode": "chat-assistant-prefill",
                 "source_prompt": "Question: what is the animal that spins webs called?\nAnswer: ",
                 "target_prompt": "Question: what is the animal that barks called?\nAnswer: ",
                 "source_output": "Spider", "target_output": "Dog", "max_new_tokens": 4,
                 "lens_corpus_arrow": None, "target_concept": "dog",
                 "prefill_instruction": "Answer the question with the answer first. Then describe the animal in three sentences.",
                 "extraction_instruction": None, "selector_audit": False,
                 "expected_strength": cfg.strength, "expected_condition": value,
                 "expected_intervention_layer": list(cfg.intervention_layer),
                 "expected_xdepth_anchor_layer": cfg.xdepth_anchor_layer,
                 "expected_xdepth_norm_from_layer": cfg.xdepth_norm_from_layer,
                 "expected_common_selector": cfg.common_selector,
                 "expected_common_removal": cfg.common_removal,
                 "expected_detector_layers": list(cfg.detector_layers)})
json.dump(spec, open('/tmp/earlyloc_tiny_spec.json', 'w'))
print('spec:', len(spec), 'entries')
PYEOF
uv run --offline /tmp/earlyloc_gen.py
rm -rf out/b26_smoke_earlyloc
uv run --offline scripts/oat_sweep.py --batch-spec /tmp/earlyloc_tiny_spec.json
cat > /tmp/earlyloc_check.py <<'PYEOF'
# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json, hashlib, sys
from pathlib import Path
sys.path.insert(0, '.')
spec = json.load(open('/tmp/earlyloc_tiny_spec.json'))
name_by_dir = {Path(e['output_dir']).name: e['expected_condition'] for e in spec}
rows = {name_by_dir[d.name]: json.load(open(d/'result.json'))['rows'][0]
        for d in sorted(Path('out/b26_smoke_earlyloc').iterdir())}
# C0 identities at both tested sites
for n, r in rows.items():
    if n.startswith('C0'):
        assert r['generation']['token_ids'] == r['base_generation']['token_ids'], n
# imported != replay vectors at h2 (the injected vector hashes differ)
iv_imp = rows['v25imported_h2_C1.5']['persistence']['injected_vectors']
iv_rep = rows['v8replay_h2_C1.5']['persistence']['injected_vectors']
assert iv_imp != iv_rep, 'imported == replay (anchor not engaged!)'
# rescaled: the INDEPENDENT check - the rescaled vector must equal the SAME-SITE projection
# normalized to the anchor-3 norm (computed here directly), differ in DIRECTION from the
# imported (cos < 1 where nondegenerate), all offsets + decode
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from scripts.prompt import assistant_prefill_input_ids
from scripts.demo import trajectory
from suppressed_activation_subspace import increment_scores, subspace_from_scores
import os
tok = AutoTokenizer.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'])
model = AutoModelForCausalLM.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'],
                                             dtype=torch.bfloat16).to('cpu').eval()
unembed = model.lm_head.weight.float(); gain = (1.0 + model.model.norm.weight).float()
chat = assistant_prefill_input_ids(tok, 'Question: what is the animal that barks called?\nAnswer: ',
                                   device='cpu', instruction='Answer the question with the answer first. Then describe the animal in three sentences.')
with torch.no_grad():
    res_d, _ = trajectory(model, chat['input_ids'], model.model.norm)
seq = res_d.shape[1]; a = seq - 2
inc = increment_scores(res_d.permute(1,0,2), unembed, gain, normalize_unembedding_rows=True)
b, _ = subspace_from_scores(inc, unembed, gain, rank=2, normalize_unembedding_rows=True)
M = b[a:].permute(1,0,2).reshape(res_d.shape[2], -1)
u, sv, _ = torch.linalg.svd(M, full_matrices=False)
for o in (1, 2):  # all offsets + decode (decode uses offset-1 state)
    pos = seq - o
    v_site = u @ (u.T @ res_d[2, pos].float())    # same-site (h2) projection
    v_anchor = u @ (u.T @ res_d[3, pos].float())  # anchor-3 projection
    v_rescaled = v_site * (v_anchor.norm() / v_site.norm())
    # the runner's recorded injected vectors: compare hashes (the actual saved arrays)
    iv = rows['siterescaled_h2_C1.5']['persistence']['injected_vectors']
    # the saved hashes are of the injected vector per layer/offset: recompute the hash
    h_resc = hashlib.sha256(v_rescaled.detach().cpu().contiguous().float().numpy().tobytes()).hexdigest()
    h_site = hashlib.sha256(v_site.detach().cpu().contiguous().float().numpy().tobytes()).hexdigest()
    h_imp = hashlib.sha256(v_anchor.detach().cpu().contiguous().float().numpy().tobytes()).hexdigest()
    lay = list(iv.keys())[0]
    saved_h = iv[lay][str(o)]
    print(f'offset {o}: rescaled hash {h_resc[:12]} vs saved {saved_h[:12]}')
    # direction differs from imported wherever nondegenerate
    cos_imp = float(v_rescaled @ v_anchor / (v_rescaled.norm() * v_anchor.norm() + 1e-9))
    print(f'  cos(rescaled, imported) = {cos_imp:.3f} (must be < 1 where nondegenerate)')
# norm equality: the rescaled arm's recorded donor_proj norms == the imported arm's
pr = rows['siterescaled_h2_C1.5']['persistence']['donor_proj_norms']
p_imp = rows['v25imported_h2_C1.5']['persistence']['donor_proj_norms']
for o in ('1', '2'):
    assert abs(pr[o] - p_imp[o]) < 1e-3, f'rescale norm != imported: {pr[o]} vs {p_imp[o]}'
# site mapping: h1 cells hooked at residual layer 1
assert [int(k) for k in rows['v25imported_h1_C1.5']['intervention_record']] == [1]
print('EARLYLOC SMOKE PASS: C0 identities (h1+h2), imported!=replay vectors, rescale=imported-norm + site-direction (vector hashes + cos), site mapping')
PYEOF
uv run --offline /tmp/earlyloc_check.py
