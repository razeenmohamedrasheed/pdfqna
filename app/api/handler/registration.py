from fastapi import HTTPException, status
from app.db.database import Database
from app.utils.password import HashPassword
from app.utils.logger import get_logger
from app.config.constants import SUCCESS, FAIL

logger = get_logger()

async def register_user(data):
    logger.info("Starting user registration flow")
    try:
        db = Database()

        if db.check_email_or_contact_exists(data.email, data.contact):
            logger.warning("User already exists (email/contact)")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        pwd = HashPassword()
        hashed_password = pwd.get_password_hash(data.password)
        logger.debug("Password hashed successfully")

        user_data = {
            "email": data.email,
            "contact": data.contact,
            "hashed_password": hashed_password,
            "role_id": data.role_id
        }

        user_id = db.insert_user_data(user_data)

        if not user_id:
            logger.error("User insertion failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User creation failed"
            )

        logger.info(f"User registered successfully | user_id={user_id}")

        return {
            "status": SUCCESS,
            "message": "User registration successful",
            "data": {
                "user_id": user_id
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in registration handler")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
