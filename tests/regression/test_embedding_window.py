"""Embedding-window checks through the production tensor code, on CPU. — PI/OpenAI"""
import unittest

import torch

from unspoken_concepts.methods.embedding_window import embedding_window, pooled
from unspoken_concepts.tensors import rms


class EmbeddingWindowTest(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        self.hs = torch.randn(17, 12, 32)
        self.embeddings = torch.randn(12, 32)

    def evaluate(self, hs=None, embeddings=None):
        return embedding_window(self.hs if hs is None else hs,
                                self.embeddings if embeddings is None else embeddings,
                                {}, 8, False, True)

    def test_uses_embeddings_not_layer16(self):
        changed = self.hs.clone()
        changed[0] = torch.randn_like(changed[0]) * 9
        torch.testing.assert_close(self.evaluate(changed), self.evaluate())
        self.assertGreater((self.evaluate(embeddings=torch.randn_like(self.embeddings)) - self.evaluate()).norm(), 0.01)

    def test_raw_average_precedes_normalisation(self):
        h = torch.tensor([[100., 0.], [0., 1.]])
        torch.testing.assert_close(pooled(h, 2, False), rms(h.mean(0)))
        self.assertGreater((pooled(h, 2, False) - pooled(h, 2, True)).norm(), 0.5)

    def test_matches_projection_and_averages_intermediate_positions(self):
        x = rms(self.hs[1:-1, -8:].mean(1))
        directions = torch.stack([self.embeddings[-8:].mean(0), self.hs[-1, -8:].mean(0)], 1)
        expected = (x - x @ directions @ torch.linalg.pinv(directions)).mean(0)
        torch.testing.assert_close(self.evaluate(), expected)
        changed = self.hs.clone()
        changed[5, -3] *= -10
        self.assertGreater((self.evaluate(changed) - self.evaluate()).norm(), 0.01)

    def test_window_invariance_and_rank_deficiency(self):
        order = torch.randperm(8)
        hs, embeddings = self.hs.clone(), self.embeddings.clone()
        hs[:, -8:] = hs[:, -8:][:, order]
        embeddings[-8:] = embeddings[-8:][order]
        hs[:, :-8] += 20
        embeddings[:-8] -= 20
        torch.testing.assert_close(self.evaluate(hs, embeddings), self.evaluate())
        hs = torch.zeros(17, 3, 4)
        embeddings = torch.zeros(3, 4)
        hs[-1, :, 0] = 1
        embeddings[:, 0] = 1
        hs[1:-1, :, 1] = 1
        result = embedding_window(hs, embeddings, {}, 8, False, True)
        torch.testing.assert_close(result, rms(torch.tensor([0., 1., 0., 0.])))

    def test_zero_endpoints_short_window_and_last_token_control(self):
        hs = self.hs[:, :3].clone()
        embeddings = torch.zeros_like(self.embeddings[:3])
        hs[-1] = 0
        expected = rms(hs[1:-1].mean(1)).mean(0)
        torch.testing.assert_close(embedding_window(hs, embeddings, {}, 8, False, True), expected)
        torch.testing.assert_close(embedding_window(hs, embeddings, {}, 3, False, True), expected)
        expected_last = rms(hs[1:-1, -1]).mean(0)
        torch.testing.assert_close(embedding_window(hs, embeddings, {}, 8, False, False), expected_last)


if __name__ == "__main__":
    unittest.main()
