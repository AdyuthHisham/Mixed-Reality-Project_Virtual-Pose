PY ?= python
VIDEO := Documentation/Documents/oculus_cast_video_07_04_2025_13_33_07.mp4

.PHONY: figures clip
figures:
	$(PY) analysis/fig_pipeline.py
	$(PY) analysis/fig_calibration.py
	$(PY) analysis/fig_quat_order.py
	$(PY) analysis/hero_gif.py

# Needs ffmpeg. Cuts the first 4 s of the Quest passthrough recording.
clip:
	ffmpeg -y -v error -ss 0 -t 4 -i $(VIDEO) \
	  -vf "fps=8,scale=400:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" media/passthrough_clip.gif
