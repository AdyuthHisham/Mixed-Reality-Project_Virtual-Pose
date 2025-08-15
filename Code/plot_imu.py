import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

# Sample IMU data (Replace with your actual IMU data)
# Quaternion (w, x, y, z) and acceleration vector (ax, ay, az)
quaternion = np.array([0.7071, 0.0, 0.7071, 0.0])  # Example quaternion (w, x, y, z)
acceleration_sensor_frame = np.array([0.0, 0.0, -9.81])  # Example acceleration (m/s^2)

# Convert quaternion to a rotation matrix
r = R.from_quat(quaternion)  # Convert quaternion to rotation object
rotation_matrix = r.as_matrix()  # Get rotation matrix
print(rotation_matrix)

# Transform the acceleration vector from the sensor frame to the global frame
acceleration_global_frame = rotation_matrix.dot(acceleration_sensor_frame)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the sensor frame acceleration vector
ax.quiver(0, 0, 0, acceleration_sensor_frame[0], acceleration_sensor_frame[1], acceleration_sensor_frame[2],
          color='b', label='Sensor Frame Acceleration')

# Plot the global frame acceleration vector
ax.quiver(0, 0, 0, acceleration_global_frame[0], acceleration_global_frame[1], acceleration_global_frame[2],
          color='r', label='Global Frame Acceleration')

# Set the labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set plot limits
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

# Add a legend
ax.legend()

# Show plot
plt.show()
