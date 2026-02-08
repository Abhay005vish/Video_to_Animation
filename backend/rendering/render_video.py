import json
import cv2
import numpy as np
from pathlib import Path


def render_stick_figure(pose_json_path, output_video_path, width=640, height=480, fps=30):
    with open(pose_json_path, "r") as f:
        pose_data = json.load(f)

    with open("../animation/bone_mapping.json", "r") as f:
        bones = json.load(f)["bones"]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

    for frame_key in pose_data:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        joints = pose_data[frame_key]

        points = {}

        # Draw joints
        for joint_name, coord in joints.items():
            x = int(coord["x"] * width)
            y = int(coord["y"] * height)
            points[joint_name] = (x, y)
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        # Draw bones
        for start, end in bones:
            j1 = f"joint_{start}"
            j2 = f"joint_{end}"
            if j1 in points and j2 in points:
                cv2.line(frame, points[j1], points[j2], (255, 255, 255), 2)

        out.write(frame)

    out.release()
    return str(output_video_path)
