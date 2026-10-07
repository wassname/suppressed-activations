"""Controls methods and related variants. — PI/OpenAI"""
from .helpers import last, project
from .registry import geometry


@geometry("mean over layers", about="Logit lens of the last token, averaged over layers 16-32 (control)")
def mean_lens(hs, embeddings, state):
    return last(hs).mean(0)


@geometry("random subspace", (1024,), fitted="random seed", about="Mean over layers, projected on a random rank-1024 subspace (control)")
def random_subspace(hs, embeddings, state, r):
    return project(state["random"][:, :r], last(hs).mean(0))


@geometry("mean calibration text", fitted="calibration text", about="Ignores the prompt: the mean layer-28 activation on calibration text (control)")
def fixed_list(hs, embeddings, state):
    return state["mean28"]
