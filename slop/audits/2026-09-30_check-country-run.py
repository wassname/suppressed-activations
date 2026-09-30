"""CPU reconstruction of the fixed country assay; no inference or semantic certification. -- PI/OpenAI"""
import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import torch
from safetensors import safe_open
from tokenizers import Tokenizer

torch.set_num_threads(1)
root=Path(sys.argv[1]).resolve()
source_sha='02b5a0957ad8d3913603217d901577956eb48fccc0fc18e1b512e8a5e1c5a498'
launcher_sha='c3077e949fde59752a8a9f786ebaaca5d658bfc32f0b215ba5b6f5caf8941e4a'
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==source_sha
assert hashlib.sha256((root/'launcher.py').read_bytes()).hexdigest()==launcher_sha
pipeline=json.loads((root/'pipeline.json').read_text())
assert pipeline['status']=='complete' and pipeline['source_sha256']==source_sha
assert [r['relation'] for r in pipeline['runs']]==['capital','currency']
assert pipeline['primary']=='raw J-coordinate exchange' and pipeline['generated_token_cap']==320
helpers=json.loads((root/'helper_sha256.json').read_text())
for p,digest in helpers.items():
    assert hashlib.sha256((root/'helpers'/p).read_bytes()).hexdigest()==digest
model_dir=Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
tok=Tokenizer.from_file(str(model_dir/'tokenizer.json'))
config=json.loads((model_dir/'config.json').read_text())
assert config['tie_word_embeddings'] and config['text_config']['tie_word_embeddings']
index=json.loads((model_dir/'model.safetensors.index.json').read_text())['weight_map']
key='model.language_model.norm.weight'
with safe_open(model_dir/index[key],framework='pt',device='cpu') as f:
    gain=1.+f.get_tensor(key).float()
key='model.language_model.embed_tokens.weight'
with safe_open(model_dir/index[key],framework='pt',device='cpu') as f:
    weight_rows=torch.cat([f.get_slice(key)[i:i+1] for i in (14898,6124)])
lens_path=Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt')
with lens_path.open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()=='1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e'
lens=torch.load(lens_path,map_location='cpu',weights_only=True)['J'][15].float()
raw_plain=(weight_rows.float()*gain).T
raw_j=(raw_plain.T @ lens).T
expected_ids={' Italy':[14898],' Japan':[6124],' Rome':[21047],' Tokyo':[25358],' euro':[17146],' yen':[55421]}
assert json.loads((root/'token_preflight.json').read_text())==expected_ids
assert {s:tok.encode(s,add_special_tokens=False).ids for s in expected_ids}==expected_ids
prompts={
    'capital':('Fact: The capital of the country shaped like a boot is','Fact: The capital of the country known as the Land of the Rising Sun is',(' Rome',' Tokyo')),
    'currency':('Fact: The currency used in the country shaped like a boot is','Fact: The currency used in the country known as the Land of the Rising Sun is',(' euro',' yen'))}
modes={'Base':'raw J','raw J-coordinate exchange':'raw J','unit J-coordinate exchange':'unit J',
       'raw plain-coordinate exchange':'raw plain','matched-random delta':'raw J'}
