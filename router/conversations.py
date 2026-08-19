from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.get("/")
def get_conversations(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    conversations = crud.get_user_conversations(
        db=db,
        user_id=user_id
    )

    return conversations