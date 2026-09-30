"""Archived CPU reproduction for prefill capture and hook ownership. — PI/OpenAI"""
import ast
from contextlib import contextmanager
from functools import partial
from itertools import product
from pathlib import Path
import faulthandler

faulthandler.dump_traceback_later(60, repeat=True)
import torch
from transformers import LlamaConfig, LlamaForCausalLM, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root = Path(__file__).resolve().parents[2]
for file, name in [('scripts/demo.py', 'layer_hooks'), ('scripts/english/08_jlens_one_pass.py', 'generate_readout')]:
    tree = ast.parse((root / file).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), file, 'exec'))

models = [
    (LlamaForCausalLM, LlamaConfig(vocab_size=32, hidden_size=16, intermediate_size=32, num_hidden_layers=32,
                                 num_attention_heads=2, num_key_value_heads=2, max_position_embeddings=64,
                                 bos_token_id=1, eos_token_id=None, pad_token_id=0)),
    (Qwen3_5ForCausalLM, Qwen3_5TextConfig(vocab_size=32, hidden_size=32, intermediate_size=64, num_hidden_layers=32,
                                         num_attention_heads=2, num_key_value_heads=1, head_dim=16,
                                         linear_key_head_dim=8, linear_value_head_dim=8,
                                         linear_num_key_heads=2, linear_num_value_heads=4,
                                         max_position_embeddings=64, bos_token_id=1, eos_token_id=None, pad_token_id=0,
                                         rope_parameters={'rope_type':'default', 'rope_theta':10000,
                                                          'partial_rotary_factor':1.0, 'mrope_interleaved':True,
                                                          'mrope_section':[3,3,2]})),
]
for seed, (constructor, config) in product((0, 1), models):
    torch.manual_seed(seed)
    model = constructor(config).eval()
    ids = torch.tensor([[1, 4, 7, 9]])
    sentinel = model.model.layers[23].register_forward_hook(lambda _module, _args, _out: None)
    def check_hooks():
        assert sentinel.id in model.model.layers[23]._forward_hooks
        hooks = [h for block in model.model.layers for h in block._forward_hooks.values()]
        assert not any(isinstance(h, partial) and h.func.__qualname__ == 'generate_readout.<locals>.capture' for h in hooks)
        print('Remaining hook types:', sorted({type(h).__name__ for h in hooks}), flush=True)
    states, tokens, coverage = generate_readout(model, ids, 23)
    baseline = model.generate(ids, max_new_tokens=8, do_sample=False, use_cache=True)
    assert tokens == baseline[0, ids.shape[1]:].tolist()
    final = {}
    def capture_final(_module, inputs):
        final['raw'] = inputs[0].clone()
    handle = model.model.norm.register_forward_pre_hook(capture_final)
    reference = model(ids, output_hidden_states=True, use_cache=False)
    handle.remove()
    for layer in (24, 27):
        assert torch.allclose(states[layer], reference.hidden_states[layer][0], rtol=1e-4, atol=1e-6)
    assert torch.allclose(states[32], final['raw'][0], rtol=1e-4, atol=1e-6)
    assert all(c == [4] + [1] * 7 for c in coverage.values())
    check_hooks()
    model.generation_config.eos_token_id = tokens[0]
    states_eos, tokens_eos, coverage_eos = generate_readout(model, ids, 26)
    assert tokens_eos == tokens[:1]
    assert set(states_eos) == {27, 32}
    assert all(c == [4] for c in coverage_eos.values())
    check_hooks()
    sentinel.remove()
    print(f'PASS {config.model_type} seed={seed}: unchanged generation; correct raw states24/27/32; cached coverage; early EOS; duplicate layer; own hooks removed, foreign hook preserved', flush=True)
faulthandler.cancel_dump_traceback_later()
print('PASS production helper on tiny real Llama and hybrid Qwen3.5; full-size BF16 parity remains to be tested', flush=True)
