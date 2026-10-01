"""Pinned08 position diagnostic; the production entry point owns inference and scoring. — PI/OpenAI"""
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

ROOT=Path.cwd()
SOURCE='scripts/english/08_jlens_one_pass.py'
DATA='data/english_person_pairs_chat_v1.json'


def main(source,manifest_path,manifest_sha):
    started=time.monotonic();torch.set_num_threads(4)
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==manifest_sha
    manifest=json.loads(manifest_path.read_text())
    for name,sha in manifest['pins'].items():
        assert not Path(name).is_absolute()
        assert hashlib.sha256((source if name==SOURCE else ROOT/name).read_bytes()).hexdigest()==sha,name
    master=ROOT/'out'/f'{datetime.now():%Y-%m-%d_%H%M%S}_person-position-diagnostic';master.mkdir(parents=True)
    for src,name in ((source,'source.py'),(manifest_path,'manifest.json'),(Path(__file__),'launcher.py')):shutil.copyfile(src,master/name)
    metadata={'stage':'incomplete','source_sha256':manifest['pins'][SOURCE],'manifest_sha256':manifest_sha,
              'reference':manifest['reference'],'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1));print(json.dumps({'master':str(master)}),flush=True)
    g=runpy.run_path(str(source))['main'].__globals__;loader=g['AutoModelForCausalLM'].from_pretrained;events=[]
    def record(module,args,kwargs):
        ids=args[0] if args else kwargs['input_ids']
        event={'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()};events.append(event)
        with (master/'forward_trace.jsonl').open('a') as stream:stream.write(json.dumps(event)+'\n')
    def load(*args,**kwargs):
        model=loader(*args,**kwargs);model.register_forward_pre_hook(record,with_kwargs=True);return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    run=g['main'](cases_json=ROOT/DATA,end_pass_readout=True,output_mask_max_n=1,erase_output=True,
        erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,expand_input_prefix=True,
        inspect_readout_positions=True,verify_readout_run=ROOT/manifest['reference'])
    traces=json.loads((run/'generation_traces.json').read_text());expected=[]
    assert len(traces)==4
    for trace in traces:
        lengths=trace['coverage']['24'];assert all(values==lengths for values in trace['coverage'].values())
        assert len(lengths)==len(trace['token_ids'])<=32 and lengths[1:]==[1]*(len(lengths)-1)
        expected.extend(lengths)
    assert [e['sequence_length'] for e in events]==expected and not any(e['grad_enabled'] for e in events)
    reproduction=json.loads((run/'position_reproduction.json').read_text());assert reproduction['readout_rows_exact']==88
    metadata.update(stage='completed',run=str(run),actual_forwards=len(events),generated_tokens=sum(len(t['token_ids']) for t in traces),
                    elapsed_seconds=time.monotonic()-started,peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    (master/'run.md').write_text('---\nkind: position-diagnostic\n---\n# Person-bridge position inspection\n\n— PI/OpenAI. Repeated captures, not new cases or a deployable selector. All88 reference rows and complete generations reproduce exactly.\n\n'+str(run/'run.md')+'\n\nForward trace: '+str(master/'forward_trace.jsonl')+'\n')
    print(json.dumps(metadata,indent=1),flush=True);print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
