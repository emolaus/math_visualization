import numpy as np
import indrautils as iu
import pyvista as pv

# Square path
# square_on_plane(center_x, center_y, angle360, side_length, n_points_per_side = 100)
points_plane = iu.square_on_plane(0.5, 0, 20, 1)

points_sphere = iu.project_plane_to_sphere(points_plane)

line_sphere = pv.lines_from_points(points_sphere, close=True)
line_plane = pv.lines_from_points(points_plane, close=True)

p = pv.Plotter()

p.add_mesh(line_sphere, color="black", line_width=3)
p.add_mesh(line_plane, color="red", line_width=3)

p.add_mesh(pv.Sphere(radius=0.5, center=(0, 0, 0.5)), style="wireframe", color="white")

p.add_mesh(pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=3, j_size=3), style="wireframe", color="white")

p.show()