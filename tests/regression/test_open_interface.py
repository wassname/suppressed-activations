"""CPU boundary tests for external adapters, including real autograd. — PI/OpenAI"""
import importlib.util
from pathlib import Path
import tempfile
import textwrap
from types import SimpleNamespace
import unittest

import torch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("score_open", ROOT / "scripts/challenge/score_open.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class OpenInterfaceTest(unittest.TestCase):
    def test_external_adapter_gradients_and_prompt_only(self):
        source = '''
        import torch
        METADATA = {key: "test" for key in (
            "name", "author", "data", "access", "supervision", "code", "revision", "settings", "overlap")}
        def calibrate(model, tokenizer, texts):
            assert torch.is_grad_enabled()
            texts = list(texts)
            assert all(isinstance(t, str) for t in texts)
            return {"count": len(texts)}
        def method(model, tokenizer, prompt, state):
            assert isinstance(prompt, str) and state == {"count": 2}
            x = torch.ones(4, requires_grad=True)
            return torch.autograd.grad(model(x).sum(), x)[0]
        '''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "external adapter.py"
            path.write_text(textwrap.dedent(source))
            entry = runner.load_adapter(path)
            model = torch.nn.Linear(4, 1, bias=False)
            with torch.no_grad():
                state = runner.calibrate_entry(entry, model, None, iter(["first", "second"]))
                vector = runner.predict(entry, model, None, "test question", state, 4)
                self.assertFalse(torch.is_grad_enabled())
            torch.testing.assert_close(vector, model.weight[0])
            self.assertFalse(vector.requires_grad)

    def test_rejects_vocab_scores_and_nonfinite_outputs(self):
        for invalid in (torch.zeros(8), torch.full((4,), float("nan")), torch.zeros(4, dtype=torch.long)):
            entry = SimpleNamespace(method=lambda *args: invalid)
            with self.subTest(shape=invalid.shape, dtype=invalid.dtype):
                with self.assertRaises(AssertionError):
                    runner.predict(entry, None, None, "question", {}, 4)

    def test_requires_resource_disclosures(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "entry.py"
            path.write_text("METADATA = {'name': 'incomplete'}\n")
            with self.assertRaisesRegex(AssertionError, "METADATA missing author"):
                runner.load_adapter(path)


if __name__ == "__main__":
    unittest.main()
