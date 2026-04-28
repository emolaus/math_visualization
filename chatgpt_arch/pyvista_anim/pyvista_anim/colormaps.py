import numpy as np
from matplotlib.colors import ListedColormap

def happy_colormap(min: float = 0.0, max: float = 1.0) -> ListedColormap:
    """Make a colormap that goes from blue to grey to yellow to red."""
    blue = np.array([12, 238, 246, 256.0])/256.0
    black = np.array([11, 11, 11, 256.0])/256.0
    grey = np.array([189, 189, 189, 256.0])/256.0
    yellow = np.array([255, 247, 0, 256.0])/256.0
    red = np.array([256.0, 0.0, 0.0, 256.0])/256.0

    mapping = np.linspace(0.0, 1.0, 256)
    newcolors = np.empty((256, 4))
    newcolors[mapping >= 0.8] = red
    newcolors[mapping < 0.8] = grey
    newcolors[mapping < 0.55] = yellow
    newcolors[mapping < 0.3] = blue
    newcolors[mapping < 0.01] = grey

    return ListedColormap(newcolors)