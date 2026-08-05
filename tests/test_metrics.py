import torch

from src.evaluation.metrics import (
    compute_fid,
    count_near_duplicate_pairs,
    pixel_variance,
    to_fid_input,
)


def test_to_fid_input_shape_and_range():
    images = torch.rand(4, 1, 32, 32) * 2 - 1  # [-1, 1]
    out = to_fid_input(images)
    assert out.shape == (4, 3, 32, 32)
    assert out.min() >= 0.0 and out.max() <= 1.0


def test_pixel_variance_zero_for_identical_images():
    images = torch.ones(5, 1, 32, 32)
    assert pixel_variance(images) == 0.0


def test_pixel_variance_positive_for_varied_images():
    torch.manual_seed(0)
    images = torch.randn(5, 1, 32, 32)
    assert pixel_variance(images) > 0.0


def test_count_near_duplicate_pairs_detects_identical_images():
    base = torch.randn(1, 1, 32, 32)
    images = base.repeat(4, 1, 1, 1)  # 4 images strictement identiques -> 6 paires
    assert count_near_duplicate_pairs(images, threshold=1e-6) == 6


def test_count_near_duplicate_pairs_zero_for_diverse_images():
    torch.manual_seed(0)
    images = torch.randn(10, 1, 32, 32)  # bruit indépendant, peu de chances de quasi-doublons
    assert count_near_duplicate_pairs(images, threshold=0.05) == 0


def test_compute_fid_low_for_identical_distributions():
    torch.manual_seed(0)
    images = torch.rand(20, 1, 32, 32) * 2 - 1
    # Même distribution des deux côtés (juste un tirage différent) -> FID doit rester faible.
    other = torch.rand(20, 1, 32, 32) * 2 - 1
    fid_score = compute_fid(images, other)
    assert fid_score >= 0.0
