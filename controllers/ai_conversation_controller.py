from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database.database import get_db
from models.ai_conversation_model import AiConversation,AiMessage
from schemas.ai_conversation_schema import AiConversationCreate, AiConversationResponse,AiMessageCreate, AiMessageResponse
from middleware.auth_middleware import get_current_user
from typing import List
import openai
from settings import settings

router = APIRouter(prefix="/aiconversations", tags=["AIConversations"])


client = openai.OpenAI(api_key=settings.OPENAI_KEY)  # or use os.environ.get("OPENAI_API_KEY")


# Get all conversations for current user
@router.get("/", response_model=List[AiConversationResponse])
def get_user_conversations(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    conversations = db.query(AiConversation).filter(
        AiConversation.user_id == current_user
    ).order_by(AiConversation.created_at.desc()).all()
    return conversations



@router.post("/", response_model=AiConversationResponse)
def create_conversation(
    conversation_data: AiConversationCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_convo = AiConversation(
        name=conversation_data.name,
        user_id=current_user,
    )
    db.add(new_convo)
    db.commit()
    db.refresh(new_convo)
    return new_convo


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    convo = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == current_user
    ).first()

    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(convo)
    db.commit()


@router.post("/{conversation_id}/messages", response_model=AiMessageResponse)
def send_message(
    conversation_id: UUID,
    message_data: AiMessageCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Check if conversation exists and belongs to the user
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == current_user
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Create the message
    new_message = AiMessage(
        conversation_id=conversation_id,
        sender="user",  # or "ai" depending on your logic
        content=message_data.content,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message_data.content}
        ]
    )

        # Create the message
    ai_message = AiMessage(
        conversation_id=conversation_id,
        sender="ai",  # or "ai" depending on your logic
        content=response.choices[0].message.content.strip(),
    )

    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message


# Get all messages in a conversation (only if user owns it)
@router.get("/{conversation_id}/messages", response_model=List[AiMessageResponse])
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == current_user
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation.messages
