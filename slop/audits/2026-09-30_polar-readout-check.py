"""Actual polar scoring branch on a tiny Qwen head and pinned tokenizer, CPU. -- PI/OpenAI"""
import ast
import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root=Path(__file__).resolve().parents[2]
source=root/'scripts/english/08_jlens_one_pass.py'
tree=ast.parse(source.read_text())
for name in ('orthogonal_polar_factor','polar_readout_scores','question_positions'):
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'))
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
branch=next(n for n in ast.walk(main) if isinstance(n,ast.If) and ast.unparse(n.test)=='polar_readout' and any(isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='span' for t in x.targets) for x in n.body))
class CpuTransfer(ast.NodeTransformer):
    def visit_Call(self,node):
        node=self.generic_visit(node)
        return node.func.value if isinstance(node.func,ast.Attribute) and node.func.attr=='cuda' else node
branch=ast.fix_missing_locations(CpuTransfer().visit(copy.deepcopy(branch)))
readout_node=next(n for n in ast.walk(main) if isinstance(n,ast.FunctionDef) and n.name=='readout')
guard=next(n for n in ast.walk(main) if isinstance(n,ast.If) and any(isinstance(c,ast.FunctionDef) and c.name=='reject_forward' for c in n.body))
tok=AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B',revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a',local_files_only=True)
vocab=[tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(len(tok))))]
data=json.loads((root/'data/english_hidden_words_v4.json').read_text())
cases=[{**c,'prompt':data['prefix']+c['prompt']} for c in data['cases']]
polar_spans=[]
for case in cases:
    encoded=tok(case['prompt'],add_special_tokens=False,return_offsets_mapping=True,return_special_tokens_mask=True)
    positions=question_positions(encoded.input_ids,encoded.offset_mapping,encoded.special_tokens_mask,set(tok.all_special_ids),len(data['prefix']),len(case['prompt']))
    polar_spans.append({'prompt':case['prompt'],'positions':positions,'input_ids':encoded.input_ids,'offsets':encoded.offset_mapping})
config=Qwen3_5TextConfig(vocab_size=len(tok),hidden_size=32,intermediate_size=64,num_hidden_layers=2,
    num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
    linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=128,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,'mrope_interleaved':True,'mrope_section':[3,3,2]})
for seed in (0,1):
    torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval(); W=model.lm_head.weight
    J=torch.randn(32,32)/32**.5; orthogonal,_=orthogonal_polar_factor(J)
    exec(compile(ast.Module(body=[readout_node,*guard.body],type_ignores=[]),str(source),'exec'))
    polar_full=[{r:torch.randn(len(s['input_ids']),32).bfloat16() for r in (24,27,32)} for s in polar_spans]
    with tempfile.TemporaryDirectory(dir=root/'.local') as tmp:
        out=Path(tmp); polar_masks=[]; polar_priors=[]
        for case_index,case in enumerate(cases):
            res=polar_full[case_index]; h=res[24]
            final_logits=readout(res[32][-1],False); other_logits=readout(polar_full[(case_index+1)%8][32][-1],False)
            mask=torch.zeros(len(tok),dtype=torch.bool); mask[100:120]=True
            output_mask=torch.zeros(len(tok),dtype=torch.bool); output_mask[:40]=True
            scores={'J-lens':readout(h[-1]),'plain lens':readout(h[-1],False)}
            exec(compile(ast.Module(body=branch.body,type_ignores=[]),str(source),'exec'))
            assert len(polar_data)==7
            saved=torch.load(out/'polar_probabilities'/f'{case_index:03d}.pt',weights_only=True)
            assert set(saved)=={'Q','original-J','plain24','plain27','early','final','other'}
            for name,(p,q,subtract) in polar_data.items():
                expected=p-q if subtract else p
                assert torch.equal(scores[name],expected.masked_fill(output_mask|(expected<=0),-torch.inf))
                z=scores[name].masked_fill(mask,-torch.inf)
                top=[i for i in z.argsort(descending=True,stable=True)[:32].tolist() if torch.isfinite(z[i])]
                finite=z.isfinite().nonzero().flatten()
                expected_top=[i for i,value in sorted(zip(finite.tolist(),z[finite].tolist()),key=lambda pair:(-pair[1],pair[0]))[:32]]
                assert top==expected_top
            for tag,z in [('original-J',readout(h[-1])),('plain24',readout(h[-1],False)),('plain27',readout(res[27][-1],False))]:
                legacy=z.softmax(-1)-final_logits.softmax(-1)
                assert torch.equal(scores['end-pass polar '+tag+' excess'],legacy.masked_fill(output_mask|(legacy<=0),-torch.inf))
            before={k:v.clone() for k,v in scores.items()}
            case={**case,'concept':'changed evaluation label','answer':'changed output label'}
            exec(compile(ast.Module(body=branch.body,type_ignores=[]),str(source),'exec'))
            assert all(torch.equal(v,scores[k]) for k,v in before.items())
        assert {p['pieces'][2] for p in polar_priors}=={' The',' In'}
    for module in (model,model.model):
        try:
            module(torch.tensor([[1,2]]))
        except AssertionError as error:
            assert 'must not call the transformer' in str(error)
        else:
            raise AssertionError('guard failed')
    z=torch.zeros(40); f=torch.cat([torch.full((20,),-4.),torch.zeros(20)])
    values,_=polar_readout_scores({'Q':z,'original-J':z,'plain24':z,'plain27':z},f,f,z)
    eligible=values['end-pass polar Q excess']; selected=[i for i in eligible.argsort(descending=True,stable=True)[:32].tolist() if torch.isfinite(eligible[i])]
    assert selected==list(range(20))
    empty,_=polar_readout_scores({'Q':z,'original-J':z,'plain24':z,'plain27':z},z,z,z)
    assert torch.isneginf(empty['end-pass polar Q excess']).all()
    print(f'PASS seed{seed}: real tiny BF16 Qwen norm/head, pinned eight spans, seven production scoring branches, full probability persistence, exact old controls, labels do not affect scores, ties/empty eligibility and model/backbone guards',flush=True)
print('PASS branch integration only; full main/full-size decomposition not yet run',flush=True)
