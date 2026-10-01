"""Tiny real-pipeline boundary readout and unchanged-final regression. — PI/OpenAI"""
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
source=root/'.local/queued/08_boundary_smoke.py';shutil.copyfile(root/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
for seed in (0,1):
    tmp=Path(tempfile.mkdtemp(prefix=f'boundary-smoke-{seed}-',dir=root/'.local'));print('retained fixture='+str(tmp),flush=True)
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    models=[];events=[]
    def load(*args,**kwargs):
        torch.manual_seed(seed);cfg=config(248320);cfg.eos_token_id=248044
        m=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False);m.cuda=lambda *a,**kw:m
        m.register_forward_pre_hook(lambda *_:events.append(torch.is_grad_enabled()));models.append(m);return m
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self;g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    args=dict(cases_json=root/'data/english_boundary_readout_v1.json',end_pass_readout=True,chat_readout=True,
              erase_output=True,erase_strength=.5,output_mask_max_n=1,readout_max_new_tokens=32)
    try:
        g['ROOT']=tmp/'base';base=g['main'](**args)
        traces=json.loads((base/'generation_traces.json').read_text());assert len(events)==sum(len(t['token_ids']) for t in traces)
        events.clear();g['ROOT']=tmp/'replay';replay=g['main'](**args,replay_readout_run=base,expand_input_prefix=True)
        assert not events
        g['ROOT']=tmp/'boundary';out=g['main'](**args,expand_input_prefix=True,boundary_readout=True)
        actual=json.loads((out/'generation_traces.json').read_text());assert actual==traces
        assert len(events)==sum(len(t['token_ids']) for t in actual) and not any(events)
        old=json.loads((replay/'readout.json').read_text());new=json.loads((out/'readout.json').read_text())
        old_map={(r['case_index'],r['method']):r for r in old}
        assert len(old)==132 and len(new)==180
        assert {k:r for r in new if (k:=(r['case_index'],r['method'])) in old_map}==old_map
        a=torch.load(base/'prefill.pt',weights_only=True);b=torch.load(out/'prefill.pt',weights_only=True)
        assert all(torch.equal(x[k],y[k]) for x,y in zip(a,b,strict=True) for k in x)
        full=torch.load(out/'prefill_positions.pt',weights_only=True)
        tok=g['AutoTokenizer'].from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
        data=json.loads((root/'data/english_boundary_readout_v1.json').read_text())
        for i,case in enumerate(data['cases']):
            point=json.loads((out/'boundary_readouts'/f'{i:03d}.json').read_text())
            positions=g['native_readout_positions'](tok,case['prompt'],point['input_ids'])
            assert positions==point['positions'] and positions['preclue']==2 and point['final_scores_exact']
            assert point['consumed_prefixes']['boundary'].endswith('<|im_end|>\n')
            assert point['consumed_prefixes']['preclue']=='<|im_start|>user\n'
            assert point['output_direction_id']==actual[i]['token_ids'][0]
            saved=torch.load(out/'boundary_readouts'/f'{i:03d}.pt',weights_only=True);assert len(saved)==8
            direction=models[-1].get_output_embeddings().weight[point['output_direction_id']].float()
            W=models[-1].get_output_embeddings().weight
            for kind,pos in positions.items():
                expected=g['fixed_position_logits'](models[-1],W,torch.eye(32),full[i],pos,direction)
                assert all(torch.equal(z,saved[name.replace('end-pass ',f'end-pass {kind} ',1)]) for name,z in expected.items())
            corrupt=point['input_ids'].copy();corrupt[0]+=1
            try:g['native_readout_positions'](tok,case['prompt'],corrupt);raise RuntimeError('bad prefix accepted')
            except AssertionError:pass
        assert 'Fixed structural readout positions' in (out/'run.md').read_text()
        assert all(p.grad is None for model in models for p in model.parameters())
        print(f'PASS seed{seed}:6 cases,132 old rows exact +48 boundary/preclue rows; exact states/full generations, one-pass coverage, cached no-forwards, metadata-only positions, raw-head reconstruction, corrupt-prefix rejection. Tiny random CPU model, no scientific result.',flush=True)
    finally:torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
