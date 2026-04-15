import numpy as np
import pyvista as pv
from PIL import Image

img = Image.open("streets3.png").convert("L")  # grayscale
img = np.array(img) / 255.0  # normalize to [0, 1]
h, w = img.shape
print(h,w)

# Grid in plane. They all have shape (h,w). x represents the real part of the complex number, and y represents the imaginary part.
x_min = -3
x_max = 1
y_min = 0
y_max = 2*np.pi # Wrap around the circle once. 
x = np.linspace(x_min, x_max, w)
y = np.linspace(y_min, y_max, h)
xx, yy = np.meshgrid(x, y)

# This is an unbounded spiral. It needs to be fitted to a finite region.
zz = np.exp(xx + 1j*yy)
XX = np.real(zz)
YY = np.imag(zz)
print(zz[0:5,0:5])

points = np.c_[XX.ravel(), YY.ravel(), np.zeros_like(XX).ravel()]
grid = pv.StructuredGrid()
grid.points = points
grid.dimensions = [w, h, 1]

# Add scalar for masking
grid["intensity"] = img.ravel().astype(float)

p = pv.Plotter()
p.add_mesh(grid, scalars="intensity", cmap="gray", show_scalar_bar=False)
p.show()