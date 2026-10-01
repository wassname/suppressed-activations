"""Eight generic prefills and twelve continuous one-pass conditions through08. — PI/OpenAI"""
from datetime import datetime
import gc
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import sys
import time
from types import SimpleNamespace

import torch
from tabulate import tabulate

ROOT=Path.cwd()
SOURCE='scripts/english/08_jlens_one_pass.py'


def main(source,manifest_path,manifest_sha):
    started=time.monotonic()
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==manifest_sha
    manifest=json.loads(manifest_path.read_text())
    for path,sha in manifest['pins'].items():
        assert hashlib.sha256((source if path==SOURCE else ROOT/path).read_bytes()).hexdigest()==sha,path
    config=json.loads((ROOT/'data/dog_spider_joint_chat_v1.json').read_text())
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_chat-causal-joint'
    master.mkdir(parents=True)
    shutil.copyfile(Path(__file__),master/'launcher.py')
    shutil.copyfile(source,master/'source.py')
    shutil.copyfile(manifest_path,master/'manifest.json')
    for path in manifest['pins']:
        if path.startswith('out/'):
            continue
        dest=master/'inputs'/path;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source if path==SOURCE else ROOT/path,dest)
    metadata={'stage':'preflight','source_sha256':manifest['pins'][SOURCE],'manifest_sha256':manifest_sha,
              'case_runs':[],'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps({'master':str(master)}),flush=True)
    g=runpy.run_path(str(source))['main'].__globals__
    torch.set_num_threads(4)
    phase='generic-preparation';events=[]
    loader=g['AutoModelForCausalLM'].from_pretrained
    def record(module,args,kwargs):
        ids=args[0] if args else kwargs['input_ids']
        item={'phase':phase,'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()}
        events.append(item)
        with (master/'forward_trace.jsonl').open('a') as stream:stream.write(json.dumps(item)+'\n')
    def load(*args,**kwargs):
        model=loader(*args,**kwargs);model.register_forward_pre_hook(record,with_kwargs=True)
        return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    prepared=g['main'](prepare_donors_json=ROOT/config['donor_config'])
    donor=prepared/'donors.pt';checkpoint=torch.load(donor,weights_only=True,map_location='cpu')
    assert len(events)==8 and not any(r['grad_enabled'] for r in events)
    assert [r['sequence_length'] for r in events]==[len(s['token_ids']) for s in checkpoint['provenance']['samples']]
    suffix=checkpoint['provenance']['samples'][0]['assistant_suffix_ids']
    assert all(s['assistant_suffix_ids']==suffix for s in checkpoint['provenance']['samples'])
    metadata.update(stage='prepared',prepared=str(prepared),donor_sha256=hashlib.sha256(donor.read_bytes()).hexdigest())
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    table=[];total_tokens=0;canonical_vectors=None
    for index,case in enumerate(config['cases']):
        gc.collect();phase=case['name'];begin=len(events)
        run=g['main'](donor_checkpoint=donor,chat_causal_json=ROOT/'data/dog_spider_joint_chat_v1.json',
            causal_case_index=index,reverse=case['reverse'],relation=case['relation'],prompt_positions=1,decode_scale=.25)
        rows=json.loads((run/'interventions.json').read_text())
        assert list(rows)==['Base','role-aligned donor','previous literal-name donor','matched-random delta']
        vectors=torch.load(run/'applied_vectors.pt',weights_only=True,map_location='cpu')
        sign=1 if case['reverse'] else -1
        if canonical_vectors is not None:assert all(torch.equal(sign*v,canonical_vectors[k]) for k,v in vectors.items())
        canonical_vectors={k:sign*v for k,v in vectors.items()}
        assert abs(float(vectors['role-aligned donor'].norm()-vectors['matched-random delta'].norm()))<1e-5
        rendering=json.loads((run/'chat_rendering.json').read_text())
        assert rendering['case']==case and rendering['assistant_suffix_ids']==suffix
        calls=events[begin:];offset=0
        for mode,row in rows.items():
            n=row['n_tokens'];assert 1<=n<=32 and len(row['coverage'])==n
            lengths=[len(rendering['input_ids'])]+[1]*(n-1)
            assert [r['sequence_length'] for r in calls[offset:offset+n]]==lengths
            assert [r['sequence_length'] for r in row['coverage']]==lengths
            assert row['selected_prompt_token_ids']==[suffix[-1]]
            assert row['assistant_suffix_ids']==suffix
            assert row['input_repr']==repr(rendering['prompt'])
            assert not any(r['grad_enabled'] for r in calls[offset:offset+n])
            offset+=n;total_tokens+=n
            table.append([case['name']+': '+mode,row['generation_scoring_text'].replace('\n','\\n').replace('|','\\|'),
                          '; '.join(row['expected_properties']),n,row['answer_log_odds_shift'],row['answer_pair_mass'],row['r2'],str(run/'run.md')])
        assert offset==len(calls)
        metadata['case_runs'].append({'case':case,'run':str(run),'forward_calls':offset})
        (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    assert len(table)==12 and len(events)==8+total_tokens<=392
    result=tabulate(table,headers=['Case / condition','Observed text','Expected properties','Tokens','8→4 log-odds shift','Bare-answer mass','r2','Full log'],tablefmt='pipe',floatfmt='.4f')
    (master/'run.md').write_text('---\ngeneric_prefills: 8\nconditions: 12\n---\n# Native-chat joint-property intervention\n\n— PI/OpenAI. '
        'Known development concepts. Task frame and donor preparation both changed. Previous literal donor retains its own norm; random matches the new donor. '
        'First-token scores do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.\n\n'+result+'\n')
    metadata.update(stage='completed',actual_forwards=len(events),generated_tokens=total_tokens,
        elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,semantic_review_pending=True)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps(metadata,indent=1),flush=True);print(result,flush=True);print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':
    main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
