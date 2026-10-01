"""Frozen readout on eight known probes under a uniform native-chat frame. — PI/OpenAI"""
from datetime import datetime
import faulthandler
import gc
import hashlib
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
SOURCE_SHA = '69455b6a07824eb675d6f738c6178691d9ff31929267944aae1b9ddf4eac6f3d'
DATA_SHA = '5b2fa09b97f8ccc3b8775da7bfe7b9dc4983e6e42aad39ab8c4e1202113ccbc0'
CONTRACT_SHA = '606a053bb4c7f3718b9bfbabfe35e3c63853cf1c3fd43faca6fd5d75720daf8a'
HELPERS = {
    'scripts/demo.py': '3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
    'scripts/english/01_detector_baselines_and_pair_transfer.py': '812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
    'scripts/english/03_selector_search.py': '51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
    'scripts/english/04_erase_and_language_pairs.py': '734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
    'suppressed_activation_subspace.py': '415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254',
}
BASE_METHODS = ['end-pass erased0.5 J-lens', 'end-pass erased0.5 plain24',
                'end-pass erased0.5 plain27', 'end-pass J-lens']
METHODS = [m.replace('end-pass ', 'end-pass input-prefix ', 1) for m in BASE_METHODS]


def check_replay(capture, replay, n):
    old = json.loads((capture / 'readout.json').read_text())
    rows = json.loads((replay / 'readout.json').read_text())
    index = {(r['case_index'], r['method']): r for r in rows}
    assert len(old) == 18 * n and len(rows) == len(index) == 22 * n
    assert all(index[r['case_index'], r['method']] == r for r in old)
    assert (capture / 'generation_traces.json').read_bytes() == (replay / 'generation_traces.json').read_bytes()
    a = torch.load(capture / 'prefill.pt', map_location='cpu', weights_only=True)
    b = torch.load(replay / 'prefill.pt', map_location='cpu', weights_only=True)
    assert len(a) == len(b) == n
    assert all(torch.equal(x[k], y[k]) for x, y in zip(a, b, strict=True) for k in x)
    exclusions = json.loads((replay / 'input_prefix_exclusions.json').read_text())
    assert len(exclusions) == n
    for i, item in enumerate(exclusions):
        added = {r['id'] for r in item['added_input_exclusions']}
        saved = torch.load(replay / 'input_prefix_scores' / f'{i:03d}.pt', weights_only=True, map_location='cpu')
        assert set(saved) == set(BASE_METHODS)
        for method in METHODS:
            assert not added.intersection(index[i, method]['selected_ids'])
    return index


