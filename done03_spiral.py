import numpy as np
import indraspearls.indrautils as iu
import pyvista as pv

# Polar grid in plane

n = 10000
m = 10
turns = 20
theta = np.linspace(0, turns*2*np.pi, n, endpoint=False) # avoid duplicate point at 2pi
# The radius will be logspaced later but this simplifies the calculation of the spiral
r_min = 0.01
# r_max = 100

line_thickness = 0.1
r = np.linspace(r_min, r_min + line_thickness, m)
tt, rr = np.meshgrid(theta, r)

# This is a hack to create a spiral pattern.
rr_delta,throw = np.meshgrid(np.linspace(-4, 3, n, endpoint=False), np.zeros(m))
rr = rr + rr_delta

xx,yy = np.exp(rr)*np.cos(tt), np.exp(rr)*np.sin(tt)

img = np.ones(rr.shape, dtype=float)*10.0

X,Y,Z = iu.project_plane_to_sphere(xx, yy)



# Grid on sphere
w = n
h = m
points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
grid_sphere = pv.StructuredGrid()
grid_sphere.points = points
grid_sphere.dimensions = [w, h, 1]

# Add scalar for masking
grid_sphere["intensity"] = img.ravel().astype(float)

zz = np.zeros_like(xx)
points_plane = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
grid_plane = pv.StructuredGrid()
grid_plane.points = points_plane
grid_plane.dimensions = [w, h, 1]
grid_plane["intensity"] = img.ravel().astype(float)

p = pv.Plotter()
p.add_mesh(grid_sphere, scalars="intensity", cmap="gray", show_scalar_bar=False)
p.add_mesh(pv.Sphere(radius=0.5, center=(0, 0, 0.5)), style="wireframe", color="white")

plane = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=100, j_size=100)
p.add_mesh(plane, style="wireframe", color="white")
p.add_mesh(grid_plane, scalars="intensity", cmap="gray", show_scalar_bar=False)
p.show()