from __future__ import annotations

from typing import Optional

import pyvista as pv

from pyvista_anim.object3D import Group3D
from pyvista_anim.animations import Animation
from pyvista_anim.state import GridState, PointsState
from pyvista_anim.view import View


class PyVistaRenderer:
    """Owns plotting and movie/interactive output."""

    def __init__(self, view: View, cmap: str = "gray"):
        self.view = view
        self.cmap = cmap
        self.plotter = pv.Plotter()
        self._add_current_mesh()

    def render_frame(self) -> None:
        self.view.update()
        self._add_current_mesh()

    def _add_current_mesh(self) -> None:
        mesh = self.view.mesh
        if "intensity" in mesh.array_names:
            self.plotter.add_mesh(
                mesh,
                cmap=self.cmap,
                scalars="intensity",
                show_scalar_bar=False,
                name="surface",
            )
        else:
            texture = getattr(self.view, "texture", None)
            if texture is not None:
                self.plotter.add_mesh(
                    mesh,
                    texture=texture,
                    name="surface",
                )
            else:
                self.plotter.add_mesh(
                    mesh,
                    name="surface",
                )

class NewRenderer:
    """Owns plotting and movie/interactive output."""

    def __init__(self, groups: list[Group3D], cmap: str = "gray"):
        self.groups = groups
        # Name each group for later reference when adding to the plotter.
        for i, group in enumerate(self.groups):
            group.name = f"group_{i}"
        self.cmap = cmap
        self.plotter = pv.Plotter()
        self._add_current_mesh()

    def render_frame(self) -> None:
        self._add_current_mesh()

    def _add_current_mesh(self) -> None:
        for group in self.groups:
            self.plotter.add_mesh(group.multiblock, cmap=self.cmap, show_scalar_bar=False, name=group.name)


def render_single_frame(
    groups: list[Group3D],
    t: float = 0.0,
    *,
    scene: Optional[Animation] = None,
    cmap: str = "gray",
) -> None:

    renderer = NewRenderer(groups, cmap=cmap)
    renderer.render_frame()
    renderer.plotter.show()

def render_movie(
    groups: list[Group3D],
    filename: str,
    fps: int,
    duration: Optional[float] = None,
    *,
    scene: Optional[Animation] = None,
    cmap: str = "gray",
) -> None:
    if duration is None and scene is not None:
        duration = scene.duration
    elif duration is None:
        raise ValueError("Provide either 'scene' or 'duration'.")

    renderer = NewRenderer(groups, cmap=cmap)
    plotter = renderer.plotter

    plotter.open_movie(filename, framerate=fps)

    n_frames = int(duration * fps)
    for frame in range(n_frames + 1):
        t = frame / fps
        print(f"Writing frame {frame}/{n_frames}: t={t:.3f} s")

        if scene is not None:
            scene.apply(t)
        renderer.render_frame()
        plotter.write_frame()

    plotter.close()

'''
This only supports a single animation at this point
'''
def render_interactive(
    groups: list[Group3D],
    fps: int,
    duration: Optional[float] = None,
    *,
    scene: Optional[Animation] = None,
    cmap: str = "gray",
) -> None:
    if duration is None and scene is not None:
        duration = scene.duration
    elif duration is None:
        raise ValueError("Provide either 'scene' or 'duration'.")

    renderer = NewRenderer(groups, cmap=cmap)
    plotter = renderer.plotter

    duration_ms = int(1000 / fps)
    max_steps = int(duration * fps)

    def stepper(step: int) -> None:
        t = step / fps
        print(f"Timer event: step={step}, t={t:.3f} s")

        # Reset all base_points
        for group in groups:
            group.reset()

        if scene is not None:
            scene.apply(t)

        renderer.render_frame()

    plotter.iren.initialize()
    plotter.add_timer_event(
        max_steps=max_steps,
        duration=duration_ms,
        callback=stepper,
    )
    plotter.show()
