import numpy as np
import pyvista as pv
import svg_parsing.svg_utils as svg_utils

point_list, line_segment_list = svg_utils.get_paths_as_lines('./svg_parsing/drstickler.svg')

# A list of Dr. Sticklers, each one is a copy of the original point list, but with different transformations applied to it.
copies = []
copies.append(point_list.copy())
copies.append(point_list.copy())
copies[1] *= 2
copies[1][:,0] = (copies[1][:,0] + 1)




def linesegments_to_pv_line_array(point_list, line_segment_list):
    ''' Expects an Nx3 numpy array of points and a list of line segments, defined by pairs of points. This will be a list of lists of length 2, with integer indices referring to the points in the array.
    ''' 
    pv_lines = []
    for line in line_segment_list:
        start_index = line[0]
        end_index = line[1]
        start_point = point_list[start_index]
        end_point = point_list[end_index]

        line = pv.lines_from_points(np.array([start_point, end_point]), close=False)
        pv_lines.append(line)
    return pv_lines

def add_lines_to_plotter(pv_lines, plotter, color="black", line_width=3):
    for line in pv_lines:
        plotter.add_mesh(line, color=color, line_width=line_width)

p = pv.Plotter()
for copy in copies:
     pv_lines = linesegments_to_pv_line_array(copy, line_segment_list)
     add_lines_to_plotter(pv_lines, p, color="black", line_width=3)

p.show()

