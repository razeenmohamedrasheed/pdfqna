from datetime import datetime, timedelta 
from fastapi.security import OAuth2PasswordBearer
from app.utils.logger import get_logger
from fastapi import HTTPException, status, Depends
from dotenv import load_dotenv
from jose import jwt, JWTError
import os

logger = get_logger()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    logger.debug(f"JWT CREATE SECRET: {SECRET_KEY}")
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str):
    try:
        logger.debug(f"JWT VERIFY SECRET: {SECRET_KEY}")
        logger.debug(f"TOKEN repr: {repr(token)}")
        logger.debug(f"TOKEN length: {len(token)}")
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return {
        "user_id": user_id
    }