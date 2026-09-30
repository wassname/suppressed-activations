"""Tiny real-Qwen preparation, validation and production-hook smoke. — PI/OpenAI"""

import ast
import hashlib
import json
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import torch
from torch import Tensor
from loguru import logger
from tabulate import tabulate
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

ROOT = Path.cwd()
source = ROOT / 'scripts/english/08_jlens_one_pass.py'
tree = ast.parse(source.read_text())
ns = dict(globals(), __file__=str(source))
for path, names in [(ROOT / 'scripts/demo.py', {'layer_hooks', 'replace_output'}),
                    (source, {'nuisance_coordinate', 'fit_nuisance_from_run', 'donor_margins',
                              'validate_donor_coordinates', 'reflect_donor_side'})]:
    nodes = [n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
hook = next(n for n in ast.walk(main) if isinstance(n, ast.FunctionDef) and n.name == 'hook')
mode_loop = next(n for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'mode')
readers = [n for n in main.body if isinstance(n, ast.FunctionDef) and n.name in {'readout', 'top_words'}]
torch.set_num_threads(1)
torch.set_grad_enabled(False)
tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B', revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a', local_files_only=True)
config = Qwen3_5TextConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=16,
                         num_attention_heads=2, num_key_value_heads=1, head_dim=16,
                         linear_key_head_dim=8, linear_value_head_dim=8, linear_num_key_heads=2,
                         linear_num_value_heads=4, max_position_embeddings=128,
                         rope_parameters={'rope_type':'default', 'rope_theta':10000, 'partial_rotary_factor':1.0,
                                          'mrope_interleaved':True, 'mrope_section':[3,3,2]})
for seed in (0, 1):
    torch.manual_seed(seed)
    model = Qwen3_5ForCausalLM(config).eval()
    model.generation_config.eos_token_id = None
    with tempfile.TemporaryDirectory(prefix='nuisance-smoke-', dir=ROOT / '.local') as temp:
        root = Path(temp)
        train, validation = root / 'train', root / 'validation'
        train.mkdir(); validation.mkdir()
        q = SimpleNamespace(MODEL='tiny-random-Qwen3_5', REVISION=f'seed{seed}')
        ns['q'] = q
        means = {'dog': torch.randn(32), 'spider': torch.randn(32)}
        donor_path = root / 'donors.pt'
        torch.save({'means': means, 'provenance': {'model':q.MODEL, 'model_revision':q.REVISION,
                    'block_index':15, 'samples':[{'token_ids':[1049]}]}}, donor_path)
        cfg1 = json.loads((ROOT / 'data/donor_coordinate_validation_v1.json').read_text())
        cfg1.update(donor_checkpoint=str(donor_path), donor_sha256=hashlib.sha256(donor_path.read_bytes()).hexdigest())
        path1 = root / 'v1.json'; path1.write_text(json.dumps(cfg1))
        ns['validate_donor_coordinates'](model, tok, path1, train)
        cfg2 = json.loads((ROOT / 'data/donor_coordinate_validation_v2.json').read_text())
        cfg2.update(donor_checkpoint=str(donor_path), donor_sha256=cfg1['donor_sha256'], training_run=str(train),
                    training_states_sha256=hashlib.sha256((train/'states.pt').read_bytes()).hexdigest(),
                    training_coordinate_sha256=hashlib.sha256((train/'coordinate.pt').read_bytes()).hexdigest())
        path2 = root / 'v2.json'; path2.write_text(json.dumps(cfg2))
        fitted = ns['fit_nuisance_from_run'](cfg2, validation)
        result = ns['validate_donor_coordinates'](model, tok, path2, validation, fitted)
        samples = [json.loads(s) for s in (validation/'samples.jsonl').read_text().splitlines()]
        states = torch.load(validation/'states.pt', weights_only=True)
        assert len(samples) == len(states) == result['n_prefills'] == 16 and result['generated_tokens'] == 0
        for sample in samples:
            x = states[sample['key']]['hidden'].double()
            expected = (x-fitted['center'].double()) @ fitted['direction'].double()
            assert torch.allclose(expected, torch.tensor(sample['corrected_margins'], dtype=torch.float64), atol=2e-5, rtol=2e-5)
        assert result['candidate_passes_prerequisite'] == all(p['corrected_dog'] < 0 < p['corrected_spider'] for p in result['pairs'])
        print(f'PASS seed={seed}: real preparation/fit/new validation/I-O/float64 replay; gate={result["candidate_passes_prerequisite"]} is not forced', flush=True)
        ids = tok(samples[0]['input'], return_tensors='pt', add_special_tokens=False).input_ids
        full_delta = means['spider']-means['dog']
        raw_direction = full_delta/full_delta.norm()
        raw_vectors = model.get_input_embeddings().weight[[5388,33213]].float().T
        inverse = torch.linalg.pinv(raw_vectors)
        ns.update(model=model, W=model.lm_head.weight, J=torch.eye(32), J_edit=torch.eye(32),
                  vocab=tok.convert_ids_to_tokens(list(range(len(tok)))), mask=torch.zeros(len(tok), dtype=torch.bool),
                  donor_reflection=True, donor_checkpoint=donor_path, raw_donor_center=(means['dog']+means['spider'])/2,
                  raw_donor_direction=raw_direction, donor_center=fitted['center'], donor_direction=fitted['direction'],
                  reflection_mode='context-projected donor reflection', reflection_noise=torch.nn.functional.normalize(torch.randn(32), dim=0),
                  donor_deltas={'full donor contrast':full_delta}, prompt_start=-1, decode_scale=1.0,
                  raw_vectors_j=raw_vectors, inverse_j=inverse, block=15, read_block=15)
        exec(compile(ast.Module(body=readers+[hook], type_ignores=[]), str(source), 'exec'), ns)
        initial_norms = {}
        for mode in ('Base','raw donor reflection','context-projected donor reflection','full donor contrast','matched-random reflection control'):
            ns.update(mode=mode, calls=[], readings=[])
            exec(compile(ast.Module(body=[mode_loop.body[0]], type_ignores=[]), str(source), 'exec'), ns)
            before = [dict(layer._forward_hooks) for layer in model.model.layers]
            with ns['layer_hooks'](model.model.layers, {15:ns['hook']}):
                generated = model.generate(ids, attention_mask=torch.ones_like(ids), max_new_tokens=4, do_sample=False, use_cache=True)
            assert before == [dict(layer._forward_hooks) for layer in model.model.layers]
            assert len(ns['calls']) == len(ns['readings']) == generated.shape[1]-ids.shape[1] == 4
            assert [c['positions'] for c in ns['calls']] == [1]*4
            assert [c['sequence_length'] for c in ns['calls']] == [ids.shape[1],1,1,1]
            initial_norms[mode] = ns['calls'][0]['requested_delta_norm'][0]
        assert abs(initial_norms['context-projected donor reflection']-initial_norms['matched-random reflection control']) < 1e-5
        print(f'PASS seed={seed}: actual production mode-coordinate selection and hook,5 conditions x4 tokens, cached coverage, fold assertions, matched prefill random norm and cleanup', flush=True)
