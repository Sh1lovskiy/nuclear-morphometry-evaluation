"""Bounded native-ID objects and sparse exclusive IoU matching.

Refactored from the archived shape kernel. An ID is one object even if it has
disconnected components; border-touching objects are retained and flagged.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import label as connected_label
from skimage.measure import regionprops

Mask = NDArray[Any]
FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class Objects:
    ids: IntArray
    area: IntArray
    eccentricity: FloatArray
    border: NDArray[np.bool_]
    components: IntArray


def validate_mask(mask: Mask) -> Mask:
    """Require bounded two-dimensional nonnegative integer labels."""
    mask = np.asarray(mask)
    if mask.ndim != 2 or not all(mask.shape) or mask.size > 1024 * 1024:
        raise ValueError("A nonempty 2D mask with at most 1,048,576 pixels is required")
    if mask.dtype.kind not in "iu":
        raise TypeError("Instance labels must have an integer dtype")
    if int(mask.min()) < 0 or int(mask.max()) > np.iinfo(np.int64).max:
        raise ValueError("Instance IDs must lie in the nonnegative int64 range")
    return mask


def eligible_map(mask: Mask, ids: IntArray) -> NDArray[np.int32]:
    """Compact eligible native IDs without allocating by the maximum label."""
    if not len(ids):
        return np.zeros(mask.shape, np.int32)
    positions = np.searchsorted(ids, mask)
    valid = positions < len(ids)
    valid &= ids[np.minimum(positions, len(ids) - 1)] == mask
    return np.where(valid, positions + 1, 0).astype(np.int32)


def objects(mask: Mask, min_area: int = 16) -> Objects:
    """Extract pixel area, second-moment eccentricity and eligibility flags."""
    mask = validate_mask(mask)
    if type(min_area) is not int or min_area < 1:
        raise ValueError("The minimum area must be a positive integer")
    ids, counts = np.unique(mask, return_counts=True)
    ids = ids[(ids > 0) & (counts >= min_area)].astype(np.int64)
    border_ids = np.unique(np.concatenate((mask[0], mask[-1], mask[:, 0], mask[:, -1])))
    area, eccentricity, components = [], [], []
    for region in regionprops(eligible_map(mask, ids), cache=False):
        area.append(int(region.area))
        eccentricity.append(float(region.eccentricity))
        components.append(int(connected_label(region.image, structure=np.ones((3, 3), int))[1]))
    return Objects(
        ids=ids,
        area=np.asarray(area, dtype=np.int64),
        eccentricity=np.asarray(eccentricity, dtype=np.float64),
        border=np.isin(ids, border_ids),
        components=np.asarray(components, dtype=np.int64),
    )


def strict_matches(
    reference: Mask, prediction: Mask, truth: Objects, predicted: Objects
) -> tuple[IntArray, IntArray, FloatArray]:
    """Unique matches at strict IoU > 0.5; exact half-overlap is excluded."""
    reference, prediction = validate_mask(reference), validate_mask(prediction)
    if reference.shape != prediction.shape:
        raise ValueError("Reference and prediction masks must have the same shape")
    g = eligible_map(reference, truth.ids)
    p = eligible_map(prediction, predicted.ids)
    both = (g > 0) & (p > 0)
    width = len(predicted.ids) + 1
    codes, intersections = np.unique(g[both].astype(np.int64) * width + p[both], return_counts=True)
    gi, pi = codes // width - 1, codes % width - 1
    union = truth.area[gi] + predicted.area[pi] - intersections
    selected = 2 * intersections > union
    gi, pi, iou = gi[selected], pi[selected], intersections[selected] / union[selected]
    if len(np.unique(gi)) != len(gi) or len(np.unique(pi)) != len(pi):
        raise ValueError("Exclusive-mask strict matching uniqueness failed")
    return gi, pi, iou
