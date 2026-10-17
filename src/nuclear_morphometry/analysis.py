"""Fixed-field contrasts and measurement-level deletion explanations."""

import math
from collections.abc import Sequence

import numpy as np

from .domain import Mask, objects
from .evaluation import evaluate


def paired_change(all_contrast: Sequence[float], survivor: Sequence[float]) -> dict[str, float]:
    """Use one orientation a-b on the same field roster; no bootstrap is implied."""
    a, b = np.asarray(all_contrast, float), np.asarray(survivor, float)
    if a.ndim != 1 or a.shape != b.shape or not len(a) or not np.isfinite([a, b]).all():
        raise ValueError("Paired contrasts must be nonempty finite vectors of equal length")
    return {
        "mean_all_contrast": float(a.mean()),
        "mean_survivor_contrast": float(b.mean()),
        "mean_change": float((b - a).mean()),
    }


def sign_discordance(
    all_contrast: Sequence[float], survivor: Sequence[float], margin: float = 0
) -> dict[str, int]:
    """Retain original and strict-both-margins denominators and exact ties."""
    paired_change(all_contrast, survivor)
    if not math.isfinite(margin) or margin < 0:
        raise ValueError("The descriptive absolute margin must be finite and nonnegative")
    a, b = np.asarray(all_contrast, float), np.asarray(survivor, float)
    qualified = (np.abs(a) > margin) & (np.abs(b) > margin)
    return {
        "common_count": len(a),
        "qualified_count": int(qualified.sum()),
        "opposite_count": int(((np.signbit(a) != np.signbit(b)) & qualified).sum()),
        "exact_ties": int(((a == 0) | (b == 0)).sum()),
    }


def cdf_selection_shift(
    values: Sequence[float], selected: Sequence[bool], threshold: float
) -> float:
    """Cov(s, 1{f<=t})/r equals the retained-minus-full empirical CDF."""
    a, s = np.asarray(values, float), np.asarray(selected)
    if (
        a.ndim != 1
        or a.shape != s.shape
        or not len(a)
        or s.dtype.kind != "b"
        or not s.any()
        or not np.isfinite(a).all()
        or not math.isfinite(threshold)
    ):
        raise ValueError("Finite features and a nonempty boolean selection are required")
    indicator = a <= threshold
    fraction = float(s.mean())
    return float(np.mean(s * indicator) - fraction * indicator.mean()) / fraction


def explain_deletions(reference: Mask, ids: Sequence[int], min_area: int = 16) -> dict[str, object]:
    """Recompute the actual joint measurement change, not a neural attribution."""
    profile = objects(reference, min_area)
    if len(set(ids)) != len(ids) or any(type(x) is not int for x in ids):
        raise ValueError("Removed IDs must be distinct native integers")
    if not set(ids).issubset(set(profile.ids.tolist())):
        raise ValueError("Every removed ID must be eligible in the reference mask")
    prediction = np.where(np.isin(reference, ids), 0, reference)
    return {
        "interpretation": "Exact joint object deletion; not neural, Shapley or clinical XAI",
        "removed_ids": list(ids),
        "omitted_area_pixels_squared": int(profile.area[np.isin(profile.ids, ids)].sum()),
        "measurements": evaluate(reference, prediction, min_area),
    }
