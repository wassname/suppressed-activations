"""Saved-score and float64 pair reconstruction for2694, no neural replay. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
import torch
from transformers import AutoTokenizer

torch.set_num_threads(4)
master = Path(sys.argv[1])
p = json.loads((master / 'pipeline.json').read_text())
assert p['stage'] == 'completed'
for filename, key in [('source.py','source_sha256'),('dataset.json','data_sha256')]:
    assert hashlib.sha256((master / filename).read_bytes()).hexdigest() == p[key]
for name, sha in p['pins'].items():
    assert hashlib.sha256((master / 'inputs' / name).read_bytes()).hexdigest() == sha
capture, replay = Path(p['capture']), Path(p['replay'])
for path in (capture, replay):
    assert hashlib.sha256((path / 'source.py').read_bytes()).hexdigest() == p['source_sha256']
    assert json.loads((path / 'cases.json').read_text()) == json.loads((master / 'dataset.json').read_text())
traces = json.loads((capture / 'generation_traces.json').read_text())
assert len(traces) == 4
assert (capture / 'generation_traces.json').read_bytes() == (replay / 'generation_traces.json').read_bytes()
old_states = torch.load(capture / 'prefill.pt', weights_only=True, map_location='cpu')
new_states = torch.load(replay / 'prefill.pt', weights_only=True, map_location='cpu')
assert len(old_states) == len(new_states) == 4
assert all(torch.equal(a[k], b[k]) for a,b in zip(old_states,new_states,strict=True) for k in a)
forwards = [json.loads(line) for line in (master / 'forward_trace.jsonl').read_text().splitlines()]
expected_lengths = []
tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B', revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a', local_files_only=True)
for trace in traces:
    assert trace['generation_overrides'] == {'max_new_tokens':32,'do_sample':False,'use_cache':True,'eos_token_id':[248044,248046]}
    ids = trace['token_ids']
    assert 1 <= len(ids) <= 32 and tok.decode(ids) == trace['decoded_verbatim']
    assert tok.decode(ids,skip_special_tokens=True) == trace['scoring_text']
    assert trace['stopped_on_eos'] == (ids[-1] in (248044,248046))
    lengths = [len(tok(trace['prompt'],add_special_tokens=False).input_ids)] + [1]*(len(ids)-1)
    assert set(trace['coverage']) == {'24','27','32'} and all(v == lengths for v in trace['coverage'].values())
    expected_lengths.extend(lengths)
assert len(forwards) == p['actual_forward_calls'] == p['generated_tokens'] == len(expected_lengths)
assert all(r['phase'] == 'capture' and not r['grad_enabled'] for r in forwards)
assert [r['sequence_length'] for r in forwards] == expected_lengths
rows = json.loads((replay / 'readout.json').read_text())
index = {(r['case_index'],r['method']):r for r in rows}
old = json.loads((capture / 'readout.json').read_text())
assert len(rows) == len(index) == 88 and len(old) == 72
assert all(index[r['case_index'],r['method']] == r for r in old)
first = torch.load(replay / 'input_prefix_scores/000.pt',weights_only=True,map_location='cpu')
vocab_size = next(iter(first.values())).numel()
vocab = [tok.convert_tokens_to_string([t]) if t is not None else '' for t in tok.convert_ids_to_tokens(list(range(vocab_size)))]
normalized = [t.strip().lower() for t in vocab]


def ids(words):
    return {i for i,t in enumerate(normalized) if any(len(t)>=min(3,len(w)) and w.lower().startswith(t) for w in words)}


def disjoint(a,b):
    return a-b,b-a


def rank(z,labels):
    if not labels:
        return 10**9
    best = z[list(labels)].max()
    return int((z>best).sum()) if torch.isfinite(best) else 10**9


exclusions = json.loads((replay / 'input_prefix_exclusions.json').read_text())
assert len(exclusions) == 4
checked = 0
max_auc_error = 0
added_counts = []
for i, record in enumerate(exclusions):
    assert record['prompt'] == traces[i]['prompt']
    words = set(re.findall(r'\w+',record['prompt'].lower()))
    legacy = words | {w[:n] for w in words for n in range(3,len(w)+1)}
    expected = {}
    for t,value in enumerate(normalized):
        origins = sorted(w for w in words if len(w)>=3 and value.startswith(w))
        if origins and value not in legacy:
            expected[t] = origins
    assert {r['id']:r['originating_words'] for r in record['added_input_exclusions']} == expected
    assert all(r['token'] == vocab[r['id']] and r['normalized'] == normalized[r['id']] for r in record['added_input_exclusions'])
    originals = torch.load(replay / 'input_prefix_scores' / f'{i:03d}.pt',weights_only=True,map_location='cpu')
    assert len(originals) == 4
    added_counts.append(len(expected))
    assert all((not bool(torch.isfinite(originals['end-pass J-lens'][r['id']]))) == r['already_output_masked'] for r in record['added_input_exclusions'])
    for method, original in originals.items():
        prior = index[i,method]
        r = index[i,method.replace('end-pass ','end-pass input-prefix ',1)]
        assert original[prior['selected_ids']].tolist() == prior['selected_scores']
        z = original.clone()
        z[list(expected)] = -torch.inf
        selected = r['selected_ids']
        assert len(selected) == len(set(selected)) == 32 and not set(selected)&set(expected)
        assert z[selected].tolist() == r['selected_scores'] and [vocab[t] for t in selected] == r['top32']
        cutoff = z.topk(32).values[-1]
        assert torch.isfinite(z[selected]).all() and (z[selected]>=cutoff).all()
        assert set((z>cutoff).nonzero().flatten().tolist()) <= set(selected)
        actual_words = sorted(set(re.findall(r'[^\W_]+',traces[i]['scoring_text'].lower())))
        assert actual_words == r['actual_words']
        hidden_is_said = any(a.casefold() in actual_words for a in r['hidden_aliases'])
        expected_observed = any(re.search(r'\b'+re.escape(a)+r'\b',traces[i]['scoring_text'],re.I) for a in r['answer_aliases'])
        assert hidden_is_said == r['hidden_is_said'] and expected_observed == r['intended_answer_observed']
        h0,s0 = ids(r['hidden_aliases']),ids(r['answer_aliases'])
        ah,an = disjoint(h0,ids(actual_words))
        _,sn = disjoint(h0,s0)
        ch,cn = disjoint(ah,an | (sn if expected_observed else set()))
        unscorable = [w for w in actual_words if not ids([w])]
        assert unscorable == r['unscorable_actual_words']
        evaluable = hidden_is_said or bool(ah and an and not unscorable and ch and cn)
        assert evaluable == r['alias_checked_evaluable']
        result = evaluable and not hidden_is_said and bool(set(selected)&ch) and not bool(set(selected)&cn)
        assert result == r['alias_checked_pass']
        if evaluable and not hidden_is_said:
            positives, negatives = z[list(ch),None],z[list(cn)][None,:]
            auc = float(((positives>negatives).double()+.5*(positives==negatives).double()).mean())
            max_auc_error = max(max_auc_error,abs(auc-r['alias_checked_auroc']))
            assert max_auc_error < 1e-7
        else:
            assert r['alias_checked_auroc'] is None
        h,s = disjoint(ids([r['concept']]),ids([r['answer']]))
        assert rank(z,h) == r['r_hidden'] and rank(z,s) == r['r_said']
        checked += 1
result = {'signature':'PI/OpenAI','passed':True,'scope':'independent saved-score/label/coverage reconstruction; cutoff membership not tied ordering; no neural or semantic certification',
          'rows_checked':checked,'old_rows_exact':72,'actual_forward_calls':len(forwards),'generated_tokens':len(expected_lengths),
          'added_exclusion_counts':added_counts,'max_auc_error':max_auc_error}
frozen = json.loads((master/'labels.json').read_text())
diagnostic = json.loads((master/'pair_metrics.json').read_text())
dataset = json.loads((master/'dataset.json').read_text())
assert frozen['dataset_sha256'] == p['data_sha256']
vocabulary_ids = sorted(set(tok.get_vocab().values()))
decoded = tok.batch_decode([[i] for i in vocabulary_ids],skip_special_tokens=False,clean_up_tokenization_spaces=False)
for case in dataset['cases']:
    eligible = [{'id':i,'token':t} for i,t in zip(vocabulary_ids,decoded,strict=True) if t.strip().casefold() in case['hidden_aliases']]
    assert eligible == frozen['labels'][case['concept']]
max_lp_error = 0
recomputed = {}
for i in range(4):
    a = torch.load(capture/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
    b = torch.load(replay/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
    assert set(a) == set(b) == set(first)
    for method,z in a.items():
        assert z.dtype == torch.float32 and torch.isfinite(z).all() and torch.equal(z,b[method])
        r = index[i,method.replace('end-pass ','end-pass input-prefix ',1)]
        assert z[r['selected_ids']].tolist() == r['selected_scores']
        values = z.numpy().astype(np.float64)
        lp = values - (values.max()+np.log(np.exp(values-values.max()).sum()))
        lp32 = z.log_softmax(-1).numpy()
        for concept,tokens in frozen['labels'].items():
            reported = diagnostic['case_scores'][str(i)][method][concept]
            ids_here = [t['id'] for t in tokens]
            best = int(np.argmax(lp[ids_here]))
            assert reported['winner']['id'] == ids_here[best]
            assert [t['id'] for t in reported['constituents']] == ids_here
            expected_lp = lp[ids_here]
            actual_lp = np.array([t['log_probability'] for t in reported['constituents']])
            max_lp_error = max(max_lp_error,float(np.max(np.abs(expected_lp-actual_lp))))
            assert np.array_equal(actual_lp, lp32[ids_here])
            assert reported['score'] == float(actual_lp.max())
            assert np.max(np.abs((actual_lp-actual_lp[0])-(expected_lp-expected_lp[0]))) < 1e-10
            recomputed[i,method,concept] = float(expected_lp.max())
max_margin_error = 0
assert len(diagnostic['pairs']) == 8 and len(diagnostic['assignment_nulls']) == 16
for r in diagnostic['pairs']:
    a,b = r['pair']; method = r['method']
    ia,ib = next((2*j,2*j+1) for j,pair in enumerate(dataset['pairs']) if pair == [a,b])
    da = recomputed[ia,method,a]-recomputed[ia,method,b]
    db = recomputed[ib,method,a]-recomputed[ib,method,b]
    max_margin_error = max(max_margin_error,abs(r['d_a']-da),abs(r['d_b']-db),abs(r['D']-(da-db)))
    assert max_margin_error < 1e-5 and r['reversal'] == (da>0>db)
    assert np.allclose(r['own_margins'],[da,-db],rtol=0,atol=1e-5)
    texts = [traces[i]['scoring_text'] for i in (ia,ib)]
    assert r['actual_scoring_texts'] == texts
    assert r['complete_four_pair'] == all(t.strip().casefold() in ('4','four') for t in texts)
    assert r['exact_scoring_text_equal'] == (texts[0] == texts[1])
    primary = next(t for t in diagnostic['pairs'] if t['pair']==[a,b] and t['method']=='end-pass erased0.5 J-lens')
    assert r['primary_minus_this_D'] == primary['D']-r['D']
for null in diagnostic['assignment_nulls']:
    pair_rows = [r for r in diagnostic['pairs'] if r['method']==null['method']]
    signs = null['assignment_signs']
    assert null['mean_D'] == sum(s*r['D'] for s,r in zip(signs,pair_rows,strict=True))/2
    assert null['reversals'] == sum(s*r['d_a']>0>s*r['d_b'] for s,r in zip(signs,pair_rows,strict=True))
result.update(pair_rows_checked=8,max_log_probability_error=max_lp_error,max_margin_error=max_margin_error,
              scope=result['scope']+'; exact float32 log-probability replay, measured float64 normalizer error and independent float64 margin reconstruction')
(master / 'verification.json').write_text(json.dumps(result,indent=1))
print(json.dumps(result,indent=1))
