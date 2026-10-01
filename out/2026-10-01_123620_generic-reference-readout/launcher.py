"""One generic prefill and two cached scoring cohorts through08. — PI/OpenAI"""
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
MANIFEST_SHA='e3269b20511e4252288de44f1292745d6e90bf282b7d64c012742f93530c4526'
SOURCE='scripts/english/08_jlens_one_pass.py'
BASES=['J-lens','plain24','plain27']
NEW=[f'end-pass input-prefix {kind}-reference erased0.5 {name}' for name in BASES for kind in ('generic','random')]
OLD=[f'end-pass input-prefix erased0.5 {name}' for name in BASES]+['end-pass input-prefix J-lens']


def check_cached(group,run):
    capture,baseline=ROOT/group['capture'],ROOT/group['baseline']
    old=json.loads((baseline/'readout.json').read_text())
    rows=json.loads((run/'readout.json').read_text())
    index={(r['case_index'],r['method']):r for r in rows}
    assert len(old)==22*group['n'] and len(rows)==len(index)==28*group['n']
    assert all(index[r['case_index'],r['method']]==r for r in old)
    assert (run/'generation_traces.json').read_bytes()==(capture/'generation_traces.json').read_bytes()
    a=torch.load(capture/'prefill.pt',weights_only=True,map_location='cpu')
    b=torch.load(run/'prefill.pt',weights_only=True,map_location='cpu')
    assert len(a)==len(b)==group['n'] and all(torch.equal(x[k],y[k]) for x,y in zip(a,b,strict=True) for k in x)
    for i in range(group['n']):
        old_scores=torch.load(baseline/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True)
        new_scores=torch.load(run/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True)
        assert old_scores.keys()==new_scores.keys() and all(torch.equal(z,new_scores[k]) for k,z in old_scores.items())
        if group['name']=='animals':
            old_raw=torch.load(baseline/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
            new_raw=torch.load(run/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
            assert old_raw.keys()==new_raw.keys() and all(torch.equal(z,new_raw[k]) for k,z in old_raw.items())
    return index


def animal_margins(run,labels):
    scored={}
    for i in range(4):
        saved=torch.load(run/'reference_readout_scores'/f'{i:03d}.pt',weights_only=True)
        assert set(saved)==set(NEW)
        for method,z in saved.items():
            lp=z.log_softmax(-1)
            for concept,ids in labels.items():
                values=[{**t,'log_probability':float(lp[t['id']])} for t in ids]
                scored[i,method,concept]=max(t['log_probability'] for t in values)
    rows=[]
    for method in NEW:
        for j,(a,b) in enumerate((('horse','cow'),('cat','goat'))):
            da=scored[2*j,method,a]-scored[2*j,method,b]
            db=scored[2*j+1,method,a]-scored[2*j+1,method,b]
            rows.append({'method':method,'pair':[a,b],'own_margins':[da,-db],'D':da-db,'reversal':da>0>db})
    return rows


def main(source,manifest_path):
    started=time.monotonic()
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==MANIFEST_SHA
    manifest=json.loads(manifest_path.read_text())
    for path,sha in manifest['pins'].items():
        actual=source if path==SOURCE else ROOT/path
        assert hashlib.sha256(actual.read_bytes()).hexdigest()==sha,path
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_generic-reference-readout'
    master.mkdir(parents=True)
    shutil.copyfile(Path(__file__),master/'launcher.py')
    shutil.copyfile(manifest_path,master/'manifest.json')
    shutil.copyfile(source,master/'source.py')
    for path in manifest['pins']:
        if path.startswith('out/'):
            continue
        dest=master/'inputs'/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source if path==SOURCE else ROOT/path,dest)
    metadata={'stage':'preflight','manifest_sha256':MANIFEST_SHA,'source_sha256':manifest['pins'][SOURCE],
              'groups':[],'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps({'master':str(master)}),flush=True)
    g=runpy.run_path(str(source))['main'].__globals__
    torch.set_num_threads(4)
    forwards=[]
    phase='generic-preparation'
    loader=g['AutoModelForCausalLM'].from_pretrained
    def record(module,args,kwargs):
        ids=args[0] if args else kwargs['input_ids']
        item={'phase':phase,'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()}
        forwards.append(item)
        with (master/'forward_trace.jsonl').open('a') as stream: stream.write(json.dumps(item)+'\n')
        assert phase=='generic-preparation','Cached scoring must not call the transformer'
    def load(*args,**kwargs):
        model=loader(*args,**kwargs)
        model.register_forward_pre_hook(record,with_kwargs=True)
        return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    prepared=g['main'](prepare_reference_json=ROOT/'data/generic_readout_reference_v1.json')
    reference=prepared/'reference.pt'
    details=torch.load(reference,weights_only=True,map_location='cpu')
    assert len(forwards)==1 and not forwards[0]['grad_enabled']
    assert forwards[0]['sequence_length']==len(details['input_ids'])
    assert all(v==[len(details['input_ids'])] for v in details['coverage'].values())
    reference_sha=hashlib.sha256(reference.read_bytes()).hexdigest()
    metadata.update(stage='prepared',reference=str(reference),reference_sha256=reference_sha)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    phase='cached-scoring'
    summaries=[]
    report='# Generic normalized-state subtraction\n\n— PI/OpenAI. One generic prefill, no new case trajectories; semantic review pending. No second norm. Random references match before projection only. Known development cases; no v5.\n'
    for group in manifest['groups']:
        gc.collect()
        run=g['main'](cases_json=ROOT/group['data'],end_pass_readout=True,output_mask_max_n=1,
            erase_output=True,erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,
            replay_readout_run=ROOT/group['capture'],expand_input_prefix=True,reference_checkpoint=reference)
        assert len(forwards)==1 and hashlib.sha256(reference.read_bytes()).hexdigest()==reference_sha
        index=check_cached(group,run)
        norms=json.loads((run/'reference_traces.json').read_text())
        assert len(norms)==6*group['n']
        report+=f"\n## {group['name']} ({group['n']} cases)\n\nFull records: {run}/readout.json\n"
        for method in NEW+OLD:
            rows=[index[i,method] for i in range(group['n'])]
            aucs=[r['alias_checked_auroc'] for r in rows if r['alias_checked_auroc'] is not None]
            base=method.replace('generic-reference ','').replace('random-reference ','')
            gains=sum(r['alias_checked_pass'] and not index[r['case_index'],base]['alias_checked_pass'] for r in rows)
            losses=sum(not r['alias_checked_pass'] and index[r['case_index'],base]['alias_checked_pass'] for r in rows)
            summaries.append({'cohort':group['name'],'method':method,'n':group['n'],
                'lexical_joint':sum(r['alias_checked_pass'] for r in rows),'paired_gains':gains,'paired_losses':losses,
                'mean_alias_auroc':sum(aucs)/len(aucs) if aucs else None,'auroc_n':len(aucs),
                'expected_answer_matches':sum(r['intended_answer_observed'] for r in rows)})
        for i in range(group['n']):
            row=index[i,OLD[0]]
            report+=f"\n### {i}: {row['concept']}\n\nInput repr:\n```text\n{row['prompt']!r}\n```\n\nUnchanged exact output:\n```text\n{row['baseline_generation']}\n```\n"
            for method in NEW+OLD:
                r=index[i,method]
                report+=f"\n{method}; lexicaljoint={r['alias_checked_pass']}:\n\n{r['top32']!r}\n"
        if group['name']=='animals':
            labels=json.loads((ROOT/'slop/audits/2026-10-01_animal-pairs-labels.json').read_text())['labels']
            (master/'animal_margins.json').write_text(json.dumps(animal_margins(run,labels),indent=1))
        metadata['groups'].append({**group,'run':str(run),'old_rows_exact':22*group['n'],'candidate_rows':6*group['n']})
        (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    table=tabulate([[r['cohort']+': '+r['method'],f"{r['lexical_joint']}/{r['n']}",r['paired_gains'],r['paired_losses'],
                     r['mean_alias_auroc'],r['auroc_n']] for r in summaries],
                    headers=['Cohort / method','Lexical joint ↑','Gains','Losses','Alias AUROC ↑','AUROC n'],tablefmt='pipe',floatfmt='.4f')
    (master/'summary.json').write_text(json.dumps(summaries,indent=1))
    (master/'run.md').write_text('---\ngeneric_prefills: 1\ncase_forward_calls: 0\n---\n'+table+'\n\n'+report)
    metadata.update(stage='completed',generic_forward_calls=1,case_forward_calls=0,
        elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,
        semantic_review_pending=True)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps(metadata,indent=1),flush=True)
    print(table,flush=True)
    print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':
    main(*map(Path,sys.argv[1:]))
