"""Separate saved-score drift from float32 log-softmax error. — PI/OpenAI"""
import json
from pathlib import Path
import numpy as np
import torch

torch.set_num_threads(4)
root=Path('out/2026-10-01_110004_animal-pairs-readout')
p=json.loads((root/'pipeline.json').read_text())
diag=json.loads((root/'pair_metrics.json').read_text())
labels=json.loads((root/'labels.json').read_text())['labels']
for i in range(4):
    tensors=torch.load(Path(p['capture'])/'unmasked_readout_scores'/f'{i:03d}.pt',weights_only=True)
    for method,z in tensors.items():
        lp32=z.log_softmax(-1)
        lp64=z.double().log_softmax(-1)
        a=z.numpy().astype(np.float64)
        np_lp=a-(a.max()+np.log(np.exp(a-a.max()).sum()))
        assert np.max(np.abs(np_lp-lp64.numpy()))<1e-10
        errors=[]
        for concept,tokens in labels.items():
            reported=diag['case_scores'][str(i)][method][concept]
            for token,stored in zip(tokens,reported['constituents'],strict=True):
                j=token['id']
                assert float(lp32[j])==stored['log_probability']
                errors.append(float(lp32[j])-float(lp64[j]))
        print(json.dumps({'case':i,'method':method,'saved_matches_torch_float32_exactly':True,
                          'max_abs_lp64_error':max(map(abs,errors)),'error_range':[min(errors),max(errors)],
                          'lp32_range':[float(lp32.min()),float(lp32.max())],
                          'log_normalizer32':float(z.max()-lp32[z.argmax()]),
                          'log_normalizer64':float(z.double().max()-lp64[z.argmax()])}),flush=True)
print('PASS saved values exactly reproduce float32; NumPy agrees with torch float64. — PI/OpenAI')
