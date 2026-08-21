from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register")
def register(
    req: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_email = crud.get_user_by_email(
        db=db,
        email=req.email
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered."
        )

    existing_username = crud.get_user_by_username(
        db=db,
        username=req.username
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=409,
            detail="Username is already taken."
        )

    hashed_password = hash_password(
        req.password
    )

    user = crud.create_user(
        db=db,
        username=req.username,
        email=req.email,
        hashed_password=hashed_password
    )

    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }