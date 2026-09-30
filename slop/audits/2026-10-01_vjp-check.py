"""Real tiny-model derivative and intervention checks, not scientific evidence. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root=Path(__file__).resolve().parents[2]
entry=root/'scripts/english/08_jlens_one_pass.py'
g=runpy.run_path(str(entry))['main'].__globals__
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(),flush=True)

def config(vocab):
    return Qwen3_5TextConfig(vocab_size=vocab,hidden_size=32,intermediate_size=64,num_hidden_layers=32,
        num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
        linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=256,
        bos_token_id=None,eos_token_id=None,pad_token_id=0,
        rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,'mrope_interleaved':True,'mrope_section':[3,3,2]})

for seed in (0,1):
    torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(config(64)).eval().requires_grad_(False)
    ids=torch.tensor([[1,4,7,9,11,13]])
    sentinel=model.model.layers[15].register_forward_hook(lambda *args:None)
    gradient,state,logits=g['naming_vjp'](model,ids,15,2,[14,15])
    direction=gradient/gradient.norm(); values=[]
    for epsilon in (-.001,.001):
        def perturb(_module,_args,output):
            changed=output.clone();changed[:,2]+=epsilon*direction
            return changed
        with g['layer_hooks'](model.model.layers,{15:perturb}):
            z=model(ids,use_cache=False).logits[0,-1]
            values.append(float(z[15]-z[14]))
    finite_difference=(values[1]-values[0])/.002
    derivative=float(gradient@direction)
    assert abs(finite_difference-derivative)<2e-4+0.02*abs(derivative),(finite_difference,derivative)
    assert sentinel.id in model.model.layers[15]._forward_hooks
    assert sum(len(b._forward_hooks) for b in model.model.layers)==1
    assert all(p.grad is None for p in model.parameters()) and not torch.is_grad_enabled()
    sentinel.remove()
    print(f'PASS float32 hybrid Qwen seed{seed}: earlier-position gradient through suffix, finite difference={finite_difference:.8g}, autograd={derivative:.8g}, hooks/parameters/grad context preserved',flush=True)

tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
torch.manual_seed(0)
model=Qwen3_5ForCausalLM(config(len(tok))).to(torch.bfloat16).eval().requires_grad_(False)
templates=json.loads((root/'data/dog_spider_donors_pronoun_v2.json').read_text())
name_ids=[tok(s,add_special_tokens=False).input_ids[0] for s in (' dog',' spider')]
gradients=[]
for concept in templates['concepts']:
    for template in templates['templates']:
        prefix=template.format(concept=concept)
        ids=tok(prefix+' is called a',add_special_tokens=False,return_tensors='pt').input_ids
        pos=len(tok(prefix,add_special_tokens=False).input_ids)-1
        gradients.append(g['naming_vjp'](model,ids,15,pos,name_ids)[0])
mean=torch.stack(gradients).mean(0); fixture_delta=.5*mean/mean.norm()
print('WARNING: synthetic donors aligned to the tiny-model gradient for positive-path coverage; not pretrained calibration or a method result',flush=True)
with tempfile.TemporaryDirectory(dir=root/'.local') as directory:
    tmp=Path(directory);(tmp/'data').mkdir()
    (tmp/'data/dog_spider_donors_pronoun_v2.json').write_bytes((root/'data/dog_spider_donors_pronoun_v2.json').read_bytes())
    donor=tmp/'donors.pt'
    torch.save({'means':{'dog':torch.zeros(32),'spider':fixture_delta},'provenance':{'model_revision':g['q'].REVISION,'block_index':15,'config':templates}},donor)
    preparation=json.loads((root/'data/dog_spider_vjp_v1.json').read_text())
    preparation['donor_sha256']=hashlib.sha256(donor.read_bytes()).hexdigest()
    config_path=tmp/'preparation.json';config_path.write_text(json.dumps(preparation))
    lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=lambda *a,**kw:model)
    g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    g['ROOT']=tmp;model.cuda=lambda *a,**kw:model
    original_cuda=torch.Tensor.cuda;original_mask=g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*a,**kw:self
    g['q'].prompt_word_mask=lambda prompt,vocab,device:original_mask(prompt,vocab,'cpu')
    before={k:v.clone() for k,v in model.named_parameters()}
    events=[];handle=model.register_forward_pre_hook(lambda *_:events.append(torch.is_grad_enabled()))
    try:
        prepared=g['main'](prepare_vjp_json=config_path,donor_checkpoint=donor)
        assert events==[True]*8,events
        artifact=torch.load(prepared/'vjp.pt',weights_only=True)
        assert artifact['provenance']['passed'] and torch.allclose(artifact['delta'],fixture_delta,atol=1e-5)
        contexts=[torch.load(f,weights_only=True) for f in sorted((prepared/'vjp-contexts').glob('*.pt'))]
        assert len(contexts)==8 and torch.equal(torch.stack([r['gradient'] for r in contexts]),artifact['gradients'])
        total=0
        for relation,count in (('legs',3),('skeleton_body',3),('arithmetic_control',2)):
            g['ROOT']=tmp/relation;events.clear()
            out=g['main'](vjp_checkpoint=prepared/'vjp.pt',reverse=True,prompt_positions=1,decode_scale=.25,relation=relation)
            rows=json.loads((out/'interventions.json').read_text());assert len(rows)==count
            vectors=torch.load(out/'applied_vectors.pt',weights_only=True)
            assert torch.allclose(vectors['offline naming VJP'].norm(),vectors['matched-random delta'].norm(),atol=1e-6)
            assert len(events)==sum(r['n_tokens'] for r in rows.values()) and not any(events)
            for mode,row in rows.items():
                n=row['n_tokens'];assert n==32 and len(row['coverage'])==n
                assert row['coverage'][0]['positions']==1
                assert all(c['positions']==c['sequence_length']==1 for c in row['coverage'][1:])
                states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True)
                delta=torch.zeros(32) if mode=='Base' else vectors[mode]
                scale=torch.tensor([1]+[.25]*(n-1))[:,None,None,None]
                assert torch.allclose(states[:,1]-states[:,0],scale*delta,atol=1e-6)
                assert torch.equal(states[:,2],states[:,1].to(torch.bfloat16).float())
                if relation=='arithmetic_control':assert row['expected_answer']=='4'
            total+=len(rows)
        assert total==8 and all(torch.equal(before[k],v) for k,v in model.named_parameters())
        assert all(p.grad is None for p in model.parameters())
        assert all(not b._forward_hooks for b in model.model.layers)
        print('PASS BF16 full main:8 offline backwards,8 generation trajectories, no eval gradients/extra forward pass, unchanged weights, identical frozen vector/schedule, matched random,32-token coverage and exact post-cast states; arithmetic expects4',flush=True)
        g['ROOT']=tmp
        negative_donor=tmp/'negative-donor.pt'
        negative_data=torch.load(donor,weights_only=True);negative_data['means']['spider']=-fixture_delta
        torch.save(negative_data,negative_donor)
        negative_config=dict(preparation);negative_config['donor_sha256']=hashlib.sha256(negative_donor.read_bytes()).hexdigest()
        negative_path=tmp/'negative-config.json';negative_path.write_text(json.dumps(negative_config))
        negative_out=tmp/'negative';negative_out.mkdir()
        try:
            g['prepare_vjp'](model,tok,15,negative_path,negative_donor,negative_out)
            raise RuntimeError('negative coefficient unexpectedly accepted')
        except AssertionError as error:
            assert 'no sign/dose rescue' in str(error)
        rejected=torch.load(negative_out/'vjp.pt',weights_only=True)
        assert not rejected['provenance']['passed'] and rejected['provenance']['coefficient']<0
        assert len(list((negative_out/'vjp-contexts').glob('*.pt')))==8
        original_vjp=g['naming_vjp'];n_completed=0
        def interrupted(*args):
            global n_completed
            if n_completed==3:raise RuntimeError('fixture interruption after three contexts')
            value=original_vjp(*args);n_completed+=1;return value
        g['naming_vjp']=interrupted
        interrupted_out=tmp/'interrupted';interrupted_out.mkdir()
        try:
            g['prepare_vjp'](model,tok,15,config_path,donor,interrupted_out)
            raise AssertionError('fixture interruption missing')
        except RuntimeError as error:
            assert str(error)=='fixture interruption after three contexts'
        finally:g['naming_vjp']=original_vjp
        partial=[torch.load(f,weights_only=True) for f in sorted((interrupted_out/'vjp-contexts').glob('*.pt'))]
        assert len(partial)==3 and all(torch.equal(r['gradient'],artifact['gradients'][i]) for i,r in enumerate(partial))
        assert not (interrupted_out/'vjp.pt').exists()
        assert all(not b._forward_hooks for b in model.model.layers)
        print('PASS negative coefficient rejected without rescue; all8 context artifacts retained; interruption after3 preserves exactly3 gradients/states/records without a completed checkpoint',flush=True)
    finally:
        handle.remove();torch.Tensor.cuda=original_cuda;g['q'].prompt_word_mask=original_mask
print('PASS tiny CPU implementation checks only; full-size backward capacity and scientific behavior untested',flush=True)
