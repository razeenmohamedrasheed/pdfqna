from fastapi import APIRouter, HTTPException, status
from app.utils.logger import get_logger
from app.api.handler.jobs import list_companies

logger = get_logger()
router = APIRouter(prefix="/jobs", tags=["Job Details"])

@router.get("/companies", status_code=status.HTTP_201_CREATED)
async def list_all_companies():

    try:
        response = await list_companies()
        return response
    except HTTPException as e:
        logger.warning(f"list companies failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during listting")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )