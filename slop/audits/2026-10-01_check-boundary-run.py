"""2720 saved-artifact reconstruction and posthoc leak diagnosis; no inference. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import re
import sys

import torch
from transformers import AutoTokenizer


torch.set_num_threads(4)
master=Path(sys.argv[1])
load=lambda p: json.loads(p.read_text())
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
p=load(master/'pipeline.json');run=Path(p['run']);manifest=load(master/'manifest.json')
assert p['stage']=='completed' and sha(master/'manifest.json')==p['manifest_sha256']
assert sha(master/'source.py')==sha(run/'source.py')==p['source_sha256']
for name,digest in manifest['pins'].items():assert sha(master/'inputs'/name)==digest,name
data=load(master/'inputs/data/english_boundary_readout_v1.json')
assert load(run/'cases.json')==data and len(data['cases'])==6
traces=load(run/'generation_traces.json');rows=load(run/'readout.json')
index={(r['case_index'],r['method']):r for r in rows};assert len(rows)==len(index)==180
states=torch.load(run/'prefill_positions.pt',map_location='cpu',weights_only=True)
last=torch.load(run/'prefill.pt',map_location='cpu',weights_only=True)
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
vocab=[tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(248320)))]
norm=[t.strip().lower() for t in vocab]
exclusions=load(run/'input_prefix_exclusions.json')

def ids(words,minimums=None):
    rules=list(zip(words,minimums,strict=True)) if minimums is not None else [(w,3) for w in words]
    return {i for i,t in enumerate(norm) if any(len(t)>=min(n,len(w)) and w.lower().startswith(t) for w,n in rules)}

def rank(z,labels):
    if not labels:return 10**9
    best=z[list(labels)].max()
    return int((z>best).sum()) if torch.isfinite(best) else 10**9

# Observed examples fixed before inspecting numeric scores; not new labels/masks. — PI/OpenAI
probes={0:['january','一月','-month','月份','december'],1:['tuesday','thursday','-day','次日'],
        2:['winter','冬季','冬天','寒冬','autumn','fall'],
        3:['red',':red','_red','红色','红色的','poisoning','poisonous','apple','apples'],
        4:['nu','nuage','cloud'],5:['wol','wolke','cloud','french','法语']}
expected_lengths=[];checked=0;max_auc_error=0;diagnosis=[];mask_nulls=[];point_indices=[]
for i,(case,trace) in enumerate(zip(data['cases'],traces,strict=True)):
    prompt=tok.apply_chat_template([{'role':'user','content':case['prompt']}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
    assert trace['prompt']==prompt
    input_ids=tok(prompt,add_special_tokens=False).input_ids
    generated=trace['token_ids'];assert 1<=len(generated)<=32
    assert tok.decode(generated)==trace['decoded_verbatim'] and tok.decode(generated,skip_special_tokens=True)==trace['scoring_text']
    assert trace['generation_overrides']=={'max_new_tokens':32,'do_sample':False,'use_cache':True,'eos_token_id':[248044,248046]}
    assert trace['stopped_on_eos']==(generated[-1] in (248044,248046))
    lengths=[len(input_ids)]+[1]*(len(generated)-1);expected_lengths+=lengths
    assert set(trace['coverage'])=={'24','27','32'} and all(v==lengths for v in trace['coverage'].values())
    for layer in (24,27,32):
        assert states[i][layer].shape==(len(input_ids),2560) and torch.isfinite(states[i][layer]).all()
        assert torch.equal(states[i][layer][-1],last[i][layer])
    meta=load(run/f'boundary_readouts/{i:03d}.json')
    closed=tok.apply_chat_template([{'role':'user','content':case['prompt']}],tokenize=True,add_generation_prompt=False,enable_thinking=False,return_dict=False)
    header=tok('<|im_start|>user\n',add_special_tokens=False).input_ids
    assert input_ids[:len(closed)]==closed and input_ids[:len(header)]==header
    assert meta['input_ids']==input_ids and meta['positions']=={'boundary':len(closed)-1,'preclue':len(header)-1}
    assert meta['consumed_prefixes']=={name:tok.decode(input_ids[:pos+1]) for name,pos in meta['positions'].items()}
    assert meta['output_direction_id']==generated[0] and meta['final_scores_exact']
    point_indices.append(meta['positions'])
    words=set(re.findall(r'\w+',prompt.lower()));legacy=words|{w[:n] for w in words for n in range(3,len(w)+1)}
    prompt_mask=torch.tensor([bool(t) and t in legacy for t in norm])
    extensions={t:sorted(w for w in words if len(w)>=3 and value.startswith(w)) for t,value in enumerate(norm) if value not in legacy}
    extensions={t:w for t,w in extensions.items() if w}
    assert {r['id']:r['originating_words'] for r in exclusions[i]['added_input_exclusions']}==extensions
    extension_mask=torch.zeros(248320,dtype=torch.bool);extension_mask[list(extensions)]=True
    w=norm[generated[0]]
    output_mask=torch.tensor([bool(t) and (t==w or t in {w[:n] for n in range(3,len(w))} or ((len(w)>=2 or '\u4e00'<=w<='\u9fff') and t.startswith(w))) for t in norm])
    output_mask[generated[0]]=True;full_mask=prompt_mask|output_mask|extension_mask
    final_raw=torch.load(run/f'unmasked_readout_scores/{i:03d}.pt',map_location='cpu',weights_only=True)
    old=torch.load(run/f'input_prefix_scores/{i:03d}.pt',map_location='cpu',weights_only=True)
    raw={name.replace('end-pass ','end-pass input-prefix ',1):z for name,z in final_raw.items()}
    raw.update(torch.load(run/f'boundary_readouts/{i:03d}.pt',map_location='cpu',weights_only=True));assert len(raw)==12
    for name,z in final_raw.items():assert torch.equal(z.masked_fill(prompt_mask|output_mask,-torch.inf),old[name]),(i,name)
    for method,raw_z in raw.items():
        assert raw_z.shape==(248320,) and torch.isfinite(raw_z).all()
        z=raw_z.masked_fill(full_mask,-torch.inf);r=index[i,method];selected=r['selected_ids'];s=set(selected)
        assert len(s)==len(selected)==32 and z[selected].tolist()==r['selected_scores']
        assert [vocab[t] for t in selected]==r['top32']
        cutoff=z.topk(32).values[-1];assert (z[selected]>=cutoff).all() and set((z>cutoff).nonzero().flatten().tolist())<=s
        actual=sorted(set(re.findall(r'[^\W_]+',trace['scoring_text'].lower())));assert actual==r['actual_words']
        h0=ids(r['hidden_aliases'],case['hidden_alias_min_chars'] if 'hidden_alias_min_chars' in case else None)
        a0=ids(actual);s0=ids(r['answer_aliases']);ah,an=h0-a0,a0-h0
        said=any(a.casefold() in actual for a in r['hidden_aliases'])
        observed=any(re.search(r'\b'+re.escape(a)+r'\b',trace['scoring_text'],re.I) for a in r['answer_aliases'])
        cn=an|((s0-h0) if observed else set());ch=ah-cn;cn=cn-ah
        unscorable=[w for w in actual if not ids([w])]
        evaluable=said or bool(ah and an and not unscorable and ch and cn)
        input_labels=ids([case['input_word']]) if 'input_word' in case else set()
        assert (said,observed,unscorable,evaluable)==(r['hidden_is_said'],r['intended_answer_observed'],r['unscorable_actual_words'],r['alias_checked_evaluable'])
        assert bool(evaluable and not said and s&ch and not s&(cn|input_labels))==r['alias_checked_pass']
        assert [vocab[t] for t in selected if t in input_labels]==r['input_hits']
        if evaluable and not said:
            a,b=z[list(ch),None],z[list(cn)][None,:]
            auc=float(((a>b).double()+.5*(a==b).double()).mean());max_auc_error=max(max_auc_error,abs(auc-r['alias_checked_auroc']));assert max_auc_error<1e-7
            mask_nulls.append({'case_index':i,'method':method,'observed':auc,'iid_same_mask_expectation':.5+.5*(float((~torch.isfinite(b)).double().mean())-float((~torch.isfinite(a)).double().mean()))})
        else:assert r['alias_checked_auroc'] is None
        h,s0=ids([r['concept']]),ids([r['answer']]);h,s0=h-s0,s0-h
        assert (rank(z,h),rank(z,s0))==(r['r_hidden'],r['r_said']);checked+=1
        if 'preclue' not in method:
            for t,value in enumerate(norm):
                if value in probes[i]:
                    diagnosis.append({'case_index':i,'method':method,'id':t,'token':vocab[t],'normalized':value,
                        'prompt_mask':bool(prompt_mask[t]),'output_mask':bool(output_mask[t]),'extension_mask':bool(extension_mask[t]),
                        'raw_score':float(raw_z[t]),'raw_rank':rank(raw_z,[t]),'masked_rank':rank(z,[t]),'selected':t in r['selected_ids']})
events=[json.loads(line) for line in (master/'forward_trace.jsonl').read_text().splitlines()]
assert len(events)==p['actual_forwards']==p['generated_tokens']==len(expected_lengths)==15
assert all(e['phase']=='capture' and not e['grad_enabled'] for e in events)
assert [e['sequence_length'] for e in events]==expected_lengths
assert checked==72
result={'checked_selected_rows':checked,'total_rows':len(rows),'forwards':len(events),'positions':point_indices,'max_auc_error':max_auc_error,
        'scope':'Saved-score/mask/position/coverage reconstruction, not neural replay or independent head reconstruction; probes chosen posthoc from observed lists.'}
(master/'verification.json').write_text(json.dumps(result,indent=1)+'\n')
(master/'output_variant_diagnostic.json').write_text(json.dumps(diagnosis,ensure_ascii=False,indent=1)+'\n')
(master/'mask_nulls.json').write_text(json.dumps(mask_nulls,indent=1)+'\n')
print(json.dumps(result,indent=1),flush=True)
