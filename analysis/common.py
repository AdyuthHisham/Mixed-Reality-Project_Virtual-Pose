"""Shared helpers. Quaternions are [w, x, y, z] unless a function says otherwise."""
import json
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation as R

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media"
METRICS = ROOT / "docs" / "metrics"

# Okabe-Ito (colour-blind safe)
BLUE, ORANGE, GREEN, VERMILION, GREY = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#888888"


def style_png(ax):
    """Mid-grey text/axes so the transparent PNG reads on light and dark pages."""
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_color(GREY)
    ax.tick_params(colors=GREY)
    ax.xaxis.label.set_color(GREY)
    ax.yaxis.label.set_color(GREY)
    ax.title.set_color(GREY)


def save_png(fig, name):
    MEDIA.mkdir(exist_ok=True)
    fig.savefig(MEDIA / name, dpi=150, transparent=True, bbox_inches="tight")


def write_metrics(name, d):
    METRICS.mkdir(parents=True, exist_ok=True)
    (METRICS / name).write_text(json.dumps(d, indent=2) + "\n")


def average_quaternion(q):
    """Markley average of [w,x,y,z] rows. Same method as Code/read_and_plot.py
    (that file imports libemg at module level, so it is re-implemented here)."""
    q = q / np.linalg.norm(q, axis=1)[:, None]
    m = (q[:, :, None] * q[:, None, :]).mean(axis=0)
    vals, vecs = np.linalg.eigh(m)
    out = vecs[:, np.argmax(vals)]
    return -out if out[0] < 0 else out


def wxyz_to_rot(q):
    q = np.atleast_2d(q)
    return R.from_quat(q[:, [1, 2, 3, 0]])


def rot_to_wxyz(r):
    return r.as_quat()[:, [3, 0, 1, 2]]


def angle_deg(r1, r2):
    return np.degrees((r1.inv() * r2).magnitude())


def synthetic_motion(t):
    """Smooth forearm-like motion: roll + pitch sweeps. Purely synthetic."""
    return R.from_euler("xyz", np.c_[40 * np.sin(0.9 * t), 30 * np.sin(0.5 * t + 1), 60 * np.sin(0.35 * t)], degrees=True)


# Fixed assumptions for the synthetic sensor (recorded in the metrics JSON)
MOUNT_EULER_DEG = (35.0, -20.0, 110.0)  # arbitrary sensor-to-world offset
NOISE_DEG = 1.0                          # per-sample orientation noise
