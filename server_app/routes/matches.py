from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from server_app.models.database import get_db
from server_app.models.entities import User, RoommateRecord
from server_app.schemas.schemas import RoommateMatchResponse
from server_app.routes.auth import get_current_user
from server_app.services.matching import calculate_compatibility

router = APIRouter(prefix="/api/matches", tags=["matches"])

@router.get("", response_model=List[RoommateMatchResponse])
def get_matches(
    room_preference: Optional[str] = Query(None),
    personality: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(RoommateRecord)
    
    if room_preference:
        query = query.filter(RoommateRecord.room_preference == room_preference)
    if personality:
        query = query.filter(RoommateRecord.personality == personality)
        
    candidates = query.all()
    
    from server_app.services.ai_service import calculate_ai_compatibility
    
    matches = []
    for candidate in candidates:
        candidate_dict = candidate.__dict__.copy()
        if "_sa_instance_state" in candidate_dict:
            del candidate_dict["_sa_instance_state"]
            
        # Try AI match if key is present
        score = calculate_ai_compatibility(current_user.__dict__, candidate_dict)
        
        # Fallback to local matching if AI fails or no key
        if score == 0:
            score = calculate_compatibility(current_user, candidate)
            
        candidate_dict['compatibility_score'] = score
        matches.append(candidate_dict)
        
    # Sort descending by score
    matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
    
    return matches[:limit]
