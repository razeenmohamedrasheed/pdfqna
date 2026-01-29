import os 
from fastapi import HTTPException, status
from datetime import timedelta
from app.db.database import Database
from app.utils.password import HashPassword
from app.utils.logger import get_logger
from app.config.constants import SUCCESS, FAIL
from dotenv import load_dotenv
from app.services.authentication import (
    create_access_token
)

logger = get_logger()
load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
print("token--------->",type(ACCESS_TOKEN_EXPIRE_MINUTES))

async def user_login(data):
    logger.info("Starting user registration flow")
    try:
        db = Database()
        pwd = HashPassword()
        user = db.get_user_by_email(data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )
        id, hashed_password = user

        if not pwd.verify_password(data.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Password"
            )
        access_token = create_access_token(
                        data={
                        "sub": id,  
                        "email": data.email
                    },
                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in registration handler")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

