"""CPU boundary tests for external adapters, including real autograd. — PI/OpenAI"""
import importlib.util
from pathlib import Path
import tempfile
import textwrap
from types import SimpleNamespace
import unittest

import torch

from unspoken_concepts import ROOT

spec = importlib.util.spec_from_file_location("score_unrestricted", ROOT / "scripts/eval/score_unrestricted.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class UnrestrictedInterfaceTest(unittest.TestCase):
    def test_external_adapter_gradients_and_prompt_only(self):
        source = '''
        import torch
        METADATA = {key: "test" for key in (
            "name", "author", "data", "external_data", "training", "extras", "code", "revision", "settings", "overlap")}
        METADATA["output"] = "vector"
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
                vector = runner.predict(entry, model, None, "test question", state, 4, 8)
                self.assertFalse(torch.is_grad_enabled())
            torch.testing.assert_close(vector, model.weight[0])
            self.assertFalse(vector.requires_grad)

    def test_explicit_token_scores_bypass_output_head(self):
        entry = SimpleNamespace(METADATA={"name": "scores", "output": "scores"},
                                method=lambda *args: torch.arange(8).float())
        output = runner.predict(entry, None, None, "question", {}, 4, 8)
        def forbidden_readout(*args):
            self.fail("token scores must not be unembedded again")
        torch.testing.assert_close(runner.to_scores(entry, output, forbidden_readout), torch.arange(8).float())

    def test_rejects_wrong_shape_and_nonfinite_outputs(self):
        for mode, size in (("vector", 4), ("scores", 8)):
            for invalid in (torch.zeros(7), torch.full((size,), float("nan")), torch.zeros(size, dtype=torch.long)):
                entry = SimpleNamespace(METADATA={"output": mode}, method=lambda *args: invalid)
                with self.subTest(mode=mode, shape=invalid.shape, dtype=invalid.dtype):
                    with self.assertRaises(AssertionError):
                        runner.predict(entry, None, None, "question", {}, 4, 8)

    def test_requires_resource_disclosures(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "entry.py"
            path.write_text("METADATA = {'name': 'incomplete'}\n")
            with self.assertRaisesRegex(AssertionError, "METADATA missing author"):
                runner.load_adapter(path)


if __name__ == "__main__":
    unittest.main()
