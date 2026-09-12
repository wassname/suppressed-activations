# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json, torch, sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, '.')
from pathlib import Path
rows = {d.name: json.load(open(d/'result.json'))['rows'][0]
        for d in sorted(Path('out/b25_smoke_rankinj').iterdir())}
fps = {n: r['persistence']['removal_cols_sha256'] for n, r in rows.items()}
print("removal fingerprints:", {n: h[:12] for n, h in fps.items()})
assert len(set(fps.values())) == 1, "removal projector differs across ranks!"
print("removal projector IDENTICAL across all conditions (fingerprint)")
spec = json.load(open('/tmp/rankinj_tiny_spec.json'))
name_by_dir = {Path(e['output_dir']).name: e['expected_condition'] for e in spec}
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from scripts.prompt import assistant_prefill_input_ids
from scripts.demo import trajectory
from suppressed_activation_subspace import increment_scores, subspace_from_scores
tok = AutoTokenizer.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'])
model = AutoModelForCausalLM.from_pretrained(os.environ['SUPPRESSED_MODEL'], revision=os.environ['SUPPRESSED_REVISION'],
                                             dtype=torch.bfloat16).to('cpu').eval()
unembed = model.lm_head.weight.float()
gain = (1.0 + model.model.norm.weight).float()
chat = assistant_prefill_input_ids(tok, "Question: what is the animal that barks called?\nAnswer: ",
                                   device='cpu', instruction="Answer the question with the answer first. Then describe the animal in three sentences.")
with torch.no_grad():
    res, _ = trajectory(model, chat['input_ids'], model.model.norm)
seq = res.shape[1]; a = seq - 2
rows1 = res.permute(1, 0, 2)
inc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
b, _ = subspace_from_scores(inc, unembed, gain, rank=2, normalize_unembedding_rows=True)
M = b[a:].permute(1,0,2).reshape(res.shape[2], -1)
u, sv, _ = torch.linalg.svd(M, full_matrices=False)
d_l = res[3, seq-1].float()
for k, condname in ((1, 'k1_C1.5'), (2, 'k2_C1.5')):
    dir_cell = [n for n, e in name_by_dir.items() if e == condname][0]
    saved = rows[dir_cell]['persistence']['injected_vectors']
    v = u[:, :k] @ (u[:, :k].T @ d_l)
    vh = hashlib.sha256(v.detach().cpu().contiguous().float().numpy().tobytes()).hexdigest()
    layer_key = list(saved.keys())[0]
    saved_h = saved[layer_key][list(saved[layer_key].keys())[0]]
    print(f"k{k}: direct {vh[:12]} vs saved {saved_h[:12]} -> {'MATCH' if vh == saved_h else 'DIFFER'}")
