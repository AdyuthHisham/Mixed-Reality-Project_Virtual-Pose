"""Component-order check between Code/UDPSender.py and Assets/UserScripts/UDPReceiver.cs.
Sender writes "w,x,y,z". Receiver reads the four numbers as x,y,z,w and then remaps
(-y, x, z, w). We compare that against the same remap applied with the correct order.
Pure arithmetic on random rotations (seed 0); no hardware involved."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from common import *

def recv(parts):  # parts = numbers in message order; mirrors UDPReceiver.cs
    qx, qy, qz, qw = parts.T
    return R.from_quat(np.c_[-qy, qx, qz, qw])

rng = np.random.default_rng(0)
true = R.random(2000, random_state=0)
w, x, y, z = rot_to_wxyz(true).T
sent = np.c_[w, x, y, z]
actual = recv(sent)                       # what the code does
intended = recv(np.c_[x, y, z, w])        # same remap, correct order
err = angle_deg(intended, actual)
size = np.degrees(true.magnitude())

fig, ax = plt.subplots(figsize=(6, 3.2))
ax.scatter(size, err, s=5, color=VERMILION, alpha=0.5)
ax.set(xlabel="rotation size of the sensor (deg)", ylabel="error shown in Unity (deg)",
       title="Sent as w,x,y,z but parsed as x,y,z,w")
style_png(ax)
save_png(fig, "quat_order_error.png")

ident = recv(np.array([[1.0, 0, 0, 0]]))
write_metrics("quat_order.json", {
    "n_random_rotations": 2000, "seed": 0,
    "median_error_deg": round(float(np.median(err)), 1),
    "max_error_deg": round(float(err.max()), 1),
    "identity_pose_shown_as_deg_from_identity": round(float(np.degrees(ident.magnitude())[0]), 1),
})