report=[]; direction_reference=None
max_state_error=0.
for run in pipeline['runs']:
    out=Path(run['path']); relation=run['relation']; prompt,target,answers=prompts[relation]
    assert (out/'source.py').read_bytes()==(root/'source.py').read_bytes()
    assert json.loads((out/'helper_sha256.json').read_text())==helpers
    inputs=torch.load(out/'basis_inputs.pt',map_location='cpu',weights_only=True)
    assert inputs['concept_ids']==[[14898],[6124]] and torch.equal(inputs['gain'],gain)
    assert torch.equal(inputs['W_rows'],weight_rows) and torch.equal(inputs['raw_plain'],raw_plain)
    assert torch.allclose(inputs['raw_J'],raw_j,atol=2e-5,rtol=2e-5)
    bases=torch.load(out/'coordinate_bases.pt',map_location='cpu',weights_only=True)
    assert set(bases)=={'raw J','unit J','raw plain'}
    assert torch.equal(bases['raw J']['vectors'],inputs['raw_J'])
    assert torch.equal(bases['raw plain']['vectors'],inputs['raw_plain'])
    assert torch.allclose(bases['unit J']['vectors'],inputs['raw_J']/inputs['raw_J'].norm(dim=0),atol=1e-7,rtol=1e-6)
    inverses={}
    for name,b in bases.items():
        v=b['vectors'].double(); singular=torch.linalg.svdvals(v)
        tolerance=torch.finfo(torch.float32).eps*max(v.shape)*singular[0]
        assert singular[-1]>tolerance
        assert math.isclose(b['rank_tolerance'],float(tolerance),rel_tol=1e-10)
        assert torch.allclose(torch.tensor(b['singular_values'],dtype=torch.float64),singular,atol=1e-9,rtol=1e-9)
        inverse=torch.linalg.lstsq(v,torch.eye(v.shape[0],dtype=torch.float64),driver='gelsd').solution
        assert torch.allclose(b['inverse'].double(),inverse,atol=1e-6,rtol=1e-4)
        inverses[name]=inverse
    direction=torch.load(out/'random_direction.pt',map_location='cpu',weights_only=True).double()
    assert abs(float(direction.norm())-1)<1e-6
    if direction_reference is not None:
        assert torch.equal(direction,direction_reference)
    direction_reference=direction
    conditions=json.loads((out/'interventions.json').read_text()); assert list(conditions)==list(modes)
    ids=tok.encode(prompt,add_special_tokens=False).ids
    special=set(json.loads((out/'tokenizer_special_ids.json').read_text())['r2_excluded_ids'])
    base=conditions['Base']; base_before=torch.load(out/'base-states.pt',map_location='cpu',weights_only=True)[0,0]
    for mode,basis_name in modes.items():
        r=conditions[mode]; n=r['n_tokens']; coverage=r['coverage']
        assert 0<n<=32 and len(coverage)==len(r['token_ids'])==n
        assert ast.literal_eval(r['input_repr'])==prompt
        assert tok.decode(r['token_ids'],skip_special_tokens=False)==r['generation']
        assert r['selected_prompt_token_ids']==ids[-1:]
        assert r['answer_token_ids']==[expected_ids[a][0] for a in answers]
        assert [r['answer_0'],r['answer_1']]==list(answers) and r['coordinate_kind']==basis_name
        assert coverage[0]['positions']==1 and coverage[0]['sequence_length']==len(ids)
        assert all(c['positions']==1 and c['sequence_length']==1 for c in coverage[1:])
        assert all(c['scale']==1 for c in coverage)
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),map_location='cpu',weights_only=True)
        assert states.shape==(n,3,1,1,2560) and torch.isfinite(states).all()
        before,requested,applied=(states[:,i].double() for i in range(3))
        assert torch.equal(states[0,0],base_before)
        v=bases[basis_name]['vectors'].double(); inverse=inverses[basis_name]
        c=before@inverse.T
        exchanged=before+(c.flip(-1)-c)@v.T
        if mode=='Base':
            expected=before
        elif mode=='matched-random delta':
            expected=before+(exchanged-before).norm(dim=-1,keepdim=True)*direction
        else:
            expected=exchanged
        error=float((requested-expected).abs().max()); max_state_error=max(max_state_error,error)
        assert torch.allclose(requested,expected,atol=3e-5,rtol=3e-5),(relation,mode,error)
        assert torch.equal(applied,requested.to(torch.bfloat16).double())
        for i,call in enumerate(coverage):
            h=before[i,0,0]; new=applied[i,0,0]; req=requested[i,0,0]
            assert call['basis']==basis_name
            for key,value in (('edit_basis_coordinates_before',h@inverse.T),('edit_basis_coordinates_after',new@inverse.T),
                              ('raw_J_pair_before',h@inputs['raw_J'].double()),('raw_J_pair_after',new@inputs['raw_J'].double())):
                assert torch.allclose(torch.tensor(call[key],dtype=torch.float64),value,atol=2e-5,rtol=2e-4),(mode,i,key)
            for key,value in (('requested_delta_norm',(req-h).norm()),('applied_delta_norm',(new-h).norm()),
                              ('relative_delta_norm',(req-h).norm()/h.norm()),('applied_relative_delta_norm',(new-h).norm()/h.norm())):
                assert math.isclose(call[key],float(value),abs_tol=2e-5,rel_tol=2e-5),(mode,i,key)
        p0,p1=r['p_answer0'],r['p_answer1']; b0,b1=base['p_answer0'],base['p_answer1']
        assert min(p0,p1,b0,b1)>0,'Probability underflow: saved log probabilities are required for independent odds reconstruction'
        shift=math.log(p1)-math.log(p0)-math.log(b1)+math.log(b0)
        assert math.isclose(shift,r['answer_log_odds_shift'],abs_tol=2e-5)
        assert math.isclose(p0+p1,r['answer_pair_mass'],abs_tol=1e-7,rel_tol=1e-6)
        kept=[t for t in r['token_ids'] if t not in special]; bigrams=list(zip(kept,kept[1:]))
        repetition=1-len(set(bigrams))/len(bigrams) if bigrams else 0.
        assert r['r2']==repetition
        assert all(math.isfinite(t['log_p']) and math.isclose(math.exp(t['log_p']),t['p'],abs_tol=1e-7,rel_tol=1e-5) for t in r['top10'])
        assert len(r['top10'])==10 and all(a['log_p']>=b['log_p'] for a,b in zip(r['top10'],r['top10'][1:]))
    primary_norm=conditions['raw J-coordinate exchange']['coverage'][0]['requested_delta_norm']
    random_norm=conditions['matched-random delta']['coverage'][0]['requested_delta_norm']
    assert math.isclose(primary_norm,random_norm,rel_tol=1e-5,abs_tol=1e-5)
    probe=json.loads((out/'clean_target_probe.json').read_text())
    assert ast.literal_eval(probe['input_repr'])==target
    h=torch.load(out/'target_state.pt',map_location='cpu',weights_only=True).double()
    target_coordinates=h@inverses['raw J'].T
    assert torch.allclose(torch.tensor(probe['raw_J_coordinates'],dtype=torch.float64),target_coordinates,atol=1e-5,rtol=1e-4)
    assert run['n_tokens']==sum(r['n_tokens'] for r in conditions.values())
    report.append({'relation':relation,'n_tokens':run['n_tokens'],'n_conditions':5,
        'source_coordinates':(base_before[0,0].double()@inverses['raw J'].T).tolist(),
        'target_coordinates':target_coordinates.tolist(),
        'primary_exceeds_random_bare_log_odds':conditions['raw J-coordinate exchange']['answer_log_odds_shift']>conditions['matched-random delta']['answer_log_odds_shift']})
assert sum(r['n_tokens'] for r in report)<=320
result={'author':'PI/OpenAI','status':'PASS pinned parameter/basis reconstruction, local edit math/casting/coverage and saved scalar metrics',
    'max_requested_state_error':max_state_error,'runs':report,
    'limits':'No model inference. Probabilities/top10 optimality and observer readouts are not independently recomputed. No complete transformer-call hardware trace; timing/no-feedback claims rely on source plus CPU instrumentation. Seed0 identity relies on source; saved direction equality is checked. Semantic coherence and hidden-concept transfer require separate review.'}
(root/'verification.json').write_text(json.dumps(result,indent=1))
print(json.dumps(result,indent=1),flush=True)
