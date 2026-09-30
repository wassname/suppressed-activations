"""Check frozen reflection execution; semantic judgment remains separate. — PI/OpenAI"""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

expected_source = subprocess.check_output(['git', 'show', '86445f1:scripts/english/08_jlens_one_pass.py'])
for argument in sys.argv[1:]:
    root = Path(argument)
    assert (root / 'source.py').read_bytes() == expected_source
    report = (root / 'run.md').read_text()
    for setting in ('block_index: 15\n', 'reverse: true\n', "prompt_slice: '-1:'\n", 'decode_scale: 1.0\n', 'donor_reflection: true\n'):
        assert setting in report, setting
    conditions = json.loads((root / 'interventions.json').read_text())
    base = conditions['Base']
    reference_stamp = {'8':'142712', ' outside':'142748'}[base['answer_0']]
    reference = json.loads(Path(f'out/2026-09-30_{reference_stamp}_jlens-one-pass/interventions.json').read_text())['Base']
    for field in ('token_ids', 'generation', 'top10', 'prefill_readout', 'final_decode_readout'):
        assert base[field] == reference[field], field
    special = set(json.loads((root / 'tokenizer_special_ids.json').read_text())['r2_excluded_ids'])
    donor = json.loads((root / 'donor_provenance.json').read_text())
    summaries = {}
    for name, row in conditions.items():
        calls = row['coverage']
        assert 1 <= len(calls) == len(row['token_ids']) == row['n_tokens'] <= 32
        assert all(c['positions'] == 1 and c['scale'] == 1 for c in calls)
        assert all(c['sequence_length'] == 1 for c in calls[1:])
        error = 0.0
        for c in calls:
            before, requested, realized = (c[k][0] for k in ('donor_margin_before', 'donor_margin_requested', 'donor_margin_after'))
            dose, applied = c['requested_delta_norm'][0], c['applied_delta_norm'][0]
            assert c['source_side'] == [before < 0]
            if name == 'conditional donor reflection':
                assert math.isclose(requested, abs(before), rel_tol=1e-5, abs_tol=1e-5)
            if name in ('conditional donor reflection', 'matched-random reflection control'):
                assert math.isclose(dose, 2 * max(-before, 0), rel_tol=1e-5, abs_tol=1e-5)
            if name == 'full donor contrast':
                assert math.isclose(dose, donor['native_donor_norm'], rel_tol=1e-5, abs_tol=1e-5)
            if dose == 0:
                assert applied == 0 and requested == realized
            error = max(error, abs(realized-requested))
        a0, a1 = row['p_answer0'], row['p_answer1']
        odds = math.log(a1/a0)-math.log(base['p_answer1']/base['p_answer0'])
        assert abs(odds-row['answer_log_odds_shift']) < 1e-5
        assert abs(a0+a1-row['answer_pair_mass']) < 1e-6
        ids = [t for t in row['token_ids'] if t not in special]
        bigrams = list(zip(ids, ids[1:]))
        repetition = 1-len(set(bigrams))/len(bigrams) if bigrams else 0
        assert abs(repetition-row['r2']) < 1e-9
        summaries[name] = {'first_line':row['generation'].splitlines()[0], 'n_tokens':row['n_tokens'],
            'prefill_margin':calls[0]['donor_margin_before'][0], 'max_cast_margin_error':error,
            'source_side_calls':sum(any(c['source_side']) for c in calls),
            'updated_calls':sum(any(v > 0 for v in c['applied_delta_norm']) for c in calls),
            'requested_norm_sum':sum(sum(c['requested_delta_norm']) for c in calls)}
    ref = conditions['conditional donor reflection']['coverage'][0]['requested_delta_norm'][0]
    rand = conditions['matched-random reflection control']['coverage'][0]['requested_delta_norm'][0]
    assert math.isclose(ref,rand,rel_tol=1e-5,abs_tol=1e-5)
    target = json.loads((root / 'clean_target_probe.json').read_text())
    source_margin = base['coverage'][0]['donor_margin_before'][0]
    result = {'author':'PI/OpenAI', 'status':'PASS numerical/coverage checks',
        'source_sha256':hashlib.sha256(expected_source).hexdigest(),
        'clean_source_margin':source_margin, 'clean_target_margin':target['donor_margin'],
        'clean_prefill_separation':source_margin < 0 < target['donor_margin'],
        'conditions':summaries,
        'limits':'No semantic/coherence certification. Later random gates and doses are not trajectory matched.'}
    (root / 'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=1))
    print(json.dumps({'run':str(root),**result},ensure_ascii=False,indent=1))
