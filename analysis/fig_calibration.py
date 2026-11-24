"""Synthetic check of the calibration step in Code/read_and_plot.py:
average a rest period, then r_global = inv(r_ref) * r_local.
The sensor is simulated (fixed mounting offset + noise); no real recording is used."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from common import *

rng = np.random.default_rng(0)
fs, rest_s, move_s = 100, 10, 20
t = np.arange(0, rest_s + move_s, 1 / fs)
moving = t >= rest_s
truth = R.identity(len(t))
truth = R.from_quat(np.where(moving[:, None], synthetic_motion(np.where(moving, t - rest_s, 0)).as_quat(), [0, 0, 0, 1]))
mount = R.from_euler("xyz", MOUNT_EULER_DEG, degrees=True)
noise = R.from_rotvec(np.radians(NOISE_DEG) * rng.standard_normal((len(t), 3)) / np.sqrt(3))
local = mount * truth * noise

ref = average_quaternion(rot_to_wxyz(local[: rest_s * fs]))
glob = wxyz_to_rot(ref).inv() * local
err_raw, err_cal = angle_deg(truth, local), angle_deg(truth, glob)

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(t, err_raw, color=VERMILION, lw=1.2, label="raw sensor quaternion")
ax.plot(t, err_cal, color=BLUE, lw=1.2, label="after rest-pose calibration")
ax.axvline(rest_s, color=GREY, ls=":")
ax.text(rest_s + 0.3, ax.get_ylim()[1] * 0.9, "motion starts", color=GREY, fontsize=8)
ax.set(xlabel="time (s)", ylabel="angle to true orientation (deg)", title="Synthetic sensor: error before and after calibration")
style_png(ax)
leg = ax.legend(frameon=False)
for tx in leg.get_texts():
    tx.set_color(GREY)
save_png(fig, "calibration_error.png")

write_metrics("calibration.json", {
    "synthetic": True, "seed": 0, "mount_euler_deg": MOUNT_EULER_DEG, "noise_deg": NOISE_DEG,
    "rest_s": rest_s, "move_s": move_s, "fs_hz": fs,
    "median_error_raw_deg": round(float(np.median(err_raw[moving])), 2),
    "median_error_calibrated_deg": round(float(np.median(err_cal[moving])), 2),
})
