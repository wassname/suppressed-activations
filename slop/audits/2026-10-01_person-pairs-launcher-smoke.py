"""Actual four-case launcher with tiny random Qwen; no scientific outputs. — PI/OpenAI"""
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
source=ROOT/'.local/queued/08_person_smoke.py';shutil.copyfile(ROOT/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
l=runpy.run_path(str(ROOT/'slop/audits/2026-10-01_person-pairs-launcher.py'))['main'].__globals__
factory=next(n for n in ast.parse((ROOT/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
loads=[]
def load(*args,**kwargs):
    torch.manual_seed(0);cfg=config(248320);cfg.eos_token_id=248044
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    model.cuda=lambda *a,**kw:model;loads.append(1);return model

z=torch.arange(6,dtype=torch.float32)
assert l['label_stats'](z,[1,4],[4,5])=={'rank':1,'max_logit':4.,'selected_prefix_hit':True}
assert l['label_stats'](z,[],[4,5])=={'rank':None,'max_logit':None,'selected_prefix_hit':False}
z[[1,4]]=-torch.inf
assert l['label_stats'](z,[1,4],[3,5])=={'rank':10**9,'max_logit':None,'selected_prefix_hit':False}
with tempfile.TemporaryDirectory(dir=ROOT/'.local') as directory:
    tmp=Path(directory)
    for name in (l['DATA'],l['LABELS'],l['CHECKS']):
        target=tmp/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest();g['ROOT']=tmp
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self;g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    try:
        pins={name:hashlib.sha256((tmp/name).read_bytes()).hexdigest() for name in (l['DATA'],l['LABELS'],l['CHECKS'])}
        pins[l['SOURCE']]=hashlib.sha256(source.read_bytes()).hexdigest()
        manifest=tmp/'manifest.json';manifest.write_text(json.dumps({'pins':pins}));sha=hashlib.sha256(manifest.read_bytes()).hexdigest()
        l['ROOT']=tmp
        real_runpy=l['runpy']
        l['runpy']=SimpleNamespace(run_path=lambda path: {'main':g['main']} if Path(path)==source else real_runpy.run_path(path))
        l['main'](source,manifest,sha)
        master,=(tmp/'out').glob('*_person-pairs-readout');p=json.loads((master/'pipeline.json').read_text())
        assert p['stage']=='completed' and p['original_rows_exact']==72 and p['candidate_rows']==16 and p['rescore_forward_calls']==0
        assert len(loads)==2 and p['actual_forwards']==p['generated_tokens']<=128
        pairs=json.loads((master/'pair_diagnostics.json').read_text());assert len(pairs)==8
        for pair in pairs:
            margins=[c['raw']['own']['max_logit']-c['raw']['partner']['max_logit'] for c in pair['cases']]
            assert pair['raw_D']==sum(margins) and pair['raw_reversal']==all(m>0 for m in margins)
        capture=Path(p['capture']);traces=json.loads((capture/'generation_traces.json').read_text());events=[json.loads(s) for s in (master/'forward_trace.jsonl').read_text().splitlines()]
        checks=real_runpy.run_path(str(tmp/l['CHECKS']));traces[0]['coverage']['24'][0]+=1
        try:checks['check_forward_trace'](traces,events)
        except AssertionError:pass
        else:raise AssertionError('Corrupt coverage passed')
        with (tmp/l['LABELS']).open('a') as stream:stream.write(' ')
        try:l['main'](source,manifest,sha)
        except AssertionError:pass
        else:raise AssertionError('Changed labels passed pin check')
        assert len(loads)==2
        print('PASS immutable-path launcher: four exact inputs,72 old rows exact+16 candidates, zero cached forwards, two fresh tiny models, eight raw/masked pair diagnostics, empty/masked-label boundaries, coverage corruption and label-pin rejection. No pretrained scientific result. — PI/OpenAI',flush=True)
    finally:torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
