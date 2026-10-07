"""Built-in method families; load model-dependent methods explicitly. — PI/OpenAI"""
from importlib import import_module

from .registry import TRANSFORMS as TRANSFORMS


def load_methods():
    for family in ("controls", "pca", "minus_ends", "embedding_window", "logit_lens", "jacobian_lens", "rise_and_fall"):
        import_module(f"{__name__}.{family}")
