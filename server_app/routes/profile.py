from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server_app.models.database import get_db
from server_app.models.entities import User
from server_app.schemas.schemas import UserResponse, UserProfileUpdate
from server_app.routes.auth import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("", response_model=UserResponse)
def update_profile(profile_data: UserProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user
