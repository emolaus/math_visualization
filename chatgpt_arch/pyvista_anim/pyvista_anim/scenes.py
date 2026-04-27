from __future__ import annotations

from pyvista_anim.animations import BendPoints, FadeElevation, RandomMobius, WaveElevation, RotatePoints
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
            WaveElevation(duration=first, amplitude=0.8, speed=3.0, cycles=1.5),
            BendPoints(duration=first, amplitude=0.12, cycles=1.0),
        ),
    )

def test_scene_2(duration: float, rate: float = 2.0):
    """Test the Random Mobius animation."""
    
    return Sequence(
        Parallel(
            RandomMobius(duration=duration, rate=rate),
            WaveElevation(duration=duration, amplitude=0.4, speed=2.0, cycles=1.5),
        )
    )