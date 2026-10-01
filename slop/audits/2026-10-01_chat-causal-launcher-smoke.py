"""Actual immutable-path launcher on tiny random Qwen; no scientific results. — PI/OpenAI"""
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

ROOT=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
source=ROOT/'.local/queued/08_chat_causal_smoke.py'
shutil.copyfile(ROOT/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
launcher=runpy.run_path(str(ROOT/'slop/audits/2026-10-01_chat-causal-launcher.py'))['main'].__globals__
factory=next(n for n in ast.parse((ROOT/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(0);cfg=config(248320);cfg.eos_token_id=248044
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    model.cuda=lambda *a,**kw:model;loads.append(1)
    return model

with tempfile.TemporaryDirectory(dir=ROOT/'.local') as directory:
    tmp=Path(directory);(tmp/'data').mkdir()
    donor_config=ROOT/'data/dog_spider_donors_chat_v4.json'
    shutil.copyfile(donor_config,tmp/'data'/donor_config.name)
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self
    g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    try:
        g['ROOT']=tmp/'literal'
        literal=g['main'](prepare_donors_json=ROOT/'data/dog_spider_donors_pronoun_v2.json')
        evaluation=json.loads((ROOT/'data/dog_spider_joint_chat_v1.json').read_text())
        evaluation.update(previous_donor=str((literal/'donors.pt').relative_to(tmp)),previous_donor_sha256=hashlib.sha256((literal/'donors.pt').read_bytes()).hexdigest())
        cases=tmp/'data/dog_spider_joint_chat_v1.json';cases.write_text(json.dumps(evaluation))
        pins={str(p.relative_to(tmp)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (tmp/'data').iterdir()}
        pins['scripts/english/08_jlens_one_pass.py']=hashlib.sha256(source.read_bytes()).hexdigest()
        pins[evaluation['previous_donor']]=evaluation['previous_donor_sha256']
        manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'pins':pins}))
        launcher['ROOT']=tmp;launcher['runpy']=SimpleNamespace(run_path=lambda *a,**kw:{'main':g['main']})
        g['ROOT']=tmp;before=len(loads)
        launcher['main'](source,manifest,hashlib.sha256(manifest.read_bytes()).hexdigest())
        master,=(tmp/'out').glob('*_chat-causal-joint')
        metadata=json.loads((master/'pipeline.json').read_text())
        assert metadata['stage']=='completed' and len(metadata['case_runs'])==3
        assert len(loads)-before==4
        assert metadata['actual_forwards']==8+metadata['generated_tokens']<=392
        for group in metadata['case_runs']:
            text=(Path(group['run'])/'run.md').read_text()
            assert 'skeleton uses its own word-answer pair' not in text
            assert 'joint skeleton and parity outcomes are assessed from complete text' in text
        arithmetic=Path(metadata['case_runs'][2]['run'])
        assert len(json.loads((arithmetic/'interventions.json').read_text()))==4
        report=(arithmetic/'run.md').read_text()
        assert 'no random arithmetic condition was run' not in report
        assert 'arithmetic remains4 and even for Base, both donors and matched random' in report
        print('PASS actual immutable-path launcher:8 generic prefills,12 conditions, four fresh tiny model loads, '
              'signed vectors/control norms, exact forward/coverage accounting, corrected four-condition arithmetic report; no pretrained results',flush=True)
    finally:
        torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
print('Tiny random CPU model only. — PI/OpenAI',flush=True)
