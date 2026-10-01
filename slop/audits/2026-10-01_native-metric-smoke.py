"""Real tiny nonidentity-J pipeline; native-metric observation must not change inference. — PI/OpenAI"""
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
source=root/'.local/queued/08_native_metric_smoke.py';shutil.copyfile(root/'scripts/english/08_jlens_one_pass.py',source)
g=runpy.run_path(str(source))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
for seed in (0,1):
    tmp=Path(tempfile.mkdtemp(prefix=f'native-metric-{seed}-',dir=root/'.local'));print('retained fixture='+str(tmp),flush=True)
    torch.manual_seed(seed);J=torch.eye(32)+.15*torch.randn(32,32)
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:J,23:J}},lens)
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
              erase_output=True,erase_strength=.5,output_mask_max_n=1,readout_max_new_tokens=32,
              expand_input_prefix=True,boundary_readout=True)
    try:
        g['ROOT']=tmp/'base';base=g['main'](**args)
        old=json.loads((base/'readout.json').read_text());assert len(old)==180
        events.clear();g['ROOT']=tmp/'candidate';out=g['main'](**args,native_metric_erasure=True,verify_readout_run=base)
        reproduction=json.loads((out/'metric_reproduction.json').read_text());assert reproduction['readout_rows_exact']==180
        traces=json.loads((out/'generation_traces.json').read_text());assert len(events)==sum(len(t['token_ids']) for t in traces) and not any(events)
        new=json.loads((out/'readout.json').read_text());assert len(new)==252
        idx={(r['case_index'],r['method']):r for r in new}
        assert all(idx[r['case_index'],r['method']]==r for r in old)
        assert all(torch.equal(a,b) for a,b in zip(models[0].parameters(),models[1].parameters(),strict=True))
        W=models[-1].get_output_embeddings().weight.float();gain=1+models[-1].model.norm.weight.float()
        for i in range(6):
            saved=torch.load(out/f'native_metric_readouts/{i:03d}.pt',weights_only=True)
            assert len(saved['scores'])==12 and set(saved['states'])=={'final','boundary','preclue'}
            for point,heads in saved['states'].items():
                for head,a in heads.items():
                    y,w,requested,applied=(a[k] for k in ('original','output_embedding','requested','applied'))
                    delta=y-requested;c=.5*(y@w)
                    if head!='random0 J-lens':
                        B=gain[:,None]*J if head=='J-lens' else torch.diag(gain)
                        grad=B.T@w;expected=c*(B@grad)/(grad@grad)
                        assert torch.allclose(delta,expected,atol=2e-6,rtol=2e-5),(i,point,head)
                    assert torch.equal(applied,requested.to(torch.bfloat16).float())
                    assert abs(float(requested@w-.5*(y@w)))<1e-4*float(y.norm()*w.norm())
                    prefix='end-pass '+(f'{point} ' if point!='final' else '')
                    method=prefix+'input-prefix metric-erased0.5 '+head
                    # BF16 linear arithmetic is the production head, not an FP32 surrogate. — PI/OpenAI
                    expected_logits=models[-1].lm_head(applied.to(torch.bfloat16)).float()
                    assert torch.equal(expected_logits,saved['scores'][method])
                a,b=heads['J-lens'],heads['random0 J-lens']
                assert torch.allclose((a['original']-a['requested']).norm(),(b['original']-b['requested']).norm(),atol=2e-6,rtol=2e-5)
        text=(out/'run.md').read_text();assert 'Held-scale native-metric erasure' in text and 'metric-erased0.5 random0 J-lens' in text
        assert all(p.grad is None for m in models for p in m.parameters())
        print(f'PASS seed{seed}: actual6-case nonidentity-J BF16 pipeline;180 original rows/states/full generations exact+72 candidates, one-pass coverage, independent B-matrix correction, head/cast/raw-score and requested random matching. Tiny model only.',flush=True)
    finally:torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
