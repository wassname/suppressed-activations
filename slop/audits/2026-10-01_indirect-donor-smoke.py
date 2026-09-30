"""Exercise donor preparation and ten real tiny-model trajectories. -- PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1);torch.set_grad_enabled(False)
root=Path(__file__).resolve().parents[2];entry=root/'scripts/english/08_jlens_one_pass.py'
g=runpy.run_path(str(entry))['main'].__globals__
factory=next(n for n in ast.parse((root/'slop/audits/2026-10-01_vjp-check.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='config')
exec(compile(ast.Module(body=[factory],type_ignores=[]),'tiny-model-config','exec'))
tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(),flush=True)
for seed in (0,1):
 torch.manual_seed(seed);model=Qwen3_5ForCausalLM(config(len(tok))).to(torch.bfloat16).eval().requires_grad_(False)
 before={k:v.clone() for k,v in model.named_parameters()}
 with tempfile.TemporaryDirectory(dir=root/'.local') as directory:
  tmp=Path(directory)
  lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.eye(32)}},lens)
  g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=lambda *a,**kw:model)
  g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
  original_cuda=torch.Tensor.cuda;original_mask=g['q'].prompt_word_mask
  torch.Tensor.cuda=lambda self,*a,**kw:self;model.cuda=lambda *a,**kw:model
  g['q'].prompt_word_mask=lambda prompt,vocab,device:original_mask(prompt,vocab,'cpu')
  events=[];observed=[]
  counter=model.register_forward_pre_hook(lambda *_:events.append(torch.is_grad_enabled()))
  sentinel=model.model.layers[15].register_forward_hook(lambda _m,_a,out:observed.append(out[0,-1].detach().float().clone()))
  try:
   g['ROOT']=tmp/'literal'
   literal=g['main'](prepare_donors_json=root/'data/dog_spider_donors_pronoun_v2.json')
   assert len(events)==8 and not any(events)
   reference=torch.load(literal/'donors.pt',weights_only=True)
   preparation=json.loads((root/'data/dog_spider_donors_indirect_v3.json').read_text())
   preparation.update(literal_control_path=str(literal/'donors.pt'),literal_control_sha256=hashlib.sha256((literal/'donors.pt').read_bytes()).hexdigest())
   data=tmp/'indirect.json';data.write_text(json.dumps(preparation))
   g['ROOT']=tmp/'indirect';events.clear();observed.clear()
   prepared=g['main'](prepare_donors_json=data)
   assert len(events)==8 and not any(events)
   checkpoint=torch.load(prepared/'donors.pt',weights_only=True)
   contexts=[torch.load(p,weights_only=True) for p in sorted((prepared/'donor-contexts').glob('*.pt'))]
   assert len(contexts)==8 and all(torch.equal(c['state'],h) for c,h in zip(contexts,observed,strict=True))
   assert all(c['record']['token_ids'][-1]==tok(' It',add_special_tokens=False).input_ids[0] for c in contexts)
   for concept in ('dog','spider'):
    stacked=torch.stack([c['state'] for c in contexts if c['record']['concept']==concept])
    assert torch.equal(stacked,checkpoint['sample_states'][concept]) and torch.equal(stacked.mean(0),checkpoint['means'][concept])
   existing_hooks=[dict(b._forward_hooks) for b in model.model.layers]
   library_hooks=[h for hooks in existing_hooks for key,h in hooks.items() if key!=sentinel.id]
   assert library_hooks and all(h.__module__=='transformers.utils.output_capturing' and h.__name__=='output_capturing_hook' for h in library_hooks)
   print(f'Observed {len(library_hooks)} persistent Transformers output-capture hooks after preparation; compare ownership rather than require an empty registry',flush=True)
   expected=checkpoint['means']['spider']-checkpoint['means']['dog']
   literal_delta=reference['means']['spider']-reference['means']['dog']
   prior_vectors=None;total=0
   for relation,count in (('legs',4),('skeleton_body',4),('arithmetic_control',2)):
    g['ROOT']=tmp/relation;events.clear();observed.clear()
    out=g['main'](donor_checkpoint=prepared/'donors.pt',indirect_donor=True,reverse=True,prompt_positions=1,decode_scale=.25,relation=relation)
    rows=json.loads((out/'interventions.json').read_text());assert len(rows)==count
    vectors=torch.load(out/'applied_vectors.pt',weights_only=True)
    assert torch.equal(vectors['indirect-description donor'],expected) and torch.equal(vectors['literal-name donor control'],literal_delta)
    assert torch.allclose(vectors['matched-random delta'].norm(),expected.norm(),atol=1e-6)
    if prior_vectors is not None:assert all(torch.equal(v,prior_vectors[k]) for k,v in vectors.items())
    prior_vectors=vectors
    assert len(events)==sum(r['n_tokens'] for r in rows.values()) and not any(events)
    offset=0
    for mode,row in rows.items():
     n=row['n_tokens'];assert n==32 and len(row['coverage'])==n
     assert row['coverage'][0]['positions']==1 and row['coverage'][0]['scale']==1
     assert all(c['positions']==c['sequence_length']==1 and c['scale']==.25 for c in row['coverage'][1:])
     states=torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True)
     assert torch.equal(states[:,2,0,0],torch.stack(observed[offset:offset+n]));offset+=n
     delta=torch.zeros(32) if mode=='Base' else vectors[mode]
     for j,(original,requested,applied) in enumerate(states):
      proposal=original+delta
      if j:proposal=original+.25*(proposal-original)
      assert torch.equal(requested,proposal) and torch.equal(applied,proposal.to(torch.bfloat16).float())
     if relation=='arithmetic_control':assert row['expected_answer']=='4'
    total+=len(rows)
   assert total==10 and all(torch.equal(before[k],v) for k,v in model.named_parameters())
   assert all(p.grad is None for p in model.parameters()) and sentinel.id in model.model.layers[15]._forward_hooks
   assert [dict(b._forward_hooks) for b in model.model.layers]==existing_hooks
   original_trajectory=g['trajectory'];completed=0
   def interrupted(*args):
    global completed
    if completed==3:raise RuntimeError('fixture interruption after3')
    result=original_trajectory(*args);completed+=1;return result
   partial=tmp/'partial';partial.mkdir();g['trajectory']=interrupted
   try:
    g['prepare_donors'](model,tok,15,data,partial)
    raise AssertionError('missing interruption')
   except RuntimeError as error:assert str(error)=='fixture interruption after3'
   finally:g['trajectory']=original_trajectory
   retained=[torch.load(p,weights_only=True) for p in sorted((partial/'donor-contexts').glob('*.pt'))]
   assert len(retained)==3 and not (partial/'donors.pt').exists()
   assert all(torch.equal(c['state'],contexts[i]['state']) for i,c in enumerate(retained))
   print(f'PASS seed{seed}: literal/indirect real preparation;8 indirect prefills; exact means/common It/capture states;10 trajectories and320 tokens, no extra eval forwards/gradients; unchanged weights/foreign hooks; identical vectors across properties; natural literal control and matched random; exact requested/BF16 states; interruption retains3 completed contexts',flush=True)
  finally:
   counter.remove();sentinel.remove();torch.Tensor.cuda=original_cuda;g['q'].prompt_word_mask=original_mask
print('PASS tiny random CPU models only; no pretrained scientific result',flush=True)
