"""Exact token/basis checks before native country exchange; no model forwards. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy

from safetensors import safe_open
import torch
from transformers import AutoTokenizer


torch.set_num_threads(4)
g=runpy.run_path('scripts/english/08_jlens_one_pass.py')['main'].__globals__
tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
strings=[' Sweden',' Japan'];ids=[tok(t,add_special_tokens=False).input_ids for t in strings]
assert all(len(t)==1 for t in ids) and ids[0]!=ids[1],ids
model_dir=Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
index=json.loads((model_dir/'model.safetensors.index.json').read_text())['weight_map']
key='model.language_model.norm.weight'
with safe_open(model_dir/index[key],framework='pt',device='cpu') as f:gain=1+f.get_tensor(key).float()
key='model.language_model.embed_tokens.weight'
with safe_open(model_dir/index[key],framework='pt',device='cpu') as f:rows=torch.cat([f.get_slice(key)[i[0]:i[0]+1] for i in ids]).float()*gain
lens=Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a')/g['LENS_FILE']
assert hashlib.sha256(lens.read_bytes()).hexdigest()==g['LENS_SHA']
J=torch.load(lens,weights_only=True,map_location='cpu')['J'][15].float()
bases=g['coordinate_swap_bases']((rows@J).T,rows.T)
results=[]
for name in ('raw J','raw plain'):
    b=bases[name];v=b['vectors'];inverse=b['inverse']
    h=torch.tensor([[2.,-1.]])@v.T
    for scale in (1.,.25):
        proposed=h+scale*(g['swap_coordinates'](h,v,inverse)-h)
        coordinates=h.double()@torch.linalg.pinv(v.double()).T
        expected=(1-scale)*coordinates+scale*coordinates.flip(-1)
        error=float((proposed.double()@torch.linalg.pinv(v.double()).T-expected).abs().max())
        assert error<1e-5
        if scale==.25:assert float((proposed.double()@torch.linalg.pinv(v.double()).T-coordinates.flip(-1)).abs().max())>1.
    results.append({'basis':name,'singular_values':b['singular_values'],'rank_tolerance':b['rank_tolerance'],
                    'condition_number':b['singular_values'][0]/b['singular_values'][1],'partial_coordinate_error':error})
print(json.dumps({'exact_strings':strings,'ids':ids,'bases':results,'forwards':0,'spelling_changes':0},indent=1),flush=True)
