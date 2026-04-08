from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from backend.models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    
    profession = Column(String)
    sleep_pattern = Column(String)
    personality = Column(String)
    cleanliness = Column(String)
    noise_tolerance = Column(String)
    room_preference = Column(String)
    bedtime = Column(String)
    wake_time = Column(String)
    sleep_type = Column(String)
    social_energy_rating = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class RoommateRecord(Base):
    __tablename__ = "roommate_records"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    profession = Column(String)
    sleep_pattern = Column(String)
    personality = Column(String)
    cleanliness = Column(String)
    noise_tolerance = Column(String)
    room_preference = Column(String)
    bedtime = Column(String)
    wake_time = Column(String)
    sleep_type = Column(String)
    social_energy_rating = Column(Integer)

class CommunityMessage(Base):
    __tablename__ = "community_messages"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author_name = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class PrivateMessage(Base):
    __tablename__ = "private_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer) # Can be a User or RoommateRecord
    receiver_is_seeded = Column(Integer, default=1) # 1 if receiver is from roommate_records
    text = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    chat_key = Column(String, index=True) # derived from min/max of ids, prefixed by type
