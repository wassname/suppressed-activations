"""Run scripts/challenge/notebook.py on the CPU (the GPU queue is busy with another agent's training). — PI/OpenAI"""
import runpy, sys
import torch
torch.nn.Module.cuda = lambda self, *a, **k: self
torch.Tensor.cuda = lambda self, *a, **k: self
sys.path.insert(0, "scripts/challenge")
sys.argv = ["notebook.py"]
runpy.run_path("scripts/challenge/notebook.py", run_name="__main__")
