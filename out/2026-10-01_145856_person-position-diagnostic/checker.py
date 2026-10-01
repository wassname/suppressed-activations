"""Check saved position coverage and exact historical parity, not neural replication. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import torch
from transformers import AutoTokenizer

root=Path.cwd();torch.set_num_threads(4)
master=root/'out/2026-10-01_145856_person-position-diagnostic'
meta=json.loads((master/'pipeline.json').read_text());run=Path(meta['run'])
manifest=json.loads((master/'manifest.json').read_text())
for name,sha in manifest['pins'].items():
    p=master/'inputs'/name
    if name=='scripts/english/08_jlens_one_pass.py':p=master/'source.py'
    elif not p.exists():p=root/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,name
proof=json.loads((run/'position_reproduction.json').read_text());old=Path(proof['reference'])
for name,sha in proof['reference_sha256'].items():assert hashlib.sha256((old/name).read_bytes()).hexdigest()==sha
traces=json.loads((run/'generation_traces.json').read_text())
assert traces==json.loads((old/'generation_traces.json').read_text())
rows=json.loads((run/'readout.json').read_text());assert len(rows)==88 and rows==json.loads((old/'readout.json').read_text())
a=torch.load(run/'prefill.pt',weights_only=True);b=torch.load(old/'prefill.pt',weights_only=True)
full=torch.load(run/'prefill_positions.pt',weights_only=True)
assert len(a)==len(b)==len(full)==len(traces)==4
assert all(torch.equal(x[k],y[k]) for x,y in zip(a,b,strict=True) for k in x)
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
lengths=[];nrows=0
for i,trace in enumerate(traces):
    p=json.loads((run/'position_readouts'/f'{i:03d}.json').read_text())
    ids=tok(trace['prompt'],add_special_tokens=False).input_ids;n=len(ids);lengths.append(n)
    assert p['input_ids']==ids and p['last_position_scores_exact'] is True
    assert p['output_direction_id']==trace['token_ids'][0]
    assert set(full[i])=={24,27,32}
    for layer,state in full[i].items():
        assert state.shape==(n,2560) and torch.isfinite(state).all()
        assert torch.equal(state[-1],a[i][layer])
    methods={r['method'] for r in p['records']};assert len(methods)==4
    assert len(p['records'])==4*n and {(r['position'],r['method']) for r in p['records']}=={(j,m) for j in range(n) for m in methods}
    for r in p['records']:
        j=r['position'];assert r['input_token_id']==ids[j] and r['consumed_prefix']==tok.decode(ids[:j+1])
        assert len(r['selected_ids'])==len(set(r['selected_ids']))==len(r['selected_scores'])==len(r['tokens'])==32
        assert r['tokens']==[tok.decode([t]) for t in r['selected_ids']]
        assert r['selected_scores']==sorted(r['selected_scores'],reverse=True)
        assert r['selected_alias_ids']==sorted(set(r['selected_ids']) & set(p['evaluation_alias_ids']))
        for kind in ('raw','masked'):
            best=r[kind+'_best_alias_id']
            assert best in p['evaluation_alias_ids'] and r[kind+'_best_alias_token']==tok.decode([best])
        if r['selected_alias_ids']:
            first=min(r['selected_ids'].index(t) for t in r['selected_alias_ids'])
            assert r['masked_alias_rank']<=first
    nrows+=len(p['records'])
events=[json.loads(s) for s in (master/'forward_trace.jsonl').read_text().splitlines()]
assert len(events)==meta['actual_forwards']==meta['generated_tokens']==8
assert not any(e['grad_enabled'] for e in events)
result={'signature':'PI/OpenAI','cases':4,'prefix_lengths':lengths,'position_head_rows':nrows,
 'readout_rows_exact':88,'full_generations_exact':True,'final_states_exact':True,'forwards':8,
 'limits':'No independent earlier-state neural capture or recomputation of all position scores/ranks; metadata/tensor/selection consistency, not semantic certification.'}
(master/'verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1))
