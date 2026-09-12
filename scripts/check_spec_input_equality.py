# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json
from pathlib import Path
from tokenizers import Tokenizer
tok = Tokenizer.from_file('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json')
WRAPPER = "Answer the question with the answer first. Then describe the animal in three sentences."
bank = json.load(open('out/2026-09-12_exact-input-bank-att3/manifest.json'))
bank_by_cell = {}
for name, e in bank['entries'].items():
    bank_by_cell.setdefault(e['cell_id'], {})[e['side']] = e
specs = json.load(open('slop/common_basis_selsite_batch.json'))
rows = []
for spec in specs:
    dirname = Path(spec['output_dir']).name
    cell_id = next((c for c in bank_by_cell if c in dirname), None)
    assert cell_id, f"no bank cell for {dirname}"
    for side in ('source', 'donor'):
        e = bank_by_cell[cell_id][side]
        prompt = spec['source_prompt'] if side == 'source' else spec['target_prompt']
        ids = e['input_ids']
        text = tok.decode(ids)
        wrapper_ok = WRAPPER in text
        prompt_ok = prompt.strip() in text
        rows.append({'dir': dirname, 'side': side, 'cell': cell_id,
                     'wrapper_in_rendered': wrapper_ok, 'prompt_in_rendered': prompt_ok,
                     'n_tokens': len(ids), 'sha': e['rendered_input_sha256']})
ok = sum(1 for r in rows if r['wrapper_in_rendered'] and r['prompt_in_rendered'])
print(f"input equality: {ok}/{len(rows)} spec-vs-bank checks pass (wrapper + content)")
json.dump(rows, open('out/2026-09-12_cb-selsite-input-equality.json','w'), indent=1, ensure_ascii=False)
assert ok == len(rows)
