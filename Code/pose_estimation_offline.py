import numpy as np
import os
from datetime import datetime
import pandas as pd

def quat_to_rotation_matrix(qw, qx, qy, qz):
    R = np.array([
        [1 - 2 * (qy**2 + qz**2), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx**2 + qz**2), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx**2 + qy**2)]
    ])
    return R

def transform_to_global(acc, quat):
    qw, qx, qy, qz = quat
    R = quat_to_rotation_matrix(qw, qx, qy, qz)
    return np.dot(R, acc)

def integrate(data, dt):
    return np.cumsum(data) * dt

if __name__ == "__main__":
    # Sampling frequency
    fs = 100  # Sampling frequency
    dt = 1 / fs  # Time step

    # Load IMU data from a space-delimited file into a NumPy array
    csv_file_path = "Data\\orientation_train\\12172308\\imu.csv"  # Update with the path to your CSV file
    imu_data = np.loadtxt(csv_file_path, delimiter=' ')

    # Split IMU data into acceleration and quaternion parts
    acc_data = imu_data[:, 0:3]  # Columns 0-2: Acceleration
    quat_data = imu_data[:, 3:7]  # Columns 3-6: Quaternion

    # Initialize lists to store positions and velocities
    positions = []
    velocities = []
    timestamps = []

    # Initial values for velocity and position
    velocity = np.array([0.0, 0.0, 0.0])
    position = np.array([1.0, 0.0, 0.0])

    # Implement ref_acc as the average of the first 50 acceleration samples
    ref_acc = np.mean(acc_data[:50], axis=0)

    try:
        for i in range(len(acc_data)):
            # Calculate global acceleration using quaternion data
            acc_global = transform_to_global(acc_data[i], quat_data[i])
            acc_global_corrected = acc_global - ref_acc  # Remove gravity

            # Update velocity and position
            velocity = velocity + acc_global_corrected * dt
            position = position + velocity * dt

            # Append current position, velocity, and timestamp
            positions.append(position.copy())
            velocities.append(velocity.copy())
            timestamps.append(i * dt)  # Simulated timestamps based on sampling rate

    except KeyboardInterrupt:
        print("Execution interrupted by user")

    # Convert collected data to numpy arrays
    positions = np.array(positions)
    velocities = np.array(velocities)
    timestamps = np.array(timestamps)

    # Prepare data for saving
    output_data = np.column_stack((timestamps, positions, velocities))
    current_time = datetime.now()
    folder_name = current_time.strftime("%m%d%H%M")
    folder_path = os.path.join("Data/orientation_test", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    output_file_path = os.path.join(folder_path, "processed_data.csv")

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(output_data, columns=["Timestamp", "Pos_X", "Pos_Y", "Pos_Z", "Vel_X", "Vel_Y", "Vel_Z"])
    df.to_csv(output_file_path, index=False)

    print(f"Processed data saved to: {output_file_path}")
