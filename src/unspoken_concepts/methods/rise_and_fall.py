"""Rise and fall methods and related variants. — PI/OpenAI"""
import torch
from ..model import W, gain, readout, rms
from ..calibration import bases
from .registry import unrestricted
from .jacobian_lens import jlens


def _token_span(scores, rank):
    """Orthonormal basis for the (centred, gain-scaled) unembedding rows of the top-`rank` tokens."""
    ids = scores.topk(rank).indices
    return torch.linalg.qr(((W - W.mean(0))[ids] * gain).T, mode="reduced").Q


def _rise_fall(early, peak, out):
    rise, fall = peak - early, peak - out
    return torch.minimum((rise - rise.mean()).clamp_min(0), (fall - fall.mean()).clamp_min(0))


@unrestricted("rise-and-fall", (27,), about="Tokens whose logit rises from layer 22 to 27 and falls by the output")
def rise_and_fall(s, peak):  # tokens whose logit rises from layer 22 to the peak and falls by the output
    return _rise_fall(readout(s["res"][22]), readout(s["res"][peak]), readout(s["res"][32]))


@unrestricted("rise-and-fall, J-lens", (28,), fitted="J-lens", external_data="published WikiText J-lens", training="Jacobian averaging", about="Rise-and-fall on J-lens scores, peak layer 28")
def rise_and_fall_j(s, peak):
    return _rise_fall(readout(jlens(s["res"][22], 22)), readout(jlens(s["res"][peak], peak)), s["logits"])


@unrestricted("rise-and-fall span", (27,), about="Span of the 32 rise-and-fall tokens' output-head rows, applied to layer 27")
def suppressed_subspace(s, l):  # per prompt: span of the 32 rise-and-fall tokens' unembeddings
    S = _token_span(rise_and_fall(s, l), 32)
    return readout(S @ (S.T @ rms(s["res"][l])))


@unrestricted("rise-and-fall span, J-lens", (28,), fitted="J-lens", external_data="published WikiText J-lens", training="Jacobian averaging", about="As rise-and-fall span, with the J-lens, layer 28")
def suppressed_subspace_j(s, peak):
    S = _token_span(rise_and_fall_j(s, peak), 32)
    return readout(S @ (S.T @ rms(jlens(s["res"][peak], peak))))


@unrestricted("calibrated rise-and-fall", (28,), fitted="calibration text", training="normalisation statistics", about="Rise-and-fall on per-token z-scores of each layer's logits, peak layer 28")
def calibrated_rise_and_fall(s, peak):  # rise-and-fall on per-token z-scores of each layer's logits
    z = lambda l: (readout(s["res"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]
    return _rise_fall(z(22), z(peak), z(32))


@unrestricted("calibrated rise-and-fall, last line", (27,), fitted="calibration text", training="normalisation statistics", about="Calibrated rise-and-fall, max over the tokens of the prompt's last line")
def calibrated_rise_and_fall_line(s, peak):  # max over the tokens of the prompt's last line, not just the last token
    z = lambda l: (readout(s["line"][l]) - bases[f"calib{l}"][0]) / bases[f"calib{l}"][1]   # [tok, vocab]
    early, mid, out = z(22), z(peak), z(32)
    return torch.stack([_rise_fall(e, m, o) for e, m, o in zip(early, mid, out)]).amax(0)


@unrestricted("calibrated rise-and-fall, attention", (28, 1.0), fitted="calibration text", training="normalisation statistics", about="Calibrated rise-and-fall, weighted towards tokens the layer-23 attention output writes")
def calibrated_rise_and_fall_attn(s, peak, temperature):  # favour tokens the layer-23 attention output also writes
    a = readout(s["attn"])
    return calibrated_rise_and_fall(s, peak) * torch.sigmoid((a - a.mean()) / (a.std() * temperature))
