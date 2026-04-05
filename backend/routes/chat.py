from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.models.database import get_db
from backend.models.entities import User, CommunityMessage, PrivateMessage
from backend.schemas.schemas import CommunityMessageResponse, CommunityMessageCreate, PrivateMessageResponse, PrivateMessageCreate
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/api", tags=["chat"])

# Community Chat
@router.get("/community/messages", response_model=List[CommunityMessageResponse])
def get_community_messages(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    messages = db.query(CommunityMessage).order_by(CommunityMessage.timestamp.desc()).offset(skip).limit(limit).all()
    return messages

@router.post("/community/messages", response_model=CommunityMessageResponse)
def post_community_message(
    msg: CommunityMessageCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_msg = CommunityMessage(
        author_id=current_user.id,
        author_name=current_user.full_name,
        text=msg.text
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# Private Chat
@router.get("/chat/{roommate_id}/messages", response_model=List[PrivateMessageResponse])
def get_private_messages(
    roommate_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Chat key is always sorted pair of IDs
    key_prefix = f"user_{min(current_user.id, roommate_id)}_{max(current_user.id, roommate_id)}"
    
    messages = db.query(PrivateMessage).filter(PrivateMessage.chat_key == key_prefix).order_by(PrivateMessage.timestamp.asc()).all()
    return messages

@router.post("/chat/{roommate_id}/messages", response_model=PrivateMessageResponse)
def post_private_message(
    roommate_id: int, 
    msg: PrivateMessageCreate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    key_prefix = f"user_{min(current_user.id, roommate_id)}_{max(current_user.id, roommate_id)}"
    
    new_msg = PrivateMessage(
        sender_id=current_user.id,
        receiver_id=roommate_id,
        receiver_is_seeded=1 if msg.receiver_is_seeded else 0,
        text=msg.text,
        chat_key=key_prefix
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg
