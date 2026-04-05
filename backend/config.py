import os

class Settings:
    PROJECT_NAME: str = "RoomieMatch Pro"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./roomiematch.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-roomie-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

settings = Settings()
