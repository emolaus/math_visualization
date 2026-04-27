from __future__ import annotations

from typing import Protocol

import numpy as np

from pyvista_anim.state import GridState


class Animation(Protocol):
    """Anything that can mutate a GridState at local time `t`."""

    duration: float

    def apply(self, state: GridState, t: float) -> None:
        ...


class WaveElevation:
    """Write a traveling sine wave into `state.elevation`."""

    def __init__(
        self,
        duration: float,
        amplitude: float = 1.0,
        speed: float = 1.0,
        cycles: float = 1.0,
    ):
        self.duration = duration
        self.amplitude = amplitude
        self.speed = speed
        self.cycles = cycles

    def apply(self, state: GridState, t: float) -> None:
        x = np.linspace(0.0, 2.0 * np.pi * self.cycles, state.w)
        y = np.linspace(0.0, 1.0, state.h)

        xx, _ = np.meshgrid(x + t * self.speed, y, indexing="xy")
        wave = self.amplitude * np.sin(xx)

        state.elevation[:] += wave + state.base_elevation
        state.intensity[:] = state.elevation + state.base_elevation


class BendPoints:
    """Bend the grid points sideways while preserving the base geometry."""

    def __init__(self, duration: float, amplitude: float = 0.15, cycles: float = 1.0):
        self.duration = duration
        self.amplitude = amplitude
        self.cycles = cycles

    def apply(self, state: GridState, t: float) -> None:
        phase = t / self.duration if self.duration > 0.0 else 1.0
        points = state.points
        x = state.base_points[:, 0]

        points[:, 1] += self.amplitude * np.sin(
            2.0 * np.pi * self.cycles * phase + x * np.pi
        )


class FadeElevation:
    """Scale the current elevation down to zero over the animation duration."""

    def __init__(self, duration: float):
        self.duration = duration

    def apply(self, state: GridState, t: float) -> None:
        phase = min(max(t / self.duration, 0.0), 1.0) if self.duration > 0.0 else 1.0
        state.elevation[:] *= 1.0 - phase
        state.intensity[:] = state.elevation
