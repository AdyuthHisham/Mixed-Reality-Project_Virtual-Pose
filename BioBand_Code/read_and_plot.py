import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from libemg import streamers
from libemg.data_handler import OnlineDataHandler
from scipy.spatial.transform import Rotation as R

def create_cube(size=0.4):
    """Returns 8 vertices of a cube centered at the origin"""
    d = size / 2
    return np.array([
        [-d, -d, -d],
        [+d, -d, -d],
        [+d, +d, -d],
        [-d, +d, -d],
        [-d, -d, +d],
        [+d, -d, +d],
        [+d, +d, +d],
        [-d, +d, +d]
    ])

def draw_cube(ax, vertices):
    """Draw cube using rotated vertices"""
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
        [vertices[0], vertices[3], vertices[7], vertices[4]]   # left
    ]
    colors = ['red', 'lime', 'blue', 'orange', 'purple', 'cyan']

    cube = Poly3DCollection(faces, facecolors=colors, linewidths=1, edgecolors='black', alpha=0.6)
    ax.add_collection3d(cube)

# def average_quaternion(quaternions):
#     """
#     Compute the average quaternion from a list of quaternions
#     using the method based on eigenvectors of the quaternion covariance matrix.
#     """
#     A = np.zeros((4, 4))
#     for q in quaternions:
#         q = q / np.linalg.norm(q)
#         A += np.outer(q, q)
#     A /= len(quaternions)
#     # eigenvector corresponding to largest eigenvalue is the average quaternion
#     eigenvalues, eigenvectors = np.linalg.eigh(A)
#     avg_quat = eigenvectors[:, np.argmax(eigenvalues)]
#     # Ensure scalar (w) component is positive
#     if avg_quat[0] < 0:
#         avg_quat = -avg_quat
#     return avg_quat


def average_quaternion(quaternions):
    """
    Compute the average quaternion from a list of quaternions (Markley method)
    """
    # Normalize each quaternion
    quats_norm = quaternions / np.linalg.norm(quaternions, axis=1)[:, None]

    # Equal weights
    weights = np.ones(len(quats_norm)) / len(quats_norm)

    # Build 4x4 matrix M
    M = np.zeros((4, 4))
    for w, q in zip(weights, quats_norm):
        M += w * np.outer(q, q)

    # Eigen decomposition of M
    eigenvalues, eigenvectors = np.linalg.eigh(M)
    # Eigenvector with largest eigenvalue is the average quaternion
    q_max = eigenvectors[:, np.argmax(eigenvalues)]

    # Make sure scalar part is positive (to avoid ambiguity in quaternion sign)
    if q_max[0] < 0:
        q_max = -q_max

    return q_max


if __name__ == "__main__":
    streamer, smm = streamers.sifi_bioarmband_streamer(emg_notch_freq=50,
                                                      name="BioArmband",
                                                      ecg=False, emg=True, eda=False, imu=True, ppg=False)
    fs = 100
    
    odh = OnlineDataHandler(smm)
    odh.analyze_hardware()
    
    odh.reset()
    time.sleep(2)

    print("HELLO THERE!")
    cube_vertices = create_cube()

    # --- Step 1: Collect 10 seconds of quaternion data ---
    print("Collecting 10 seconds of IMU data to compute reference orientation...")
    ref_quats = []
    start_time = time.time()
    while time.time() - start_time < 30:
        data, count = odh.get_data(N=10)
        imu = data.get('imu', None)
        if imu is None or imu.shape[0] == 0:
            continue
        quats = imu[:, 3:7]  # [w, x, y, z]
        for quat in quats:
            norm = np.linalg.norm(quat)
            if norm == 0 or np.isnan(norm):
                continue
            quat_norm = quat / norm
            ref_quats.append(quat_norm)
        time.sleep(0.01)

    if len(ref_quats) == 0:
        raise RuntimeError("No valid quaternions collected during reference period.")

    ref_quats = np.array(ref_quats)
    ref_quat = average_quaternion(ref_quats)
    print(f"Reference quaternion: {ref_quat}")

    # Reference rotation object (to rotate from local frame to global frame)
    R_ref_inv = R.from_quat([ref_quat[1], ref_quat[2], ref_quat[3], ref_quat[0]]).inv()

    # --- Step 2: Real-time visualization using ref quaternion ---
    plt.ion()
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Live IMU Orientation - Rotating Cube (Global Frame)")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    max_iter = 500
    for _ in range(max_iter):
        time.sleep(0.1)
        data, count = odh.get_data(N=20)
        imu = data.get('imu', None)
        if imu is None or imu.shape[0] == 0:
            continue

        quats = imu[:, 3:7]  # [w, x, y, z]

        for quat in quats:
            norm = np.linalg.norm(quat)
            if norm == 0 or np.isnan(norm):
                continue
            quat_norm = quat / norm
            r_local = R.from_quat([quat_norm[1], quat_norm[2], quat_norm[3], quat_norm[0]])  # [x, y, z, w]

            # Convert local quaternion to global frame
            r_global = R_ref_inv * r_local

            rotated_vertices = r_global.apply(cube_vertices)

            ax.cla()
            ax.set_title("Live IMU Orientation - Rotating Cube (Global Frame)")
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 1])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            draw_cube(ax, rotated_vertices)

             # --- Add quaternion text ---
            quat_text = f"Quat: [{quat_norm[1]:.3f}, {quat_norm[2]:.3f}, {quat_norm[3]:.3f}, {quat_norm[0]:.3f}]"
            ax.text2D(0.05, 0.95, quat_text, transform=ax.transAxes, fontsize=10, color='black')


            plt.draw()
            plt.pause(0.01)

    plt.ioff()
    print("Real-time visualization ended.")
    plt.show()
