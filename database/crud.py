from sqlalchemy.orm import Session

from .models import (
    User,
    Conversation,
    Message,
    Document,
    Chunk,
    RetrievalLog
)

# ___
def create_user()

def get_user_by_email()

def get_user_by_username()

def update_last_login()



# ____

def create_conversation(
    db: Session,
    user_id=None,
    title=None
):
    conversation = Conversation(
        user_id=user_id,
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

def get_conversation(
    db: Session,
    conversation_id
):
    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

def get_user_conversations(
    db: Session,
    user_id
):
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

def archive_conversation(
    db: Session,
    conversation_id
):
    conversation = get_conversation(
        db,
        conversation_id
    )

    if conversation is None:
        return None

    conversation.is_archived = True

    db.commit()
    db.refresh(conversation)

    return conversation


# _____

def create_message(
    db: Session,
    conversation_id,
    role,
    content
):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_messages(
    db: Session,
    conversation_id
):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

def get_message(
    db: Session,
    message_id
):
    return (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )

#___

def create_document()

def get_document()

def get_documents()

#______


def create_chunk()

def get_chunks()


# ____




def create_retrieval_log()