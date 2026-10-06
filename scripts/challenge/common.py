"""Shared model, lens, vocabulary and forward pass for the challenge scripts. — PI/OpenAI"""
import hashlib
import re
from pathlib import Path

import torch
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]


def fetch(rel, url, md5):
    """Download a data file once and check it."""
    path = ROOT / rel
    if not path.exists():
        import urllib.request
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, path)
    assert hashlib.md5(path.read_bytes()).hexdigest() == md5, f"{path} does not match {url}"
    return path


TWOHOP = lambda: fetch("data/twohop/TwoHopFact.csv",  # CC-BY-4.0, Yang et al. 2024
                       "https://huggingface.co/datasets/soheeyang/TwoHopFact/resolve/main/TwoHopFact.csv",
                       "02f99628a997e73d34c51693cf9aef44")
WENDLER_ZH = lambda: fetch("data/wendler_words/zh/clean.csv",  # Wendler et al. 2024 word list
                           "https://raw.githubusercontent.com/epfl-dlab/llm-latent-language/main/data/langs/zh/clean.csv",
                           "444042b7f62f06afdd18b122150d47e4")
MODEL, REVISION = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LENS = ("neuronpedia/jacobian-lens", "qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt",
        "16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a", "1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e")
LANG_NAME = {"ru": "Русский", "ko": "한국어", "ar": "العربية", "hi": "हिन्दी", "th": "ไทย"}
SCRIPT = {"ru": "\u0400-\u04ff", "ko": "\u1100-\u11ff\u3130-\u318f\uac00-\ud7af", "ar": "\u0600-\u06ff\u0750-\u077f",
          "hi": "\u0900-\u097f", "th": "\u0e00-\u0e7f"}  # Unicode blocks; none shared with each other, Latin or Han

torch.set_grad_enabled(False)
tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # CPU works too, slowly
model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=torch.bfloat16).to(DEVICE).eval()
W, gain = model.lm_head.weight.float(), 1.0 + model.model.norm.weight.float()  # output head; final RMSNorm gain
vocab = [tok.convert_tokens_to_string([t]) if t is not None else "" for t in tok.convert_ids_to_tokens(list(range(W.shape[0])))]


def load_jlens():
    """J[l] maps the residual after block l (residual l+1) to the final residual."""
    repo, file, rev, sha = LENS
    path = hf_hub_download(repo, filename=file, revision=rev)
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == sha
    return torch.load(path, weights_only=True, map_location="cpu")["J"]


def rms(h):
    h = h.float()
    return h * torch.rsqrt(h.square().mean(-1, keepdim=True) + 1e-6)


def readout(v):
    """The model's own output head on residual-space vectors [..., d] -> [..., vocab]."""
    return (gain * rms(v)) @ W.T


def tokens_in_script(pattern):
    return frozenset(t for t, v in enumerate(vocab) if re.search(f"[{pattern}]", v))


_captured = {}
model.model.norm.register_forward_pre_hook(lambda _m, args: _captured.__setitem__("final", args[0]))
model.model.layers[23].self_attn.register_forward_hook(lambda _m, _a, out: _captured.__setitem__("attn23", out[0]))


def forward(text, max_length=None):
    """One forward pass. Returns residuals [33, seq, d] (index 32 = before the final norm), layer-23 attention output
    [seq, d], and next-token logits at the last position."""
    ids = tok(text, return_tensors="pt", add_special_tokens=False, truncation=max_length is not None, max_length=max_length).input_ids.to(DEVICE)
    out = model(input_ids=ids, use_cache=False, output_hidden_states=True)
    res = torch.stack(list(out.hidden_states[:-1]) + [_captured["final"]])[:, 0]
    return res, _captured["attn23"][0], out.logits[0, -1].float()
