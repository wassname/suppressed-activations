"""Production validation on tiny random hybrid Qwen, real tokenizer and file I/O. — PI/OpenAI"""

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
from loguru import logger
from tabulate import tabulate
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

root = Path.cwd()
source = root / 'scripts/english/08_jlens_one_pass.py'
namespace = dict(globals(), ROOT=root, __file__=str(source))
for path, names in [(root / 'scripts/demo.py', {'layer_hooks'}),
                    (source, {'donor_margins', 'validate_donor_coordinates'})]:
    nodes = [n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
torch.set_num_threads(1)
torch.set_grad_enabled(False)
tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B', revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a', local_files_only=True)
config = Qwen3_5TextConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=16,
                         num_attention_heads=2, num_key_value_heads=1, head_dim=16,
                         linear_key_head_dim=8, linear_value_head_dim=8, linear_num_key_heads=2,
                         linear_num_value_heads=4, max_position_embeddings=128,
                         rope_parameters={'rope_type': 'default', 'rope_theta': 10000,
                                          'partial_rotary_factor': 1.0, 'mrope_interleaved': True,
                                          'mrope_section': [3, 3, 2]})
for seed in (0, 1):
    torch.manual_seed(seed)
    model = Qwen3_5ForCausalLM(config).eval()
    with tempfile.TemporaryDirectory(prefix='donor-smoke-', dir=root / '.local') as temp:
        out = Path(temp)
        fixture = json.loads((root / 'data/donor_coordinate_validation_v1.json').read_text())
        donor_path = out / 'donors.pt'
        q = SimpleNamespace(MODEL='tiny-random-Qwen3_5', REVISION=f'seed{seed}')
        namespace['q'] = q
        torch.save({'means': {'dog': torch.randn(32), 'spider': torch.randn(32)},
                    'provenance': {'model': q.MODEL, 'model_revision': q.REVISION,
                                   'block_index': 15, 'samples': [{'token_ids': [1049]}]}}, donor_path)
        fixture['donor_checkpoint'] = str(donor_path)
        fixture['donor_sha256'] = hashlib.sha256(donor_path.read_bytes()).hexdigest()
        config_path = out / 'fixture.json'
        config_path.write_text(json.dumps(fixture))
        before_hooks = [dict(layer._forward_hooks) for layer in model.model.layers]
        namespace['validate_donor_coordinates'](model, tok, config_path, out)
        assert before_hooks == [dict(layer._forward_hooks) for layer in model.model.layers]
        result = json.loads((out / 'result.json').read_text())
        samples = [json.loads(s) for s in (out / 'samples.jsonl').read_text().splitlines()]
        states = torch.load(out / 'states.pt', weights_only=True)
        coordinate = torch.load(out / 'coordinate.pt', weights_only=True)
        assert result['n_prefills'] == len(samples) == len(states) == 16
        assert result['generated_tokens'] == 0
        for sample in samples:
            tensors = states[sample['key']]
            raw = (tensors['hidden'].double() - coordinate['center'].double()) @ coordinate['direction'].double()
            corrected = ((tensors['hidden'].double() - tensors['embeddings'].double()) -
                         (coordinate['center'].double() - coordinate['reference_embedding'].double())) @ coordinate['direction'].double()
            assert torch.allclose(raw, torch.tensor(sample['raw_margins'], dtype=torch.float64), atol=2e-5, rtol=2e-5)
            assert torch.allclose(corrected, torch.tensor(sample['corrected_margins'], dtype=torch.float64), atol=2e-5, rtol=2e-5)
        print(f'PASS tiny hybrid Qwen seed={seed}: 16 real prefills, no generation, full I/O, independent float64 projection and hook cleanup', flush=True)
