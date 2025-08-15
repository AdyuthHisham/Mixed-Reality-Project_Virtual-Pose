import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from libemg import streamers
from libemg.data_handler import OnlineDataHandler
from libemg.gui import GUI
import os
from datetime import datetime
import time
import csv

def quat_to_rotation_matrix(qw, qx, qy, qz):
    R = np.array([
        [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qz*qw), 2*(qx*qz + qy*qw)],
        [2*(qx*qy + qz*qw), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qx*qw)],
        [2*(qx*qz - qy*qw), 2*(qy*qz + qx*qw), 1 - 2*(qx**2 + qy**2)]
    ])
    return R

def transform_to_global(acc, quat):
    qw, qx, qy, qz = quat
    R = quat_to_rotation_matrix(qw, qx, qy, qz)
    return np.dot(R, acc)

def integrate(data, dt):
    return np.cumsum(data) * dt

if __name__ == "__main__":
    # Create data handler and streamer
    streamer, smm = streamers.sifi_bioarmband_streamer(emg_notch_freq=50,
                                                   name="BioArmband",
                                                   ecg=False, emg=True, eda=False, imu=True, ppg=False)
    fs = 100  # Sampling frequency
    odh = OnlineDataHandler(smm)
    odh.reset()

    time.sleep(10)

    i = 0
    max_iter = 500
    # Initialize lists to store IMU data, positions, and velocities
    imu_data_all = []
    positions = []
    velocities = []
    timestamps = []
    
    # Initial values for velocity and position (zeroed)
    velocity = np.array([0, 0, 0])
    position = np.array([1, 0, 0])
    
    # Create a plot window for visualizing the position
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    # Initialize plot lines
    line_x, = ax.plot([], [], label="X Position")
    line_y, = ax.plot([], [], label="Y Position")
    line_z, = ax.plot([], [], label="Z Position")
    ax.legend(loc="best")
    ax.set_title("Object Pose Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Position (m)")
    try:
        while(i<max_iter):  # Run until manually interrupted
            # print("HALLO")
            time.sleep(0.1)  # Adjust this for the sampling rate
            data, count = odh.get_data(N=300)  # Increase the sample size as needed
            imu = data['imu']
            
            # Extract acceleration and quaternion data
            acc_data = np.vstack([imu[:,0], imu[:,1], imu[:,2]]).T  # Acceleration (Nx3)
            quat_data = np.vstack([imu[:,3], imu[:,4], imu[:,5], imu[:,6]]).T  # Quaternion (Nx4)
            


            for i in range(len(acc_data[0])):
                # Calculate global acceleration using quaternion data
                acc_global = transform_to_global(acc_data[i], quat_data[i])
                acc_global_corrected = acc_global - np.array([0, 0, 9.81])  # Remove gravity
                
                # Calculate the time step (dt) between samples
                # dt = np.diff(timestamps)[i] if i > 0 else 0.01
                dt = 0.01
                velocity = velocity + acc_global_corrected * dt  # Update velocity (integration)
                position = position + velocity * dt  # Update position (integration)
                
                # Append current position and velocity
                positions.append(position)
                velocities.append(velocity)
                timestamps.append(time.time())  # Append the current timestamp
                
                # Plotting the position in real-time
                line_x.set_data(timestamps, np.array(positions)[:, 0])
                line_y.set_data(timestamps, np.array(positions)[:, 1])
                line_z.set_data(timestamps, np.array(positions)[:, 2])
                ax.relim()
                ax.autoscale_view()
                plt.pause(0.05)

            # Append IMU data to list for later saving
            imu_data_all.append(imu)

            i += 1
    except KeyboardInterrupt:
        print("Exit command entered")

    # Convert the collected IMU data and position data to a single numpy array
    imu_data_all = np.vstack(imu_data_all)
    positions = np.array(positions)
    velocities = np.array(velocities)

    # Save IMU data and pose (position + velocity) to a CSV using pandas
    df_imu = pd.DataFrame(imu_data_all, columns=[f'Channel_{i+1}' for i in range(imu_data_all.shape[1])])
    df_pose = pd.DataFrame(positions, columns=['Pos_X', 'Pos_Y', 'Pos_Z'])
    df_velocity = pd.DataFrame(velocities, columns=['Vel_X', 'Vel_Y', 'Vel_Z'])
    df_timestamp = pd.DataFrame(timestamps, columns=['Timestamp'])
    
    df = pd.concat([df_timestamp,df_imu, df_pose, df_velocity], axis=1)

    # Create folders for data collection
    current_time = datetime.now()
    folder_name = current_time.strftime("%m%d%H%M")
    folder_path = os.path.join("Data\\orientation_test", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Data folder created at: {folder_path}")
    # Set the file path for CSV logging
    csv_file_path = os.path.join(folder_path, "test_out.csv")

    df.to_csv(csv_file_path, index=False)
