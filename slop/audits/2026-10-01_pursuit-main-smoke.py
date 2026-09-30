"""Full pursuit/main and baseline parity on real tiny32-layer Qwen CPU fixtures. Not model evidence. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

gradient = '--gradient-pursuit' in sys.argv
prefix_name = 'gradient ' if gradient else ''
artifact_name = 'gradient_pursuit' if gradient else 'pursuit'
torch.set_num_threads(1)
torch.set_grad_enabled(False)
root=Path(__file__).resolve().parents[2]
entry=root/'scripts/english/08_jlens_one_pass.py'
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(),flush=True)
ns=runpy.run_path(str(entry)); g=ns['main'].__globals__
old=runpy.run_path(str(root/'out/2026-10-01_045248_jlens-one-pass/source.py')); old_g=old['main'].__globals__
tok=AutoTokenizer.from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
config=Qwen3_5TextConfig(vocab_size=len(tok),hidden_size=32,intermediate_size=64,num_hidden_layers=32,
    num_attention_heads=2,num_key_value_heads=1,head_dim=16,linear_key_head_dim=8,linear_value_head_dim=8,
    linear_num_key_heads=2,linear_num_value_heads=4,max_position_embeddings=128,bos_token_id=None,eos_token_id=None,pad_token_id=0,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,'mrope_interleaved':True,'mrope_section':[3,3,2]})
full_data=json.loads((root/'data/english_hidden_words_v4.json').read_text())
clues=g['PURSUIT_CLUES']
for case, clue in zip(full_data['cases'], clues, strict=True):
    prompt=full_data['prefix']+case['prompt']
    enc=tok(prompt,add_special_tokens=False,return_offsets_mapping=True,return_special_tokens_mask=True)
    span={'input_ids':enc.input_ids,'offsets':enc.offset_mapping,
        'positions':g['question_positions'](enc.input_ids,enc.offset_mapping,enc.special_tokens_mask,set(tok.all_special_ids),len(full_data['prefix']),len(prompt))}
    positions=g['pursuit_diagnostic_positions'](prompt,span,clue)
    assert all(span['offsets'][i][1] <= prompt.index(clue) for i in positions.values())
print('PASS all8 pinned-tokenizer identifying spans; diagnostic tokens end before identifying text',flush=True)
g['PURSUIT_CLUES']=(clues[0],clues[2])
print('WARNING: tiny random BF16 Qwen CPU fixture, not the pinned 4B weights; zero scientific inference',flush=True)
for seed in (0,1):
    torch.manual_seed(seed)
    model=Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    with tempfile.TemporaryDirectory(dir=root/'.local') as tmp:
        tmp=Path(tmp); cache=tmp/'cache';cache.mkdir()
        data=json.loads((root/'data/english_hidden_words_v4.json').read_text());data['cases']=[data['cases'][0],data['cases'][2]]
        config_path=tmp/'cases.json';config_path.write_text(json.dumps(data))
        states=[]; traces=[]; spans=[]
        for case in data['cases']:
            prompt=data['prefix']+case['prompt']
            enc=tok(prompt,add_special_tokens=False,return_offsets_mapping=True,return_special_tokens_mask=True)
            res,generated,coverage=g['generate_readout'](model,torch.tensor([enc.input_ids]),23)
            states.append(res);traces.append({'prompt':prompt,'token_ids':generated,'coverage':coverage,
                'generation_overrides':{'max_new_tokens':8,'do_sample':False,'use_cache':True}})
            spans.append({'prompt':prompt,'input_ids':enc.input_ids,'offsets':enc.offset_mapping,
                'positions':g['question_positions'](enc.input_ids,enc.offset_mapping,enc.special_tokens_mask,set(tok.all_special_ids),len(data['prefix']),len(prompt))})
        torch.save(states,cache/'prefill_positions.pt')
        torch.save([{r:h[-1] for r,h in res.items()} for res in states],cache/'prefill.pt')
        (cache/'generation_traces.json').write_text(json.dumps(traces));(cache/'question_spans.json').write_text(json.dumps(spans))
        (cache/'source.py').write_bytes(entry.read_bytes())
        lens=tmp/'lens.pt';torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.randn(32,32)/32**.5}},lens)
        g['ROOT']=tmp;g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=lambda *a,**kw:model)
        g['hf_hub_download']=lambda *a,**kw:str(lens);g['LENS_SHA']=hashlib.sha256(lens.read_bytes()).hexdigest()
        model.cuda=lambda *a,**kw:model
        original_cuda=torch.Tensor.cuda;original_mask=g['q'].prompt_word_mask
        torch.Tensor.cuda=lambda self,*a,**kw:self
        g['q'].prompt_word_mask=lambda prompt,vocab,device:original_mask(prompt,vocab,'cpu')
        before_weight=model.lm_head.weight.clone();before_norm=model.model.norm.weight.clone()
        try:
            out=g['main'](cases_json=config_path,end_pass_readout=True,output_mask_max_n=1,
                erase_output=True,erase_strength=.5,matching_pursuit=True,gradient_pursuit=gradient,replay_readout_run=cache)
            for key in ('AutoModelForCausalLM','hf_hub_download','LENS_SHA','q','PURSUIT_CLUES'):
                old_g[key]=g[key]
            old_g['ROOT']=tmp/'baseline'
            baseline=old_g['main'](cases_json=config_path,end_pass_readout=True,output_mask_max_n=1,
                erase_output=True,erase_strength=.5,matching_pursuit=gradient,replay_readout_run=cache)
        finally:
            torch.Tensor.cuda=original_cuda;g['q'].prompt_word_mask=original_mask
        rows=json.loads((out/'readout.json').read_text());components=json.loads((out/f'{artifact_name}_records.json').read_text())
        diagnostics=json.loads((out/f'{artifact_name}_diagnostics.json').read_text())
        assert len(rows)==(96 if gradient else 72) and len(components)==6 and len(diagnostics)==4
        assert len(list((out/f'{artifact_name}_tensors').glob('*.pt')))==6
        baseline_rows=json.loads((baseline/'readout.json').read_text())
        by_key={(r['case_index'],r['method']):r for r in rows}
        assert len(baseline_rows)==(72 if gradient else 42)
        assert all(by_key[r['case_index'],r['method']]==r for r in baseline_rows)
        assert torch.equal(model.lm_head.weight,before_weight) and torch.equal(model.model.norm.weight,before_norm)
        for r in components:
            case_rows={x['method']:x for x in rows if x['case_index']==r['case_index']}
            for variant in ('pursuit','raw-dot matched','unit-dot matched'):
                scored=case_rows[f"end-pass {prefix_name}{variant} {r['representation']}"]
                assert scored['returned_cardinality']==r['postmask_cardinality']
                assert len(scored['selected_ids'])==scored['return_limit']
            assert r['reconstruction_max_error'] < 1e-4
            saved=torch.load(out/f'{artifact_name}_tensors'/f"{r['case_index']:03d}-{r['representation']}.pt",weights_only=True)
            sparse=saved['scores']['pursuit']
            assert torch.isfinite(sparse).nonzero().numel()==r['postmask_cardinality']
            for variant,key in (('pursuit','pursuit'),('raw-dot matched','raw-dot full32'),('unit-dot matched','unit-dot full32')):
                n=r['postmask_cardinality']
                expected=saved['scores'][key].argsort(descending=True,stable=True)[:n].tolist()
                assert case_rows[f"end-pass {prefix_name}{variant} {r['representation']}"]['selected_ids']==expected
            if gradient:
                cap=case_rows[f"end-pass gradient-budget matching pursuit {r['representation']}"]
                old=case_rows[f"end-pass pursuit {r['representation']}"]
                assert cap['selected_ids']==old['selected_ids'][:r['postmask_cardinality']]
                assert len(r['updates'])==len(r['steps_selected_ids'])<=32
        for r in diagnostics:
            assert r['clue'] not in r['consumed_prefix']
            assert r['position'] < len(spans[r['case_index']]['input_ids'])-1
            assert len(r['active_ids'])==len(r['coefficients'])==len(r['normalized_coefficients'])
            assert len(r['steps_selected_ids'])<=32
        assert json.loads((out/'replay_source.json').read_text())['model_forward_calls']==0
        assert [r['token_ids'] for r in json.loads((out/'generation_traces.json').read_text())]==[t['token_ids'] for t in traces]
        assert all(torch.equal(x[r],y[r][-1]) for x,y in zip(torch.load(out/'prefill.pt',weights_only=True),states) for r in x)
        for module in (model,model.model):
            try:
                module(torch.tensor([[1,2]]))
            except AssertionError as error:
                assert 'must not call the transformer' in str(error)
            else:
                raise AssertionError('main failed to install replay guard')
    print(f'PASS seed{seed}: gradient={gradient}, full main, real tiny BF16 Qwen prefills/decode cache, both prefixes,{len(rows)} rows, same-cardinality controls, diagnostics,{len(baseline_rows)} baseline rows exact, unchanged parameters/IDs/states, no scoring forwards',flush=True)
print('PASS CPU full-main smoke against archived pre-chat source; not new full-size model evidence',flush=True)
