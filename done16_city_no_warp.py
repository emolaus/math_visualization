import numpy as np
import pyvista as pv

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

p = pv.Plotter()
p.add_mesh(city, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')
p.show()
