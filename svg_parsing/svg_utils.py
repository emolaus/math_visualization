import xml.etree.ElementTree as ET
import numpy as np

def strlist2float(strlist):
    return [float(element) for element in strlist]

def svgcoordinate_str_to_point(svgstr):
    '''Expects something like "10.435,-21.413" 
    Returns [10.435,21.413,0]
    Note that y is flipped by this function. SVG defines y as positive down, but we want y to be positive up.
    '''
    point = strlist2float(svgstr.split(',')) + [0.0]
    point[1] = -point[1]
    return point

def svgcoordinate_str_to_numpy_point(svgstr):
    return np.array(svgcoordinate_str_to_point(svgstr), dtype=float)

def parse_paths_from_svg_root(root):
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    
    # There is a list of paths, each path has an id and a list of svgpoints.
    # This function will create two structures:
    # 1. An Nx3 numpy array of points
    # 2. A list of line segments, defined by pairs of points. This will be a list of lists of length 2, with integer indices referring to the points in the array.

    list_of_point_arrays = []
    list_of_line_segment_arrays = []
    total_points = 0
    total_line_segments = 0
    accumulated_index = 0
    for path in paths:
        id = path.attrib['id']
        svgpoints = path.attrib['d'].split(' ')
        start_command = svgpoints[0]
        if start_command != 'm' and start_command != 'M':
            raise ValueError(f'Unsupported start command in path {id}: {start_command}. Expected m or M.') 
        
        svgpoints = svgpoints[1:]
        
        pointlist = np.zeros((len(svgpoints), 3))
        line_segments = np.zeros((len(svgpoints)-1, 2), dtype=int)  
        total_points += len(svgpoints)
        total_line_segments += len(svgpoints)-1

        starting_point = svgcoordinate_str_to_numpy_point(svgpoints[0])
        pointlist = [starting_point] # python array [x,y,z]

        for i in range(1, len(svgpoints)):
            point = svgpoints[i]
            last_point = pointlist[i-1]
            xyz = []
            if point == 'h' or point == 'H' or point == 'v' or point == 'V':
                raise ValueError(f'Unsupported command in path {id}: point number {i}. v and h commands are not supported.') 
            if point == 'z' or point == 'Z':
                # z = closed path.
                xyz = starting_point
            else:
                xyz = svgcoordinate_str_to_point(point)
                if start_command == 'm':
                    # Because except for first point, 'm' command in svg means move from last point
                    xyz[0] = xyz[0] + last_point[0]
                    xyz[1] = xyz[1] + last_point[1]
            pointlist.append(xyz)
        
        line_segments = np.array([[i + accumulated_index, i + 1 + accumulated_index] for i in range(len(pointlist)-1)])

        list_of_point_arrays.append(np.array(pointlist))
        list_of_line_segment_arrays.append(line_segments)
        accumulated_index += len(pointlist)
    
    point_list = np.concatenate(list_of_point_arrays, axis=0)
    line_segment_list = np.concatenate(list_of_line_segment_arrays, axis=0) 
    return point_list, line_segment_list

def normalize_points(points_list):
    # Normalize the lines to be between 0 and 1 in the y direction, and between 0 and 1 in the x direction. 
    # We can do this by first translating the lines so that the minimum y value is at 0, and then scaling the lines so that the maximum y value is at 1. 
    # We can also scale the x values by the same factor as the y values, so that the aspect ratio of the image is preserved.
    minimums = points_list.min(axis=0)
    maximums = points_list.max(axis=0)
    x_min = minimums[0]
    y_min = minimums[1]
    x_max = maximums[0]
    y_max = maximums[1]
    divisor = y_max - y_min
    points_list[:,1] = (points_list[:,1] - y_min) / divisor
    points_list[:,0] = (points_list[:,0] - x_min) / divisor
    return points_list

def parse_svg_file(filename):
    file = open(filename)
    tree = ET.parse(file)
    root = tree.getroot()
    
    file.close()
    return root

def get_paths_as_lines(filename):
    root = parse_svg_file(filename)
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    point_list, line_segment_list = parse_paths_from_svg_root(root) 
    points_list = normalize_points(point_list)
    return point_list, line_segment_list