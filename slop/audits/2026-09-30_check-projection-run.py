"""Independent saved-state/least-squares and execution reconstruction. — PI/OpenAI"""

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import torch
from tokenizers import Tokenizer

root = Path(sys.argv[1])
torch.set_num_threads(1)
source = subprocess.check_output(['git','show','4348227:scripts/english/08_jlens_one_pass.py'])
config_bytes = subprocess.check_output(['git','show','4348227:data/donor_coordinate_validation_v2.json'])
assert (root/'source.py').read_bytes() == source
assert (root/'config.json').read_bytes() == config_bytes
config = json.loads(config_bytes)
training = Path(config['training_run'])
for name in ('states','coordinate'):
    assert hashlib.sha256((training/f'{name}.pt').read_bytes()).hexdigest() == config[f'training_{name}_sha256']
assert hashlib.sha256(Path(config['donor_checkpoint']).read_bytes()).hexdigest() == config['donor_sha256']
old_states = torch.load(training/'states.pt', weights_only=True, map_location='cpu')
old_coordinate = torch.load(training/'coordinate.pt', weights_only=True, map_location='cpu')
means = torch.stack([(old_states[f'{style}-{i}-dog']['hidden'][-1].double()+old_states[f'{style}-{i}-spider']['hidden'][-1].double())/2
                     for style in ('explicit','indirect') for i in range(4)])
center = means.mean(0)
M = means-center
old_u = old_coordinate['direction'].double()
tolerance = torch.finfo(torch.float64).eps*max(M.shape)
solution = torch.linalg.lstsq(M.T, old_u, rcond=tolerance, driver='gelsd')
assert int(solution.rank) == 7
retained = old_u-M.T@solution.solution
direction = retained/retained.norm()
fitted = torch.load(root/'projection.pt', weights_only=True, map_location='cpu')
assert torch.equal(fitted['center'], center.float())
assert torch.allclose(fitted['direction'].double(), direction, atol=1e-7, rtol=1e-6)
assert abs(float(retained.norm())-fitted['retained_direction_norm']) < 1e-10
Q = fitted['nuisance_basis']
assert torch.allclose(Q@Q.T, torch.eye(7, dtype=torch.float64), atol=1e-12, rtol=1e-12)
assert torch.allclose(M, (M@Q.T)@Q, atol=1e-12, rtol=1e-12)
assert torch.allclose(M@direction, torch.zeros(8, dtype=torch.float64), atol=1e-12)
raw_coordinate = torch.load(root/'coordinate.pt', weights_only=True, map_location='cpu')
assert torch.equal(raw_coordinate['center'], old_coordinate['center']) and torch.equal(raw_coordinate['direction'], old_coordinate['direction'])
samples = [json.loads(line) for line in (root/'samples.jsonl').read_text().splitlines()]
states = torch.load(root/'states.pt', weights_only=True, map_location='cpu')
expected_pairs = {f'{style}-{i}' for style in config['referents'] for i in range(len(config['endings']))}
expected_keys = {f'{pair}-{concept}' for pair in expected_pairs for concept in ('dog','spider')}
assert len(samples) == len(states) == 16
assert set(states) == {sample['key'] for sample in samples} == expected_keys
tokenizer = Tokenizer.from_file('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json')
errors, margins = [], {}
for sample in samples:
    expected = config['prefix'].format(referent=config['referents'][sample['style']][sample['concept']])+config['endings'][sample['ending_index']]
    assert sample['input'] == expected and sample['input_repr'] == repr(expected)
    assert tokenizer.encode(expected,add_special_tokens=False).ids == sample['token_ids']
    x = states[sample['key']]
    assert sample['token_ids'] == x['token_ids'].tolist() and sample['forward_calls'] == 1
    assert x['hidden'].shape == x['embeddings'].shape == (len(sample['token_ids']),2560)
    h = x['hidden'].double()
    for c,u,name in ((raw_coordinate['center'],raw_coordinate['direction'],'raw_margins'),
                     (fitted['center'],fitted['direction'],'corrected_margins')):
        values = (h-c.double())@u.double()
        recorded = torch.tensor(sample[name], dtype=torch.float64)
        errors.append(float((values-recorded).abs().max()))
        assert torch.allclose(values,recorded,atol=2e-5,rtol=2e-5)
        margins[sample['key'],name] = float(values[-1])
result = json.loads((root/'result.json').read_text())
assert len(result['pairs']) == 8 and {p['key'] for p in result['pairs']} == expected_pairs
paired_decomposition = []
for pair in result['pairs']:
    difference = states[pair['key']+'-spider']['hidden'][-1].double()-states[pair['key']+'-dog']['hidden'][-1].double()
    raw_gap = float(difference@old_u)
    removed_gap = float(difference@(old_u-retained))
    retained_gap = float(difference@retained)
    assert abs(raw_gap-removed_gap-retained_gap) < 1e-12
    paired_decomposition.append({'pair':pair['key'],'raw_gap':raw_gap,'removed_component_gap':removed_gap,
                                  'retained_component_gap':retained_gap,'projected_unit_gap':float(difference@direction)})
    for name,flag in (('raw_margins','raw_brackets'),('corrected_margins','corrected_brackets')):
        d,s = (margins[pair['key']+'-'+concept,name] for concept in ('dog','spider'))
        assert pair[flag] == (d<0<s)
        prefix = 'raw' if name == 'raw_margins' else 'corrected'
        assert abs(pair[prefix+'_dog']-d) < 2e-5 and abs(pair[prefix+'_spider']-s) < 2e-5
        gap_field = 'pair_difference' if name == 'raw_margins' else 'candidate_pair_difference'
        assert abs(pair[gap_field]-(s-d)) < 2e-5
