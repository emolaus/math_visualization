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

        self.flatgrid = pv.StructuredGrid()
        self.flatgrid.points = state.base_points.copy()
        self.flatgrid.dimensions = [state.w, state.h, 1]
        self.flatgrid["elevation"] = state.elevation.ravel().astype(float)
        self.flatgrid["intensity"] = state.intensity.ravel().astype(float)

        self.mesh = self._make_warped_mesh()

    def update(self) -> pv.StructuredGrid:
        self.flatgrid.points = self.state.points
        self.flatgrid["elevation"] = self.state.elevation.ravel().astype(float)
        self.flatgrid["intensity"] = self.state.intensity.ravel().astype(float)
        self.mesh = self._make_warped_mesh()
        return self.mesh

    def _make_warped_mesh(self) -> pv.StructuredGrid:
        return self.flatgrid.warp_by_scalar("elevation", factor=self.warp_factor)
