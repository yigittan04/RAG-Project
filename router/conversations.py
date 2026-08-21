from pydantic import BaseModel
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

class ConversationCreate(BaseModel):
    user_id: UUID
    title: str | None = None

@router.post("")
def create_conversation(
    req: ConversationCreate,
    db: Session = Depends(get_db)
):
    conversation = crud.create_conversation(
        db=db,
        user_id=req.user_id,
        title=req.title
    )

    return conversation


@router.get("")
def get_conversations(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    conversations = crud.get_user_conversations(
        db=db,
        user_id=user_id
    )

    return conversations

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    conversation = crud.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return conversation


@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    conversation = crud.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    messages = crud.get_messages(
        db=db,
        conversation_id=conversation_id
    )

    return messages

@router.patch("/{conversation_id}/archive")
def archive_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    conversation = crud.archive_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    return conversation
