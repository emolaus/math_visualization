from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class GridState:
    """Mutable frame state for one StructuredGrid animation frame.

    The static mesh definition is represented by `base_points`.
    Each frame starts by resetting `points`, `elevation`, and `intensity`,
    then animations modify those arrays.
    """

    base_points: np.ndarray
    points: np.ndarray
    elevation: np.ndarray
    intensity: np.ndarray
    w: int
    h: int

    def reset(self) -> None:
        """Reset mutable state to the flat/base frame."""
        self.points[:] = self.base_points
        self.elevation[:] = 0.0
        self.intensity[:] = 0.0


def make_grid_state(w: int, h: int) -> GridState:
    """Create a flat rectangular grid state in the x/y plane.

    Arrays shaped like images use shape `(h, w)`.
    PyVista point arrays use shape `(h * w, 3)`.
    """
    x = np.linspace(-1.0, 1.0, w)
    y = np.linspace(-1.0, 1.0, h)

    xx, yy = np.meshgrid(x, y, indexing="xy")
    zz = np.zeros_like(xx)

    base_points = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
    elevation = np.zeros((h, w), dtype=float)
    intensity = np.zeros((h, w), dtype=float)

    return GridState(
        base_points=base_points,
        points=base_points.copy(),
        elevation=elevation,
        intensity=intensity,
        w=w,
        h=h,
    )