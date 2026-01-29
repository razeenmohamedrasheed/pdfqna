from fastapi import APIRouter, HTTPException, status
from app.utils.logger import get_logger
from app.schemas.schemas import Login
from app.api.handler.login import user_login

logger = get_logger()

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def user_registration(payload: Login):
    logger.info("Registration request received")
    try:
        response = await user_login(payload)
        return response
    except HTTPException as e:
        logger.warning(f"login failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during Login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
