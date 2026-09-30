"""Production scorer algebra checks, not a transformer smoke test. — PI/OpenAI"""
import ast
from pathlib import Path
import torch

source = ast.parse(Path('scripts/english/08_jlens_one_pass.py').read_text())
main = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
loop = next(n for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple)
            and [getattr(t, 'id', '') for t in n.target.elts] == ['name', 'z'])
code = compile(ast.Module(body=[loop], type_ignores=[]), '<production contrast loop>', 'exec')
for seed in (0, 1):
    torch.manual_seed(seed)
    intermediate, final = torch.randn(128), torch.randn(128)
    mask = torch.arange(128) % 7 == 0
    def evaluate(labels, current=intermediate):
        env = dict(torch=torch, scores={'J-lens':current, 'plain lens':current}, final_logits=final,
                   output_mask=mask, readout=lambda state, _: state, res={27:current[None]},
                   replay_readout_run=None, components={}, hidden=labels, said=labels[::-1],
                   case={'concept':str(labels), 'said_text':str(labels[::-1])})
        exec(code, env)
        return env['scores']
    first, permuted = evaluate([1,2]), evaluate([99,101])
    for name in first:
        assert torch.equal(first[name], permuted[name])
    d = first['end-pass logit contrast J-lens']
    assert torch.equal(d[~mask], (intermediate-final)[~mask])
    assert torch.isneginf(d[mask]).all()
    ratio = (intermediate.log_softmax(-1)-final.log_softmax(-1)).masked_fill(mask, -torch.inf)
    assert torch.equal(d.topk(32).indices, ratio.topk(32).indices)
    self_scores = evaluate([1,2], final)
    assert (self_scores['end-pass logit contrast J-lens'][~mask] == 0).all()
    assert torch.isneginf(self_scores['end-pass probability contrast J-lens']).all()
    print(f'PASS seed={seed}: signed difference, masks, log-ratio ranking, self-zero, label/text invariance')
reject = next(n for n in ast.walk(main) if isinstance(n, ast.FunctionDef) and n.name == 'reject_forward')
namespace = {}
exec(compile(ast.Module(body=[reject], type_ignores=[]), '<production replay guard>', 'exec'), namespace)
model = torch.nn.Linear(2,2)
model.register_forward_pre_hook(namespace['reject_forward'])
try:
    model(torch.zeros(2))
except AssertionError as error:
    assert str(error) == 'Cached readout scoring must not call the transformer'
else:
    raise AssertionError('Replay guard allowed a model call')
print('PASS production replay guard blocks a model forward')
