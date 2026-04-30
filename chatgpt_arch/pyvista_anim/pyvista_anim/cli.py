from __future__ import annotations

import argparse
import random

from pyvista_anim.animations import RandomMobius, RotatePoints
from pyvista_anim.render import render_interactive, render_movie, render_single_frame
from pyvista_anim.scenes import make_default_scene, test_scene_1, test_scene_2, test_scene_3, test_scene_4
from pyvista_anim.state import make_grid_state, make_grid_state_city
from pyvista_anim.view import PolyDataView, StructuredGridView
from pyvista_anim.colormaps import happy_colormap


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pyvista-anim",
        description="Mathematical PyVista StructuredGrid animations",
    )
    parser.add_argument("-d", "--debugval", default=0.0, type=float)
    parser.add_argument("-D", "--duration", default=3.0, type=float, help="Duration in seconds")
    parser.add_argument("-m", "--movie", action="store_true")
    parser.add_argument("-n", "--name", help="Output movie filename")
    parser.add_argument("-f", "--framerate", default=25, type=int)
    parser.add_argument("-s", "--singleframe", action="store_true")
    parser.add_argument("--width", default=50, type=int)
    parser.add_argument("--height", default=50, type=int)
    parser.add_argument("--warp-factor", default=0.2, type=float)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.framerate <= 0:
        raise ValueError("framerate must be positive")
    if args.duration <= 0.0:
        raise ValueError("duration must be positive")
    if args.width <= 1 or args.height <= 1:
        raise ValueError("width and height must both be greater than 1")

    if args.movie and args.name is None:
        args.name = f"movie{random.randint(1000, 9999)}.mp4"

    print(args)

    # state = make_grid_state(args.width, args.height)
    # state = make_grid_state_city(args.width, args.height, block_count=20)
    # view = StructuredGridView(state, warp_factor=args.warp_factor)
    
    # scene = make_default_scene(args.duration)
    # scene = test_scene_2(args.duration, rate=2.0)
    scene = test_scene_4(args.duration)

    # colormap = happy_colormap(state.intensity.min(), state.intensity.max())
    view = PolyDataView("D:/Code/math_visualizations/3Dmodel/tinker.obj")
    if args.singleframe:
        render_single_frame(view) 
        # render_single_frame(view, t=args.debugval, state=state, scene=scene)
    elif args.movie:
        render_movie(view, args.name, fps=25, duration=args.duration) 
        # render_movie(view, filename=args.name, fps=args.framerate, state=state, scene=scene)
        print(f"Made movie {args.name}")
    else:
        render_interactive(view, fps=25, duration=10.0, state=view, scene=RotatePoints(10.0, angle=45))
        # render_interactive(view, fps=25, duration=args.duration, scene=scene)  
        # render_interactive(view, fps=args.framerate, state=state, scene=scene, cmap=colormap)


if __name__ == "__main__":
    main()
