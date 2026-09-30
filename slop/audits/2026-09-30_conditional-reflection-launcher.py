"""Frozen reverse legs/body test; no probe feeds subsequent editing. — PI/OpenAI"""
import faulthandler
import gc
from pathlib import Path
import runpy
import sys

faulthandler.dump_traceback_later(90, repeat=True)
root = Path(__file__).resolve().parents[2]
namespace = runpy.run_path(sys.argv[1])
for relation in ('legs', 'skeleton_body'):
    namespace['logger'].remove()
    namespace['logger'].add(sys.stderr)
    namespace['main'](block_index=15, readout_block_index=23, reverse=True,
                      prompt_positions=1, decode_scale=1.0, plural=True,
                      donor_checkpoint=root / 'out/2026-09-30_133218_jlens-one-pass/donors.pt',
                      donor_reflection=True, relation=relation)
    gc.collect()
    namespace['torch'].cuda.empty_cache()
faulthandler.cancel_dump_traceback_later()
