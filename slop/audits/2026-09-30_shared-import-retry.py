"""Retry unchanged experiments with imports shared; no scientific method change. — PI/OpenAI"""
import faulthandler
import gc
from pathlib import Path
import runpy
import sys

faulthandler.dump_traceback_later(90, repeat=True)
root = Path(__file__).resolve().parents[2]
source = root / '.local/queued/08_frozen_4fc70e4.py'
namespace = runpy.run_path(str(source))
common = dict(donor_checkpoint=root / 'out/2026-09-30_105132_jlens-one-pass/donors.pt',
              plural=True, equal_donor_norm=True, prompt_positions=1)
for case in ({'reverse': True}, {'relation': 'skeleton_body'}):
    namespace['logger'].remove()
    namespace['logger'].add(sys.stderr)
    namespace['main'](**common, **case)
    gc.collect()
    namespace['torch'].cuda.empty_cache()
faulthandler.cancel_dump_traceback_later()