assert result['ordered_pairs'] == sum(p['raw_gap'] > 0 for p in paired_decomposition)
assert result['candidate_ordered_pairs'] == sum(p['projected_unit_gap'] > 0 for p in paired_decomposition)
assert result['corrected_brackets'] == sum(p['corrected_brackets'] for p in result['pairs'])
assert result['raw_brackets'] == sum(p['raw_brackets'] for p in result['pairs'])
passed = result['corrected_brackets'] == 8
assert result['candidate_passes_prerequisite'] == fitted['validation']['passed'] == passed
assert fitted['validation']['result_sha256'] == hashlib.sha256((root/'result.json').read_bytes()).hexdigest()
assert fitted['validation']['config_sha256'] == hashlib.sha256(config_bytes).hexdigest()
assert result['n_prefills'] == 16 and result['generated_tokens'] == 0
pipeline = json.loads((root/'pipeline.json').read_text())
assert pipeline['passed'] == passed and Path(pipeline['validation']) == root.resolve()
assert len(pipeline['causal_runs']) == (2 if passed else 0)
causal = []
for experiment in pipeline['causal_runs']:
    out = Path(experiment['path'])
    assert (out/'source.py').read_bytes() == source
    md = (out/'run.md').read_text()
    for setting in ('block_index: 15\n','reverse: true\n',"prompt_slice: '-1:'\n",'decode_scale: 1.0\n','donor_reflection: true\n'):
        assert setting in md
    rows = json.loads((out/'interventions.json').read_text())
    assert set(rows) == {'Base','raw donor reflection','context-projected donor reflection','full donor contrast','matched-random reflection control'}
    donor = json.loads((out/'donor_provenance.json').read_text())
    assert donor['coordinate']['sha256'] == hashlib.sha256((root/'projection.pt').read_bytes()).hexdigest()
    old_stamp = {'legs':'155111','skeleton_body':'155140'}[experiment['relation']]
    reference = json.loads(Path(f'out/2026-09-30_{old_stamp}_jlens-one-pass/interventions.json').read_text())
    for new,old in [('Base','Base'),('raw donor reflection','conditional donor reflection'),('full donor contrast','full donor contrast')]:
        for field in ('token_ids','generation','top10','prefill_readout','final_decode_readout'):
            assert rows[new][field] == reference[old][field], (new,field)
    special = set(json.loads((out/'tokenizer_special_ids.json').read_text())['r2_excluded_ids'])
    summary = {}
    base = rows['Base']
    for name,row in rows.items():
        calls = row['coverage']
        assert 1 <= len(calls) == row['n_tokens'] == len(row['token_ids']) <= 32
        assert all(c['positions'] == 1 and c['scale'] == 1 for c in calls)
        assert all(c['sequence_length'] == 1 for c in calls[1:])
        assert row['coordinate_kind'] == ('raw' if name == 'raw donor reflection' else 'context projection')
        cast_error = 0
        for c in calls:
            before,requested,applied_margin = (c[k][0] for k in ('donor_margin_before','donor_margin_requested','donor_margin_after'))
            dose,applied = c['requested_delta_norm'][0],c['applied_delta_norm'][0]
            assert c['source_side'] == [before<0]
            if name in ('raw donor reflection','context-projected donor reflection'):
                assert math.isclose(requested,abs(before),rel_tol=1e-5,abs_tol=1e-5)
            if name in ('raw donor reflection','context-projected donor reflection','matched-random reflection control'):
                assert math.isclose(dose,2*max(-before,0),rel_tol=1e-5,abs_tol=1e-5)
            if name == 'full donor contrast':
                assert math.isclose(dose,donor['native_donor_norm'],rel_tol=1e-5,abs_tol=1e-5)
            if dose == 0:
                assert applied == 0 and requested == applied_margin
            cast_error = max(cast_error,abs(applied_margin-requested))
        p0,p1 = row['p_answer0'],row['p_answer1']
        assert abs(math.log(p1/p0)-math.log(base['p_answer1']/base['p_answer0'])-row['answer_log_odds_shift']) < 1e-5
        assert abs(p0+p1-row['answer_pair_mass']) < 1e-6
        ids = [t for t in row['token_ids'] if t not in special]
        bigrams = list(zip(ids,ids[1:]))
        assert abs((1-len(set(bigrams))/len(bigrams) if bigrams else 0)-row['r2']) < 1e-9
        summary[name] = {'first_line':row['generation'].splitlines()[0], 'n_tokens':row['n_tokens'],
                         'max_cast_margin_error':cast_error,'prefill_margin':calls[0]['donor_margin_before'][0],
                         'updated_calls':sum(any(v>0 for v in c['applied_delta_norm']) for c in calls)}
    assert math.isclose(rows['context-projected donor reflection']['coverage'][0]['requested_delta_norm'][0],
                        rows['matched-random reflection control']['coverage'][0]['requested_delta_norm'][0],rel_tol=1e-5,abs_tol=1e-5)
    causal.append({'relation':experiment['relation'],'path':str(out),'conditions':summary})
report = {'author':'PI/OpenAI','status':'PASS saved-source/math/tokenization/gate consistency; NOT semantic certification',
          'retained_norm':float(retained.norm()),'max_absolute_margin_reconstruction_error':max(errors),
          'candidate_brackets':result['corrected_brackets'],'raw_brackets':result['raw_brackets'],
          'prerequisite_passed':passed,'causal':causal,
          'posthoc_paired_margin_decomposition':paired_decomposition,
          'limits':'Reconstruction checks internal consistency, not authenticity of model states or semantic transfer.'}
(root/'verification.json').write_text(json.dumps(report,indent=1))
print(json.dumps(report,indent=1))
