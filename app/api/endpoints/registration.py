from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import Registration
from app.api.handler.registration import register_user
from app.utils.logger import get_logger

logger = get_logger()

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def user_registration(payload: Registration):
    logger.info("Registration request received")
    try:
        response = await register_user(payload)
        return response
    except HTTPException as e:
        logger.warning(f"Registration failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during registration")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
