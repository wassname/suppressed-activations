"""Run the actual launcher with tiny real Qwen weights and the eight frozen inputs. — PI/OpenAI"""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from types import SimpleNamespace

import torch
from transformers import Qwen3_5TextConfig, Qwen3_5ForCausalLM

ROOT = Path.cwd()
source = ROOT / 'scripts/english/08_jlens_one_pass.py'
launcher_path = ROOT / 'slop/audits/2026-10-01_native-v4-launcher.py'
launcher = runpy.run_path(str(launcher_path))['main'].__globals__
g = runpy.run_path(str(source))['main'].__globals__
torch.set_grad_enabled(False)
torch.set_num_threads(1)
config = Qwen3_5TextConfig(vocab_size=248320, hidden_size=32, intermediate_size=64, num_hidden_layers=32,
    num_attention_heads=2, num_key_value_heads=1, head_dim=16, linear_key_head_dim=8, linear_value_head_dim=8,
    linear_num_key_heads=2, linear_num_value_heads=4, max_position_embeddings=256,
    bos_token_id=None, eos_token_id=248044, pad_token_id=248044,
    rope_parameters={'rope_type':'default','rope_theta':10000,'partial_rotary_factor':1.,
                     'mrope_interleaved':True,'mrope_section':[3,3,2]})
models = []


def tiny_loader(*args, **kwargs):
    torch.manual_seed(0)
    model = Qwen3_5ForCausalLM(config).to(torch.bfloat16).eval()
    model.cuda = lambda *a, **kw: model
    models.append(model)
    return model


with tempfile.TemporaryDirectory(dir=ROOT / '.local') as directory:
    tmp = Path(directory)
    for name in [*launcher['HELPERS'], 'data/english_hidden_words_v4.json',
                 'data/english_hidden_words_v4_chat.json', 'slop/audits/2026-10-01_native-v4-preregistration.md']:
        dest = tmp / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    torch.manual_seed(0)
    lens = tmp / 'lens.pt'
    torch.save({'d_model':32,'n_prompts':1000,'J':{15:torch.eye(32),23:torch.randn(32,32)/32**.5}}, lens)
    g['ROOT'] = tmp
    g['AutoModelForCausalLM'] = SimpleNamespace(from_pretrained=tiny_loader)
    g['hf_hub_download'] = lambda *args, **kwargs: str(lens)
    g['LENS_SHA'] = hashlib.sha256(lens.read_bytes()).hexdigest()
    launcher['ROOT'] = tmp
    launcher['runpy'] = SimpleNamespace(run_path=lambda path: {'main': g['main']})
    cuda, mask = torch.Tensor.cuda, g['q'].prompt_word_mask
    torch.Tensor.cuda = lambda self, *args, **kwargs: self
    g['q'].prompt_word_mask = lambda prompt, vocab, device: mask(prompt, vocab, 'cpu')
    try:
        launcher['main'](source, tmp / 'data/english_hidden_words_v4_chat.json')
        master, = (tmp / 'out').glob('*_native-v4-readout')
        metadata = json.loads((master / 'pipeline.json').read_text())
        assert metadata['stage'] == 'completed'
        assert metadata['original_rows_exact'] == 144 and metadata['candidate_rows'] == 32
        assert metadata['rescore_forward_calls'] == 0 and metadata['generated_tokens'] <= 256
        assert len(models) == 2
        assert all(torch.equal(a, b) for a, b in zip(models[0].parameters(), models[1].parameters(), strict=True))
        traces = json.loads((Path(metadata['capture']) / 'generation_traces.json').read_text())
        forwards = [json.loads(s) for s in (master / 'forward_trace.jsonl').read_text().splitlines()]
        launcher['check_forward_trace'](traces, forwards)
        altered = json.loads(json.dumps(traces))
        altered[0]['coverage']['27'][0] += 1
        try:
            launcher['check_forward_trace'](altered, forwards)
        except AssertionError:
            pass
        else:
            raise AssertionError('Mismatched layer coverage was accepted')
        print('PASS actual launcher seed0: eight fixed inputs,144 old rows exact+32 candidates, '
              'two tiny model loads, one generation per input, zero cached forwards, '
              'coverage mismatch rejected, unchanged weights, final report and all assertions', flush=True)
    finally:
        torch.Tensor.cuda = cuda
        g['q'].prompt_word_mask = mask
print('Tiny random32-layer BF16 Qwen CPU only; no pretrained behavioral result. Source/launcherSHA:',
      hashlib.sha256(source.read_bytes()).hexdigest(), hashlib.sha256(launcher_path.read_bytes()).hexdigest(), flush=True)
