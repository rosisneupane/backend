from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database.database import get_db
from models.conversation_model import Conversation
from models.user_model import User
from schemas.conversation_schema import ConversationCreate,ConversationResponse
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user),
):
    """Creates a new conversation with users"""
    # Ensure the creator is included in the user list
    user_ids = set(conversation_data.user_ids) if conversation_data.user_ids else set()
    user_ids.add(current_user)  # Add creator ID

    users = db.query(User).filter(User.id.in_(user_ids)).all()
    print(users)

    if not users:
        raise HTTPException(status_code=400, detail="No valid users provided")

    new_conversation = Conversation(
        name=conversation_data.name,
        details=conversation_data.details,
        created_by=current_user,
        users=users  # Assigning users to conversation
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return ConversationResponse(
        id=new_conversation.id,
        name=new_conversation.name,
        details=new_conversation.details,
        created_by=new_conversation.created_by,
        created_at=new_conversation.created_at,
        user_ids=[user.id for user in new_conversation.users]  # Extract user IDs
    )


@router.get("/", response_model=list[ConversationResponse])
def get_all_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves all conversations"""
    conversations = db.query(Conversation).all()

    return [
        ConversationResponse(
            id=conv.id,
            name=conv.name,
            details=conv.details,
            created_by=conv.created_by,
            created_at=conv.created_at,
            user_ids=[user.id for user in conv.users]  # Extract user IDs
        )
        for conv in conversations
    ]


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves a single conversation by ID"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        details=conversation.details,
        created_by=conversation.created_by,
        created_at=conversation.created_at,
        user_ids=[user.id for user in conversation.users]  # Extract user IDs
    )


# Delete a conversation (Only creator can delete)
@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Deletes a conversation if the user is the creator"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.created_by != current_user:
        raise HTTPException(status_code=403, detail="Only the creator can delete this conversation")

    db.delete(conversation)
    db.commit()
    return {"message": "Conversation deleted successfully"}
