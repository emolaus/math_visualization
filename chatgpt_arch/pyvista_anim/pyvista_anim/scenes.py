from __future__ import annotations
from matplotlib import scale
import numpy as np

from pyvista_anim.animations import BendPoints, FadeElevation, RandomMobius, SimpleScalePoints, SwirlPoints, WaveElevation, RotatePoints, SimpleExpPoints
from pyvista_anim.timeline import Parallel, Sequence


def make_default_scene(duration: float):
    """A small demo scene combining parallel and serial animation."""
    first = min(duration * 0.6, duration)
    second = max(duration - first, 0.1)

    return Sequence(
        Parallel(
            WaveElevation(duration=first, amplitude=0.8, speed=3.0, cycles=1.5),
            BendPoints(duration=first, amplitude=0.12, cycles=1.0),
        ),
        Parallel(
            WaveElevation(duration=second, amplitude=0.3, speed=-2.0, cycles=2.0),
            FadeElevation(duration=second),
        ),
    )

def test_scene_1(duration: float):
    """Test that the default scene can be created and applied to a state."""
    first = min(duration * 0.6, duration)
    second = max(duration - first, 0.1)

    return Sequence(
        Parallel(
            WaveElevation(duration=first, amplitude=0.01, speed=3.0, cycles=1.5),
            # BendPoints(duration=first, amplitude=0.12, cycles=1.0),
        ),
    )

def test_scene_2(duration: float, rate: float = 2.0):
    """Test the Random Mobius animation."""
    
    return Sequence(
        Parallel(
            SwirlPoints(duration=duration, strength=0.5),
            # WaveElevation(duration=duration, amplitude=0.4, speed=2.0, cycles=1.5),
        )
    )

def test_scene_3(duration: float):
    ''' Test applying multiple points animations in parallel. '''
    return Sequence(
        Parallel(
            WaveElevation(duration=duration, amplitude=0.1, speed=5.0, cycles = 2), #, speed=2.0, cycles=1.5
            # RandomMobius(duration=duration, rate=2.0),
            SimpleExpPoints(duration=0.5, final_angle=2*np.pi),
        ),
    )

def test_scene_4(duration: float):
    ''' Test applying multiple points animations in parallel. '''
    angle = np.atan2(-0.5, 2*np.pi)
    scale_x = np.cos(angle)
    scale_y = 1 / np.cos(angle)*1.5
    return Sequence(
        Parallel(
            RotatePoints(duration=2, angle=angle*180/np.pi), #, speed=2.0, cycles=1.5
            SimpleScalePoints(duration=2, scale_x=scale_x, scale_y=scale_y),
            # RandomMobius(duration=duration, rate=2.0),
            SimpleExpPoints(duration=0.5, final_angle=2*np.pi),
        ),
    )