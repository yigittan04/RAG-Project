from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .models import (
    User,
    Conversation,
    Message,
    Document,
    Chunk,
    RetrievalLog
)


def create_user(
    db: Session,
    username,
    email,
    hashed_password
):
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(
    db: Session,
    email
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def get_user_by_username(
    db: Session,
    username
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

def update_last_login(
    db: Session,
    user: User
):
    user.last_login = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    return user



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



def create_document(
    db: Session,
    filename,
    uploaded_by,
    total_chunks,
    file_size,
    mime_type,
    storage_path,
    file_hash,
    status="processed"
):
    document = Document(
        filename=filename,
        uploaded_by=uploaded_by,
        total_chunks=total_chunks,
        file_size=file_size,
        mime_type=mime_type,
        storage_path=storage_path,
        file_hash=file_hash,
        status=status
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def get_document(
    db: Session,
    document_id
):
    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

def get_documents(
    db: Session,
    user_id
):
    return (
        db.query(Document)
        .filter(Document.uploaded_by == user_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )

def get_document_by_hash(
    db: Session,
    file_hash
):
    return (
        db.query(Document)
        .filter(Document.file_hash == file_hash)
        .first()
    )



def create_chunk()

def get_chunks()


# ____




def create_retrieval_log()