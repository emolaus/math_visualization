from __future__ import annotations

import pyvista as pv

from pyvista_anim.animations import Animation
from pyvista_anim.state import GridState
from pyvista_anim.view import StructuredGridView


class PyVistaRenderer:
    """Owns plotting and movie/interactive output."""

    def __init__(self, view: StructuredGridView, cmap: str = "gray"):
        self.view = view
        self.cmap = cmap
        self.plotter = pv.Plotter()
        self._add_current_mesh()

    def render_frame(self) -> None:
        self.view.update()
        self._add_current_mesh()

    def _add_current_mesh(self) -> None:
        self.plotter.add_mesh(
            self.view.mesh,
            cmap=self.cmap,
            scalars="intensity",
            show_scalar_bar=False,
            name="surface",
        )


def render_single_frame(
    state: GridState,
    scene: Animation,
    view: StructuredGridView,
    t: float,
) -> None:
    state.reset()
    scene.apply(state, t)

    renderer = PyVistaRenderer(view)
    renderer.render_frame()
    renderer.plotter.show()


def render_movie(
    state: GridState,
    scene: Animation,
    view: StructuredGridView,
    filename: str,
    fps: int,
) -> None:
    renderer = PyVistaRenderer(view)
    plotter = renderer.plotter

    plotter.open_movie(filename, framerate=fps)

    n_frames = int(scene.duration * fps)
    for frame in range(n_frames + 1):
        t = frame / fps
        print(f"Writing frame {frame}/{n_frames}: t={t:.3f} s")

        state.reset()
        scene.apply(state, t)
        renderer.render_frame()
        plotter.write_frame()

    plotter.close()


def render_interactive(
    state: GridState,
    scene: Animation,
    view: StructuredGridView,
    fps: int,
) -> None:
    renderer = PyVistaRenderer(view)
    plotter = renderer.plotter

    duration_ms = int(1000 / fps)
    max_steps = int(scene.duration * fps)

    def stepper(step: int) -> None:
        t = step / fps
        print(f"Timer event: step={step}, t={t:.3f} s")

        state.reset()
        scene.apply(state, t)
        renderer.render_frame()

    plotter.iren.initialize()
    plotter.add_timer_event(
        max_steps=max_steps,
        duration=duration_ms,
        callback=stepper,
    )
    plotter.show()
