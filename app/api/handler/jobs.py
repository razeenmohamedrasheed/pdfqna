from fastapi import HTTPException, status
from app.utils.logger import get_logger
from app.db.database import Database

logger = get_logger()
async def list_companies():
    try:
        db = Database()
        companies = db.list_all_companies()
        return {
            "message": "success",
            "data" : companies
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in registration handler")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )