"""Actual launcher on all12 fixed inputs with tiny random Qwen caches. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from types import SimpleNamespace

import torch
from transformers import Qwen3_5TextConfig,Qwen3_5ForCausalLM

ROOT=Path.cwd()
source=ROOT/'scripts/english/08_jlens_one_pass.py'
launcher=runpy.run_path(str(ROOT/'slop/audits/2026-10-01_generic-reference-launcher.py'))['main'].__globals__
g=runpy.run_path(str(source))['main'].__globals__
original=json.loads((ROOT/'slop/audits/2026-10-01_generic-reference-manifest.json').read_text())
torch.set_grad_enabled(False)
torch.set_num_threads(4)
config=Qwen3_5TextConfig(vocab_size=248320,hidden_size=32,intermediate_size=64,num_hidden_layers=32,
    num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
    linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=256,
    bos_token_id=None,eos_token_id=248044,pad_token_id=248044,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,
                     'mrope_interleaved':True,'mrope_section':[3,3,2]})
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(0)
    model=Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    model.cuda=lambda *a,**kw:model
    loads.append(1)
    return model

with tempfile.TemporaryDirectory(dir=ROOT/'.local') as directory:
    tmp=Path(directory)
    fixed=[name for name in original['pins'] if not name.startswith('out/')]
    for name in fixed:
        dest=tmp/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,dest)
    lens=tmp/'lens.pt'
    torch.manual_seed(0)
    torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.randn(32,32)/32**.5}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    g['hf_hub_download']=lambda *a,**kw:str(lens)
    g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self
    g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    try:
        groups=[]
        print('Tiny random bootstrap caches; NOT pretrained evidence.',flush=True)
        for group in original['groups']:
            g['ROOT']=tmp/'bootstrap'/group['name']
            settings={'cases_json':tmp/group['data'],'end_pass_readout':True,'output_mask_max_n':1,
                      'erase_output':True,'erase_strength':.5,'chat_readout':True,'readout_max_new_tokens':32}
            capture=g['main'](**settings)
            baseline=g['main'](**settings,replay_readout_run=capture,expand_input_prefix=True)
            groups.append({**group,'capture':str(capture.relative_to(tmp)),'baseline':str(baseline.relative_to(tmp))})
        pins={name:hashlib.sha256((tmp/name).read_bytes()).hexdigest() for name in fixed}
        for group in groups:
            for folder in ('capture','baseline'):
                for path in (tmp/group[folder]).rglob('*'):
                    if path.is_file():pins[str(path.relative_to(tmp))]=hashlib.sha256(path.read_bytes()).hexdigest()
        manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'groups':groups,'pins':pins}))
        launcher['ROOT']=tmp
        launcher['MANIFEST_SHA']=hashlib.sha256(manifest.read_bytes()).hexdigest()
        launcher['runpy']=SimpleNamespace(run_path=lambda *a,**kw:{'main':g['main']})
        g['ROOT']=tmp
        before=len(loads)
        launcher['main'](source,manifest)
        master,=(tmp/'out').glob('*_generic-reference-readout')
        metadata=json.loads((master/'pipeline.json').read_text())
        assert metadata['stage']=='completed' and metadata['generic_forward_calls']==1 and metadata['case_forward_calls']==0
        assert len(loads)-before==3
        assert [(r['old_rows_exact'],r['candidate_rows']) for r in metadata['groups']]==[(176,48),(88,24)]
        assert len(json.loads((master/'summary.json').read_text()))==20
        assert len(json.loads((master/'animal_margins.json').read_text()))==12
        print('PASS actual launcher/all12 fixed inputs: one generic prefill, three fresh tiny model loads, '
              '264 old rows exact+72 new, raw/masked score parity, unchanged outputs/states, zero case forwards, '
              '20 summary rows and12 animal pair records',flush=True)
    finally:
        torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
print('Tiny random CPU model only. No pretrained generic reference observed. — PI/OpenAI',flush=True)
