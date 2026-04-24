import numpy as np
import pyvista as pv
import indrautils as iu
from PIL import Image

'''
Den här koden är ett exempel på hur man kan välja en punkt i det högra subplotet och använda den 
för att transformera något i vänstra subplotet. I det här fallet har jag ritat en räv i det vänstra subplotet och 
när man höger-klickar i det högra subplotet så kommer den punkten att användas som "a" i en mobius transform som appliceras på räven.
'''

p = pv.Plotter(shape=(1, 2), title="Subplots Example")
p.subplot(0, 0)
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
zz = np.zeros_like(xx)
planepoints = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
# shape of planepoints: (187200, 3)
grid_mask = pv.StructuredGrid()
# shape of grid mask points: (187200, 3)
grid_mask.points = planepoints
grid_mask.dimensions = [w, h, 1]
# Add scalar for masking
grid_mask["intensity"] = img.ravel().astype(float)

p.add_mesh(grid_mask, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')

new_cpos = pv.CameraPosition(
    position=(0, 00, 8),
    focal_point=(0.02430, 0.0336, -0.02225),
    viewup=(0.0, 1.0, 0.0),
)
p.camera_position = new_cpos

p.subplot(0, 1)
p.add_mesh(pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=2, j_size=2, i_resolution=100, j_resolution=100), style="wireframe", color="black")
p.add_text("Right-click to select the 'a' in the mobius transform", font_size=12)
new_cpos = pv.CameraPosition(
    position=(0, 00, 8),
    focal_point=(0.02430, 0.0336, -0.02225),
    viewup=(0.0, 1.0, 0.0),
)
p.camera_position = new_cpos


def print_mouse_position():
    print("Here")
    print("Camera position:", p.camera_position)

    # point = p.pick_mouse_position()
    point = p.pick_click_position()
    print(f"Mouse clicked at: {point}")

p.add_key_event(
    "a",  # Press 'a' to trigger the callback
    print_mouse_position
)

def mouse_right_click_callback(point):
    x = point[0]
    y = point[1]
    print(f"Right-clicked at: ({x}, {y})")
    p.subplot(0, 0)
    # iu.mobius_transform
    X = xx.ravel() 
    Y = yy.ravel()
    X_real, Y_imag, _ = iu.mobius_transform(X, Y, x, 0.5, 0.5, 1)
    grid_mask.points[:,0] = X_real
    grid_mask.points[:,1] = Y_imag
    p.add_mesh(grid_mask, scalars="intensity", cmap="gray", show_scalar_bar=False, name='mask')
    p.update()


p.track_click_position(mouse_right_click_callback)

p.show()