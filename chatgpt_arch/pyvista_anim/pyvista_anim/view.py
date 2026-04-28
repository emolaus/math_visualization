from __future__ import annotations

import pyvista as pv

from pyvista_anim.state import GridState


class StructuredGridView:
    """PyVista adapter for GridState.

    This keeps PyVista-specific mutation out of animation classes.
    """

    def __init__(self, state: GridState, warp_factor: float = 0.2):
        self.state = state
        self.warp_factor = warp_factor

        self.mesh = pv.StructuredGrid()
        self.mesh.points = state.base_points.copy()
        self.mesh.dimensions = [state.w, state.h, 1]
        self.mesh["intensity"] = state.intensity.ravel().astype(float)


    def update(self) -> pv.StructuredGrid:
        self.mesh.points = self.state.points
        self.mesh["intensity"] = self.state.intensity.ravel().astype(float)
        return self.mesh

