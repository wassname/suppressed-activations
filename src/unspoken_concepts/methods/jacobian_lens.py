"""Jacobian lens methods and related variants. — PI/OpenAI"""
from ..model import DEVICE, load_jlens, readout, rms
from ..calibration import bases
from .registry import unrestricted


J = load_jlens()


_J = {}


def jlens(x, l):
    """Residual l through the Jacobian lens to the final residual."""
    if l not in _J:
        _J[l] = J[l - 1].to(DEVICE).float()
    return x.float() @ _J[l].T


@unrestricted("J-lens", (23,), fitted="J-lens", external_data="published WikiText J-lens", training="Jacobian averaging", about="Jacobian lens (Gurnee et al. 2026) at layer 23")
def j_lens(s, l):
    return readout(jlens(s["res"][l], l))


@unrestricted("J-lens minus output PCA", (28, 256), fitted="J-lens, calibration text", external_data="published WikiText J-lens", training="Jacobian averaging + PCA", about="J-lens at layer 28, minus the top-256 output-layer PCs")
def j_minus_output(s, l, r):
    x, B = rms(jlens(s["res"][l], l)), bases["output"][:, :r]
    return readout(x - B @ (B.T @ x))


@unrestricted("attention output, J-lens", (23,), fitted="J-lens", external_data="published WikiText J-lens", training="Jacobian averaging", about="J-lens of what layer 23's attention adds at the last token")
def attention_output_j(s, l):  # what layer 23's attention adds at the last token
    return readout(jlens(s["attn"], l + 1))
