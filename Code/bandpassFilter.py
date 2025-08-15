import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

""" Script to apply a bandpass filter to IMU data and visualize the results. """

# --- Bandpass filter functions ---
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, high, btype='low')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# --- Load CSV ---
df = pd.read_csv(r"Data/2025_7_28_11h48m19_IMU.csv")  # Replace with your CSV file path

# --- Compute sampling frequency ---
time = df['Time'].values
dt = time[1] - time[0]  # assuming uniform sampling
fs = 1 / dt

# --- Set bandpass filter parameters ---
lowcut = 0.0    # Hz
highcut = 1.0 # Hz
order = 4       # filter order

# --- Apply filter ---
df['filtered_roll'] = butter_bandpass_filter(df['roll'].values, lowcut, highcut, fs, order)
df['filtered_pitch'] = butter_bandpass_filter(df['pitch'].values, lowcut, highcut, fs, order)
df['filtered_yaw'] = butter_bandpass_filter(df['yaw'].values, lowcut, highcut, fs, order)

# --- Plot original and filtered signals ---
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, df['roll'], label='Original Roll')
plt.plot(time, df['filtered_roll'], label='Filtered Roll')
plt.ylabel('Roll (rad)')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(time, df['pitch'], label='Original Pitch', color='orange')
plt.plot(time, df['filtered_pitch'], label='Filtered Pitch', color='red')
plt.ylabel('Pitch (rad)')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(time, df['yaw'], label='Original Yaw', color='green')
plt.plot(time, df['filtered_yaw'], label='Filtered Yaw', color='lime')
plt.xlabel('Time (s)')
plt.ylabel('Yaw (rad)')
plt.legend()
plt.grid(True)

plt.suptitle("Bandpass Filtered IMU Signals")
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

df['roll'] = butter_bandpass_filter(df['roll'].values, lowcut, highcut, fs, order)
df['pitch'] = butter_bandpass_filter(df['pitch'].values, lowcut, highcut, fs, order)
df['yaw'] = butter_bandpass_filter(df['yaw'].values, lowcut, highcut, fs, order)

df.to_csv(r"Data/2025_7_28_11h48m19_IMU_filtered.csv", index=False)