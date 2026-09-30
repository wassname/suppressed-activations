"""Country coordinate algebra and real tiny-Qwen main; no scientific model result. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root = Path(__file__).resolve().parents[2]
entry = root / 'scripts/english/08_jlens_one_pass.py'
g = runpy.run_path(str(entry))['main'].__globals__
tok = AutoTokenizer.from_pretrained(g['q'].MODEL, revision=g['q'].REVISION, local_files_only=True)
config = Qwen3_5TextConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=32,
    num_attention_heads=2, num_key_value_heads=1, head_dim=16, linear_key_head_dim=8, linear_value_head_dim=8,
    linear_num_key_heads=2, linear_num_value_heads=4, max_position_embeddings=128,
    bos_token_id=None, eos_token_id=None, pad_token_id=0,
    rope_parameters={'rope_type':'default', 'rope_theta':10000, 'partial_rotary_factor':1.,
                     'mrope_interleaved':True, 'mrope_section':[3,3,2]})
strings = [' Italy',' Japan',' Rome',' Tokyo',' euro',' yen']
assert all(len(tok.encode(s,add_special_tokens=False)) == 1 for s in strings)
for seed in (0,1):
    torch.manual_seed(seed)
    vectors = torch.randn(32,2) * torch.tensor([1.,3.])
    plain = torch.randn(32,2)
    bases = g['coordinate_swap_bases'](vectors,plain)
    h = torch.randn(3,32)
    swapped = g['swap_coordinates'](h,bases['raw J']['vectors'],bases['raw J']['inverse'])
    inverse64 = torch.linalg.pinv(vectors.double())
    expected64 = h.double() + ((h.double() @ inverse64.T).flip(-1)-h.double() @ inverse64.T) @ vectors.double().T
    assert torch.allclose(swapped.double(),expected64,atol=2e-6,rtol=2e-6)
    assert torch.allclose(swapped @ bases['raw J']['inverse'].T, (h @ bases['raw J']['inverse'].T).flip(-1),atol=1e-5)
    assert torch.allclose(g['swap_coordinates'](swapped,vectors,bases['raw J']['inverse']),h,atol=1e-5)
    unit = g['swap_coordinates'](h,bases['unit J']['vectors'],bases['unit J']['inverse'])
    scores = g['swap_lens_scores'](h,vectors,bases['raw J']['inverse'])
    assert not torch.allclose(swapped,unit) and not torch.allclose(swapped,scores)
    residual = h - (h @ bases['raw J']['inverse'].T) @ vectors.T
    residual_after = swapped - (swapped @ bases['raw J']['inverse'].T) @ vectors.T
    assert torch.allclose(residual,residual_after,atol=2e-6)
    for invalid in (torch.zeros_like(vectors), vectors[:, :1].expand(-1,2)):
        try:
            g['coordinate_swap_bases'](invalid,plain)
        except AssertionError:
            pass
        else:
            raise AssertionError('zero/dependent basis accepted')
    print(f'PASS algebra seed{seed}: independent float64 solution, coordinates, involution, residual, raw!=unit!=raw-score, rank rejection',flush=True)

    model = Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    model.model.norm.weight.copy_(torch.linspace(-.1,.1,32).to(torch.bfloat16))
    gain = 1. + model.model.norm.weight.float()
    assert not torch.equal(gain,(1.+model.model.norm.weight).float())
    sentinel = model.model.layers[15].register_forward_hook(lambda *args: None)
    original_hooks = [set(block._forward_hooks) for block in model.model.layers]
    with tempfile.TemporaryDirectory(dir=root/'.local') as directory:
        tmp = Path(directory)
        lens_path = tmp/'lens.pt'
        torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32)+.1*torch.randn(32,32),23:torch.randn(32,32)/32**.5}},lens_path)
        g['AutoModelForCausalLM'] = SimpleNamespace(from_pretrained=lambda *a,**kw:model)
        g['hf_hub_download'] = lambda *a,**kw:str(lens_path)
        g['LENS_SHA'] = hashlib.sha256(lens_path.read_bytes()).hexdigest()
        model.cuda = lambda *a,**kw:model
        original_cuda, original_mask = torch.Tensor.cuda,g['q'].prompt_word_mask
        torch.Tensor.cuda = lambda self,*a,**kw:self
        g['q'].prompt_word_mask = lambda prompt,vocab,device: original_mask(prompt,vocab,'cpu')
        try:
            for relation in ('capital','currency'):
                early_stop = seed == 1 and relation == 'currency'
                if early_stop:
                    model.lm_head.bias = torch.nn.Parameter(torch.zeros(len(tok),dtype=torch.bfloat16))
                    model.lm_head.bias[tok.eos_token_id] = 1000
                    model.generation_config.eos_token_id = tok.eos_token_id
                g['ROOT'] = tmp/relation
                g['ROOT'].mkdir()
                forward_inputs = []
                def record_input(_module,args,kwargs):
                    ids = kwargs['input_ids'] if 'input_ids' in kwargs else args[0]
                    forward_inputs.append(ids.clone())
                input_handle = model.register_forward_pre_hook(record_input,with_kwargs=True)
                try:
                    out = g['main'](relation=relation,prompt_positions=1)
                finally:
                    input_handle.remove()
                records = json.loads((out/'interventions.json').read_text())
                assert list(records) == ['Base','raw J-coordinate exchange','unit J-coordinate exchange','raw plain-coordinate exchange','matched-random delta']
                inputs = torch.load(out/'basis_inputs.pt',weights_only=True)
                assert torch.equal(inputs['gain'],gain)
                expected_rows = model.lm_head.weight[[14898,6124]].float()*gain
                assert torch.equal(inputs['raw_plain'],expected_rows.T)
                matrices = torch.load(out/'coordinate_bases.pt',weights_only=True)
                direction = torch.load(out/'random_direction.pt',weights_only=True)
                assert torch.allclose(direction.norm(),torch.tensor(1.),atol=1e-6)
                offset = 0
                source,target = g['RELATIONS'][relation][0]
                source_ids = tok(source,return_tensors='pt',add_special_tokens=False).input_ids
                for mode,r in records.items():
                    n = r['n_tokens']
                    assert n == (1 if early_stop else 32) and len(r['coverage']) == n
                    if early_stop:
                        assert r['token_ids'] == [tok.eos_token_id] and r['r2'] == 0
                    assert torch.equal(forward_inputs[offset],source_ids)
                    for j in range(1,n):
                        assert forward_inputs[offset+j].tolist() == [[r['token_ids'][j-1]]]
                    offset += n
                    assert r['input_repr'] == repr(source) and r['generation'] == tok.decode(r['token_ids'])
                    assert r['selected_prompt_token_ids'] == source_ids[0,-1:].tolist()
                    assert r['coverage'][0]['sequence_length'] == source_ids.shape[1]
                    assert all(c['positions']==1 and c['sequence_length']==1 for c in r['coverage'][1:])
                    states = torch.load(out/(mode.lower().replace(' ','-')+'-states.pt'),weights_only=True)
                    assert states.shape == (n,3,1,1,32)
                    before,requested,applied = states[:,0],states[:,1],states[:,2]
                    assert torch.equal(applied,requested.to(torch.bfloat16).float())
                    if mode == 'Base':
                        assert torch.equal(before,requested) and r['answer_log_odds_shift']==0
                    elif mode == 'matched-random delta':
                        b = matrices['raw J']; delta = g['swap_coordinates'](before,b['vectors'],b['inverse'])-before
                        assert torch.allclose(requested,before+delta.norm(dim=-1,keepdim=True)*direction,atol=1e-6)
                    else:
                        b = matrices[r['coordinate_kind']]
                        expected = g['swap_coordinates'](before,b['vectors'],b['inverse'])
                        assert torch.allclose(expected,requested,atol=2e-6,rtol=2e-6)
                        assert all(c['coordinate_applied_error'] <= c['cast_coordinate_error_bound']+1e-3 for c in r['coverage'])
                    assert (out/mode.lower().replace(' ','-')/'run.md').is_file()
                assert len(forward_inputs) == offset+1
                assert torch.equal(forward_inputs[-1],tok(target,return_tensors='pt',add_special_tokens=False).input_ids)
                assert [set(block._forward_hooks) for block in model.model.layers] == original_hooks
                assert not (out/'readout.json').is_file() or json.loads((out/'readout.json').read_text()) == []
                clean = model.generate(source_ids,max_new_tokens=32,do_sample=False,repetition_penalty=1.,use_cache=True)
                assert clean[0,source_ids.shape[1]:].tolist() == records['Base']['token_ids']
                print(f'PASS main seed{seed}/{relation}: real32-layer BF16 Qwen,5x{1 if early_stop else 32} tokens+one post-target prefill, exact decode inputs/coverage,3 exchange bases, own-state fixed random, casts, correct float32 gain, Base replay, foreign hook ownership, all artifacts',flush=True)
        finally:
            torch.Tensor.cuda,g['q'].prompt_word_mask = original_cuda,original_mask
    sentinel.remove()
for arguments in ({'relation':'capital'}, {'relation':'currency','prompt_positions':1,'swap_logits':True},
                  {'relation':'capital','prompt_positions':1,'cases_json':Path('forbidden.json')}):
    try:
        g['main'](**arguments)
    except AssertionError:
        pass
    else:
        raise AssertionError('incompatible country settings accepted')
print('PASS fixed-setting guards. CPU random-model smoke only; no 4B scientific outcome.',flush=True)
