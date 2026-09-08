# Written by PI/gpt-5.4 for Michael J. Clark.

import json
from pathlib import Path

import torch

from scripts.spider_ant_demo import (
    coordinate_swap,
    coordinate_swap_leg,
    sample_component_hook,
)
from scripts.demo import intervention_hooks, layer_hooks
from scripts.prompt import first_answer
from suppressed_activation_subspace import (
    component,
    cross_position_covariance,
    match_norm,
    matched_random_rotation,
    random_basis_like,
    remove,
    replace,
    steer,
    subspace_from_scores,
    persistent_suppressed_activation_subspace,
    token_persistent_subspace,
    suppressed_activation_scores,
)


def main() -> None:
    # Unit source directions preserve linear-map vocabulary ranking. -- Codex/GPT-6
    states = torch.tensor([[2., -3.], [1., 4.], [-2., 1.]])
    linear_map = torch.tensor([[1., 2., 0.], [-1., 0., 3.], [0., 2., 1.]])
    vocabulary = torch.tensor([[1., 0., 2.], [-1., 2., 1.], [3.1, 1., -1.]])
    norms = states.norm(dim=0)
    direction_actions = linear_map @ (states / norms)
    direct_scores = vocabulary @ linear_map @ states
    unit_scores = vocabulary @ direction_actions
    torch.testing.assert_close(unit_scores * norms, direct_scores)
    assert torch.equal(unit_scores.argsort(dim=0), direct_scores.argsort(dim=0))
    print("PASS: normalized full-residual J actions preserve vocabulary ranks and recover scores by source norm")
    # Equal diagonal energy can hide alternating token signs. -- Codex/GPT-6
    persistent = torch.tensor([[[1., 0.], [1., 0.], [1., 0.]]])
    alternating = persistent * torch.tensor([1., -1., 1.])[None, :, None]
    final = torch.zeros_like(persistent)
    steady_energy = cross_position_covariance(persistent) - cross_position_covariance(final)
    alternating_energy = cross_position_covariance(alternating) - cross_position_covariance(final)
    torch.testing.assert_close(steady_energy, torch.diag(torch.tensor([1., 0.])))
    torch.testing.assert_close(alternating_energy, torch.diag(torch.tensor([-1./3., 0.])))
    explicit = torch.stack([torch.outer(alternating[0, t], alternating[0, u])
                            for t in range(3) for u in range(3) if t != u]).mean(0)
    torch.testing.assert_close(alternating_energy, explicit)
    print("PASS: temporal attenuation retains same-sign contrast and rejects alternating signs at equal diagonal energy")
    # Repeating identical token projectors must not create extra directions. -- Codex/GPT-6
    rng = torch.Generator().manual_seed(72)
    repeated_states = torch.randn(1, 3, 12, generator=rng).expand(4, -1, -1)
    vocabulary = torch.randn(16, 12, generator=rng)
    support, spectrum, candidates = token_persistent_subspace(
        repeated_states, vocabulary, torch.ones(12), persistent_rank=8,
        early_layer=0, peak_layer=1, output_layer=2, rank=2,
    )
    selected_basis, _ = subspace_from_scores(
        suppressed_activation_scores(repeated_states[:1], vocabulary, torch.ones(12),
                                     early_layer=0, peak_layer=1, output_layer=2),
        vocabulary, torch.ones(12), rank=2,
    )
    assert support.shape == (12, 2) and spectrum.shape == (8,)
    assert torch.equal(candidates, candidates[:1].expand_as(candidates))
    torch.testing.assert_close(support @ support.T, selected_basis[0] @ selected_basis[0].T,
                               atol=1e-6, rtol=1e-5)
    print("PASS: full persistent support excludes numerical-null directions from repeated candidates")
    # A rising output is not suppression, even when the middle layer rises. -- Codex/GPT-6
    angles = torch.tensor([0.1, 0.4, 0.8])
    rising_states = torch.stack((angles.sin(), angles.cos()), dim=-1)[None]
    symmetric_rows = torch.tensor([[1., 0.], [-1., 0.]])
    for normalize in (False, True):
        rising_scores = suppressed_activation_scores(
            rising_states, symmetric_rows, torch.ones(2),
            early_layer=0, peak_layer=1, output_layer=2,
            normalize_unembedding_rows=normalize,
        )
        assert rising_scores[0, 0] == 0
        peaked_scores = suppressed_activation_scores(
            rising_states[:, [0, 2, 1]], symmetric_rows, torch.ones(2),
            early_layer=0, peak_layer=1, output_layer=2,
            normalize_unembedding_rows=normalize,
        )
        assert peaked_scores[0, 0] > 0
    print("PASS: suppression requires both a rise and a fall in raw and normalized scoring")
    assert first_answer(" **No**. Later: Yes", ("Yes", "No")) == "No"
    assert first_answer("1. Later: Yes", ("Yes", "No")) is None
    assert first_answer("Nobody", ("No", "Yes")) is None
    assert first_answer("16.", ("6", "8")) is None
    assert first_answer(" **ant**.", (" spider", " ant")) == " ant"
    assert first_answer("8. Correction: 6", ("6", "8")) == "8"
    generator = torch.Generator().manual_seed(1)
    shared = torch.linalg.qr(torch.randn(11, 4, generator=generator)).Q
    donor = torch.randn(2, 5, 11, generator=generator)
    source = torch.randn(1, 5, 11, generator=generator)
    for strength in (0.0, 0.5, 1.0, 2.0):
        replacement_record = {}
        hook = intervention_hooks(
            shared, shared, donor, operation="shared_replace", strength=strength,
            blocks_to_hook=[0], positions=3, source_position=4, target_position=4,
            match_component_norm=False, restore_norm=False,
            record=replacement_record,
        )[0]
        edited = hook(None, None, source)
        torch.testing.assert_close(edited[:, -3:] @ shared,
                                   (1-strength)*(source[:, -3:] @ shared)
                                   + strength*(donor[1, -3:].unsqueeze(0) @ shared))
        if strength == 0:
            torch.testing.assert_close(edited, source, rtol=0, atol=0)
        elif strength == 1:
            torch.testing.assert_close(edited[:, -3:] @ shared, donor[1, -3:].unsqueeze(0) @ shared)
            torch.testing.assert_close(edited[:, :2], source[:, :2])
            delta = edited - source
            torch.testing.assert_close(delta, (delta @ shared) @ shared.T, atol=1e-6, rtol=1e-5)
            torch.testing.assert_close(hook(None, None, edited), edited)
            decoded = hook(None, None, source[:, -1:])
            torch.testing.assert_close(decoded @ shared, donor[1, -1:].unsqueeze(0) @ shared)
        low_precision = source.to(torch.bfloat16)
        low_edited = hook(None, None, low_precision)
        expected = low_precision[:, -3:].float()
        expected = expected + strength * ((donor[1, -3:].unsqueeze(0) - expected) @ shared) @ shared.T
        torch.testing.assert_close(low_edited[:, -3:], expected.to(torch.bfloat16), rtol=0, atol=0)
        saved_coordinates = torch.tensor(replacement_record[1]["replacement_trace"][-1]["after_model_dtype"])
        torch.testing.assert_close(saved_coordinates, (low_edited[:, -3:].float() @ shared)[0])
    print("PASS: shared replacement aligns donor tokens, reaches coordinates, preserves complement and covers decode")
    block = torch.nn.Identity()
    captured = []
    capture_handle = block.register_forward_hook(lambda _m, _i, output: captured.append(output))
    with layer_hooks([block], {0: lambda _m, _i, output: output + 1}):
        edited = block(torch.zeros(1, 1, 3))
    torch.testing.assert_close(captured[0], edited)
    capture_handle.remove()
    print("PASS: intervention runs before an existing hidden-state capture hook")
    # Verify nonorthogonal coordinate exchange through the production hook. -- Codex
    directions = torch.randn(11, 2, generator=generator)
    directions /= directions.norm(dim=0)
    hidden = torch.randn(1, 5, 11, generator=generator)
    swap_hook = intervention_hooks(
        directions[None], directions[None], torch.zeros(2, 5, 11),
        operation="coordinate_swap", coordinate_directions=directions,
        blocks_to_hook=[0], positions=3, restore_norm=False,
    )[0]
    swapped = swap_hook(None, None, hidden)
    torch.testing.assert_close(swapped[:, :2], hidden[:, :2])
    dual = torch.linalg.pinv(directions).T
    torch.testing.assert_close((swapped @ dual)[:, -3:], (hidden @ dual)[:, -3:].flip(-1))
    orthogonal = torch.eye(11) - directions @ torch.linalg.pinv(directions)
    torch.testing.assert_close(swapped @ orthogonal, hidden @ orthogonal, atol=1e-6, rtol=1e-5)
    torch.testing.assert_close(swap_hook(None, None, swapped), hidden, atol=1e-6, rtol=1e-5)
    torch.testing.assert_close(swapped.norm(dim=-1), hidden.norm(dim=-1))
    torch.testing.assert_close(swap_hook(None, None, hidden[:, -1:]) @ dual, (hidden[:, -1:] @ dual).flip(-1))
    print("PASS: coordinate swap exchanges nonorthogonal coordinates, preserves complement, covers decode")
    source_only_hook = intervention_hooks(
        directions[None], directions[None], torch.zeros(2, 5, 11),
        operation="coordinate_swap", coordinate_directions=directions,
        source_dominant_only=True, blocks_to_hook=[0], positions=3, restore_norm=False,
    )[0]
    source_only = source_only_hook(None, None, hidden)
    source_only_coords = (source_only @ dual)[:, -3:]
    assert torch.all(source_only_coords[..., 1] >= source_only_coords[..., 0] - 1e-6)
    torch.testing.assert_close(source_only_hook(None, None, source_only), source_only, atol=1e-6, rtol=1e-5)
    print("PASS: source-dominant swap reaches target side and a second edit leaves it there")
    clamp_direction = directions[:, 0]
    clamp_hook = intervention_hooks(
        directions[None], directions[None], torch.zeros(2, 5, 11),
        operation="coordinate_clamp", fixed_deltas={1: clamp_direction},
        target_coordinates={1: torch.tensor(0.5)},
        blocks_to_hook=[0], positions=3, restore_norm=False,
    )[0]
    clamped = clamp_hook(None, None, hidden)
    torch.testing.assert_close(clamped[:, :2], hidden[:, :2])
    torch.testing.assert_close((clamped @ clamp_direction)[:, -3:],
                               (hidden @ clamp_direction)[:, -3:].clamp_min(0.5))
    clamp_orthogonal = torch.eye(11) - torch.outer(clamp_direction, clamp_direction)
    torch.testing.assert_close(clamped @ clamp_orthogonal, hidden @ clamp_orthogonal)
    torch.testing.assert_close(clamp_hook(None, None, clamped), clamped)
    torch.testing.assert_close(clamp_hook(None, None, hidden[:, -1:]), clamped[:, -1:])
    print("PASS: template clamp reaches coordinate threshold, preserves complement and covers decode")
    residuals = torch.randn(1, 3, 11, generator=generator).expand(4, -1, -1)
    unembedding = torch.randn(30, 11, generator=generator)
    basis, persistence, _ = token_persistent_subspace(
        residuals, unembedding, torch.ones(11), persistent_rank=3,
        early_layer=0, peak_layer=1, output_layer=2, rank=3,
    )
    torch.testing.assert_close(persistence[:3], torch.ones(3))
    torch.testing.assert_close(basis.T @ basis, torch.eye(3), atol=1e-6, rtol=1e-6)
    print("PASS: identical token spaces have unit SVD persistence")
    rescaled_unembedding = unembedding * torch.linspace(0.3, 4.0, unembedding.shape[0])[:, None]
    normalized_bases = [token_persistent_subspace(
        residuals, matrix, torch.ones(11), persistent_rank=3,
        early_layer=0, peak_layer=1, output_layer=2, rank=3,
        normalize_unembedding_rows=True,
    )[0] for matrix in (unembedding, rescaled_unembedding)]
    torch.testing.assert_close(normalized_bases[0] @ normalized_bases[0].T,
                               normalized_bases[1] @ normalized_bases[1].T, atol=2e-6, rtol=1e-5)
    counterexample_basis, _ = subspace_from_scores(
        torch.tensor([[1., 0.]]), torch.tensor([[2., 0.], [0., 1.]]), torch.ones(2),
        rank=1, normalize_unembedding_rows=True,
    )
    torch.testing.assert_close(component(torch.tensor([[1., 2.]]), counterexample_basis),
                               torch.tensor([[-.5, .5]]))
    print("PASS: normalized detector spans resist row scaling and match scored directions")
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

    delta = component(torch.randn(5, generator=generator), suffix_source_basis)
    fixed_hook = intervention_hooks(
        suffix_source_basis, suffix_target_basis, suffix_target_residuals,
        operation="fixed_delta", fixed_deltas={1: delta}, strength=2.0,
        blocks_to_hook=[0], positions=2, restore_norm=False,
    )[0]
    fixed_patched = fixed_hook(None, None, suffix_hidden)
    torch.testing.assert_close(fixed_patched[:, :-2], suffix_hidden[:, :-2])
    torch.testing.assert_close(
        fixed_patched[:, -2:] - suffix_hidden[:, -2:],
        (2 * delta).expand(1, 2, -1),
    )
    torch.testing.assert_close(remove(fixed_patched, suffix_source_basis),
                               remove(suffix_hidden, suffix_source_basis), atol=2e-6, rtol=2e-6)
    print("PASS: fixed displacement is identical across patched tokens and preserves orthogonal content")

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

    decode_hidden = suffix_hidden[:, :1]
    decode_patched = fixed_target_hook(None, None, decode_hidden)
    assert decode_patched.shape == decode_hidden.shape
    assert not torch.equal(decode_patched, decode_hidden)
    print("PASS: persistent intervention patches one cached decode token")

    scores = torch.tensor([[0.0, 4.0, 2.0, 3.0, 1.0]])
    toy_unembedding = torch.randn(5, 5, generator=generator)
    _, selected = subspace_from_scores(scores, toy_unembedding, torch.ones(5), rank=2)
    assert selected.tolist() == [[1, 3]]
    print("PASS: subspace construction selects the highest supplied persistent scores")

    residuals_by_position = torch.randn(4, 3, 5, generator=generator)
    basis, selected, scores_by_position = persistent_suppressed_activation_subspace(
        residuals_by_position,
        toy_unembedding,
        torch.ones(5),
        early_layer=0,
        peak_layer=1,
        output_layer=2,
        rank=2,
    )
    assert basis.shape == (1, 5, 2)
    assert selected.shape == (1, 2)
    assert scores_by_position.shape == (4, 5)
    print("PASS: persistent selector aggregates sparse evidence without a hard minimum")

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
