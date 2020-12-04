import numpy as np
import matplotlib.pyplot as plt

def plot_poses(poses, subind, show=False):
    ax = plt.subplot(subind, adjustable='datalim', aspect='equal')
    xmin, xmax, ymin, ymax = (0, 0, 0, 0)
    for pose in poses:
        x, y, theta = pose.get_params()
        draw_pose(ax, x, y, theta)
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

    plt.plot([0, 0], [0, 1], 'r')
    plt.plot([0, 1], [0, 0], 'r')
    plt.xlim(np.round(xmin)-1, np.round(xmax)+1)
    plt.ylim(np.round(ymin)-1, np.round(ymax)+1)
    plt.grid(True)
    if show:
        plt.show()

def draw_pose(ax, x, y, theta):
    radius = 0.5
    circle = plt.Circle((x, y), radius, color='k', fill=False)
    ax.add_patch(circle)
    ax.arrow(x, y, radius*np.cos(theta), radius*np.sin(theta),
             width=0.1, head_length=0.2, length_includes_head=True)

def plot_point(point):
    plt.plot(point[0], point[1], 'ro')