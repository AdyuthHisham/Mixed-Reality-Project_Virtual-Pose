import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R
from matplotlib.animation import FuncAnimation

"""
Script to read generated IMU data from a CSV file and animate a cube in 3D space.
The cube's orientation is updated based on roll, pitch, and yaw values from the CSV.
"""

# --- Load Data ---
df = pd.read_csv(r"Data/2025_7_28_11h48m19_IMU_filtered.csv")
roll = df['roll'].to_numpy()
pitch = df['pitch'].to_numpy()
yaw = df['yaw'].to_numpy()
time = df['Time'].to_numpy()

# --- Cube Geometry ---
def get_cube():
    points = np.array([
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [-0.5,  0.5, -0.5],
        [-0.5,  0.5,  0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5, -0.5],
        [ 0.5,  0.5,  0.5]
    ])
    return points

# --- Setup Plot ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
title = ax.set_title("")

cube_points = get_cube()
# Initial faces (ordered as before)
face_indices = [
    [0,1,3,2],  # -X
    [4,5,7,6],  # +X
    [0,1,5,4],  # -Y
    [2,3,7,6],  # +Y
    [0,2,6,4],  # -Z
    [1,3,7,5],  # +Z (FRONT FACE)
]

# Initial face vertices
faces = [[cube_points[i] for i in face] for face in face_indices]
# Define face colors: front face is red, others are cyan
face_colors = ['cyan', 'red', 'cyan', 'cyan', 'cyan', 'cyan']


cube_collection = Poly3DCollection(faces, facecolors=face_colors, edgecolors='black', alpha=0.7)
ax.add_collection3d(cube_collection)

# --- Update Function ---
def update(frame):
    r = R.from_euler('xyz', [roll[frame], pitch[frame], yaw[frame]], degrees=False)
    rotated_points = r.apply(get_cube())

    # Rotate all faces
    new_faces = [[rotated_points[i] for i in face] for face in face_indices]
    cube_collection.set_verts(new_faces)

    title.set_text(f"Time: {time[frame]:.2f}s")
    return cube_collection, title

# --- Run Animation ---
ani = FuncAnimation(fig, update, frames=len(roll), interval=10, blit=False)
plt.show()
