"""Artifact consistency only; not a neural/rank replay. -- PI/OpenAI"""
import ast
import hashlib
import json
from pathlib import Path

root=Path('out/2026-10-01_060504_jlens-one-pass')
def load(name):return json.loads((root/name).read_text())
traces=load('generation_traces.json'); rendering=load('chat_rendering.json'); rows=load('readout.json')
pipeline=load('pipeline.json'); summaries=load('paired_summary.json')
assert hashlib.sha256((root/'source.py').read_bytes()).hexdigest()==pipeline['source_sha256']
assert hashlib.sha256(Path('data/english_geography_chat_v1.json').read_bytes()).hexdigest()==pipeline['data_sha256']
for name,sha in pipeline['helper_sha256'].items():assert hashlib.sha256((root/'helpers'/name).read_bytes()).hexdigest()==sha
assert len(traces)==4 and len(rows)==72 and len({(r['case_index'],r['method']) for r in rows})==72
for i,(trace,render) in enumerate(zip(traces,rendering['cases'],strict=True)):
    answer='Asia' if i<2 else 'Africa'
    assert ast.literal_eval(render['rendered_repr'])==trace['prompt']
    assert trace['decoded_verbatim']==answer+'<|im_end|>' and trace['scoring_text']==answer
    assert trace['token_ids']==([37186,248046] if i<2 else [71090,248046])
    assert trace['n_tokens']==2 and trace['stopped_on_eos']
    assert all(v==[len(render['input_ids']),1] for v in trace['coverage'].values())
    assert trace['generation_overrides']=={'max_new_tokens':32,'do_sample':False,'use_cache':True,'eos_token_id':[248044,248046]}
    for r in [r for r in rows if r['case_index']==i]:
        assert r['generation_token_ids']==trace['token_ids'] and r['baseline_generation']==trace['decoded_verbatim']
        assert r['prompt']==trace['prompt'] and r['scoring_text']==answer
        assert len(r['top32'])==len(r['selected_ids'])==len(r['selected_scores'])==32
        assert r['selected_scores']==sorted(r['selected_scores'],reverse=True)
for summary in summaries:
    rs=sorted([r for r in rows if r['method']==summary['method']],key=lambda r:r['case_index'])
    assert len(rs)==4 and sum(r['alias_checked_pass'] for r in rs)==summary['joint_alias_passes']
    assert sum(r['alias_checked_auroc'] for r in rs)/4==summary['mean_alias_auroc']
    assert [r['pair_hidden_rank']<r['pair_partner_rank'] for r in rs]==summary['pair_rank_wins']
    assert all(r['r_said']==10**9 for r in rs)
    assert max(abs(r['alias_checked_auroc']-a) for r,a in zip(rs,[1,1,4/7,1],strict=True))<1e-7
result={'signature':'PI/OpenAI','scope':'metadata/coverage/order/hash checks, not model or full-vocabulary score reconstruction',
        'trajectories':4,'generated_tokens':8,'unique_rows':72,'fixed_method_rows_checked':16,
        'mean_auc_mask_membership_pattern':25/28,'max_auc_arithmetic_error':abs(25/28-summaries[0]['mean_alias_auroc']),
        'actual_mask_tensors_reconstructed':False,'full_rank_reconstruction':False,'passed':True}
(root/'metadata_verification.json').write_text(json.dumps(result,indent=1));print(json.dumps(result,indent=1))
