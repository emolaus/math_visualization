import xml.etree.ElementTree as ET
import numpy as np

def strlist2float(strlist):
    return [float(element) for element in strlist]

def svgcoordinate_str_to_point(svgstr):
    '''Expects something like "10.435,-21.413" 
    Returns [10.435,21.413,0]
    Note that y is flipped.
    '''
    point = strlist2float(svgstr.split(',')) + [0.0]
    point[1] = -point[1]
    return point

def line_segments_from_paths(paths):
    # Pairwise list of line endsvgpoints
    lines = []
    ''' Expects path data to be in the form of a list of svgpoints, with no curves. 
    Such as
    d="m 143.86517,100.11236 -0.74158,46.34831 -13.16292,10.9382 -5.19101,12.79214 -7.60112,-4.26405"
    or 
    d="M 143.86517,100.11236 -0.74158,46.34831 -13.16292,10.9382 -5.19101,12.79214 -7.60112,-4.26405 z"
    
    m means move relative to previous point
    M means move to absolute position
    '''
    for path in paths:
        id = path.attrib['id']
        # print('parsing path',id)
        svgpoints = path.attrib['d'].split(' ')
        start_command = svgpoints[0]
        svgpoints = svgpoints[1:]
        
        starting_point = svgcoordinate_str_to_point(svgpoints[0])

        # this will be a list of lists of length 2, where each inner list is a point [x,y]
        pointlist = [starting_point]

        y_min = 1000000
        y_max = -1000000
        x_min = 100000
        for i in range(1, len(svgpoints)):
            point = svgpoints[i]
            last_point = pointlist[i-1]
            xyz = []
            if point == 'h' or point == 'H' or point == 'v' or point == 'V':
                print(id,'contains a curve command, which is not supported. Skipping path.')
                break
            if point == 'z' or point == 'Z':
                # z = closed path.
                print("closed path")
                xyz = starting_point
            else:
                xyz = svgcoordinate_str_to_point(point)

                if start_command == 'm':
                    # Because except for first point, 'm' command in svg means move from last point
                    xyz[0] = xyz[0] + last_point[0]
                    xyz[1] = xyz[1] + last_point[1]
                x = xyz[0]
                y = xyz[1]
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
                if x < x_min:
                    x_min = x

            pointlist.append(xyz)

        for i in range(len(pointlist)-1):
            lines.append([pointlist[i], pointlist[i+1]])

    lines = np.array(lines).astype(float)
    return lines, x_min, y_min, y_max

def normalize_lines(lines, x_min, y_min, y_max):
    # Normalize the lines to be between 0 and 1 in the y direction, and between 0 and 1 in the x direction. 
    # We can do this by first translating the lines so that the minimum y value is at 0, and then scaling the lines so that the maximum y value is at 1. 
    # We can also scale the x values by the same factor as the y values, so that the aspect ratio of the image is preserved.
    lines[:,:,1] = (lines[:,:,1] - y_min) / (y_max - y_min)
    lines[:,:,0] = (lines[:,:,0] - x_min) / (y_max - y_min)
    return lines

def parse_svg_file(filename):
    file = open(filename)
    tree = ET.parse(file)
    root = tree.getroot()
    
    file.close()
    return root

def svg_to_normalized_lines(filename):
    root = parse_svg_file(filename)
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    lines, x_min, y_min, y_max = line_segments_from_paths(paths)
    lines = normalize_lines(lines, x_min, y_min, y_max)
    return lines

def svg_to_lines(filename):
    root = parse_svg_file(filename)
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    lines, x_min, y_min, y_max = line_segments_from_paths(paths)
    return lines