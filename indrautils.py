import numpy as np
# *** 2D affine maps ***
def rotation(theta, N=1):
    ''' Anticlockwise rotation '''
    theta = theta * N
    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])
    return R

def translation(tx, ty, N=1):
    ''' Translation by (tx, ty) '''
    tx = tx * N
    ty = ty * N
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    return T

def scale(factor, N=1):
    ''' Scaling by factor '''
    factor = factor ** N
    S = np.array([[factor, 0, 0],
                  [0, factor, 0],
                  [0, 0, 1]])
    return S
# *** Stereographic projection ***
# Sphere of diameter 1 with south pole on origin (0,0,0)
# and so north pole in (0,0,1).
# (u,v,w) are coordinates on the sphere and 
# (x,y,0) are coordinates on the plane.

def rotate_riemann_sphere_around_x_axis(u, v, w, theta):
    ''' Assuming a sphere of diameter 1 with south pole on origin (0,0,0) and north pole in (0,0,1). '''
    w = w - 0.5 # shift to center at origin
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    v_rotated = v * cos_theta - w * sin_theta
    w_rotated = v * sin_theta + w * cos_theta
    w_rotated = w_rotated + 0.5 # shift back to original position
    uvw_rotated = np.array([u, v_rotated, w_rotated])
    return uvw_rotated[0], uvw_rotated[1], uvw_rotated[2]


def mobius_transform_from_xy(x, y, a, b, c, d):
    ''' 
    Apply the Mobius transformation (az + b) / (cz + d) to points in the plane,
    where z = x + iy. Returns x,y,z - the transformed x and y coordinates in the plane, and zeros in z.
    '''
    z = x + 1j*y
    transformed_z = (a*z + b) / (c*z + d)
    return transformed_z.real, transformed_z.imag, z.imag*0

def mobius_transform_on_complex(z, a, b, c, d):
    ''' 
    Apply the Mobius transformation (az + b) / (cz + d) to points in the plane,
    where z = x + iy. Returns the transformed complex number.
    '''
    transformed_z = (a*z + b) / (c*z + d)
    return transformed_z

# Projection is drawing a straight line from the north pole to the plane and finding the intersection point,
# or drawing a straight line from the north pole through the point on the sphere and finding the intersection point with the plane.
# The equations are from page 59 in Indra's Pearls, 2002 edition.
def project_sphere_to_plane(*args):
    ''' Accepts a points object with shape (n_points, 3) or separate x,y,z arrays. Returns x,y,z - the projected x and y coordinates in the plane, and zeros in z. '''
    return_as_points = False
    if len(args) == 1:
        points = args[0]
        u, v, w = points[:, 0], points[:, 1], points[:, 2]
        return_as_points = True
    elif len(args) == 3:
        u, v, w = args
    else:
        raise ValueError("Invalid input. Provide either a single (n_points, 3) array or separate x,y,z arrays.")
    x = u / (1 - w)
    y = v / (1 - w)
    if return_as_points:
        return np.c_[x, y, np.zeros_like(x)]
    return x, y, np.zeros_like(x)

def project_plane_to_sphere(x,y):
    xy_squared_dist = x*x+y*y
    u = x / (xy_squared_dist + 1)
    v = y / (xy_squared_dist + 1)
    w = xy_squared_dist / (xy_squared_dist + 1)
    return u, v, w

# *** 2D shapes in the plane ***
def circle_on_plane(center_x, center_y, radius, n_points = 100):
    ''' Returns x and y coordinates of points on a circle in the plane. '''
    angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    x = center_x + radius * np.cos(angles)
    y = center_y + radius * np.sin(angles)
    z = np.zeros_like(x)
    return x, y, z

def square_on_plane(center_x, center_y, angle360, side_length, n_points_per_side = 100):
    ''' Returns x and y coordinates of points on a square in the plane. '''
    ''' Rotate counterclockwise by angle360 degrees and then translate to (center_x, center_y) '''
    # Start with a unit square with corners at (0,0), (1,0), (1,1), (0,1)
    x_side1 = np.linspace(0, 1, n_points_per_side, endpoint=False)
    y_side1 = np.zeros_like(x_side1)
    
    x_side2 = np.zeros_like(x_side1)
    y_side2 = np.linspace(0, 1, n_points_per_side, endpoint=False)
    
    x_side3 = np.linspace(1, 0, n_points_per_side, endpoint=False)
    y_side3 = np.ones_like(x_side3)
    
    x_side4 = np.ones_like(x_side1)
    y_side4 = np.linspace(1, 0, n_points_per_side, endpoint=True)

    x = np.concatenate([x_side1, x_side2, x_side3, x_side4])
    y = np.concatenate([y_side1, y_side2, y_side3, y_side4])
    z = np.zeros_like(x)

    # Center the square at the origin
    x = x - 0.5
    y = y - 0.5

    # Rotate the square
    angle_rad = np.deg2rad(angle360)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    x_rotated = x * cos_angle - y * sin_angle
    y_rotated = x * sin_angle + y * cos_angle

    # Scale the square to the desired side length
    x = x_rotated * side_length
    y = y_rotated * side_length

    # Translate the square to the desired center
    x = x + center_x
    y = y + center_y

    return x, y, z