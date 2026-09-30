"""One cached v4 development comparison; selection is not semantic validation. -- PI/OpenAI"""
import json
import runpy
import sys
from pathlib import Path

from loguru import logger

main = runpy.run_path(sys.argv[1])['main']
out = main(cases_json=Path(sys.argv[2]), end_pass_readout=True, output_mask_max_n=1,
           erase_output=True, erase_strength=.5, token_kl=True,
           replay_readout_run=Path('out/2026-09-30_142814_jlens-one-pass'))
rows = {row['method']:row for row in json.loads((out/'summary.json').read_text())}
order = ['plain27','J-lens','plain24']
counts = {name:rows['end-pass positive token-KL '+name]['alias_checked_joint_pass'] for name in order}
assert all(rows['end-pass positive token-KL '+name]['n']==8 for name in order)
winner = max(order,key=counts.__getitem__)
mismatched = rows['end-pass mismatched positive token-KL '+winner]['alias_checked_joint_pass']
assert rows['end-pass erased0.5 plain27']['alias_checked_joint_pass'] == 6
selection = {'author':'PI/OpenAI','role':'v4 development screening only', 'tie_order':order,
             'matched_counts':counts, 'selected_representation':winner,
             'selected_mismatched_count':mismatched, 'n':8,
             'numeric_screen_passed':counts[winner]>=7 and counts[winner]>mismatched,
             'all_three_perfect':all(count==8 for count in counts.values()),
             'semantic_review':'not performed; required before new-example evaluation; no switching winner if it fails',
             'limits':'Matched/mismatched near-equality or ceiling requires investigation, not a subtraction-benefit claim.'}
(out/'token_kl_selection.json').write_text(json.dumps(selection,indent=1))
logger.info('{}',json.dumps(selection,indent=1))
print(out/'run.md')
