import numpy as np
import indrautils as iu
import pyvista as pv

points_plane = iu.square_on_plane(0, 0, 0, 1)
line_plane = pv.lines_from_points(points_plane, close=True)

p = pv.Plotter()
actor = p.add_mesh(line_plane, color="red", line_width=3)
def callback(step):
    print(f"Timer event: step {step}")
    actor.position = [step / 100.0, step / 100.0, 0]

    # Not needed in this example, it forces a strict screen refresh on every tick
    p.render()

# Explicitly initialize the interactor before adding the timer
p.iren.initialize()

# max_steps: The maximum number of times the timer callback will be called. 
p.add_timer_event(max_steps=1000, duration=50, callback=callback)

p.add_mesh(pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=3, j_size=3), style="wireframe", color="white")

p.show()