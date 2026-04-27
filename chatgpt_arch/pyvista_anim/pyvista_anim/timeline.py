from __future__ import annotations

from pyvista_anim.animations import Animation
from pyvista_anim.state import GridState


class Parallel:
    """Run several animations at the same local time."""

    def __init__(self, *animations: Animation):
        if not animations:
            raise ValueError("Parallel requires at least one animation")

        self.animations = animations
        self.duration = max(anim.duration for anim in animations)

    def apply(self, state: GridState, t: float) -> None:
        for anim in self.animations:
            if 0.0 <= t <= anim.duration:
                anim.apply(state, t)
            elif t > anim.duration:
                # Hold each child at its final state.
                anim.apply(state, anim.duration)


class Sequence:
    """Run animations one after another."""

    def __init__(self, *animations: Animation):
        if not animations:
            raise ValueError("Sequence requires at least one animation")

        self.animations = animations
        self.duration = sum(anim.duration for anim in animations)

    def apply(self, state: GridState, t: float) -> None:
        elapsed = 0.0

        for anim in self.animations:
            start = elapsed
            end = elapsed + anim.duration

            if start <= t < end:
                anim.apply(state, t - start)
                return

            elapsed = end

        # Hold final frame after the sequence is over.
        last = self.animations[-1]
        last.apply(state, last.duration)
