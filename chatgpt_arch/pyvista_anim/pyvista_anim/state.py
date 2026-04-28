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
    intensity: np.ndarray
    w: int
    h: int

    def reset(self) -> None:
        """Reset mutable state to the flat/base frame."""
        self.points[:] = self.base_points
        self.intensity[:] = self.base_points[:,2]


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
    intensity = np.zeros((h, w), dtype=float)

    return GridState(
        base_points=base_points,
        points=base_points.copy(),
        intensity=intensity,
        w=w,
        h=h,
    )

def make_city_grid(w: int, h: int, block_count: int = 10, max_height: float = 1.0, random: bool = True, min_height: float = 0.2) -> np.ndarray:
    """Make a grid of building blocks with random heights."""
    x = np.linspace(0.0, 1.0, w)
    y = np.linspace(0.0, 6.28, h)

    xx, yy = np.meshgrid(x, y, indexing="xy") # indexing="xy" is default
    zz = np.zeros_like(xx)

    block_width = w // (block_count * 2)
    block_height = h // (block_count * 2)
    for i in range(block_count):
        for j in range(block_count):
            y_start = i * 2 * block_height
            y_end = y_start + block_height
            x_start = j * 2 * block_width
            x_end = x_start + block_width
            height = max_height
            if random:
                height = min_height + (max_height - min_height) * np.random.random()
            zz[y_start:y_end, x_start:x_end] = height

    return np.c_[xx.ravel(), yy.ravel(), zz.ravel()]

# , block_count=int(args.debugval), max_height=0.8, random=True, min_height=0.1
def make_grid_state_city(w: int, h: int, block_count: int = 10) -> GridState:
    """Create a flat rectangular grid state in the x/y plane.

    Arrays shaped like images use shape `(h, w)`.
    PyVista point arrays use shape `(h * w, 3)`.
    """
    base_points = make_city_grid(w, h, block_count=block_count)
    intensity = base_points[:,2].copy()

    return GridState(
        base_points=base_points,
        points=base_points.copy(),
        intensity=intensity,
        w=w,
        h=h,
    )