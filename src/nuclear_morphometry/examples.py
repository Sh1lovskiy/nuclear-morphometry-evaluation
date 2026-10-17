"""Synthetic labeled masks; these are not histological observations."""

import numpy as np

from .domain import Mask


def synthetic_masks() -> tuple[Mask, Mask, Mask]:
    """Two 4x4 squares and one 2x8 rectangle, all with 16 pixels."""
    reference = np.zeros((16, 24), dtype=np.int32)
    reference[2:6, 2:6] = 1
    reference[9:13, 2:6] = 2
    reference[4:6, 12:20] = 3
    square_deleted = reference.copy()
    square_deleted[square_deleted == 1] = 0
    rectangle_deleted = reference.copy()
    rectangle_deleted[rectangle_deleted == 3] = 0
    return reference, square_deleted, rectangle_deleted
