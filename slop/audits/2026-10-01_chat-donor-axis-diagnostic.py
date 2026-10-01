"""Posthoc geometry on saved states; never an editor input or a fitted replacement. — PI/OpenAI"""
import json
from pathlib import Path
import torch

torch.set_num_threads(4)
root=Path('out/2026-10-01_132256_chat-causal-joint')
p=json.loads((root/'pipeline.json').read_text())
a=torch.load(Path(p['prepared'])/'donors.pt',weights_only=True,map_location='cpu')
dog,spider=(a['means'][k].double() for k in ('dog','spider'))
delta=spider-dog;u=delta/delta.norm();center=(dog+spider)/2
rows=[];source_states={}
for group in p['case_runs']:
    name=group['case']['name'];run=Path(group['run'])
    for condition in ('base','role-aligned-donor'):
        states=torch.load(run/(condition+'-states.pt'),weights_only=True,map_location='cpu')
        before,requested,applied=states[0].reshape(3,-1).double()
        if condition=='base':source_states[name]=before
        rows.append({'case':name,'condition':condition,'source_coordinate':float((before-center)@u),
            'requested_coordinate':float((requested-center)@u),'applied_coordinate':float((applied-center)@u),
            'orthogonal_to_axis_norm':float(((before-center)-((before-center)@u)*u).norm())})
contrast=source_states['spider_to_dog']-source_states['dog_to_spider']
result={'signature':'PI/OpenAI','posthoc':True,'scope':'Saved-state projection only; does not establish a causal feature, calibrate a threshold, fit a new direction or measure necessity.',
 'donor_endpoints':{'dog':float((dog-center)@u),'spider':float((spider-center)@u)},
 'cases':rows,'task_pair_difference_norm':float(contrast.norm()),'task_pair_coordinate_gap':float(contrast@u),
 'task_pair_fraction_squared_norm_on_donor_axis':float((contrast@u).square()/contrast.square().sum()),
 'caution':'Task prompts differ in descriptions and lengths; their difference is not isolated concept ground truth. Same-sign coordinates alone do not invalidate additive steering.'}
(root/'donor_axis_diagnostic.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1),flush=True)
