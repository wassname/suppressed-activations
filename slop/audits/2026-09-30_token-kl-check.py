"""Production scoring-loop algebra/guard tests; no transformer inference. -- PI/OpenAI"""
import ast
from pathlib import Path

import torch

source = ast.parse(Path('scripts/english/08_jlens_one_pass.py').read_text())
helper = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'positive_token_kl_log_scores')
main = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
loop = next(n for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple)
            and [getattr(t,'id','') for t in n.target.elts] == ['name','z'])
namespace = {'torch':torch}
exec(compile(ast.Module(body=[helper],type_ignores=[]),'<production token-KL>','exec'), namespace)
score_fn = namespace['positive_token_kl_log_scores']
code = compile(ast.Module(body=[loop],type_ignores=[]),'<production comparison loop>','exec')
replay_if = next(n for n in loop.body if isinstance(n, ast.If) and ast.unparse(n.test) == 'replay_readout_run is not None')
mismatch_code = compile(ast.Module(body=[replay_if.body[-1]],type_ignores=[]),'<production mismatch score>','exec')
for seed in (0,1):
    torch.manual_seed(seed)
    intermediate, final, other = torch.randn(3,128,dtype=torch.float64)
    mask = torch.arange(128)%7 == 0
    def evaluate(labels, enabled=True):
        env = dict(torch=torch, positive_token_kl_log_scores=score_fn, token_kl=enabled,kl_names=set(),
                   scores={'J-lens':intermediate,'plain lens':intermediate}, final_logits=final,
                   output_mask=mask, readout=lambda state,_: state,res={27:intermediate[None]},
                   replay_readout_run=None,components={},hidden=labels,said=labels[::-1],
                   case={'concept':str(labels),'said_text':str(labels[::-1])})
        exec(code,env)
        return env
    env, permuted, old = evaluate([1,2]), evaluate([70,101]), evaluate([1,2],False)
    for name,value in env['scores'].items():
        assert torch.equal(value,permuted['scores'][name])
    for name,value in old['scores'].items():
        assert torch.equal(value,env['scores'][name])
    lp,lq = intermediate.log_softmax(-1), final.log_softmax(-1)
    contribution = lp.exp()*(lp-lq).clamp_min(0)
    expected = score_fn(intermediate,final).masked_fill(mask,-torch.inf)
    eligible = torch.isfinite(expected)
    assert torch.allclose(expected[eligible].exp(),contribution[eligible],atol=1e-14,rtol=1e-12)
    assert torch.equal(eligible,(lp>lq)&~mask)
    for representation in ('J-lens','plain24','plain27'):
        assert torch.equal(env['scores']['end-pass positive token-KL '+representation],expected)
        env.update(name=representation,z=intermediate,other_logits=other)
        exec(mismatch_code,env)
        assert torch.equal(env['scores']['end-pass mismatched positive token-KL '+representation],score_fn(intermediate,other).masked_fill(mask,-torch.inf))
    assert torch.isneginf(score_fn(final,final)).all()
    shifted = score_fn(intermediate+13,final-7)
    valid = torch.isfinite(shifted)
    assert torch.equal(valid,lp>lq)
    assert torch.allclose(shifted[valid],score_fn(intermediate,final)[valid],atol=1e-11,rtol=1e-11)
    print(f'PASS seed={seed}: exact positive contribution, eligibility/mask, all three matched/mismatched transforms, old-score parity, label/text invariance, self-zero, additive-logit invariance',flush=True)
underflow = score_fn(torch.tensor([0.,-1000.]),torch.tensor([0.,-1010.]))
assert torch.isfinite(underflow[1]) and underflow[1].exp() == 0
assert abs(float(underflow[1])-(-1000+float(torch.tensor(10.).log()))) < 1e-4
selection = next(n for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'top_ids' for t in n.targets))
tie_env = {'z':torch.tensor([1.,1.,-torch.inf,0.]),'name':'KL','kl_names':{'KL'}}
exec(compile(ast.Module(body=[selection],type_ignores=[]),'<production stable selection>','exec'),tie_env)
assert tie_env['top_ids'].tolist() == [0,1,3,2]
assert [i for i in tie_env['top_ids'].tolist() if torch.isfinite(tie_env['z'][i])] == [0,1,3]
auc_assignment = next(n for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='checked_auc' for t in n.targets) and isinstance(n.value,ast.Call))
auc_env = {'torch':torch,'positives':torch.tensor([[-torch.inf]]),'negatives':torch.tensor([[-torch.inf]])}
exec(compile(ast.Module(body=[auc_assignment],type_ignores=[]),'<production AUROC>','exec'),auc_env)
assert auc_env['checked_auc'] == .5
reject = next(n for n in ast.walk(main) if isinstance(n,ast.FunctionDef) and n.name=='reject_forward')
exec(compile(ast.Module(body=[reject],type_ignores=[]),'<production forward guard>','exec'),namespace)
model = torch.nn.Linear(2,2)
model.register_forward_pre_hook(namespace['reject_forward'])
try:
    model(torch.zeros(2))
except AssertionError as error:
    assert str(error)=='Cached readout scoring must not call the transformer'
else:
    raise AssertionError('Replay guard allowed a forward')
print('PASS underflow-safe log ranking, stable token-ID ties, fewer-than32 finite entries, ineligible AUROC tie=.5, and actual replay forward guard',flush=True)
