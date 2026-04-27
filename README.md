# Math visualizations
I've started with the book Indra's Pearls and decided to go with pyvista for visualizations.

## Current plan
pyvista uses a funny-looking matrix that I will use for the util API:
>>> x = np.arange(5)
>>> y = np.arange(5)+5
>>> z = np.arange(5)+10
>>> x = np.arange(3)   
>>> y = np.arange(3)+3 
>>> z = np.arange(3)+6 
>>> points = np.c_[x,y,z]
>>> points
array([[0, 3, 6],
       [1, 4, 7],
       [2, 5, 8]])

so x is for example points[:,0]

## TODO
Update indrautils.py
- project_sphere_to_plane -> return z as well

Update existing examples

# branch better_architecture
I want to find a better way to structure test code.
- reusable animations
- animate or make video by parameter passing