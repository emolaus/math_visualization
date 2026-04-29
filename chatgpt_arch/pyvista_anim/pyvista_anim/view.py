from __future__ import annotations

from typing import Protocol

import pyvista as pv

from pyvista_anim.state import GridState


class View(Protocol):
    """Minimal interface required by PyVistaRenderer."""

    mesh: pv.DataSet

    def update(self) -> None:
        ...


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


class PolyDataView:
    """View for a static 3D model loaded from a file via pyvista.read().

    The mesh is loaded once at construction time and never mutated, so
    update() is a no-op.  Texture support covers two paths:

    * OBJ + paired MTL — pyvista.read() embeds the texture automatically;
      no texture_path is needed.
    * Any other format — pass an explicit texture_path to a PNG/JPG/etc.
      that pyvista.read_texture() can load.
    """

    texture: pv.Texture | None

    def __init__(
        self,
        path: str | None = None,
        texture_path: str | None = None,
        mesh: pv.PolyData | None = None,
    ) -> None:
        if mesh is not None:
            self.mesh = mesh
        elif path is not None:
            self.mesh = pv.read(path)
        else:
            raise ValueError("Provide either 'path' or 'mesh'.")

        if texture_path is not None:
            self.texture = pv.read_texture(texture_path)
        else:
            self.texture = None

    def update(self) -> None:
        pass

