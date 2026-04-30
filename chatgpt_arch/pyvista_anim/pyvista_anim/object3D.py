import pyvista as pv
import numpy as np
'''
An object is a single pyvista mesh like PolyData or StructuredGrid.   
They must have a points array.

A group is a collection of objects that should be manipulated together.
A group shares two np arrays: all_base_points and all_points.  Each object in the group has a view into those arrays, 
so manipulating all_points will affect all objects in the group.
'''
def normalize_points(points, scale_factor = 1.0, axis = 0):
    '''
    Move the points so that it fits the first quadrant and normalize to a given axis (default x).
    Optionally apply a uniform scale factor to all points.
    '''
    points *= scale_factor

    points[:,0] -= points[:,0].min()
    points[:,1] -= points[:,1].min()
    points[:,2] -= points[:,2].min()

    d = points[:,axis].max()
    points[:,0] /= d
    points[:,1] /= d
    points[:,2] /= d

class Object3D:
    def __init__(self, mesh: pv.DataSet):
        self.mesh = mesh
        self.base_points = mesh.points.copy()
        self.points = mesh.points

class Group3D:

    multiblock: pv.MultiBlock
    all_base_points: np.ndarray
    all_points: np.ndarray
    name: str # Used by the Renderer to identify the mesh in the plotter.

    def __init__(self, meshes: list[Object3D]):
        self.multiblock = pv.MultiBlock([mesh.mesh for mesh in meshes])

    def append(self, mesh: Object3D):
        if hasattr(self, "all_base_points"):
            raise ValueError("Cannot append to group after all_base_points has been generated.")
        self.multiblock.append(mesh.mesh)

    def generate_all_points(self):
        self.all_base_points = np.concatenate([mesh.points.copy() for mesh in self.multiblock], axis=0)
        self.all_points = self.all_base_points.copy()
        current_index = 0
        for block in self.multiblock:
            num_points = block.points.shape[0]
            block.points = self.all_points[current_index:current_index+num_points]
            current_index += num_points

    def plot(self):
        self.multiblock.plot()

