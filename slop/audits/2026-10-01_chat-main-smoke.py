"""Exercise native-chat main on tiny real BF16 Qwen, not scientific model weights. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace

import torch
from transformers import AutoTokenizer, Qwen3_5TextConfig, Qwen3_5ForCausalLM

torch.set_num_threads(1)
torch.set_grad_enabled(False)
root = Path(__file__).resolve().parents[2]
entry = root/'scripts/english/08_jlens_one_pass.py'
g = runpy.run_path(str(entry))['main'].__globals__
tok = AutoTokenizer.from_pretrained(g['q'].MODEL, revision=g['q'].REVISION, local_files_only=True)
print('source_sha256='+hashlib.sha256(entry.read_bytes()).hexdigest(), flush=True)
centering = '--generic-reference' in sys.argv
expand = '--input-prefix' in sys.argv or centering
if expand:
    words=[' Continents','CONTINENTAL',' cont','article','art','named',' nam','onion',' toffee']
    normalized=[w.strip().lower() for w in words]
    matches=g['input_prefix_extensions']('NAME art continent on to',normalized)
    assert matches=={0:['continent'],1:['continent'],3:['art'],4:['art'],5:['name']},matches
    legacy=g['q'].prompt_word_mask('NAME art continent on to',normalized,'cpu')
    assert legacy[6] and 6 not in matches
    assert g['input_prefix_extensions']('continent continents',['continents'])=={0:['continent','continents']}
    assert g['input_prefix_extensions']('on to',normalized)=={}
    print('PASS complete-word anchoring/case/space/short-word rules; legacy nam remains excluded; art→article overmask and multiple origins explicit',flush=True)
config = Qwen3_5TextConfig(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=32,
    num_attention_heads=2, num_key_value_heads=1, head_dim=16, linear_key_head_dim=8, linear_value_head_dim=8,
    linear_num_key_heads=2, linear_num_value_heads=4, max_position_embeddings=256,
    bos_token_id=None, eos_token_id=248044, pad_token_id=248044,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,'mrope_interleaved':True,'mrope_section':[3,3,2]})
for seed in (0, 1):
    torch.manual_seed(seed)
    model = Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    before = {k: v.clone() for k, v in model.named_parameters()}
    defaults = model.generation_config.to_dict()
    sentinel = model.model.layers[23].register_forward_hook(lambda *args: None)
    with tempfile.TemporaryDirectory(dir=root/'.local') as directory:
        tmp = Path(directory)
        data = json.loads((root/'data/english_geography_chat_v1.json').read_text())
        data['cases'] = data['cases'][:2]
        dataset = tmp/'cases.json'; dataset.write_text(json.dumps(data))
        lens = tmp/'lens.pt'
        torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.randn(32,32)/32**.5}}, lens)
        g['ROOT'] = tmp
        g['AutoModelForCausalLM'] = SimpleNamespace(from_pretrained=lambda *a, **kw: model)
        g['hf_hub_download'] = lambda *a, **kw: str(lens)
        g['LENS_SHA'] = hashlib.sha256(lens.read_bytes()).hexdigest()
        model.cuda = lambda *a, **kw: model
        cuda, mask = torch.Tensor.cuda, g['q'].prompt_word_mask
        torch.Tensor.cuda = lambda self, *a, **kw: self
        g['q'].prompt_word_mask = lambda prompt, vocab, device: mask(prompt, vocab, 'cpu')
        try:
            if centering:
                calls=[]
                counter=model.register_forward_pre_hook(lambda *args: calls.append(1))
                g['ROOT']=tmp/'reference-preparation'
                prepared=g['main'](prepare_reference_json=root/'data/generic_readout_reference_v1.json')
                counter.remove()
                checkpoint=prepared/'reference.pt'
                assert len(calls)==1
                prepared_reference=torch.load(checkpoint,weights_only=True)
                assert set(prepared_reference['states'])=={24,27} and prepared_reference['ignored_generated_token_count']==1
                assert all(v==[len(prepared_reference['input_ids'])] for v in prepared_reference['coverage'].values())
                g['ROOT']=tmp
            out = g['main'](cases_json=dataset, end_pass_readout=True, output_mask_max_n=1,
                            erase_output=True, erase_strength=.5, chat_readout=True, readout_max_new_tokens=32)
            traces = json.loads((out/'generation_traces.json').read_text())
            rows = json.loads((out/'readout.json').read_text())
            assert len(traces)==2 and len(rows)==36
            saved = torch.load(out/'prefill.pt', weights_only=True)
            matrix = torch.load(lens, weights_only=True)['J'][23]
            for i, trace in enumerate(traces):
                ids = tok(trace['prompt'], add_special_tokens=False, return_tensors='pt').input_ids
                assert trace['generation_overrides']=={'max_new_tokens':32,'do_sample':False,'use_cache':True,'eos_token_id':[248044,248046]}
                direct = model.generate(ids, **trace['generation_overrides'])[0, ids.shape[1]:].tolist()
                assert trace['token_ids']==direct and len(direct)==trace['n_tokens']==32
                assert all(c==[ids.shape[1]]+[1]*31 for c in trace['coverage'].values())
                assert trace['decoded_verbatim']==tok.decode(direct)
                assert trace['scoring_text']==tok.decode(direct, skip_special_tokens=True)
                states, one, coverage = g['generate_readout'](model, ids, 23, 32, [direct[0], 248046])
                assert one==direct[:1] and all(c==[ids.shape[1]] for c in coverage.values())
                assert all(torch.equal(saved[i][r], states[r][-1]) for r in states)
                unmasked = torch.load(out/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
                W = model.lm_head.weight
                output_id = model.lm_head(model.model.norm(saved[i][32])).float().argmax()
                direction = W[output_id].float()
                transported = saved[i][24].float() @ matrix.T
                raw = model.lm_head(model.model.norm(transported.to(W.dtype))).float()
                assert torch.equal(unmasked['end-pass J-lens'],raw)
                for name,state in [('J-lens',transported),('plain24',saved[i][24]),('plain27',saved[i][27])]:
                    normalized = model.model.norm(state.to(W.dtype)).float()
                    removed = (normalized@direction)/direction.square().sum()*direction
                    expected = model.lm_head((normalized-.5*removed).to(W.dtype)).float()
                    assert torch.equal(unmasked['end-pass erased0.5 '+name],expected)
                assert len(unmasked)==4 and all(torch.isfinite(z).all() for z in unmasked.values())
                for row in [r for r in rows if r['case_index']==i]:
                    assert len(row['selected_ids'])==len(row['selected_scores'])==len(row['top32'])==32
                    assert row['pair_hidden_rank']>=0 and row['pair_partner_rank']>=0
                    if row['method'] in unmasked:
                        assert unmasked[row['method']][row['selected_ids']].tolist()==row['selected_scores']
            assert sentinel.id in model.model.layers[23]._forward_hooks
            assert sum(len(b._forward_hooks) for b in model.model.layers)==1
            g['ROOT']=tmp/'replay'
            replay=g['main'](cases_json=dataset,end_pass_readout=True,output_mask_max_n=1,
                erase_output=True,erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,replay_readout_run=out,
                expand_input_prefix=expand)
            replay_rows={(r['case_index'],r['method']):r for r in json.loads((replay/'readout.json').read_text())}
            assert all(replay_rows[r['case_index'],r['method']]==r for r in rows)
            for i in range(2):
                before_scores=torch.load(out/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
                after_scores=torch.load(replay/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
                assert all(torch.equal(z,after_scores[name]) for name,z in before_scores.items())
            print(f'PASS seed{seed}: unmasked diagnostic scores equal direct readout/half-erasure, selected scores unchanged and replay exact',flush=True)
            if expand:
                assert len(replay_rows)==44
                exclusions=json.loads((replay/'input_prefix_exclusions.json').read_text())
                assert len(exclusions)==2
                for i,record in enumerate(exclusions):
                    original_scores=torch.load(replay/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True)
                    assert len(original_scores)==4
                    added=record['added_input_exclusions'];assert added
                    for item in added:
                        assert item['token']==tok.decode([item['id']])
                        assert item['normalized']==item['token'].strip().lower()
                        assert all(len(w)>=3 and item['normalized'].startswith(w) for w in item['originating_words'])
                    added_ids=[a['id'] for a in added]
                    for name,original in original_scores.items():
                        masked=original.clone();masked[added_ids]=-torch.inf
                        new_name=name.replace('end-pass ','end-pass input-prefix ',1)
                        row=replay_rows[i,new_name]
                        assert masked.topk(32).indices.tolist()==row['selected_ids']
                        assert masked[row['selected_ids']].tolist()==row['selected_scores']
                        assert not set(row['selected_ids'])&set(added_ids)
                print(f'PASS seed{seed}:44 rows/36 originals exact,8 candidate full-vocabulary top32 refills, exclusion origins, saved-score reconstruction, transformer calls blocked',flush=True)
            if centering:
                def reject(*args):
                    raise AssertionError('Extra transformer forward during reference rescoring')
                rejecting=[m.register_forward_pre_hook(reject) for m in (model,model.model)]
                try:
                    counter.remove()
                    try:
                        model(torch.tensor([[1,2]]))
                    except AssertionError as error:
                        assert str(error)=='Cached readout scoring must not call the transformer'
                    else:
                        raise AssertionError('Extra-forward test guard did not reject a model call')
                    g['ROOT']=tmp/'centered'
                    centered=g['main'](cases_json=dataset,end_pass_readout=True,output_mask_max_n=1,
                        erase_output=True,erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,
                        replay_readout_run=out,expand_input_prefix=True,reference_checkpoint=checkpoint)
                    new_rows={(r['case_index'],r['method']):r for r in json.loads((centered/'readout.json').read_text())}
                    assert len(new_rows)==56 and all(new_rows[k]==v for k,v in replay_rows.items())
                    refs=torch.load(centered/'normalized_references.pt',weights_only=True)
                    vector=torch.randn(32,generator=torch.Generator().manual_seed(0))
                    vector=vector/vector.norm()
                    for name,state in [('J-lens',prepared_reference['states'][24].float()@matrix.T),('plain24',prepared_reference['states'][24]),('plain27',prepared_reference['states'][27])]:
                        expected=model.model.norm(state.to(W.dtype)).float()
                        assert torch.equal(refs['generic'][name],expected)
                        assert torch.equal(refs['random'][name],vector*expected.norm())
                        assert torch.allclose(refs['random'][name].norm(),expected.norm(),atol=1e-6,rtol=1e-6)
                    for i in range(2):
                        raw=torch.load(centered/'reference_readout_scores'/f'{i:03d}.pt',weights_only=True)
                        original=torch.load(replay/'input_prefix_scores'/f'{i:03d}.pt',weights_only=True)
                        zero_scores=torch.load(out/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
                        direction=W[model.lm_head(model.model.norm(saved[i][32])).float().argmax()].float()
                        for name,state in [('J-lens',saved[i][24].float()@matrix.T),('plain24',saved[i][24]),('plain27',saved[i][27])]:
                            normalized=model.model.norm(state.to(W.dtype)).float()
                            zero=g['subtract_reference'](normalized,torch.zeros_like(normalized),direction)
                            assert torch.equal(model.lm_head(zero.to(W.dtype)).float(),zero_scores['end-pass erased0.5 '+name])
                            for kind in ('generic','random'):
                                method=f'end-pass input-prefix {kind}-reference erased0.5 {name}'
                                delta=normalized-refs[kind][name]
                                expected=delta-.5*((delta@direction)/direction.square().sum()*direction)
                                actual=g['subtract_reference'](normalized,refs[kind][name],direction)
                                assert torch.equal(actual,expected)
                                x,w=delta.double(),direction.double()
                                precise=x-.5*(x@w)/w.square().sum()*w
                                assert (actual.double()-precise).norm()<1e-5
                                assert torch.equal(raw[method],model.lm_head(expected.to(W.dtype)).float())
                                masked=raw[method].masked_fill(~torch.isfinite(original['end-pass erased0.5 '+name]),-torch.inf)
                                masked[[a['id'] for a in exclusions[i]['added_input_exclusions']]]=-torch.inf
                                row=new_rows[i,method]
                                assert masked.topk(32).indices.tolist()==row['selected_ids']
                                assert masked[row['selected_ids']].tolist()==row['selected_scores']
                    bad={**prepared_reference,'revision':'wrong-model-revision'}
                    bad_path=tmp/'bad-reference.pt';torch.save(bad,bad_path)
                    g['ROOT']=tmp/'bad-reference-run'
                    try:
                        g['main'](cases_json=dataset,end_pass_readout=True,output_mask_max_n=1,
                            erase_output=True,erase_strength=.5,chat_readout=True,readout_max_new_tokens=32,
                            replay_readout_run=out,expand_input_prefix=True,reference_checkpoint=bad_path)
                    except AssertionError:
                        pass
                    else:
                        raise AssertionError('Mismatched reference revision accepted')
                    assert len(calls)==1
                finally:
                    for handle in rejecting: handle.remove()
                    counter.remove()
                assert sentinel.id in model.model.layers[23]._forward_hooks
                assert sum(len(b._forward_hooks) for b in model.model.layers)==1
                print(f'PASS seed{seed}: one generic prefill;56 rows/44 unchanged,12 centered candidates;zero-reference parity, float64 projection, fixed prematched random, exact masked scores, wrong revision rejected, no cached forwards',flush=True)
            assert all(torch.equal(before[k],v) for k,v in model.named_parameters())
            assert defaults==model.generation_config.to_dict()
        finally:
            torch.Tensor.cuda=cuda; g['q'].prompt_word_mask=mask
            sentinel.remove()
    print(f'PASS seed{seed}: native chat,32-token full main, exact raw/scoring text, same-prefill states, early EOS override, coverage, owned hooks,36 replay rows exact, unchanged parameters/defaults', flush=True)
print('PASS tiny random CPU model only; no pretrained scientific generations', flush=True)
