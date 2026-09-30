"""Independent cached float64 reconstruction; no model inference. — PI/OpenAI"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import torch

out = Path(sys.argv[1])
assert (out / 'source.py').read_bytes() == subprocess.check_output(['git', 'show', 'efd41dc:scripts/english/08_jlens_one_pass.py'])
assert (out / 'config.json').read_bytes() == subprocess.check_output(['git', 'show', 'efd41dc:data/donor_coordinate_validation_v1.json'])
config = json.loads((out / 'config.json').read_text())
assert hashlib.sha256(Path(config['donor_checkpoint']).read_bytes()).hexdigest() == config['donor_sha256']
samples = [json.loads(s) for s in (out / 'samples.jsonl').read_text().splitlines()]
states = torch.load(out / 'states.pt', map_location='cpu', weights_only=True)
coordinate = torch.load(out / 'coordinate.pt', map_location='cpu', weights_only=True)
donor = torch.load(config['donor_checkpoint'], map_location='cpu', weights_only=True)
center = (donor['means']['spider'] + donor['means']['dog']) / 2
direction = donor['means']['spider'] - donor['means']['dog']
direction /= direction.norm()
assert torch.equal(center, coordinate['center']) and torch.equal(direction, coordinate['direction'])
assert len(samples) == len(states) == 16
errors, rows = [], {}
for sample in samples:
    x = states[sample['key']]
    expected = config['prefix'].format(referent=config['referents'][sample['style']][sample['concept']]) + config['endings'][sample['ending_index']]
    assert sample['input'] == expected and sample['input_repr'] == repr(expected)
    assert sample['token_ids'] == x['token_ids'].tolist() and sample['forward_calls'] == 1
    assert x['hidden'].shape == x['embeddings'].shape == (len(sample['token_ids']), 2560)
    h, e = x['hidden'].double(), x['embeddings'].double()
    c, u, ref = [coordinate[k].double() for k in ('center', 'direction', 'reference_embedding')]
    raw = (h - c) @ u
    corrected = ((h - e) - (c - ref)) @ u
    for values, name in [(raw, 'raw_margins'), (corrected, 'corrected_margins')]:
        recorded = torch.tensor(sample[name], dtype=torch.float64)
        errors.append(float((values - recorded).abs().max()))
        assert torch.allclose(values, recorded, rtol=2e-5, atol=2e-5)
    mask = x['token_ids'] == config['reference_token_id']
    assert torch.equal(x['embeddings'][mask].float(), coordinate['reference_embedding'].expand(int(mask.sum()), -1))
    rows[sample['key']] = (float(raw[-1]), float(corrected[-1]))
result = json.loads((out / 'result.json').read_text())
for pair in result['pairs']:
    dog, spider = [rows[pair['key'] + '-' + concept] for concept in ('dog', 'spider')]
    assert abs((spider[0]-dog[0]) - (spider[1]-dog[1])) < 1e-9
    assert pair['raw_brackets'] == (dog[0] < 0 < spider[0])
    assert pair['corrected_brackets'] == (dog[1] < 0 < spider[1])
assert result['raw_brackets'] == result['corrected_brackets'] == 2
assert result['ordered_pairs'] == 8 and not result['candidate_passes_prerequisite']
assert result['n_prefills'] == 16 and result['generated_tokens'] == 0
report = {'author': 'PI/OpenAI', 'status': 'PASS source/config/donor hash and independent float64 reconstruction',
          'max_absolute_reconstruction_error': max(errors), 'n_prefills': 16, 'generated_tokens': 0,
          'raw_brackets': 2, 'corrected_brackets': 2, 'ordered_pairs': 8, 'candidate_passes_prerequisite': False,
          'posthoc_global_threshold_diagnostic': {}}
for i, name in enumerate(('raw', 'corrected')):
    dogs = [r[i] for k, r in rows.items() if k.endswith('-dog')]
    spiders = [r[i] for k, r in rows.items() if k.endswith('-spider')]
    report['posthoc_global_threshold_diagnostic'][name] = {
        'max_dog': max(dogs), 'min_spider': min(spiders), 'separation_interval_width': min(spiders)-max(dogs),
        'strict_global_threshold_exists': max(dogs) < min(spiders),
        'pooled_auroc': sum(float(s>d) + .5*float(s==d) for s in spiders for d in dogs) / 64,
        'limits': 'Eight dependent matched pairs, not64 independent samples; diagnostic only, no cutoff fitted.'}
(out / 'verification.json').write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))
