"""Actual four-case launcher on tiny Qwen; no pretrained behavior. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from types import SimpleNamespace

import torch
from transformers import Qwen3_5TextConfig, Qwen3_5ForCausalLM

ROOT=Path.cwd()
source=ROOT/'scripts/english/08_jlens_one_pass.py'
launcher=runpy.run_path(str(ROOT/'slop/audits/2026-10-01_animal-pairs-launcher.py'))['main'].__globals__
g=runpy.run_path(str(source))['main'].__globals__
common=runpy.run_path(str(launcher['COMMON']))
torch.set_grad_enabled(False)
torch.set_num_threads(1)
config=Qwen3_5TextConfig(vocab_size=248320,hidden_size=32,intermediate_size=64,num_hidden_layers=32,
    num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
    linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=256,
    bos_token_id=None,eos_token_id=248044,pad_token_id=248044,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,
                     'mrope_interleaved':True,'mrope_section':[3,3,2]})
models=[]
def tiny_loader(*args,**kwargs):
    torch.manual_seed(0)
    model=Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    model.cuda=lambda *a,**kw:model
    models.append(model)
    return model

with tempfile.TemporaryDirectory(dir=ROOT/'.local') as directory:
    tmp=Path(directory)
    for name in {*launcher['PINS'],*common['HELPERS']}:
        dest=tmp/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,dest)
    lens=tmp/'lens.pt'
    torch.manual_seed(0)
    torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.randn(32,32)/32**.5}},lens)
    g['ROOT']=tmp
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=tiny_loader)
    g['hf_hub_download']=lambda *args,**kwargs:str(lens)
    g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
    launcher['ROOT']=tmp
    for key in ('COMMON','DATA','LABELS'):
        launcher[key]=tmp/launcher[key].relative_to(ROOT)
    launcher['runpy']=SimpleNamespace(run_path=lambda path: {'main':g['main']} if Path(path)==source else common)
    cuda,mask=torch.Tensor.cuda,g['q'].prompt_word_mask
    torch.Tensor.cuda=lambda self,*args,**kwargs:self
    g['q'].prompt_word_mask=lambda prompt,vocab,device:mask(prompt,vocab,'cpu')
    try:
        launcher['main'](source)
        master,=(tmp/'out').glob('*_animal-pairs-readout')
        meta=json.loads((master/'pipeline.json').read_text())
        assert meta['stage']=='completed' and meta['original_rows_exact']==72 and meta['candidate_rows']==16
        assert meta['rescore_forward_calls']==0 and meta['actual_forward_calls']==meta['generated_tokens']<=128
        assert len(models)==2 and all(torch.equal(a,b) for a,b in zip(models[0].parameters(),models[1].parameters(),strict=True))
        diag=json.loads((master/'pair_metrics.json').read_text())
        assert len(diag['pairs'])==8 and len(diag['assignment_nulls'])==16
        for r in diag['pairs']:
            assert r['D']==r['d_a']-r['d_b'] and r['own_margins']==[r['d_a'],-r['d_b']]
        dataset=json.loads(launcher['DATA'].read_text())
        frozen=json.loads(launcher['LABELS'].read_text())
        capture,replay=Path(meta['capture']),Path(meta['replay'])
        index=common['check_replay'](capture,replay,4)
        path=replay/'unmasked_readout_scores'/'000.pt'
        altered=torch.load(path,weights_only=True)
        altered[common['BASE_METHODS'][0]][0]+=1
        torch.save(altered,path)
        try:
            launcher['pair_metrics'](capture,replay,dataset,frozen,common,index)
        except AssertionError:
            pass
        else:
            raise AssertionError('Changed pre-mask replay scores accepted')
        print('PASS actual animal launcher seed0: four native inputs,72 old rows exact+16 candidates, '
              '128-or-fewer tokens, zero cached forwards, exact pre-mask/selected-score parity, '
              'eight pair records,16 descriptive permutations, altered raw replay rejected, unchanged weights',flush=True)
    finally:
        torch.Tensor.cuda=cuda
        g['q'].prompt_word_mask=mask
print('Tiny random BF16 Qwen only; no pretrained animal generations. — PI/OpenAI',flush=True)
