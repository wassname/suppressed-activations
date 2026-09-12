# /// script
# requires-python = ">=3.12"
# ///
"""Baseline drift + semantic analysis for the 2x2 batch (runs post-1149). -- PI[claude]"""
import json, hashlib, statistics as st
from pathlib import Path
B = Path('out/2026-09-12_cb-2x2')
HIST = Path('out/2026-09-10_eval-candidate-C1.5-')
conds = ["A-baseline","B-injref-remPs","C-injv-remPref","D-injv-remPs","C0-remPref","C0-remPs"]
def qtype(cid): return cid.split('-')[0]
rows = {}
for cond in conds:
    cells = sorted(B.glob(f"{cond}-*"))
    rows[cond] = {c.name[len(cond)+1:]: json.load(open(c/'result.json'))['rows'][0] for c in cells}
# 1) historical drift: arm A vs the 2026-09-10 candidate continuations (byte level + first logits)
drift = []
for cid, r in rows['A-baseline'].items():
    h = json.load(open(HIST.with_suffix('') .__str__() if False else f'out/2026-09-10_eval-candidate-C1.5-{cid}/result.json'))['rows'][0]
    same_text = r['generation']['text'] == h['generation']['text']
    same_hash = r['first_logits_sha256']['steered'] == h['first_logits_sha256']['steered']
    drift.append({'cell': cid, 'text_identical': same_text, 'steered_hash_identical': same_hash,
                  'tokens_now': r['generation_tokens'], 'tokens_hist': h['generation_tokens']})
# 2) semantic outcomes per condition
def verdict(r):
    t = r['generation']['text']
    return {'first60': t[:60], 'tokens': r['generation_tokens'], 'r2': r['repeated_bigram_fraction']}
out = {'drift': drift, 'semantics': {c: {k: verdict(r) for k, r in rs.items()} for c, rs in rows.items()}}
Path('out/2026-09-12_cb-2x2/analysis.json').write_text(json.dumps(out, indent=1))
n_same = sum(1 for d0 in drift if d0['text_identical'])
n_hash = sum(1 for d0 in drift if d0['steered_hash_identical'])
print(f"baseline drift: {n_same}/12 text-identical to historical; {n_hash}/12 steered-hash identical")
