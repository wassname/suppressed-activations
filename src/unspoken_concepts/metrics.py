"""Prompt-level F1 and bootstrap intervals, without loading the model. — PI/OpenAI"""
import random


def f1(rs):
    tp, fp = sum(r["hidden"] for r in rs), sum(r["leaked"] for r in rs)
    return 2 * tp / (2 * tp + fp + len(rs) - tp)


def delta_ci(rs, base, n_boot=2000):
    """F1(rs) - F1(base) on the same prompts, with a 90% paired bootstrap interval."""
    by_key = {(r["split"], r["word"]): r for r in base}
    pairs = [(r, by_key[(r["split"], r["word"])]) for r in rs]
    assert len(pairs) == len(base)
    rng = random.Random(0)
    boots = sorted(f1(a) - f1(b) for a, b in (zip(*[rng.choice(pairs) for _ in pairs]) for _ in range(n_boot)))
    return f"{f1(rs) - f1(base):+.2f} ({boots[int(0.05 * n_boot)]:+.2f} to {boots[int(0.95 * n_boot)]:+.2f})"


def f1_ci(rs, n_boot=2000):
    """90% bootstrap interval over prompts."""
    rng = random.Random(0)
    boots = sorted(f1([rng.choice(rs) for _ in rs]) for _ in range(n_boot))
    return f"{boots[int(0.05 * n_boot)]:.2f}–{boots[int(0.95 * n_boot)]:.2f}"
