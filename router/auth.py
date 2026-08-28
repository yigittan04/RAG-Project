from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from security import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

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

@router.post("/login")
def login(
    req: LoginRequest,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(
        db=db,
        email=req.email
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        req.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive."
        )

    crud.update_last_login(
        db=db,
        user=user
    )

    access_token = create_access_token(
        user_id=str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin
    }