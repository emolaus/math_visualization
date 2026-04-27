import argparse
import numpy as np
import pyvista as pv

# Börja med enklast möjliga.
def get_initial_grid(w, h):
    elevation_base = np.zeros((w,h))
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros_like(xx)
    points_base = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]

    # Create the grid
    flatgrid = pv.StructuredGrid()
    flatgrid.points = points_base
    flatgrid.dimensions = [w,h,1]
    flatgrid['elevation'] = elevation_base.ravel().astype(float)
    flatgrid['intensity'] = elevation_base.ravel().astype(float)
    grid = flatgrid.warp_by_scalar('elevation', factor=0.5)
    return grid, points_base, elevation_base, w, h, flatgrid

def stepfunc():
    pass

class WaveAnimation:
    '''
    This class will add a wave to the elevation of the grid.
    '''
    def __init__(self, grid, points_base, elevation_base, w, h, duration, flatgrid):
        self.grid = grid
        self.points_base = points_base
        self.elevation_base = elevation_base
        self.w = w
        self.h = h
        self.flatgrid = flatgrid
        self.duration = duration
        self.xx = np.zeros((w,h))
    
    def step(self, time, scale=1.0):
        # let's do just x direction for now
        self.xx, _ = np.meshgrid(np.linspace(0, 2 * np.pi, self.w) + time*scale, np.linspace(0, 1, self.h))
        self.xx = np.sin((self.xx))
        self.flatgrid['elevation'] = self.xx.ravel().astype(float)
        self.grid = self.flatgrid.warp_by_scalar('elevation', factor=0.2)

if __name__ == '__main__':
    # ---- Argument parsing ---- 
    # python .\WIP15_better_architecture.py -h to get this information, and 'help' information below
    parser = argparse.ArgumentParser(
        prog='Architecture tests', 
        description='Wave propagation in 2D with better architecture')
    
    # action='store_true' means that if the flag is present, movie will be set to True, otherwise it will be False
    parser.add_argument('-d', '--debugval', help='A debug value to pass to whatever Im up to right now ', default=0.0, type=float)
    parser.add_argument('-t','--time', help='Simulation time', default=3.0, type=float)
    parser.add_argument('-m', '--movie', action='store_true', help='Make video instead of animation')
    parser.add_argument('-n', '--name', help='Name of the output file, if movie')
    parser.add_argument('-f', '--framerate', default=25, type=int, help='Framerate for the movie or animation')
    parser.add_argument('-s', '--singleframe', action='store_true', help='Show a single frame instead of animation')
    
    args = parser.parse_args()
    args.duration_ms = int(1 / float(args.framerate) * 1000)
    if args.movie and (args.name is None):
        randint = int((np.random.random()*10000))
        args.name = f'movie{randint}.mp4'

    args.max_steps = int(args.framerate * args.time)
    print(args)

    # --- Experiment ---
    # Create the grid
    w, h = 50, 5
    grid, points_base, elevation_base, w, h, flatgrid = get_initial_grid(w, h)
    a1 = WaveAnimation(grid, points_base, elevation_base, w, h, args.time, flatgrid)
    p = pv.Plotter()
    p.add_mesh(a1.grid, cmap="gray", show_scalar_bar=False, name='wave')

    if args.singleframe:
        a1.step(args.debugval)
        p.add_mesh(a1.grid, cmap="gray", scalars="intensity", show_scalar_bar=False, name='wave')
        p.show()

    elif args.movie:
        p.open_movie(args.name, framerate=args.framerate)
        p.write_frame()
        for step in range(args.max_steps):
            print(f"Writing frame {step}")
            a1.step(step * args.duration_ms / 1000.0)
            p.add_mesh(a1.grid, cmap="gray", scalars="intensity", show_scalar_bar=False, name='wave')
            p.write_frame()
        p.close()
        print(f"Made movie {args.name}")

    else: # Animated plot
        p.iren.initialize()
        def stepper(step):
            print(f"Timer event: step {step}")
            a1.step(step * args.duration_ms / 1000.0)
            p.add_mesh(a1.grid, cmap="gray", scalars="intensity", show_scalar_bar=False, name='wave')
        p.add_timer_event(max_steps=args.max_steps, duration=args.duration_ms, callback=stepper )
        p.show()


    # p.add_mesh(warped, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')
    # Add mesh to plotter
    # p = pv.Plotter()
    # p.add_mesh(grid, cmap="gray", show_scalar_bar=False, name='mask')
    # p.show()
