from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from app.utils.logger import get_logger
from app.services.authentication import (
    get_current_user
)
from app.api.handler.documents import (
    handle_file_upload
)

logger = get_logger()

router = APIRouter(prefix="/docs", tags=["Document Upload"])



@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_files(file: UploadFile = File(...),current_user: dict = Depends(get_current_user)):
    logger.info("Registration request received")
    try:
        if not current_user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized User"
        )
        response = await handle_file_upload(file,current_user)
        return response
    except HTTPException as e:
        logger.warning(f"File Upload Failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during Upload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )