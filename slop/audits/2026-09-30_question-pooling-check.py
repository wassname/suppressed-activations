"""Production pooling/capture checks on CPU; not scientific evidence. -- PI/OpenAI"""
import ast
from contextlib import contextmanager
from functools import partial
import hashlib
import json
from pathlib import Path
import tempfile

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root = Path(__file__).resolve().parents[2]
source = root/'scripts/english/08_jlens_one_pass.py'
tree = ast.parse(source.read_text())
for path,names in [(root/'scripts/demo.py',{'layer_hooks'}), (source,{'generate_readout','question_positions','capture_question_prefills','position_pooling_scores'})]:
    nodes = [n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'))
span = question_positions([1,2,3,4,5], [(0,3),(3,6),(6,7),(7,8),(8,10)], [0,0,0,1,0], {3}, 5, 10)
assert span==[4]
for seed in (0,1):
    torch.manual_seed(seed)
    z,f,other = torch.randn(7,257,dtype=torch.float64),torch.randn(257,dtype=torch.float64),torch.randn(257,dtype=torch.float64)
    result,maximum,last,final,other_p,peak = position_pooling_scores(z,f,other)
    direct = (z.softmax(-1)-f.softmax(-1)).max(0).values
    assert torch.allclose(result['pooled'],direct.masked_fill(direct<=0,-torch.inf),atol=1e-14,rtol=1e-14)
    assert torch.equal(peak,z.softmax(-1).argmax(0))
    one = position_pooling_scores(z[-1:],f,other)[0]
    assert torch.equal(one['pooled'],one['pooling last'])
    shifted = position_pooling_scores(z+torch.arange(7)[:,None],f+3,other-2)[0]
    assert all(torch.allclose(result[k],shifted[k],atol=1e-14,rtol=1e-14) for k in result)
    empty = position_pooling_scores(z[-1:],z[-1],z[-1])[0]
    assert all(torch.isneginf(empty[k]).all() for k in ('pooled','pooling last','pooled mismatched'))
    assert not torch.equal(result['pooled'],result['pooled mismatched'])
    mask = torch.zeros(257,dtype=torch.bool); mask[:100]=True
    for score in result.values():
        masked=score.masked_fill(mask,-torch.inf)
        top=[i for i in masked.argsort(descending=True,stable=True)[:32].tolist() if torch.isfinite(masked[i])]
        expected=sorted((i for i in range(257) if torch.isfinite(masked[i])),key=lambda i:(-float(masked[i]),i))[:32]
        assert top==expected and not set(top).intersection(range(100))
    print(f'PASS seed{seed}: full-vocabulary arithmetic, constant final-last comparator, singleton identity, shifts, positivity, masks and ranking',flush=True)

equal=torch.zeros(2,40,dtype=torch.float64)
f=torch.cat([torch.full((20,),-4.),torch.zeros(20)]).double()
tied=position_pooling_scores(equal,f,f)
assert tied[-1].tolist()==[0]*40
assert [i for i in tied[0]['pooled'].argsort(descending=True,stable=True)[:32].tolist() if torch.isfinite(tied[0]['pooled'][i])]==list(range(20))
print('PASS exact token/position ties and fewer-than32 eligible tokens',flush=True)

tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
special = set(tok.all_special_ids)|{i for i,t in tok.added_tokens_decoder.items() if t.special}
prefix='Fact: The capital of Japan is Tokyo.\n'
prompts=[prefix+'Fact: The fruit is',prefix+'Fact: The shape is']
config = Qwen3_5TextConfig(vocab_size=len(tok),hidden_size=32,intermediate_size=64,num_hidden_layers=32,
    num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
    linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=128,bos_token_id=None,eos_token_id=None,pad_token_id=0,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,'mrope_interleaved':True,'mrope_section':[3,3,2]})
main = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
branch = next(n for n in ast.walk(main) if isinstance(n,ast.If) and ast.unparse(n.test)=='pool_question' and any(isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='positions' for t in x.targets) for x in n.body))
readout_node = next(n for n in ast.walk(main) if isinstance(n,ast.FunctionDef) and n.name=='readout')
for seed in (0,1):
    torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(config).eval()
    with tempfile.TemporaryDirectory(dir=root/'.local') as tmp:
        tmp=Path(tmp); reference=tmp/'reference'; out=tmp/'captured'; reference.mkdir();out.mkdir()
        old, traces=[],[]
        for prompt in prompts:
            ids=tok(prompt,return_tensors='pt',add_special_tokens=False).input_ids
            res,generated,coverage=generate_readout(model,ids,23)
            old.append({r:h[-1].cpu() for r,h in res.items()})
            traces.append({'prompt':prompt,'token_ids':generated,'coverage':coverage})
        torch.save(old,reference/'prefill.pt')
        (reference/'generation_traces.json').write_text(json.dumps(traces))
        (reference/'source.py').write_text('fixture, not model evidence -- PI/OpenAI')
        captured, generations, spans=capture_question_prefills(model,tok,prompts,prefix,23,special,reference,out)
        assert len(captured)==len(spans)==2
        assert torch.equal(torch.load(out/'prefill_positions.pt',weights_only=True)[0][24],captured[0][24])
        assert json.loads((out/'capture_reference.json').read_text())['last_states_and_generated_ids_equal']
        assert all(len(g['token_ids'])==8 for g in generations)
        for s in spans:
            assert all(s['offsets'][i][0]>=len(prefix) for i in s['positions'])
            assert s['positions'][-1]==len(s['input_ids'])-1
        W=model.lm_head.weight; J=torch.randn(32,32)/32**.5
        exec(compile(ast.Module(body=[readout_node],type_ignores=[]),str(source),'exec'))
        for case_index in range(2):
            res=captured[case_index]; h=res[24]; question_spans=spans
            final_logits=readout(res[32][-1],False); other_logits=readout(captured[1-case_index][32][-1],False)
            mask=torch.zeros(len(tok),dtype=torch.bool); mask[:40]=True
            output_mask=torch.zeros_like(mask); output_mask[int(final_logits.argmax())]=True
            pool_masks=[]; scores={}; pool_data={}
            exec(compile(ast.Module(body=branch.body,type_ignores=[]),str(source),'exec'))
            assert len(scores)==len(pool_data)==12
            for representation,state,use_j in [('J-lens',h,True),('plain24',h,False),('plain27',res[27],False)]:
                legacy=readout(state[-1],use_j).softmax(-1)-final_logits.softmax(-1)
                assert torch.equal(scores['end-pass pooling last '+representation],legacy.masked_fill(output_mask|(legacy<=0),-torch.inf))
            for name,(p,q,peaks,subtract) in pool_data.items():
                expected=(p-q if subtract else p)
                assert torch.equal(scores[name],expected.masked_fill(output_mask|(expected<=0),-torch.inf))
                assert set(peaks.tolist()).issubset(set(spans[case_index]['positions']))
        assert not any(isinstance(h,partial) and h.func.__qualname__=='generate_readout.<locals>.capture' for block in model.model.layers for h in block._forward_hooks.values())
        old[0][24][0]+=1
        torch.save(old,reference/'prefill.pt')
        try:
            capture_question_prefills(model,tok,prompts,prefix,23,special,reference,out)
        except AssertionError as error:
            assert 'last states changed' in str(error)
            assert not json.loads((out/'capture_reference.json').read_text())['last_states_and_generated_ids_equal']
            assert len(json.loads((out/'capture_generations.json').read_text()))==1
        else:
            raise AssertionError('changed reference state accepted')
    guard=next(n for n in ast.walk(main) if isinstance(n,ast.If) and any(isinstance(c,ast.FunctionDef) and c.name=='reject_forward' for c in n.body))
    exec(compile(ast.Module(body=guard.body,type_ignores=[]),str(source),'exec'))
    assert torch.isfinite(readout(captured[0][24][-1])).all()
    for module in (model,model.model):
        try:
            module(torch.tensor([[1,2]]))
        except AssertionError as error:
            assert 'must not call the transformer' in str(error)
        else:
            raise AssertionError('scoring allowed a transformer forward')
    print(f'PASS seed{seed}: tiny real hybrid Qwen32 layers, pinned tokenizer, production capture/I/O and all12 scoring branches; exact legacy last scores; changed reference rejected; scoring guards reject model/backbone',flush=True)
print('PASS CPU components/integration; full main and full-size BF16 parity still require the bounded run',flush=True)
