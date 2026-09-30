"""One fixed country-coordinate experiment, two properties, no outcome-dependent branches. -- PI/OpenAI"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import time

from tabulate import tabulate

helpers = {
    'scripts/demo.py':'3fd42d760c0ed01a68e7160b7d64c87168f1859f008e232464f7e10c01c4bc39',
    'scripts/english/01_detector_baselines_and_pair_transfer.py':'812afe3ca2728b2c6ebfb6d516b1edb11e51e6849182bdb8b172ff277c61fa8b',
    'scripts/english/03_selector_search.py':'51523c7a3769dd11184dbfe6d134213584ed203a6effc44a940ade8b8af358fb',
    'scripts/english/04_erase_and_language_pairs.py':'734ab7803a3884eb248daceb7bc3fad5b2e85b42b542de20205901402c4c65f0',
    'suppressed_activation_subspace.py':'415b39ec6d5960ef0bf1533ec271ac4d9fd22bde6fd14f322c454e4f65a5b254'}
helper_bytes = {p:Path(p).read_bytes() for p in helpers}
assert all(hashlib.sha256(helper_bytes[p]).hexdigest()==digest for p,digest in helpers.items())
source = Path(sys.argv[1]); source_bytes = source.read_bytes()
started = time.monotonic()
root = Path('out') / (time.strftime('%Y-%m-%d_%H%M%S')+'_country-swap')
root.mkdir(parents=True)
(root/'source.py').write_bytes(source_bytes)
(root/'launcher.py').write_bytes(Path(__file__).read_bytes())
(root/'helper_sha256.json').write_text(json.dumps(helpers,indent=1))
for p,data in helper_bytes.items():
    dest=root/'helpers'/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
main = runpy.run_path(str(source))['main']
g=main.__globals__
tok=g['AutoTokenizer'].from_pretrained(g['q'].MODEL,revision=g['q'].REVISION,local_files_only=True)
expected_ids={' Italy':[14898],' Japan':[6124],' Rome':[21047],' Tokyo':[25358],' euro':[17146],' yen':[55421]}
encoded={s:tok.encode(s,add_special_tokens=False) for s in expected_ids}
(root/'token_preflight.json').write_text(json.dumps(encoded,indent=1))
assert encoded==expected_ids,encoded
records=[]; results=[]
pipeline = {'author':'PI/OpenAI','source_sha256':hashlib.sha256(source_bytes).hexdigest(),
    'status':'incomplete','runs':[], 'generated_token_cap':320,'target_prefill_count':2,
    'primary':'raw J-coordinate exchange','selection':'One Italy-to-Japan pair across two properties, not independent concept swaps; no winner/prompt rescue.'}
(root/'pipeline.json').write_text(json.dumps(pipeline,indent=1))
for relation in ('capital','currency'):
    assert source.read_bytes()==source_bytes
    assert all(Path(p).read_bytes()==data for p,data in helper_bytes.items())
    out=main(block_index=15,readout_block_index=23,relation=relation,prompt_positions=1,decode_scale=1.)
    assert (out/'source.py').read_bytes()==source_bytes
    assert all(Path(p).read_bytes()==data for p,data in helper_bytes.items())
    (out/'helper_sha256.json').write_text(json.dumps(helpers,indent=1))
    (out/'experiment_root.txt').write_text(str(root.resolve())+'\n')
    conditions=json.loads((out/'interventions.json').read_text())
    assert list(conditions)==['Base','raw J-coordinate exchange','unit J-coordinate exchange','raw plain-coordinate exchange','matched-random delta']
    for mode,r in conditions.items():
        assert 0<r['n_tokens']<=32 and len(r['coverage'])==r['n_tokens']
        assert r['coverage'][0]['positions']==1
        assert all(c['positions']==1 and c['sequence_length']==1 for c in r['coverage'][1:])
        log=out/mode.lower().replace(' ','-')/'run.md'
        initial=r['generation'].splitlines()[0]
        records.append([f'[{relation}: {mode}]({os.path.relpath(log,root)})',r['answer_log_odds_shift'],r['expected_answer'],
                        repr(initial),r['answer_pair_mass'],r['r2'],r['n_tokens']])
    primary=conditions['raw J-coordinate exchange']; random=conditions['matched-random delta']
    results.append({'relation':relation,'base_initial_text':conditions['Base']['generation'].splitlines()[0],
        'primary_initial_text':primary['generation'].splitlines()[0],
        'primary_exceeds_random_bare_log_odds':primary['answer_log_odds_shift']>random['answer_log_odds_shift'],
        'semantic_validity':'unreviewed; lexical text is not an automatic success decision'})
    pipeline['runs'].append({'relation':relation,'path':str(out.resolve()),'n_tokens':sum(r['n_tokens'] for r in conditions.values())})
    (root/'pipeline.json').write_text(json.dumps(pipeline,indent=1))
assert len(records)==10 and sum(r['n_tokens'] for r in pipeline['runs'])<=320
pipeline.update(status='complete',results=results,elapsed_seconds=time.monotonic()-started)
(root/'pipeline.json').write_text(json.dumps(pipeline,indent=1))
table=tabulate(records,headers=['condition','answer log-odds shift','expected','initial text (not judged)','bare-answer mass','r2','tokens'],tablefmt='pipe',floatfmt='.5f')
md=('---\nexperiment: country-coordinate-swap\nmodel: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a\nblock_index: 15\nreadout_block_index: 23\nprompt_slice: "-1:"\ncontinuous: true\nstrength: 1\nmax_new_tokens: 32\nseed: 0\n---\n'
    '# One country pair, two properties\n\n-- PI/OpenAI\n\n'
    'SHOULD: correct Rome/euro Base answers become coherent Tokyo/yen under the SAME raw-coordinate rule, with greater target-directed bare-answer log odds than random on both. '
    'Initial text and numeric comparisons below are not a semantic verdict. An article can obscure first-token answer movement. '
    'Wrong Base invalidates the assay; do not replace prompts or promote a control. Inspect complete32-token continuations and source-country disclosure. '
    'No sparse decomposition or clean-pass clamp. Random matches the primary proposal norm on its own state; later doses differ. '
    'One selected pair, two dependent properties, five conditions each, no tuning. The prior trailing-space currency prompt failed; these exact no-space prompts were fixed before this run. '
    'Each property has one clean-target prefill AFTER its conditions, with no feedback to editing. '
    'Pinned source/helpers and full local tensors are saved; unmodified source/target passes never prepare the editor.\n\n'+table+'\n')
(root/'run.md').write_text(md)
print(table,flush=True)
print(root.resolve()/'run.md',flush=True)
