import cv2
import json
from pathlib import Path

try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
except Exception as e:
    raise RuntimeError(
        "MediaPipe broken or missing. Install with: pip install mediapipe==0.10.9"
    ) from e


def extract_pose_from_video(video_path, output_json_path):

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    all_frames = {}
    frame_idx = 0

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            frame_data = {}
            if results.pose_landmarks:
                for i, lm in enumerate(results.pose_landmarks.landmark):
                    frame_data[f"joint_{i}"] = {
                        "x": float(lm.x),
                        "y": float(lm.y),
                        "z": float(lm.z),
                        "visibility": float(lm.visibility)
                    }

            all_frames[f"frame_{frame_idx}"] = frame_data
            frame_idx += 1

    cap.release()

    Path(output_json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, "w") as f:
        json.dump(all_frames, f, indent=2)

    return output_json_path
