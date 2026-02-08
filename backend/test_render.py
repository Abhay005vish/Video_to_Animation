from rendering.render_video import render_stick_figure
from pathlib import Path

VIDEO_ID = "7c06130c-e2dc-4c77-863b-de3d7cc76bed"

pose_json = Path("../storage/motion_data") / f"{VIDEO_ID}.json"
output_video = Path("../storage/outputs") / f"{VIDEO_ID}_stick.mp4"

render_stick_figure(str(pose_json), str(output_video))

print("Stick-figure video generated successfully")
