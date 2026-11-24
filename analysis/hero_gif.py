"""media/hero.gif: synthetic sensor, raw quaternion vs calibrated. Labelled synthetic in the title."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R
from common import *

d = 0.5
V = np.array([[sx * d, sy * d * 0.6, sz * d * 1.6] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])  # forearm-like box
F = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
rng = np.random.default_rng(0)
t = np.linspace(0, 8, 120)
truth = synthetic_motion(t)
mount = R.from_euler("xyz", MOUNT_EULER_DEG, degrees=True)
raw = mount * truth
cal = mount.inv() * raw  # ideal calibration; see calibration_error.png for the noisy case

fig = plt.figure(figsize=(7.5, 3.6), dpi=70, facecolor="#f6f7f9")
axes = [fig.add_subplot(1, 2, i + 1, projection="3d", facecolor="#f6f7f9") for i in range(2)]
titles = ["raw sensor frame", "after calibration"]
cols = [VERMILION, BLUE]

def draw(i):
    for ax, rot, ttl, c in zip(axes, (raw, cal), titles, cols):
        ax.cla()
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
        ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])
        ax.set_title(ttl, color="#222", fontsize=11)
        v = rot[i].apply(V)
        ax.add_collection3d(Poly3DCollection([v[f] for f in F], facecolors=c, edgecolors="#222", alpha=0.7))
    fig.suptitle("Synthetic IMU input (not recorded data)", color="#444", fontsize=9, y=0.98)

FuncAnimation(fig, draw, frames=len(t)).save(MEDIA / "hero.gif", writer=PillowWriter(fps=15))
