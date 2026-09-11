from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.database import get_db
from database import crud

import os

load_dotenv()

security = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY environment variable is not set."
    )


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    user_id: str
) -> str:

    payload = {
        "sub": user_id
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    user = crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive."
        )

    return user