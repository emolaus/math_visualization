# from __future__ import annotations
import numpy as np
import indrautils as iu
import pyvista as pv
from PIL import Image
'''
Tricket är att inte rendera en animation. Så, gör inte p.show(), använd inte timer, utan stega fram efter varje rendering.
'''
make_movie = False

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
        img[y_start:y_end, x_start:x_end] = 0.5 + 0.5 * np.random.random()

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

def callback(step):
    points = points_plane.copy()

    a = 1 + np.cos(step / 100.0 - 0.5) + np.cos(step / 97.0 - 0.5)*1j
    b = np.cos(step / 86.3 - 0.5) + np.cos(step / 91.2 - 0.5)*1j
    c = np.cos(step / 94.3 - 0.5) + np.cos(step / 67.3 - 0.5)*1j
    d = 1 + np.cos(step / 54.3 - 0.5) + np.cos(step / 92.3 - 0.5)*1j

    mobius_transform(points, a, b, c, d)

    # points[:, 0] += 0.5 * np.sin(step / 10.0)  # animate x-coordinates
    grid_plane_fox.points = points
    warped = grid_plane_fox.warp_by_scalar('elevation', factor=0.5)
    p.add_mesh(warped, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')

    # Not needed in this example, it forces a strict screen refresh on every tick
    # p.render()
    if make_movie:
        p.write_frame()


if make_movie:
    p.open_movie("mobius_elevation_test.mp4", framerate=25)

# p.show()

if make_movie:
    for i in range(250):
        print(f"Writing frame {i}")
        callback(i+1)
        

p.close()