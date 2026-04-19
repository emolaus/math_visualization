import numpy as np
import pyvista as pv
import svg_parsing.svg_utils as svg_utils

lines = svg_utils.svg_to_normalized_lines('./svg_parsing/drstickler.svg')
print('lines shape:', lines.shape)
print(lines[0])

def linesegments_to_pv_line_array(lines):
    ''' expects a numpy array of shape N,2,3
    '''
    pv_lines = []
    for i in range(lines.shape[0]):
        line = lines[i]
        start_point = line[0]
        end_point = line[1]
        print(i, 'start_point:', start_point, 'end_point:', end_point)

        line = pv.lines_from_points(np.array([start_point, end_point]), close=False)
        pv_lines.append(line)
    return pv_lines

original_dr_stickler = linesegments_to_pv_line_array(lines.copy())
lines_1 = lines.copy()
lines_2 = lines.copy()
lines_1[:,:,0] = lines_1[:,:,0] + 1
dr_stickler_1 = linesegments_to_pv_line_array(lines_1)



p = pv.Plotter()
for line in original_dr_stickler:
    p.add_mesh(line, color="black", line_width=3)
for line in dr_stickler_1:
    p.add_mesh(line, color="black", line_width=3)
p.show()