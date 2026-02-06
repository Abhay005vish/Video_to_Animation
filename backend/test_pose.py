from pose_extraction.extract_pose import extract_pose_from_video

video_path = "../storage/uploads/raw_videos/7c06130c-e2dc-4c77-863b-de3d7cc76bed.mp4"
output_path = "../storage/motion_data/7c06130c-e2dc-4c77-863b-de3d7cc76bed.json"
extract_pose_from_video(video_path, output_path)
print("Pose extraction completed")
