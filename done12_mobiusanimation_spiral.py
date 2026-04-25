import numpy as np
import indrautils as iu
import pyvista as pv
from PIL import Image

points_spiral = iu.growth_spiral_on_plane(0, 0, 0.01, 100.0, 20.0, n_points = 10000)
lines_spiral = pv.lines_from_points(points_spiral, close=False)

p = pv.Plotter()
actor = p.add_mesh(lines_spiral, color="black", line_width=1.5)

def mobius_transform(points, a, b, c, d):
    '''Apply a Möbius transformation to a set of points directly in the points array.'''
    x = points[:, 0]
    y = points[:, 1]
    z0 = x + 1j * y
    z1 = (a * z0 + b) / (c * z0 + d)
    points[:, 0] = z1.real
    points[:, 1] = z1.imag

def callback(step):
    print(f"Timer event: step {step}")
    # This works
    # actor.position = [step / 100.0, step / 100.0, 0]

    points = points_spiral.copy()

    a = 1 + np.cos(step / 100.0 - 0.5) + np.cos(step / 97.0 - 0.5)*1j
    b = np.cos(step / 86.3 - 0.5) + np.cos(step / 91.2 - 0.5)*1j
    c = np.cos(step / 94.3 - 0.5) + np.cos(step / 67.3 - 0.5)*1j
    d = 1 + np.cos(step / 54.3 - 0.5) + np.cos(step / 92.3 - 0.5)*1j

    mobius_transform(points, a, b, c, d)

    # points[:, 0] += 0.5 * np.sin(step / 10.0)  # animate x-coordinates
    lines_spiral.points = points

    # Not needed in this example, it forces a strict screen refresh on every tick
    p.render()

# Explicitly initialize the interactor before adding the timer
p.iren.initialize()

# max_steps: The maximum number of times the timer callback will be called. 
p.add_timer_event(max_steps=10000, duration=25, callback=callback)


new_cpos = pv.CameraPosition(
    position=(0, 00, 8),
    focal_point=(0.02430, 0.0336, -0.02225),
    viewup=(0.0, 1.0, 0.0),
)
p.camera_position = new_cpos

p.show()