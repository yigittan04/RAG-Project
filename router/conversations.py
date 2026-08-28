from pydantic import BaseModel
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from security import get_current_user
from database.models import User
from database.database import get_db
from database import crud

router = APIRouter(
prefix="/conversations",
tags=["Conversations"]
)

class ConversationCreate(BaseModel):
    title: str | None = None

@router.post("")
def create_conversation(
    req: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    conversation = crud.create_conversation(
        db=db,
        user_id=current_user.id,
        title=req.title
    )

    return conversation


@router.get("")
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    conversations = crud.get_user_conversations(
        db=db,
        user_id=current_user.id
    )

    return conversations


@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this conversation."
        )

    return conversation


@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this conversation."
        )

    messages = crud.get_messages(
        db=db,
        conversation_id=conversation_id
    )

    return messages


@router.patch("/{conversation_id}/archive")
def archive_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this conversation."
        )

    conversation = crud.archive_conversation(
        db=db,
        conversation_id=conversation_id
    )

    return conversation
