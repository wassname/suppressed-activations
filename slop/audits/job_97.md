# Job 97 audit

Target: pueue job 97, the requested Spider→Ant direct and within-subspace coordinate test. It exited 1 before model loading. Sources: [`job_97_full.log`](job_97_full.log), [`job_97_script.py`](job_97_script.py), [`job_97_status.json`](job_97_status.json).

| stage | expected | observed | consequence |
|---|---|---|---|
| repository import | import `scripts.demo` | `ModuleNotFoundError: No module named 'scripts'` | no model or intervention ran |
| extraction | find Spider in the prompt subspace | absent | unresolved |
| coordinate swaps | compare direct and projected Spider→Ant | absent | unresolved |

> File "/workspace/2026/suppressed-activations/.local/spider_ant_coordinates.py", line 8, in <module>
> from scripts.demo import ...
> ModuleNotFoundError: No module named 'scripts'

### H1 [harness | Almost Certain | 99%]
- **Mechanism:** Python adds `.local/`, not its repository parent, to `sys.path` for this script.
- **Evidence:** the missing module is the local `scripts` package; execution stopped at line 8.
- **Contrary evidence:** none.
- **Test/action:** insert the repository parent before local imports and rerun unchanged settings.

### H2 [method | Chances a little better than even | 50%]
- **Mechanism:** a direct Spider→Ant coordinate swap changes 8 toward 6.
- **Evidence:** none from this run.
- **Contrary evidence:** none from this run.
- **Test/action:** same experiment after only the import fix.

### H3 [data | Remote | 5%]
- **Mechanism:** model, prompt, or tokenization caused the failure.
- **Evidence:** none; these stages were not reached.
- **Contrary evidence:** import failed first.
- **Test/action:** do not alter data.

Decision: the resolve condition is not judgeable. This is an invalid scientific run with probability 0.99–1.00. The earliest failed link is repository import. The next action is a same-protocol rerun with only `sys.path` corrected.

Written by PI/gpt-5.4.
