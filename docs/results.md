# Results, data sources and known mismatches

Nothing here comes from a recorded dataset: the repo contains no IMU recordings. Every number below is produced by a script in `analysis/` and written to `docs/metrics/`.

| Figure / claim | Source | Notes |
|---|---|---|
| `media/pipeline.svg` | `analysis/fig_pipeline.py` | Drawn from `Code/UDPSender.py` and `Assets/UserScripts/UDPReceiver.cs` (port 9050, 20 Hz). |
| `media/calibration_error.png`, `docs/metrics/calibration.json` | `analysis/fig_calibration.py` | **Synthetic sensor.** Fixed mounting offset (35, -20, 110 deg), 1 deg noise, 10 s rest then 20 s motion, seed 0. Checks that the rest-pose averaging in `Code/read_and_plot.py` removes a fixed offset. It does not test drift or real armband behaviour. |
| `media/quat_order_error.png`, `docs/metrics/quat_order.json` | `analysis/fig_quat_order.py` | Arithmetic on 2000 random rotations (seed 0), mirroring the parsing in `UDPReceiver.cs`. Not tested on the headset. |
| `media/hero.gif` | `analysis/hero_gif.py` | Synthetic motion, ideal calibration. Illustration only. |
| `media/passthrough_clip.gif` | `make clip` (ffmpeg) | First 4 s of `Documentation/Documents/oculus_cast_video_*.mp4`, a Quest casting recording. |

## Mismatches and open issues

1. **Quaternion component order.** `UDPSender.py` sends `w,x,y,z`. `UDPReceiver.cs` reads the four numbers as `x,y,z,w`, then applies `(-y, x, z, w)`. By arithmetic this shows the neutral pose as a 180 deg rotation and gives a median error of about 151 deg over random rotations (`quat_order.json`). This has not been checked on hardware, and the source files are unchanged. It may be part of why the orientation was hard to align.
2. **Local-to-global conversion** (`read_and_plot.py`) works on synthetic data with a fixed offset. On the real armband the project notes say it did not align reliably; the cause was not found.
3. **Root pose only.** `CustomSkeletonModifier` overrides joint poses from a dictionary that is empty in the committed version; the UDP data is not yet wired into `OVRSkeleton`.
4. **Position estimation** (`pose_estimation_online.py`, double integration of acceleration) was not completed.
5. `OVRSkeleton_paste.cs` is Meta's `OVRSkeleton.cs` with our `CustomSkeletonModifier` added; Meta's licence (`LICENSE.txt`) applies to the SDK parts.
