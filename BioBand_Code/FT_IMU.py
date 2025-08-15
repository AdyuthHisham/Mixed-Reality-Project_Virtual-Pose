import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Load CSV ---
df = pd.read_csv(r"Data/2025_7_28_14h6m11_IMU.csv")  # Replace with your actual file path
time = df['Time'].values
dt = time[1] - time[0]  # sampling interval (assumes uniform)
fs = 1 / dt             # sampling frequency

# --- Signals Dictionary ---
signals = {
    'Roll': df['roll'].values,
    'Pitch': df['pitch'].values,
    'Yaw': df['yaw'].values
}

# --- Setup Subplots ---
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

for idx, (label, signal) in enumerate(signals.items()):
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=dt)

    positive_freqs = freqs[:len(freqs)//2]
    magnitude = np.abs(fft_vals)[:len(freqs)//2]

    axes[idx].plot(positive_freqs, magnitude)
    axes[idx].set_title(f"FFT of {label}")
    axes[idx].set_ylabel("Magnitude")
    axes[idx].grid(True)

axes[-1].set_xlabel("Frequency (Hz)")
plt.tight_layout()
plt.show()
