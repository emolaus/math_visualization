import numpy as np
import pyvista as pv
import indrautils as iu

p = pv.Plotter(shape=(1, 2), title="Subplots Example")
p.subplot(0, 0)
p.add_text("Plot nr 1", font_size=12)
p.subplot(0, 1)
p.add_mesh(pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=2, j_size=2, i_resolution=10, j_resolution=10), style="wireframe", color="black")
p.add_text("Clicks are recorded. Press 'a' to print clicked 3D position.", font_size=12)


def print_mouse_position():
    print("Here")
    # point = p.pick_mouse_position()
    point = p.pick_click_position()
    print(f"Mouse clicked at: {point}")

def mouse_move_callback(x, y):
    print(f"Mouse moved to: ({x}, {y})")

p.add_key_event(
    "a",  # Press 'a' to trigger the callback
    print_mouse_position
)

p.show()