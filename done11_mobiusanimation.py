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
y = np.linspace(-1, 1, h)
xx, yy = np.meshgrid(x, y)
zz = np.zeros_like(xx)
planepoints = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
# shape of planepoints: (187200, 3)
grid_mask = pv.StructuredGrid()
# shape of grid mask points: (187200, 3)
grid_mask.points = planepoints
grid_mask.dimensions = [w, h, 1]
# Add scalar for masking
grid_mask["intensity"] = img.ravel().astype(float)

p = pv.Plotter()
actor = p.add_mesh(grid_mask, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')

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

    points = planepoints.copy()

    a = 1 + np.cos(step / 100.0 - 0.5) + np.cos(step / 97.0 - 0.5)*1j
    b = np.cos(step / 86.3 - 0.5) + np.cos(step / 91.2 - 0.5)*1j
    c = np.cos(step / 94.3 - 0.5) + np.cos(step / 67.3 - 0.5)*1j
    d = 1 + np.cos(step / 54.3 - 0.5) + np.cos(step / 92.3 - 0.5)*1j

    mobius_transform(points, a, b, c, d)

    # points[:, 0] += 0.5 * np.sin(step / 10.0)  # animate x-coordinates
    grid_mask.points = points

    # Not needed in this example, it forces a strict screen refresh on every tick
    p.render()

# Explicitly initialize the interactor before adding the timer
p.iren.initialize()

# max_steps: The maximum number of times the timer callback will be called. 
p.add_timer_event(max_steps=1000, duration=50, callback=callback)


new_cpos = pv.CameraPosition(
    position=(0, 00, 8),
    focal_point=(0.02430, 0.0336, -0.02225),
    viewup=(0.0, 1.0, 0.0),
)
p.camera_position = new_cpos

p.show()