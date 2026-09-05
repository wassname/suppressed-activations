# Written by PI/gpt-5.4 for Michael J. Clark.

import json
from pathlib import Path

import torch

from suppressed_activation_subspace import (
    component,
    match_norm,
    matched_random_rotation,
    random_basis_like,
    remove,
    replace,
    steer,
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

    data = json.loads((Path(__file__).resolve().parents[1] / "data/causal_demo.json").read_text())
    rows = {row["condition"]: row["metrics"] for row in data["interventions"]}
    positive_conditions = ("replace_C=+0.125", "replace_C=+0.25", "replace_C=+0.5", "replace_C=+1")
    log_odds = [rows[condition]["log_odds_target_vs_source"] for condition in positive_conditions]
    assert all(left < right for left, right in zip(log_odds, log_odds[1:]))
    generations = {row["condition"]: row for row in data["dose_generations"]}
    assert all(len(generations[condition]["token_ids"]) == 64 for condition in positive_conditions)
    assert all("<think>" not in generations[condition]["text"] for condition in positive_conditions)
    print(f"PASS: positive replacement doses increase target log odds: {log_odds}")


if __name__ == "__main__":
    main()
