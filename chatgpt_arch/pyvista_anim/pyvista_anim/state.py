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
    base_elevation: np.ndarray
    elevation: np.ndarray
    intensity: np.ndarray
    w: int
    h: int

    def reset(self) -> None:
        """Reset mutable state to the flat/base frame."""
        self.points[:] = self.base_points
        self.elevation[:] = self.base_elevation
        self.intensity[:] = self.base_elevation


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
    base_elevation = elevation.copy()
    intensity = np.zeros((h, w), dtype=float)

    return GridState(
        base_points=base_points,
        points=base_points.copy(),
        elevation=elevation,
        base_elevation=base_elevation,
        intensity=intensity,
        w=w,
        h=h,
    )

def make_grid_state_city_1(w: int, h: int) -> GridState:
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
    base_elevation = elevation.copy()
    block_count = 10
    block_width = w // block_count
    block_height = h // block_count
    for i in range(block_count):
        for j in range(block_count):
            y_start = i * 2 * block_height
            y_end = y_start + block_height
            x_start = j * 2 * block_width
            x_end = x_start + block_width
            elevation[y_start:y_end, x_start:x_end] = 0.5 + 1.0 * np.random.random()
    base_elevation = elevation.copy()
    intensity = elevation.copy()

        # y_start = i * 50
        # y_end = y_start + 25
        # x_start = j * 50
        # x_end = x_start + 25

    return GridState(
        base_points=base_points,
        points=base_points.copy(),
        elevation=elevation,
        base_elevation=base_elevation,
        intensity=intensity,
        w=w,
        h=h,
    )