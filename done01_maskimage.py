import numpy as np
import indraspearls.indrautils as iu
import pyvista as pv
from PIL import Image



# Load a mask
img = Image.open("mask_fox.png").convert("L")  # grayscale
mask = np.array(img) > 128  # binary mask, True for white pixels
mask = np.flipud(mask)  # flippa vertikalt så att positiva y-axeln pekar uppåt i bild
# Om jag har ritat en räv som tittar åt vänster, så kommer "upp" att vara åt positiva y-hållet, 
# och "vänster" att vara åt negativa x-hållet. Det är lite

# Grid in plane
# Hard-coded for now
n = 200
x = np.linspace(-1, 1, n)
y = np.linspace(0, 2, n)
xx, yy = np.meshgrid(x, y)

# Simpler mask: filled square. Same shape as the grid.
# mask = (np.abs(xx) <= 0.5) & (np.abs(yy) <= 0.5)



# denominator = xx**2 + yy**2 + 1

# X = 2 * xx / denominator
# Y = 2 * yy / denominator
# X = xx / denominator
# Y = yy / denominator
# Z = (xx**2 + yy**2 - 1) / denominator
X,Y,Z = iu.project_plane_to_sphere(xx, yy)



points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
grid = pv.StructuredGrid()
grid.points = points
grid.dimensions = [n, n, 1]

# Add scalar for masking
grid["mask"] = mask.ravel().astype(float)

p = pv.Plotter()
p.add_mesh(grid, scalars="mask", opacity=0.8)
p.add_mesh(pv.Sphere(radius=0.5, center=(0, 0, 0.5)), style="wireframe", color="black")
p.show()