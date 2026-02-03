import uuid
import shutil
from fastapi import UploadFile, File, APIRouter, HTTPException

router = APIRouter()

UPLOAD_DIR = "../storage/uploads/raw_videos"

@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 videos are allowed")

    video_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Video uploaded successfully",
        "video_id": video_id,
        "file_path": file_path
    }
