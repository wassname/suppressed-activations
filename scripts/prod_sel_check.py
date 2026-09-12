# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru>=0.7", "pyarrow>=21", "tabulate>=0.9", "torch>=2.8", "transformers>=5.5"]
# ///
import json, torch, sys
sys.path.insert(0, '.')
from suppressed_activation_subspace import increment_scores, suppressed_activation_scores
BANK = __import__('pathlib').Path('out/2026-09-12_exact-input-bank-att3')
unembed = torch.load(BANK/'unembedding.pt', weights_only=False).float()
gain = torch.load(BANK/'norm_gain.pt', weights_only=False).float()
cmp_data = json.load(open('out/2026-09-12_selector-comparison-v2/selector_comparison.json'))
mismatch = 0; n = 0
for name, entry in cmp_data['per_cell'].items():
    res = torch.load(BANK/f'{name}_residuals.pt', weights_only=False).float()
    seq = res.shape[1]; a = seq - 4
    rows1 = res.permute(1, 0, 2)
    sc = increment_scores(rows1, unembed, gain, normalize_unembedding_rows=True)
    top = sc[a:].topk(8, dim=-1).indices.tolist()
    n += 1
    if top != entry['increment_cand_ids']:
        mismatch += 1
        if mismatch <= 2: print("MISMATCH", name)
print(f"production increment_scores vs CPU candidate IDs: {n-mismatch}/{n} identical")
snap_mismatch = 0
for name, entry in cmp_data['per_cell'].items():
    res = torch.load(BANK/f'{name}_residuals.pt', weights_only=False).float()
    seq = res.shape[1]; a = seq - 4
    rows1 = res.permute(1, 0, 2)
    sc = suppressed_activation_scores(rows1, unembed, gain, early_layer=23, peak_layer=25,
                                      output_layer=32, normalize_unembedding_rows=True)
    top = sc[a:].topk(8, dim=-1).indices.tolist()
    if top != entry['snapshot3_ids']: snap_mismatch += 1
print(f"snapshot selector vs CPU snapshot IDs: {24-snap_mismatch}/24 identical")
json.dump({'production_increment_vs_cpu': f'{24-mismatch}/24', 'snapshot_vs_cpu': f'{24-snap_mismatch}/24'},
          open('out/2026-09-12_selector-comparison-v2/production_selector_equality.json','w'), indent=1)
