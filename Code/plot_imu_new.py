import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

# --- Load CSV ---
df = pd.read_csv(r"Data/2025_8_7_12h11m2_IMU.csv")  # Replace with your actual filename

# --- Normalize quaternions if needed ---
quats = df[['quat_w', 'quat_x', 'quat_y', 'quat_z']].to_numpy()
norms = np.linalg.norm(quats, axis=1)
quats = quats / norms[:, None]

# Convert ONE quaternion to rotation matrix (e.g., index 1)
w, x, y, z = quats[5]  # or any other index
r = R.from_quat([x, y, z, w])  # Note: SciPy expects [x, y, z, w]
R_matrix = r.as_matrix()
print("Rotation Matrix:\n", R_matrix)
# # --- Plot 1: Quaternions as 3D vectors (orientation) ---
# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_title("Orientation (Quaternion as vector)")

# quats_xyzw = df[["quat_x", "quat_y", "quat_z", "quat_w"]].to_numpy()
# # Convert quaternion to rotation vectors
# rot = R.from_quat(quats_xyzw)  # scipy expects [x, y, z, w]
# vectors = rot.apply(np.tile([1, 0, 0], (len(quats), 1)))  # Show orientation of x-axis

# for i in range(0, len(df), max(1, len(df) // 20)):  # Reduce points for clarity
#     ax.quiver(0, 0, 0, vectors[i, 0], vectors[i, 1], vectors[i, 2], length=0.5, normalize=True)

# ax.set_xlim([-1, 1])
# ax.set_ylim([-1, 1])
# ax.set_zlim([-1, 1])

# # --- Roll Plot ---
# plt.figure(figsize=(8, 4))
# plt.plot(df['Time'].values, df['roll'].values, label='Roll')
# plt.xlabel("Time (s)")
# plt.ylabel("Roll (rad)")
# plt.title("Roll Over Time")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # --- Pitch Plot ---
# plt.figure(figsize=(8, 4))
# plt.plot(df['Time'].values, df['pitch'].values, label='Pitch', color='orange')
# plt.xlabel("Time (s)")
# plt.ylabel("Pitch (rad)")
# plt.title("Pitch Over Time")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # --- Yaw Plot ---
# plt.figure(figsize=(8, 4))
# plt.plot(df['Time'].values, df['yaw'].values, label='Yaw', color='green')
# plt.xlabel("Time (s)")
# plt.ylabel("Yaw (rad)")
# plt.title("Yaw Over Time")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# --- Plot 3: Acceleration ---
fig3, axes_acc = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
for ax in axes_acc:
    ax.set_ylim(-2, 2.5)
    ax.grid(True)

axes_acc[0].plot(df['Time'].values, df['accel_x'].values, label='Accel X')
axes_acc[1].plot(df['Time'].values, df['accel_y'].values, label='Accel Y', color='purple')
axes_acc[2].plot(df['Time'].values, df['accel_z'].values, label='Accel Z', color='brown')

axes_acc[0].set_ylabel("X (m/s²)")
axes_acc[1].set_ylabel("Y (m/s²)")
axes_acc[2].set_ylabel("Z (m/s²)")
axes_acc[2].set_xlabel("Time (s)")
fig3.suptitle("Acceleration Over Time")

plt.tight_layout()
plt.show()

# Exclude the first 15 rows for stats calculation
accel_x_mean = df['accel_x'][10:].mean()
accel_x_std = df['accel_x'][10:].std()

accel_y_mean = df['accel_y'][10:].mean()
accel_y_std = df['accel_y'][10:].std()

accel_z_mean = df['accel_z'][10:].mean()
accel_z_std = df['accel_z'][10:].std()

# Normalize all rows using mean/std from row 15 onward
df['accel_x_norm'] = (df['accel_x'][10:] - accel_x_mean) / accel_x_std
df['accel_y_norm'] = (df['accel_y'][10:] - accel_y_mean) / accel_y_std
df['accel_z_norm'] = (df['accel_z'][10:] - accel_z_mean) / accel_z_std

fig3, axes_acc = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
for ax in axes_acc:
    ax.grid(True)

axes_acc[0].plot(df['Time'].values[10:], df['accel_x_norm'].values[10:], label='Accel X (norm)')
axes_acc[1].plot(df['Time'].values[10:], df['accel_y_norm'].values[10:], label='Accel Y (norm)', color='purple')
axes_acc[2].plot(df['Time'].values[10:], df['accel_z_norm'].values[10:], label='Accel Z (norm)', color='brown')

axes_acc[0].set_ylabel("X (norm)")
axes_acc[1].set_ylabel("Y (norm)")
axes_acc[2].set_ylabel("Z (norm)")
axes_acc[2].set_xlabel("Time (s)")
fig3.suptitle("Normalized Acceleration Over Time (Excluding First 30 Samples)")

plt.tight_layout()
plt.show()