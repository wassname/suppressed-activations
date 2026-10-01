"""Four fixed person probes via08; reuse native-v4 replay/coverage checks. — PI/OpenAI"""
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
DATA='data/english_person_pairs_chat_v1.json'
LABELS='slop/audits/2026-10-01_person-pairs-labels.json'
CHECKS='slop/audits/2026-10-01_native-v4-launcher.py'


def label_stats(z,ids,selected):
    if not ids:return {'rank':None,'max_logit':None,'selected_prefix_hit':False}
    maximum=z[ids].max()
    return {'rank':int((z>maximum).sum()) if torch.isfinite(maximum) else 10**9,
            'max_logit':float(maximum) if torch.isfinite(maximum) else None,
            'selected_prefix_hit':bool(set(ids)&set(selected))}


def main(source,manifest_path,manifest_sha):
    started=time.monotonic();torch.set_num_threads(4)
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==manifest_sha
    manifest=json.loads(manifest_path.read_text())
    for name,sha in manifest['pins'].items():assert hashlib.sha256((source if name==SOURCE else ROOT/name).read_bytes()).hexdigest()==sha,name
    data=ROOT/DATA;dataset=json.loads(data.read_text());labels=json.loads((ROOT/LABELS).read_text())
    assert len(dataset['cases'])==4 and dataset['required_max_new_tokens']==32
    assert labels['data_sha256']==hashlib.sha256(data.read_bytes()).hexdigest()
    checks=runpy.run_path(str(ROOT/CHECKS));methods=checks['METHODS']
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_person-pairs-readout';master.mkdir(parents=True)
    for src,name in ((source,'source.py'),(manifest_path,'manifest.json'),(Path(__file__),'launcher.py')):shutil.copyfile(src,master/name)
    for name in manifest['pins']:
        if name==dataset['source_dataset']:continue
        dest=master/'inputs'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source if name==SOURCE else ROOT/name,dest)
    metadata={'stage':'preflight','source_sha256':manifest['pins'][SOURCE],'manifest_sha256':manifest_sha,'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1));print(json.dumps({'master':str(master)}),flush=True)
    g=runpy.run_path(str(source))['main'].__globals__;loader=g['AutoModelForCausalLM'].from_pretrained
    phase='capture';events=[]
    def record(module,args,kwargs):
        ids=args[0] if args else kwargs['input_ids']
        event={'phase':phase,'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()};events.append(event)
        with (master/'forward_trace.jsonl').open('a') as stream:stream.write(json.dumps(event)+'\n')
        assert phase=='capture','Cached scoring must not call the transformer'
    def load(*args,**kwargs):
        model=loader(*args,**kwargs);model.register_forward_pre_hook(record,with_kwargs=True);return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    settings={'cases_json':data,'end_pass_readout':True,'output_mask_max_n':1,'erase_output':True,
              'erase_strength':.5,'chat_readout':True,'readout_max_new_tokens':32}
    capture=g['main'](**settings);traces=json.loads((capture/'generation_traces.json').read_text())
    assert len(traces)==4 and all(1<=len(t['token_ids'])<=32 for t in traces)
    checks['check_forward_trace'](traces,events)
    metadata.update(stage='captured',capture=str(capture),actual_forwards=len(events),generated_tokens=sum(len(t['token_ids']) for t in traces))
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1));gc.collect();phase='rescore'
    replay=g['main'](**settings,replay_readout_run=capture,expand_input_prefix=True)
    index=checks['check_replay'](capture,replay,4)
    assert len(events)==metadata['actual_forwards'] and all(e['phase']=='capture' for e in events)
    pair_rows=[]
    for method in methods:
        base=method.replace('input-prefix ','')
        for a,b in ((0,1),(2,3)):
            shared=set(labels['cases'][a]['ids'])&set(labels['cases'][b]['ids'])
            classes={i:sorted(set(labels['cases'][i]['ids'])-shared) for i in (a,b)}
            items=[]
            for i,partner in ((a,b),(b,a)):
                raw=torch.load(replay/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True,map_location='cpu')[base]
                old=torch.load(capture/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True,map_location='cpu')[base]
                assert torch.equal(raw,old)
                masked=torch.load(replay/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True,map_location='cpu')[base]
                exclusions=json.loads((replay/'input_prefix_exclusions.json').read_text())[i]['added_input_exclusions']
                masked[[r['id'] for r in exclusions]]=-torch.inf
                item={'case_index':i,'concept':dataset['cases'][i]['concept']}
                for kind,z,selected in (('raw',raw,raw.topk(32).indices.tolist()),('masked',masked,index[i,method]['selected_ids'])):
                    own=label_stats(z,classes[i],selected);other=label_stats(z,classes[partner],selected)
                    margin=None if own['max_logit'] is None or other['max_logit'] is None else own['max_logit']-other['max_logit']
                    item[kind]={'own':own,'partner':other,'own_margin':margin}
                items.append(item)
            margins=[item['raw']['own_margin'] for item in items]
            pair_rows.append({'method':method,'case_indices':[a,b],'ambiguous_ids':sorted(shared),'cases':items,
                'actual_outputs_identical':traces[a]['scoring_text']==traces[b]['scoring_text'],
                'raw_D':sum(margins) if all(m is not None for m in margins) else None,
                'raw_reversal':all(m>0 for m in margins) if all(m is not None for m in margins) else None})
    (master/'pair_diagnostics.json').write_text(json.dumps(pair_rows,ensure_ascii=False,indent=1))
    summary=[]
    for method in methods:
        rows=[index[i,method] for i in range(4)];aucs=[r['alias_checked_auroc'] for r in rows if r['alias_checked_auroc'] is not None]
        summary.append({'method':method,'n':4,'lexical_joint':sum(r['alias_checked_pass'] for r in rows),
            'mean_alias_auroc':sum(aucs)/len(aucs) if aucs else None,'auroc_n':len(aucs),
            'expected_answer_matches':sum(r['intended_answer_observed'] for r in rows)})
    (master/'summary.json').write_text(json.dumps(summary,indent=1))
    table=tabulate([[r['method'],f"{r['lexical_joint']}/4",r['mean_alias_auroc'],r['auroc_n'],r['expected_answer_matches']] for r in summary],
        headers=['Method','Lexical joint','Alias AUROC','AUROC n','Expected matches /4'],tablefmt='pipe',floatfmt='.4f')
    report='---\ngenerations: 4\noriginal_rows_exact: 72\ncandidate_rows: 16\n---\n# Frozen readout on person bridges\n\n— PI/OpenAI. Development only; same-country shortcuts and name-fragment ambiguity remain. No first-hop filter. Full semantic review pending.\n\n'+table+'\n'
    for i in range(4):
        row=index[i,methods[0]]
        report+=f"\n## {i}: {row['concept']}\n\nInput repr:\n```text\n{row['prompt']!r}\n```\n\nExact continuation ({len(traces[i]['token_ids'])} tokens):\n```text\n{row['baseline_generation']}\n```\n"
        for method in methods:report+=f"\n{method}; lexicaljoint={index[i,method]['alias_checked_pass']}:\n\n{index[i,method]['top32']!r}\n"
    report+=f'\nCapture: {capture}/run.md\n\nFull scores: {replay}/readout.json\n\nPair diagnostics: {master}/pair_diagnostics.json\n'
    (master/'run.md').write_text(report)
    metadata.update(stage='completed',replay=str(replay),original_rows_exact=72,candidate_rows=16,rescore_forward_calls=0,
        elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,semantic_review_pending=True)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1));print(json.dumps(metadata,indent=1),flush=True)
    print(table,flush=True);print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
