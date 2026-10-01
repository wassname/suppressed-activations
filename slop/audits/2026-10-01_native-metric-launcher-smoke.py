"""Actual native-metric coordinator against a retained nonidentity-J tiny reference. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import sys
from types import SimpleNamespace
import torch
from transformers import Qwen3_5TextConfig,Qwen3_5ForCausalLM

root=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
source=root/'.local/queued/08_native_metric_launcher_smoke.py';shutil.copyfile(root/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
launch=runpy.run_path(str(root/'slop/audits/2026-10-01_boundary-readout-launcher.py'))['main'].__globals__
check=runpy.run_path(str(root/'slop/audits/2026-10-01_native-v4-launcher.py'))['check_forward_trace']
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
tmp=Path(tempfile.mkdtemp(prefix='native-metric-launcher-',dir=root/'.local'));print('retained fixture='+str(tmp),flush=True)
paths=['data/english_boundary_readout_v1.json','data/english_hidden_words_v4_chat.json','out/2026-09-30_125500_jlens-one-pass/cases.json','slop/audits/2026-10-01_native-v4-launcher.py']
for name in paths:
    dest=tmp/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dest)
pins={name:hashlib.sha256((tmp/name).read_bytes()).hexdigest() for name in paths}
pins['scripts/english/08_jlens_one_pass.py']=hashlib.sha256(source.read_bytes()).hexdigest()
manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'pins':pins}))
fixture=Path(sys.argv[1]);reference,=(fixture/'base/out').glob('*_jlens-one-pass');shutil.copytree(reference,tmp/'reference')
lens=fixture/'lens.pt'
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(1);cfg=config(248320);cfg.eos_token_id=248044
    m=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False);m.cuda=lambda *a,**kw:m;loads.append(m);return m
g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load);g['hf_hub_download']=lambda *a,**kw:str(lens)
g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest();g['ROOT']=tmp
launch['ROOT']=tmp;launch['runpy']=SimpleNamespace(run_path=lambda p:{'main':g['main']} if Path(p)==source else {'check_forward_trace':check})
cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask;torch.Tensor.cuda=lambda self,*a,**kw:self
g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
try:
    launch['main'](source,manifest,hashlib.sha256(manifest.read_bytes()).hexdigest(),native_metric=True,reference=tmp/'reference')
    master,=(tmp/'out').glob('*_native-metric-readout');meta=json.loads((master/'pipeline.json').read_text())
    assert meta['stage']=='completed' and len(loads)==1
    assert meta['actual_forwards']==meta['generated_tokens']<=192
    out=Path(meta['run']);assert len(json.loads((out/'readout.json').read_text()))==252
    assert len(list((out/'native_metric_readouts').glob('*.json')))==6
    assert json.loads((out/'metric_reproduction.json').read_text())['readout_rows_exact']==180
    assert 'translation' in (master/'run.md').read_text() and 'preclue' in (master/'run.md').read_text()
    print('PASS actual immutable-path coordinator: exact6-case selection, one fresh tiny model,252 rows,144 fixed-position lists,180-row/reference state-generation parity, per-call coverage and grouped report. No pretrained result.',flush=True)
finally:torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
