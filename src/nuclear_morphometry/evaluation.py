"""Established segmentation scores and explicit all/survivor populations."""

import math

import numpy as np
from numpy.typing import ArrayLike
from scipy.stats import wasserstein_distance

from .domain import Mask, eligible_map, objects, strict_matches, validate_mask

Number = float | int | None


def w1(a: ArrayLike, b: ArrayLike) -> float | None:
    """Unscaled scalar W1; an empty measurement is undefined, never zero."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Feature distributions must contain only finite values")
    return float(wasserstein_distance(a, b)) if len(a) and len(b) else None


def omission_scores(n: int, k: int, total_area: int, omitted_area: int) -> dict[str, Number]:
    """Exact whole-object deletion controls; this is not a general mask metric."""
    if any(type(x) is not int for x in [n, k, total_area, omitted_area]):
        raise ValueError("Deletion counts and pixel areas must be integers")
    if not (n > 0 and 0 <= k < n and total_area > 0 and 0 <= omitted_area < total_area):
        raise ValueError("Deletion controls require n>0, 0<=k<n and 0<=U<A")
    if (k == 0) != (omitted_area == 0):
        raise ValueError("Zero omitted objects and zero omitted area must agree")
    if total_area < n or omitted_area < k or total_area - omitted_area < n - k:
        raise ValueError("Every omitted and retained object must occupy at least one pixel")
    retained = n - k
    return {
        "pq": 2 * retained / (2 * n - k),
        "instance_f1": 2 * retained / (2 * n - k),
        "foreground_dice": 2 * (total_area - omitted_area) / (2 * total_area - omitted_area),
        "foreground_iou": (total_area - omitted_area) / total_area,
        "count_absolute_error": k,
    }


def evaluate(reference: Mask, prediction: Mask, min_area: int = 16) -> dict[str, Number]:
    """Evaluate one field on native eligible objects (pixel area >= min_area)."""
    reference, prediction = validate_mask(reference), validate_mask(prediction)
    if reference.shape != prediction.shape:
        raise ValueError("Reference and prediction masks must have the same shape")
    truth, predicted = objects(reference, min_area), objects(prediction, min_area)
    gi, pi, iou = strict_matches(reference, prediction, truth, predicted)
    n, p, matches = len(truth.ids), len(predicted.ids), len(gi)
    g = eligible_map(reference, truth.ids) > 0
    r = eligible_map(prediction, predicted.ids) > 0
    intersection, union = int((g & r).sum()), int((g | r).sum())
    combined_area = int(g.sum() + r.sum())
    median_area = float(np.median(truth.area)) if n else None
    area_error = w1(truth.area, predicted.area)
    result: dict[str, Number] = {
        "reference_count": n,
        "prediction_count": p,
        "matched_count": matches,
        "count_absolute_error": abs(p - n),
        "count_signed_error": p - n,
        "pq": float(2 * iou.sum() / (n + p)) if n + p else 1.0,
        "instance_f1": 2 * matches / (n + p) if n + p else 1.0,
        "segmentation_quality": float(np.mean(iou)) if matches else None,
        "precision": matches / p if p else None,
        "recall": matches / n if n else None,
        "foreground_dice": 2 * intersection / combined_area if combined_area else 1.0,
        "foreground_iou": intersection / union if union else 1.0,
        "area_w1_pixels_squared": area_error,
        "area_w1_reference_median_normalized": (
            area_error / median_area if area_error is not None and median_area else None
        ),
        "eccentricity_w1_all": w1(truth.eccentricity, predicted.eccentricity),
        "eccentricity_w1_survivors": w1(truth.eccentricity[gi], predicted.eccentricity[pi]),
        "reference_border_count": int(truth.border.sum()),
        "prediction_border_count": int(predicted.border.sum()),
        "reference_disconnected_count": int((truth.components > 1).sum()),
        "prediction_disconnected_count": int((predicted.components > 1).sum()),
    }
    if any(isinstance(v, float) and not math.isfinite(v) for v in result.values()):
        raise ValueError("Evaluation produced a nonfinite value")
    return result
