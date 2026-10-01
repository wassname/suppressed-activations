"""Real tiny-Qwen native coordinate exchange and direct Base comparison. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5ForCausalLM, Qwen3_5TextConfig

root=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
entry=root/'scripts/english/08_jlens_one_pass.py';g=runpy.run_path(str(entry))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(),flush=True)
for seed in (0,1):
    tmp=Path(tempfile.mkdtemp(prefix=f'native-coordinate-{seed}-',dir=root/'.local'));print('fixture='+str(tmp),flush=True)
    cfg=config(len(tok));cfg.eos_token_id=248044;torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    model.model.norm.weight.copy_(torch.linspace(-.1,.2,32).to(torch.bfloat16))
    weights={k:v.clone() for k,v in model.named_parameters()};defaults=model.generation_config.to_dict()
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32)+.1*torch.randn(32,32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=lambda *a,**kw:model)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self;model.cuda=lambda *a,**kw:model
    g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    events=[];observed=[]
    counter=model.register_forward_pre_hook(lambda *_:events.append(torch.is_grad_enabled()))
    sentinel=model.model.layers[15].register_forward_hook(lambda _m,_a,out:observed.append(out[0,-1].detach().float().clone()))
    hooks=[dict(b._forward_hooks) for b in model.model.layers]
    discriminated_partial=0
    try:
        evaluation=json.loads((root/'data/sweden_japan_joint_chat_v1.json').read_text())
        evaluation['donor_config']=str(root/'data/sweden_japan_donors_chat_v1.json')
        cases=tmp/'cases.json';cases.write_text(json.dumps(evaluation))
        system=json.loads(Path(evaluation['donor_config']).read_text())['system']
        for index,case in enumerate(evaluation['cases']):
            prompt,suffix=g['native_prompt'](tok,system,case['user_content'])
            ids=tok(prompt,return_tensors='pt',add_special_tokens=False).input_ids
            baseline=model.generate(ids,max_new_tokens=32,do_sample=False,repetition_penalty=1.,use_cache=True,
                eos_token_id=sorted({248044,tok.eos_token_id}))[0,ids.shape[1]:].tolist()
            events.clear();observed.clear();g['ROOT']=tmp/case['name']
            out=g['main'](raw_coordinate_exchange=True,chat_causal_json=cases,causal_case_index=index,
                reverse=case['reverse'],relation=case['relation'],prompt_positions=1,decode_scale=.25)
            rows=json.loads((out/'interventions.json').read_text())
            assert list(rows)==['Base','raw J-coordinate exchange','raw plain-coordinate exchange','matched-random delta']
            assert rows['Base']['token_ids']==baseline
            assert not (out/'donors.pt').exists() and not (out/'clean_target_probe.json').exists()
            bases=torch.load(out/'coordinate_bases.pt',weights_only=True)
            random=torch.load(out/'random_direction.pt',weights_only=True)
            assert abs(float(random.norm())-1)<1e-6
            assert len(events)==sum(r['n_tokens'] for r in rows.values()) and not any(events)
            offset=0
            for mode,row in rows.items():
                n=row['n_tokens'];assert 1<=n<=32 and len(row['coverage'])==n
                assert row['selected_prompt_token_ids']==[suffix[-1]] and row['assistant_suffix_ids']==suffix
                assert row['eos_token_ids']==sorted({248044,tok.eos_token_id})
                assert row['expected_properties']==(case['base_expected'] if mode in ('Base','matched-random delta') else case['edited_expected'])
                assert row['answer_token_sequences']==[tok(a,add_special_tokens=False).input_ids for a in ('Stockholm','Tokyo')]
                states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True)
                assert len(states)==n and torch.equal(states[:,2,0,0],torch.stack(observed[offset:offset+n]));offset+=n
                b=bases['raw plain' if mode=='raw plain-coordinate exchange' else 'raw J'];v=b['vectors'].double();inverse=torch.linalg.pinv(v)
                for step,(original,requested,applied) in enumerate(states):
                    scale=.25 if step else 1.;h=original.double();c=h@inverse.T
                    delta=(c.flip(-1)-c)@v.T
                    if mode=='Base':delta=torch.zeros_like(delta)
                    elif mode=='matched-random delta':delta=delta.norm(dim=-1,keepdim=True)*random.double()
                    expected=h+scale*delta
                    assert torch.allclose(requested.double(),expected,atol=1e-5,rtol=1e-5),(seed,index,mode,step)
                    assert torch.equal(applied,requested.to(torch.bfloat16).float())
                    coverage=row['coverage'][step];assert coverage['scale']==scale and coverage['positions']==1
                    if step and mode in ('raw J-coordinate exchange','raw plain-coordinate exchange') and float((c-c.flip(-1)).abs().max())>.01:
                        assert not torch.allclose(requested.double()@inverse.T,c.flip(-1),atol=1e-4,rtol=1e-4)
                        discriminated_partial+=1
            report=(out/'run.md').read_text();assert 'raw_coordinate_exchange: true' in report and 'No donor forward' in report
            assert 'first tokens only, not full multi-token answers' in report
        assert discriminated_partial>0
        assert all(torch.equal(weights[k],v) for k,v in model.named_parameters())
        assert all(p.grad is None for p in model.parameters()) and defaults==model.generation_config.to_dict()
        assert hooks==[dict(b._forward_hooks) for b in model.model.layers]
        print(f'PASS seed{seed}:12 real tiny trajectories; unhooked Base parity; no donor/target-prefill; independent float64 raw-coordinate/partial-decode/random and BF16 reconstruction; all coverage/suffix/EOS/properties; weights/hooks unchanged; partial-vs-full discriminators={discriminated_partial}.',flush=True)
    finally:
        counter.remove();sentinel.remove();torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
