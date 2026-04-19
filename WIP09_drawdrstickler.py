import numpy as np
import pyvista as pv
import svg_parsing.svg_utils as svg_utils

lines = svg_utils.svg_to_normalized_lines('./svg_parsing/drstickler.svg')
print('lines shape:', lines.shape)
print(lines[0])
pv_lines = []

for i in range(lines.shape[0]):
    line = lines[i]
    start_point = line[0]
    end_point = line[1]
    # start_point[1] = -start_point[1]
    # end_point[1] = -end_point[1]
    print(i, 'start_point:', start_point, 'end_point:', end_point)

    line = pv.lines_from_points(np.array([start_point, end_point]), close=False)
    pv_lines.append(line)

p = pv.Plotter()
for line in pv_lines:
    p.add_mesh(line, color="black", line_width=3)
p.show()