def main(source, data):
    started = time.monotonic()
    faulthandler.dump_traceback_later(120, repeat=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA
    assert hashlib.sha256(data.read_bytes()).hexdigest() == DATA_SHA
    dataset = json.loads(data.read_text())
    original_path = ROOT / dataset['source_dataset']
    assert hashlib.sha256(original_path.read_bytes()).hexdigest() == dataset['source_dataset_sha256']
    original = json.loads(original_path.read_text())
    assert len(dataset['cases']) == 8 and dataset['prefix'] == ''
    for old, new in zip(original['cases'], dataset['cases'], strict=True):
        assert new == {**old, 'prompt': 'Complete the fact with only the missing word or phrase:\n' + old['prompt']}
    contract = ROOT / 'slop/audits/2026-10-01_native-v4-preregistration.md'
    assert hashlib.sha256(contract.read_bytes()).hexdigest() == CONTRACT_SHA
    for name, sha in HELPERS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
    master = ROOT / 'out' / f'{datetime.now():%Y-%m-%d_%H%M%S}_native-v4-readout'
    master.mkdir(parents=True)
    for src, name in ((source, 'source.py'), (data, 'dataset.json'), (original_path, 'original_dataset.json'),
                      (Path(__file__), 'launcher.py'), (contract, 'preregistration.md')):
        shutil.copyfile(src, master / name)
    for name in HELPERS:
        dest = master / 'helpers' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    metadata = {'stage': 'preflight', 'source_sha256': SOURCE_SHA, 'data_sha256': DATA_SHA,
                'contract_sha256': CONTRACT_SHA, 'helper_sha256': HELPERS, 'goals_completed': False}
    (master / 'pipeline.json').write_text(json.dumps(metadata, indent=1))
    print(json.dumps({'master': str(master), 'stage': 'preflight'}), flush=True)
    g = runpy.run_path(str(source))['main'].__globals__
    torch.set_num_threads(4)
    forwards = []
    phase = 'capture'
    loader = g['AutoModelForCausalLM'].from_pretrained

    def record_forward(module, args, kwargs):
        ids = args[0] if args else kwargs['input_ids']
        record = {'phase': phase, 'sequence_length': ids.shape[1], 'grad_enabled': torch.is_grad_enabled()}
        forwards.append(record)
        with (master / 'forward_trace.jsonl').open('a') as stream:
            stream.write(json.dumps(record) + '\n')
        assert phase == 'capture', 'Rescoring must not call the transformer'

    def tracked_loader(*args, **kwargs):
        model = loader(*args, **kwargs)
        model.register_forward_pre_hook(record_forward, with_kwargs=True)
        return model

    g['AutoModelForCausalLM'] = SimpleNamespace(from_pretrained=tracked_loader)
    settings = {'cases_json': data, 'end_pass_readout': True, 'output_mask_max_n': 1,
                'erase_output': True, 'erase_strength': .5, 'chat_readout': True, 'readout_max_new_tokens': 32}
    capture = g['main'](**settings)
    traces = json.loads((capture / 'generation_traces.json').read_text())
    assert len(traces) == 8 and all(1 <= len(t['token_ids']) <= 32 for t in traces)
    assert len(forwards) == sum(len(t['token_ids']) for t in traces)
    assert not any(r['grad_enabled'] for r in forwards)
    assert [r['sequence_length'] for r in forwards] == [c['sequence_length'] for t in traces for c in t['coverage']]
    metadata.update(stage='captured', capture=str(capture), actual_forward_calls=len(forwards),
                    generated_tokens=sum(len(t['token_ids']) for t in traces),
                    capture_elapsed_seconds=time.monotonic() - started)
    (master / 'pipeline.json').write_text(json.dumps(metadata, indent=1))
    gc.collect()
    phase = 'rescore'
    replay = g['main'](**settings, replay_readout_run=capture, expand_input_prefix=True)
    index = check_replay(capture, replay, 8)
    assert len(forwards) == metadata['actual_forward_calls'] and all(r['phase'] == 'capture' for r in forwards)
    results = []
    for method in METHODS:
        rows = [index[i, method] for i in range(8)]
        aucs = [r['alias_checked_auroc'] for r in rows if r['alias_checked_auroc'] is not None]
        results.append({'method': method, 'n': 8, 'joint_alias_passes': sum(r['alias_checked_pass'] for r in rows),
                        'mean_alias_auroc': sum(aucs) / len(aucs) if aucs else None, 'auroc_n': len(aucs),
                        'expected_answer_matches': sum(r['intended_answer_observed'] for r in rows)})
    (master / 'summary.json').write_text(json.dumps(results, indent=1))
    table = tabulate([[r['method'], f"{r['joint_alias_passes']}/8", r['mean_alias_auroc'], r['auroc_n'],
                       f"{r['expected_answer_matches']}/8"] for r in results],
                     headers=['Method', 'Lexical joint ↑', 'Alias AUROC ↑', 'AUROC n', 'Expected-answer matches'],
                     tablefmt='pipe', floatfmt='.4f')
    report = ('---\ngenerations: 8\nmax_new_tokens: 32\noriginal_rows_exact: 144\ncandidate_rows: 32\n---\n'
              '# Frozen prefix readout, native-chat v4\n\n— PI/OpenAI. Known concepts under a new uniform frame, not heldout concepts. '
              'Same head as2686; original144 rows exact,32 candidates. Full-list semantic review pending. '
              'Generated text is evaluation-only; rescoring has zero transformer calls.\n\n' + table + '\n')
    for i in range(8):
        row = index[i, METHODS[0]]
        report += f"\n## {i}: {row['concept']}\n\nRendered input repr:\n```text\n{row['prompt']!r}\n```\n\nExact continuation:\n```text\n{row['baseline_generation']}\n```\n\nToken count: {len(traces[i]['token_ids'])}.\n"
        for method in METHODS:
            r = index[i, method]
            report += f"\n### {method}\n\nLexical joint={r['alias_checked_pass']}.\n\n{r['top32']!r}\n"
    report += f'\nCapture: {capture}/run.md\n\nFull candidate records: {replay}/readout.json\n'
    (master / 'run.md').write_text(report)
    for name, sha in HELPERS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
    metadata.update(stage='completed', replay=str(replay), elapsed_seconds=time.monotonic() - started,
                    original_rows_exact=144, candidate_rows=32, rescore_forward_calls=0,
                    peak_allocated_gib=torch.cuda.max_memory_allocated() / 2**30,
                    semantic_review_pending=True)
    (master / 'pipeline.json').write_text(json.dumps(metadata, indent=1))
    print(json.dumps(metadata, indent=1), flush=True)
    print(table, flush=True)
    print('run.md: ' + str(master / 'run.md'), flush=True)
    faulthandler.cancel_dump_traceback_later()


if __name__ == '__main__':
    main(*map(Path, sys.argv[1:]))
