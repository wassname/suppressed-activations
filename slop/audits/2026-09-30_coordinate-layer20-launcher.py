"""Test the intermediate layer between earlier16 and24 coordinate trials. — PI/OpenAI"""
import faulthandler
import gc
from pathlib import Path
import runpy
import sys

faulthandler.dump_traceback_later(90, repeat=True)
root = Path(__file__).resolve().parents[2]
namespace = runpy.run_path(str(root / '.local/queued/08_decode_control_9cba28e.py'))
for reverse in (False, True):
    namespace['logger'].remove()
    namespace['logger'].add(sys.stderr)
    namespace['main'](block_index=19, readout_block_index=23, reverse=reverse,
                      cases_json=root / '.local/queued/intervention_only.json', prompt_positions=3, decode_scale=1.0)
    gc.collect()
    namespace['torch'].cuda.empty_cache()
faulthandler.cancel_dump_traceback_later()
