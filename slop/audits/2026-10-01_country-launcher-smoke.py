"""Run shared launcher for both declared families with fresh tiny models. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from types import SimpleNamespace
import torch
from transformers import Qwen3_5TextConfig,Qwen3_5ForCausalLM

root=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
source=root/'.local/queued/08_country_launcher_smoke.py';shutil.copyfile(root/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
launcher=runpy.run_path(str(root/'slop/audits/2026-10-01_chat-causal-launcher.py'))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(0);cfg=config(248320);cfg.eos_token_id=248044
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    model.cuda=lambda *a,**kw:model;loads.append(1);return model
for filename,n_conditions in [('dog_spider_joint_chat_v1.json',12),('sweden_japan_joint_chat_v1.json',9)]:
    tmp=Path(tempfile.mkdtemp(prefix='country-launcher-smoke-',dir=root/'.local'));(tmp/'data').mkdir()
    print('retained fixture='+str(tmp),flush=True)
    evaluation=json.loads((root/'data'/filename).read_text())
    donor_config=root/evaluation['donor_config'];shutil.copyfile(donor_config,tmp/evaluation['donor_config'])
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self;g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    try:
        if evaluation['previous_donor'] is not None:
            g['ROOT']=tmp/'literal';literal=g['main'](prepare_donors_json=root/'data/dog_spider_donors_pronoun_v2.json')
            evaluation.update(previous_donor=str((literal/'donors.pt').relative_to(tmp)),previous_donor_sha256=hashlib.sha256((literal/'donors.pt').read_bytes()).hexdigest())
        config_path=Path('data')/filename;(tmp/config_path).write_text(json.dumps(evaluation))
        pins={str(p.relative_to(tmp)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (tmp/'data').iterdir()}
        pins['scripts/english/08_jlens_one_pass.py']=hashlib.sha256(source.read_bytes()).hexdigest()
        if evaluation['previous_donor'] is not None:pins[evaluation['previous_donor']]=evaluation['previous_donor_sha256']
        manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'pins':pins}))
        launcher['ROOT']=tmp;launcher['runpy']=SimpleNamespace(run_path=lambda *a,**kw:{'main':g['main']})
        g['ROOT']=tmp;before=len(loads)
        launcher['main'](source,manifest,hashlib.sha256(manifest.read_bytes()).hexdigest(),config_path,'test-causal-joint')
        master,=(tmp/'out').glob('*_test-causal-joint');metadata=json.loads((master/'pipeline.json').read_text())
        assert metadata['stage']=='completed' and len(metadata['case_runs'])==3 and len(loads)-before==4
        assert metadata['actual_forwards']==8+metadata['generated_tokens']<=8+32*n_conditions
        rows=[json.loads((Path(c['run'])/'interventions.json').read_text()) for c in metadata['case_runs']]
        assert sum(map(len,rows))==n_conditions
        for c in metadata['case_runs']:
            text=(Path(c['run'])/'run.md').read_text()
            assert 'first tokens only, not full multi-token answers' in text
            assert 'skeleton uses its own word-answer pair' not in text
        arithmetic=(Path(metadata['case_runs'][2]['run'])/'run.md').read_text()
        assert 'arithmetic remains4 and even for every condition' in arithmetic
        assert 'first-token' in (master/'run.md').read_text().lower()
        print(f'PASS {filename}: actual shared launcher;8 generic prefills,{n_conditions} conditions,4 fresh tiny models, signed/control vectors, exact forward/coverage accounting, probability scope and arithmetic report. No pretrained result.',flush=True)
    finally:torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
