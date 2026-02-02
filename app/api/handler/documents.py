from fastapi import HTTPException, status
from app.utils.logger import get_logger
import os

logger = get_logger()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_file_upload(file,current_user):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "uploaded_by": current_user["user_id"]
        }

    except Exception as e:
        logger.exception("Unexpected error during Upload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )