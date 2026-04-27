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
    grid = flatgrid.warp_by_scalar('elevation', factor=0.5)
    return grid, points_base, elevation_base, w, h

class WaveAnimation:
    '''
    This class will add a wave to the elevation of the grid.
    '''
    def __init__(self, grid, points_base, elevation_base, w, h, duration):
        self.grid = grid
        self.points_base = points_base
        self.elevation_base = elevation_base
        self.w = w
        self.h = h
        self.duration = duration
        self.xx = np.zeros((w,h))
    
    def step(self, time):
        # let's do just x direction for now
        self.xx, _ = np.meshgrid(np.linspace(0, 1, self.w), np.linspace(0, 1, self.h))
        self.xx = np.sin(2 * np.pi * time * (self.xx))
        self.grid.elevation = self.xx.ravel().astype(float)

if __name__ == '__main__':

    # python .\WIP15_better_architecture.py -h to get this information, and 'help' information below
    parser = argparse.ArgumentParser(
        prog='Architecture tests', 
        description='Wave propagation in 2D with better architecture')
    
    # action='store_true' means that if the flag is present, movie will be set to True, otherwise it will be False
    parser.add_argument('-d', '--debugval', help='A debug value to pass to whatever Im up to right now ', default=0.0, type=float)
    parser.add_argument('-m', '--movie', action='store_true', help='Make video instead of animation')
    parser.add_argument('-n', '--name', help='Name of the output file, if movie')
    parser.add_argument('-t','--time', help='Simulation time', default=10.0, type=float)
    args = parser.parse_args()
    if args.movie and (args.name is None):
        randint = int((np.random.random()*10000))
        args.name = f'movie{randint}.mp4'

    if args.movie:
        print(f"Making movie: {args.name}")

    # Create the grid
    w, h = 5, 1
    grid, points_base, elevation_base, w, h = get_initial_grid(w, h)
    a1 = WaveAnimation(grid, points_base, elevation_base, w, h, args.time)
    a1.step(float(args.debugval))
    print('elevation: ', grid.elevation)
    # Add mesh to plotter
    # p = pv.Plotter()
    # p.add_mesh(grid, cmap="gray", show_scalar_bar=False, name='mask')
    # p.show()
