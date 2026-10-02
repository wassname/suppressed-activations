"""Eight generic prefills and configured continuous conditions through08. — PI/OpenAI"""
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


def main(source,manifest_path,manifest_sha,config_path=Path('data/dog_spider_joint_chat_v1.json'),run_kind='chat-causal-joint',
         raw_coordinate_exchange=False,reference_master=None):
    assert raw_coordinate_exchange or reference_master is None  # new configs have no reference run; Base parity skipped
    started=time.monotonic()
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==manifest_sha
    manifest=json.loads(manifest_path.read_text())
    for path,sha in manifest['pins'].items():
        assert hashlib.sha256((source if path==SOURCE else ROOT/path).read_bytes()).hexdigest()==sha,path
    config=json.loads((ROOT/config_path).read_text())
    modes=(['Base','raw J-coordinate exchange','raw plain-coordinate exchange','matched-random delta'] if raw_coordinate_exchange else
           ['Base','role-aligned donor']+(['previous literal-name donor'] if config['previous_donor'] is not None else [])+['matched-random delta'])
    if raw_coordinate_exchange:
        assert config['previous_donor'] is None
    if reference_master is not None:
        reference=json.loads((reference_master/'pipeline.json').read_text())
        assert reference['stage']=='completed' and len(reference['case_runs'])==len(config['cases'])
    n_conditions=len(modes)*len(config['cases'])
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_{run_kind}'
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
              'case_runs':[],'goals_completed':False,'raw_coordinate_exchange':raw_coordinate_exchange,
              'reference_master':str(reference_master) if reference_master is not None else None}
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
    donor=None;suffix=None;generic_prefills=0
    if not raw_coordinate_exchange:
        prepared=g['main'](prepare_donors_json=ROOT/config['donor_config'])
        donor=prepared/'donors.pt';checkpoint=torch.load(donor,weights_only=True,map_location='cpu')
        assert len(events)==8 and not any(r['grad_enabled'] for r in events)
        assert [r['sequence_length'] for r in events]==[len(s['token_ids']) for s in checkpoint['provenance']['samples']]
        suffix=checkpoint['provenance']['samples'][0]['assistant_suffix_ids']
        assert all(s['assistant_suffix_ids']==suffix for s in checkpoint['provenance']['samples'])
        generic_prefills=8
        metadata.update(prepared=str(prepared),donor_sha256=hashlib.sha256(donor.read_bytes()).hexdigest())
    metadata.update(stage='running',generic_prefills=generic_prefills)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    table=[];total_tokens=0;canonical_vectors=None
    for index,case in enumerate(config['cases']):
        gc.collect();phase=case['name'];begin=len(events)
        run=g['main'](donor_checkpoint=donor,chat_causal_json=ROOT/config_path,
            causal_case_index=index,reverse=case['reverse'],relation=case['relation'],prompt_positions=config['prompt_positions'],decode_scale=.25,
            raw_coordinate_exchange=raw_coordinate_exchange)
        rows=json.loads((run/'interventions.json').read_text())
        assert list(rows)==modes
        if raw_coordinate_exchange:
            if reference_master is not None:
                previous=reference['case_runs'][index];assert previous['case']==case
                base=json.loads((Path(previous['run'])/'interventions.json').read_text())['Base']
                assert all(rows['Base'][k]==base[k] for k in ('token_ids','generation','input_repr','top10','prefill_readout'))
            assert not (run/'donors.pt').exists() and not (run/'clean_target_probe.json').exists()
        else:
            vectors=torch.load(run/'applied_vectors.pt',weights_only=True,map_location='cpu')
            sign=1 if case['reverse'] else -1
            if canonical_vectors is not None:assert all(torch.equal(sign*v,canonical_vectors[k]) for k,v in vectors.items())
            canonical_vectors={k:sign*v for k,v in vectors.items()}
            assert abs(float(vectors['role-aligned donor'].norm()-vectors['matched-random delta'].norm()))<1e-5
        rendering=json.loads((run/'chat_rendering.json').read_text())
        if suffix is None:suffix=rendering['assistant_suffix_ids']
        assert rendering['case']==case and rendering['assistant_suffix_ids']==suffix
        calls=events[begin:];offset=0
        for mode,row in rows.items():
            n=row['n_tokens'];assert 1<=n<=32 and len(row['coverage'])==n
            lengths=[len(rendering['input_ids'])]+[1]*(n-1)
            assert [r['sequence_length'] for r in calls[offset:offset+n]]==lengths
            assert [r['sequence_length'] for r in row['coverage']]==lengths
            assert row['selected_prompt_token_ids']==([suffix[-1]] if config['prompt_positions']==1 else rendering['input_ids'])
            assert row['coverage'][0]['positions']==(1 if config['prompt_positions']==1 else len(rendering['input_ids']))
            assert row['assistant_suffix_ids']==suffix
            assert row['input_repr']==repr(rendering['prompt'])
            assert not any(r['grad_enabled'] for r in calls[offset:offset+n])
            offset+=n;total_tokens+=n
            table.append([case['name']+': '+mode,row['generation_scoring_text'].replace('\n','\\n').replace('|','\\|'),
                          '; '.join(row['expected_properties']),n,row['answer_log_odds_shift'],row['answer_pair_mass'],row['r2'],str(run/'run.md')])
        assert offset==len(calls)
        metadata['case_runs'].append({'case':case,'run':str(run),'forward_calls':offset})
        (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    assert len(table)==n_conditions and len(events)==generic_prefills+total_tokens<=generic_prefills+32*n_conditions
    first=rows['Base']['answer_first_token_strings']
    result=tabulate(table,headers=['Case / condition','Observed text','Expected properties','Tokens',f'First-token {first[0]!r}→{first[1]!r} log-odds shift','First-token pair mass','r2','Full log'],tablefmt='pipe',floatfmt='.4f')
    description=('Raw coordinate exchange, no donor preparation; random matches requested candidate norm on its own state, not diverging trajectories after BF16. '+('Base tokens, top10 and prefill readout reproduce the pinned reference. ' if reference_master is not None else 'No reference run for Base parity. ') if raw_coordinate_exchange else
                 'Natural donor addition; random matches its norm. ')
    (master/'run.md').write_text(f'---\ngeneric_prefills: {generic_prefills}\nraw_coordinate_exchange: {str(raw_coordinate_exchange).lower()}\nconditions: {n_conditions}\nconfig: {config_path}\n---\n# Native-chat joint-property intervention\n\n— PI/OpenAI. '
        'Known development concepts; selection/configuration declared in the pinned inputs. '+description+
        'First-token scores are not full multi-token answer probabilities and do not establish joint consistency or coherence; semantic review is pending. Wrong/capped outputs stay in the denominator.\n\n'+result+'\n')
    metadata.update(stage='completed',actual_forwards=len(events),generated_tokens=total_tokens,
        elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,semantic_review_pending=True)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps(metadata,indent=1),flush=True);print(result,flush=True);print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path);parser.add_argument('manifest',type=Path);parser.add_argument('manifest_sha')
    parser.add_argument('--config-json',type=Path,default=Path('data/dog_spider_joint_chat_v1.json'))
    parser.add_argument('--run-kind',default='chat-causal-joint')
    parser.add_argument('--raw-coordinate-exchange',action='store_true')
    parser.add_argument('--reference-master',type=Path)
    args=parser.parse_args()
    main(args.source,args.manifest,args.manifest_sha,args.config_json,args.run_kind,args.raw_coordinate_exchange,args.reference_master)
