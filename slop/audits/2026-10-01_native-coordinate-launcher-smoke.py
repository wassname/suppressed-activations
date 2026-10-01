"""Actual native-coordinate coordinator against retained real tiny trajectories. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from types import SimpleNamespace

import torch
from transformers import Qwen3_5TextConfig, Qwen3_5ForCausalLM

root=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
fixture=root/'.local/native-coordinate-1-itwidtii'
source=root/'.local/queued/08_native_coordinate_launcher_smoke.py';shutil.copyfile(root/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
launcher=runpy.run_path(str(root/'slop/audits/2026-10-01_chat-causal-launcher.py'))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
tmp=Path(tempfile.mkdtemp(prefix='native-coordinate-launcher-',dir=root/'.local'));(tmp/'data').mkdir();(tmp/'reference').mkdir()
print('fixture='+str(tmp),flush=True)
config_path=Path('data/sweden_japan_joint_chat_v1.json');evaluation=json.loads((root/config_path).read_text())
shutil.copyfile(root/config_path,tmp/config_path);shutil.copyfile(root/evaluation['donor_config'],tmp/evaluation['donor_config'])
reference={'stage':'completed','case_runs':[]}
for i,case in enumerate(evaluation['cases']):
    original,=(fixture/case['name']).glob('out/*/interventions.json')
    target=tmp/'reference'/str(i);target.mkdir();shutil.copyfile(original,target/'interventions.json')
    reference['case_runs'].append({'case':case,'run':str(target)})
(tmp/'reference/pipeline.json').write_text(json.dumps(reference))
pins={str(p.relative_to(tmp)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('data','reference') for p in (tmp/folder).rglob('*.json')}
pins['scripts/english/08_jlens_one_pass.py']=hashlib.sha256(source.read_bytes()).hexdigest()
manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'pins':pins}))
vocab_size=len(g['AutoTokenizer'].from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True))
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(1);cfg=config(vocab_size);cfg.eos_token_id=248044
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    model.model.norm.weight.copy_(torch.linspace(-.1,.2,32).to(torch.bfloat16))
    model.cuda=lambda *a,**kw:model;loads.append(1);return model
g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
lens=fixture/'lens.pt';g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
torch.Tensor.cuda=lambda self,*a,**kw:self;g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
try:
    launcher['ROOT']=tmp;g['ROOT']=tmp
    launcher['runpy']=SimpleNamespace(run_path=lambda *a,**kw:{'main':g['main']})
    launcher['main'](source,manifest,hashlib.sha256(manifest.read_bytes()).hexdigest(),config_path,
                     'native-coordinate-test',True,tmp/'reference')
    master,=(tmp/'out').glob('*_native-coordinate-test');p=json.loads((master/'pipeline.json').read_text())
    assert p['stage']=='completed' and p['raw_coordinate_exchange'] and p['generic_prefills']==0
    assert len(loads)==len(p['case_runs'])==3 and p['actual_forwards']==p['generated_tokens']<=384
    events=[json.loads(line) for line in (master/'forward_trace.jsonl').read_text().splitlines()]
    assert all(e['phase'] in {c['name'] for c in evaluation['cases']} and not e['grad_enabled'] for e in events)
    assert 'generic_prefills: 0' in (master/'run.md').read_text()
    print('PASS actual coordinator:3 fresh tiny models,12 trajectories,zero generic/target prefills,exact Base token/top10/readout reference parity,coverage/budget and final report.',flush=True)
finally:
    torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
