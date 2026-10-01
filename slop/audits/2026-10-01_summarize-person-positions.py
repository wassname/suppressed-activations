"""Posthoc views of recorded positions, not a new selector or inference path. — PI/OpenAI"""
import json
from pathlib import Path

master=Path('out/2026-10-01_145856_person-position-diagnostic')
run=Path(json.loads((master/'pipeline.json').read_text())['run'])
data=json.loads(Path('data/english_person_pairs_chat_v1.json').read_text())
methods=['end-pass input-prefix erased0.5 J-lens','end-pass input-prefix erased0.5 plain24','end-pass input-prefix erased0.5 plain27','end-pass input-prefix J-lens']
text='# Person readouts before the assistant prefix\n\n— PI/OpenAI. Posthoc views from2718, not new cases or a deployable-selector result. Every position was inspected numerically; the two views below are chosen after observing those curves. Boundary = newline after the user close marker, before the assistant header. Title end is a labelled-input diagnostic, not a proposed language-independent rule. Full generations and all88 original rows exactly match2716.\n'
summary=[]
for i,case in enumerate(data['cases']):
    record=json.loads((run/'position_readouts'/f'{i:03d}.json').read_text())
    rows=record['records'];by_position={r['position']:r['consumed_prefix'] for r in rows}
    boundary,=[p for p,s in by_position.items() if s.endswith('<|im_end|>\n')]
    title=case['prompt'].split(' was born')[0]
    title_end,=[p for p,s in by_position.items() if s.endswith(title)]
    text+='\n## '+case['concept']+'\n'
    for kind,p in [('title-end diagnostic',title_end),('pre-assistant boundary',boundary)]:
        text+=f'\n### {kind}, position{p}\n\nConsumed prefix repr:\n```text\n{by_position[p]!r}\n```\n'
        for method in methods:
            row,=[r for r in rows if r['position']==p and r['method']==method]
            text+=f"\n{method}: masked alias rank={row['masked_alias_rank']}, token={row['masked_best_alias_token']!r}; raw rank={row['raw_alias_rank']}, token={row['raw_best_alias_token']!r}.\n\n{row['tokens']!r}\n"
            summary.append({'case_index':i,'view':kind,'position':p,'method':method,'masked_alias_rank':row['masked_alias_rank'],
                            'masked_best_alias_token':row['masked_best_alias_token'],'selected_alias_ids':row['selected_alias_ids']})
text+='\nSource: '+str(run/'position_readouts')+'\n'
(master/'position_views.md').write_text(text)
(master/'position_views.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1))
print(str(master/'position_views.md'))
