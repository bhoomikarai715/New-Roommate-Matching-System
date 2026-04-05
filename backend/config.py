from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RoomieMatch Pro"
    # Essential production overrides via Environment Variables:
    DATABASE_URL: str = "sqlite:///./roomiematch.db" # Default for local
    SECRET_KEY: str = "super-secret-roomie-key-override-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    class Config:
        env_file = ".env"

settings = Settings()
