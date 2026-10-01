"""Six fixed cases through08, with observed one-pass coverage. — PI/OpenAI"""
from datetime import datetime
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

ROOT=Path.cwd();SOURCE='scripts/english/08_jlens_one_pass.py'
DATA='data/english_boundary_readout_v1.json'
CHECKER='slop/audits/2026-10-01_native-v4-launcher.py'

def main(source,manifest_path,manifest_sha):
    started=time.monotonic();assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==manifest_sha
    manifest=json.loads(manifest_path.read_text())
    for name,sha in manifest['pins'].items():assert hashlib.sha256((source if name==SOURCE else ROOT/name).read_bytes()).hexdigest()==sha,name
    data=json.loads((ROOT/DATA).read_text());assert len(data['cases'])==6
    for name,sha in data['sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
    original=json.loads((ROOT/'data/english_hidden_words_v4_chat.json').read_text())
    assert data['cases'][:4]==[{**c,'boundary_evaluation_group':'English non-geography'} for c in original['cases'][:4]]
    translations=json.loads((ROOT/'out/2026-09-30_125500_jlens-one-pass/cases.json').read_text())
    for j,(pair,index) in enumerate(zip(('de→fr','fr→de'),data['translation_source_indices'],strict=True),4):
        assert index==next(i for i,c in enumerate(translations['cases']) if c['pair']==pair)
        c=translations['cases'][index]
        assert data['cases'][j]=={**c,'prompt':'Complete the last translation with only the missing word:\n'+c['prompt'],'boundary_evaluation_group':'translation'}
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_boundary-readout';master.mkdir(parents=True)
    for src,name in ((source,'source.py'),(manifest_path,'manifest.json'),(Path(__file__),'launcher.py')):shutil.copyfile(src,master/name)
    for name in manifest['pins']:
        dest=master/'inputs'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source if name==SOURCE else ROOT/name,dest)
    meta={'stage':'preflight','source_sha256':manifest['pins'][SOURCE],'manifest_sha256':manifest_sha,'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(meta,indent=1));print(json.dumps({'master':str(master)}),flush=True)
    g=runpy.run_path(str(source))['main'].__globals__;check=runpy.run_path(str(ROOT/CHECKER))['check_forward_trace']
    torch.set_num_threads(4);events=[];loader=g['AutoModelForCausalLM'].from_pretrained
    def record(_m,args,kwargs):
        ids=args[0] if args else kwargs['input_ids'];item={'phase':'capture','sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()}
        events.append(item)
        with (master/'forward_trace.jsonl').open('a') as f:f.write(json.dumps(item)+'\n')
    def load(*args,**kwargs):
        model=loader(*args,**kwargs);model.register_forward_pre_hook(record,with_kwargs=True);return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    out=g['main'](cases_json=ROOT/DATA,chat_readout=True,end_pass_readout=True,expand_input_prefix=True,
        erase_output=True,erase_strength=.5,output_mask_max_n=1,readout_max_new_tokens=32,boundary_readout=True)
    traces=json.loads((out/'generation_traces.json').read_text());assert len(traces)==6
    check(traces,events);assert len(events)==sum(len(t['token_ids']) for t in traces)<=192
    rows=json.loads((out/'readout.json').read_text());assert len(rows)==180
    selected=[r for r in rows if r['method'].startswith(('end-pass input-prefix ','end-pass boundary ','end-pass preclue '))]
    assert len(selected)==72
    table=[]
    for group,indices in [('English non-geography',range(4)),('translation',range(4,6))]:
        for method in dict.fromkeys(r['method'] for r in selected):
            subset=[r for r in selected if r['case_index'] in indices and r['method']==method]
            table.append([group,method,f"{sum(r['alias_checked_pass'] for r in subset)}/{len(subset)}",sum(not r['alias_checked_evaluable'] for r in subset)])
    result=tabulate(table,headers=['Group','Method','Lexical joint↑','Unscored'],tablefmt='pipe')
    (master/'run.md').write_text('# Fixed boundary development test\n\n— PI/OpenAI. Post2718 rule; same captures, masks and heads. Two reciprocal translations share cloud. Native translation wrapper is new. No unseen or semantic-success claim. Preclue uses final-output direction/full-input masks too.\n\n'+result+'\n\nAll exact inputs, continuations and72 full lists: '+str(out/'run.md')+'\n')
    meta.update(stage='completed',run=str(out),actual_forwards=len(events),generated_tokens=sum(len(t['token_ids']) for t in traces),
        elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,semantic_review_pending=True)
    (master/'pipeline.json').write_text(json.dumps(meta,indent=1));print(json.dumps(meta,indent=1),flush=True);print(result,flush=True);print('run.md: '+str(master/'run.md'),flush=True)

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
