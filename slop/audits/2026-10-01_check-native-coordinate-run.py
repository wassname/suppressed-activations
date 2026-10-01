"""Independent saved-state/native-weight checks; not a neural replay. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import sys

from safetensors import safe_open
import torch
from transformers import AutoTokenizer

torch.set_num_threads(4)
root=Path.cwd();master=Path(sys.argv[1]);meta=json.loads((master/'pipeline.json').read_text())
assert meta['stage']=='completed' and meta['raw_coordinate_exchange'] and meta['generic_prefills']==0
assert meta['actual_forwards']==meta['generated_tokens']<=384 and len(meta['case_runs'])==3
manifest=json.loads((master/'manifest.json').read_text())
for p,sha in manifest['pins'].items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==sha,p
snapshot=Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
index=json.loads((snapshot/'model.safetensors.index.json').read_text())['weight_map']
key='model.language_model.norm.weight'
with safe_open(snapshot/index[key],framework='pt',device='cpu') as f:gain=1+f.get_tensor(key).float()
key='model.language_model.embed_tokens.weight'
with safe_open(snapshot/index[key],framework='pt',device='cpu') as f:w=torch.cat([f.get_slice(key)[i:i+1] for i in (22466,6124)])
lens=Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt')
assert hashlib.sha256(lens.read_bytes()).hexdigest()=='1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e'
j=torch.load(lens,map_location='cpu',weights_only=True)['J'][15].double()
tok=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
assert [tok(s,add_special_tokens=False).input_ids for s in (' Sweden',' Japan')]==[[22466],[6124]]
reference=json.loads((root/meta['reference_master']/'pipeline.json').read_text())
max_request_error=max_coordinate_error=max_orthogonal_error=0.;n_states=0;summary=[];shared_random=None
for case_index,entry in enumerate(meta['case_runs']):
    run=Path(entry['run']);case=entry['case'];rows=json.loads((run/'interventions.json').read_text())
    assert list(rows)==['Base','raw J-coordinate exchange','raw plain-coordinate exchange','matched-random delta']
    prior=reference['case_runs'][case_index];assert prior['case']==case
    base=json.loads((Path(prior['run'])/'interventions.json').read_text())['Base']
    assert all(rows['Base'][k]==base[k] for k in ('token_ids','generation','input_repr','top10','prefill_readout'))
    inputs=torch.load(run/'basis_inputs.pt',weights_only=True,map_location='cpu')
    assert inputs['concept_ids']==[[22466],[6124]] and torch.equal(inputs['gain'],gain) and torch.equal(inputs['W_rows'],w)
    bases=torch.load(run/'coordinate_bases.pt',weights_only=True,map_location='cpu')
    expected_plain=(w.double()*gain.double()).T
    for key,expected in [('raw plain',expected_plain),('raw J',j.T@expected_plain)]:
        assert torch.allclose(bases[key]['vectors'].double(),expected,atol=1e-6,rtol=3e-6)
        assert torch.allclose(bases[key]['inverse'].double(),torch.linalg.pinv(expected),atol=1e-6,rtol=3e-6)
    random=torch.load(run/'random_direction.pt',weights_only=True,map_location='cpu')
    assert random.dtype==torch.float32 and abs(float(random.norm())-1)<1e-6
    if shared_random is not None:assert torch.equal(random,shared_random)
    shared_random=random
    baseline_states=torch.load(run/'base-states.pt',weights_only=True,map_location='cpu')
    for mode,row in rows.items():
        states=torch.load(run/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True,map_location='cpu')
        assert len(states)==row['n_tokens']==len(row['token_ids'])==len(row['coverage'])<=32
        assert row['generation']==tok.decode(row['token_ids'],skip_special_tokens=False)
        assert row['token_ids'][-1] in (248044,248046) and row['eos_token_ids']==[248044,248046]
        assert row['expected_properties']==(case['base_expected'] if mode in ('Base','matched-random delta') else case['edited_expected'])
        assert row['token_ids']==rows['Base']['token_ids'] and torch.equal(states[:,0],baseline_states[:,0])
        b=bases['raw plain' if mode=='raw plain-coordinate exchange' else 'raw J'];v=b['vectors'].double();inverse=torch.linalg.pinv(v)
        for step,(original,requested,applied) in enumerate(states):
            scale=.25 if step else 1.;h=original.double();c=h@inverse.T
            delta=(c.flip(-1)-c)@v.T
            if mode=='Base':delta=torch.zeros_like(delta)
            elif mode=='matched-random delta':delta=delta.norm(dim=-1,keepdim=True)*random.double()
            expected=h+scale*delta
            error=float((requested.double()-expected).abs().max());max_request_error=max(max_request_error,error)
            assert torch.allclose(requested.double(),expected,atol=1e-5,rtol=1e-5)
            assert torch.equal(applied,requested.to(torch.bfloat16).float())
            coverage=row['coverage'][step];assert coverage['scale']==scale and coverage['positions']==1
            if mode in ('raw J-coordinate exchange','raw plain-coordinate exchange'):
                expected_c=(1-scale)*c+scale*c.flip(-1)
                coordinate_error=float((requested.double()@inverse.T-expected_c).abs().max())
                max_coordinate_error=max(max_coordinate_error,coordinate_error);assert coordinate_error<1e-5
                d=requested.double()-h;orthogonal=float((d-(d@inverse.T)@v.T).norm())
                max_orthogonal_error=max(max_orthogonal_error,orthogonal);assert orthogonal<1e-5
            n_states+=1
        h,requested,applied=states[0].double()
        summary.append({'case':case['name'],'mode':mode,'generation':row['generation'],'tokens':row['n_tokens'],
            'before_coordinates':(h@inverse.T).flatten().tolist(),'requested_coordinates':(requested@inverse.T).flatten().tolist(),
            'applied_coordinates':(applied@inverse.T).flatten().tolist(),
            'requested_norm':float((requested-h).norm()),'applied_norm':float((applied-h).norm()),
            'relative_applied_norm':float((applied-h).norm()/h.norm()),
            'prefill_readout':row['prefill_readout'],'final_decode_readout':row['final_decode_readout']})
    assert entry['forward_calls']==sum(r['n_tokens'] for r in rows.values())
    assert not (run/'donors.pt').exists() and not (run/'clean_target_probe.json').exists()
events=[json.loads(s) for s in (master/'forward_trace.jsonl').read_text().splitlines()]
assert len(events)==n_states==meta['actual_forwards']==60 and not any(e['grad_enabled'] for e in events)
assert all(e['phase'] in {c['case']['name'] for c in meta['case_runs']} for e in events)
for entry in meta['case_runs']:
    run=Path(entry['run']);rows=json.loads((run/'interventions.json').read_text());ev=[e for e in events if e['phase']==entry['case']['name']]
    rendering=json.loads((run/'chat_rendering.json').read_text());offset=0
    for row in rows.values():
        n=row['n_tokens'];assert [e['sequence_length'] for e in ev[offset:offset+n]]==[len(rendering['input_ids'])]+[1]*(n-1);offset+=n
        assert row['selected_prompt_token_ids']==rendering['assistant_suffix_ids'][-1:]
result={'scope':'Saved states, pinned native rows/gain/J, reference tokens/top10/readouts, coverage. No independent neural replay or GPU RNG regeneration.',
        'states':n_states,'conditions':len(summary),'generic_prefills':0,'max_requested_element_error':max_request_error,
        'max_requested_coordinate_error':max_coordinate_error,'max_orthogonal_norm_error':max_orthogonal_error,
        'all_generations_equal_Base':True,'capital_changes':0,'currency_changes':0,'joint_changes':0,'country_cases':2,
        'arithmetic_preserved_per_mode':'1/1','unfinished_or_capped':0}
(master/'verification.json').write_text(json.dumps(result,indent=1)+'\n')
(master/'conditions_compact.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in summary))
print(json.dumps(result,indent=1),flush=True)
