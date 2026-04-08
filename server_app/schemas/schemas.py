from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserProfileUpdate(BaseModel):
    profession: Optional[str] = None
    sleep_pattern: Optional[str] = None
    personality: Optional[str] = None
    cleanliness: Optional[str] = None
    noise_tolerance: Optional[str] = None
    room_preference: Optional[str] = None
    bedtime: Optional[str] = None
    wake_time: Optional[str] = None
    sleep_type: Optional[str] = None
    social_energy_rating: Optional[int] = None

class UserResponse(UserBase, UserProfileUpdate):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class RoommateRecordResponse(BaseModel):
    id: int
    full_name: Optional[str]
    profession: Optional[str]
    sleep_pattern: Optional[str]
    personality: Optional[str]
    cleanliness: Optional[str]
    noise_tolerance: Optional[str]
    room_preference: Optional[str]
    bedtime: Optional[str]
    wake_time: Optional[str]
    sleep_type: Optional[str]
    social_energy_rating: Optional[int]

    class Config:
        from_attributes = True

class RoommateMatchResponse(RoommateRecordResponse):
    compatibility_score: float

class CommunityMessageCreate(BaseModel):
    text: str

class CommunityMessageResponse(BaseModel):
    id: int
    author_id: Optional[int]
    author_name: str
    text: str
    timestamp: datetime

    class Config:
        from_attributes = True

class PrivateMessageCreate(BaseModel):
    text: str
    receiver_is_seeded: bool = True

class PrivateMessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    receiver_is_seeded: int
    text: str
    timestamp: datetime
    chat_key: str

    class Config:
        from_attributes = True
