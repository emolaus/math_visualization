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

h, w = 600, 1000

img = np.zeros((h,w))
print(f"Image shape: {img.shape}")

for i in range(18):
    for j in range(18):
        y_start = i * 50
        y_end = y_start + 25
        x_start = j * 50
        x_end = x_start + 25
        img[y_start:y_end, x_start:x_end] = 0.2 + 0.8 * np.random.random()



# Grid in plane
x = np.linspace(-1, 1, w)
y = np.linspace(-1, 1, h)
xx, yy = np.meshgrid(x, y)

points_plane = np.c_[xx.ravel(), yy.ravel(), np.zeros_like(xx).ravel()]
grid_plane_fox = pv.StructuredGrid()
grid_plane_fox.points = points_plane
grid_plane_fox.dimensions = [w,h,1]

# Add scalar for masking
grid_plane_fox["intensity"] = img.ravel().astype(float)
grid_plane_fox["elevation"] = img.ravel().astype(float)
warped = grid_plane_fox.warp_by_scalar('elevation', factor=0.5)

p = pv.Plotter()
p.add_mesh(warped, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')

def mobius_transform(points, a, b, c, d):
    '''Apply a Möbius transformation to a set of points directly in the points array.'''
    x = points[:, 0]
    y = points[:, 1]
    z0 = x + 1j * y
    z1 = (a * z0 + b) / (c * z0 + d)
    points[:, 0] = z1.real
    points[:, 1] = z1.imag

max_steps = 250
duration = 100  # milliseconds between timer events
def callback(step):
    print(f"Timer event: step {step}")
    # This works
    # actor.position = [step / 100.0, step / 100.0, 0]

    points = points_plane.copy()

    seconds = step * duration / 1000.0  # convert to seconds for smoother animation 
    radians = seconds * 2 * np.pi  # convert to radians for smooth periodic motion

    ### Möbius transformation with time-varying parameters
    t = radians/5.0
    a = 1 + np.sin(t*0.11) + np.sin(t*0.23)*1j
    b = np.sin(t*0.05) + np.sin(t*0.17)*1j
    c = np.sin(t*0.29) + np.sin(t*0.09)*1j
    d = 1 + np.sin(t*0.151) + np.sin(t*0.37)*1j
    mobius_transform(points, a, b, c, d)

    # Animated waves on elevation
    img1 = img.copy()
    for i in range(w):
        t1 = i / w * 2 * np.pi + t  # add time component for animation
        img1[:, i] += 0.2 * np.sin(t1*2)

    ### Swirling transformation
    # t = radians/10.0
    # theta = 0.3
    # z0 = (points[:, 0]*t + 1j * points[:, 1]*t)*(np.cos(theta) + 1j * np.sin(theta))
    # z1 = np.exp(z0)
    # points[:, 0] = z1.real
    # points[:, 1] = z1.imag

    # points[:, 0] += 0.5 * np.sin(step / 10.0)  # animate x-coordinates
    grid_plane_fox.points = points
    grid_plane_fox["elevation"] = img1.ravel().astype(float)
    warped = grid_plane_fox.warp_by_scalar('elevation', factor=0.5)
    p.add_mesh(warped, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')

    # Not needed in this example, it forces a strict screen refresh on every tick
    p.render()

# Explicitly initialize the interactor before adding the timer
p.iren.initialize()

# max_steps: The maximum number of times the timer callback will be called. 
p.add_timer_event(max_steps=max_steps, duration=duration, callback=callback)


p.show()
