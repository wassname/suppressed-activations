"""Same-answer diagnostic through the existing one-pass runner. — PI/OpenAI"""
from datetime import datetime
import gc
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import shutil
import sys
import time
from types import SimpleNamespace

import torch
from tabulate import tabulate

ROOT = Path.cwd()
COMMON = ROOT / 'slop/audits/2026-10-01_native-v4-launcher.py'
SOURCE_SHA = '7a98cb4a752f7f5e1d257c31681f8d7716a4e6e1a92dfb169599eb5406d2b183'
PINS = {
    'data/english_animal_pairs_chat_v1.json': '256fdb5d8ef2970259aefe894fa751ca14d200120f5553c8d511b681badea61e',
    'slop/audits/2026-10-01_animal-pairs-labels.json': 'ae8a991ad1b83a28a47c21059c8359b8d119ebad044b89e8891ecf77eb64ec51',
    'slop/audits/2026-10-01_native-v4-launcher.py': '7f81e356803715412e00b27c69a9fde8ae406068b68bb9f95e56731a6887a6e8',
    'slop/audits/2026-10-01_animal-pairs-preregistration.md': '5947917dcf14cdf15332aa7b0e0baf1e235f2fa8e288bd29c9902350fc7c2d75',
    'data/english_hidden_words_v2.json': 'c3e4efbebb01eb58d290ab0e120f4cecd798216ace4837a618180bd602c26590',
}
DATA = ROOT / 'data/english_animal_pairs_chat_v1.json'
LABELS = ROOT / 'slop/audits/2026-10-01_animal-pairs-labels.json'


