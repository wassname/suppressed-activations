"""Inspect inventory overlap and native tokenization without model inference. -- PI/OpenAI"""
import csv
import hashlib
import json
import re
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path('/home/code/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')
DATA = ROOT / 'data/english_geography_chat_v1.json'
names = ['Oman', 'Qatar', 'Namibia', 'Botswana', 'Muscat', 'Doha', 'Windhoek', 'Gaborone']
patterns = {n: re.compile(r'\b'+re.escape(n)+r'\b', re.I) for n in names}
paths = sorted((ROOT/'data').glob('*.json')) + sorted((ROOT/'out').glob('*/cases.json'))
paths += [ROOT/'out/2026-09-29_204246_twohop-english/result.json']
paths = [p for p in paths if p != DATA and 'human' not in str(p).lower()]
hits = {n: [] for n in names}
for p in paths:
    text = p.read_text()
    for n, pattern in patterns.items():
        if pattern.search(text):
            hits[n].append(str(p.relative_to(ROOT)))
source = ROOT/'data/twohop/TwoHopFact.csv'
counts, examples = dict.fromkeys(names, 0), {n: [] for n in names}
with source.open() as stream:
    for row in csv.DictReader(stream):
        for n, pattern in patterns.items():
            matching = {k: v for k, v in row.items() if pattern.search(v)}
            if matching:
                counts[n] += 1
                if len(examples[n]) < 2:
                    examples[n].append(matching)
tok = AutoTokenizer.from_pretrained(CACHE, local_files_only=True)
generation = json.loads((CACHE/'config.json').read_text())['text_config']
recorded = json.loads((ROOT/'out/2026-10-01_045248_jlens-one-pass/generation_defaults.json').read_text())
assert isinstance(generation['eos_token_id'], int) and generation['eos_token_id'] == recorded['eos_token_id']
eos_ids = sorted({tok.eos_token_id, generation['eos_token_id']})
assert [tok.convert_ids_to_tokens(t) for t in eos_ids] == ['<|endoftext|>', '<|im_end|>']
vocab = [tok.convert_tokens_to_string([t]).strip().lower() for t in tok.convert_ids_to_tokens(list(range(len(tok))))]
rows = []
for case in json.loads(DATA.read_text())['cases']:
    messages = [{'role': 'user', 'content': case['prompt']}]
    rendered = tok.apply_chat_template(messages, tokenize=False, enable_thinking=False, add_generation_prompt=True)
    ids = tok.apply_chat_template(messages, tokenize=True, return_dict=False, enable_thinking=False, add_generation_prompt=True)
    assert tok(rendered, add_special_tokens=False).input_ids == ids
    assert 'Tokyo' not in rendered and '<think>\n\n</think>' in rendered
    labels = {a: [i for i, t in enumerate(vocab) if len(t) >= 3 and a.lower().startswith(t)]
              for a in case['hidden_aliases']+case['partner_aliases']+case['answer_aliases']}
    assert all(labels.values()), labels
    assert not set(sum((labels[a] for a in case['hidden_aliases']), [])) & set(sum((labels[a] for a in case['partner_aliases']), []))
    rows.append({'concept': case['concept'], 'rendered_repr': repr(rendered), 'input_ids': ids,
                 'pieces': tok.convert_ids_to_tokens(ids), 'labels': labels})
result = {'author': 'PI/OpenAI', 'model_revision': CACHE.name, 'model_forward_calls': 0,
          'data_sha256': hashlib.sha256(DATA.read_bytes()).hexdigest(),
          'inventories_checked': [str(p.relative_to(ROOT)) for p in paths], 'inventory_hits': hits,
          'twohop_source': str(source.relative_to(ROOT)), 'twohop_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'twohop_row_counts': counts, 'twohop_examples': examples,
          'novelty_limit': 'Corpus exposure is not proof of prior evaluation. Rejected TwoHopFact generations were not saved, so absence from recorded cases cannot establish unseen concepts. These are new prompt/property pairs, not certified-new concepts.',
          'chat_flags': {'enable_thinking': False, 'add_generation_prompt': True},
          'chat_template_sha256': hashlib.sha256(tok.chat_template.encode()).hexdigest(),
          'tokenizer_eos_id': tok.eos_token_id, 'model_eos_id': generation['eos_token_id'],
          'model_eos_source': 'Pinned config.json text_config, cross-checked against job2668 generation_defaults.json; no separate generation_config.json exists in the pinned snapshot.',
          'prospective_eos_ids': eos_ids, 'renderings': rows}
(ROOT/'slop/audits/2026-10-01_chat-preflight.json').write_text(json.dumps(result, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in result.items() if k not in ('inventories_checked', 'twohop_examples')}, ensure_ascii=False, indent=1))
