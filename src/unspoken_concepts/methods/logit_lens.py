"""Logit lens methods and related variants. — PI/OpenAI"""
import torch
from ..model import W, gain, readout, rms
from .registry import unrestricted


@unrestricted("logit lens, best layer", (27,), about="Logit lens at layer 27, the best layer on the dev pair: what knowing the layer is worth")
def plain(s, l):  # the old rule: shows what knowing the layer is worth
    return readout(s["res"][l])


@unrestricted("logit lens minus read and said", (28, 8), about="Layer 28 minus the prompt's token directions and the model's top-8 next tokens")
def minus_read_and_said(s, l, k):  # remove the prompt's token directions and the model's top-k next tokens
    ids = torch.cat([s["ids"], s["logits"].topk(k).indices]).unique()
    Q = torch.linalg.qr((W[ids] * gain).T, mode="reduced").Q
    x = rms(s["res"][l])
    return readout(x - Q @ (Q.T @ x))
