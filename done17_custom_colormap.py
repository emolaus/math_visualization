import numpy as np
import pyvista as pv
from matplotlib.colors import ListedColormap

h, w = 1000, 1000
# Grid in plane
x = np.linspace(-1, 1, h)
y = np.linspace(-1, 1, w)
xx, yy = np.meshgrid(x, y)
zz = np.zeros_like(xx)

N_blocks = 10
block_size = h // N_blocks
half_block = block_size // 2

for i in range(N_blocks):
    for j in range(N_blocks):
        y_start = 1 + i * block_size
        y_end = y_start + half_block
        x_start = 1 + j * block_size
        x_end = x_start + half_block
        zz[y_start:y_end, x_start:x_end] = 0.2 + 0.5 * np.random.random()

points = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
city = pv.StructuredGrid()
city.points = points
city.dimensions = [h,w,1]

city["intensity"] = points[:, 2].copy()



# Define the colors we want to use
blue = np.array([12 / 256, 238 / 256, 246 / 256, 1.0])
black = np.array([11 / 256, 11 / 256, 11 / 256, 1.0])
grey = np.array([189 / 256, 189 / 256, 189 / 256, 1.0])
yellow = np.array([255 / 256, 247 / 256, 0 / 256, 1.0])
red = np.array([1.0, 0.0, 0.0, 1.0])

mapping = np.linspace(city['intensity'].min(), city['intensity'].max(), 256)
newcolors = np.empty((256, 4))
newcolors[mapping >= 0.8] = red
newcolors[mapping < 0.8] = grey
newcolors[mapping < 0.55] = yellow
newcolors[mapping < 0.3] = blue
newcolors[mapping < 0.01] = grey

# Make the colormap from the listed colors
# my_colormap = ListedColormap(newcolors)

from chatgpt_arch.pyvista_anim.pyvista_anim.colormaps import happy_colormap
my_colormap = happy_colormap(city['intensity'].min(), city['intensity'].max())


p = pv.Plotter()
p.add_mesh(city, scalars="intensity", cmap=my_colormap, show_scalar_bar=False, name='mask')
p.show()


