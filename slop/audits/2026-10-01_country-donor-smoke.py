"""Real tiny-Qwen country trajectories; no pretrained scientific claims. — PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

root=Path.cwd();torch.set_num_threads(4);torch.set_grad_enabled(False)
entry=root/'scripts/english/08_jlens_one_pass.py';g=runpy.run_path(str(entry))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-config','exec'))
tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(),flush=True)
for seed in (0,1):
    tmp=Path(tempfile.mkdtemp(prefix=f'country-smoke-{seed}-',dir=root/'.local'));print('retained fixture='+str(tmp),flush=True)
    cfg=config(len(tok));cfg.eos_token_id=248044;torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(cfg).to(torch.bfloat16).eval().requires_grad_(False)
    weights={k:v.clone() for k,v in model.named_parameters()};defaults=model.generation_config.to_dict()
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=lambda *a,**kw:model)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self;model.cuda=lambda *a,**kw:model
    g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    events=[];observed=[]
    counter=model.register_forward_pre_hook(lambda *_:events.append(torch.is_grad_enabled()))
    sentinel=model.model.layers[15].register_forward_hook(lambda _m,_a,out:observed.append(out[0,-1].detach().float().clone()))
    try:
        preparation=root/'data/sweden_japan_donors_chat_v1.json';evaluation=json.loads((root/'data/sweden_japan_joint_chat_v1.json').read_text())
        evaluation['donor_config']=str(preparation);cases=tmp/'cases.json';cases.write_text(json.dumps(evaluation))
        g['ROOT']=tmp/'prep';prepared=g['main'](prepare_donors_json=preparation)
        assert len(events)==8 and not any(events)
        donor=torch.load(prepared/'donors.pt',weights_only=True)
        contexts=[torch.load(p,weights_only=True) for p in sorted((prepared/'donor-contexts').glob('*.pt'))]
        assert all(torch.equal(c['state'],h) for c,h in zip(contexts,observed,strict=True))
        for concept in ('Sweden','Japan'):
            samples=torch.stack([c['state'] for c in contexts if c['record']['concept']==concept])
            assert torch.equal(samples,donor['sample_states'][concept]) and torch.equal(samples.mean(0),donor['means'][concept])
        base_delta=donor['means']['Sweden']-donor['means']['Japan'];prior=None
        hooks=[dict(b._forward_hooks) for b in model.model.layers]
        for index,case in enumerate(evaluation['cases']):
            g['ROOT']=tmp/case['name'];events.clear();observed.clear()
            out=g['main'](donor_checkpoint=prepared/'donors.pt',chat_causal_json=cases,causal_case_index=index,
                reverse=case['reverse'],prompt_positions=1,decode_scale=.25,relation=case['relation'])
            rows=json.loads((out/'interventions.json').read_text());vectors=torch.load(out/'applied_vectors.pt',weights_only=True)
            assert list(rows)==['Base','role-aligned donor','matched-random delta']
            sign=1 if case['reverse'] else -1
            assert torch.equal(vectors['role-aligned donor'],sign*base_delta)
            assert torch.allclose(vectors['matched-random delta'].norm(),base_delta.norm(),atol=1e-6)
            if prior is not None:assert all(torch.equal(sign*v,prior[k]) for k,v in vectors.items())
            prior={k:sign*v for k,v in vectors.items()}
            assert len(events)==sum(r['n_tokens'] for r in rows.values()) and not any(events)
            offset=0
            for mode,row in rows.items():
                n=row['n_tokens'];assert 1<=n<=32 and len(row['coverage'])==n
                assert row['selected_prompt_token_ids']==[row['assistant_suffix_ids'][-1]]
                assert row['eos_token_ids']==sorted({248044,tok.eos_token_id})
                expected=case['edited_expected'] if mode=='role-aligned donor' else case['base_expected']
                assert row['expected_properties']==expected
                assert row['answer_token_sequences']==[tok(a,add_special_tokens=False).input_ids for a in ('Stockholm','Tokyo')]
                assert all(len(a)>1 for a in row['answer_token_sequences'])
                assert row['answer_first_token_strings']==[tok.decode([a[0]]) for a in row['answer_token_sequences']]
                assert row['generation_scoring_text']==tok.decode(row['token_ids'],skip_special_tokens=True)
                states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True)
                assert torch.equal(states[:,2,0,0],torch.stack(observed[offset:offset+n]));offset+=n
                delta=torch.zeros(32) if mode=='Base' else vectors[mode]
                for j,(original,requested,applied) in enumerate(states):
                    proposed=original+delta
                    if j:proposed=original+.25*(proposed-original)
                    assert torch.equal(requested,proposed) and torch.equal(applied,proposed.to(torch.bfloat16).float())
                    c=row['coverage'][j];assert c['positions']==1 and c['scale']==(.25 if j else 1)
                if case['relation']=='arithmetic_control':assert row['expected_answer']==('control' if mode=='matched-random delta' else '4')
            report=(out/'run.md').read_text()
            assert 'first tokens only, not full multi-token answers' in report
            assert 'Previously chosen spider/dog' not in report and 'Twelve conditions' not in report
            assert '9 conditions' in report and 'No previous-donor comparator' in report
        assert all(torch.equal(weights[k],v) for k,v in model.named_parameters())
        assert all(p.grad is None for p in model.parameters()) and defaults==model.generation_config.to_dict()
        assert hooks==[dict(b._forward_hooks) for b in model.model.layers]
        print(f'PASS seed{seed}:8 generic prefills,9 trajectories; correct signed country means/random controls; exact requested/BF16/downstream states, suffix/coverage/EOS, multi-token probability scope and arithmetic expectations; unchanged weights/hooks/defaults. No pretrained result.',flush=True)
    finally:
        counter.remove();sentinel.remove();torch.Tensor.cuda=cuda;g['q'].prompt_word_mask=mask
