# Written by PI/gpt-5.4 for Michael J. Clark.

import json
from pathlib import Path

import torch

from scripts.spider_ant_demo import (
    coordinate_swap,
    coordinate_swap_leg,
    sample_component_hook,
)
from scripts.demo import intervention_hooks
from suppressed_activation_subspace import (
    component,
    match_norm,
    matched_random_rotation,
    random_basis_like,
    remove,
    replace,
    steer,
    subspace_from_scores,
)


def main() -> None:
    generator = torch.Generator().manual_seed(1)
    source_basis = torch.linalg.qr(torch.randn(3, 11, 4, generator=generator), mode="reduced").Q
    target_basis = torch.linalg.qr(torch.randn(3, 11, 4, generator=generator), mode="reduced").Q
    source_rotation = torch.linalg.qr(torch.randn(3, 4, 4, generator=generator), mode="reduced").Q
    target_rotation = torch.linalg.qr(torch.randn(3, 4, 4, generator=generator), mode="reduced").Q
    source_h = torch.randn(3, 11, generator=generator)
    target_h = torch.randn(3, 11, generator=generator)

    torch.testing.assert_close(
        component(source_h, source_basis),
        component(source_h, source_basis @ source_rotation),
    )
    torch.testing.assert_close(
        remove(source_h, source_basis, restore_norm=True),
        remove(source_h, source_basis @ source_rotation, restore_norm=True),
    )
    torch.testing.assert_close(
        steer(source_h, source_basis, 0.5, restore_norm=True),
        steer(source_h, source_basis @ source_rotation, 0.5, restore_norm=True),
    )
    torch.testing.assert_close(
        component(remove(source_h, source_basis), source_basis),
        torch.zeros_like(source_h),
        atol=2e-6,
        rtol=2e-6,
    )
    torch.testing.assert_close(remove(source_h, source_basis, restore_norm=True).norm(dim=-1), source_h.norm(dim=-1))
    replaced = replace(source_h, source_basis, target_h, target_basis, restore_norm=True)
    torch.testing.assert_close(replaced.norm(dim=-1), source_h.norm(dim=-1))
    torch.testing.assert_close(
        replaced,
        replace(
            source_h,
            source_basis @ source_rotation,
            target_h,
            target_basis @ target_rotation,
            restore_norm=True,
        ),
    )
    torch.testing.assert_close(steer(source_h, source_basis, -1), remove(source_h, source_basis))

    random_basis = random_basis_like(source_basis, seed=0)
    torch.testing.assert_close(
        random_basis.transpose(-2, -1) @ random_basis,
        torch.eye(4).expand(3, -1, -1),
        atol=2e-6,
        rtol=2e-6,
    )
    distance = torch.full((3, 1), 0.5)
    rotated = matched_random_rotation(source_h, component(source_h, random_basis), distance)
    torch.testing.assert_close(rotated.norm(dim=-1), source_h.norm(dim=-1))
    torch.testing.assert_close((rotated - source_h).norm(dim=-1), distance.squeeze(-1))

    realistic_h = match_norm(torch.randn(3, 1, 2560, generator=generator), torch.full((3, 1, 2560), 34 / 2560**0.5))
    realistic_distance = torch.tensor([[[1.2]], [[3.0]], [[6.0]]])
    realistic_rotated = matched_random_rotation(
        realistic_h, torch.randn(3, 1, 2560, generator=generator), realistic_distance
    )
    torch.testing.assert_close(realistic_rotated.norm(dim=-1), realistic_h.norm(dim=-1), atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(
        (realistic_rotated - realistic_h).norm(dim=-1),
        realistic_distance.squeeze(-1),
        atol=1e-4,
        rtol=1e-4,
    )
    print("PASS: projection operators are basis-invariant and preserve requested norms")

    h = torch.randn(1, 3, 5, generator=generator)
    directions = torch.linalg.qr(torch.randn(5, 2, generator=generator)).Q[None]
    mask = torch.tensor([False, False, True])
    swapped = coordinate_swap(h, directions, 1.0, mask, restore_norm=False)
    source = coordinate_swap_leg(h, directions, "source", mask, restore_norm=False)
    target = coordinate_swap_leg(h, directions, "target", mask, restore_norm=False)
    torch.testing.assert_close(swapped - h, (source - h) + (target - h))
    print("PASS: source and target components sum to the C=1 coordinate delta")

    sample_mask = torch.tensor([False, False, True])
    sample_hook = sample_component_hook(
        directions[0], directions[0], h[0, -1], 1.0, sample_mask
    )
    sample_patched = sample_hook(None, None, h)
    torch.testing.assert_close(sample_patched[:, :-1], h[:, :-1])
    print("PASS: sample-component hook accepts a boolean position mask")

    suffix_source_basis = torch.linalg.qr(torch.randn(5, 2, generator=generator)).Q
    suffix_target_basis = torch.linalg.qr(torch.randn(5, 2, generator=generator)).Q
    suffix_target_residuals = torch.randn(2, 5, 5, generator=generator)
    suffix_hidden = torch.randn(1, 5, 5, generator=generator)
    suffix_hook = intervention_hooks(
        suffix_source_basis,
        suffix_target_basis,
        suffix_target_residuals,
        operation="replace",
        blocks_to_hook=[0],
        positions=2,
    )[0]
    suffix_patched = suffix_hook(None, None, suffix_hidden)
    torch.testing.assert_close(suffix_patched[:, :-2], suffix_hidden[:, :-2])
    assert not torch.equal(suffix_patched[:, -2:], suffix_hidden[:, -2:])
    print("PASS: suffix intervention changes only the requested prompt positions")

    fixed_target_hook = intervention_hooks(
        suffix_source_basis,
        suffix_target_basis,
        suffix_target_residuals,
        operation="replace",
        blocks_to_hook=[0],
        positions=2,
        source_position=3,
        target_position=1,
    )[0]
    fixed_target_patched = fixed_target_hook(None, None, suffix_hidden)
    torch.testing.assert_close(fixed_target_patched[:, :2], suffix_hidden[:, :2])
    torch.testing.assert_close(fixed_target_patched[:, 4:], suffix_hidden[:, 4:])
    assert not torch.equal(fixed_target_patched[:, 2:4], suffix_hidden[:, 2:4])
    print("PASS: persistent intervention uses explicit source and donor content positions")

    scores = torch.tensor([[0.0, 4.0, 2.0, 3.0, 1.0]])
    toy_unembedding = torch.randn(5, 5, generator=generator)
    _, selected = subspace_from_scores(scores, toy_unembedding, torch.ones(5), rank=2)
    assert selected.tolist() == [[1, 3]]
    print("PASS: subspace construction selects the highest supplied persistent scores")

    data = json.loads((Path(__file__).resolve().parents[1] / "data/causal_demo.json").read_text())
    rows = {row["condition"]: row["metrics"] for row in data["interventions"]}
    positive_conditions = ("replace_C=+0.125", "replace_C=+0.25", "replace_C=+0.5", "replace_C=+1")
    log_odds = [rows[condition]["log_odds_target_vs_source"] for condition in positive_conditions]
    assert all(left < right for left, right in zip(log_odds, log_odds[1:]))
    generations = {row["condition"]: row for row in data["dose_generations"]}
    assert all(len(generations[condition]["token_ids"]) == 64 for condition in positive_conditions)
    print(f"PASS: positive replacement doses increase target log odds: {log_odds}")


if __name__ == "__main__":
    main()
