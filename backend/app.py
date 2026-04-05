import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.database import engine, Base, SessionLocal
from backend.routes import auth, profile, matches, chat, agreement
from backend.services.seeder import seed_database
from backend.config import settings

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed data
    with SessionLocal() as db:
        seed_database(db)
        
    yield
    # Shutdown logic if any

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(matches.router)
app.include_router(chat.router)
app.include_router(agreement.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
