import json
import cv2
import numpy as np
from pathlib import Path


def render_stick_figure(pose_json_path, output_video_path, width=640, height=480, fps=30):
    """
    Render stick figure animation from pose JSON.
    """

    # -----------------------------------
    # Resolve project base directory
    # -----------------------------------
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load bone mapping safely
    bone_path = BASE_DIR / "animation" / "bone_mapping.json"
    if not bone_path.exists():
        raise FileNotFoundError(f"bone_mapping.json not found at {bone_path}")

    # Load pose data
    pose_json_path = Path(pose_json_path)
    if not pose_json_path.exists():
        raise FileNotFoundError(f"Pose JSON not found at {pose_json_path}")

    with open(pose_json_path, "r") as f:
        pose_data = json.load(f)

    with open(bone_path, "r") as f:
        bones = json.load(f)["bones"]

    # -----------------------------------
    # Prepare output video writer
    # -----------------------------------
    output_video_path = Path(output_video_path)
    output_video_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        str(output_video_path),
        fourcc,
        fps,
        (width, height)
    )

    # -----------------------------------
    # Render frame by frame
    # -----------------------------------
    for frame_key in sorted(pose_data.keys(), key=lambda x: int(x.split("_")[1])):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        joints = pose_data[frame_key]
        points = {}

        # Draw joints
        for joint_name, coord in joints.items():
            if "x" not in coord or "y" not in coord:
                continue

            x = int(coord["x"] * width)
            y = int(coord["y"] * height)

            points[joint_name] = (x, y)

            # Green circle for joint
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        # Draw bones (connections)
        for start, end in bones:
            j1 = f"joint_{start}"
            j2 = f"joint_{end}"

            if j1 in points and j2 in points:
                cv2.line(
                    frame,
                    points[j1],
                    points[j2],
                    (255, 255, 255),
                    2
                )

        out.write(frame)

    out.release()

    print(f"Stick figure video saved at: {output_video_path}")

    return str(output_video_path)