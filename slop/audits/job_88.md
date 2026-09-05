# Job 88 audit

Target: pueue job 88, `uv run python /tmp/english_demo.py --output slop/research/spider_dog_trial.json`, in `/workspace/2026/suppressed-activations`; it exited 1 after three seconds. Sources: [`job_88_script.py`](job_88_script.py), [`job_88_full.log`](job_88_full.log), [`job_88_status.json`](job_88_status.json).

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| import | load repository projection functions | `ModuleNotFoundError` | no | full log lines 1–6 | none | no model code ran |
| model/extraction | load Qwen and extract spider/dog subspaces | absent | no | no loading lines | all readouts | scientific hypothesis untested |
| intervention/control | semantic replacement and 32 random controls | absent | no | no result artifact | all causal metrics | resolve condition not judgeable |
| persistence | JSON with provenance | absent | no | import failed before `main` | run metadata | no result exists |

## Primary evidence

The complete log is six lines:

> File "/tmp/english_demo.py", line 22, in <module>
>     from suppressed_activation_subspace import (
> ModuleNotFoundError: No module named 'suppressed_activation_subspace'

The saved script inserts `Path(__file__).resolve().parents[1]`. For `/tmp/english_demo.py` that path is `/`, not `/workspace/2026/suppressed-activations` ([`job_88_repro.log`](job_88_repro.log)).

## Hypotheses

### H1 [harness | Almost Certain | 99%]
- **Mechanism:** copying a repository script to `/tmp` invalidated its relative repository-root import.
- **Evidence:** the log names the missing local module; the path reproduction gives inserted path `/`.
- **Contrary evidence:** none.
- **Discriminating test:** run the script from `scripts/` or set `sys.path` to the explicit repository root; import should pass.
- **Action:** keep the trial script in the repository's ignored `.local/` directory and rerun unchanged experiment settings.
- **Interpretability:** no scientific result.

### H2 [method | Chances a little better than even | 50%]
- **Mechanism:** the spider→dog component replacement may change the answer toward `4`.
- **Evidence:** none from job 88; job 87 only established readout ranks.
- **Contrary evidence:** no intervention ran, and LM-head readout need not identify a causal direction.
- **Discriminating test:** the originally queued experiment with matched controls.
- **Action:** rerun after only the import-path fix.
- **Interpretability:** no.

### H3 [data | Remote | 5%]
- **Mechanism:** model or prompt data caused the failure.
- **Evidence:** none; execution stopped at module import.
- **Contrary evidence:** the model loader was never reached.
- **Discriminating test:** import succeeds before any model access after relocating the script.
- **Action:** do not alter prompts, layers, rank, or strengths.
- **Interpretability:** no.

## Decision

1. **Resolve-condition verdict:** not judgeable; no semantic or random intervention ran.
2. **Prediction check:** spider→dog beats 95% of controls — unresolved.
3. **Earliest unsupported link:** repository import; successful module import supports it.
4. **Validity:** `P(scientific result is invalid) ≈ 0.99–1.00`; classification: invalid run.
5. **Highest-information clues:** missing local module, `/tmp` script path, failure before model loading.
6. **Missing metrics:** every extraction and causal metric.
7. **Bugs requiring code changes:** H1 requires relocation or an explicit root path only.
8. **Misconceptions requiring reinterpretation:** none about the method; job 88 says nothing about it.
9. **What would change the verdict:** a successful unchanged rerun from a repository-local path.
10. **Recommended sequence:** relocate the exact script, rerun, then audit the causal result; do not change experiment settings.

Written by PI/gpt-5.4.
