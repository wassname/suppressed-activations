"""2721 geometry reconstruction from pinned weights and saved states; no inference. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import sys

from safetensors import safe_open
import torch


torch.set_num_threads(4)
master = Path(sys.argv[1])
load = lambda path: json.loads(path.read_text())
pipeline = load(master / 'pipeline.json')
assert pipeline['native_metric_erasure'] and pipeline['stage'] == 'completed'
run = Path(pipeline['run'])
reference = Path(pipeline['reference_run'])
current = torch.load(run / 'prefill.pt', weights_only=True, map_location='cpu')
previous = torch.load(reference / 'prefill.pt', weights_only=True, map_location='cpu')
assert len(current) == len(previous) == 6
for a, b in zip(current, previous, strict=True):
    assert a.keys() == b.keys() and all(torch.equal(a[k], b[k]) for k in a)
traces = load(run / 'generation_traces.json')
rows = {(r['case_index'], r['method']): r for r in load(run / 'readout.json')}
model_dir = Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
weight_map = load(model_dir / 'model.safetensors.index.json')['weight_map']
key = 'model.language_model.norm.weight'
with safe_open(model_dir / weight_map[key], framework='pt', device='cpu') as f:
    gain = (1. + f.get_tensor(key).float()).double()
lens_path = Path('/home/code/.cache/huggingface/hub/models--neuronpedia--jacobian-lens/snapshots/16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a/qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt')
with lens_path.open('rb') as stream:
    assert hashlib.file_digest(stream, 'sha256').hexdigest() == '1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e'
J = torch.load(lens_path, weights_only=True, map_location='cpu')['J'][23].double()
B = gain[:, None] * J
noise = torch.randn(2560, generator=torch.Generator(device='cpu').manual_seed(0), dtype=torch.float32).double()
max_direction_error = max_request_error = max_coordinate_error = max_norm_match_error = 0.
max_head_quantization_ratio = 0.
records = []
key = 'model.language_model.embed_tokens.weight'
with safe_open(model_dir / weight_map[key], framework='pt', device='cpu') as f:
    weights = f.get_slice(key)
    for i, generation in enumerate(traces):
        w = weights[generation['token_ids'][0]:generation['token_ids'][0]+1].flatten().double()
        base = w / (w @ w)
        a = B.T @ w
        native = B @ a / (a @ a)
        plain = gain.square() * w / ((gain.square() * w) @ w)
        orthogonal = noise - base * (noise @ w)
        random = base + (native-base).norm() * orthogonal / orthogonal.norm()
        directions = {'J-lens': native, 'plain24': plain, 'plain27': plain, 'random0 J-lens': random}
        saved = torch.load(run / f'native_metric_readouts/{i:03d}.pt', weights_only=True, map_location='cpu')
        metadata = load(run / f'native_metric_readouts/{i:03d}.json')
        recorded = {(t['point'], t['head']): t for t in metadata['traces']}
        assert len(recorded) == 12
        for point, values in saved['states'].items():
            assert set(values) == set(directions)
            for head, state in values.items():
                assert torch.equal(state['output_embedding'].double(), w)
                y, requested, applied, d = [state[k].double() for k in ('original', 'requested', 'applied', 'direction')]
                direction_error = float((d-directions[head]).norm() / directions[head].norm())
                max_direction_error = max(max_direction_error, direction_error)
                assert direction_error < 1e-5, (i, point, head, direction_error)
                c = .5 * (y @ w)
                request_error = float((requested-(y-c*directions[head])).norm() / y.norm())
                max_request_error = max(max_request_error, request_error)
                assert request_error < 1e-5, (i, point, head, request_error)
                assert torch.equal(requested.to(torch.bfloat16).double(), applied)
                coordinate_error = float(abs(requested @ w-c) / (y.norm()*w.norm()))
                max_coordinate_error = max(max_coordinate_error, coordinate_error)
                assert coordinate_error < 1e-5
                prefix = 'end-pass ' + (point+' ' if point != 'final' else '')
                method = prefix+'input-prefix metric-erased0.5 '+head
                selected = rows[i, method]['selected_ids']
                selected_weights = torch.cat([weights[t:t+1] for t in selected]).double()
                exact_scores = selected_weights @ applied
                observed = saved['scores'][method][selected].double()
                bf = observed.to(torch.bfloat16)
                spacing = torch.maximum((torch.nextafter(bf, torch.full_like(bf, torch.inf)).double()-observed).abs(),
                                        (torch.nextafter(bf, torch.full_like(bf, -torch.inf)).double()-observed).abs())
                eps = torch.finfo(torch.float32).eps
                gamma = 2560*eps/(1-2560*eps)
                bound = .5*spacing + gamma*(selected_weights*applied).abs().sum(-1)
                quantization_ratio = float(((exact_scores-observed).abs()/bound).max())
                max_head_quantization_ratio = max(max_head_quantization_ratio, quantization_ratio)
                assert quantization_ratio <= 1, (i, point, head, quantization_ratio)
                trace = recorded[point, head]
                expected = {'before': float(y@w), 'requested_after': float(requested@w),
                            'applied_after': float(applied@w), 'old_requested_norm': float((c*base).norm()),
                            'requested_norm': float((c*d).norm()), 'applied_norm': float((y-applied).norm()),
                            'original_norm': float(y.norm())}
                assert all(abs(expected[k]-trace[k]) <= 2e-5*max(1,abs(expected[k])) for k in expected), (i, point, head)
                records.append({'case_index': i, 'point': point, 'head': head,
                    'requested_coordinate_relative_error': coordinate_error,
                    'realized_coordinate_error': float(applied@w-c),
                    'requested_to_old_norm': trace['requested_norm']/trace['old_requested_norm'],
                    'requested_norm': trace['requested_norm'], 'applied_norm': trace['applied_norm']})
            j, r = recorded[point, 'J-lens'], recorded[point, 'random0 J-lens']
            norm_error = abs(j['requested_norm']-r['requested_norm'])/j['requested_norm']
            max_norm_match_error = max(max_norm_match_error, norm_error)
            assert norm_error < 1e-5
assert len(records) == 72
result = {'checked_corrections': 72, 'independently_reconstructed_selected_head_scores': 72*32,
          'final_states_exact_to_reference': True, 'max_relative_direction_error': max_direction_error,
          'max_relative_request_error': max_request_error, 'max_requested_coordinate_relative_error': max_coordinate_error,
          'max_requested_random_norm_relative_error': max_norm_match_error,
          'max_selected_score_error_over_bf16_rounding_plus_float32_accumulation_bound': max_head_quantization_ratio,
          'scope': 'Pinned-weight float64 direction/request and selected-head reconstruction from saved normalized states; not independent transformer replay or full-vocabulary head reconstruction.',
          'records': records}
(master/'geometry_verification.json').write_text(json.dumps(result, indent=1)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'}, indent=1), flush=True)
