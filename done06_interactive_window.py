import numpy as np
import pyvista as pv
import indrautils as iu

t = np.linspace(0, 2*np.pi, 500)
x = np.cos(t)
y = np.sin(t)
z = np.zeros_like(x)

# project the point to the sphere
u, v, w = iu.project_plane_to_sphere(x, y)

theta = 0

# rotate the points on the sphere around the x-axis by theta degrees
ut, vt, wt = iu.rotate_riemann_sphere_around_x_axis(u, v, w, theta)

# project the rotated points back to the plane
xt, yt, zt = iu.project_sphere_to_plane(ut, vt, wt)

# Stack the coordinates into a single array of shape (n_points, 3)
# Get back e.g. x by doing orig_points[:, 0]
points_orig = np.c_[x, y, z]
points_sphere = np.c_[ut, vt, wt]
points_projected = np.c_[xt, yt, zt]



p = pv.Plotter()
line_sphere = pv.lines_from_points(points_sphere)
line_orig = pv.lines_from_points(points_orig)
line_projected = pv.lines_from_points(points_projected)
p.add_mesh(line_sphere, color="black")
p.add_mesh(line_orig, color="black")
p.add_mesh(line_projected, color="green")
p.add_mesh(pv.Sphere(radius=0.5, center=(0, 0, 0.5)), style="wireframe", color="white")
plane = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=10, j_size=10)


def update(angle):
    global theta
    theta = angle
    # rotate the points on the sphere around the x-axis by theta degrees
    ut, vt, wt = iu.rotate_riemann_sphere_around_x_axis(u, v, w, angle)
    
    # project the rotated points back to the plane
    xt, yt, zt = iu.project_sphere_to_plane(ut, vt, wt)

    # update sphere curve
    line_sphere.points = np.c_[ut, vt, wt]
    line_sphere.Modified()

    # update projected curve
    line_projected.points = np.c_[xt, yt, zt]
    line_projected.Modified()

    p.render()

p.add_slider_widget(
    update,
    [-np.pi, np.pi],
    value=0,
    title="Rotation angle (press 'a' or 'd' to rotate)",
)
def keypress_a_callback():
    update(theta + np.pi/100)
def keypress_d_callback():
    update(theta - np.pi/100)
p.add_key_event(
    "a",  # Press 'a' to trigger the callback
    keypress_a_callback
)
p.add_key_event(
    "d",  # Press 'd' to trigger the callback
    keypress_d_callback
)
p.show()