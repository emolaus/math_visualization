from __future__ import annotations

from typing import Protocol

from matplotlib.pyplot import step
from matplotlib.pyplot import step
import numpy as np

from pyvista_anim.state import GridState, PointsState


class Animation(Protocol):
    """Anything that can mutate a pyvista points array (shape (n_points, 3)) at local time `t`."""

    duration: float

    def apply(self, t: float) -> None:
        ...

class PointsTranslationX:
    """Translate the grid points in a specified direction.
    
    """

    def __init__(self, points: np.ndarray, duration: float, distance: float, starting_point: float = 0.0):
        self.points = points
        self.duration = duration
        self.distance = distance
        self.starting_point = starting_point

    def apply(self, t: float) -> None:
        phase = t / self.duration if self.duration > 0.0 else 1.0
        self.points[:, 0] = self.starting_point + self.distance * phase

class PointsNoiseZ:
    """Add noise to the grid points in the z direction."""

    def __init__(self, points: np.ndarray, duration: float, amplitude: float = 0.05):
        self.points = points
        self.duration = duration
        self.amplitude = amplitude

    def apply(self, t: float) -> None:
        phase = t / self.duration if self.duration > 0.0 else 1.0
        noise = self.amplitude * np.random.randn(self.points.shape[0]) * phase
        self.points[:, 2] += noise

class WaveElevation:
    """Write a traveling sine wave onto the grid elevation (z)."""

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
        state.points[:, 2] = wave.ravel() + state.base_points[:, 2]

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

class RotatePoints:
    """Rotate the grid points around the z-axis while preserving the base geometry."""

    def __init__(self, duration: float, angle: float = 360.0):
        self.duration = duration
        self.angle = np.radians(angle)

    def apply(self, state: GridState, t: float) -> None:
        phase = t / self.duration if self.duration > 0.0 else 1.0
        points = state.points
        # base_points = state.base_points

        theta = self.angle * phase
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        x = points[:, 0]
        y = points[:, 1]

        points[:, 0] = cos_theta * x - sin_theta * y
        points[:, 1] = sin_theta * x + cos_theta * y

class SimpleScalePoints:
    """Scale the grid points up and down while preserving the base geometry."""

    def __init__(self, duration: float, scale_x: float = 1.0, scale_y: float = 1.0):
        self.duration = duration
        self.scale_x = scale_x
        self.scale_y = scale_y

    def apply(self, state: GridState, t: float) -> None:
        phase = t / self.duration if self.duration > 0.0 else 1.0
        points = state.points
        # base_points = state.base_points

        s_x = 1.0 + (self.scale_x - 1.0) * phase
        s_y = 1.0 + (self.scale_y - 1.0) * phase

        points[:, 0] = points[:, 0] * s_x
        points[:, 1] = points[:, 1] * s_y

class RandomMobius:
    """Randomly perturb points in a Möbius-like way.
    A rate of 2.0 is pretty calm, 10.0 is pretty wild.
    """

    def __init__(self, duration: float, rate: float = 1.0):
        self.duration = duration
        self.rate = rate

    def apply(self, state: GridState, t: float) -> None:
        step = int(t / 0.04)
        seconds = step * self.duration / 1000.0  # convert to seconds for smoother animation 
        radians = seconds * 2 * np.pi  # convert to radians for smooth periodic motion

    # ### Möbius transformation with time-varying parameters
        t = radians*self.rate
        a = 1 + np.sin(t*0.11) + np.sin(t*0.23)*1j
        b = np.sin(t*0.05) + np.sin(t*0.17)*1j
        c = np.sin(t*0.29) + np.sin(t*0.09)*1j
        d = 1 + np.sin(t*0.151) + np.sin(t*0.37)*1j
        self._mobius_transform(state.points, a, b, c, d, normalize=True)

    def _mobius_transform(self, points, a, b, c, d, normalize=True):
        '''Apply a Möbius transformation to a set of points directly in the points array.'''
        
        # determinant
        det = a*d - b*c
        if np.isclose(det, 0):
            raise ValueError("Not a valid Möbius transform: ad - bc = 0")
        
        if normalize:
            # normalize so determinant = 1
            lam = 1 / np.sqrt(det)
            a *= lam
            b *= lam
            c *= lam
            d *= lam

        x = points[:, 0]
        y = points[:, 1]
        z0 = x + 1j * y
        z1 = (a * z0 + b) / (c * z0 + d)
        points[:, 0] = z1.real
        points[:, 1] = z1.imag

class SimpleExpPoints:
    """Swirl the grid points around the center while preserving the base geometry."""

    def __init__(self, duration: float, final_angle: float = 2 * np.pi):
        self.duration = duration
        self.final_angle = final_angle # ignored for now

    def apply(self, state: GridState, t: float) -> None:
        theta = 0.3
        points = state.points.copy()
        points[:, 1] -= points[:, 1].min()
        points[:, 1] /= points[:, 1].max()
        points[:, 1] *= np.pi * 2 * t/self.duration
        z0 = points[:, 0] + 1j * points[:, 1]
        z1 = np.exp(z0)
        state.points[:, 0] = z1.real
        state.points[:, 1] = z1.imag


class SwirlPoints:
    """Swirl the grid points around the center while preserving the base geometry."""

    def __init__(self, duration: float, strength: float = 0.5):
        self.duration = duration
        self.strength = strength

    def apply(self, state: GridState, t: float) -> None:
        pass
        theta = 0.3
        z0 = (state.points[:, 0]*t + 1j * state.points[:, 1]*t)*(np.cos(theta) + 1j * np.sin(theta))
        z1 = np.exp(z0)
        state.points[:, 0] = z1.real
        state.points[:, 1] = z1.imag

class FadeElevation:
    """ OUTDATED, DO NOT USE
    Scale the current elevation down to zero over the animation duration.
    This is not correct or useful at the moment
    """

    def __init__(self, duration: float):
        self.duration = duration

    def apply(self, state: GridState, t: float) -> None:
        phase = min(max(t / self.duration, 0.0), 1.0) if self.duration > 0.0 else 1.0
        # state.points[:, 2] *= 1.0 - phase
        state.points[:,2] = state.base_points[:,2] + state.points[:,2] * (1.0 - phase)
        state.intensity = state.points[:, 2]
