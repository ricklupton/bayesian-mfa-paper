import matplotlib.tri as tri
import numpy as np
import matplotlib.pyplot as plt

_corners = np.array([[0, 0], [1, 0], [0.5, 0.75**0.5]])
_triangle = tri.Triangulation(_corners[:, 0], _corners[:, 1])

# Mid-points of triangle sides opposite of each corner
midpoints = [(_corners[(i + 1) % 3] + _corners[(i + 2) % 3]) / 2.0 \
             for i in range(3)]
def xy2bc(xy, tol=1.e-3):
    '''Converts 2D Cartesian coordinates to barycentric.'''
    s = [(_corners[i] - midpoints[i]).dot(xy - midpoints[i]) / 0.75 \
         for i in range(3)]
    return np.clip(s, tol, 1.0 - tol)

def plot_points(X, barycentric=True, border=True, ax=None, labels=None,
                **kwargs):
    '''Plots a set of points in the simplex.
    Arguments:
        `X` (ndarray): A 2xN array (if in Cartesian coords) or 3xN array
                       (if in barycentric coords) of points to plot.
        `barycentric` (bool): Indicates if `X` is in barycentric coords.
        `border` (bool): If True, the simplex border is drawn.
        kwargs: Keyword args passed on to `plt.plot`.
    '''
    if ax is None:
        fig, ax = plt.subplots()
    if barycentric is True:
        X = X.dot(_corners)
    kwargs.setdefault('alpha', 0.8)
    kwargs.setdefault('ms', 3)
    ax.plot(X[:, 0], X[:, 1], 'k.', **kwargs)
    ax.axis('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.75**0.5)
    ax.axis('off')
    if labels is not None:
        alignments = [('bottom', 'right'), ('bottom', 'left'), ('bottom', 'center')]
        for (x, y), (va, ha), label in zip(_corners, alignments, labels):
            ax.text(x, y, label, transform=ax.transAxes, ha=ha, va=va)
    if border is True:
        # ax.hold(1)
        ax.triplot(_triangle, linewidth=1)
