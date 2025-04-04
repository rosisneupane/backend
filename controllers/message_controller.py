from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from models.conversation_model import Message
from models.conversation_model import Conversation
from models.user_model import User
from database.database import get_db
from schemas.message_schema import MessageCreate, MessageResponse
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=MessageResponse)
def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Make sure this is a User object
):
    """Send a message to a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == message_data.conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if current_user not in [user.id for user in conversation.users]:
        raise HTTPException(status_code=403, detail="You are not a participant in this conversation")

    new_message = Message(
        conversation_id=message_data.conversation_id,
        sender_id=current_user,
        content=message_data.content,
        timestamp=datetime.utcnow()
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message  # Automatically mapped by MessageResponse with orm_mode


@router.get("/conversation/{conversation_id}", response_model=list[MessageResponse])
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all messages of a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if current_user not in [user.id for user in conversation.users]:
        raise HTTPException(status_code=403, detail="You are not a participant in this conversation")

    # Eager load sender relationship to avoid N+1 queries
    from sqlalchemy.orm import selectinload
    messages = db.query(Message)\
        .options(selectinload(Message.sender))\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.timestamp).all()

    return messages  # Automatically serialized using MessageResponse