def read_setup(source):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA
    for name, sha in PINS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
    common = runpy.run_path(str(COMMON))
    for name, sha in common['HELPERS'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
    dataset = json.loads(DATA.read_text())
    assert dataset['prefix'] == '' and dataset['required_max_new_tokens'] == 32
    assert [c['concept'] for c in dataset['cases']] == ['horse', 'cow', 'cat', 'goat']
    old = {c['concept']: c for c in json.loads((ROOT / dataset['source_dataset']).read_text())['cases']}
    for case in dataset['cases']:
        expected = 'Complete the fact with only the missing word or phrase:\n' + old[case['concept']]['prompt'].replace('The name for the young of', 'The number of legs on')
        assert case['prompt'] == expected and case['answer_aliases'] == ['4', 'four']
    return common, dataset


def enumerate_labels(g, dataset):
    tok = g['AutoTokenizer'].from_pretrained(g['q'].MODEL, revision=g['q'].REVISION, local_files_only=True)
    ids = sorted(set(tok.get_vocab().values()))
    decoded = tok.batch_decode([[i] for i in ids], skip_special_tokens=False, clean_up_tokenization_spaces=False)
    labels = {c['concept']: [{'id': i, 'token': t} for i, t in zip(ids, decoded, strict=True)
                            if t.strip().casefold() in c['hidden_aliases']] for c in dataset['cases']}
    assert all(labels.values())
    rendering = []
    for c in dataset['cases']:
        messages = [{'role': 'user', 'content': c['prompt']}]
        text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        token_ids = tok.apply_chat_template(messages, tokenize=True, return_dict=False, add_generation_prompt=True, enable_thinking=False)
        assert tok(text, add_special_tokens=False).input_ids == token_ids
        rendering.append({'concept': c['concept'], 'prompt': text, 'input_ids': token_ids})
    return {'signature': 'PI/OpenAI', 'dataset_sha256': hashlib.sha256(DATA.read_bytes()).hexdigest(),
            'labels': labels, 'rendering': rendering}


def pair_metrics(capture, replay, dataset, frozen, common, index):
    scores = {}
    for i in range(4):
        before = torch.load(capture / 'unmasked_readout_scores' / f'{i:03d}.pt', weights_only=True)
        after = torch.load(replay / 'unmasked_readout_scores' / f'{i:03d}.pt', weights_only=True)
        assert set(before) == set(after) == set(common['BASE_METHODS'])
        scores[i] = {}
        for method, z in before.items():
            assert z.dtype == torch.float32 and torch.isfinite(z).all() and torch.equal(z, after[method])
            row = index[i, method.replace('end-pass ', 'end-pass input-prefix ', 1)]
            assert z[row['selected_ids']].tolist() == row['selected_scores']
            lp = z.log_softmax(-1)
            scores[i][method] = {}
            for concept, tokens in frozen['labels'].items():
                values = [{**t, 'log_probability': float(lp[t['id']])} for t in tokens]
                winner = max(values, key=lambda t: t['log_probability'])
                scores[i][method][concept] = {'score': winner['log_probability'], 'winner': winner, 'constituents': values}
    pairs, nulls = [], []
    for method in common['BASE_METHODS']:
        these = []
        for pair_index, (a, b) in enumerate(dataset['pairs']):
            ia, ib = 2 * pair_index, 2 * pair_index + 1
            da = scores[ia][method][a]['score'] - scores[ia][method][b]['score']
            db = scores[ib][method][a]['score'] - scores[ib][method][b]['score']
            texts = [index[i, common['METHODS'][0]]['scoring_text'] for i in (ia, ib)]
            result = {'method': method, 'pair': [a, b], 'd_a': da, 'd_b': db, 'own_margins': [da, -db],
                      'D': da-db, 'reversal': da > 0 > db, 'actual_scoring_texts': texts,
                      'complete_four_pair': all(t.strip().casefold() in ('4', 'four') for t in texts),
                      'exact_scoring_text_equal': texts[0] == texts[1]}
            pairs.append(result)
            these.append(result)
        for signs in itertools.product((1, -1), repeat=2):
            nulls.append({'method': method, 'assignment_signs': signs,
                          'mean_D': sum(s*r['D'] for s,r in zip(signs,these,strict=True))/2,
                          'reversals': sum(s*r['d_a']>0>s*r['d_b'] for s,r in zip(signs,these,strict=True))})
    for r in pairs:
        primary = next(p for p in pairs if p['pair']==r['pair'] and p['method']==common['BASE_METHODS'][0])
        r['primary_minus_this_D'] = primary['D'] - r['D']
    return {'signature': 'PI/OpenAI', 'case_scores': scores, 'pairs': pairs, 'assignment_nulls': nulls}


def main(source, preflight=False):
    common, dataset = read_setup(source)
    g = runpy.run_path(str(source))['main'].__globals__
    torch.set_num_threads(4)
    frozen = enumerate_labels(g, dataset)
    if preflight:
        assert not LABELS.exists(), 'Do not overwrite the frozen pre-output label enumeration'
        LABELS.write_text(json.dumps(frozen, ensure_ascii=False, indent=1))
        print(json.dumps({'label_counts': {k:len(v) for k,v in frozen['labels'].items()}, 'generations': 0}))
        return
    assert frozen == json.loads(LABELS.read_text())
    started = time.monotonic()
    master = ROOT / 'out' / f'{datetime.now():%Y-%m-%d_%H%M%S}_animal-pairs-readout'
    master.mkdir(parents=True)
    for src,name in ((source,'source.py'),(DATA,'dataset.json'),(LABELS,'labels.json'),(Path(__file__),'launcher.py')):
        shutil.copyfile(src,master/name)
    for name in {**PINS, **common['HELPERS']}:
        dest = master / 'inputs' / name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,dest)
    metadata = {'stage':'preflight','pins':{**PINS,**common['HELPERS']},'source_sha256':SOURCE_SHA,
                'data_sha256':frozen['dataset_sha256'],'goals_completed':False}
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps({'master':str(master)}),flush=True)
    forwards, phase = [], 'capture'
    loader = g['AutoModelForCausalLM'].from_pretrained
    def track(module,args,kwargs):
        ids = args[0] if args else kwargs['input_ids']
        r = {'phase':phase,'sequence_length':ids.shape[1],'grad_enabled':torch.is_grad_enabled()}
        forwards.append(r)
        with (master/'forward_trace.jsonl').open('a') as stream:
            stream.write(json.dumps(r)+'\n')
        assert phase=='capture'
    def load(*args,**kwargs):
        model=loader(*args,**kwargs)
        model.register_forward_pre_hook(track,with_kwargs=True)
        return model
    g['AutoModelForCausalLM']=SimpleNamespace(from_pretrained=load)
    settings={'cases_json':DATA,'end_pass_readout':True,'output_mask_max_n':1,'erase_output':True,
              'erase_strength':.5,'chat_readout':True,'readout_max_new_tokens':32}
    capture=g['main'](**settings)
    traces=json.loads((capture/'generation_traces.json').read_text())
    assert len(traces)==4 and all(1<=len(t['token_ids'])<=32 for t in traces)
    common['check_forward_trace'](traces,forwards)
    count=len(forwards)
    metadata.update(stage='captured',capture=str(capture),actual_forward_calls=count)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    gc.collect()
    phase='rescore'
    replay=g['main'](**settings,replay_readout_run=capture,expand_input_prefix=True)
    index=common['check_replay'](capture,replay,4)
    assert len(forwards)==count
    diagnostic=pair_metrics(capture,replay,dataset,frozen,common,index)
    (master/'pair_metrics.json').write_text(json.dumps(diagnostic,ensure_ascii=False,indent=1))
    table=tabulate([[r['method'],'/'.join(r['pair']),r['D'],*r['own_margins'],r['reversal'],
                     r['complete_four_pair'],r['exact_scoring_text_equal']] for r in diagnostic['pairs']],
                    headers=['Method','Pair','D ↑','Own a ↑','Own b ↑','Reversal','Both four','Exact text equal'],tablefmt='pipe',floatfmt='.4f')
    report='---\ngenerations: 4\nmax_new_tokens: 32\noriginal_rows_exact: 72\ncandidate_rows: 16\n---\n# Same-answer animal identities\n\n— PI/OpenAI. Known concepts, new property/frame; unmasked margins are not purity or necessity. All cases retained. Semantic review pending.\n\n'+table+'\n'
    for i,trace in enumerate(traces):
        row=index[i,common['METHODS'][0]]
        report+=f"\n## {i}: {row['concept']}\n\nInput repr:\n```text\n{row['prompt']!r}\n```\n\nExact continuation:\n```text\n{row['baseline_generation']}\n```\n\nTokens: {len(trace['token_ids'])}.\n"
        for method in common['METHODS']:
            r=index[i,method]
            report+=f"\n### {method}\n\nLexical joint={r['alias_checked_pass']}; alias AUROC={r['alias_checked_auroc']}.\n\n{r['top32']!r}\n"
    report+=f'\nCapture: {capture}/run.md\n\nComplete candidate records: {replay}/readout.json\n'
    (master/'run.md').write_text(report)
    metadata.update(stage='completed',replay=str(replay),elapsed_seconds=time.monotonic()-started,
                    original_rows_exact=72,candidate_rows=16,rescore_forward_calls=0,
                    generated_tokens=sum(len(t['token_ids']) for t in traces),semantic_review_pending=True,
                    peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30)
    (master/'pipeline.json').write_text(json.dumps(metadata,indent=1))
    print(json.dumps(metadata,indent=1),flush=True)
    print(table,flush=True)
    print('run.md: '+str(master/'run.md'),flush=True)


if __name__=='__main__':
    main(Path(sys.argv[1]),preflight='--preflight' in sys.argv[2:])
