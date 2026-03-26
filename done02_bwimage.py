import numpy as np
import indrautils as iu
import pyvista as pv
from PIL import Image

# Load a mask
img = Image.open("fox.png").convert("L")  # grayscale
img = np.array(img) / 255.0  # normalize to [0, 1]
img = np.flipud(img)  # flippa vertikalt så att positiva y-axeln pekar uppåt i bild
# Om jag har ritat en räv som tittar åt vänster, så kommer "upp" att vara åt positiva y-hållet, 
# och "vänster" att vara åt negativa x-hållet. Det är lite

h, w = img.shape

# Grid in plane
x = np.linspace(-1, 1, w)
y = np.linspace(0, 2, h)
xx, yy = np.meshgrid(x, y)

X,Y,Z = iu.project_plane_to_sphere(xx, yy)



points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
grid = pv.StructuredGrid()
grid.points = points
grid.dimensions = [w, h, 1]

# Add scalar for masking
grid["intensity"] = img.ravel().astype(float)

p = pv.Plotter()
p.add_mesh(grid, scalars="intensity", cmap="gray", show_scalar_bar=False)
p.add_mesh(pv.Sphere(radius=0.5, center=(0, 0, 0.5)), style="wireframe", color="white")
p.show()