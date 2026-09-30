"""Saved-state/span/component audit; not semantic certification. -- PI/OpenAI"""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import torch
from tokenizers import Tokenizer

torch.set_num_threads(1)
root=Path(sys.argv[1]); load=lambda p:json.loads(p.read_text())
assert (root/'source.py').read_bytes()==subprocess.check_output(['git','show','a53ba01:scripts/english/08_jlens_one_pass.py'])
assert (root/'cases.json').read_text()==Path('out/2026-09-30_175925_jlens-one-pass/cases.json').read_text()
ref=load(root/'capture_reference.json'); original=Path(ref['run'])
assert ref['last_states_and_generated_ids_equal']
for name,digest in ref['sha256'].items():
    assert hashlib.sha256((original/name).read_bytes()).hexdigest()==digest
for path,digest in load(root/'helper_sha256.json').items():
    assert hashlib.sha256((root/'helpers'/path).read_bytes()).hexdigest()==digest
full=torch.load(root/'prefill_positions.pt',map_location='cpu',weights_only=True)
last=torch.load(original/'prefill.pt',map_location='cpu',weights_only=True)
traces=load(root/'generation_traces.json'); spans=load(root/'question_spans.json')
assert traces==load(original/'generation_traces.json') and len(full)==len(last)==len(spans)==8
assert sum(len(t['token_ids']) for t in traces)==64
special=set(load(root/'tokenizer_special_ids.json')['r2_excluded_ids'])
tok=Tokenizer.from_file('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json')
prefix=load(root/'cases.json')['prefix']
for i,s in enumerate(spans):
    encoded=tok.encode(s['prompt'],add_special_tokens=False)
    assert encoded.ids==s['input_ids'] and [list(x) for x in encoded.offsets]==s['offsets']
    assert encoded.special_tokens_mask==s['special_mask'] and s['prefix_length']==len(prefix)
    assert s['prompt'].startswith(prefix) and s['prompt']==traces[i]['prompt']
    expected=[j for j,((a,b),token,flag) in enumerate(zip(encoded.offsets,encoded.ids,encoded.special_tokens_mask,strict=True)) if not flag and token not in special and len(prefix)<=a<b<=len(s['prompt'])]
    assert s['positions']==expected and expected[-1]==len(encoded.ids)-1
    assert set(full[i])==set(last[i])=={24,27,32}
    for layer,h in full[i].items():
        assert h.shape==(len(encoded.ids),2560) and torch.equal(h[-1],last[i][layer])
    assert all(c==[len(encoded.ids)]+[1]*7 for c in traces[i]['coverage'].values())
rows={(r['case_index'],r['method']):r for r in load(root/'readout.json')}
assert len(rows)==264
old=load(Path('out/2026-09-30_151032_jlens-one-pass/readout.json'))
assert len(old)==168 and all(rows[(r['case_index'],r['method'])]==r for r in old)
masks={m['case_index']:set(m['prompt_mask_ids'])|set(m['output_mask_ids']) for m in load(root/'pool_masks.json')}
components=load(root/'pool_components.json'); assert len(components)==96
peaks=[]
for trace in components:
    i,name=trace['case_index'],trace['method']; row=rows[(i,name)]
    tokens={t['id']:t for t in trace['tokens']}; selected=trace['selected_ids']
    assert len(selected)==len(set(selected))<=32 and row['top32']==[tokens[t]['token'] for t in selected]
    for t in tokens.values():
        assert t['peak_position'] in spans[i]['positions']
        if 'pooling last' in name:
            assert t['peak_position']==spans[i]['positions'][-1]
        value=t['p']-t['comparison_p'] if trace['subtract'] else t['p']
        eligible=value>0 and t['id'] not in masks[i]
        assert (t['score'] is not None)==eligible
        if eligible:
            assert math.isclose(value,t['score'],rel_tol=1e-6,abs_tol=1e-10)
    assert all(tokens[t]['score'] is not None for t in selected)
    assert selected==sorted(selected,key=lambda t:(-tokens[t]['score'],t))
    assert trace['eligible_n']>=len(selected)
    for t in tokens.values():
        if t['score'] is not None and t['id'] not in selected and selected:
            assert (-t['score'],t['id'])>=(-tokens[selected[-1]]['score'],selected[-1])
    hidden,said=set(trace['hidden_label_ids']),set(trace['said_label_ids'])
    assert row['alias_checked_hidden_found']==bool(hidden.intersection(selected))
    assert row['alias_checked_said_excluded']==(not said.intersection(selected))
    passed=row['alias_checked_evaluable'] and not row['hidden_is_said'] and bool(hidden.intersection(selected)) and not said.intersection(selected) and not row['input_hits']
    assert row['alias_checked_pass']==passed
    if row['alias_checked_evaluable'] and not row['hidden_is_said']:
        score=lambda t: tokens[t]['score'] if tokens[t]['score'] is not None else -math.inf
        auc=sum(float(score(h)>score(s))+.5*float(score(h)==score(s)) for h in hidden for s in said)/(len(hidden)*len(said))
        assert math.isclose(auc,row['alias_checked_auroc'],rel_tol=1e-6,abs_tol=1e-6)
    if name in ('end-pass pooled J-lens','end-pass pooled plain27'):
        best=max(hidden,key=lambda t:tokens[t]['p'])
        for label,t in [('best hidden variant',tokens[best])]+[('selected population',t) for t in tokens.values() if t['id'] in selected and t['token'].strip()=='population']:
            position=t['peak_position']; a,b=spans[i]['offsets'][position]
            peaks.append({'concept':row['concept'],'method':name,'role':label,'token':t['token'],'p_peak':t['p'],'comparison_p':t['comparison_p'],
                          'score':t['score'],'position':position,'input_piece':spans[i]['prompt'][a:b],'prefix_through_peak':spans[i]['prompt'][:b]})
summary={r['method']:r for r in load(root/'summary.json')}
for name,item in summary.items():
    matched=[r for (_,method),r in rows.items() if method==name]
    assert len(matched)==item['n']==8 and sum(r['alias_checked_pass'] for r in matched)==item['alias_checked_joint_pass']
selection=load(root/'pool_selection.json')
counts={n:summary['end-pass pooled '+n]['alias_checked_joint_pass'] for n in ['plain27','J-lens','plain24']}
winner=max(counts,key=counts.__getitem__)
assert selection['selected_representation']==winner and selection['pooled_counts']==counts
own_last=summary['end-pass pooling last '+winner]['alias_checked_joint_pass']
mismatch=summary['end-pass pooled mismatched '+winner]['alias_checked_joint_pass']
assert selection['numeric_screen_passed']==(counts[winner]>=7 and counts[winner]>own_last and counts[winner]>mismatch)
report={'author':'PI/OpenAI','status':'PASS full saved-state parity, independent retokenization/spans,168 old rows and96 component/scorer records',
        'n_generations':8,'n_generated_tokens':64,'selection':selection,'peak_diagnostics':peaks,
        'limits':'Saved components verify arithmetic and recorded peak bounds, not independently reconstructed full-vocabulary peak probabilities/top32 optimality or semantic exclusion. Model-call counts derive from traces and inspected source.'}
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=1))
print(json.dumps(report,ensure_ascii=False,indent=1))
