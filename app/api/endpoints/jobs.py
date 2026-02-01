from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.logger import get_logger
from app.api.handler.jobs import list_companies
from app.services.authentication import (
    get_current_user
)

logger = get_logger()
router = APIRouter(prefix="/jobs", tags=["Job Details"])

@router.get("/companies", status_code=status.HTTP_201_CREATED)
async def list_all_companies(current_user: dict = Depends(get_current_user)
):

    try:
        if not current_user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized User"
        )

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