"""Saved-state/trace reconstruction, not independent neural replication. — PI/OpenAI"""
import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import torch
from transformers import AutoTokenizer

torch.set_num_threads(4)
root=Path(sys.argv[1]);p=json.loads((root/'pipeline.json').read_text());assert p['stage']=='completed'
manifest=json.loads((root/'manifest.json').read_text())
assert hashlib.sha256((root/'manifest.json').read_bytes()).hexdigest()==p['manifest_sha256']
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==p['source_sha256']
for name,sha in manifest['pins'].items():
    file=Path(name) if name.startswith('out/') else root/'inputs'/name
    assert hashlib.sha256(file.read_bytes()).hexdigest()==sha,name
config=json.loads((root/'inputs/data/dog_spider_joint_chat_v1.json').read_text())
prep_config=json.loads((root/'inputs'/config['donor_config']).read_text())
prepared=Path(p['prepared']);a=torch.load(prepared/'donors.pt',weights_only=True,map_location='cpu')
assert hashlib.sha256((prepared/'donors.pt').read_bytes()).hexdigest()==p['donor_sha256']
assert a['provenance']['config']==prep_config
literal=torch.load(config['previous_donor'],weights_only=True,map_location='cpu')
contexts=[torch.load(f,weights_only=True,map_location='cpu') for f in sorted((prepared/'donor-contexts').glob('*.pt'))]
assert len(contexts)==8 and [c['record'] for c in contexts]==a['provenance']['samples']
assert a['provenance']==json.loads((prepared/'donors.json').read_text())
tok=AutoTokenizer.from_pretrained(a['provenance']['model'],revision=a['provenance']['model_revision'],local_files_only=True)
def render(user):
    messages=[{'role':'system','content':config['system']},{'role':'user','content':user}]
    text=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
    ids=tok(text,add_special_tokens=False).input_ids
    before=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=False,enable_thinking=False,return_dict=False)
    assert ids[:len(before)]==before
    return text,ids,ids[len(before):]
max_mean_error=0.
for c in contexts:
    r=c['record'];text,ids,suffix=render(r['user_content'])
    assert ast.literal_eval(r['input_repr'])==text and r['token_ids']==ids and r['assistant_suffix_ids']==suffix
    assert r['user_content'] in [t.format(concept=r['concept']) for t in prep_config['templates']]
for concept in prep_config['concepts']:
    states=torch.stack([c['state'] for c in contexts if c['record']['concept']==concept])
    assert len(states)==4 and torch.equal(states,a['sample_states'][concept])
    error=(states.double().mean(0)-a['means'][concept].double()).abs()
    assert (error<=8*torch.finfo(torch.float32).eps*states.double().abs().mean(0)).all()
    max_mean_error=max(max_mean_error,float(error.max()))
delta=a['means']['spider']-a['means']['dog'];old=literal['means']['spider']-literal['means']['dog']
trace=[json.loads(s) for s in (root/'forward_trace.jsonl').read_text().splitlines()]
assert not any(r['grad_enabled'] for r in trace)
assert [r['sequence_length'] for r in trace if r['phase']=='generic-preparation']==[len(c['record']['token_ids']) for c in contexts]
all_rows=[];comparisons=[];canonical_random=None;relative_changes=[]
for group in p['case_runs']:
    case=group['case'];out=Path(group['run']);rows=json.loads((out/'interventions.json').read_text())
    assert list(rows)==['Base','role-aligned donor','previous literal-name donor','matched-random delta']
    sign=1 if case['reverse'] else -1
    vectors=torch.load(out/'applied_vectors.pt',weights_only=True,map_location='cpu')
    assert torch.equal(vectors['role-aligned donor'],sign*delta)
    assert torch.equal(vectors['previous literal-name donor'],sign*old)
    random=sign*vectors['matched-random delta']
    if canonical_random is None:canonical_random=random
    assert torch.equal(random,canonical_random) and torch.allclose(random.norm(),delta.norm(),atol=1e-6,rtol=1e-6)
    text,input_ids,suffix=render(case['user_content'])
    rendering=json.loads((out/'chat_rendering.json').read_text())
    assert rendering['prompt']==text and rendering['input_ids']==input_ids and rendering['assistant_suffix_ids']==suffix
    assert all(c['record']['assistant_suffix_ids']==suffix for c in contexts)
    calls=[r['sequence_length'] for r in trace if r['phase']==case['name']]
    assert calls==[c['sequence_length'] for r in rows.values() for c in r['coverage']]
    assert len(calls)==group['forward_calls']
    special=set(json.loads((out/'tokenizer_special_ids.json').read_text())['r2_excluded_ids'])
    for mode,r in rows.items():
        n=r['n_tokens'];assert 1<=n<=32 and n==len(r['token_ids'])==len(r['coverage'])
        assert [c['sequence_length'] for c in r['coverage']]==[len(input_ids)]+[1]*(n-1)
        assert r['coverage'][0]['positions']==1 and r['coverage'][0]['scale']==1
        assert all(c['positions']==1 and c['scale']==.25 for c in r['coverage'][1:])
        assert r['input_repr']==repr(text) and r['selected_prompt_token_ids']==[suffix[-1]]
        assert r['generation']==tok.decode(r['token_ids'])
        assert r['generation_scoring_text']==tok.decode(r['token_ids'],skip_special_tokens=True)
        assert n==32 or r['token_ids'][-1] in r['eos_token_ids']
        expected=case['base_expected'] if mode in ('Base','matched-random delta') else case['edited_expected']
        assert r['expected_properties']==expected
        states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True,map_location='cpu')
        update=torch.zeros_like(delta) if mode=='Base' else vectors[mode]
        requested=states[:,0]+update;requested[1:]=states[1:,0]+.25*(requested[1:]-states[1:,0])
        assert torch.equal(requested,states[:,1]) and torch.equal(requested.to(torch.bfloat16).float(),states[:,2])
        relative_changes.append({'case':case['name'],'condition':mode,'prefill_applied_relative_norm':float((states[0,2]-states[0,0]).norm()/states[0,0].norm())})
        assert math.isclose(r['answer_pair_mass'],r['p_answer0']+r['p_answer1'],abs_tol=1e-7)
        base=rows['Base'];shift=math.log(r['p_answer1']/r['p_answer0'])-math.log(base['p_answer1']/base['p_answer0'])
        assert abs(shift-r['answer_log_odds_shift'])<1e-6
        assert all(math.isclose(t['p'],math.exp(t['log_p']),rel_tol=1e-6) for t in r['top10'])
        ids=[t for t in r['token_ids'] if t not in special];bigrams=list(zip(ids,ids[1:]))
        repetition=1-len(set(bigrams))/len(bigrams) if bigrams else 0
        assert abs(repetition-r['r2'])<1e-12
        all_rows.append(r)
    comparisons.append({'case':case['name'],'all_conditions_same_token_ids':all(r['token_ids']==rows['Base']['token_ids'] for r in rows.values()),
        'base_text':rows['Base']['generation_scoring_text'],'base_matches_expected':rows['Base']['generation_scoring_text']=='; '.join(case['base_expected']),
        'primary_matches_target':rows['role-aligned donor']['generation_scoring_text']=='; '.join(case['edited_expected'])})
assert len(all_rows)==12 and len(trace)==8+sum(r['n_tokens'] for r in all_rows)==p['actual_forwards']
result={'signature':'PI/OpenAI','passed':True,'scope':'Hash/render/means, signed vectors, exact saved F32/BF16 updates, forward coverage, token decoding, scalar probabilities/repetition; not independent neural or semantic certification',
 'contexts':8,'conditions':12,'actual_forwards':len(trace),'generated_tokens':sum(r['n_tokens'] for r in all_rows),
 'max_float64_mean_error':max_mean_error,'donor_norm':float(delta.norm()),'literal_norm':float(old.norm()),'comparisons':comparisons,'relative_changes':relative_changes}
(root/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1),flush=True)
