"""Remove diagnostic dumps from readable reports; retain raw results. -- Codex/GPT-6"""

import json
import re
from pathlib import Path


def compact(root: Path) -> None:
    changed = 0
    removed = 0
    for path in root.glob('*/conditions/*/run.md'):
        raw = path.parents[2] / 'result.json'
        if not raw.exists():
            continue
        original = path.read_text()
        if 'Resolved config:' not in original:
            continue
        rows = json.loads(raw.read_text())['rows']
        condition = next(row for row in rows if row['condition_id'] == path.parent.name)
        blocks = list(re.finditer(r'```json\n(.*?)\n```', original, re.S))
        updated = original
        for block in reversed(blocks[1:]):
            value = json.loads(block[1])
            assert any(value == condition[key] for key in (
                'readout_by_position', 'named_suppression_diagnostics',
                'clamped_donor', 'intervention_record', 'persistence',
            ) if key in condition), path
            updated = updated[:block.start()] + (
                '[Full diagnostic data](../../result.json) '
                f'(`rows` → `{condition["condition_id"]}`).'
            ) + updated[block.end():]
        if updated != original:
            before = re.findall(r'```(?:text|python)\n.*?\n```', original, re.S)
            after = re.findall(r'```(?:text|python)\n.*?\n```', updated, re.S)
            assert before == after, path
            path.write_text(updated)
            changed += 1
            removed += len(original) - len(updated)
    print(f'Compacted {changed} reports; removed {removed:,} characters of duplicated JSON. Exact model strings unchanged.')


if __name__ == '__main__':
    compact(Path('out'))
