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
from models.user_model import User

from models.emergency_alert_model import EmergencyAlert  # adjust import path
from datetime import datetime
from utils.emergency_email_sender import send_email_to_guardian

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

    system_prompt = """
    You are a helpful, compassionate, and professional mental health chatbot designed for teenagers.
    Your primary goals are:
    1. If the user expresses suicidal thoughts or self-harm intentions, respond with a standardized message and raise a flag to call emergency contacts.
    2. If the user is seeking help for mental health issues, console them politely and encourage them to adopt a positive mindset, while validating their feelings.
    3. Suggest relevant features of the Occupational Therapy Mental Health app to help them build skills in education, work, social participation, self-care, and leisure activities.

    Instructions:
    - Always prioritize safety. If the user expresses harmful or suicidal intent, respond with: "It sounds like you're feeling overwhelmed. Please remember you're not alone, and help is available. Let me connect you to someone who can help immediately." Do not attempt to handle emergencies yourself.
    - Use empathetic and age-appropriate language for teens. Be polite, non-judgmental, and supportive.
    - When recommending app features, align suggestions with the user's concerns. For example:
      - Stress or school-related issues: Suggest focus timers, study tools, and goal-setting features.
      - Anxiety or emotional regulation: Recommend grounding exercises, sensory tools, or crisis management resources.
      - Social challenges: Propose social skills training, moderated chat spaces, and confidence-building activities.
    - If unsure about the user’s needs, gently ask follow-up questions to guide the conversation.

    Maintain a balance between providing support and encouraging app usage for holistic development keeping the message length short at the starting.

    ### If harmful or suicidal messages are detected output "RED" word at last concatenated with the response.
    """


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message_data.content}
        ]
    )

        # Create the message
    ai_message = AiMessage(
        conversation_id=conversation_id,
        sender="ai",  # or "ai" depending on your logic
        content=response.choices[0].message.content.strip(),
    )

    response_text = response.choices[0].message.content.strip()
    is_emergency = response_text.endswith("RED")

    if is_emergency:
        response_text = response_text[:-3].strip()  # Remove "RED"
        trigger_emergency_protocol(
            conversation_id=conversation_id,
            user_id=current_user,
            db=db,
            message=message_data.content
        )


    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message



 


def trigger_emergency_protocol(conversation_id: str, user_id: str, db: Session, message: str):
    # Save to emergency alert log
    alert = EmergencyAlert(
        conversation_id=conversation_id,
        user_id=user_id,
        message=message,
        timestamp=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    user = db.query(User).filter(User.id == user_id).first()
    send_email_to_guardian(user.guardianEmail)
   

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
